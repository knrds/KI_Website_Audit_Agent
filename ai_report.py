from __future__ import annotations

import json
import os

from pydantic import ValidationError

from models import AuditReport, Recommendation, ReportGenerationResult, WebsiteSignals


SYSTEM_PROMPT = """\
Du bist ein strenger SEO- und Conversion-Audit-Assistent fuer lokale Unternehmen.

Regeln:
- Bewerte ausschliesslich die gemessenen Website-Daten aus dem JSON.
- Erfinde keine Inhalte, Rechtsdetails, Lighthouse-Werte, Unterseiten oder Branchenfakten.
- Wenn ein Signal fehlt oder unsicher ist, benenne es als fehlend oder unklar.
- Bewerte streng: Vorhanden reicht nicht; Signale muessen Kunden gewinnen helfen.
- Empfehlungen muessen konkret erklaeren, wie mehr Anfragen, Anrufe oder Buchungen entstehen.
- Priorisiere lokales SEO, Suchsnippet, klare Leistung, Trust, Kontaktwege und Call-to-Action.
- Gib genau ein JSON-Objekt zurueck, ohne Markdown und ohne Erklaertext.
- Das JSON muss die Felder summary, score, key_issues und recommendations enthalten.
- score ist eine ganze Zahl von 0 bis 100.
- recommendations enthaelt maximal 5 Eintraege.
- Jede recommendation hat title, priority, business_value und action.
- priority ist genau einer dieser Werte: hoch, mittel, niedrig.
"""


def create_report(signals: WebsiteSignals, prefer_ai: bool = True) -> ReportGenerationResult:
    """Create an AI report when possible, otherwise return the local fallback."""

    if prefer_ai:
        try:
            report = create_ai_report(signals)
            return ReportGenerationResult(
                report=report,
                source="ai",
                message="KI-Bericht wurde erfolgreich erzeugt.",
            )
        except Exception as exc:  # noqa: BLE001 - fallback should catch provider/runtime issues
            fallback = create_local_report(signals)
            return ReportGenerationResult(
                report=fallback,
                source="local",
                message=f"Lokaler Bericht genutzt: {exc}",
            )

    return ReportGenerationResult(
        report=create_local_report(signals),
        source="local",
        message="Lokaler Bericht wurde manuell ausgewaehlt.",
    )


def create_ai_report(signals: WebsiteSignals) -> AuditReport:
    """Generate a structured report with the OpenAI SDK or a compatible API."""

    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        raise RuntimeError("OPENAI_API_KEY fehlt oder ist noch ein Platzhalter.")

    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("OpenAI-Paket ist nicht installiert. Bitte requirements.txt installieren.") from exc

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    base_url = os.getenv("OPENAI_BASE_URL") or None
    client = OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": _build_user_prompt(signals)},
    ]

    parse_method = getattr(client.chat.completions, "parse", None)
    if parse_method:
        try:
            completion = parse_method(
                model=model,
                messages=messages,
                response_format=AuditReport,
                temperature=0.15,
            )
            parsed = completion.choices[0].message.parsed
            if parsed:
                return _normalize_report(AuditReport.model_validate(parsed), signals)
        except Exception:
            pass

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.15,
    )
    content = completion.choices[0].message.content
    if not content:
        raise RuntimeError("KI-Antwort war leer.")

    return _normalize_report(_parse_report_content(content), signals)


def create_local_report(signals: WebsiteSignals) -> AuditReport:
    """Create a strict deterministic SEO and conversion report from measured signals."""

    score = _calculate_score(signals)
    if signals.reachable:
        summary = (
            f"Die Website {signals.url} ist erreichbar. Der strenge SEO- und Conversion-Score liegt bei "
            f"{score}/100; bewertet wurden Auffindbarkeit, lokaler Kontext, Vertrauen und Anfragewahrscheinlichkeit."
        )
    else:
        summary = (
            f"Die Website {signals.url} konnte nicht erfolgreich geprueft werden. "
            "Bitte URL, Zertifikat, Hosting oder Weiterleitungen kontrollieren."
        )

    return AuditReport(
        summary=summary,
        score=score,
        key_issues=_collect_issues(signals),
        recommendations=_build_recommendations(signals),
    )


