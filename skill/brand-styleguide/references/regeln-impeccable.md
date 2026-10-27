# Regeln: Impeccable (Kurzfassung)

| | |
|---|---|
| Quelle | github.com/pbakaus/impeccable, Ordner `.claude/skills/impeccable` (Paul Bakaus), Skill-Version 4.7.1 |
| Stand | Commit `3671d50f0ac9a662ce0615e85a256110c9cd720b` vom 25.10.2026 |
| Lizenz | Apache 2.0, `vendor/impeccable/LICENSE` und `NOTICE.md` |
| Original | `vendor/impeccable/SKILL.original.md` und `vendor/impeccable/reference/*.md` |

Eigene deutsche Kurzfassung mit Fundstellen, keine Übersetzung. Im Zweifel gilt das Original.

**Nur als Regelwerk.** Das Programm `scripts/impeccable` liegt nicht bei und wird nicht genutzt: kein `context`, kein Detektor `detect`, kein `concept-seed`, kein Live-Modus, keine Hooks, keine Ablage unter `.impeccable/`. Verlangt das Original einen solchen Befehl, gilt er hier nicht. Den mechanischen Befund ersetzen die Skripte dieses Skills und das Lesen des Prüfers.

**Klassen:** K1 Mindeststandard (gilt immer, Abweichung nur als ausdrückliche Entscheidung des Users), K2 Stil (die Marke gewinnt, Abweichung begründet in Kapitel 0), K3 Handwerk (Standard, Ausnahme mit Begründung). Arbeitsregeln zum Vorgehen führt diese Datei als K3.

## Wofür der Skill es nutzt

**P5 Richtungen:** Die Verweigern-Liste aus `craft-floor.md` und die Abschnitte 1, 3 und 4 aus `new-work.md` (Bestand klären, Farbstrategie, Schriftreflexe, Kalibrierung) sind die Gegenprobe für jede Stilrichtung. `bolder.md` beschreibt, wie „mutiger“ entsteht, ohne die Marke zu verlassen.

**P7 Prüfung:** Der Prüfer nutzt `craft-floor.md` (prüfen und verweigern), `critique.md` (Spezifitätsurteil, Heuristiken, Schweregrade) und `audit.md` (fünf Dimensionen), dazu die Vertiefungen zu Typografie, Farbe, Layout und Bewegung.

**P6 Format:** `DESIGN.md` und `PRODUCT.md` entstehen so, dass Impeccable im Kunden-Repo direkt darauf arbeiten kann (Abschnitte unten).

## Grundsätze

| Regel | Klasse | Fundstelle |
|---|---|---|
| Das Briefing gewinnt: festgelegte Ästhetik, Epoche, Material, Schriften und Paletten gelten, auch gegen eine Warnung vor gesättigten Mustern | K2 | SKILL › How to design |
| Verfeinern bewahrt Identität, Verhalten, Text und alles außerhalb des Auftrags. Neugestaltung ersetzt den alten Look und nutzt ihn als Beleg, was der Gegenstand ist. Nie halb und halb | K3 | SKILL › How to design |
| Sachliche Texte und Behauptungen nur nach Rückfrage ändern oder ergänzen | K3 | SKILL › How to design |
| Belastete Symbole (Militarismus, Überlegenheit, Hassbewegungen) nie als Motiv, Abzeichen oder Ornament. Inhalt, der sie sachlich dokumentiert, bleibt | K1* | SKILL › How to design |
| Fehlt `DESIGN.md`, ist ein Projekt nicht ohne Gestaltung: Was im Code steht, ist Beleg | K3 | SKILL › How to design |
| Anspruch nach Modus der Fläche, nicht des Produkts: Persuade (Marketing, Landingpage, Preise) und Experience (Portfolio) mit voller Haltung, Operate (Werkzeuge) und Read (Doku, Artikel, Guides) mit Präzision und Zurückhaltung | K3 | SKILL › Modes |
| Gerendert in den ausgelieferten Größen prüfen, Prüfungen bündeln statt nach jeder Kleinigkeit | K3 | SKILL, Core principles |

