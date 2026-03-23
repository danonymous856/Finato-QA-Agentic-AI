from __future__ import annotations

from typing import List

from models.schemas import FailureAnalysis, FailureDetail, PipelineContext


class FailureDetectionAgent:
    """
    Agent that inspects test execution results and extracts failures.
    """

    def run(self, context: PipelineContext) -> PipelineContext:
        ter = context.test_execution_result
        failures: List[FailureDetail] = []

        if ter:
            for r in ter.results:
                if not r.success:
                    failures.append(
                        FailureDetail(
                            test_case_id=r.test_case_id,
                            title=r.title,
                            error=r.error or "Unknown error",
                            stack_trace=r.stack_trace,
                            logs=r.logs,
                        )
                    )

        context.failure_analysis = FailureAnalysis(
            has_failures=bool(failures),
            failures=failures,
        )
        return context