def create_placeholder_report(signals: WebsiteSignals) -> AuditReport:
    """Backward-compatible wrapper for the first prototype."""

    return create_local_report(signals)


def _build_user_prompt(signals: WebsiteSignals) -> str:
    payload = {
        "task": "Erstelle einen strengen Website-Audit-Bericht fuer ein lokales Unternehmen.",
        "website_signals": signals.model_dump(),
        "scoring_context": (
            "Der Score soll SEO-Qualitaet und Kundengewinnung bewerten. Kritisch sind lokale Suchintention, "
            "klares Leistungsangebot, Title/Meta-Qualitaet, starke CTAs, Kontaktwege, Vertrauen, strukturierte "
            "Daten und ausreichende Content-Tiefe."
        ),
        "output_contract": {
            "summary": "Kurzes Fazit in 1-2 Saetzen.",
            "score": "Strenger Integer 0-100 auf Basis der gemessenen Signale.",
            "key_issues": "Liste der wichtigsten Probleme, nur aus gemessenen Daten ableiten.",
            "recommendations": "Maximal 5 konkrete Vorschlaege mit Prioritaet, Business-Nutzen und Umsetzungsaktion.",
        },
    }
    return json.dumps(payload, ensure_ascii=True, indent=2)


def _parse_report_content(content: str) -> AuditReport:
    cleaned = content.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        return AuditReport.model_validate_json(cleaned)
    except ValidationError as exc:
        raise RuntimeError(f"KI-Antwort passte nicht zum AuditReport-Schema: {exc}") from exc


def _normalize_report(report: AuditReport, signals: WebsiteSignals) -> AuditReport:
    local_report = create_local_report(signals)

    recommendations = report.recommendations[:5]
    existing_titles = {recommendation.title for recommendation in recommendations}
    for recommendation in local_report.recommendations:
        if len(recommendations) >= 5:
            break
        if recommendation.title not in existing_titles:
            recommendations.append(recommendation)
            existing_titles.add(recommendation.title)

    return AuditReport(
        summary=report.summary or local_report.summary,
        score=max(0, min(report.score, 100)),
        key_issues=(report.key_issues or local_report.key_issues)[:10],
        recommendations=recommendations,
    )


def _calculate_score(signals: WebsiteSignals) -> int:
    if not signals.reachable:
        return 0

    score = 0

    score += 8
    if signals.status_code and 200 <= signals.status_code < 400:
        score += 4
    if not signals.has_noindex:
        score += 6
    if signals.has_viewport_meta:
        score += 3
    if signals.load_time_ms is not None and signals.load_time_ms <= 3500:
        score += 4

    if signals.page_title:
        score += 4
    if 30 <= signals.title_length <= 65:
        score += 5
    if signals.title_has_business_keyword:
        score += 3
    if signals.title_has_local_keyword:
        score += 3

    if signals.meta_description:
        score += 4
    if 80 <= signals.meta_description_length <= 170:
        score += 5
    if signals.meta_description_has_benefit:
        score += 3
    if signals.meta_description_has_cta:
        score += 3

    if signals.h1_count == 1:
        score += 6
    if signals.h2_count >= 2:
        score += 3
    if signals.word_count >= 500:
        score += 8
    elif signals.word_count >= 250:
        score += 4

    if signals.has_call_to_action:
        score += 4
    if signals.has_strong_call_to_action:
        score += 8
    if signals.has_contact_info:
        score += 5
    if signals.has_address:
        score += 5
    if signals.has_opening_hours:
        score += 3

    if signals.has_local_seo_signals:
        score += 4
    if signals.has_service_keywords:
        score += 4
    if signals.has_trust_signals:
        score += 5
    if signals.has_reviews_or_testimonials:
        score += 4
    if signals.has_offer_or_price_signal:
        score += 2

    if signals.has_structured_data:
        score += 2
    if signals.has_local_business_schema:
        score += 6
    if signals.has_canonical:
        score += 2
    if signals.has_open_graph:
        score += 2
    if signals.internal_link_count >= 5:
        score += 2
    if signals.image_count and signals.images_missing_alt / signals.image_count <= 0.25:
        score += 2
    if signals.has_imprint:
        score += 2
    if signals.has_privacy_policy:
        score += 2
    if signals.screenshot_path:
        score += 1

    return min(score, 100)


