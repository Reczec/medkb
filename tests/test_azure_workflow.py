"""Untrusted CI events and untested manual commits cannot cross the delivery gate."""

from copy import deepcopy
from pathlib import Path

import pytest
import yaml

from scripts.azure.ci_guard import validated_sha

SHA = "a" * 40
RUN = {
    "name": "CI",
    "conclusion": "success",
    "status": "completed",
    "head_branch": "main",
    "head_sha": SHA,
    "event": "push",
    "head_repository": {"full_name": "Reczec/medkb"},
}


def test_successful_main_ci_selects_exact_tested_sha():
    assert validated_sha("workflow_run", {"workflow_run": RUN}) == SHA


@pytest.mark.parametrize(
    "field,value",
    [
        ("conclusion", "failure"),
        ("status", "in_progress"),
        ("head_branch", "feature"),
        ("head_repository", {"full_name": "attacker/medkb"}),
        ("head_sha", "abc; echo injected"),
        ("event", "pull_request"),
        ("name", "Other workflow"),
    ],
)
def test_unsafe_ci_event_is_rejected(field, value):
    run = deepcopy(RUN)
    run[field] = value
    with pytest.raises(ValueError):
        validated_sha("workflow_run", {"workflow_run": run})


def test_manual_retry_requires_successful_ci_for_same_sha():
    assert validated_sha("workflow_dispatch", {"inputs": {"sha": SHA}}, [RUN]) == SHA
    with pytest.raises(ValueError):
        validated_sha("workflow_dispatch", {"inputs": {"sha": "b" * 40}}, [RUN])
    with pytest.raises(ValueError):
        validated_sha("workflow_dispatch", {"inputs": {"sha": SHA}}, [])


def test_other_trigger_is_rejected():
    with pytest.raises(ValueError):
        validated_sha("pull_request", {"workflow_run": RUN})


def test_workflow_keeps_privileged_jobs_separate_and_checks_out_tested_sha():
    workflow = yaml.safe_load(
        (Path(__file__).resolve().parents[1] / ".github/workflows/azure-deploy.yml").read_text()
    )
    jobs = workflow["jobs"]
    assert workflow["permissions"] == {"contents": "read"}
    assert jobs["verify"]["permissions"] == {"contents": "read", "actions": "read"}
    assert jobs["image"]["permissions"] == {"contents": "read", "packages": "write"}
    assert jobs["deploy"]["permissions"] == {"contents": "read", "id-token": "write"}
    assert jobs["deploy"]["environment"] == "azure-demo"
    assert workflow["concurrency"] == {"group": "azure-demo", "cancel-in-progress": False}
    for name in ("image", "deploy"):
        checkout = jobs[name]["steps"][0]
        assert checkout["with"] == {
            "ref": "${{ needs.verify.outputs.sha }}",
            "persist-credentials": False,
        }
