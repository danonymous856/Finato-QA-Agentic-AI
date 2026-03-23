from __future__ import annotations

import subprocess
from pathlib import Path

from models.schemas import DeploymentConfig, DeploymentResult, PipelineContext


class DeploymentAgent:
    """
    Agent responsible for deploying the application or services under test.

    This reference implementation supports two modes:
    - If a docker-compose file is configured, it runs `docker compose up -d`.
    - Otherwise, it assumes the application is already running and returns success.
    """

    def __init__(self, config: DeploymentConfig | None = None) -> None:
        self.config = config or DeploymentConfig(environment_name="local")

    def deploy(self) -> DeploymentResult:
        compose_file = self.config.docker_compose_file
        if not compose_file:
            return DeploymentResult(
                success=True,
                message="No deployment config provided; assuming system under test is already running.",
            )

        compose_path = Path(compose_file)
        if not compose_path.exists():
            return DeploymentResult(
                success=False, message=f"Docker compose file not found: {compose_file}"
            )

        cmd = ["docker", "compose", "-f", str(compose_path), "up", "-d"]
        process = subprocess.run(cmd, capture_output=True, text=True)
        logs = process.stdout + "\n" + process.stderr
        success = process.returncode == 0
        message = "Deployment succeeded" if success else "Deployment failed"

        return DeploymentResult(success=success, message=message, logs=logs)

    def run(self, context: PipelineContext) -> PipelineContext:
        # Use deployment config from context if present
        if context.deployment_config:
            self.config = context.deployment_config
        context.deployment_result = self.deploy()
        return context

