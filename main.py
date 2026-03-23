from __future__ import annotations

import asyncio
from pprint import pprint

from orchestrator.workflow import OrchestratorAgent


def main() -> None:
    orchestrator = OrchestratorAgent()
    context = asyncio.run(orchestrator.run_pipeline())

    print("=== Pipeline completed ===")
    print(f"Requirements collected: {len(context.requirements)}")
    print(f"Generated test cases: {len(context.test_cases)}")
    if context.deployment_result:
        print(f"Deployment success: {context.deployment_result.success}")
    if context.unit_test_result:
        print(f"Unit tests success: {context.unit_test_result.success}")
    if context.test_execution_result:
        print(f"Automated test execution success: {context.test_execution_result.success}")
    if context.failure_analysis:
        print(f"Failures detected: {len(context.failure_analysis.failures)}")
    print(f"Bug reports generated: {len(context.bug_reports)}")
    print(f"Jira tickets created (real or simulated): {len(context.jira_tickets)}")

    if context.jira_tickets:
        print("\n=== Example Jira ticket ===")
        pprint(context.jira_tickets[0].model_dump())


if __name__ == "__main__":
    main()

