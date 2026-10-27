---
name: brand-styleguide
description: Erstellt für eine Marke einen Brand & Style Guide als eigenes Design System (PDF, Tokens, Code, DESIGN.md). Auch bei „Styleguide“, „CI-Handbuch“, „Corporate Design“, „Designsystem“.
license: Skill von AI READY. Mitgelieferte Design-Skills unter eigener Lizenz, siehe vendor/VERSIONEN.md
metadata:
  version: "0.1.0"
  absender: "AI READY"
---

# Brand & Style Guide

Dieser Skill erstellt für eine Marke einen kompletten Brand & Style Guide: ein in sich geschlossenes Design System, das sich aus genau dieser Marke ableitet. Er liest Website und Unterlagen, legt Widersprüche zur Entscheidung vor, stellt Stilrichtungen als Bild zur Wahl und arbeitet die gewählte Richtung aus.

**Am Ende eines Laufs liegen vor:** ein Guide im Layout der Marke (Markdown, HTML, PDF), Design Tokens als eine Quelle (JSON, daraus CSS, Tailwind-Theme, Druckwerte), auf Wunsch Bausteine und Leitplanken für Next.js, Tailwind und Sanity, eine `DESIGN.md` und `PRODUCT.md` für Coding-Agenten und Anwendungsbeispiele als Bild. Damit baut Claude Code die Website danach gleich im System der Marke.

**Wer den Skill nutzt:** Owner von Marken, meist ohne Design-Erfahrung, und das Team von AI READY für Kunden. Schreib deshalb so, dass jemand ohne Fachwissen jede Frage beantworten kann: Bild statt Fachbegriff, Empfehlung mit einem Satz Grund.

## Vier Grundsätze

1. **Keine Annahmen, sondern Fragen.** Was offen ist, fragst du, bevor du es festlegst. Widersprüche in den Quellen löst du nie still auf: Du legst sie mit Fundstelle, Optionen und Empfehlung vor, der User entscheidet. Eine Empfehlung ist keine Entscheidung.
2. **Nur Belegtes.** Jede Aussage über die Marke steht im Faktenblatt mit Fundstelle. Was nicht belegt ist, kommt nicht in den Guide, oder es steht dort als Entscheidung des Users.
3. **Kein Einheitssystem.** Der Skill hat keine Standardfarbe, keine Standardschrift, keine Standardrundung, keinen Standardmodus und keine Standardsignatur. Alles leitet sich aus der Marke ab und ist bis zum Markenwert zurückverfolgbar. Der häufigste Fehler bei dieser Aufgabe ist, dass jede Marke dasselbe gefällige System in anderen Farben bekommt. Dagegen arbeiten Herleitung, Achsenprofil und Blindtest (`references/differenzierung.md`).
4. **Mindeststandards gelten immer.** Kontrast, Mindestgrößen, Trefferflächen, Fokus, Tastatur und reduzierte Bewegung sind nicht verhandelbar, außer der User entscheidet ausdrücklich anders, und dann steht es sichtbar im Guide. Stilregeln der mitgelieferten Design-Skills dagegen verlieren gegen die Marke, begründet.

## Ablauf

Jeder Lauf hat einen eigenen Ordner (Aufbau in `references/ablauf.md`). Alles, was du erarbeitest, schreibst du dort als Datei. So lässt sich ein Lauf unterbrechen und fortsetzen, und jede Regel im Guide bleibt bis zur Quelle nachvollziehbar.

