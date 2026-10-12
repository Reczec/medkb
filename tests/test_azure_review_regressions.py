"""Actual operator boundaries identified by the independent Azure review."""

import json
import os
import subprocess
from types import SimpleNamespace

import pytest

from scripts.azure import deploy, preflight

SUBSCRIPTION = "670958af-a1c1-4b8a-8fc9-0aa868ff8b44"


@pytest.mark.parametrize("key", ["dbname", "host", "user", "password", "service", "options"])
def test_database_query_cannot_override_isolated_target(key):
    with pytest.raises(ValueError):
        deploy.validate_database_url(
            f"postgresql+psycopg://isolated:secret@host/medkb_azure?sslmode=require&{key}=neondb"
        )


def test_cli_disables_persistent_logging_even_when_parent_enables_it(monkeypatch):
    monkeypatch.setenv("AZURE_LOGGING_ENABLE_LOG_FILE", "true")
    monkeypatch.setattr(preflight.shutil, "which", lambda name: "/tools/az")

    def fail(command, **kwargs):
        assert kwargs["env"]["AZURE_LOGGING_ENABLE_LOG_FILE"] == "false"
        return SimpleNamespace(returncode=1, stderr="private-key", stdout="private-key")

    monkeypatch.setattr(preflight.subprocess, "run", fail)
    with pytest.raises(ValueError) as error:
        preflight.az_json(["containerapp", "secret", "list"])
    assert "private-key" not in str(error.value)


def test_windows_cli_runs_python_without_batch_shell(monkeypatch, tmp_path):
    root = tmp_path / "tools&safe"
    (root / "bin").mkdir(parents=True)
    (root / "python.exe").touch()
    monkeypatch.setattr(preflight.shutil, "which", lambda name: str(root / "bin/az.cmd"))
    seen = []
    monkeypatch.setattr(
        preflight.subprocess,
        "run",
        lambda command, **kwargs: (
            seen.append(command) or SimpleNamespace(returncode=0, stdout="{}")
        ),
    )
    preflight.az_json(["version"])
    assert seen[0][:4] == [str(root / "python.exe"), "-IBm", "azure.cli", "version"]


def test_subscription_shell_metacharacters_rejected_before_cli(monkeypatch):
    monkeypatch.setattr(preflight, "az_json", lambda args: pytest.fail("CLI must not run"))
    with pytest.raises(ValueError):
        preflight.preflight("id&echo BAD", "medkb-azure-demo-test", "2026-10-20")


def test_app_rejected_before_secret_fetch(monkeypatch):
    monkeypatch.setattr(
        "sys.argv",
        [
            "deploy",
            "--subscription",
            SUBSCRIPTION,
            "--resource-group",
            "medkb-azure-demo-test",
            "--app",
            "bad&echo BAD",
            "--image",
            "ghcr.io/reczec/medkb@sha256:" + "a" * 64,
            "--expires-on",
            "2026-10-20",
        ],
    )
    monkeypatch.setattr(deploy, "preflight", lambda *args: None)
    monkeypatch.setattr(deploy, "az_json", lambda args: pytest.fail("secret fetch must not run"))
    with pytest.raises(SystemExit):
        deploy.main()


def test_what_if_requests_json_and_returns_only_safe_change_summary(monkeypatch):
    def preview(arguments):
        assert "--no-pretty-print" in arguments
        return {
            "changes": [
                {
                    "resourceId": "safe-id",
                    "changeType": "Modify",
                    "delta": [{"path": "private-key", "after": "private-key"}],
                }
            ]
        }

    monkeypatch.setattr(deploy, "az_json", preview)
    result = deploy.run_deployment(
        SUBSCRIPTION,
        "medkb-azure-demo-test",
        "demo",
        "ghcr.io/reczec/medkb@sha256:" + "a" * 64,
        [
            {
                "name": "database-url",
                "value": "postgresql://user:secret@host/medkb_azure?sslmode=require",
            },
            {"name": "jwt-secret", "value": "private-key"},
        ],
        False,
        apply=False,
    )
    assert result == {
        "applied": False,
        "changes": [{"resourceId": "safe-id", "changeType": "Modify"}],
    }
    assert "private-key" not in json.dumps(result)


@pytest.mark.skipif(os.name != "nt", reason="Actual Windows DACL contract")
def test_secret_restriction_removes_existing_explicit_everyone_grant(tmp_path):
    path = tmp_path / "secret.json"
    path.touch()
    subprocess.run(["icacls", str(path), "/grant", "*S-1-1-0:R"], check=True, capture_output=True)
    deploy.restrict_file(path)
    env = dict(os.environ, MEDKB_SECRET_PATH=str(path))
    script = "[IO.File]::GetAccessControl($env:MEDKB_SECRET_PATH).Access | ForEach-Object { $_.IdentityReference.Translate([System.Security.Principal.SecurityIdentifier]).Value }"
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "S-1-1-0" not in result.stdout
    assert len(result.stdout.splitlines()) == 1
