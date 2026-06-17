# KI-gestuetzter Website-Audit-Agent

Ein kleines, praxisnahes Portfolio-Projekt fuer automatische Website-Audits von
lokalen Unternehmen. Das Tool nimmt eine einzelne Website-URL entgegen,
analysiert einfache technische und inhaltliche Kriterien und erstellt daraus
einen kompakten Audit-Bericht mit Score, Problemen und konkreten Empfehlungen.

Das Projekt ist bewusst klein gehalten. Es soll kein vollstaendiges SaaS-Produkt
sein, sondern eine saubere Demo fuer Python-Entwicklung, Browser-Automation,
strukturierte Datenmodelle, Website-Analyse und spaetere KI-Auswertung.

## Aktueller Stand

Der aktuelle MVP ist lauffaehig und kann eine einzelne URL pruefen.

Bereits umgesetzt:

- Streamlit-Oberflaeche mit URL-Eingabe
- Playwright-basierter Seitenaufruf im Headless-Browser
- HTTP-Status und grobe Ladezeitmessung
- HTML-Auswertung mit BeautifulSoup
- Erkennung von Seitentitel, Meta Description und H1
- einfache Heuristiken fuer Call-to-Action, Impressum, Datenschutz und Kontaktinformationen
- Screenshot der analysierten Website
- Pydantic-Modelle fuer strukturierte Audit-Daten
- lokaler regelbasierter Score von 0 bis 100
- optionaler KI-Bericht ueber OpenAI API oder kompatible API
- Validierung der KI-Antwort mit Pydantic
- automatischer Fallback auf lokalen Bericht, wenn kein API-Key vorhanden ist
- bis zu 5 konkrete Verbesserungsvorschlaege mit Prioritaet und Business-Nutzen
- Anzeige von Rohdaten und technischen Hinweisen in Streamlit

Noch nicht umgesetzt:

- PDF-Export
- mobile Zweitansicht
- Lighthouse- oder Web-Vitals-Analyse
- Datenbank, Login, Multi-URL-Crawling oder SaaS-Funktionen

Die KI-Anbindung ist optional. Ohne `.env` oder API-Key wird automatisch ein
lokaler regelbasierter Bericht erzeugt, damit das Projekt weiterhin ohne externe
Abhaengigkeiten demo-faehig bleibt.

## Stand nach init.md

Aus dem urspruenglichen Implementierungsplan sind aktuell diese Schritte
umgesetzt:

1. Projektordner und Setup
2. Dependencies und Env-Beispiel
3. Grundstruktur mit Modulen
4. Playwright-basierter Website-Aufruf
5. Website-Daten extrahieren
6. Basischecks fuer Titel, Meta, H1, CTA, Impressum, Datenschutz und Kontakt
7. Streamlit-UI
8. KI-Bericht mit API-Key-Erkennung, Pydantic-Validierung und lokalem Fallback
9. Fehlerbehandlung teilweise umgesetzt
10. README und Portfolio-Dokumentation gestartet

Noch offen fuer eine runde Version 1:

- echten lokalen Testlauf in einer stabilen Python-Umgebung ausfuehren
- UI-Fehlertexte weiter polieren
- optional Demo-Screenshot fuer README/Portfolio erzeugen
- optional mobilen Screenshot ergaenzen

## Zielgruppe

Das Tool ist fuer einfache Website-Erstchecks gedacht, zum Beispiel fuer:

- lokale Dienstleister
- Handwerksbetriebe
- Restaurants, Cafes und kleine Laeden
- Agentur- oder Freelancer-Demos
- Portfolio-Projekte bei Bewerbungen

Es ersetzt kein professionelles SEO-, Rechts- oder Performance-Audit. Es zeigt
aber schnell, ob eine Website grundlegende Signale fuer Vertrauen, Auffindbarkeit
und Kontaktaufnahme bietet.

## Projektstruktur

```text
app.py
audit.py
ai_report.py
models.py
utils.py
requirements.txt
.env.example
.gitignore
README.md
outputs/
  screenshots/
    .gitkeep
Stitch_Design/
```

## Dateien

`app.py`

Streamlit-App. Baut die Oberflaeche, nimmt die URL entgegen, startet den Audit
und zeigt Score, Basischecks, Screenshot, Empfehlungen und Rohdaten an.

`audit.py`

Technischer Audit-Kern. Oeffnet die Website mit Playwright, wartet auf den DOM,
liest HTML aus, erstellt einen Screenshot und extrahiert die wichtigsten Signale
mit BeautifulSoup.

`ai_report.py`

Berichtsschicht. Versucht bei gesetztem API-Key einen KI-Bericht zu erzeugen.
Die Antwort wird als `AuditReport` validiert. Wenn kein Key gesetzt ist, ein
Provider-Fehler auftritt oder die Antwort nicht zum Modell passt, nutzt die App
automatisch den lokalen regelbasierten Bericht.

`models.py`

Pydantic-Datenmodelle fuer Website-Signale, Empfehlungen und den Audit-Bericht.
Dadurch bleiben Datenfluss und spaetere KI-JSON-Strukturen klar nachvollziehbar.

`utils.py`

Kleine Hilfsfunktionen, aktuell fuer URL-Normalisierung, sichere Dateinamen und
Ordnererstellung.

`outputs/screenshots/`

Speicherort fuer erzeugte Screenshots. Bilddateien werden per `.gitignore` nicht
committet, damit das Repository sauber bleibt.

## Installation

Voraussetzung:

- Python 3.11 oder neuer
- PowerShell oder ein anderes Terminal

Projekt starten:

```powershell
cd D:\Auto_AI_Projects\KI_Website_Audit_Agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
streamlit run app.py
```

