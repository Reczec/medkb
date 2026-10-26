from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime

import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.ai import store
from app.database import Base, make_engine
from app.demo import reset_demo
from app.models import AIUsage


def test_cache_identity_changes_with_every_context_dimension(test_settings):
    key = store.cache_key("explain", 1, {"content": "original"}, "patient", test_settings)
    assert len(key) == 64
    assert key != store.cache_key("explain", 1, {"content": "edited"}, "patient", test_settings)
    assert key != store.cache_key("explain", 1, {"content": "original"}, "doctor", test_settings)
    assert key != store.cache_key("summary", 1, {"content": "original"}, "patient", test_settings)
    assert key != store.cache_key("explain", 2, {"content": "original"}, "patient", test_settings)
    test_settings.ai_model = "other"
    assert key != store.cache_key("explain", 1, {"content": "original"}, "patient", test_settings)
    test_settings.ai_model = "gemini-3.5-flash-lite"
    test_settings.ai_base_url = "https://other.example"
    assert key != store.cache_key("explain", 1, {"content": "original"}, "patient", test_settings)


def test_cache_roundtrip_duplicate_and_reset(db_session, test_settings):
    assert store.read_cache(db_session, "key") is None
    store.write_cache(db_session, "key", "explain", 1, test_settings, {"text": "first"})
    store.write_cache(db_session, "key", "explain", 1, test_settings, {"text": "second"})
    reset_demo(db_session)
    assert store.read_cache(db_session, "key") == {"text": "second"}


def test_client_quota_stops_at_exact_limit_and_rolls_back_global(db_session, test_settings):
    for _ in range(30):
        store.reserve(db_session, "client", test_settings, "de")
    with pytest.raises(HTTPException) as error:
        store.reserve(db_session, "client", test_settings, "de")
    assert error.value.status_code == 429
    assert int(error.value.headers["Retry-After"]) > 0
    assert store.usage_today(db_session) == 30


def test_global_quota_does_not_increment_other_client(db_session, test_settings):
    test_settings.ai_daily_limit = 1
    store.reserve(db_session, "first", test_settings, "de")
    with pytest.raises(HTTPException):
        store.reserve(db_session, "second", test_settings, "de")
    assert store.usage_today(db_session) == 1
    row = db_session.get(AIUsage, ("second", store.day()))
    assert row is None or row.count == 0


def test_quota_resets_at_utc_day_boundary(db_session, test_settings, monkeypatch):
    monkeypatch.setattr(store, "utcnow", lambda: datetime(2026, 10, 11, 23, 59, 59, tzinfo=UTC))
    test_settings.ai_client_daily_limit = 1
    store.reserve(db_session, "client", test_settings, "de")
    with pytest.raises(HTTPException) as error:
        store.reserve(db_session, "client", test_settings, "de")
    assert error.value.headers["Retry-After"] == "1"
    monkeypatch.setattr(store, "utcnow", lambda: datetime(2026, 10, 12, tzinfo=UTC))
    assert store.usage_today(db_session) == 0
    store.reserve(db_session, "client", test_settings, "de")
    assert store.usage_today(db_session) == 1


def test_client_identity_is_hashed_and_salted(test_settings):
    identity = store.client_identity("127.0.0.1", test_settings)
    assert len(identity) == 64 and "127.0.0.1" not in identity
    test_settings.jwt_secret = "another-secret"
    assert identity != store.client_identity("127.0.0.1", test_settings)


def test_parallel_last_slot_is_reserved_only_once(tmp_path, test_settings):
    target = make_engine(f"sqlite:///{tmp_path / 'quota.db'}")
    Base.metadata.create_all(target)
    test_settings.ai_daily_limit = 1

    def attempt(name):
        with Session(target) as db:
            try:
                store.reserve(db, name, test_settings, "de")
                return True
            except HTTPException:
                return False

    try:
        with ThreadPoolExecutor(2) as pool:
            assert sorted(pool.map(attempt, ["first", "second"])) == [False, True]
        with Session(target) as db:
            assert store.usage_today(db) == 1
    finally:
        target.dispose()
