from __future__ import annotations

from models import AuditReport, Recommendation, WebsiteSignals


def create_local_report(signals: WebsiteSignals) -> AuditReport:
    """Create a deterministic report from measured signals.

    This is the local fallback before the OpenAI integration is added.
    """

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
