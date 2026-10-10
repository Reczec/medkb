import jwt
import pytest

from app.auth import create_token, decode_token, hash_password, verify_password
from app.config import Settings
from app.models import User


def settings(**overrides) -> Settings:
    return Settings(_env_file=None, jwt_secret="unit-test-secret-with-32-bytes-ok!", **overrides)


def make_user() -> User:
    return User(id=7, username="dr", password_hash="x", role="doctor", display_name="Dr. Demo")


# ------------------------------------------------------------------------ helpers


def test_password_roundtrip():
    hashed = hash_password("geheim123")
    assert hashed != "geheim123"
    assert verify_password("geheim123", hashed)
    assert not verify_password("falsch", hashed)


def test_token_roundtrip_carries_id_and_role():
    claims = decode_token(create_token(make_user(), settings()), settings())
    assert claims["sub"] == "7"
    assert claims["role"] == "doctor"


def test_expired_token_is_rejected():
    token = create_token(make_user(), settings(jwt_hours=-1))
    with pytest.raises(jwt.InvalidTokenError):
        decode_token(token, settings())


def test_token_signed_with_other_secret_is_rejected():
    token = create_token(
        make_user(), Settings(_env_file=None, jwt_secret="another-secret-that-is-32-bytes-long")
    )
    with pytest.raises(jwt.InvalidTokenError):
        decode_token(token, settings())
