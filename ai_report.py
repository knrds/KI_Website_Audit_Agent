from __future__ import annotations

import json
import os

from pydantic import ValidationError

from models import AuditReport, Recommendation, ReportGenerationResult, WebsiteSignals


SYSTEM_PROMPT = """\
Du bist ein pragmatischer Website-Audit-Assistent fuer lokale Unternehmen.

Regeln:
- Bewerte ausschliesslich die gemessenen Website-Daten aus dem JSON.
- Erfinde keine Inhalte, Rechtsdetails, Lighthouse-Werte, Unterseiten oder Branchenfakten.
- Wenn ein Signal fehlt oder unsicher ist, benenne es als fehlend oder unklar.
- Schreibe kurz, konkret und business-orientiert.
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
                temperature=0.2,
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
        temperature=0.2,
    )
    content = completion.choices[0].message.content
    if not content:
        raise RuntimeError("KI-Antwort war leer.")

    return _normalize_report(_parse_report_content(content), signals)


def create_local_report(signals: WebsiteSignals) -> AuditReport:
    """Create a deterministic report from measured signals."""

    issues = _collect_issues(signals)
    recommendations = _build_recommendations(signals)
    score = _calculate_score(signals)

    if signals.reachable:
        summary = (
            f"Die Website {signals.url} ist erreichbar und wurde automatisiert geprueft. "
            f"Der aktuelle Basis-Score liegt bei {score}/100."
        )
    else:
        summary = (
            f"Die Website {signals.url} konnte nicht erfolgreich geprueft werden. "
            "Bitte URL, Zertifikat oder Erreichbarkeit kontrollieren."
        )

    return AuditReport(
        summary=summary,
        score=score,
        key_issues=issues,
        recommendations=recommendations,
    )


def create_placeholder_report(signals: WebsiteSignals) -> AuditReport:
    """Backward-compatible wrapper for the first prototype."""

    return create_local_report(signals)


def _build_user_prompt(signals: WebsiteSignals) -> str:
    payload = {
        "task": "Erstelle einen kurzen Website-Audit-Bericht fuer ein lokales Unternehmen.",
        "website_signals": signals.model_dump(),
        "output_contract": {
            "summary": "Kurzes Fazit in 1-2 Saetzen.",
            "score": "Integer 0-100 auf Basis der gemessenen Signale.",
            "key_issues": "Liste der wichtigsten Probleme, nur aus gemessenen Daten ableiten.",
            "recommendations": "Maximal 5 konkrete Vorschlaege mit Prioritaet und Business-Nutzen.",
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

    key_issues = report.key_issues or local_report.key_issues
    summary = report.summary or local_report.summary

    return AuditReport(
        summary=summary,
        score=report.score,
        key_issues=key_issues[:8],
        recommendations=recommendations,
    )


def _calculate_score(signals: WebsiteSignals) -> int:
    score = 0

    if signals.reachable:
        score += 25
    if signals.page_title:
        score += 12
    if signals.meta_description:
        score += 12
    if signals.h1:
        score += 10
    if signals.has_call_to_action:
        score += 12
    if signals.has_imprint:
        score += 8
    if signals.has_privacy_policy:
        score += 8
    if signals.has_contact_info:
        score += 10
    if signals.screenshot_path:
        score += 3

    return min(score, 100)


def _collect_issues(signals: WebsiteSignals) -> list[str]:
    issues: list[str] = []

    if not signals.reachable:
        issues.append("Die Website war nicht erfolgreich erreichbar.")
    if not signals.page_title:
        issues.append("Es wurde kein Seitentitel gefunden.")
    if not signals.meta_description:
        issues.append("Es wurde keine Meta Description gefunden.")
    if not signals.h1:
        issues.append("Es wurde keine H1-Ueberschrift gefunden.")
    elif signals.h1_count > 1:
        issues.append(f"Es wurden {signals.h1_count} H1-Ueberschriften gefunden.")
    if not signals.has_call_to_action:
        issues.append("Es wurde kein klarer Call-to-Action erkannt.")
    if not signals.has_imprint:
        issues.append("Es wurde kein Impressum erkannt.")
    if not signals.has_privacy_policy:
        issues.append("Es wurde keine Datenschutzerklaerung erkannt.")
    if not signals.has_contact_info:
        issues.append("Es wurden keine klaren Kontaktinformationen erkannt.")
    if not signals.screenshot_path:
        issues.append("Es konnte kein Screenshot gespeichert werden.")

    if not issues and signals.notes:
        issues.extend(signals.notes)

    return issues or ["Keine kritischen Basisprobleme erkannt."]


def _build_recommendations(signals: WebsiteSignals) -> list[Recommendation]:
    recommendations: list[Recommendation] = []

    if not signals.reachable:
        recommendations.append(
            Recommendation(
                title="Erreichbarkeit sicherstellen",
                priority="hoch",
                business_value="Besucher und Suchmaschinen koennen die Website nur bewerten, wenn sie stabil laedt.",
                action="Hosting, Domain, SSL-Zertifikat und Weiterleitungen pruefen.",
            )
        )

    if not signals.page_title or not signals.meta_description:
        recommendations.append(
            Recommendation(
                title="Suchergebnis-Snippet verbessern",
                priority="hoch",
                business_value="Ein klarer Titel und eine gute Beschreibung erhoehen die Klickrate in Suchmaschinen.",
                action="Einen eindeutigen Seitentitel und eine Meta Description fuer die Startseite setzen.",
            )
        )

    if not signals.h1 or signals.h1_count > 1:
        recommendations.append(
            Recommendation(
                title="Hauptueberschrift schaerfen",
                priority="mittel",
                business_value="Besucher verstehen schneller, welches Angebot die Website macht.",
                action="Genau eine klare H1 mit Angebot, Ort oder Nutzenversprechen verwenden.",
            )
        )

    if not signals.has_call_to_action:
        recommendations.append(
            Recommendation(
                title="Klaren Call-to-Action platzieren",
                priority="hoch",
                business_value="Mehr Besucher werden zu Anfragen, Anrufen oder Buchungen gefuehrt.",
                action="Einen gut sichtbaren Button wie 'Termin buchen', 'Anrufen' oder 'Angebot anfragen' einbauen.",
            )
        )

    if not signals.has_contact_info:
        recommendations.append(
            Recommendation(
                title="Kontaktinformationen sichtbarer machen",
                priority="hoch",
                business_value="Lokale Kunden koennen schneller Kontakt aufnehmen.",
                action="Telefonnummer, E-Mail und Adresse im Header, Footer oder Kontaktbereich anzeigen.",
            )
        )

    if not signals.has_imprint or not signals.has_privacy_policy:
        recommendations.append(
            Recommendation(
                title="Rechtliche Pflichtseiten verlinken",
                priority="hoch",
                business_value="Das staerkt Vertrauen und reduziert rechtliche Risiken.",
                action="Impressum und Datenschutzerklaerung gut sichtbar im Footer verlinken.",
            )
        )

    fallback_recommendations = [
        Recommendation(
            title="Startseite fuer lokale Kunden optimieren",
            priority="mittel",
            business_value="Ein lokaler Bezug hilft Besuchern, das Angebot schneller einzuordnen.",
            action="Ort, Leistungsgebiet und wichtigste Leistung im oberen Seitenbereich nennen.",
        ),
        Recommendation(
            title="Vertrauen oberhalb des ersten Scrolls aufbauen",
            priority="mittel",
            business_value="Bewertungen, Referenzen oder kurze Leistungsbeweise koennen die Anfragequote erhoehen.",
            action="Ein bis drei Vertrauenselemente wie Bewertungen, Siegel oder Kundenstimmen sichtbar platzieren.",
        ),
        Recommendation(
            title="Angebot klar strukturieren",
            priority="mittel",
            business_value="Eine klare Leistungsuebersicht reduziert Rueckfragen und hilft bei Kaufentscheidungen.",
            action="Die wichtigsten Leistungen mit kurzen Nutzenargumenten in einem gut scanbaren Bereich zeigen.",
        ),
        Recommendation(
            title="Mobile Darstellung manuell pruefen",
            priority="niedrig",
            business_value="Viele lokale Besucher kommen ueber Smartphones und erwarten schnelle Kontaktwege.",
            action="Startseite auf Smartphone-Breite pruefen und besonders Header, CTA und Kontaktbereich kontrollieren.",
        ),
        Recommendation(
            title="Naechste Messung mit Performance-Daten ergaenzen",
            priority="niedrig",
            business_value="Ladezeit und technische Stabilitaet beeinflussen Nutzererlebnis und Suchmaschinenqualitaet.",
            action="In einer spaeteren Version Lighthouse oder Web Vitals ergaenzen.",
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
