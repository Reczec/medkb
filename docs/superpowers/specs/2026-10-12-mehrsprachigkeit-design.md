# MedKB – Mehrsprachigkeit (Englisch primär, Deutsch umschaltbar) – Design-Spec

Stand: 2026-10-12 · Status: zur Freigabe · Ergänzt `2026-10-10-medkb-v2-design.md`

## 1. Ziel

Ein internationaler Recruiter sieht die Demo standardmäßig komplett auf Englisch (Oberfläche, Einträge, KI-Antworten, Quellen) und kann mit einem Klick auf Deutsch wechseln. Die Diplomarbeit stammt aus Österreich, deshalb bleibt Deutsch vollwertig.

Die Spezifikation v2 (§1 „Nicht im Umfang“) schloss Mehrsprachigkeit aus. Dieses Dokument hebt das für die zwei Sprachen **en** und **de** auf. Weitere Sprachen bleiben ausgeschlossen.

### Entscheidungen

- Standardsprache **en**, Umschalter **EN | DE**. Die Wahl liegt im Browser (`localStorage`, Schlüssel `medkb:lang`). Keine Browsersprach-Erkennung: Englisch ist der Standard.
- Umfang **komplett**: Oberfläche, Einträge, KI, Quellen, Servermeldungen.
- Deutsch bleibt die **kanonische** Sprache der Einträge. Die regelbasierte Klassifikation ist der Kern der Diplomarbeit und arbeitet auf deutschem Text. Fachgebiete und Dokumenttypen bleiben in der Datenbank deutsch.

## 2. Oberfläche

- Eigene kleine Übersetzungsschicht ohne neue Bibliothek: typisierte Wörterbücher `de` und `en` mit flachen Schlüsseln, `t(key, params)` mit `{name}`-Platzhaltern und Plural über `count` (`key_one`/`key_other`).
- Die deutschen Texte der heutigen Oberfläche bilden das Wörterbuch `de` unverändert. Englisch wird neu geschrieben: Satzschreibung statt Title Case, „Prototype with example data – not medical advice.“ als Hinweis.
- Ein Vollständigkeitstest verlangt dieselben Schlüssel und Platzhalter in beiden Sprachen.
- Daten, Zahlen und relative Zeiten richten sich nach der Sprache (`en-GB`, `de-AT`). `<html lang>` folgt der Wahl.
- Fachgebiete und Dokumenttypen werden übersetzt angezeigt (`Kardiologie` → `Cardiology`), die Farben bleiben.
- Der Umschalter sitzt in der Seitenleiste unter dem Theme-Umschalter und auf der Login-Seite (Desktop und Handy). Ein Wechsel lädt die Seite nicht neu und verwirft keine Formulareingaben.

## 3. Inhalte

Dokumente bekommen eine optionale englische Fassung in vier Spalten: `title_en`, `content_en`, `sections_en`, `keywords_en`. `content_en` wird wie `content` aus den Abschnitten zusammengesetzt, mit englischen Abschnittsnamen. Weiterlesen-Links bekommen `label_en`.

- **Anzeige:** In der englischen Ansicht gilt je Feld die englische Fassung, sonst die deutsche. Fehlt jede englische Fassung, steht ein Hinweis „Only available in German“ am Eintrag.
- **Suche:** Titel, Schlagwörter und Inhalt beider Sprachen werden durchsucht, mit denselben Gewichten (Titel 3, Schlagwörter 2, Inhalt 1). Ein deutscher Begriff findet also auch in der englischen Oberfläche den Eintrag und umgekehrt.
- **Editor (Admin):** Der deutsche Text bleibt Pflicht und kanonisch. Ein aufklappbarer Bereich „English version“ nimmt Titel, Text oder Abschnitte und Schlagwörter auf. Die Klassifikation läuft weiter auf dem deutschen Text.
- **Archiv:** Export und Wiederherstellung enthalten die neuen Felder; alte Archive bekommen Standardwerte. Bestehende Datenbanken erhalten die Spalten über `ADDED_COLUMNS`.
- **Seed:** Alle 47 Beispieleinträge erhalten eine englische Fassung (Titel, Abschnitte, Schlagwörter) und englische Link-Beschriftungen.

