Du bist mein technischer Projektplaner, Software-Architekt und Entwicklungsagent.

Ich möchte ein kleines, vorzeigbares Portfolio-Projekt entwickeln:

**Projektname:** KI-gestützter Website-Audit-Agent für lokale Unternehmen

## Projektidee

Ein Nutzer gibt eine Website-URL ein, zum Beispiel:

`https://baeckerei-schmidt.de`

Das Tool analysiert automatisch die Website und prüft einfache, relevante Kriterien:

- Ist die Website erreichbar?
- Gibt es einen Seitentitel?
- Gibt es eine Meta Description?
- Gibt es eine H1-Überschrift?
- Gibt es klare Call-to-Actions?
- Gibt es ein Impressum?
- Gibt es eine Datenschutzerklärung?
- Gibt es sichtbare Kontaktinformationen?
- Kann ein Screenshot der Website erstellt werden?
- Optional später: mobile Ansicht, Ladezeit, Lighthouse-Scores

Danach erstellt eine KI einen kurzen Audit-Bericht mit:

- Kurzfazit
- Score von 0 bis 100
- wichtigsten Problemen
- 5 konkreten Verbesserungsvorschlägen
- Priorität je Vorschlag
- Business-Nutzen je Vorschlag

## Ziel des Projekts

Das Projekt soll kein perfektes SaaS-Produkt werden, sondern ein kleines, sauberes und vorzeigbares KI-/Automatisierungsprojekt für Bewerbungen, Portfolio und praktische Webdesign-/Marketing-Anwendungen.

Es soll zeigen:

- Python-Entwicklung
- Browser Automation
- einfache Website-Analyse
- strukturierte Datenverarbeitung
- KI-Auswertung
- Business-Verständnis
- saubere Dokumentation

## Gewünschter Tech-Stack

Bitte plane das Projekt bevorzugt mit:

- Python
- Playwright
- Streamlit
- BeautifulSoup
- OpenAI API oder kompatible KI-API
- Pydantic für strukturierte Daten
- optional später: Lighthouse CLI
- optional später: PDF-Export
- optional später: Airtable oder n8n

## Sehr wichtig

Halte das Projekt klein und realistisch.

Bitte vermeide am Anfang:

- Login-System
- Datenbankpflicht
- große Dashboards
- kompletten SEO-Crawler
- automatische Massenmails
- Google-Maps-Scraping
- komplexe SaaS-Architektur
- zu viele Features auf einmal

Der MVP soll zuerst nur eine einzelne URL analysieren und einen Bericht ausgeben.

## Deine Aufgabe

Erstelle einen konkreten Entwicklungsplan für dieses Projekt.

Arbeite bitte strukturiert in folgenden Punkten:

1. Projektziel
   - Was soll das Tool leisten?
   - Welches Problem löst es?
   - Warum ist es als Portfolio-Projekt sinnvoll?

2. MVP-Definition
   - Welche Funktionen müssen in Version 1 unbedingt funktionieren?
   - Welche Funktionen werden bewusst weggelassen?
   - Was ist ein gutes Ergebnis für die erste Version?

3. Architektur
   - Welche Dateien und Module soll das Projekt haben?
   - Welche Aufgabe hat jede Datei?
   - Wie fließen die Daten durch das System?

4. Datenmodell
   - Welche Daten werden aus der Website extrahiert?
   - Wie soll das Audit-Ergebnis strukturiert werden?
   - Welche JSON-Struktur bekommt die KI?
   - Welche JSON-Struktur soll die KI zurückgeben?

5. Technische Umsetzung
   - Wie wird Playwright verwendet?
   - Wie wird HTML analysiert?
   - Wie werden Screenshots erzeugt?
   - Wie wird Streamlit aufgebaut?
   - Wie wird die KI angebunden?

6. KI-Komponente
   - Wo genau wird KI eingesetzt?
   - Welchen System-Prompt soll die KI bekommen?
   - Wie werden Halluzinationen reduziert?
   - Wie wird sichergestellt, dass die KI nur auf Basis der gemessenen Daten urteilt?

7. Schritt-für-Schritt-Entwicklungsplan
   Erstelle eine konkrete Reihenfolge:
   - Schritt 1: Projektordner und Setup
   - Schritt 2: Dependencies installieren
   - Schritt 3: Grundstruktur erstellen
   - Schritt 4: Playwright-Test
   - Schritt 5: Website-Daten extrahieren
   - Schritt 6: Basischecks bauen
   - Schritt 7: Streamlit-UI bauen
   - Schritt 8: KI-Bericht erzeugen
   - Schritt 9: Fehlerbehandlung
   - Schritt 10: README und Portfolio-Demo vorbereiten

8. Konkrete Dateien
   Erstelle einen Vorschlag für diese Projektstruktur:

   website-audit-agent/
   - app.py
   - audit.py
   - ai_report.py
   - models.py
   - utils.py
   - requirements.txt
   - .env.example
   - README.md
   - outputs/screenshots/

9. Akzeptanzkriterien
   Definiere klare Kriterien, wann Version 1 fertig ist.

10. Erweiterungs-Roadmap
    Plane drei Phasen:

- Phase 1: einfache Demo
- Phase 2: bessere Portfolio-Version
- Phase 3: professionelle Unternehmens-Version

11. Risiken und einfache Alternativen
    Erkläre, was technisch schwierig werden kann und welche einfache Lösung es jeweils gibt.

12. Nächster konkreter Schritt
    Gib mir am Ende exakt den nächsten Schritt, mit dem ich anfangen soll.

## Arbeitsweise

Bitte arbeite pragmatisch und entwicklerorientiert.

Erkläre neue Konzepte kurz und verständlich, aber verliere dich nicht in Theorie.

Triff sinnvolle Entscheidungen selbst, wenn mehrere Optionen möglich sind.

Bevorzuge einfache, robuste Lösungen.

Gib mir keine riesige Enterprise-Architektur, sondern einen Plan, den ein Informatikstudent mit grundlegenden Programmierkenntnissen realistisch umsetzen kann.

Starte jetzt mit dem vollständigen Projektplan.
