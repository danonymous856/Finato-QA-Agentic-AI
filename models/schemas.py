from __future__ import annotations

from enum import Enum
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field


class RequirementSource(str, Enum):
    BRD = "brd"
    JIRA = "jira"


class Requirement(BaseModel):
    id: str
    title: str
    description: str
    acceptance_criteria: List[str] = Field(default_factory=list)
    source: RequirementSource
    source_ref: Optional[str] = None  # e.g. filename or Jira key


class TestPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class TestStep(BaseModel):
    description: str


class TestCase(BaseModel):
    test_case_id: str
    title: str
    requirement_id: Optional[str] = None
    steps: List[str]
    expected_result: str
    priority: TestPriority = TestPriority.MEDIUM
    tags: List[str] = Field(default_factory=list)
    component: Optional[str] = None


class DeploymentConfig(BaseModel):
    environment_name: str = "local"
    docker_compose_file: Optional[str] = None
    extra_env: Dict[str, str] = Field(default_factory=dict)


class DeploymentResult(BaseModel):
    success: bool
    message: str
    url: Optional[str] = None
    logs: Optional[str] = None


class UnitTestResult(BaseModel):
    success: bool
    total: int
    passed: int
    failed: int
    errors: int
    report_path: Optional[str] = None
    logs: Optional[str] = None


class TestType(str, Enum):
    API = "api"
    UI = "ui"
    BACKEND = "backend"


class TestExecutionRequest(BaseModel):
    test_cases: List[TestCase]
    base_url: Optional[str] = None
    test_type: TestType = TestType.API


class SingleTestExecutionResult(BaseModel):
    test_case_id: str
    title: str
    success: bool
    logs: Optional[str] = None
    error: Optional[str] = None
    stack_trace: Optional[str] = None


class TestExecutionResult(BaseModel):
    success: bool
    results: List[SingleTestExecutionResult]


class FailureDetail(BaseModel):
    test_case_id: str
    title: str
    error: str
    stack_trace: Optional[str] = None
    logs: Optional[str] = None


class FailureAnalysis(BaseModel):
    has_failures: bool
    failures: List[FailureDetail] = Field(default_factory=list)


class BugReport(BaseModel):
    title: str
    summary: str
    steps_to_reproduce: List[str]
    expected_result: str
    actual_result: str
    logs: Optional[str] = None
    stack_trace: Optional[str] = None
    severity: TestPriority = TestPriority.MEDIUM
    related_test_case_id: Optional[str] = None


class JiraTicket(BaseModel):
    key: str
    url: Optional[str] = None
    summary: str
    description: str


class PipelineContext(BaseModel):
    """
    Shared context object passed between agents by the orchestrator.
    """

    brd_path: Optional[str] = None
    jira_query: Optional[str] = None

    requirements: List[Requirement] = Field(default_factory=list)
    test_cases: List[TestCase] = Field(default_factory=list)

    deployment_config: DeploymentConfig = Field(default_factory=DeploymentConfig)
    deployment_result: Optional[DeploymentResult] = None

    unit_test_result: Optional[UnitTestResult] = None
    test_execution_result: Optional[TestExecutionResult] = None
    failure_analysis: Optional[FailureAnalysis] = None
    bug_reports: List[BugReport] = Field(default_factory=list)
    jira_tickets: List[JiraTicket] = Field(default_factory=list)