## 4. Server

- Die Sprache kommt aus dem Header `Accept-Language` (`en` oder `de`, sonst `en`). Das Frontend sendet ihn bei jeder Anfrage, auch beim KI-Streaming.
- Vom Server erzeugte Texte (Anmeldefehler, fehlende Berechtigung, KI-Limit, KI-Hinweise, „keine passenden Einträge“) kommen in der Anfragesprache. Was in der Datenbank steht (Protokoll `demo_reset`), wird einmal auf Englisch gespeichert.
- ICD-11: Die WHO-Antwort wird in der Anfragesprache geholt (de ist weiterhin eine WHO-Vorabversion), der Cache-Schlüssel enthält die Sprache schon. PubMed und openFDA sind englisch und bleiben es.

## 5. KI

- Die Anweisungen an das Modell sind englisch und enthalten die Antwortsprache. Rollen-Ton, Formatvorgabe, Sicherheitsregeln und Hinweis „Notruf 144“ gelten unverändert.
- Der Eintragstext im Prompt ist die englische Fassung, wenn die Anfrage englisch ist und es sie gibt, sonst die deutsche (das Modell antwortet trotzdem in der Anfragesprache).
- **Cache:** Der Schlüssel für `de` bleibt wortgleich, damit die vorgewärmten 376 deutschen Antworten gültig bleiben. Für `en` kommt die Sprache in den Schlüssel.
- **Entwurf** (Admin) wird immer auf Deutsch erzeugt, weil Deutsch kanonisch ist. Die englische Fassung schreibt der Admin im Editor.
- **Assistent:** Die Stoppwortliste für Fragen enthält englische Wörter („what“, „helps“, „should“ …); die Teilmengen-Suche aus der vorigen Runde funktioniert für beide Sprachen.
- **Vorwärmen:** `python -m app.ai.prewarm --lang en|de|both`. Die 376 englischen Antworten brauchen ein eigenes Tagesbudget (globales Limit 500 pro UTC-Tag).

## 6. Nicht im Umfang

- Weitere Sprachen.
- Automatisches Übersetzen von Einträgen (KI-Übersetzung im Editor ist eine mögliche Erweiterung).
- Ein englisches Klassifikations-Vokabular. Die Klassifikation bleibt deutsch und erklärt sich mit deutschen Wortstämmen; die Oberfläche weist darauf hin.
- Serverseitige Speicherung der Sprachwahl pro Nutzer.

## 7. Tests

- Backend: Sprachermittlung und lokalisierte Meldungen, englische Felder (Validierung, Zusammensetzen, Archiv, Schemaupgrade, Suche in beiden Sprachen), KI-Prompts und Cache-Schlüssel je Sprache, ICD je Sprache, Vollständigkeit der Seed-Übersetzungen.
- Frontend: Vollständigkeitstest der Wörterbücher, Provider und Umschalter, `Accept-Language` im API-Client, Rückfall auf Deutsch mit Hinweis. Bestehende Komponententests laufen mit `lang="de"` (Standard der Testhilfe) und bleiben dadurch unverändert; je Bereich kommen englische Tests dazu.
- Playwright: Die vorhandenen Abläufe setzen `medkb:lang=de`; neue Abläufe prüfen Englisch als Standard, den Wechsel und dessen Beständigkeit.

## 8. Annahmen und Risiken

- Die englischen Texte sind redaktionelle Demo-Inhalte auf Lehrbuchniveau und tragen denselben Hinweis wie die deutschen („keine medizinische Beratung“).
- Fachbegriffe richten sich nach der englischen Fassung der WHO-ICD-11 und MedlinePlus, österreichische Besonderheiten (Notruf 144, Telefonseelsorge 142, Vorsorgeuntersuchung) bleiben mit Länderhinweis erhalten.
- Das tägliche KI-Limit begrenzt das Vorwärmen: Der englische Cache entsteht nach dem nächsten UTC-Tageswechsel.