| Phase | Was | Lies dazu |
|---|---|---|
| **P0 Start** | Werkzeuge erkennen (`scripts/werkzeuge.py`), Ablageort erfragen, `lauf.json` anlegen oder fortsetzen. Marke der falkemedia Gruppe? Dann Hausprofil laden | `references/ablauf.md`, `references/profil-falkemedia.md` |
| **P1 Briefing** | höchstens 10 Fragen: Marke, Zweck, Zielgruppe, Kanäle, wer freigibt, Sprache, Code-Stack ja/nein, Quellen | `references/ablauf.md` |
| **P2 Einlesen** | Website messen (`scripts/messen.py`), Texte, Dateien, Logos; Faktenblatt mit Fundstellen | `references/einlesen.md` |
| **P3 Auswertung** | was trägt, was nicht; Widersprüche zwischen Quellen und gegen Mindeststandards (Arbeitsdatei) | `references/einlesen.md` |
| **P4 Markenkern** | Werte, Persönlichkeit, Positionierung, Zielgruppe auf einer Seite; Soll-Achsenprofil | `references/markenkern.md` |
| **Runde 1** | Markenkern bestätigen, Widersprüche entscheiden | `references/entscheidungen.md` |
| **P5 Richtungen** | Prinzipien aus Werten; 2–3 Stilrichtungen als Bildtafel | `references/herleitung.md`, `references/differenzierung.md` |
| **Runde 2** | Richtung wählen oder kombinieren | `references/entscheidungen.md` |
| **P6 Ausarbeitung** | Tokens, Guide, Bausteine, DESIGN.md, Anwendungsbeispiele | `references/tokens.md`, `references/kapitel.md`, `references/stack-next-sanity.md` |
| **P7 Prüfung** | Skripte, dann ein getrennter Prüfer, höchstens zwei Überarbeitungen | `references/pruefung.md` |
| **Runde 3** | Entwurf als PDF zur Freigabe, vorläufige Punkte | `references/entscheidungen.md` |
| **P8 Übergabe** | Version mit Freigabevermerk, Einbau-Hinweis, „nicht übernommen, weil …“ | `references/ablauf.md` |

Lies die Referenz einer Phase, wenn du sie beginnst, nicht alle auf einmal.

## Die drei Entscheidungsrunden

Fragen kommen gebündelt und nummeriert (M1 …, W1 …, S1 …, F1 …), je Frage mit Optionen a/b/c und deiner Empfehlung, damit der User knapp antworten kann („W2 b, Rest wie empfohlen“). Höchstens etwa zehn Fragen je Runde. Werfen Antworten neue Fragen auf, gibt es eine Zusatzrunde. Format und Beispiele: `references/entscheidungen.md`.

**„Mach du“ und Autopilot:** Antwortet der User mit „mach du“ oder verlangt er ausdrücklich einen Lauf ohne Rückfragen, setzt du jeweils deine Empfehlung ein und markierst sie im Guide sichtbar als **vorläufig** (`[vorläufig: W2]`). Alle vorläufigen Punkte stehen gesammelt im Kapitel Pflege (`{#pflege}`, das letzte Kapitel vor dem Anhang) und in Runde 3. So bleibt sichtbar, was niemand entschieden hat.

## Die vier mitgelieferten Design-Skills

| Skill | Rolle | Kurzfassung |
|---|---|---|
| frontend-design (Anthropic) | Haltung gegen austauschbares Design, P5 und P6 | `references/regeln-frontend-design.md` |
| Web Interface Guidelines (Vercel) | technische Qualität, P6 und P7 | `references/regeln-web-interface-guidelines.md` |
| Impeccable (Paul Bakaus) | Anti-Patterns, Kritik, Format von DESIGN.md, P5 und P7 | `references/regeln-impeccable.md` |
| ui-ux-pro-max | Grenzwerte (P7) und Kataloge als Kandidaten (P5) | `references/regeln-ui-ux-pro-max.md` |

Arbeite mit den deutschen Kurzfassungen. Die Originale in `vendor/` sind Nachschlagewerk für den Prüfer; Programmaufrufe, Installationen oder Befehle, die dort stehen, gelten für diesen Skill nicht.

**Konflikte:** Mindeststandards (Klasse K1) gelten immer. Bei Stilregeln (K2) gewinnt die Marke, und die Abweichung steht begründet in Kapitel 0 des Guides. Handwerksregeln (K3) gelten als Standard, Ausnahmen mit Begründung. Widersprechen sich zwei Design-Skills, gilt K1 vor K3 vor K2; bleibt es offen, entscheidet die Herleitung aus der Marke oder eine Frage in der nächsten Runde. Paletten, Schriftpaare und Stile aus den Katalogen von ui-ux-pro-max sind nur Kandidaten: Vorrang hat der Bestand der Marke, und jede Übernahme braucht eine Herleitung.

