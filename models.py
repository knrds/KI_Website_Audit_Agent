from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


Priority = Literal["hoch", "mittel", "niedrig"]
ReportSource = Literal["ai", "local"]


class WebsiteSignals(BaseModel):
    """Raw website facts collected by the audit module."""

    url: str
    final_url: str | None = None
    reachable: bool = False
    status_code: int | None = None
    load_time_ms: int | None = None
    page_title: str | None = None
    title_length: int = 0
    title_has_business_keyword: bool = False
    title_has_local_keyword: bool = False
    meta_description: str | None = None
    meta_description_length: int = 0
    meta_description_has_benefit: bool = False
    meta_description_has_cta: bool = False
    h1: str | None = None
    h1_count: int = 0
    h2_count: int = 0
    word_count: int = 0
    has_call_to_action: bool = False
    call_to_action_texts: list[str] = Field(default_factory=list)
    has_strong_call_to_action: bool = False
    strong_call_to_action_texts: list[str] = Field(default_factory=list)
    has_imprint: bool = False
    has_privacy_policy: bool = False
    has_contact_info: bool = False
    contact_signals: list[str] = Field(default_factory=list)
    has_address: bool = False
    has_opening_hours: bool = False
    has_local_seo_signals: bool = False
    local_seo_signals: list[str] = Field(default_factory=list)
    has_service_keywords: bool = False
    service_signals: list[str] = Field(default_factory=list)
    has_trust_signals: bool = False
    trust_signals: list[str] = Field(default_factory=list)
    has_reviews_or_testimonials: bool = False
    has_offer_or_price_signal: bool = False
    has_viewport_meta: bool = False
    has_canonical: bool = False
    has_noindex: bool = False
    has_open_graph: bool = False
    has_structured_data: bool = False
    structured_data_types: list[str] = Field(default_factory=list)
    has_local_business_schema: bool = False
    internal_link_count: int = 0
    external_link_count: int = 0
    image_count: int = 0
    images_missing_alt: int = 0
    seo_warnings: list[str] = Field(default_factory=list)
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


class ReportGenerationResult(BaseModel):
    """Report plus metadata about how it was generated."""

    report: AuditReport
    source: ReportSource
    message: str | None = None
