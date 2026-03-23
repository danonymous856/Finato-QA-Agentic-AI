from __future__ import annotations

from typing import List, Optional

from models.schemas import Requirement, PipelineContext
from tools.docx_parser import parse_brd_requirements
from tools.jira_client import JiraClient
from config.settings import get_settings


class RequirementsAgent:
    """
    Agent responsible for collecting requirements from BRD documents and Jira.
    """

    def __init__(self, jira_client: Optional[JiraClient] = None) -> None:
        self.settings = get_settings()
        self.jira_client = jira_client or JiraClient()

    def read_brd(self, path: Optional[str] = None) -> List[Requirement]:
        path = path or self.settings.default_brd_path
        return parse_brd_requirements(path)

    def fetch_jira_requirements(self, jql: Optional[str] = None) -> List[Requirement]:
        jql = jql or f'project = {self.settings.jira.project_key} AND type = Story'
        return self.jira_client.fetch_requirements_from_jira(jql)

    def run(self, context: PipelineContext) -> PipelineContext:
        brd_requirements: List[Requirement] = []
        if context.brd_path:
            brd_requirements = self.read_brd(context.brd_path)
        else:
            # Try default BRD path; ignore errors if missing for demo purposes
            try:
                brd_requirements = self.read_brd()
            except Exception:
                brd_requirements = []

        jira_requirements: List[Requirement] = []
        if context.jira_query:
            jira_requirements = self.fetch_jira_requirements(context.jira_query)
        else:
            try:
                jira_requirements = self.fetch_jira_requirements()
            except Exception:
                jira_requirements = []

        context.requirements = brd_requirements + jira_requirements
        return context

