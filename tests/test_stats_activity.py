from datetime import UTC, datetime, timedelta

from app.models import AuditLog
from tests.conftest import make_doc


def test_activity_has_30_days_oldest_first_ending_today(client):
    activity = client.get("/api/stats").json()["activity"]
    assert len(activity) == 30
    today = datetime.now(UTC).date()
    assert activity[-1]["date"] == today.isoformat()
    assert activity[0]["date"] == (today - timedelta(days=29)).isoformat()
    assert all(day["count"] == 0 for day in activity)


def test_activity_counts_audit_entries_of_today(client):
    doc = make_doc(client)
    client.patch(f"/api/documents/{doc['id']}", json={"title": "Neuer Titel"})
    assert client.get("/api/stats").json()["activity"][-1]["count"] == 2


def test_activity_ignores_entries_older_than_30_days(client, db_session):
    db_session.add(
        AuditLog(action="create", detail="alt", timestamp=datetime.now(UTC) - timedelta(days=31))
    )
    db_session.commit()
    assert sum(d["count"] for d in client.get("/api/stats").json()["activity"]) == 0


def test_activity_counts_entry_from_yesterday_on_its_day(client, db_session):
    db_session.add(
        AuditLog(action="create", detail="gestern", timestamp=datetime.now(UTC) - timedelta(days=1))
    )
    db_session.commit()
    activity = client.get("/api/stats").json()["activity"]
    assert activity[-2]["count"] == 1
    assert activity[-1]["count"] == 0
