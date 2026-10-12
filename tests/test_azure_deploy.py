"""Deployment owns a bounded graph and must not discard or expose existing secrets."""

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from scripts.azure import deploy

ROOT = Path(__file__).resolve().parents[1]
IMAGE = "ghcr.io/reczec/medkb@sha256:" + "a" * 64
SECRETS = [
    {
        "name": "database-url",
        "value": "postgresql+psycopg://isolated:secret@host/medkb_azure?sslmode=require",
    },
    {"name": "jwt-secret", "value": "persist-this-secret"},
    {"name": "ai-api-key", "value": "provider-private-key"},
]


@pytest.mark.parametrize(
    "image",
    [
        "ghcr.io/reczec/medkb:latest",
        "ghcr.io/reczec/medkb@sha256:abc",
        "evil.test/app@sha256:" + "a" * 64,
        IMAGE + ";echo bad",
    ],
)
def test_unpinned_or_wrong_repository_image_is_rejected(image):
    with pytest.raises(ValueError, match="digest"):
        deploy.validate_digest(image)


def test_parameters_preserve_secrets_and_reference_them(capsys):
    parameters = deploy.build_parameters(IMAGE, SECRETS, False)
    assert parameters["appSecrets"]["value"]["items"] == SECRETS
    assert parameters["ragEnabled"]["value"] is False
    assert {"name": "AI_API_KEY", "secretRef": "ai-api-key"} in parameters["secretEnv"]["value"]
    assert capsys.readouterr().out == ""


def test_routine_cli_requests_and_preserves_actual_secret_values(monkeypatch, capsys):
    captured = []
    monkeypatch.setattr(
        "sys.argv",
        [
            "deploy",
            "--subscription",
            "subscription",
            "--resource-group",
            "medkb-azure-demo-test",
            "--app",
            "demo",
            "--image",
            IMAGE,
            "--expires-on",
            "2026-10-20",
        ],
    )
    monkeypatch.setattr(deploy, "preflight", lambda *args: None)
    monkeypatch.setattr(
        deploy,
        "az_json",
        lambda arguments: (
            {"properties": {"template": {"containers": [{"env": []}]}}}
            if arguments[:2] == ["containerapp", "show"]
            else SECRETS
            if "--show-values" in arguments
            else [{"name": s["name"]} for s in SECRETS]
        ),
    )

    def apply(subscription, resource_group, app, image, secrets, rag_enabled, **kwargs):
        captured.append(deploy.build_parameters(image, secrets, rag_enabled))

    monkeypatch.setattr(deploy, "run_deployment", apply)
    deploy.main()
    assert captured[0]["appSecrets"]["value"]["items"] == SECRETS
    assert "provider-private-key" not in capsys.readouterr().out


def test_routine_deployment_preserves_enabled_rag_and_checks_current_database(monkeypatch):
    seen = []
    monkeypatch.setattr(
        "sys.argv",
        [
            "deploy",
            "--subscription",
            "subscription",
            "--resource-group",
            "medkb-azure-demo-test",
            "--app",
            "demo",
            "--image",
            IMAGE,
            "--expires-on",
            "2026-10-20",
        ],
    )
    monkeypatch.setattr(deploy, "preflight", lambda *args: None)
    monkeypatch.setattr(
        deploy,
        "az_json",
        lambda arguments: (
            SECRETS
            if arguments[:3] == ["containerapp", "secret", "list"]
            else {
                "properties": {
                    "template": {
                        "containers": [{"env": [{"name": "RAG_ENABLED", "value": "true"}]}]
                    }
                }
            }
        ),
    )
    monkeypatch.setattr(deploy, "verify_rag_database", lambda url: seen.append(url), raising=False)
    monkeypatch.setattr(deploy, "run_deployment", lambda *args, **kwargs: seen.append(args[5]))
    deploy.main()
    assert seen == ["postgresql+psycopg://isolated:secret@host/medkb_azure?sslmode=require", True]


