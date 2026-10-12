"""What-if by default; secure parameters preserve secrets on every deployment."""

import argparse
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

from scripts.azure.preflight import az_json, preflight

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
        account = f"{os.environ['USERDOMAIN']}\\{os.environ['USERNAME']}"
        result = subprocess.run(
            ["icacls", str(path), "/inheritance:r", "/grant:r", f"{account}:F"],
            capture_output=True,
            check=False,
        )
        if result.returncode:
            raise ValueError("Cannot restrict local secret file permissions")
    else:
        path.chmod(0o600)


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
    if not re.fullmatch(r"[a-z][a-z0-9-]{0,29}[a-z0-9]", app) or "--" in app:
        raise ValueError("Invalid Container App name")
    parameters = build_parameters(image, secrets, rag_enabled)
    parameters["appName"] = {"value": app}
    descriptor, filename = tempfile.mkstemp(prefix="medkb-azure-", suffix=".json")
    path = Path(filename)
    try:
        os.close(descriptor)
        restrict_file(path)
        path.write_text(json.dumps({"parameters": parameters}), encoding="utf-8")
        az_json(
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
        )
        # What-if/result bodies can include resolved app configuration. Do not return/log them.
        return {"applied": apply}
    finally:
        path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("subscription", "resource-group", "app", "image", "expires-on"):
        parser.add_argument(f"--{name}", required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--rag-enabled", action="store_true")
    parser.add_argument("--bootstrap-secrets-file", type=Path)
    args = parser.parse_args()
    try:
        validate_digest(args.image)
        preflight(args.subscription, args.resource_group, args.expires_on)
        if args.bootstrap_secrets_file:
            # Source must be under ignored scratch; never treat a committed file as a secret store.
            source = args.bootstrap_secrets_file.resolve()
            if not source.is_relative_to(ROOT / ".superpowers"):
                raise ValueError("Bootstrap secret file must be inside ignored .superpowers/")
            restrict_file(source)
            secrets = json.loads(source.read_text(encoding="utf-8"))
        else:
            secrets = az_json(
                [
                    "containerapp",
                    "secret",
                    "list",
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
        run_deployment(
            args.subscription,
            args.resource_group,
            args.app,
            args.image,
            secrets,
            args.rag_enabled,
            apply=args.apply,
        )
        if args.apply and args.bootstrap_secrets_file:
            source.unlink()
    except (ValueError, OSError, TypeError, KeyError):
        parser.exit(1, "Deployment blocked/failed; sensitive CLI and file contents suppressed.\n")
    print(
        "Deployment applied." if args.apply else "What-if completed; no resource changes applied."
    )


if __name__ == "__main__":
    main()