\* Kein Barrierefreiheitsthema. Der Skill behandelt diese Grenze wie K1: Abweichung nur als ausdrückliche Entscheidung.

## Qualitätsboden: prüfen

| Regel | Klasse | Fundstelle |
|---|---|---|
| Kontrast: Fließtext und Platzhalter mindestens 4,5 : 1, große Schrift mindestens 3 : 1 | K1 | craft-floor › Verify |
| Auf farbigen Flächen Nebentext aus dem Farbton oder der Vordergrundfarbe tönen, nie Grau | K2 | craft-floor › Verify |
| Tiefe: Schatten mit Versatz und weicher Unschärfe. Farbiger Schein ohne Versatz ist Dekoration | K2 | craft-floor › Verify |
| Abstände: enge Gruppen, großzügige Trennung, über einer Überschrift mehr Raum als darunter (berechnete Werte lesen) | K3 | craft-floor › Verify |
| Schrift: Lesebreite 65–75 Zeichen, Display höchstens 6 rem, Laufweite nicht enger als −0,04 em, ausgeglichene Überschriften, deutliche Stufen in Größe und Gewicht, echter Text in jedem Breakpoint | K3 | craft-floor › Verify |
| Bewegung: ein gestalteter Moment, keine verstreuten Effekte und keine gleiche Einblendung je Sektion. Exponentielles Ausklingen aus einem schon sichtbaren Zustand. Blur, Backdrop-Filter, Clip-Path, Maske und Schatten gehören zur Palette, solange sie flüssig laufen | K2 | craft-floor › Verify |
| Zustände: Hover, deaktiviert, Laden, Fehler, leer, dazu echter Inhalt, funktionierende Steuerung, responsive Komposition, Tastaturfokus (Fokus selbst K1) | K3 | craft-floor › Verify |
| Browser-Flächen aus der Palette gestalten: Textauswahl, Einfügemarke, eigene Scrollbalken, Fokusring, Unterstreichungsabstand, Ziffern in Tabellen | K3 | craft-floor › Verify |
| Text in der Sprache des Produkts. Steuerelemente nennen ihre Handlung, Fehler nennen Problem und Ausweg | K3 | craft-floor › Verify |
| Jede Anforderung des Briefings ist vorhanden und in Sekunden auffindbar | K3 | craft-floor › Verify |

## Reflexe, die man verweigert

Die Quelle nennt diese Muster Standards der Kategorie, keine Verbote: Das Briefing kann sie begründen. Einzige Ausnahme ist die Eyebrow (siehe Zeile).

| Regel | Klasse | Fundstelle |
|---|---|---|
| Seitenstruktur aus gleich großen Karten mit Icon, Überschrift und Text. Verschachtelte Karten sind laut Quelle immer falsch | K2 | craft-floor › Refuse |
| Hero-Kennzahl-Vorlage: große Zahl, kleines Label, Kennzahlen, Akzent | K2 | craft-floor › Refuse |
| Kicker oder Eyebrow über einer Überschrift. **In der Quelle ein Bann, den kein Briefing aufhebt.** In diesem Skill K2 nach Konzept 4.2 | K2 | craft-floor › Refuse |
| Abschnittsnummern 01 / 02 / 03, außer die Abfolge trägt Information | K2 | craft-floor › Refuse |
| Modal für eine Aufgabe, die weder Unterbrechung noch geschützten Fokus braucht | K3 | craft-floor › Refuse |
| Verlaufstext. Betonung entsteht über Gewicht oder Größe | K2 | craft-floor › Refuse |
| Glas und Blur als Dekoration statt als gezielter Effekt | K2 | craft-floor › Refuse |
| Farbiger Rand links oder rechts über 1 px an Karten, Listeneinträgen, Hinweisen, Alerts | K2 | craft-floor › Refuse |
| Harte Versatzschatten (`box-shadow: 4px 4px 0`) außerhalb einer wirklich neobrutalistischen Welt | K2 | craft-floor › Refuse |
| Sparklines, Fortschrittsringe und weiche Rechtecke als Ersatz für Inhalt | K2 | craft-floor › Refuse |
| Monospace als Kostüm für „technisch“ statt für Code, Daten, Maße | K2 | craft-floor › Refuse |
| Systemschrift als Display-Stimme (Impact, Arial Black, Plattform-Grotesk). Eine passende Schrift besorgen und selbst hosten | K2 | craft-floor › Refuse |
| Unicode-Zeichen oder Emoji statt Iconsystem. Icons aus echter Bibliothek oder eigenem SVG, ein Strich, ein Gewicht | K3 | craft-floor › Refuse |
| Geometrische Masken statt echter Kontur bei Fotomotiven. Alphamaske aus dem Bild ableiten oder Freisteller produzieren | K3 | craft-floor › Refuse |
| Hell oder dunkel nach Branche gewählt. Stattdessen aus der Nutzungsszene: wer, wo, bei welchem Licht | K2 | craft-floor › Refuse |

