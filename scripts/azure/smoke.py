"""Bounded public health and exact deployed revision verification."""

import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request

from scripts.azure.preflight import az_json


def check_health(url: str, timeout_seconds: int = 180) -> None:
    parsed = urllib.parse.urlsplit(url)
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
        or parsed.path not in ("", "/")
        or timeout_seconds <= 0
    ):
        raise ValueError("An HTTPS base URL without credentials/query/path is required")
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        try:
            request = urllib.request.Request(url.rstrip("/") + "/api/health")
            with urllib.request.urlopen(
                request, timeout=min(10, max(0.1, deadline - time.monotonic()))
            ) as response:
                if json.load(response) == {"status": "ok"}:
                    return
        except (urllib.error.URLError, TimeoutError, OSError, ValueError):
            pass
        time.sleep(min(5, max(0, deadline - time.monotonic())))
    raise ValueError("HTTPS health timed out")


def check_deployment(
    subscription: str,
    resource_group: str,
    app: str,
    image: str,
    timeout_seconds: int = 180,
) -> str:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        result = az_json(
            [
                "containerapp",
                "show",
                "--subscription",
                subscription,
                "--resource-group",
                resource_group,
                "--name",
                app,
            ],
            timeout_seconds=max(0.1, deadline - time.monotonic()),
        )
        properties = result.get("properties", {})
        containers = properties.get("template", {}).get("containers", [])
        latest = properties.get("latestRevisionName")
        if (
            latest
            and latest == properties.get("latestReadyRevisionName")
            and properties.get("provisioningState") == "Succeeded"
            and len(containers) == 1
            and containers[0].get("image") == image
        ):
            url = "https://" + properties["configuration"]["ingress"]["fqdn"]
            check_health(url, timeout_seconds)
            return url
        time.sleep(min(5, max(0, deadline - time.monotonic())))
    raise ValueError("Expected image revision did not become ready")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url")
    args = parser.parse_args()
    try:
        check_health(args.url)
    except ValueError as error:
        parser.exit(1, f"Health check failed: {error}\n")
    print("HTTPS health verified.")


if __name__ == "__main__":
    main()