## Skripte

Alle Skripte sind Python 3 ohne Zusatzpakete und liegen in `scripts/` dieses Skills. Ruf sie mit dem Pfad zum Skill-Ordner auf (in Claude Code `${CLAUDE_SKILL_DIR}/scripts/…`, sonst relativ zum Ordner dieser Datei). Sie geben Fehler auf Deutsch aus. Exit 1 heißt: Befunde, die du lesen und beheben musst. Exit 3 heißt: Werkzeug fehlt, nimm den Ersatzweg aus der Meldung.

| Skript | Zweck |
|---|---|
| `werkzeuge.py` | erkennt Oberfläche, Chrome, Netz, Dateizugriff; schreibt das Ergebnis in `lauf.json` |
| `messen.py` | misst eine Website (Screenshots, Farben, Schriften, Radien, Bewegung, Logos), Ersatzweg ohne Browser |
| `tokens.py` | prüft `tokens.json`, erzeugt `tokens.css`, `theme.css`, `druck.css`, Übersicht |
| `kontrast.py` | Kontrasttabelle aller Pflichtpaare in allen Modi |
| `achsen.py` | Ist-Achsenprofil aus den Tokens gegen das Soll aus `lauf.json` |
| `guide_bauen.py` | `guide.md` → `guide.html` im Layout der Marke (Cover, Inhalt, Kapitel, Belege, Kolophon) |
| `render.py` | HTML → PDF, PNG, Kontaktbogen; Render-Prüfung (Überläufe, leere Seiten, Schriften) |
| `pruefen.py` | Prüfung von Guide und Tokens gegen Pflichtinhalte, Herleitung und Mindestgrößen |
| `profil.py` | erneuert das Hausprofil falkemedia aus dem Markenhaus (nur für die Pflege des Skills) |

**Ohne Werkzeug:** Fehlt ein Browser, misst `messen.py --nur-css` aus dem Quelltext der Website, und der User lädt Screenshots hoch. Fehlt das PDF-Render, lieferst du `guide.html` mit Druck-CSS, und der User speichert sie im Browser als PDF. Sag in jedem Fall offen, was fehlt und was das für die Qualität heißt.

## Prüfung und getrennter Prüfer

Bevor ein Entwurf an den User geht, laufen die Skripte, dann prüft ein Prüfer, der den Guide nicht geschrieben hat. Wo es Subagenten gibt (Claude Code, Cowork), startest du ihn als eigenen Agenten ohne den Gesprächsverlauf. Im claude.ai-Chat gibt es keine Subagenten: Dort schnürst du ein Prüfpaket und bittest den User, es in einem neuen Chat prüfen zu lassen. Ein Befund zu einer Tatsache wird nie wegformuliert: belegen oder streichen. Details und Prüfliste: `references/pruefung.md`.

## Was du dem User am Ende gibst

Den Guide als PDF (oder HTML mit Anleitung), die Liste der vorläufigen Punkte, was aus den Quellen nicht übernommen wurde und warum, und den Einbau-Hinweis für das Website-Repo. Nenne Dateien mit Pfad. Schick PDFs und Bilder, statt sie nur zu beschreiben.

## Dateien im Skill

| Ordner | Inhalt |
|---|---|
| `references/` | Ablauf, Einlesen, Entscheidungen, Markenkern, Kapitel, Herleitung, Differenzierung, Tokens, Stack, Prüfung, Hausprofil, Kurzfassungen der vier Design-Skills |
| `scripts/` | siehe oben |
| `assets/guide/` | Mechanik des Guide-Layouts (Seiten, Umbrüche, Druck), keine Gestaltung |
| `assets/richtungen/` | Bildtafel für Stilrichtungen |
| `assets/beispiele/` | Gerüste für Musterseite, Social-Kachel, Cover |
| `assets/code/` | Bausteine, Leitplanken, Vorlagen für DESIGN.md und PRODUCT.md |
| `vendor/` | die vier Design-Skills im Original mit Lizenzen, Stände in `VERSIONEN.md` |