## Neue Gestaltung: Richtung finden

| Regel | Klasse | Fundstelle |
|---|---|---|
| Erst klären, was schon gilt: Neugestaltung, bestehende Welt, unvollständige Marke oder keine visuelle Autorität. Bestätigte Assets und erkennbare Züge bleiben | K3 | new-work › 1 |
| Kandidaten aus der Kulturwelt der Zielgruppe: sieben konkrete visuelle Systeme, Artefakte, Orte oder Rituale, nach Resonanz geordnet. Die Seite, die die Branche immer baut, und ihr vorhersehbares Gegenteil bleiben draußen | K3 | new-work › 3 |
| Auf Werkzeug- und Leseflächen keine Welt aus den Geräten, die die Zielgruppe bedient (Terminal, Messgerät, Schaltpult): Sie wird Kostüm | K2 | new-work › 3 |
| Farbstrategie vor Farben: zurückhaltend (getönte Neutrale plus ein Akzent), engagiert (eine gesättigte Farbe trägt 30–60 % der Fläche), volle Palette (3–4 benannte Rollen), getränkt (die Fläche ist die Farbe) | K2 | new-work › 4 |
| Hell oder dunkel ist nie Standard. Ein Satz zur physischen Szene entscheidet | K2 | new-work › 4 |
| Diese Schriften gelten als Trainings-Standards und brauchen einen Grund, den keine andere Schrift erfüllt (Themen-Assoziation zählt nicht): Fraunces, Playfair Display, Cormorant, Lora, Crimson, Newsreader, Syne, Space Grotesk, Space Mono, IBM Plex, Inter als Display, DM Sans, DM Serif, Outfit, Plus Jakarta Sans, Instrument Sans | K2 | new-work › 4 |
| Kalibrierung: Cremegrund mit Serife und Terrakotta oder Signalrot; Fast-Schwarz mit Neonakzent und Leuchtkanten; Zeitungshaarlinien mit kursiver Serife und kleinen Mono-Labels; flache gesättigte Farbe mit schwarzen Kästen, harten Schatten, schwerer Condensed. Lässt sich der Look aus der Branche erraten, nacharbeiten | K2 | new-work › 4 |
| Warme, buchnahe und kindbezogene Themen führen reflexhaft zu Creme, Serife und Lampenlicht. Diesen ersten Entwurf als verbraucht betrachten | K2 | new-work › 4 |
| `DESIGN.md` beschreibt die gebaute Welt, nicht den Plan | K3 | new-work › 5; degraded/documenter |

## Vertiefungen

