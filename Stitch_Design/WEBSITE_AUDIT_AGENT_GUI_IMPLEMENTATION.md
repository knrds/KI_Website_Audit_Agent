# GUI-Implementierungsbrief — Website Audit Agent

## 1. Zweck dieses Dokuments

Dieses Dokument beschreibt die gewünschte GUI für das Projekt **KI-gestützter Website-Audit-Agent für lokale Unternehmen**.  
Es dient als Übergabe an einen KI-Coding-Agenten oder Entwickler, der die vorhandenen Stitch-/Google-AI-Studio-Designs in eine echte Oberfläche umsetzen soll.

Die Designs liegen lokal unter:

```text
D:\Auto_AI_Projects\KI_Website_Audit_Agent\Stitch_Design
```

Ziel ist eine **saubere, realistische MVP-GUI**, die professionell wirkt, aber nicht wie ein überladenes Enterprise-SaaS.

---

## 2. Projektkontext

Der Website Audit Agent analysiert eine eingegebene Website-URL und erzeugt daraus einen kompakten Audit-Bericht.

Der Nutzer gibt eine URL ein, zum Beispiel:

```text
https://baeckerei-schmidt.de
```

Danach prüft das System unter anderem:

- Website erreichbar
- Seitentitel vorhanden
- Meta Description vorhanden
- H1 vorhanden
- Call-to-Action erkannt
- Impressum gefunden
- Datenschutzerklärung gefunden
- Kontaktinformationen gefunden
- Screenshot erstellt
- später optional: Mobile Preview, Ladezeit, Lighthouse-Scores

Die KI erstellt daraus:

- Score von 0 bis 100
- Kurzfazit
- technische Checkliste
- fünf konkrete Handlungsempfehlungen
- Priorität je Empfehlung
- Business-Nutzen
- optionale Outreach-Zusammenfassung

---

## 3. Relevante Design-Dateien

Die Stitch-Designs bestehen aus mehreren Screens/Zuständen. Diese sollen als visuelle Referenz genutzt werden.

### 3.1 Designsystem

```text
DESIGN.md
```

Enthält:

- Farbsystem
- Typografie
- Spacing
- Border Radius
- Komponentenregeln
- Statusfarben
- Card-/Button-/Input-Styling

### 3.2 Startscreen

```text
code 3.html
screen 3.png
```

Zustand: Nutzer hat noch keinen Audit gestartet.

Kernelemente:

- zentriertes Logo/Icon
- Titel: `Website Audit Agent`
- Badge: `PORTFOLIO MVP`
- Untertitel: `KI-gestützte Website-Analyse für lokale Unternehmen`
- großes URL-Eingabefeld
- Button: `Audit starten`
- Hinweisbox: `Analysiert SEO-Basics, CTA, Impressum, Kontaktinformationen und Website-Struktur.`
- Footer mit Datenschutz und Impressum

### 3.3 Loading-State

```text
code.html
screen.png
```

Zustand: Analyse läuft.

Kernelemente:

- Topbar mit Logo/Titel und Icons
- zentrierte Loading-Card
- Titel: `Analyse wird durchgeführt`
- Erklärungstext
- Fortschrittsbalken
- Stepper mit vier Schritten:
  1. Website wird geladen
  2. Screenshot wird erstellt
  3. HTML wird analysiert
  4. KI-Bericht wird erzeugt
- Button: `Abbrechen`

### 3.4 Ergebnis-Dashboard

```text
code 1.html
screen 1.png
```

Zustand: Audit war erfolgreich.

Kernelemente:

- Topbar
- Sidebar links
- Dashboard-Header
- analysierte URL
- Audit-Datum
- Buttons:
  - PDF exportieren
  - Audit speichern
  - Neue Website
- Score-Karte mit Ring-Visualisierung
- Website-Preview mit Desktop/Mobile-Umschalter
- technische Checkliste
- KI-Kurzfazit
- Outreach-Zusammenfassung
- fünf Handlungsempfehlungen
- Footer

### 3.5 Fehlerzustand

```text
code 2.html
screen 2.png
```

Zustand: Website nicht erreichbar.

Kernelemente:

