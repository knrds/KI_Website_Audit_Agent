from __future__ import annotations

from pathlib import Path

import streamlit as st

from ai_report import create_report
from audit import run_audit
from models import WebsiteSignals


st.set_page_config(
    page_title="KI Website Audit Agent",
    page_icon="AI",
    layout="wide",
)


def main() -> None:
    st.title("KI-gestuetzter Website-Audit-Agent")
    st.caption("MVP: echte Website-Pruefung mit optionalem KI-Bericht")

    with st.sidebar:
        st.header("Audit starten")
        url = st.text_input("Website-URL", placeholder="https://example.com")
        prefer_ai = st.checkbox("KI-Bericht verwenden", value=True)
        start = st.button("Website analysieren", type="primary", use_container_width=True)

    if not start:
        st.info("Gib links eine URL ein und starte den Audit.")
        return

    if not url.strip():
        st.warning("Bitte gib zuerst eine Website-URL ein.")
        return

    with st.spinner("Website wird geladen und analysiert..."):
        signals = run_audit(url)
        report_result = create_report(signals, prefer_ai=prefer_ai)
        report = report_result.report

    score_col, status_col, source_col, load_col, url_col = st.columns([1, 1, 1, 1, 3])
    score_col.metric("Score", f"{report.score}/100")
    status_col.metric("Status", _status_label(signals))
    source_col.metric("Bericht", _report_source_label(report_result.source))
    load_col.metric("Ladezeit", _load_time_label(signals))
    url_col.write("Finale URL")
    url_col.code(signals.final_url or signals.url)

    if report_result.message:
        if report_result.source == "ai":
            st.success(report_result.message)
        else:
            st.info(report_result.message)

    st.subheader("Kurzfazit")
    st.write(report.summary)

    left_col, right_col = st.columns([2, 1])
    with left_col:
        st.subheader("Basischecks")
        st.dataframe(_build_check_rows(signals), hide_index=True, use_container_width=True)

    with right_col:
        st.subheader("Screenshot")
        if signals.screenshot_path and Path(signals.screenshot_path).exists():
            st.image(signals.screenshot_path, use_container_width=True)
            st.caption(signals.screenshot_path)
        else:
            st.warning("Kein Screenshot verfuegbar.")

    st.subheader("Wichtigste Probleme")
    for issue in report.key_issues:
        st.write(f"- {issue}")

    st.subheader("Verbesserungsvorschlaege")
    for recommendation in report.recommendations:
        with st.container(border=True):
            st.markdown(f"**{recommendation.title}**")
            st.write(f"Prioritaet: {recommendation.priority}")
            st.write(f"Business-Nutzen: {recommendation.business_value}")
            st.write(f"Konkrete Aktion: {recommendation.action}")

    with st.expander("Gemessene Rohdaten"):
        st.json(signals.model_dump(), expanded=True)

    if signals.notes:
        with st.expander("Technische Hinweise"):
            for note in signals.notes:
                st.write(f"- {note}")


def _status_label(signals: WebsiteSignals) -> str:
    if signals.status_code:
        return str(signals.status_code)
    return "nicht erreichbar"


def _load_time_label(signals: WebsiteSignals) -> str:
    if signals.load_time_ms is None:
        return "-"
    return f"{signals.load_time_ms} ms"


def _report_source_label(source: str) -> str:
    if source == "ai":
        return "KI"
    return "lokal"


def _build_check_rows(signals: WebsiteSignals) -> list[dict[str, str]]:
    return [
        {
            "Check": "Website erreichbar",
            "Status": _yes_no(signals.reachable),
            "Details": f"HTTP {signals.status_code}" if signals.status_code else "-",
        },
        {
            "Check": "Seitentitel",
            "Status": _yes_no(bool(signals.page_title)),
            "Details": signals.page_title or "-",
        },
        {
            "Check": "Meta Description",
            "Status": _yes_no(bool(signals.meta_description)),
            "Details": signals.meta_description or "-",
        },
        {
            "Check": "H1-Ueberschrift",
            "Status": _yes_no(bool(signals.h1)),
            "Details": signals.h1 or "-",
        },
        {
            "Check": "Call-to-Action",
            "Status": _yes_no(signals.has_call_to_action),
            "Details": ", ".join(signals.call_to_action_texts) or "-",
        },
        {
            "Check": "Impressum",
            "Status": _yes_no(signals.has_imprint),
            "Details": "gefunden" if signals.has_imprint else "-",
        },
        {
            "Check": "Datenschutzerklaerung",
            "Status": _yes_no(signals.has_privacy_policy),
            "Details": "gefunden" if signals.has_privacy_policy else "-",
        },
        {
            "Check": "Kontaktinformationen",
            "Status": _yes_no(signals.has_contact_info),
            "Details": ", ".join(signals.contact_signals) or "-",
        },
    ]


def _yes_no(value: bool) -> str:
    return "ja" if value else "nein"


if __name__ == "__main__":
    main()
