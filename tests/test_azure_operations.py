"""Bounded health verification and cleanup never target unrelated resources."""

import io
import json
from urllib.error import HTTPError

import pytest

from scripts.azure import cleanup, smoke


def test_health_refuses_insecure_or_credential_urls():
    for url in (
        "http://demo.azurecontainerapps.io",
        "https://user:password@demo.azurecontainerapps.io",
        "https://demo.azurecontainerapps.io/?key=secret",
    ):
        with pytest.raises(ValueError):
            smoke.check_health(url)


def test_health_accepts_real_status_contract(monkeypatch):
    monkeypatch.setattr(
        smoke.urllib.request,
        "urlopen",
        lambda request, timeout: io.BytesIO(json.dumps({"status": "ok"}).encode()),
    )
    smoke.check_health("https://demo.azurecontainerapps.io")


def test_repeated_503_has_bounded_timeout(monkeypatch):
    clock = [0]
    monkeypatch.setattr(smoke.time, "monotonic", lambda: clock[0])
    monkeypatch.setattr(
        smoke.time, "sleep", lambda seconds: clock.__setitem__(0, clock[0] + seconds)
    )

    def unavailable(request, timeout):
        raise HTTPError(request.full_url, 503, "Unavailable", {}, None)

    monkeypatch.setattr(smoke.urllib.request, "urlopen", unavailable)
    with pytest.raises(ValueError, match="timed out"):
        smoke.check_health("https://demo.azurecontainerapps.io", timeout_seconds=12)
    assert clock[0] == 12


@pytest.mark.parametrize(
    "actual,expected,group,expected_group",
    [
        ("other", "expected", "medkb-azure-demo-test", "medkb-azure-demo-test"),
        ("expected", "expected", "medkb-azure-demo-other", "medkb-azure-demo-test"),
        ("expected", "expected", "production", "production"),
    ],
)
def test_cleanup_refuses_wrong_target(actual, expected, group, expected_group):
    with pytest.raises(ValueError):
        cleanup.validate_cleanup_target(actual, expected, group, expected_group)


def test_preview_and_wrong_confirmation_never_delete(monkeypatch):
    calls = []

    def azure(arguments):
        calls.append(arguments)
        if arguments[:2] == ["account", "show"]:
            return {"id": "expected"}
        if arguments[:2] == ["group", "show"]:
            return {"tags": {"project": "medkb-azure-demo"}}
        if arguments[:2] == ["resource", "list"]:
            return []
        pytest.fail("Deletion must not be called")

    monkeypatch.setattr(cleanup, "az_json", azure)
    monkeypatch.setattr("builtins.input", lambda prompt: "wrong-group")
    cleanup.cleanup_group(
        "expected", "expected", "medkb-azure-demo-test", "medkb-azure-demo-test", delete=False
    )
    with pytest.raises(ValueError, match="confirmation"):
        cleanup.cleanup_group(
            "expected", "expected", "medkb-azure-demo-test", "medkb-azure-demo-test", delete=True
        )
    assert all(arguments[:2] != ["group", "delete"] for arguments in calls)


def test_revision_cannot_pass_for_old_ready_image(monkeypatch):
    clock = [0]
    monkeypatch.setattr(smoke.time, "monotonic", lambda: clock[0])
    monkeypatch.setattr(
        smoke.time, "sleep", lambda seconds: clock.__setitem__(0, clock[0] + seconds)
    )
    monkeypatch.setattr(
        smoke,
        "az_json",
        lambda arguments, **kwargs: {
            "properties": {
                "latestRevisionName": "new",
                "latestReadyRevisionName": "old",
                "provisioningState": "Succeeded",
                "template": {"containers": [{"image": "new-image"}]},
            }
        },
    )
    with pytest.raises(ValueError, match="revision"):
        smoke.check_deployment(
            "subscription", "medkb-azure-demo-test", "demo", "new-image", timeout_seconds=12
        )


def test_revision_cli_timeout_cannot_exceed_remaining_poll_budget(monkeypatch):
    def show(arguments, *, timeout_seconds):
        assert 0 < timeout_seconds <= 12
        return {
            "properties": {
                "latestRevisionName": "new",
                "latestReadyRevisionName": "new",
                "provisioningState": "Succeeded",
                "template": {"containers": [{"image": "new-image"}]},
                "configuration": {"ingress": {"fqdn": "demo.azurecontainerapps.io"}},
            }
        }

    monkeypatch.setattr(smoke, "az_json", show)
    monkeypatch.setattr(smoke, "check_health", lambda url, timeout_seconds: None)
    assert (
        smoke.check_deployment(
            "subscription", "medkb-azure-demo-test", "demo", "new-image", timeout_seconds=12
        )
        == "https://demo.azurecontainerapps.io"
    )