| Regel | Klasse | Fundstelle |
|---|---|---|
| Fließtext mindestens 1 rem / 16 px, außer eine dichte Rolle, eine Plattformkonvention oder eine Nutzereinstellung begründet es | K1 | typeset › Apply |
| Lesebreite 45–75 Zeichen. Zeilenabstand umgekehrt zur Zeilenlänge, abgestimmt auf Schrift, Breite und Sprache, kein Einheitsverhältnis | K3 | typeset › Apply |
| Heller Text auf Dunkel: etwas mehr Zeilenabstand, etwas Laufweite, eine Gewichtsstufe mehr, wenn die Schrift es braucht | K3 | typeset › Apply |
| Wenige Rollen und Familien. Eine zweite Familie nur für eine Rolle, die nur sie erfüllt | K2 | typeset › Set the system |
| Namen von Rollen und Tokens beschreiben den Zweck, nicht den Wert | K3 | typeset › Set the system |
| Nur genutzte Schriftschnitte laden, metrisch passende Ersatzschriften, kein unsichtbarer Text beim Laden | K3 | typeset › Apply |
| Browser-Zoom, Schrifteinstellungen und Textskalierung der Nutzer bleiben erhalten | K1 | typeset › Apply |
| Absätze über Abstand oder Einzug trennen, nicht beides | K2 | typeset › Apply |
| `text-wrap: balance` für Überschriften, `pretty` für Fließtext. Umbrüche von Hand nur zwischen Sinneinheiten, in jeder Breite geprüft | K3 | typeset › Line breaks |
| Rollen statt Farbmuster: Grund und erhöhte Flächen, Text primär und sekundär, Handlung, Fokus, Auswahl, Linien, Erfolg, Warnung, Fehler, Info, Datenreihen | K3 | colorize › Choose a strategy |
| Farbton aus der Bedeutung des Produkts und der Richtung, nie aus einer Branchen-Assoziation | K2 | colorize › Choose a strategy |
| Neue Web-Paletten bevorzugt in OKLCH, sonst den Farbraum des Projekts beibehalten | K3 | colorize › Choose a strategy |
| Die stärkste Farbe besitzt eine bewusste Fläche oder Rolle. Die Farbe der Haupthandlung nicht für Dekoration verbrauchen | K2 | colorize › Apply |
| Neutrale nur tönen, wenn der Markenton Zusammenhalt stiftet. Neutrales Grau ist zulässig | K2 | colorize › Apply |
| Kontrast: Fließtext 4,5 : 1, große Schrift 3 : 1, Steuerelemente, Icons und Fokus 3 : 1. Auch Zustände, Overlays, Text auf Bild, beide Modi. Farbfehlsichtigkeit simulieren, Farbe nie allein | K1 | colorize › Contrast and perception |
| Dunkelmodus eigens komponieren, nicht invertieren. Ein Themewechsel ordnet semantische Rollen neu zu | K3 | colorize › Apply |
| Explizite Farben statt Ketten aus Transparenzen, weil Alpha den Kontrast vom Untergrund abhängig macht | K3 | colorize › Contrast and perception |
| Squint-Test: unscharf betrachtet sind Primäres, Sekundäres und die Gruppen in Reihenfolge erkennbar | K3 | layout › Two isolated assessments |
| Nach Bedeutung gruppieren, Nähe vor Containern. Rhythmus aus engen und großzügigen Abständen | K3 | layout › Apply |
| Dokumentierte Abstandsskala statt Einzelwerte. Eine 4er-Basis liefert Zwischenstufen, die einer reinen 8er-Reihe fehlen | K3 | layout › Apply |
| Wiederholte Karten, Spalten, Sektionen nur, wenn die Inhalte wirklich gleichwertig sind. Tiefe nur, wenn sie Zustand oder Hierarchie klärt | K2 | layout › Two isolated assessments, Apply |
| Tastatur-, Touch- und Screenreader-Reihenfolge entspricht der sichtbaren. Trefferflächen bleiben nutzbar, auch wenn das Sichtbare klein ist | K1 | layout › Apply, Verify |
| Bewegung erklärt Zustand, Beziehung oder Hierarchie oder ist der eine verdiente Moment. Generisches Einblenden, Hover-Anheben, Parallax und Scroll-Reveal sind keine These | K2 | animate › Set the motion thesis |
| Dauern: 100–150 ms Sofort-Rückmeldung, 150–300 ms Zustandswechsel, 300–500 ms Layout, Overlay, Ansichtswechsel, 500–800 ms ein gestalteter Auftritt | K3 | animate › Timing and easing |
| Ausgang schneller als Eingang, natürliches Abbremsen (Beispiel `cubic-bezier(0.16, 1, 0.3, 1)`), kein Federn und keine Elastik aus Reflex | K3 | animate › Timing and easing |
| Inhalt ist im Ausgangszustand sichtbar, damit ein Skriptfehler die Seite nicht versteckt. `will-change` nur während der Animation | K3 | animate › Implement to the runtime |
| Jede Web-Animation hat einen Pfad für reduzierte Bewegung: Raumbewegung weg, bedeutungstragende Rückmeldung bleibt. Pauschales Abschalten aller Bewegung ist ein Befund | K1 | animate › Accessibility and control; audit › 1 |
| Gestaffeltes Einblenden nur für echte Listen, mit begrenzter Gesamtverzögerung. Nicht wesentliche Schleifen stoppen außerhalb des Sichtfelds | K2 | animate › Choose material, Accessibility |

