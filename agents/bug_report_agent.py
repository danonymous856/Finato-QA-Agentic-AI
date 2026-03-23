from __future__ import annotations

from pathlib import Path
from typing import List

from models.schemas import BugReport, FailureDetail, PipelineContext, TestPriority


class BugReportAgent:
    """
    Agent that converts failures into structured bug reports.
    """

    def __init__(self) -> None:
        self.prompt_path = Path("prompts/bug_report_prompt.txt")

    def _create_bug_report_from_failure(self, failure: FailureDetail) -> BugReport:
        severity = TestPriority.HIGH
        if "timeout" in failure.error.lower():
            severity = TestPriority.MEDIUM

        summary = f"[Auto] Failure in test {failure.test_case_id}: {failure.title}"
        steps = [
            f"Execute automated test case {failure.test_case_id}",
            "Review logs attached to this ticket.",
        ]

        return BugReport(
            title=summary,
            summary=summary,
            steps_to_reproduce=steps,
            expected_result="Automated test case passes without errors.",
            actual_result=f"Automated test case failed with error: {failure.error}",
            logs=failure.logs,
            stack_trace=failure.stack_trace,
            severity=severity,
            related_test_case_id=failure.test_case_id,
        )

    def run(self, context: PipelineContext) -> PipelineContext:
        if not context.failure_analysis or not context.failure_analysis.failures:
            return context

        reports: List[BugReport] = []
        for failure in context.failure_analysis.failures:
            reports.append(self._create_bug_report_from_failure(failure))

        context.bug_reports = reports
        return context

