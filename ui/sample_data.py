from __future__ import annotations

from datetime import datetime


def sample_audit_result() -> dict:
    return {
        "url": "https://baeckerei-schmidt.de",
        "audit_date": datetime.now().strftime("%d.%m.%Y, %H:%M Uhr"),
        "score": 68,
        "status_label": "Warnung: Optimierung empfohlen",
        "score_summary": (
            "Die Basis ist solide, aber es gibt entscheidende Potenziale in der technischen SEO "
            "und Konvertierung."
        ),
        "screenshot_path": None,
        "checks": [
            {"label": "Website erreichbar", "status": "passed"},
            {"label": "Seitentitel vorhanden", "status": "passed"},
            {"label": "Meta Description vorhanden", "status": "warning"},
            {"label": "H1 vorhanden", "status": "passed"},
            {"label": "CTA erkannt", "status": "failed"},
            {"label": "Impressum gefunden", "status": "passed"},
            {"label": "Datenschutzerklaerung gefunden", "status": "passed"},
            {"label": "Kontaktinformationen gefunden", "status": "passed"},
            {"label": "Screenshot erstellt", "status": "passed"},
        ],
        "ai_summary": (
            "Die Website ist grundsaetzlich erreichbar und enthaelt wichtige Vertrauenselemente "
            "wie Impressum und Kontaktinformationen. Es fehlt jedoch ein klarer Call-to-Action "
            "im sichtbaren Bereich, und die SEO-Basis sollte fuer lokale Suchanfragen geschaerft werden."
        ),
        "outreach_text": (
            "Hallo Baeckerei Schmidt-Team,\n\n"
            "mir ist aufgefallen, dass Ihre Website eine solide Basis hat, aber wertvolle "
            "Kundenanfragen verpasst, da ein klarer Handlungsaufruf auf der Startseite fehlt. "
            "Gerne zeige ich Ihnen kurz, wie wir das schnell optimieren koennen."
        ),
        "recommendations": [
            {
                "priority": "hoch",
                "title": "Klaren Call-to-Action im Header ergaenzen",
                "reason": "Besucher benoetigen direkte Fuehrung zur gewuenschten Aktion.",
                "business_value": "Kann mehr Kontaktanfragen erzeugen.",
            },
            {
                "priority": "hoch",
                "title": "Oeffnungszeiten direkt sichtbar machen",
                "reason": "Fuer ein lokales Geschaeft sind Oeffnungszeiten eine der wichtigsten Informationen.",
                "business_value": "Reduziert Suchaufwand und steigert Vertrauen.",
            },
            {
                "priority": "mittel",
                "title": "Meta Description fuer lokale Suche optimieren",
                "reason": "Die aktuelle Description ist zu generisch.",
                "business_value": "Verbessert die Darstellung in Suchergebnissen.",
            },
            {
                "priority": "mittel",
                "title": "Telefonnummer auf Mobilgeraeten prominenter platzieren",
                "reason": "Mobile Nutzer sollten schnell anrufen koennen.",
                "business_value": "Erhoeht die Chance auf direkte Kontaktaufnahme.",
            },
            {
                "priority": "niedrig",
                "title": "Startseite visuell moderner strukturieren",
                "reason": "Kosmetische Verbesserungen koennen die wahrgenommene Wertigkeit steigern.",
                "business_value": "Staerkt Vertrauen und professionellen Eindruck.",
            },
        ],
    }