- Topbar
- großes Fehler-Icon
- Titel: `Website nicht erreichbar`
- Erklärungstext
- vier Fehlerursachen als Karten:
  - URL ungültig
  - Zugriff blockiert
  - Zeitüberschreitung
  - SSL-/Verbindungsproblem
- URL-Eingabefeld
- Button: `Erneut versuchen`
- Footer

---

## 4. Ziel der GUI-Implementierung

Die GUI soll folgende vier Zustände sauber abbilden:

```text
IDLE      → Startscreen mit URL-Eingabe
LOADING   → Analyse wird durchgeführt
SUCCESS   → Ergebnis-Dashboard
ERROR     → Website nicht erreichbar
```

Die Umsetzung soll zunächst mit Demo-Daten funktionieren.  
Wenn Backend-Funktionen bereits existieren, sollen sie angebunden werden. Wenn nicht, soll die UI mit Mock-Daten laufen.

Wichtig:

- Die GUI darf nicht vom Backend blockiert werden.
- Das UI soll auch ohne echte KI/API lauffähig sein.
- Der Nutzerfluss muss komplett demonstrierbar sein.
- Keine Login-Seite.
- Keine echte Datenbankpflicht.
- Keine Massenverarbeitung.
- Kein großes Admin-Dashboard.

---

## 5. Empfohlene technische Umsetzung

### Option A — empfohlen für das aktuelle MVP

**Streamlit + Custom CSS**

Vorteile:

- passt zum bestehenden Python-Projekt
- schnell umsetzbar
- Backend und UI bleiben in einem Projekt
- ideal für Portfolio-Demo
- keine zusätzliche Frontend-Komplexität

Empfohlene Struktur:

```text
website-audit-agent/
│
├── app.py
├── audit.py
├── ai_report.py
├── models.py
├── utils.py
│
├── ui/
│   ├── __init__.py
│   ├── components.py
│   ├── sample_data.py
│   └── state.py
│
├── assets/
│   └── styles.css
│
├── outputs/
│   └── screenshots/
│
├── requirements.txt
└── .env.example
```

### Option B — später für exaktere Designumsetzung

**React + Tailwind + Python API**

Vorteile:

- Design kann näher am Stitch-HTML umgesetzt werden
- saubere Komponentenarchitektur
- besser für echtes Produkt

Nachteil:

- mehr Setup
- API-Schicht notwendig
- für MVP unnötig groß

Für dieses Projekt gilt: **erst Streamlit, später optional React.**

---

## 6. Visuelles Designsystem

### 6.1 Grundstil

Die Oberfläche soll wirken:

- modern
- ruhig
- technisch
- vertrauenswürdig
- analytisch
- businessnah
- minimalistisch

Sie soll nicht wirken:

- verspielt
- grell
- überladen
- wie ein riesiges Enterprise-System
- wie eine generische Admin-Vorlage

### 6.2 Farben

Wichtige Farben aus dem Design:

```css
--background: #fcf8ff;
--surface: #fcf8ff;
--surface-container-lowest: #ffffff;
--surface-container-low: #f5f2ff;
--surface-container: #f0ecf9;
--surface-container-high: #eae6f4;
--surface-container-highest: #e4e1ee;

--text-main: #1b1b24;
--text-muted: #464555;

--primary: #3525cd;
--primary-container: #4f46e5;
--primary-soft: #e2dfff;

--outline: #777587;
--outline-variant: #c7c4d8;

--success: #059669;
--warning: #f59e0b;
--error: #ba1a1a;
```

Statusfarben:

```text
Bestanden → Grün/Emerald
Warnung   → Amber/Orange
Fehler    → Rot/Rose
```

### 6.3 Typografie

Schriftart:

```text
Inter
```

Typografische Rollen:

```text
Display:      48px, 700, line-height 1.1
Headline LG:  32px, 600, line-height 1.2
Headline MD:  24px, 600, line-height 1.3
Headline SM:  20px, 600, line-height 1.4
Body LG:      18px, 400, line-height 1.6
Body MD:      16px, 400, line-height 1.5
Body SM:      14px, 400, line-height 1.5
Label:        12–14px, 500–600
```

Falls Streamlit genutzt wird, soll Inter per CSS importiert werden:

