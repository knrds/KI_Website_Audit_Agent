from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


Priority = Literal["hoch", "mittel", "niedrig"]


class WebsiteSignals(BaseModel):
    """Raw website facts collected by the audit module."""

    url: str
    final_url: str | None = None
    reachable: bool = False
    status_code: int | None = None
    load_time_ms: int | None = None
    page_title: str | None = None
    meta_description: str | None = None
    h1: str | None = None
    h1_count: int = 0
    has_call_to_action: bool = False
    call_to_action_texts: list[str] = Field(default_factory=list)
    has_imprint: bool = False
    has_privacy_policy: bool = False
    has_contact_info: bool = False
    contact_signals: list[str] = Field(default_factory=list)
    screenshot_path: str | None = None
    notes: list[str] = Field(default_factory=list)


class Recommendation(BaseModel):
    """One concrete improvement suggested in the audit report."""

    title: str
    priority: Priority
    business_value: str
    action: str


class AuditReport(BaseModel):
    """Structured report shown in the Streamlit prototype."""

    summary: str
    score: int = Field(ge=0, le=100)
    key_issues: list[str] = Field(default_factory=list)
    recommendations: list[Recommendation] = Field(default_factory=list)