@pytest.mark.parametrize("url", ["sqlite:///local.db", "postgresql://user:password@host/neondb"])
def test_nonisolated_database_is_rejected_without_disclosing_credentials(url):
    with pytest.raises(ValueError) as error:
        deploy.validate_database_url(url)
    assert "password" not in str(error.value)


@pytest.mark.parametrize("query", ["", "?sslmode=disable", "?sslmode=prefer"])
def test_database_password_requires_enforced_tls(query):
    with pytest.raises(ValueError, match="TLS"):
        deploy.validate_database_url("postgresql://user:password@host/medkb_azure" + query)


@pytest.mark.parametrize(
    "secrets",
    [
        [],
        [{"name": "jwt-secret", "value": "secret"}],
        SECRETS + [{"name": "jwt-secret", "value": "duplicate"}],
    ],
)
def test_missing_or_duplicate_secrets_block_deployment(secrets):
    with pytest.raises(ValueError):
        deploy.build_parameters(IMAGE, secrets, False)


def test_parameter_file_is_deleted_even_when_cli_fails(monkeypatch, tmp_path, capsys):
    seen = []

    def fail(arguments):
        path = Path(arguments[arguments.index("--parameters") + 1].removeprefix("@"))
        seen.append(path)
        data = json.loads(path.read_text())
        assert (
            data["parameters"]["appSecrets"]["value"]["items"][2]["value"] == "provider-private-key"
        )
        assert "provider-private-key" not in " ".join(arguments)
        raise ValueError("Azure CLI failed; raw output suppressed")

    monkeypatch.setattr(deploy, "az_json", fail)
    with pytest.raises(ValueError):
        deploy.run_deployment(
            "subscription", "medkb-azure-demo-test", "demo", IMAGE, SECRETS, False, apply=False
        )
    assert len(seen) == 1 and not seen[0].exists()
    assert "provider-private-key" not in capsys.readouterr().out


def test_compiled_template_has_only_bounded_consumption_resources(tmp_path):
    compiler = os.environ.get("BICEP_EXE") or shutil.which("bicep")
    if not compiler:
        pytest.skip("Bicep compiler required; dedicated IaC CI job runs this contract")
    destination = tmp_path / "template.json"
    subprocess.run(
        [compiler, "build", str(ROOT / "infra/azure/main.bicep"), "--outfile", str(destination)],
        check=True,
    )
    template = json.loads(destination.read_text())
    resources = template["resources"]
    if isinstance(resources, dict):
        resources = list(resources.values())
    assert {r["type"] for r in resources} == {
        "Microsoft.App/managedEnvironments",
        "Microsoft.App/containerApps",
    }
    environment = next(r for r in resources if r["type"].endswith("managedEnvironments"))
    app = next(r for r in resources if r["type"].endswith("containerApps"))
    assert environment["properties"]["appLogsConfiguration"]["destination"] == "none"
    assert environment["properties"]["workloadProfiles"] == [
        {"name": "Consumption", "workloadProfileType": "Consumption"}
    ]
    configuration = app["properties"]["configuration"]
    assert configuration["activeRevisionsMode"] == "Single"
    assert configuration["ingress"]["external"] is True
    assert configuration["ingress"]["allowInsecure"] is False
    assert configuration["ingress"]["targetPort"] == 8000
    assert app["properties"]["template"]["scale"]["minReplicas"] == 0
    assert app["properties"]["template"]["scale"]["maxReplicas"] == 1
    compute = app["properties"]["template"]["containers"][0]["resources"]
    assert compute["cpu"] == "[json('0.5')]"
    assert compute["memory"] == "1Gi"
    assert template["parameters"]["appSecrets"]["type"] == "secureObject"
    assert template["parameters"]["location"]["defaultValue"] == "northeurope"
    assert set(template["parameters"]["location"]["allowedValues"]) == {"westeurope", "northeurope"}
    assert set(template["outputs"]) == {"hostname"}
