# 🤖 KI-gestützter Website-Audit-Agent (Showcase MVP)

Ein interaktiver Website-Audit-Agent für lokale Unternehmen, der vollautomatisch SEO-Basics, Conversion-Heuristiken und Web-Strukturen analysiert. Das Projekt wurde als sauberes, vorzeigbares Portfolio- und Showcase-Projekt konzipiert, das fortgeschrittene Python-Entwicklung, Browser-Automation (Playwright), HTML-Parsing (BeautifulSoup) und strukturierte KI-Auswertung (OpenAI API & Pydantic) demonstriert.

Die Benutzeroberfläche basiert auf Streamlit und wurde mit einem maßgeschneiderten Custom CSS im modernen "Stitch Design"-Stil (Surface-on-Base, minimalistische Karten, interaktive Status-Badges) gestaltet.

---

## ✨ Features des MVP-Prototyps

Das Tool bietet eine voll funktionsfähige Ende-zu-Ende-Pipeline für Website-Analysen:

*   **Browser-Automation (Playwright):** Öffnet die Ziel-URL in einem Headless-Chromium-Browser, prüft die Erreichbarkeit, misst die Ladezeit und erstellt ein visuelles Bildschirmfoto (Desktop-Ansicht).
*   **Heuristisches HTML-Parsing (BeautifulSoup):** Extrahiert und analysiert Seitentitel, Meta Descriptions, H1- und H2-Überschriften, Canonical-Tags, strukturierte Daten (z. B. `LocalBusiness` Schema), Bild-Alt-Attribute und Kontaktinformationen (Telefon, E-Mail, Adresse, Öffnungszeiten).
*   **Strikte Scoring-Logik (0–100):** Ein transparenter, regelbasierter Score bewertet die SEO-Grundlagen und Conversion-Stärke der Website (z. B. CTA-Vorhandensein, lokale SEO-Signale, Trust-Elemente).
*   **Strukturierte KI-Analyse (OpenAI API):** Sendet die extrahierten Signale an die OpenAI API und validiert die strukturierte Antwort mittels Pydantic gegen das Datenmodell. Die KI erzeugt:
    *   Ein prägnantes Kurzfazit.
    *   5 priorisierte, konkrete Verbesserungsvorschläge (mit Begründung und Business-Nutzen).
    *   Einen personalisierten Outreach-Entwurf für die Kundenakquise.
*   **Lokaler Fallback-Modus:** Sollte kein OpenAI-API-Schlüssel konfiguriert sein oder ein Fehler auftreten, generiert die App automatisch einen detaillierten regelbasierten Audit-Bericht. Das Projekt bleibt dadurch jederzeit ohne API-Kosten voll funktionsfähig und präsentabel!
*   **Modernes Dashboard-UI:**
    *   **Startscreen:** Übersichtlich mit URL-Eingabe und einem "Demo-Modus" für schnelle Präsentationen.
    *   **Loading-State:** Ein animierter Stepper visualisiert live den Fortschritt der einzelnen Analysephasen.
    *   **Ergebnis-Dashboard:** Aufgeteilt in Overview (Score, Screenshot, Checkliste, KI-Fazit, Outreach-Kopie) und eine detaillierte **SEO-Detailansicht** sowie eine lokale **Audit-Historie** (für die aktuelle Session).
    *   **Fehlerseite:** Fängt blockierte Verbindungen, SSL-Probleme oder Timeouts ab und bietet verständliche Lösungsansätze.

---

## 🛠️ Tech-Stack & Architektur

Dieses Projekt demonstriert Best Practices in der Python-Entwicklung und Datenverarbeitung:

*   **Python 3.11+**
*   **Streamlit** (UI-Framework & Session-State-Management)
*   **Playwright** (Headless Browser für Crawling & Screenshots)
*   **BeautifulSoup4** (HTML-Parsing & Signalextraktion)
*   **Pydantic v2** (Strenge Datenvalidierung und Typisierung für Signale und KI-Antworten)
*   **OpenAI SDK** (Strukturierter JSON-Mode für die Berichterstellung)
*   **Tailored CSS** (Integration eines konsistenten CSS-Designsystems über CSS-Injektion)

---

## 📂 Projektstruktur

```text
├── app.py                  # Streamlit-Hauptanwendung (Zustandssteuerung & Routing)
├── audit.py                # Core-Audit-Modul (Playwright & BeautifulSoup-Parser)
├── ai_report.py            # KI-Schicht (OpenAI API-Anbindung, Prompting & Fallbacks)
├── models.py               # Pydantic-Modelle (WebsiteSignals, Recommendation, AuditReport)
├── utils.py                # Hilfsfunktionen (URL-Normalisierung, sichere Dateinamen)
├── requirements.txt        # Projekt-Abhängigkeiten
├── .env.example            # Vorlage für Umgebungsvariablen
├── .gitignore              # Git-Ausschlussregeln
├── assets/
│   └── styles.css          # Custom Stylesheet im modernen Stitch-Design
├── ui/
│   ├── __init__.py
│   ├── components.py       # UI-Komponenten (Karten, Checklisten, Topbar, Ladezustand)
│   ├── sample_data.py      # Mockdaten für den interaktiven Demo-Modus
│   └── state.py            # Session-State-Helper für die App-Zustände
├── outputs/
│   └── screenshots/        # Speicherort für generierte Screenshots (gitignored)
└── Stitch_Design/          # Design-Referenzen und Mockups (Entwicklungsverlauf)
```

