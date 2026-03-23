from __future__ import annotations

from typing import List

try:
    from jira import JIRA
except ImportError:  # pragma: no cover - optional dependency during tests
    JIRA = None  # type: ignore

from models.schemas import Requirement, RequirementSource, JiraTicket, BugReport
from config.settings import get_settings


class JiraClient:
    """
    Thin wrapper around the official Jira client library.
    Falls back to a no-op implementation if configuration is missing.
    """

    def __init__(self) -> None:
        self.settings = get_settings().jira
        self._client = None

        if (
            self.settings.url
            and self.settings.username
            and self.settings.api_token
            and JIRA is not None
        ):
            self._client = JIRA(
                server=self.settings.url,
                basic_auth=(self.settings.username, self.settings.api_token),
            )

    def is_configured(self) -> bool:
        return self._client is not None

    def fetch_requirements_from_jira(self, jql: str) -> List[Requirement]:
        if not self._client:
            # Fallback: return an empty list, allowing pipeline to run locally
            return []

        issues = self._client.search_issues(jql)
        requirements: List[Requirement] = []
        for issue in issues:
            fields = issue.fields
            description = getattr(fields, "description", "") or ""
            requirements.append(
                Requirement(
                    id=str(issue.key),
                    title=str(fields.summary),
                    description=description,
                    acceptance_criteria=[],
                    source=RequirementSource.JIRA,
                    source_ref=str(issue.key),
                )
            )
        return requirements

    def create_bug_ticket(self, report: BugReport) -> JiraTicket:
        """
        Create a Jira ticket from a bug report. If Jira isn't configured,
        this returns a synthetic ticket object for demonstration purposes.
        """
        description_lines = [
            "*Summary*",
            report.summary,
            "",
            "*Steps to Reproduce*",
        ]
        description_lines.extend(f"# {step}" for step in report.steps_to_reproduce)
        description_lines.extend(
            [
                "",
                "*Expected Result*",
                report.expected_result,
                "",
                "*Actual Result*",
                report.actual_result,
            ]
        )
        if report.logs:
            description_lines.extend(["", "*Logs*", "{{noformat}}", report.logs, "{{noformat}}"])
        if report.stack_trace:
            description_lines.extend(
                ["", "*Stack Trace*", "{{noformat}}", report.stack_trace, "{{noformat}}"]
            )
        description = "\n".join(description_lines)

        if not self._client or not self.settings.project_key:
            # Local fallback
            key = "DEMO-1"
            url = f"{self.settings.url or 'http://localhost/jira'}/browse/{key}"
            return JiraTicket(key=key, url=url, summary=report.summary, description=description)

        issue_dict = {
            "project": {"key": self.settings.project_key},
            "summary": report.summary,
            "description": description,
            "issuetype": {"name": "Bug"},
        }
        issue = self._client.create_issue(fields=issue_dict)
        url = f"{self.settings.url}/browse/{issue.key}"
        return JiraTicket(key=str(issue.key), url=url, summary=report.summary, description=description)

