"""What-if by default; secure parameters preserve secrets on every deployment."""

import argparse
import json
import os
import re
import subprocess
import tempfile
import urllib.parse
from pathlib import Path

from scripts.azure.preflight import az_json, preflight, verify_rag_database
from scripts.azure.smoke import check_deployment

ROOT = Path(__file__).resolve().parents[2]
SECRET_NAMES = {
    "database-url",
    "jwt-secret",
    "ai-api-key",
    "embedding-api-key",
    "icd-client-id",
    "icd-client-secret",
    "ncbi-api-key",
}


def validate_digest(image: str) -> None:
    if not re.fullmatch(r"ghcr\.io/reczec/medkb@sha256:[a-f0-9]{64}", image):
        raise ValueError("A pinned MedKB GHCR sha256 digest is required")


def validate_database_url(url: str) -> None:
    parsed = urllib.parse.urlsplit(url)
    if (
        parsed.scheme not in {"postgres", "postgresql", "postgresql+psycopg"}
        or not parsed.hostname
        or not parsed.username
        or not parsed.password
        or parsed.path != "/medkb_azure"
    ):
        raise ValueError("A separate PostgreSQL database named medkb_azure is required")
    query = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    if set(query) - {"sslmode", "channel_binding"}:
        raise ValueError("Database connection query contains unsupported overrides")
    if "channel_binding" in query and query["channel_binding"] != ["require"]:
        raise ValueError("Only required channel binding is supported")
    sslmode = query.get("sslmode", [])
    if len(sslmode) != 1 or sslmode[0] not in {"require", "verify-ca", "verify-full"}:
        raise ValueError("Enforced TLS (sslmode=require or stronger) is required")


def build_parameters(image: str, secrets: list[dict], rag_enabled: bool) -> dict:
    validate_digest(image)
    names = [secret.get("name") for secret in secrets]
    if len(names) != len(set(names)) or not {"database-url", "jwt-secret"} <= set(names):
        raise ValueError("Unique database-url and jwt-secret app secrets are required")
    for secret in secrets:
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,252}", secret.get("name", "")):
            raise ValueError("Invalid app secret name")
        if not secret.get("value") and not secret.get("keyVaultUrl"):
            raise ValueError("App secret value/reference is missing")
    validate_database_url(
        next(secret.get("value", "") for secret in secrets if secret["name"] == "database-url")
    )
    return {
        "image": {"value": image},
        "appSecrets": {"value": {"items": secrets}},
        "secretEnv": {
            "value": [
                {"name": name.replace("-", "_").upper(), "secretRef": name}
                for name in names
                if name in SECRET_NAMES
            ]
        },
        "ragEnabled": {"value": rag_enabled},
    }


def restrict_file(path: Path) -> None:
    """On Windows POSIX mode alone does not remove inherited read permissions."""
    if os.name == "nt":
        script = """
$ErrorActionPreference = 'Stop'
$path = $env:MEDKB_SECRET_PATH
$sid = [System.Security.Principal.WindowsIdentity]::GetCurrent().User
$acl = New-Object System.Security.AccessControl.FileSecurity
$acl.SetOwner($sid)
$acl.SetAccessRuleProtection($true, $false)
$rule = New-Object System.Security.AccessControl.FileSystemAccessRule($sid, 'FullControl', 'Allow')
$acl.AddAccessRule($rule)
[IO.File]::SetAccessControl($path, $acl)
"""
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
            env=dict(os.environ, MEDKB_SECRET_PATH=str(path)),
            capture_output=True,
            check=False,
        )
        if result.returncode:
            raise ValueError("Cannot restrict local secret file permissions")
    else:
        path.chmod(0o600)


def validate_app(app: str) -> None:
    if not re.fullmatch(r"[a-z][a-z0-9-]{0,29}[a-z0-9]", app) or "--" in app:
        raise ValueError("Invalid Container App name")


