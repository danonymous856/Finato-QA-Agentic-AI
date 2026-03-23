from __future__ import annotations

import asyncio
from typing import Optional

from models.schemas import PipelineContext
from agents.requirements_agent import RequirementsAgent
from agents.test_generator_agent import TestCaseGeneratorAgent
from agents.deployment_agent import DeploymentAgent
from agents.unit_test_agent import UnitTestAgent
from agents.execution_agent import TestExecutionAgent
from agents.failure_detection_agent import FailureDetectionAgent
from agents.bug_report_agent import BugReportAgent
from agents.jira_agent import JiraAgent


class OrchestratorAgent:
    """
    High-level orchestrator controlling the full QA workflow.
    """

    def __init__(self) -> None:
        self.requirements_agent = RequirementsAgent()
        self.test_generator_agent = TestCaseGeneratorAgent()
        self.deployment_agent = DeploymentAgent()
        self.unit_test_agent = UnitTestAgent()
        self.execution_agent = TestExecutionAgent()
        self.failure_detection_agent = FailureDetectionAgent()
        self.bug_report_agent = BugReportAgent()
        self.jira_agent = JiraAgent()

    async def run_pipeline(
        self,
        brd_path: Optional[str] = None,
        jira_query: Optional[str] = None,
    ) -> PipelineContext:
        """
        Execute the full pipeline:
        BRD/Jira -> Requirements -> Test cases -> Deploy -> Unit tests
        -> Execute tests -> Detect failures -> Bug reports -> Jira tickets
        """
        context = PipelineContext(brd_path=brd_path, jira_query=jira_query)

        # Step 1: requirements
        context = self.requirements_agent.run(context)

        # Step 2: test case generation
        context = self.test_generator_agent.run(context)

        # Step 3: deployment
        context = self.deployment_agent.run(context)

        # Step 4: unit tests
        context = self.unit_test_agent.run(context)

        # Step 5: execute generated tests
        context = self.execution_agent.run(context)

        # Step 6: detect failures
        context = self.failure_detection_agent.run(context)

        # Step 7: bug reports
        context = self.bug_report_agent.run(context)

        # Step 8: Jira tickets
        context = self.jira_agent.run(context)

        return context

