from __future__ import annotations

from pathlib import Path
from typing import List

from models.schemas import Requirement, TestCase, TestPriority, PipelineContext
from config.settings import get_settings


class DummyLLMClient:
    """
    Minimal LLM stub so the project runs without external configuration.
    """

    def generate_test_cases(self, requirements: List[Requirement]) -> List[TestCase]:
        test_cases: List[TestCase] = []
        for idx, req in enumerate(requirements, start=1):
            tc_id = f"TC_{idx:03d}"
            title = f"Validate requirement: {req.title}"
            steps = [
                f"Read requirement '{req.title}'",
                "Prepare test data based on acceptance criteria",
                "Execute the scenario via appropriate interface (API/UI/backend)",
                "Verify system behavior against acceptance criteria",
            ]
            expected_result = "System behaves according to the requirement and all acceptance criteria."
            priority = TestPriority.HIGH if "login" in req.title.lower() else TestPriority.MEDIUM
            test_cases.append(
                TestCase(
                    test_case_id=tc_id,
                    title=title,
                    requirement_id=req.id,
                    steps=steps,
                    expected_result=expected_result,
                    priority=priority,
                    tags=["auto-generated"],
                )
            )
        return test_cases


class TestCaseGeneratorAgent:
    """
    Agent that uses an LLM (or a stub) to generate structured test cases from requirements.
    """

    def __init__(self) -> None:
        self.settings = get_settings()
        self.llm_client = DummyLLMClient()
        self.prompt_path = Path("prompts/test_generation_prompt.txt")

    def run(self, context: PipelineContext) -> PipelineContext:
        if not context.requirements:
            # Nothing to do
            return context

        # In a real system we would feed requirements and the prompt into an LLM here.
        test_cases = self.llm_client.generate_test_cases(context.requirements)
        context.test_cases = test_cases
        return context