## Kritik, Audit, mutiger und leiser

| Regel | Klasse | Fundstelle |
|---|---|---|
| Zuerst das Spezifitätsurteil, vor jedem mechanischen Befund: Wirkt das Ergebnis für dieses Produkt gemacht, oder könnte ein fremdes Produkt es unverändert nutzen? | K3 | critique › Assessment A, Design Specificity Verdict |
| Gestaltungsreview und mechanischer Befund laufen getrennt, ohne Einblick ineinander | K3 | critique › Hard Invariants |
| Nielsens 10 Heuristiken je 0–4. Bänder: 36–40 sehr gut, 28–35 gut, 20–27 akzeptabel, 12–19 schwach, 0–11 kritisch. Heuristik 7 und 10 dürfen auf Persuade- und Experience-Flächen „n/a“ sein, dann prozentual werten | K3 | critique › Heuristics Scoring Guide |
| Kognitive Last: höchstens 4 sichtbare Optionen je Entscheidung, Gruppen mit höchstens 4 Einträgen. Checkliste mit 8 Punkten, ab 4 Fehlern kritisch | K3 | critique › Cognitive Load Assessment |
| Schweregrade: P0 blockiert, P1 schwer (auch jeder WCAG-AA-Verstoß), P2 gering, P3 Feinschliff | K3 | critique › Issue Severity; audit › Detailed Findings |
| Personas nach Oberfläche, für Landingpages Jordan (Erstnutzer), Riley (Stresstest), Casey (mobil, abgelenkt). Weitere Personas nur aus echtem Markenkontext | K3 | critique › Persona-Based Design Testing |
| Audit in fünf Dimensionen je 0–4 (Barrierefreiheit, Performance, Theming, Responsive, Umsetzungstreue), Summe von 20 | K3 | audit › Diagnostic Scan |
| Trefferflächen 44 × 44 px. WCAG 2.5.8 verlangt mindestens 24 × 24 CSS-px, mit Ausnahmen | K1 | audit › 4 Responsive Design |
| Keine fest codierten Farben außerhalb der Tokens, Dunkelmodus vollständig | K3 | audit › 3 Theming |
| „Mutiger“ verstärkt, was das System schon besitzt. Keine neue Farbe, Schrift oder Grundform ohne Rückfrage. Skelett-Test: Die Struktur ohne Text sagt noch, worum es geht | K3 | bolder |
| „Leiser“ heißt verfeinert, nicht generisch: Sättigung auf 70–85 %, Neutrale dominieren, Akzent um 10 %, Gewichte senken (etwa 900 auf 600), nie Grau auf Farbe, kein Federn | K2 | quieter |

## Typische Konflikte mit Marken

