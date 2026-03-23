import asyncio

from orchestrator.workflow import OrchestratorAgent


def test_orchestrator_runs_end_to_end():
    orchestrator = OrchestratorAgent()
    context = asyncio.run(orchestrator.run_pipeline())

    # The pipeline should complete without raising and produce a context object.
    assert context is not None
    # Requirements and test cases may be empty in a bare environment, but objects should exist.
    assert hasattr(context, "requirements")
    assert hasattr(context, "test_cases")