def _collect_issues(signals: WebsiteSignals) -> list[str]:
    issues: list[str] = []

    if not signals.reachable:
        issues.append("Die Website war nicht erfolgreich erreichbar.")
    if signals.has_noindex:
        issues.append("Die Seite enthaelt ein Noindex-Signal und kann dadurch aus Suchergebnissen verschwinden.")
    if not signals.page_title:
        issues.append("Es wurde kein Seitentitel gefunden.")
    elif not 30 <= signals.title_length <= 65:
        issues.append(f"Der Seitentitel ist mit {signals.title_length} Zeichen nicht optimal fuer Suchergebnisse.")
    if signals.page_title and not signals.title_has_business_keyword:
        issues.append("Der Seitentitel nennt Leistung oder Angebot nicht klar genug.")
    if signals.page_title and not signals.title_has_local_keyword:
        issues.append("Der Seitentitel enthaelt keinen klaren lokalen Bezug.")
    if not signals.meta_description:
        issues.append("Es wurde keine Meta Description gefunden.")
    elif not 80 <= signals.meta_description_length <= 170:
        issues.append(
            f"Die Meta Description ist mit {signals.meta_description_length} Zeichen nicht stark genug ausbalanciert."
        )
    if signals.meta_description and not signals.meta_description_has_benefit:
        issues.append("Die Meta Description nennt keinen klaren Kundennutzen.")
    if signals.meta_description and not signals.meta_description_has_cta:
        issues.append("Die Meta Description enthaelt keine klare Handlungsaufforderung.")
    if not signals.h1:
        issues.append("Es wurde keine H1-Ueberschrift gefunden.")
    elif signals.h1_count > 1:
        issues.append(f"Es wurden {signals.h1_count} H1-Ueberschriften gefunden.")
    if signals.word_count < 250:
        issues.append(f"Die Startseite hat sehr wenig sichtbaren Text ({signals.word_count} Woerter).")
    if not signals.has_call_to_action:
        issues.append("Es wurde kein klarer Call-to-Action erkannt.")
    elif not signals.has_strong_call_to_action:
        issues.append("Es gibt CTA-Signale, aber keinen starken Anfrage- oder Buchungs-CTA.")
    if not signals.has_contact_info:
        issues.append("Es wurden keine klaren Kontaktinformationen erkannt.")
    if not signals.has_address:
        issues.append("Es wurde keine klare lokale Adresse erkannt.")
    if not signals.has_opening_hours:
        issues.append("Es wurden keine Oeffnungszeiten erkannt.")
    if not signals.has_trust_signals:
        issues.append("Es wurden keine starken Vertrauenssignale wie Bewertungen, Referenzen oder Erfahrung erkannt.")
    if not signals.has_local_business_schema:
        issues.append("Es wurde kein LocalBusiness Structured Data erkannt.")
    if signals.image_count and signals.images_missing_alt:
        issues.append(f"{signals.images_missing_alt} von {signals.image_count} Bildern haben keinen Alt-Text.")
    if not signals.has_imprint:
        issues.append("Es wurde kein Impressum erkannt.")
    if not signals.has_privacy_policy:
        issues.append("Es wurde keine Datenschutzerklaerung erkannt.")
    if not signals.screenshot_path:
        issues.append("Es konnte kein Screenshot gespeichert werden.")

    issues.extend(signals.seo_warnings)
    return _deduplicate(issues)[:10] or ["Keine kritischen Basisprobleme erkannt."]


