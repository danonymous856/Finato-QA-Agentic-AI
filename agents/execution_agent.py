from __future__ import annotations

from typing import List

import requests

from models.schemas import (
    PipelineContext,
    TestExecutionRequest,
    TestExecutionResult,
    SingleTestExecutionResult,
    TestType,
)
from config.settings import get_settings


class TestExecutionAgent:
    """
    Agent that executes generated test cases.

    This minimal implementation supports API-style tests by issuing simple
    HTTP GET requests to the configured base URL and marking tests as passed
    if the response status code is 200. UI and backend tests can be added
    later using Playwright and pytest-based scenarios.
    """

    def __init__(self) -> None:
        self.settings = get_settings()

    def execute_api_tests(self, request: TestExecutionRequest) -> TestExecutionResult:
        base_url = request.base_url or self.settings.base_url
        results: List[SingleTestExecutionResult] = []

        for tc in request.test_cases:
            url = base_url
            logs = f"Calling {url} for test case {tc.test_case_id}"
            try:
                response = requests.get(url, timeout=5)
                success = response.status_code == 200
                logs += f"\nStatus code: {response.status_code}"
                results.append(
                    SingleTestExecutionResult(
                        test_case_id=tc.test_case_id,
                        title=tc.title,
                        success=success,
                        logs=logs,
                        error=None if success else f"Unexpected status code: {response.status_code}",
                        stack_trace=None,
                    )
                )
            except Exception as exc:  # pragma: no cover - network-dependent
                results.append(
                    SingleTestExecutionResult(
                        test_case_id=tc.test_case_id,
                        title=tc.title,
                        success=False,
                        logs=logs,
                        error=str(exc),
                        stack_trace=None,
                    )
                )

        overall_success = all(r.success for r in results) if results else True
        return TestExecutionResult(success=overall_success, results=results)

    def run(self, context: PipelineContext) -> PipelineContext:
        if not context.test_cases:
            return context

        req = TestExecutionRequest(
            test_cases=context.test_cases,
            base_url=self.settings.base_url,
            test_type=TestType.API,
        )
        context.test_execution_result = self.execute_api_tests(req)
        return context

