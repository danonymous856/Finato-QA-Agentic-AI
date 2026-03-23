from __future__ import annotations

from pathlib import Path

from models.schemas import UnitTestResult, PipelineContext
from tools.test_runner import run_pytest


class UnitTestAgent:
    """
    Agent that runs the unit test suite using pytest.
    """

    def __init__(self, tests_path: str = "tests") -> None:
        self.tests_path = tests_path

    def run_unit_tests(self) -> UnitTestResult:
        junit_path = Path("reports/pytest-report.xml")
        junit_path.parent.mkdir(parents=True, exist_ok=True)
        return run_pytest(self.tests_path, str(junit_path))

    def run(self, context: PipelineContext) -> PipelineContext:
        context.unit_test_result = self.run_unit_tests()
        return context