| Bestand der Marke | Regel | Behandlung |
|---|---|---|
| Eyebrows oder Kicker | craft-floor: Bann | K2 nach Konzept, die Marke gewinnt begründet. Offener Punkt für die Verträglichkeit: Impeccable-Werkzeuge im Kunden-Repo melden das Element weiter, und `degraded/documenter.md` verbietet, ein Bann-Element in `DESIGN.md` als Regel zu führen |
| Hausschrift steht auf der Liste der Trainings-Standards (z. B. Inter, Space Grotesk) | new-work › 4 | K2. Dass sie die Schrift der Marke ist, ist der verlangte Grund. Eine neu gewählte Schrift von der Liste braucht eine Herleitung |
| Bestand entspricht einem Kalibrierungs-Look | new-work › 4, craft-floor | K2. Bestand gewinnt, das Eigene muss aus Signaturen und Markenmaterial kommen (Blindtest) |
| farbige Seitenränder an Hinweisboxen, Verlaufstext, Glas, harte Versatzschatten | craft-floor › Refuse | K2. Bleibt, wenn die Marke es begründet, sonst Vorschlag in Runde 1 |
| hell oder dunkel nach Branche | craft-floor, new-work | K2. Die Nutzungsszene steht als Herleitung im Guide |
| Animation über `transform` und `opacity` hinaus | craft-floor, animate: erlaubt; Vercel: verboten | K3. Ausnahme mit Begründung und Messung auf dem Zielgerät |
| Lesebreite | 65–75 (craft-floor, operate) gegen 45–75 (typeset) | K3. Impeccable ist in sich uneinheitlich, frontend-design nennt unter 80 Zeichen, ui-ux-pro-max 65–75. Der Wert kommt als `layout.lesebreite` aus der Marke, begründet |
| Farbformat | OKLCH bevorzugt, explizite Farben statt Transparenz | K3. `tokens.md` verlangt `#RRGGBB` und erlaubt Deckkraft nur über `color-mix`. Das Kontrastskript mischt vor dem Rechnen, damit bleibt der Kontrast prüfbar |

## Verzeichnis: welche Datei für welche Frage

| Datei in `reference/` | Der Prüfer schlägt sie auf, wenn … |
|---|---|
| `craft-floor.md` | … Mindestqualität und verweigerte Reflexe zu prüfen sind (P5 Gegenprobe, P7) |
| `critique.md` | … zu urteilen ist, ob das Ergebnis spezifisch ist: Heuristiken, kognitive Last, Personas, Schweregrade |
| `audit.md` | … die technische Prüfung in fünf Dimensionen mit Bewertungsbändern ansteht |
| `typeset.md` | … Schriftrollen, Skala, Lesebreite, Umbrüche oder das Laden von Schriften fraglich sind |
| `colorize.md` | … Farbrollen, Farbstrategie, Kontrasttabelle oder Dunkelmodus zu prüfen sind |
| `layout.md` | … Gruppierung, Rhythmus, Abstandsskala oder Reihenfolge fraglich sind |
| `animate.md` | … Bewegungsthese, Dauern, Kurven oder reduzierte Bewegung zu prüfen sind |
| `new-work.md` | … eine Stilrichtung gegen Bestand, Farbstrategie, Schriftreflexe und Kalibrierung zu halten ist (ohne `concept-seed`) |
| `bolder.md`, `quieter.md` | … eine Richtung „mutiger“ oder ein Dämpfen ohne Generik zu bewerten ist |
| `document.md` | … `DESIGN.md` zu schreiben oder auf Verträglichkeit zu prüfen ist |
| `init.md` | … `PRODUCT.md` zu schreiben oder zu prüfen ist |
| `degraded/documenter.md` | … zu prüfen ist, ob `DESIGN.md` nur Gebautes enthält und kein Bann-Element als Regel führt |
| `polish.md` | … die Endkontrolle ansteht: Zustände, Konsistenz, Abweichung von Tokens, Reihenfolge der Behebung |
| `clarify.md` | … Texte in Bedienelementen, Begriffe und Lokalisierung zu prüfen sind (Kapitel 12) |
| `harden.md` | … Randfälle zu prüfen sind: lange Texte, leere Daten, Übersetzung (30–40 % Platzreserve, Deutsch ist meist die längste Sprache) |
| `adapt.md` | … Responsives, Breakpoints, Touch oder die Module Druck und Mail zu prüfen sind |
| `operate.md`, `mode-persuade.md`, `mode-read.md`, `mode-operate.md` | … zu klären ist, was der Modus erlaubt: Website meist Persuade, der Guide selbst Read |
| `delight.md` | … ein Moment mit Persönlichkeit zu bewerten ist, etwa ein Signatur-Element |
| `distill.md` | … zu prüfen ist, ob etwas überflüssig ist |
| `extract.md` | … in der Auswertung zu entscheiden ist, was Token oder Baustein wird (erst ab dreifacher Nutzung mit gleicher Absicht) |
| `optimize.md` | … Performance zu prüfen ist (LCP unter 2,5 s, INP unter 200 ms, CLS unter 0,1) |

