from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path

import streamlit as st

from ai_report import create_report
from audit import run_audit
from models import AuditReport, Recommendation, WebsiteSignals
from ui import components
from ui.sample_data import sample_audit_result
from ui.state import ERROR, LOADING, SUCCESS, init_state, reset_to_idle, set_error, set_success
from utils import normalize_url


st.set_page_config(
    page_title="Website Audit Agent",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def main() -> None:
    components.load_css()
    init_state()

    view = st.session_state["view"]
    if view == SUCCESS and st.session_state.get("audit_result"):
        render_success_dashboard(st.session_state["audit_result"])
    elif view == ERROR:
        render_error_page()
    elif view == LOADING:
        run_analysis_flow(st.session_state.get("current_url", ""))
    else:
        render_start_screen()


def render_start_screen() -> None:
    components.render_start_hero()

    with st.form("audit_start_form", clear_on_submit=False):
        url_col, button_col = st.columns([3, 1])
        with url_col:
            url = st.text_input(
                "Website-URL",
                value=st.session_state.get("current_url", ""),
                placeholder="https://baeckerei-schmidt.de",
                label_visibility="collapsed",
            )
        with button_col:
            submitted = st.form_submit_button("Audit starten", type="primary", use_container_width=True)

    demo_col, _ = st.columns([1, 3])
    with demo_col:
        demo_clicked = st.button("Demo-Ergebnis anzeigen", use_container_width=True)

    components.render_start_hero_close()
    components.render_footer(start=True)

    if demo_clicked:
        set_success(sample_audit_result())
        st.rerun()

    if submitted:
        if not url.strip():
            st.warning("Bitte gib zuerst eine Website-URL ein.")
            return
        st.session_state["current_url"] = normalize_url(url.strip())
        st.session_state["view"] = LOADING
        st.rerun()


def run_analysis_flow(raw_url: str) -> None:
    url = normalize_url(raw_url)
    st.session_state["current_url"] = url

    components.render_topbar()
    loading_slot = st.empty()

    for progress, step in ((0.18, 1), (0.42, 2), (0.66, 3)):
        with loading_slot.container():
            components.render_loading_shell(progress=progress, active_step=step)
            st.button("Abbrechen", disabled=True, key=f"cancel_loading_{step}", use_container_width=False)
        time.sleep(0.25)

    try:
        signals = run_audit(url)
        with loading_slot.container():
            components.render_loading_shell(progress=0.88, active_step=4)
            st.button("Abbrechen", disabled=True, key="cancel_loading_report", use_container_width=False)

        report_result = create_report(signals, prefer_ai=True)
        if not signals.reachable:
            message = "; ".join(signals.notes) or "Die Website konnte nicht erfolgreich geladen werden."
            set_error(url, message)
        else:
            set_success(build_audit_view_data(signals, report_result.report, report_result.source))
    except Exception as exc:  # noqa: BLE001 - user-facing UI should never show a traceback
        set_error(url, str(exc))

    st.rerun()


def render_success_dashboard(result: dict) -> None:
    components.render_topbar()

    sidebar_col, main_col = st.columns([0.24, 0.76], gap="large")
    with sidebar_col:
        components.render_sidebar()

    with main_col:
        header_left, header_right = st.columns([1.4, 1])
        with header_left:
            st.markdown(
                f"""
                <div class="dashboard-header" style="margin-bottom: 4px;">
                    <div>
                        <h1 class="dashboard-title">Ergebnis-Dashboard</h1>
                        <div class="meta-row">
                            {components.icon("language")} <span>{result["url"]}</span>
                            <span>•</span>
                            {components.icon("calendar_today")} <span>{result["audit_date"]}</span>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with header_right:
            button_cols = st.columns(3)
            button_cols[0].button("PDF exportieren", disabled=True, use_container_width=True)
            button_cols[1].button("Audit speichern", disabled=True, use_container_width=True)
            if button_cols[2].button("Neue Website", type="primary", use_container_width=True):
                reset_to_idle()
                st.rerun()

        score_col, preview_col = st.columns([0.36, 0.64], gap="large")
        with score_col:
            components.render_score_card(
                score=result["score"],
                status_label=result["status_label"],
                summary=result["score_summary"],
            )
        with preview_col:
            preview_mode = st.radio(
                "Website Preview",
                ["Desktop", "Mobile"],
                horizontal=True,
                label_visibility="collapsed",
                key="preview_mode",
            )
            components.render_preview_header()
            screenshot = result.get("screenshot_path") if preview_mode == "Desktop" else None
            if screenshot and Path(screenshot).exists():
                st.image(screenshot, use_container_width=True)
            else:
                components.render_preview_placeholder()
            components.render_preview_footer()

        lower_left, lower_right = st.columns([0.58, 0.42], gap="large")
        with lower_left:
            components.render_checklist(result["checks"])
        with lower_right:
            components.render_summary_card("KI-Kurzfazit", result["ai_summary"], "auto_awesome")
            st.write("")
            components.render_outreach_card(result["outreach_text"])
            st.button("Text kopieren", disabled=True, use_container_width=True)

        components.render_recommendations(result["recommendations"])
        components.render_footer(start=False)


def render_error_page() -> None:
    components.render_topbar()
    message = st.session_state.get("error_message")
    current_url = st.session_state.get("current_url", "")

    components.render_error_intro(message)
    components.render_error_reasons()

    st.markdown('<div class="section-card" style="max-width: 720px; margin: 0 auto;">', unsafe_allow_html=True)
    with st.form("retry_form"):
        st.caption("Zu pruefende URL")
        url_col, button_col = st.columns([2, 1])
        with url_col:
            retry_url = st.text_input(
                "Zu pruefende URL",
                value=current_url,
                placeholder="https://example.com",
                label_visibility="collapsed",
            )
        with button_col:
            retry_clicked = st.form_submit_button("Erneut versuchen", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    components.render_error_close()
    components.render_footer(start=False)

    if retry_clicked:
        if retry_url.strip():
            st.session_state["current_url"] = normalize_url(retry_url.strip())
            st.session_state["view"] = LOADING
            st.rerun()
        else:
            st.warning("Bitte gib eine URL ein.")


def build_audit_view_data(signals: WebsiteSignals, report: AuditReport, source: str) -> dict:
    recommendations = [recommendation_to_view(item) for item in report.recommendations[:5]]
    while len(recommendations) < 5:
        recommendations.append(sample_audit_result()["recommendations"][len(recommendations)])

    return {
        "url": signals.final_url or signals.url,
        "audit_date": datetime.now().strftime("%d.%m.%Y, %H:%M Uhr"),
        "score": report.score,
        "status_label": score_status_label(report.score),
        "score_summary": report.summary,
        "screenshot_path": signals.screenshot_path,
        "checks": build_checks(signals),
        "ai_summary": report.summary if source == "ai" else build_local_summary(signals, report),
        "outreach_text": build_outreach_text(signals, report),
        "recommendations": recommendations,
    }


def recommendation_to_view(recommendation: Recommendation) -> dict:
    return {
        "priority": recommendation.priority,
        "title": recommendation.title,
        "reason": recommendation.action,
        "business_value": recommendation.business_value,
    }


def build_checks(signals: WebsiteSignals) -> list[dict[str, str]]:
    return [
        {"label": "Website erreichbar", "status": "passed" if signals.reachable else "failed"},
        {"label": "Seitentitel vorhanden", "status": "passed" if signals.page_title else "failed"},
        {"label": "Meta Description vorhanden", "status": meta_status(signals)},
        {"label": "H1 vorhanden", "status": h1_status(signals)},
        {"label": "CTA erkannt", "status": cta_status(signals)},
        {"label": "Impressum gefunden", "status": "passed" if signals.has_imprint else "failed"},
        {"label": "Datenschutzerklaerung gefunden", "status": "passed" if signals.has_privacy_policy else "failed"},
        {"label": "Kontaktinformationen gefunden", "status": "passed" if signals.has_contact_info else "failed"},
        {"label": "Screenshot erstellt", "status": "passed" if signals.screenshot_path else "failed"},
    ]


def meta_status(signals: WebsiteSignals) -> str:
    if not signals.meta_description:
        return "failed"
    if (
        80 <= signals.meta_description_length <= 170
        and signals.meta_description_has_benefit
        and signals.meta_description_has_cta
    ):
        return "passed"
    return "warning"


def h1_status(signals: WebsiteSignals) -> str:
    if signals.h1_count == 1:
        return "passed"
    if signals.h1_count > 1:
        return "warning"
    return "failed"


def cta_status(signals: WebsiteSignals) -> str:
    if signals.has_strong_call_to_action:
        return "passed"
    if signals.has_call_to_action:
        return "warning"
    return "failed"


def score_status_label(score: int) -> str:
    if score >= 90:
        return "Stark: Gute Grundlage"
    if score >= 50:
        return "Warnung: Optimierung empfohlen"
    return "Kritisch: Hoher Handlungsbedarf"


def build_local_summary(signals: WebsiteSignals, report: AuditReport) -> str:
    problem_count = len([item for item in report.key_issues if item])
    return (
        f"Die Website wurde mit {report.score}/100 bewertet. Es wurden {problem_count} relevante SEO-, "
        "Local-SEO- und Conversion-Themen erkannt, die vor allem Auffindbarkeit und Anfragequote betreffen."
    )


def build_outreach_text(signals: WebsiteSignals, report: AuditReport) -> str:
    first_issue = report.key_issues[0] if report.key_issues else "mehrere Optimierungspotenziale sichtbar sind"
    first_recommendation = report.recommendations[0].title if report.recommendations else "die Website gezielter optimieren"
    return (
        "Hallo,\n\n"
        f"mir ist bei Ihrer Website {signals.final_url or signals.url} aufgefallen, dass {first_issue}. "
        f"Ein schneller Hebel waere: {first_recommendation}. Dadurch koennte die Seite mehr lokale Besucher "
        "in konkrete Anfragen, Anrufe oder Termine verwandeln.\n\n"
        "Gerne zeige ich Ihnen kurz, welche drei Anpassungen den groessten Effekt haetten."
    )


if __name__ == "__main__":
    main()