def run_deployment(
    subscription: str,
    resource_group: str,
    app: str,
    image: str,
    secrets: list[dict],
    rag_enabled: bool,
    *,
    apply: bool,
) -> dict:
    validate_app(app)
    parameters = build_parameters(image, secrets, rag_enabled)
    parameters["appName"] = {"value": app}
    descriptor, filename = tempfile.mkstemp(prefix="medkb-azure-", suffix=".json")
    path = Path(filename)
    try:
        os.close(descriptor)
        restrict_file(path)
        path.write_text(json.dumps({"parameters": parameters}), encoding="utf-8")
        result = az_json(
            [
                "deployment",
                "group",
                "create" if apply else "what-if",
                "--subscription",
                subscription,
                "--resource-group",
                resource_group,
                "--name",
                "medkb-demo",
                "--template-file",
                str(ROOT / "infra/azure/main.bicep"),
                "--parameters",
                f"@{path}",
            ]
            + ([] if apply else ["--no-pretty-print"])
        )
        # What-if/result bodies can include resolved app configuration. Do not return/log them.
        if apply:
            return {"applied": True}
        return {
            "applied": False,
            "changes": [
                {"resourceId": item["resourceId"], "changeType": item["changeType"]}
                for item in result.get("changes", [])
            ],
        }
    finally:
        path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("subscription", "resource-group", "app", "image", "expires-on"):
        parser.add_argument(f"--{name}", required=True)
    parser.add_argument("--apply", action="store_true")
    rag = parser.add_mutually_exclusive_group()
    rag.add_argument("--rag-enabled", dest="rag_enabled", action="store_true")
    rag.add_argument("--disable-rag", dest="rag_enabled", action="store_false")
    parser.set_defaults(rag_enabled=None)
    parser.add_argument("--bootstrap-secrets-file", type=Path)
    args = parser.parse_args()
    try:
        validate_digest(args.image)
        validate_app(args.app)
        preflight(args.subscription, args.resource_group, args.expires_on)
        if args.bootstrap_secrets_file:
            # Source must be under ignored scratch; never treat a committed file as a secret store.
            source = args.bootstrap_secrets_file.resolve()
            if not source.is_relative_to(ROOT / ".superpowers"):
                raise ValueError("Bootstrap secret file must be inside ignored .superpowers/")
            restrict_file(source)
            secrets = json.loads(source.read_text(encoding="utf-8"))
            rag_enabled = bool(args.rag_enabled)
        else:
            secrets = az_json(
                [
                    "containerapp",
                    "secret",
                    "list",
                    "--show-values",
                    "--subscription",
                    args.subscription,
                    "--resource-group",
                    args.resource_group,
                    "--name",
                    args.app,
                ]
            )
            secrets = [
                {
                    k: v
                    for k, v in item.items()
                    if k in {"name", "value", "keyVaultUrl", "identity"} and v is not None
                }
                for item in secrets
            ]
            current = az_json(
                [
                    "containerapp",
                    "show",
                    "--subscription",
                    args.subscription,
                    "--resource-group",
                    args.resource_group,
                    "--name",
                    args.app,
                ]
            )
            env = current["properties"]["template"]["containers"][0].get("env", [])
            previous = any(
                item.get("name") == "RAG_ENABLED" and item.get("value") == "true" for item in env
            )
            rag_enabled = previous if args.rag_enabled is None else args.rag_enabled
        build_parameters(args.image, secrets, rag_enabled)
        if rag_enabled:
            verify_rag_database(
                next(secret["value"] for secret in secrets if secret["name"] == "database-url")
            )
        result = run_deployment(
            args.subscription,
            args.resource_group,
            args.app,
            args.image,
            secrets,
            rag_enabled,
            apply=args.apply,
        )
        if not args.apply and result is not None:
            print(json.dumps(result))
        if args.apply:
            print(check_deployment(args.subscription, args.resource_group, args.app, args.image))
        if args.apply and args.bootstrap_secrets_file:
            source.unlink()
    except Exception:
        parser.exit(1, "Deployment blocked/failed; sensitive CLI and file contents suppressed.\n")
    print(
        "Deployment applied." if args.apply else "What-if completed; no resource changes applied."
    )


if __name__ == "__main__":
    main()