**Für diesen Skill nicht relevant:** native Apps (`ios.md`, `android.md`, `adapt.native.md`, `audit.native.md`), Programm, Live-Modus und Befehlsmenü (`live.md`, `live-setup.md`, `generate.md`, `hooks.md`, `doctor.md`, `routing.md`), Bildentwürfe und Asset-Pipeline des Programms (`visualize.md`, `region-map.md`, `component-review.md`, `degraded/asset-producer.md`, `degraded/finish-reviewer.md`, `degraded/manual-edit-applier.md`), Erststart in Apps (`onboard.md`), eigenes Briefing-Interview (`shape.md`, der Skill hat P1), Effekte jenseits der Konvention (`overdrive.md`) und der veraltete Alias `craft.md`.

## DESIGN.md laut Impeccable (`document.md`)

**Zweck:** Datei in der Projektwurzel, die Coding-Agenten beim Bauen neuer Seiten in der Marke hält. Das Format folgt der DESIGN.md-Spezifikation von Google Labs (Stitch). Die Tokens im Kopf sind verbindlich, der Text erklärt ihre Anwendung.

**Kopf (YAML, maschinenlesbar):**
- Erlaubte Gruppen: `name`, `description`, `colors`, `typography`, `rounded`, `spacing`, `components`. Keine weiteren Gruppen oben, also kein `motion`, `breakpoints`, `shadows`.
- Verweise als `{colors.primary}`. Komponenten dürfen auf Grundwerte verweisen, Grundwerte nicht aufeinander.
- Farben als gültiger CSS-Farbwert, Hex empfohlen. Ein Format, kein zweiter Wert im Text.
- Typografie je Rolle als Objekt mit nur den echten Eigenschaften (`fontFamily`, `fontSize`, `fontWeight`, `lineHeight`, `letterSpacing`, `fontFeature`, `fontVariation`).
- Schlüssel der Skalen sind offen: Namen des Projekts verwenden, nicht in Material-Namen umbenennen.
- Komponenten mit höchstens diesen 8 Eigenschaften: `backgroundColor`, `textColor`, `typography`, `rounded`, `padding`, `size`, `height`, `width`. Varianten als Geschwister (`button-primary`, `button-primary-hover`).

**Textteil:** acht Abschnitte in fester Reihenfolge mit genau diesen englischen Überschriften. Weglassen ist erlaubt, umbenennen nicht, weil Werkzeuge die Überschriften lesen. Unbekannte zusätzliche Abschnitte bleiben erhalten.

| Abschnitt | Inhalt |
|---|---|
| `## Overview` | „Creative North Star“ als benannte Metapher, 2–3 Absätze zu Persönlichkeit, Dichte, Ästhetik, nur bestätigte Ablehnungen, Liste „Key Characteristics“ |
| `## Colors` | Charakter in einem Satz, Gruppen Primary, Secondary und Tertiary (nur wenn vorhanden), Neutral. Je Farbe beschreibender Name, Wert, wo und warum |
| `## Typography` | Display-, Body- und ggf. Label-Schrift mit Ersatz, Charakter, Hierarchie Display, Headline, Title, Body, Label mit Gewicht, Größe, Zeilenhöhe |
| `## Layout` | Raster, Container, Dichte, Responsives, Abstandsrhythmus. Werte nur, wenn belegt |
| `## Elevation & Depth` | Schatten, tonale Schichten oder beides. „Keine Schatten“ ausdrücklich sagen. Schattenvokabular mit Wert |
| `## Shapes` | Radien, Ecken, Ränder, Beschnitt, wiederkehrende Formen |
| `## Components` | je Baustein eine Charakterzeile, Form, Farbzuordnung, Zustände (Buttons, Chips, Karten, Felder, Navigation, Signatur-Baustein) |
| `## Do's and Don'ts` | konkrete Leitplanken, jede beginnt mit „Do“ oder „Don't“, Werte nur, wenn festgelegt |

