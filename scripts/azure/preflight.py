"""Read-only trial checks; missing evidence is never treated as protection."""

import argparse
import json
import os
import re
import shutil
import subprocess
from datetime import UTC, date, datetime
from pathlib import Path


def validate_trial(account: dict, expires_on: str, today: date) -> None:
    if account.get("state") != "Enabled":
        raise ValueError("Subscription must be Enabled")
    if account.get("subscriptionPolicies", {}).get("spendingLimit") != "On":
        raise ValueError("Verified spending limit On is required")
    if today >= date.fromisoformat(expires_on):
        raise ValueError("Trial expired; deployment blocked")


def validate_target(
    actual_subscription: str, expected_subscription: str, resource_group: str
) -> None:
    if (
        not re.fullmatch(
            r"[a-fA-F0-9]{8}(?:-[a-fA-F0-9]{4}){3}-[a-fA-F0-9]{12}", expected_subscription
        )
        or actual_subscription != expected_subscription
    ):
        raise ValueError("Subscription does not match the explicit expected target")
    if not re.fullmatch(r"medkb-azure-demo-[a-z0-9][a-z0-9-]{0,39}", resource_group):
        raise ValueError("Resource group must be a named medkb-azure-demo-* group")


def validate_rag_readiness(coverage: dict[str, tuple[int, int]]) -> None:
    if any(coverage.get(lang) != (271, 271) for lang in ("de", "en")):
        raise ValueError("Complete current bilingual index (271 chunks per language) required")


def rag_coverage(db, settings) -> dict[str, tuple[int, int]]:
    from app.rag.index import corpus, vectors

    result = {}
    for lang in ("de", "en"):
        current = corpus(db, settings, (lang,))
        result[lang] = (len({chunk.key for chunk in current}), len(vectors(db, current)))
    return result


def verify_rag_database(database_url: str) -> None:
    from sqlalchemy import create_engine, text
    from sqlalchemy.orm import Session

    from app.config import Settings
    from app.database import normalize_url

    engine = create_engine(normalize_url(database_url), connect_args={"connect_timeout": 10})
    try:
        with Session(engine) as db:
            db.execute(text("SET TRANSACTION READ ONLY"))
            validate_rag_readiness(rag_coverage(db, Settings(_env_file=None)))
    finally:
        engine.dispose()


def az_json(arguments: list[str], *, timeout_seconds: float = 600) -> dict | list:
    """Capture CLI output. Never expose raw stderr: it can contain app credentials."""
    executable = shutil.which("az")
    if not executable:
        raise ValueError("Azure CLI is missing; install the official distribution")
    command = [executable]
    if Path(executable).suffix.lower() in {".cmd", ".bat"}:
        python = Path(executable).resolve().parent.parent / "python.exe"
        if not python.is_file():
            raise ValueError("Azure CLI bundled Python is missing; batch execution is refused")
        command = [str(python), "-IBm", "azure.cli"]
    environment = dict(os.environ)
    environment["AZURE_LOGGING_ENABLE_LOG_FILE"] = "false"
    try:
        result = subprocess.run(
            [*command, *arguments, "--output", "json", "--only-show-errors"],
            env=environment,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout_seconds,
        )
    except (OSError, subprocess.TimeoutExpired):
        raise ValueError("Azure CLI failed or timed out; raw output suppressed") from None
    if result.returncode:
        raise ValueError("Azure CLI failed; raw output suppressed")
    try:
        return json.loads(result.stdout) if result.stdout.strip() else {}
    except json.JSONDecodeError:
        raise ValueError("Azure CLI returned invalid JSON; raw output suppressed") from None


def preflight(subscription: str, resource_group: str, expires_on: str) -> None:
    validate_target(subscription, subscription, resource_group)
    # az account show's cached profile can omit subscriptionPolicies. Read fresh ARM evidence.
    account = az_json(
        [
            "rest",
            "--method",
            "get",
            "--url",
            f"https://management.azure.com/subscriptions/{subscription}?api-version=2022-12-01",
        ]
    )
    validate_target(account.get("subscriptionId", ""), subscription, resource_group)
    validate_trial(account, expires_on, datetime.now(UTC).date())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subscription", required=True)
    parser.add_argument("--resource-group", required=True)
    parser.add_argument("--expires-on", required=True)
    args = parser.parse_args()
    try:
        preflight(args.subscription, args.resource_group, args.expires_on)
    except ValueError as error:
        parser.exit(1, f"Preflight blocked: {error}\n")
    print(
        "Protected, enabled, unexpired subscription verified. Check portal credit/offer separately."
    )


if __name__ == "__main__":
    main()
