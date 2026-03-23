from __future__ import annotations

from typing import List

from models.schemas import JiraTicket, PipelineContext, BugReport
from tools.jira_client import JiraClient


class JiraAgent:
    """
    Agent that creates Jira tickets from bug reports.
    """

    def __init__(self, client: JiraClient | None = None) -> None:
        self.client = client or JiraClient()

    def create_tickets(self, reports: List[BugReport]) -> List[JiraTicket]:
        tickets: List[JiraTicket] = []
        for report in reports:
            tickets.append(self.client.create_bug_ticket(report))
        return tickets

    def run(self, context: PipelineContext) -> PipelineContext:
        if not context.bug_reports:
            return context

        context.jira_tickets = self.create_tickets(context.bug_reports)
        return context