def _build_recommendations(signals: WebsiteSignals) -> list[Recommendation]:
    recommendations: list[Recommendation] = []

    if not signals.reachable:
        recommendations.append(
            Recommendation(
                title="Erreichbarkeit sofort sicherstellen",
                priority="hoch",
                business_value="Jede technische Nichterreichbarkeit kostet direkte Anfragen und verhindert SEO-Wirkung.",
                action="Hosting, Domain, SSL-Zertifikat, Weiterleitungen und Serverantwort pruefen.",
            )
        )

    if (
        not signals.page_title
        or not 30 <= signals.title_length <= 65
        or not signals.title_has_business_keyword
        or not signals.title_has_local_keyword
        or not signals.meta_description
        or not 80 <= signals.meta_description_length <= 170
        or not signals.meta_description_has_benefit
        or not signals.meta_description_has_cta
    ):
        recommendations.append(
            Recommendation(
                title="Suchsnippet auf kaufbereite lokale Suche ausrichten",
                priority="hoch",
                business_value=(
                    "Ein besseres Snippet steigert die Klickrate bei Menschen, die bereits nach einer lokalen "
                    "Leistung suchen und damit besonders nah an einer Anfrage sind."
                ),
                action=(
                    "Title nach dem Muster 'Leistung in Ort | Marke' formulieren. Meta Description mit Nutzen, "
                    "Einzugsgebiet und CTA schreiben, z. B. 'Schnelle Beratung in [Ort] - jetzt Termin anfragen'."
                ),
            )
        )

    if not signals.h1 or signals.h1_count > 1 or not signals.has_service_keywords or signals.word_count < 500:
        recommendations.append(
            Recommendation(
                title="Startseite auf Angebot, Ort und Entscheidungsgruende fokussieren",
                priority="hoch",
                business_value=(
                    "Besucher entscheiden in Sekunden, ob die Website ihr Problem loest. Mehr relevante Inhalte "
                    "helfen gleichzeitig Suchmaschinen, die Leistung und den lokalen Bezug zu verstehen."
                ),
                action=(
                    "Eine einzige H1 mit Leistung und Ort setzen. Darunter 3-5 Leistungsbereiche, typische "
                    "Kundenprobleme, Ablauf, Einzugsgebiet und klare Gruende fuer die Beauftragung ergaenzen."
                ),
            )
        )

    if not signals.has_strong_call_to_action:
        recommendations.append(
            Recommendation(
                title="Anfrage-CTA sichtbarer und verbindlicher machen",
                priority="hoch",
                business_value=(
                    "Ein starker CTA reduziert Reibung und verwandelt mehr Besucher in Anrufe, Termine oder "
                    "Angebotsanfragen."
                ),
                action=(
                    "Im sichtbaren Startbereich und nach jedem Leistungsblock Buttons wie 'Kostenloses Angebot "
                    "anfragen', 'Termin buchen' oder 'Jetzt anrufen' platzieren. Telefonnummer mobil klickbar machen."
                ),
            )
        )

    if not signals.has_contact_info or not signals.has_address or not signals.has_opening_hours:
        recommendations.append(
            Recommendation(
                title="Lokale Kontakt- und NAP-Signale vollstaendig machen",
                priority="hoch",
                business_value=(
                    "Vollstaendige Kontaktinformationen schaffen Vertrauen und helfen lokalen Kunden, sofort "
                    "den naechsten Schritt zu gehen."
                ),
                action=(
                    "Name, Adresse, Telefonnummer, E-Mail, Oeffnungszeiten und Einzugsgebiet konsistent im Footer "
                    "und Kontaktbereich zeigen. Telefon und E-Mail als klickbare Links auszeichnen."
                ),
            )
        )

    if not signals.has_trust_signals or not signals.has_reviews_or_testimonials:
        recommendations.append(
            Recommendation(
                title="Trust-Beweise direkt neben CTAs zeigen",
                priority="hoch",
                business_value=(
                    "Bewertungen, Referenzen und Erfahrung senken Unsicherheit. Das ist oft der Unterschied "
                    "zwischen Absprung und Anfrage."
                ),
                action=(
                    "Google-Bewertungen, Kundenstimmen, Referenzprojekte, Zertifikate, Meistertitel oder Jahre "
                    "Erfahrung sichtbar einbauen. Neben jedem CTA ein kurzes Trust-Element platzieren."
                ),
            )
        )

    if not signals.has_local_business_schema or not signals.has_structured_data:
        recommendations.append(
            Recommendation(
                title="LocalBusiness Structured Data ergaenzen",
                priority="mittel",
                business_value=(
                    "Strukturierte Daten helfen Suchmaschinen, Unternehmen, Adresse, Telefon, Oeffnungszeiten "
                    "und Leistungsbereich eindeutig zu interpretieren."
                ),
                action=(
                    "JSON-LD fuer LocalBusiness oder passenden Subtyp einbauen: Name, URL, Telefon, Adresse, "
                    "Oeffnungszeiten, Logo, Bild und sameAs-Profile."
                ),
            )
        )

    if signals.image_count and signals.images_missing_alt:
        recommendations.append(
            Recommendation(
                title="Bilder fuer SEO und Verkauf staerker nutzen",
                priority="mittel",
                business_value=(
                    "Beschreibende Bildtexte helfen Barrierefreiheit, Bildsuche und Vertrauen, besonders bei "
                    "lokalen Leistungen mit sichtbaren Ergebnissen."
                ),
                action=(
                    "Fehlende Alt-Texte mit konkreten Motiven, Leistung und Ort ergaenzen. Referenzbilder mit "
                    "Projektbeschreibung und Ergebnisnutzen kombinieren."
                ),
            )
        )

    fallback_recommendations = [
        Recommendation(
            title="Landingpage fuer wichtigste Geldleistung bauen",
            priority="hoch",
            business_value=(
                "Eine eigene, fokussierte Seite fuer die profitabelste Leistung kann mehr qualifizierte Anfragen "
                "bringen als eine allgemeine Startseite."
            ),
            action=(
                "Top-Leistung waehlen und eine Seite mit Problem, Leistung, Ort, Ablauf, Preisen/Angebot, FAQ, "
                "Referenzen und CTA erstellen."
            ),
        ),
        Recommendation(
            title="FAQ mit echten Kaufbarrieren ergaenzen",
            priority="mittel",
            business_value="Antworten auf Preis-, Ablauf- und Verfuegbarkeitsfragen reduzieren Zweifel vor der Anfrage.",
            action="5-8 Fragen beantworten: Kosten, Dauer, Gebiet, Terminvergabe, Garantie, Vorbereitung und Notfaelle.",
        ),
        Recommendation(
            title="Interne Verlinkung auf Leistungen und Kontakt verbessern",
            priority="mittel",
            business_value="Klare interne Wege helfen Nutzern und Suchmaschinen, die wichtigsten Angebotsseiten zu finden.",
            action="Von Startseite, Leistungsuebersicht und Footer auf Kernleistungen, Referenzen und Kontakt verlinken.",
        ),
        Recommendation(
            title="Angebot mit Risiko-Reduktion formulieren",
            priority="mittel",
            business_value="Konkrete Garantien, klare naechste Schritte und transparente Erwartungen erhoehen Vertrauen.",
            action="Formulierungen wie 'kostenlose Ersteinschaetzung', 'Antwort innerhalb von 24h' oder 'Festpreisangebot' pruefen.",
        ),
        Recommendation(
            title="Mobile Darstellung manuell pruefen",
            priority="niedrig",
            business_value="Viele lokale Besucher kommen ueber Smartphones und erwarten schnelle Kontaktwege.",
            action="Startseite auf Smartphone-Breite pruefen und besonders Header, CTA und Kontaktbereich kontrollieren.",
        ),
    ]

    existing_titles = {recommendation.title for recommendation in recommendations}
    for recommendation in fallback_recommendations:
        if recommendation.title not in existing_titles:
            recommendations.append(recommendation)
            existing_titles.add(recommendation.title)
        if len(recommendations) >= 5:
            break

    return recommendations[:5]


def _deduplicate(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result