```css
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap");

html, body, [class*="css"] {
  font-family: "Inter", sans-serif;
}
```

### 6.4 Spacing

Basis-System:

```text
4px Grid
8px kleine Abstände
16px Standard-Abstände
24px Card-Gutter
32px größere Sektionen
48px große Sektionen
64px Hero-Abstände
```

### 6.5 Radius und Schatten

```text
Inputs/Buttons: 8px
Cards: 16–24px
Badges: full/pill
```

Cards:

```css
border: 1px solid #c7c4d8;
box-shadow: 0 1px 3px rgba(0,0,0,0.08);
background: #ffffff;
```

Hover:

```css
box-shadow: 0 10px 15px -3px rgba(0,0,0,0.10);
```

---

## 7. UI-Komponenten

### 7.1 App Shell

Wiederverwendbare Basisstruktur:

- Topbar
- optional Sidebar
- Main Content Area
- Footer

Die Sidebar wird nur im Ergebnis-Dashboard genutzt.  
Startscreen, Loading-State und Error-State bleiben fokussiert und verwenden keine Sidebar.

### 7.2 Topbar

In Loading, Success und Error sichtbar.

Elemente:

- links: Icon + `Website Audit Agent`
- rechts:
  - Notifications Icon
  - Settings Icon
  - User Avatar

Im MVP sind die Icons rein visuell, ohne Funktion.

### 7.3 Footer

Desktop:

- links Copyright
- rechts Links

Startscreen:

```text
Datenschutz
Impressum
```

Dashboard/Loading/Error:

```text
Documentation
Privacy Policy
Support
Terms of Service
```

Für MVP dürfen die Links ohne echte Zielseite sein.

### 7.4 URL Input

Bestandteile:

- Icon links
- Placeholder: `https://baeckerei-schmidt.de`
- Button: `Audit starten`

Regeln:

- Eingabe muss wie URL wirken
- Button klar primär
- Enter soll Audit starten
- bei leerer Eingabe Fehlermeldung anzeigen

### 7.5 Buttons

Primär:

```text
Audit starten
Neue Website
Erneut versuchen
```

Sekundär:

```text
PDF exportieren
Audit speichern
Text kopieren
Abbrechen
```

MVP-Regeln:

- PDF exportieren und Audit speichern dürfen zunächst deaktiviert oder als Platzhalter implementiert sein.
- Sie sollen aber visuell vorhanden sein, weil sie das Portfolio professioneller wirken lassen.

### 7.6 Score Card

Daten:

```text
score: 0–100
status_label: z.B. "Warnung: Optimierung empfohlen"
summary_short: 1–2 Sätze
```

Visual:

- runder Fortschrittsring
- Score groß in der Mitte
- Text: `von 100`
- Farbe abhängig vom Score:
  - 0–49 rot
  - 50–89 orange
  - 90–100 grün

### 7.7 Website Preview

Daten:

```text
desktop_screenshot_path
mobile_screenshot_path optional
```

Visual:

- Card mit Header `Website Preview`
- Toggle:
  - Desktop
  - Mobile
- Browser-Frame-Optik
- falls kein Screenshot vorhanden:
  - neutraler Placeholder
  - Text: `Kein Screenshot verfügbar`

### 7.8 Technische Checkliste

Checks:

- Website erreichbar
- Seitentitel vorhanden
- Meta Description vorhanden
- H1 vorhanden
- CTA erkannt
- Impressum gefunden
- Datenschutzerklärung gefunden
- Kontaktinformationen gefunden
- Screenshot erstellt

Statuswerte:

```text
passed
warning
failed
unknown
```

Anzeige:

```text
passed  → grünes Icon + Badge "Bestanden"
warning → orangenes Icon + Badge "Warnung"
failed  → rotes Icon + Badge "Fehler"
unknown → graues Icon + Badge "Unklar"
```

### 7.9 KI-Kurzfazit

Eine Card mit:

- Icon `auto_awesome`
- Titel `KI-Kurzfazit`
- Text mit 2–3 Sätzen

Wichtig: Hinweis im Prompt/Backend, dass die KI nur auf Basis der gemessenen Daten bewertet.

### 7.10 Outreach-Zusammenfassung

Eine Card mit:

