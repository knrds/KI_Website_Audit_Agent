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
        st.subheader("Audit-Checks")
        tabs = st.tabs(["Basis", "SEO", "Local SEO", "Conversion"])
        with tabs[0]:
            st.dataframe(_build_basic_rows(signals), hide_index=True, use_container_width=True)
        with tabs[1]:
            st.dataframe(_build_seo_rows(signals), hide_index=True, use_container_width=True)
        with tabs[2]:
            st.dataframe(_build_local_rows(signals), hide_index=True, use_container_width=True)
        with tabs[3]:
            st.dataframe(_build_conversion_rows(signals), hide_index=True, use_container_width=True)

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

    if signals.seo_warnings:
        with st.expander("Strenge SEO-Warnungen"):
            for warning in signals.seo_warnings:
                st.write(f"- {warning}")

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


def _build_basic_rows(signals: WebsiteSignals) -> list[dict[str, str]]:
    return [
        {
            "Check": "Website erreichbar",
            "Status": _yes_no(signals.reachable),
            "Details": f"HTTP {signals.status_code}" if signals.status_code else "-",
        },
        {
            "Check": "Seitentitel",
            "Status": _yes_no(bool(signals.page_title)),
            "Details": _with_length(signals.page_title, signals.title_length),
        },
        {
            "Check": "Meta Description",
            "Status": _yes_no(bool(signals.meta_description)),
            "Details": _with_length(signals.meta_description, signals.meta_description_length),
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
    ]


def _build_seo_rows(signals: WebsiteSignals) -> list[dict[str, str]]:
    return [
        {
            "Check": "Title-Laenge",
            "Status": _yes_no(30 <= signals.title_length <= 65),
            "Details": f"{signals.title_length} Zeichen",
        },
        {
            "Check": "Title nennt Leistung",
            "Status": _yes_no(signals.title_has_business_keyword),
            "Details": "Leistung/Angebot im Titelkontext erkannt" if signals.title_has_business_keyword else "-",
        },
        {
            "Check": "Meta-Laenge",
            "Status": _yes_no(80 <= signals.meta_description_length <= 170),
            "Details": f"{signals.meta_description_length} Zeichen",
        },
        {
            "Check": "Meta mit Nutzen",
            "Status": _yes_no(signals.meta_description_has_benefit),
            "Details": "Nutzenbegriff erkannt" if signals.meta_description_has_benefit else "-",
        },
        {
            "Check": "Meta mit CTA",
            "Status": _yes_no(signals.meta_description_has_cta),
            "Details": "CTA-Begriff erkannt" if signals.meta_description_has_cta else "-",
        },
        {
            "Check": "H1-Struktur",
            "Status": _yes_no(signals.h1_count == 1),
            "Details": f"{signals.h1_count} H1, {signals.h2_count} H2",
        },
        {
            "Check": "Content-Tiefe",
            "Status": _yes_no(signals.word_count >= 500),
            "Details": f"{signals.word_count} sichtbare Woerter",
        },
        {
            "Check": "Canonical",
            "Status": _yes_no(signals.has_canonical),
            "Details": "gefunden" if signals.has_canonical else "-",
        },
        {
            "Check": "Noindex",
            "Status": "kritisch" if signals.has_noindex else "ok",
            "Details": "Noindex gefunden" if signals.has_noindex else "kein Noindex erkannt",
        },
        {
            "Check": "Open Graph",
            "Status": _yes_no(signals.has_open_graph),
            "Details": "og:title, og:description und og:image erkannt" if signals.has_open_graph else "-",
        },
        {
            "Check": "Bilder Alt-Texte",
            "Status": _yes_no(not signals.image_count or signals.images_missing_alt / signals.image_count <= 0.25),
            "Details": f"{signals.images_missing_alt} ohne Alt bei {signals.image_count} Bildern",
        },
        {
            "Check": "Interne Links",
            "Status": _yes_no(signals.internal_link_count >= 5),
            "Details": f"{signals.internal_link_count} intern, {signals.external_link_count} extern",
        },
    ]


def _build_local_rows(signals: WebsiteSignals) -> list[dict[str, str]]:
    return [
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
        {
            "Check": "Adresse",
            "Status": _yes_no(signals.has_address),
            "Details": "Adresse/PLZ erkannt" if signals.has_address else "-",
        },
        {
            "Check": "Oeffnungszeiten",
            "Status": _yes_no(signals.has_opening_hours),
            "Details": "gefunden" if signals.has_opening_hours else "-",
        },
        {
            "Check": "Lokale Signale",
            "Status": _yes_no(signals.has_local_seo_signals),
            "Details": ", ".join(signals.local_seo_signals) or "-",
        },
        {
            "Check": "Structured Data",
            "Status": _yes_no(signals.has_structured_data),
            "Details": ", ".join(signals.structured_data_types) or "-",
        },
        {
            "Check": "LocalBusiness Schema",
            "Status": _yes_no(signals.has_local_business_schema),
            "Details": "gefunden" if signals.has_local_business_schema else "-",
        },
    ]


def _build_conversion_rows(signals: WebsiteSignals) -> list[dict[str, str]]:
    return [
        {
            "Check": "Starker CTA",
            "Status": _yes_no(signals.has_strong_call_to_action),
            "Details": ", ".join(signals.strong_call_to_action_texts) or "-",
        },
        {
            "Check": "Leistungsangebot",
            "Status": _yes_no(signals.has_service_keywords),
            "Details": ", ".join(signals.service_signals) or "-",
        },
        {
            "Check": "Trust-Signale",
            "Status": _yes_no(signals.has_trust_signals),
            "Details": ", ".join(signals.trust_signals) or "-",
        },
        {
            "Check": "Bewertungen/Testimonials",
            "Status": _yes_no(signals.has_reviews_or_testimonials),
            "Details": "gefunden" if signals.has_reviews_or_testimonials else "-",
        },
        {
            "Check": "Angebot/Preis-Signal",
            "Status": _yes_no(signals.has_offer_or_price_signal),
            "Details": "gefunden" if signals.has_offer_or_price_signal else "-",
        },
        {
            "Check": "Mobile Viewport",
            "Status": _yes_no(signals.has_viewport_meta),
            "Details": "gefunden" if signals.has_viewport_meta else "-",
        },
    ]


def _yes_no(value: bool) -> str:
    return "ja" if value else "nein"


def _with_length(value: str | None, length: int) -> str:
    if not value:
        return "-"
    return f"{value} ({length} Zeichen)"


if __name__ == "__main__":
    main()
