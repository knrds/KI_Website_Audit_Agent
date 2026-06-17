from __future__ import annotations

from html import escape
from pathlib import Path

import streamlit as st


def load_css(path: str = "assets/styles.css") -> None:
    css_path = Path(path)
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def icon(name: str, extra_class: str = "") -> str:
    return f'<span class="material-symbols-outlined {extra_class}">{escape(name)}</span>'


def render_topbar() -> None:
    st.markdown(
        f"""
        <div class="topbar">
            <div class="brand">
                <span class="brand-mark">{icon("query_stats")}</span>
                <span>Website Audit Agent</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer(start: bool = False) -> None:
    links = ["Datenschutz", "Impressum"] if start else ["Documentation", "Privacy Policy", "Support", "Terms of Service"]
    link_html = "".join(f'<a href="#">{escape(label)}</a>' for label in links)
    st.markdown(
        f"""
        <div class="footer-bar">
            <span>© 2024 Website Audit Agent. All rights reserved.</span>
            <span class="footer-links">{link_html}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_start_hero() -> None:
    st.markdown(
        f"""
        <div class="start-shell">
            <div class="start-inner">
                <div class="hero-mark">{icon("manage_search")}</div>
                <div class="headline-row">
                    <h1 class="app-title">Website Audit Agent</h1>
                    <span class="badge badge-primary">Portfolio MVP</span>
                </div>
                <p class="subtitle">KI-gestuetzte Website-Analyse fuer lokale Unternehmen</p>
        """,
        unsafe_allow_html=True,
    )


def render_start_hero_close() -> None:
    st.markdown(
        f"""
                <div class="hint-box">
                    {icon("info")}
                    <span>Analysiert SEO-Basics, CTA, Impressum, Kontaktinformationen und Website-Struktur.</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_loading_shell(progress: float, active_step: int) -> None:
    steps = [
        ("Website wird geladen", "Verbindung zur Ziel-URL wird hergestellt"),
        ("Screenshot wird erstellt", "Ansicht wird gerendert"),
        ("HTML wird analysiert", "SEO-, Local-SEO- und Conversion-Signale werden geprueft"),
        ("KI-Bericht wird erzeugt", "Empfehlungen werden priorisiert"),
    ]
    rows = []
    for index, (title, subtitle) in enumerate(steps, start=1):
        state = "done" if index < active_step else "active" if index == active_step else ""
        symbol = "check_circle" if index < active_step else "progress_activity" if index == active_step else "radio_button_unchecked"
        rows.append(
            f'<div class="step-item {state}"><span>{icon(symbol)}</span><div>'
            f"<div>{escape(title)}</div><small>{escape(subtitle)}</small></div></div>"
        )

    st.markdown(
        f"""
        <div class="loading-shell">
            <div class="loading-card section-card">
                <h1 class="loading-title">Analyse wird durchgefuehrt</h1>
                <p class="summary-text">
                    Bitte haben Sie einen Moment Geduld. Wir erfassen und evaluieren die Daten der Ziel-URL.
                </p>
                <div style="margin: 28px 0 8px;">
                    <div style="height: 10px; background: #eae6f4; border-radius: 999px; overflow: hidden;">
                        <div style="width: {max(0, min(progress, 1)) * 100:.0f}%; height: 100%; background: #4f46e5; border-radius: 999px;"></div>
                    </div>
                </div>
                <div class="step-list">{''.join(rows)}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    st.markdown(
        f"""
        <div class="side-nav">
            <h2>Audit Agent</h2>
            <p>Analytical SEO</p>
            <div class="nav-note">Nutze die Navigation in der linken Spalte fuer die MVP-Funktionen.</div>
            <div class="side-link active">{icon("dashboard")} Dashboard</div>
            <div class="side-link">{icon("history")} Audit History</div>
            <div class="side-link">{icon("query_stats")} SEO Tools</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_score_card(score: int, status_label: str, summary: str) -> None:
    color = score_color(score)
    circumference = 283
    offset = circumference - (circumference * max(0, min(score, 100)) / 100)
    st.markdown(
        f"""
        <div class="section-card score-card">
            <div style="text-align: right;"><span class="status-pill {score_status_class(score)}">{escape(status_label)}</span></div>
            <h2 class="card-title">Gesamt-Score</h2>
            <div class="score-ring-wrap">
                <svg viewBox="0 0 100 100" aria-hidden="true">
                    <circle cx="50" cy="50" r="45" fill="none" stroke="#e5e7eb" stroke-width="8"></circle>
                    <circle cx="50" cy="50" r="45" fill="none" stroke="{color}" stroke-width="8"
                        stroke-linecap="round" stroke-dasharray="{circumference}" stroke-dashoffset="{offset:.1f}"></circle>
                </svg>
                <div class="score-number">{score}<span>von 100</span></div>
            </div>
            <p class="summary-text">{escape(summary)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_preview_header() -> None:
    st.markdown(
        f"""
        <div class="section-card">
            <div class="card-title" style="justify-content: space-between;">
                <span>Website Preview</span>
                <span class="ghost-button" style="padding: 6px 10px;">{icon("desktop_windows")} Desktop</span>
            </div>
            <div class="preview-frame">
                <div class="browser-dots"><span class="dot-red"></span><span class="dot-amber"></span><span class="dot-green"></span></div>
        """,
        unsafe_allow_html=True,
    )


def render_preview_footer() -> None:
    st.markdown("</div></div>", unsafe_allow_html=True)


def render_preview_placeholder() -> None:
    st.markdown(
        f"""
        <div class="preview-placeholder">
            <div>
                {icon("image_not_supported")}
                <p>Kein Screenshot verfuegbar</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_checklist(checks: list[dict]) -> None:
    rows = []
    for item in checks:
        status = str(item.get("status", "unknown"))
        label = str(item.get("label", "Unbekannter Check"))
        rows.append(
            f'<div class="check-row"><div class="check-main">'
            f'<span class="{status_class(status)}">{icon(status_icon(status))}</span>'
            f"<span>{escape(label)}</span></div>"
            f'<span class="status-pill {status_class(status)}">{escape(status_label(status))}</span></div>'
        )
    st.markdown(
        f"""
        <div class="section-card">
            <h2 class="card-title">{icon("checklist")} Technische Checkliste</h2>
            {''.join(rows)}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_summary_card(title: str, text: str, icon_name: str) -> None:
    st.markdown(
        f"""
        <div class="section-card">
            <h2 class="card-title">{icon(icon_name)} {escape(title)}</h2>
            <p class="summary-text">{escape(text)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_outreach_card(text: str) -> None:
    st.markdown(
        f"""
        <div class="section-card">
            <h2 class="card-title">{icon("mail")} Outreach-Zusammenfassung</h2>
            <div class="outreach-box">{escape(text)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_recommendations(recommendations: list[dict]) -> None:
    cards = []
    for item in recommendations[:5]:
        priority = str(item.get("priority", "mittel")).lower()
        title = str(item.get("title", "Empfehlung"))
        reason = str(item.get("reason", item.get("action", "")))
        business_value = str(item.get("business_value", ""))
        cards.append(
            f'<div class="recommendation-card {priority_class(priority)}">'
            f'<span class="priority-pill {priority_status_class(priority)}">{escape(priority_label(priority))}</span>'
            f"<h3>{escape(title)}</h3><p>{escape(reason)}</p>"
            f"<p><strong>Business-Nutzen:</strong> {escape(business_value)}</p></div>"
        )
    st.markdown(
        f"""
        <h2 class="dashboard-title" style="margin-top: 34px;">Handlungsempfehlungen</h2>
        <div class="recommendation-grid">{''.join(cards)}</div>
        """,
        unsafe_allow_html=True,
    )


def render_error_intro(message: str | None = None) -> None:
    detail = message or "Der Audit Agent konnte keine Verbindung zur Zieladresse herstellen."
    st.markdown(
        f"""
        <div class="error-shell">
            <div class="error-content">
                <div class="error-mark">{icon("visibility_off")}</div>
                <h1 class="error-title">Website nicht erreichbar</h1>
                <p class="subtitle" style="margin-bottom: 0;">
                    {escape(detail)} Bitte ueberpruefen Sie die untenstehenden Fehlerquellen.
                </p>
        """,
        unsafe_allow_html=True,
    )


def render_error_reasons() -> None:
    reasons = [
        ("link_off", "URL ungueltig", "Die eingegebene Adresse enthaelt moeglicherweise Tippfehler oder die Domain existiert nicht mehr."),
        ("shield_locked", "Zugriff blockiert", "Die Website blockiert automatisierte Zugriffe, etwa durch Firewall, Bot-Schutz oder robots.txt."),
        ("hourglass_empty", "Zeitueberschreitung", "Der Zielserver hat innerhalb des definierten Zeitfensters nicht geantwortet."),
        ("gpp_bad", "SSL-/Verbindungsproblem", "DNS, Weiterleitung oder SSL/TLS-Verbindung konnten nicht sauber aufgebaut werden."),
    ]
    cards = []
    for icon_name, title, text in reasons:
        cards.append(
            f'<div class="reason-card"><span class="icon-button status-failed">{icon(icon_name)}</span>'
            f"<div><h3>{escape(title)}</h3><p>{escape(text)}</p></div></div>"
        )
    st.markdown(f'<div class="reason-grid">{"".join(cards)}</div>', unsafe_allow_html=True)


def render_error_close() -> None:
    st.markdown("</div></div>", unsafe_allow_html=True)


def status_label(status: str) -> str:
    return {
        "passed": "Bestanden",
        "warning": "Warnung",
        "failed": "Fehler",
        "unknown": "Unklar",
    }.get(status, "Unklar")


def status_icon(status: str) -> str:
    return {
        "passed": "check_circle",
        "warning": "warning",
        "failed": "error",
        "unknown": "help",
    }.get(status, "help")


def status_class(status: str) -> str:
    return {
        "passed": "status-passed",
        "warning": "status-warning",
        "failed": "status-failed",
        "unknown": "status-unknown",
    }.get(status, "status-unknown")


def score_color(score: int) -> str:
    if score >= 90:
        return "#059669"
    if score >= 50:
        return "#f59e0b"
    return "#ba1a1a"


def score_status_class(score: int) -> str:
    if score >= 90:
        return "status-passed"
    if score >= 50:
        return "status-warning"
    return "status-failed"


def priority_class(priority: str) -> str:
    return {"hoch": "high", "mittel": "medium", "niedrig": "low"}.get(priority, "medium")


def priority_status_class(priority: str) -> str:
    return {"hoch": "status-failed", "mittel": "status-warning", "niedrig": "status-passed"}.get(priority, "status-warning")


def priority_label(priority: str) -> str:
    return {"hoch": "Hoch", "mittel": "Mittel", "niedrig": "Niedrig"}.get(priority, "Mittel")