- Titel `Outreach-Zusammenfassung`
- Monospace-Textblock
- Button `Text kopieren`

Im MVP reicht ein visuell dargestellter Textblock.  
Der Kopieren-Button kann optional später mit JavaScript/Streamlit-Komponente umgesetzt werden.

### 7.11 Handlungsempfehlungen

Genau fünf Cards.

Jede Card enthält:

- Prioritätsbadge
- Titel
- kurze Begründung
- optional Business-Nutzen

Prioritäten:

```text
hoch    → rot/rose
mittel  → amber/orange
niedrig → grün/emerald
```

Beispiel:

```text
Priorität: Hoch
Titel: Klaren Call-to-Action im Header ergänzen
Begründung: Besucher benötigen direkte Führung zur gewünschten Aktion.
Business-Nutzen: Kann mehr Kontaktanfragen erzeugen.
```

### 7.12 Error Reason Cards

Vier Fehlerkarten:

1. URL ungültig
2. Zugriff blockiert
3. Zeitüberschreitung
4. SSL-/Verbindungsproblem

Danach:

- URL-Eingabe mit aktueller URL
- Button `Erneut versuchen`

---

## 8. UI-State-Model

In Streamlit kann der Zustand über `st.session_state` verwaltet werden.

Empfohlene Keys:

```python
st.session_state["view"] = "idle"      # idle | loading | success | error
st.session_state["current_url"] = ""
st.session_state["audit_result"] = None
st.session_state["error_message"] = None
```

Ablauf:

```text
Startscreen
→ URL eingeben
→ Button "Audit starten"
→ view = "loading"
→ Audit-Funktion ausführen
→ Erfolg: view = "success"
→ Fehler: view = "error"
```

Für eine Demo ohne echtes Backend:

```text
Startscreen
→ Button
→ kurzer Loading-State
→ Demo-Ergebnis anzeigen
```

---

## 9. Datenmodell für die GUI

### 9.1 Audit Result

```json
{
  "url": "https://baeckerei-schmidt.de",
  "audit_date": "24. Okt 2023, 14:30 Uhr",
  "score": 68,
  "status_label": "Warnung: Optimierung empfohlen",
  "score_summary": "Die Basis ist solide, aber es gibt entscheidende Potenziale in der technischen SEO und Konvertierung.",
  "screenshots": {
    "desktop": "outputs/screenshots/desktop.png",
    "mobile": null
  },
  "checks": [
    {
      "label": "Website erreichbar",
      "status": "passed"
    },
    {
      "label": "Seitentitel vorhanden",
      "status": "passed"
    },
    {
      "label": "Meta Description vorhanden",
      "status": "warning"
    },
    {
      "label": "H1 vorhanden",
      "status": "passed"
    },
    {
      "label": "CTA erkannt",
      "status": "failed"
    },
    {
      "label": "Impressum gefunden",
      "status": "passed"
    },
    {
      "label": "Datenschutzerklärung gefunden",
      "status": "passed"
    },
    {
      "label": "Kontaktinformationen gefunden",
      "status": "passed"
    }
  ],
  "ai_summary": "Die Website ist grundsätzlich erreichbar und enthält wichtige Vertrauenselemente wie Impressum und Kontaktinformationen. Es fehlt jedoch ein klarer Call-to-Action im sichtbaren Bereich, und die SEO-Basis könnte durch eine bessere Meta Description gestärkt werden.",
  "outreach_text": "Hallo Bäckerei Schmidt-Team,\n\nmir ist aufgefallen, dass Ihre Website eine solide Basis hat, aber wertvolle Kundenanfragen verpasst, da ein klarer Handlungsaufruf auf der Startseite fehlt. Gerne zeige ich Ihnen kurz auf, wie wir das schnell optimieren können.",
  "recommendations": [
    {
      "priority": "hoch",
      "title": "Klaren Call-to-Action im Header ergänzen",
      "reason": "Besucher benötigen direkte Führung zur gewünschten Aktion.",
      "business_value": "Kann mehr Kontaktanfragen erzeugen."
    },
    {
      "priority": "hoch",
      "title": "Öffnungszeiten direkt sichtbar machen",
      "reason": "Für ein lokales Geschäft sind Öffnungszeiten eine der wichtigsten Informationen.",
      "business_value": "Reduziert Suchaufwand für Besucher."
    },
    {
      "priority": "mittel",
      "title": "Meta Description für lokale Suche optimieren",
      "reason": "Die aktuelle Description ist generisch.",
      "business_value": "Verbessert die Darstellung in Suchergebnissen."
    },
    {
      "priority": "mittel",
      "title": "Telefonnummer auf Mobilgeräten prominenter platzieren",
      "reason": "Mobile Nutzer sollten schnell anrufen können.",
      "business_value": "Erhöht die Chance auf direkte Kontaktaufnahme."
    },
    {
      "priority": "niedrig",
      "title": "Startseite visuell moderner strukturieren",
      "reason": "Kosmetische Verbesserungen können die wahrgenommene Wertigkeit steigern.",
      "business_value": "Stärkt Vertrauen und professionellen Eindruck."
    }
  ]
}
```

