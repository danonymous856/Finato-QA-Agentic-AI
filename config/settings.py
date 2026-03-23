from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

from pydantic import BaseModel


class JiraSettings(BaseModel):
    url: Optional[str] = None
    username: Optional[str] = None
    api_token: Optional[str] = None
    project_key: Optional[str] = None


class LLMSettings(BaseModel):
    provider: str = "openai"  # or "dummy"
    model: str = "gpt-4.1-mini"
    api_key: Optional[str] = None


class Settings(BaseModel):
    jira: JiraSettings = JiraSettings()
    llm: LLMSettings = LLMSettings(api_key=os.getenv("OPENAI_API_KEY"))
    default_brd_path: str = "examples/sample_brd.docx"
    base_url: str = "http://localhost:8000"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Cached settings loader. Reads from environment variables where appropriate.
    """
    jira = JiraSettings(
        url=os.getenv("JIRA_URL"),
        username=os.getenv("JIRA_USERNAME"),
        api_token=os.getenv("JIRA_API_TOKEN"),
        project_key=os.getenv("JIRA_PROJECT_KEY"),
    )
    llm = LLMSettings(
        provider=os.getenv("LLM_PROVIDER", "openai"),
        model=os.getenv("LLM_MODEL", "gpt-4.1-mini"),
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    return Settings(jira=jira, llm=llm)