**Schreibweise:** beschreibend vor technisch, der exakte Wert in Klammern. „Named Rules“ im Muster `**The … Rule.**`, ein bis drei je Abschnitt. Harte Sprache nur für echte Invarianten. Nichts aus `PRODUCT.md` doppeln, keine erfundenen Komponenten oder Tokens, keine Klassennamen aus dem Code. Bestehende `DESIGN.md` nie still überschreiben: zeigen und fragen (auffrischen, ersetzen, zusammenführen). Ein Verbot darf kein Mittel treffen, das die Marke selbst nutzt (`degraded/documenter.md`).

**Beiwerk:** Die Datei `.impeccable/design.json` (schemaVersion 2) ergänzt Tonleitern je Farbe, Schatten, Bewegung, Breakpoints, 5–10 Bausteine als eigenständige HTML/CSS-Schnipsel mit Präfix `ds-` und einen Erzählteil. Sie dient dem Live-Panel des Programms. Das Konzept regelt sie nicht. Vor der ersten Umsetzung gibt es einen Seed-Modus mit Kommentar `<!-- SEED: … -->` und nur `name` und `description` im Kopf.

**Zuordnung zu `tokens.md` (nicht geregelt, Vorschlag zur Entscheidung):** `farbe.rolle.*` nach `colors`, `schrift.web.*` nach `typography`, `radius` nach `rounded`, `abstand` nach `spacing`, Bausteine nach `components`. `bewegung`, `schatten` und `layout.breakpoints` gehören nicht in den Kopf, sondern in den Text oder in das Beiwerk. Offen ist, ob deutsche Rollennamen im Kopf verträglich sind: Die Quelle nennt Skalen-Schlüssel offen, zeigt bei Typografie aber englische Rollen. Ebenfalls offen: wohin Mindeststandards und Checkliste aus Konzept 6.3 kommen, weil die acht Abschnitte sie nicht vorsehen.

## PRODUCT.md laut Impeccable (`init.md`)

**Zweck:** dauerhafte Produktwahrheit in der Projektwurzel. Nur bestätigte Fakten, offene Entscheidungen als solche markiert, unpassende Abschnitte weglassen. Gehört nicht hinein: visuelle Welt, Paletten, Schriften, Komponenten, Seitenkonzepte, Modus, erfundene Belege (Testimonials, Kunden, Kennzahlen, Preise).

**Aufbau:** Überschrift `# Product`, darunter wörtlich der Kommentar `<!-- impeccable:product-schema 1 -->`, dann:

| Abschnitt | Inhalt |
|---|---|
| `## Platform` | nur der Wert `web`, `ios`, `android` oder `adaptive` |
| `## Stack` | nur bei neuen Projekten: die Antwort des Users |
| `## Users` | Hauptnutzer, ihre Situation und Aufgabe |
| `## Product Purpose` | was das Produkt tut, warum es existiert, was Erfolg ist |
| `## Positioning` | Mechanismus oder Anspruch, den ein Nachbarprodukt nicht wahrheitsgemäß kopieren kann |
| `## Operating Context` | Abläufe, Umgebungen, Werkzeuge, Dokumente, Rituale |
| `## Capabilities and Constraints` | bestätigte Funktionen, technische Grenzen, Begriffe, offene Fakten |
| `## Brand Commitments` | Name, Stimme, Assets, Persönlichkeit, verbindliche Vorgaben zur Identität |
| `## Evidence on Hand` | echte Inhalte, Daten, Referenzen, Presse mit Pfad, Fehlendes ausdrücklich benannt |
| `## Product Principles` | 3–5 dauerhafte strategische Prinzipien, keine visuellen Rezepte |
| `## Accessibility & Inclusion` | bekannte Bedarfe oder geforderter Standard |

**Aus dem Markenkern (P4):** Zielgruppe nach `Users`, Positionierung nach `Positioning`, Werte, Persönlichkeit und Ton nach `Brand Commitments`. Die Gestaltungsprinzipien des Guides sind visuell und gehören nach `DESIGN.md`, nicht nach `Product Principles`.