---

## 10. Streamlit-Implementierungshinweise

### 10.1 CSS laden

In `app.py`:

```python
from pathlib import Path
import streamlit as st

def load_css(path: str = "assets/styles.css"):
    css = Path(path).read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
```

### 10.2 Grundstruktur

```python
def main():
    load_css()

    view = st.session_state.get("view", "idle")

    if view == "idle":
        render_start_screen()
    elif view == "loading":
        render_loading_screen()
    elif view == "success":
        render_result_dashboard(st.session_state["audit_result"])
    elif view == "error":
        render_error_screen(st.session_state.get("current_url", ""))
```

### 10.3 Startscreen

Wichtig:

- Streamlit Standard-Header möglichst ausblenden
- zentrierte Hero-Section
- custom HTML via `st.markdown(..., unsafe_allow_html=True)`
- URL-Eingabe kann mit `st.form` umgesetzt werden

### 10.4 Loading-State

Streamlit führt normalerweise synchron aus. Für Demo:

```python
with st.spinner("Analyse läuft..."):
    result = run_audit_or_mock(url)
```

Für eine visuelle Loading-Seite kann man:

1. `view = "loading"` setzen
2. `st.rerun()`
3. Audit ausführen
4. danach `view = "success"` oder `view = "error"`

Pragmatisch für MVP reicht:

- Progressbar
- Status-Texte
- kurze `time.sleep()`-Simulation bei Demo-Modus

### 10.5 Ergebnis-Dashboard

Streamlit-kompatibel:

- `st.columns([1, 2])` für Score + Preview
- `st.columns([7, 5])` für Checkliste + KI/Outreach
- `st.columns(3)` für Empfehlungskarten
- Custom Cards per HTML/CSS

### 10.6 Fehlerzustand

Fehlerzustand soll nicht technisch-chaotisch wirken.  
Keine Python-Tracebacks zeigen.

Stattdessen:

```text
Website nicht erreichbar
Mögliche Gründe:
- URL ungültig
- Zugriff blockiert
- Zeitüberschreitung
- SSL-/Verbindungsproblem
```

---

## 11. Akzeptanzkriterien

Die GUI gilt als fertig für Version 1, wenn:

- [ ] Startscreen zeigt URL-Eingabe und Audit-Button.
- [ ] Klick auf Audit startet einen sichtbaren Analyseprozess.
- [ ] Loading-State zeigt mindestens vier Analyse-Schritte.
- [ ] Erfolgsfall zeigt das Ergebnis-Dashboard.
- [ ] Dashboard enthält Score, Preview, Checkliste, KI-Fazit, Outreach und fünf Empfehlungen.
- [ ] Fehlerfall zeigt professionelle Fehlerseite mit Retry-Funktion.
- [ ] UI nutzt Inter, Indigo-Akzent, helle Cards und Statusfarben.
- [ ] Layout ist auf Desktop sauber.
- [ ] Mobile Ansicht bricht nicht komplett.
- [ ] Die App läuft auch mit Mock-Daten ohne echte API.
- [ ] Keine Login-, CRM- oder Enterprise-Funktionen wurden eingebaut.
- [ ] Code ist modular genug, um später Backend-Funktionen anzuschließen.

---

## 12. Umfang bewusst begrenzen

Nicht in diese GUI-Version einbauen:

- Login
- Benutzerprofile
- echte Benachrichtigungen
- echte Settings-Seite
- Audit History mit Datenbank
- Competitor Tools
- echte PDF-Erzeugung
- echtes CRM
- Massenverarbeitung
- Teamfunktionen
- komplexe Charts

Diese Elemente dürfen visuell angedeutet sein, aber nicht funktional im MVP.

---

# 13. Implementierungs-Prompt für den KI-Coding-Agenten

Kopiere den folgenden Prompt in deinen Entwicklungsagenten.

```text
Du bist mein Senior Frontend-/Python-Entwicklungsagent.

Ich möchte die Stitch-/Google-AI-Studio-Designs für meinen "Website Audit Agent" in meinem bestehenden Projekt implementieren.

Projektpfad:
D:\Auto_AI_Projects\KI_Website_Audit_Agent

Designpfad:
D:\Auto_AI_Projects\KI_Website_Audit_Agent\Stitch_Design

Dort liegen die Designreferenzen:

- DESIGN.md
- code 1.html
- code 2.html
- code 3.html
- code.html
- screen 1.png
- screen 2.png
- screen 3.png
- screen.png

Die Designs zeigen vier UI-Zustände:

1. Startscreen mit URL-Eingabe
2. Loading-State während der Analyse
3. Ergebnis-Dashboard nach erfolgreichem Audit
4. Fehlerzustand, wenn die Website nicht erreichbar ist

Bitte implementiere die GUI passend zu diesen Designs.

Wichtige Projektregel:
Das Projekt ist ein MVP/Portfolio-Projekt. Baue keine überladene SaaS-Plattform. Kein Login, keine echte Datenbankpflicht, kein CRM, keine Massenverarbeitung, keine unnötigen Enterprise-Features.

Technologie:
Nutze bevorzugt Streamlit mit Custom CSS, weil das Projekt ein Python-Projekt ist. Falls bereits eine andere UI-Struktur existiert, passe dich an, aber halte die Umsetzung möglichst einfach.

Ziel:
Die App soll eine einzelne Website-URL analysieren und danach einen professionellen Audit-Report anzeigen.

Implementiere mindestens folgende UI-Zustände:

STATE 1: IDLE / Startscreen
- zentriertes Logo/Icon
- Titel: "Website Audit Agent"
- Badge: "PORTFOLIO MVP"
- Untertitel: "KI-gestützte Website-Analyse für lokale Unternehmen"
- URL-Eingabefeld mit Placeholder: "https://baeckerei-schmidt.de"
- Button: "Audit starten"
- Hinweis: "Analysiert SEO-Basics, CTA, Impressum, Kontaktinformationen und Website-Struktur."
- Footer mit Datenschutz und Impressum

STATE 2: LOADING / Analyse läuft
- Topbar mit "Website Audit Agent"
- zentrierte Loading-Card
- Titel: "Analyse wird durchgeführt"
- kurzer Erklärungstext
- Fortschrittsbalken
- Stepper mit:
  1. Website wird geladen
  2. Screenshot wird erstellt
  3. HTML wird analysiert
  4. KI-Bericht wird erzeugt
- Button: "Abbrechen"

STATE 3: SUCCESS / Ergebnis-Dashboard
- Topbar
- linke Sidebar auf Desktop
- Header "Ergebnis-Dashboard"
- analysierte URL und Datum
- Buttons:
  - "PDF exportieren"
  - "Audit speichern"
  - "Neue Website"
- Score-Karte mit Ring und Score 0–100
- Website Preview mit Desktop/Mobile Toggle
- technische Checkliste
- KI-Kurzfazit
- Outreach-Zusammenfassung mit "Text kopieren"
- genau fünf Handlungsempfehlungen
- Footer

STATE 4: ERROR / Website nicht erreichbar
- Topbar
- großes Fehler-Icon
- Titel: "Website nicht erreichbar"
- Erklärungstext
- vier Fehlerkarten:
  - URL ungültig
  - Zugriff blockiert
  - Zeitüberschreitung
  - SSL-/Verbindungsproblem
- URL-Eingabefeld mit aktueller URL
- Button: "Erneut versuchen"
- Footer

Designvorgaben:
- Schriftart: Inter
- Hintergrund: sehr helles Off-White / #fcf8ff oder #f9fafb
- Cards: Weiß, 1px Border, dezenter Schatten
- Primärfarbe: Indigo / #4f46e5
- Textfarbe: #1b1b24
- Muted Text: #464555
- Success: Emerald/Grün
- Warning: Amber/Orange
- Error: Rose/Rot
- Buttons und Inputs: 8px Radius
- Cards: 16–24px Radius
- viel Whitespace
- klare visuelle Hierarchie
- keine schweren Schatten
- keine bunten Verläufe
- keine übertriebenen Animationen

Empfohlene Dateien:
- app.py
- ui/components.py
- ui/sample_data.py
- ui/state.py
- assets/styles.css

Falls diese Dateien noch nicht existieren, erstelle sie.
Falls bereits Dateien existieren, verändere sie vorsichtig und zerstöre keine funktionierende Backend-Logik.

Backend-Anbindung:
Wenn bereits Funktionen wie `audit_website(url)` oder `generate_report(audit_data)` existieren, binde sie an.
Wenn sie nicht existieren oder Fehler werfen, nutze Mock-Daten, damit die GUI lauffähig bleibt.

Mock-Daten:
Nutze als Demo:
URL: https://baeckerei-schmidt.de
Score: 68
Status: "Warnung: Optimierung empfohlen"

Checks:
- Website erreichbar: Bestanden
- Seitentitel vorhanden: Bestanden
- Meta Description vorhanden: Warnung
- H1 vorhanden: Bestanden
- CTA erkannt: Fehler
- Impressum gefunden: Bestanden
- Datenschutzerklärung gefunden: Bestanden
- Kontaktinformationen gefunden: Bestanden

KI-Kurzfazit:
"Die Website ist grundsätzlich erreichbar und enthält wichtige Vertrauenselemente wie Impressum und Kontaktinformationen. Es fehlt jedoch ein klarer Call-to-Action im sichtbaren Bereich, und die SEO-Basis könnte durch eine bessere Meta Description gestärkt werden."

Handlungsempfehlungen:
1. Klaren Call-to-Action im Header ergänzen — Hoch
2. Öffnungszeiten direkt sichtbar machen — Hoch
3. Meta Description für lokale Suche optimieren — Mittel
4. Telefonnummer auf Mobilgeräten prominenter platzieren — Mittel
5. Startseite visuell moderner strukturieren — Niedrig

Wichtige technische Anforderungen:
- Die App muss lokal startbar sein.
- Keine externen API-Aufrufe sind für die GUI-Demo erforderlich.
- Keine echten PDF-/Speicherfunktionen nötig; Buttons dürfen Placeholder sein.
- Fehlermeldungen dürfen keine Python-Tracebacks zeigen.
- UI soll responsive genug sein, um auf kleineren Bildschirmen nicht kaputtzugehen.
- Code sauber modularisieren.
- Kommentare nur dort, wo sie hilfreich sind.
- Nach der Umsetzung kurz erklären:
  1. Welche Dateien geändert/erstellt wurden.
  2. Wie ich die App starte.
  3. Welche Funktionen noch Mock-Daten nutzen.
  4. Was der nächste sinnvolle Entwicklungsschritt ist.

Bitte beginne mit der GUI-Implementierung und halte dich eng an die Stitch-Designs.
```

---

## 14. Realistische Umsetzungsempfehlung

Baue zuerst nur:

```text
Startscreen → Loading Demo → Ergebnis-Dashboard mit Mock-Daten → Error-Screen
```

Danach erst:

```text
echter Playwright-Audit → echter Screenshot → echte KI-Auswertung
```

Das ist die sauberste Reihenfolge, weil du dann früh eine vorzeigbare Oberfläche hast und das Backend später Schritt für Schritt anschließen kannst.

---

## 15. Nächster konkreter Schritt

Gib dem KI-Coding-Agenten den Prompt aus Abschnitt 13.

Danach soll er zuerst nur diese Dateien erzeugen:

```text
app.py
ui/components.py
ui/sample_data.py
assets/styles.css
```

Er soll danach die App lokal startbar machen mit:

```bash
streamlit run app.py
```