Danach ist die App normalerweise erreichbar unter:

```text
http://localhost:8501
```

## Nutzung

1. App mit `streamlit run app.py` starten.
2. Eine Website-URL in der Sidebar eingeben, zum Beispiel `https://example.com`.
3. Button `Website analysieren` klicken.
4. Ergebnis in der App ansehen:
   - Score
   - HTTP-Status
   - Ladezeit
   - Basischecks
   - Screenshot
   - wichtigste Probleme
   - Verbesserungsvorschlaege
   - gemessene Rohdaten

## Konfiguration

Fuer echte KI-Berichte kann eine lokale `.env` angelegt werden:

```powershell
Copy-Item .env.example .env
```

Beispiel:

```text
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
OPENAI_BASE_URL=
```

`OPENAI_BASE_URL` bleibt leer, wenn die normale OpenAI API verwendet wird. Fuer
OpenAI-kompatible Anbieter kann dort eine alternative `/v1`-Base-URL eingetragen
werden.

Wenn kein API-Key gesetzt ist, startet die App trotzdem und verwendet den
lokalen Fallback-Bericht.

## Bewertungslogik

Der aktuelle Score ist bewusst einfach und transparent. Punkte gibt es fuer:

- erreichbare Website
- vorhandenen Seitentitel
- vorhandene Meta Description
- vorhandene H1
- erkennbare Call-to-Action-Elemente
- Impressum
- Datenschutzerklaerung
- Kontaktinformationen
- erfolgreich gespeicherten Screenshot

Diese Logik ist keine finale SEO-Bewertung. Sie dient als robuste MVP-Grundlage,
die spaeter durch KI-Auswertung und weitere Messwerte erweitert werden kann.

## KI-Auswertung und Halluzinationsschutz

Die KI bekommt nicht den kompletten Website-Text, sondern nur die gemessenen
Signale aus `WebsiteSignals`. Der System-Prompt verbietet erfundene Inhalte,
Rechtsdetails, Lighthouse-Werte, Unterseiten und Branchenfakten. Die Antwort
muss wieder dem Pydantic-Modell `AuditReport` entsprechen.

Wenn die KI-Antwort leer ist, ungueltiges JSON enthaelt oder nicht zum Modell
passt, wird automatisch der lokale Bericht genutzt. Dadurch bleibt die App
robust und nachvollziehbar.

## Grenzen des aktuellen MVP

- Es wird nur eine einzelne URL analysiert.
- Es gibt keinen Crawler fuer Unterseiten.
- Rechtliche Seiten werden nur ueber einfache Text- und Link-Heuristiken erkannt.
- Kontaktinformationen werden ueber einfache Muster wie E-Mail, Telefonnummer,
  `mailto:` und `tel:` gesucht.
- Der Screenshot ist aktuell Desktop-basiert.
- Manche Websites blockieren Headless-Browser oder laden Inhalte erst nach
  komplexen Cookie-/Consent-Interaktionen.

## Troubleshooting

Wenn Playwright meldet, dass Chromium fehlt:

```powershell
playwright install chromium
```

Wenn `python` auf Windows auf einen alten oder falschen Pfad zeigt, Python neu
installieren oder die Windows-App-Ausfuehrungsaliase fuer Python pruefen. Danach
die virtuelle Umgebung neu erstellen:

```powershell
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
```

Wenn eine Website nicht erreichbar ist, kann das verschiedene Ursachen haben:

- URL falsch geschrieben
- DNS- oder SSL-Problem
- Website blockiert Headless-Browser
- Timeout wegen langsamer Seite
- Weiterleitung oder Consent-Layer verhindert vollstaendige Analyse

## Roadmap

Phase 1: einfache Demo

- Eine URL pruefen
- Screenshot speichern
- Basischecks anzeigen
- lokalen Score erzeugen
- README und Portfolio-Setup dokumentieren

Status: weitgehend umgesetzt.

Phase 2: bessere Portfolio-Version

- KI-Prompt weiter testen und mit Demo-Websites vergleichen
- Beispiel-Audits fuer README/Portfolio dokumentieren
- mobile Ansicht als zweiten Screenshot hinzufuegen
- UI-Fehlerbehandlung verbessern
- Beispiel-Screenshots und Demo-Workflow dokumentieren

Phase 3: professionellere Unternehmens-Version

- PDF-Export
- Lighthouse-CLI oder Web-Vitals-Messung
- mehrere URLs pro Session
- Export nach CSV, Airtable oder n8n
- Audit-Historie mit Datenbank
- besseres Prompting fuer Branchenkontext
- sauberer Deployment-Weg fuer Demo oder Kundenpraesentation

## Akzeptanzkriterien fuer Version 1

Version 1 gilt als fertig, wenn:

- die App lokal mit `streamlit run app.py` startet
- eine URL eingegeben und analysiert werden kann
- ein Screenshot gespeichert wird
- die wichtigsten Basischecks sichtbar sind
- ein Score zwischen 0 und 100 angezeigt wird
- mindestens drei konkrete Empfehlungen erscheinen
- technische Fehler fuer den Nutzer verstaendlich angezeigt werden
- die README die lokale Installation und Nutzung erklaert

## Portfolio-Nutzen

Das Projekt zeigt in kompakter Form:

- Python-Entwicklung mit klarer Modulstruktur
- Browser-Automation mit Playwright
- HTML-Parsing mit BeautifulSoup
- strukturierte Datenverarbeitung mit Pydantic
- Streamlit als schnelle Demo-Oberflaeche
- pragmatische Produktentscheidungen fuer einen realistischen MVP
- Business-orientierte Bewertung statt rein technischer Messwerte

## Lizenz

Noch nicht festgelegt.