---

## 🚀 Installation & Lokaler Start

### Voraussetzungen
Stellen Sie sicher, dass Python (Version 3.11 oder neuer) auf Ihrem System installiert ist.

1.  **Repository klonen & in das Verzeichnis wechseln:**
    ```bash
    cd KI_Website_Audit_Agent
    ```

2.  **Virtuelle Umgebung erstellen und aktivieren:**
    *   **Windows (PowerShell):**
        ```powershell
        python -m venv .venv
        .\.venv\Scripts\Activate.ps1
        ```
    *   **macOS / Linux:**
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```

3.  **Abhängigkeiten installieren:**
    ```bash
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ```

4.  **Playwright Chromium-Browser installieren:**
    ```bash
    playwright install chromium
    ```

5.  **Anwendung starten:**
    ```bash
    streamlit run app.py
    ```
    Die Anwendung öffnet sich automatisch in Ihrem Standardbrowser unter `http://localhost:8501`.

---

## ⚙️ Konfiguration (Optional für echte KI-Berichte)

Das Tool kann vollkommen ohne API-Schlüssel gestartet werden (dank des integrierten Heuristik-Fallbacks). Für vollwertige KI-Analysen können Sie die OpenAI API wie folgt anbinden:

1.  Kopieren Sie die `.env.example` Datei zu `.env`:
    ```bash
    cp .env.example .env
    ```
2.  Tragen Sie Ihren API-Schlüssel und das gewünschte Modell in die `.env` ein:
    ```env
    OPENAI_API_KEY=ihr_api_schluessel_hier
    OPENAI_MODEL=gpt-4o-mini
    OPENAI_BASE_URL=
    ```
    *(Hinweis: Für alternative, OpenAI-kompatible Schnittstellen kann `OPENAI_BASE_URL` entsprechend angepasst werden).*

---

## 📊 Bewertungskriterien & Logik

Der berechnete Score (0 bis 100) basiert auf harten Kriterien, die für kleine, lokale Dienstleister geschäftskritisch sind:

*   **Technische Erreichbarkeit (Status-Code & Timeouts)**
*   **SEO-Basics:** Vorhandensein, Länge und Qualität von Seitentitel und Meta-Beschreibung (inkl. Prüfung auf Benefit/CTA).
*   **Content-Struktur:** Korrekte Verwendung von genau einer H1-Überschrift sowie das Vorhandensein relevanter Leistungsbegriffe.
*   **Conversion-Stärke:** Erkennung von starken Handlungsaufforderungen (CTAs) im sichtbaren Bereich.
*   **Lokale Relevanz:** Erkennung von Adressdaten, Öffnungszeiten und dem `LocalBusiness` Schema (Structured Data).
*   **Trust-Faktoren:** Vorhandensein von Kundenbewertungen, Testimonials, Referenzen oder Auszeichnungen.
*   **Rechtliche Sicherheit:** Vorhandensein von Impressums- und Datenschutzerklärungs-Links.

---

## 🔒 Halluzinationsschutz & Auswertungssicherheit

Damit die KI keine fehlerhaften Behauptungen über die geprüfte Website aufstellt (Halluzinationen), wurde ein strenges Sicherheitskonzept implementiert:
1.  **Datenminimierung:** An die API wird kein roher HTML-Code übergeben, sondern ausschließlich das strukturierte, lokal validierte Pydantic-Modell `WebsiteSignals`.
2.  **Strikter Systemprompt:** Der Prompt verbietet der KI das Erfinden von Fakten, Brancheninformationen oder nicht gemessenen technischen Werten.
3.  **Pydantic-Validierung:** Die Antwort der KI wird direkt über das Modell `AuditReport` geparst. Ist das JSON ungültig oder entspricht nicht dem Schema, greift die App geräuschlos auf den regelbasierten Fallback-Bericht zurück.

---

## 🌟 Showcase-Nutzen (Bewerbungen & Portfolio)

Dieses Projekt dient als praktischer Beleg für folgende Fähigkeiten:
*   **Saubere Software-Architektur:** Klare Trennung von UI-Logik (`ui/`), Business-Logic (`audit.py`, `ai_report.py`), Datenmodellierung (`models.py`) und Konfiguration.
*   **Praxisnahe Automation:** Robuster Einsatz von Playwright zur Gewinnung strukturierter Rohdaten und Screenshots im Hintergrund.
*   **Modernes UI-UX-Design:** Einbindung maßgeschneiderter CSS-Stylesheets in Streamlit für ansprechende Micro-Interaktionen, responsive Layouts und stimmige visuelle Zustände.
*   **Robuste Fehlerbehandlung:** Graceful Degradation und API-Fallbacks sorgen für eine fehlerfreie Vorführbarkeit der Anwendung unter allen Bedingungen.

---

## 📄 Lizenz

Dieses Projekt ist unter der MIT-Lizenz veröffentlicht. Weitere Details finden Sie in der Lizenzdatei.
