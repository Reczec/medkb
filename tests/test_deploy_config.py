"""The deployment files say what the public demo needs, and never contain a secret."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECRETS = {"DATABASE_URL", "AI_API_KEY", "ICD_CLIENT_ID", "ICD_CLIENT_SECRET", "NCBI_API_KEY"}


def render_env() -> dict[str, list[str]]:
    """envVars of render.yaml as {key: [the property lines that follow it]} (no YAML library)."""
    env: dict[str, list[str]] = {}
    current = None
    for line in (ROOT / "render.yaml").read_text(encoding="utf-8").splitlines():
        if match := re.match(r"\s*- key: (\w+)", line):
            current = match.group(1)
            env[current] = []
        elif current and re.match(r"\s{8,}\w+:", line):
            env[current].append(line.strip())
        elif current and not line.startswith(" " * 6):
            current = None
    return env


def test_blueprint_describes_a_free_docker_web_service():
    text = (ROOT / "render.yaml").read_text(encoding="utf-8")
    for line in (
        "type: web",
        "runtime: docker",
        "plan: free",
        "healthCheckPath: /api/health",
        "branch: main",
    ):
        assert line in text, line


def test_blueprint_sets_the_public_demo():
    env = render_env()
    assert env["DEMO_MODE"] == ['value: "true"']
    assert env["DEMO_RESET_HOURS"] == ['value: "3"']
    assert env["JWT_SECRET"] == ["generateValue: true"]


def test_secrets_are_never_values_in_the_blueprint():
    env = render_env()
    assert SECRETS <= set(env)
    for key in SECRETS | {"CLIENT_IP_HEADER"}:
        assert env[key] == ["sync: false"], key


def test_image_binds_the_platform_port_and_ignores_forwarded_headers():
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    command = next(line for line in dockerfile.splitlines() if line.startswith("CMD"))
    assert "${PORT:-8000}" in command
    # Render sets FORWARDED_ALLOW_IPS=*; uvicorn would then trust any X-Forwarded-For.
    assert "--no-proxy-headers" in command
    assert "PORT" in next(line for line in dockerfile.splitlines() if "urlopen" in line)


def test_render_deploys_only_after_ci_passes():
    assert "autoDeployTrigger: checksPass" in (ROOT / "render.yaml").read_text(encoding="utf-8")
