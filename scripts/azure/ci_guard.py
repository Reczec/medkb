"""Select an exact successfully tested main commit, never a PR/fork payload."""

import json
import os
import re
import urllib.parse
import urllib.request
from pathlib import Path


def successful_run(run: dict, sha: str) -> bool:
    return (
        run.get("name") == "CI"
        and run.get("conclusion") == "success"
        and run.get("status") == "completed"
        and run.get("head_branch") == "main"
        and run.get("event") == "push"
        and run.get("head_sha") == sha
        and run.get("head_repository", {}).get("full_name") == "Reczec/medkb"
    )


def validated_sha(event_name: str, event: dict, runs: list[dict] | None = None) -> str:
    if event_name == "workflow_run":
        run = event.get("workflow_run", {})
        sha = run.get("head_sha", "")
        candidates = [run]
    elif event_name == "workflow_dispatch":
        sha = event.get("inputs", {}).get("sha", "")
        candidates = runs or []
    else:
        raise ValueError("Unsupported delivery trigger")
    if not re.fullmatch(r"[a-f0-9]{40}", sha):
        raise ValueError("Full commit SHA required")
    if not any(successful_run(run, sha) for run in candidates):
        raise ValueError("Successful push CI for this exact main commit is required")
    return sha


def main() -> None:
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text(encoding="utf-8"))
    event_name = os.environ["GITHUB_EVENT_NAME"]
    runs = None
    if event_name == "workflow_dispatch":
        sha = event.get("inputs", {}).get("sha", "")
        if not re.fullmatch(r"[a-f0-9]{40}", sha):
            raise ValueError("Full commit SHA required")
        query = urllib.parse.urlencode(
            {
                "branch": "main",
                "event": "push",
                "head_sha": sha,
                "status": "completed",
                "per_page": 100,
            }
        )
        request = urllib.request.Request(
            f"https://api.github.com/repos/Reczec/medkb/actions/workflows/ci.yml/runs?{query}",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {os.environ['GH_TOKEN']}",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            runs = json.load(response)["workflow_runs"]
    sha = validated_sha(event_name, event, runs)
    with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as output:
        output.write(f"sha={sha}\n")


if __name__ == "__main__":
    main()
