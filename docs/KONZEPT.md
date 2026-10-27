# Skill `brand-styleguide` · Konzept

> **Stand:** 0.2 · freigegeben von Max am 26.10.2026 (Go für Bau und Downloads), K1–K7 entschieden
>
> **Grundlage:** Startprompt `PROMPT-SKILL-BRAND-STYLEGUIDE-2026-10-23.md`, Antworten Runde 1 und 2 (23.10.), Vorbild AI READY Brand & Style Guide v1.4
>
> **Gebaut wird erst nach deinem Go** (Abschnitt 11), mit `skill-creator` und Evals.

---

## 0 · Kurzfassung

Der Skill erstellt für eine Marke einen kompletten Brand & Style Guide: ein in sich geschlossenes Design System, das sich aus der Marke ableitet. Er liest die Website, vorhandene Vorgaben und Dateien, legt Widersprüche zur Entscheidung vor, stellt zwei bis drei Stilrichtungen als Bild zur Wahl und arbeitet die gewählte Richtung aus. Am Ende stehen ein Guide im Layout der Marke (Markdown und PDF), Design Tokens, Bausteine für Next.js, Tailwind und Sanity, Leitplanken im Code und eine Regeldatei für Claude Code. Damit baut Claude Code die Website danach gleich im System der Marke.

Gegen das Einheitssystem wirken vier Dinge zusammen: Der Skill enthält **keine Standardwerte** (keine Farbe, Schrift, Rundung oder Stilrichtung), jede Regel braucht eine **Herleitung** aus der Marke, ein **Achsenprofil** misst, ob das Ergebnis zur Marke passt, und ein **Blindtest** mit erfundenen Ablenker-Marken prüft in jedem Lauf, ob das System erkennbar zu genau dieser Marke gehört.

Der User entscheidet an vier Stellen: im Briefing, in drei kurzen Runden (Markenkern und Widersprüche, Stilrichtung, Freigabe). Kein Widerspruch wird still aufgelöst.

---

## 1 · Rahmen (entschieden)

| Thema | Entscheidung |
|---|---|
| Name, Absender | `brand-styleguide`, Absender AI READY im Kolophon, auch bei Marken der Gruppe (A3, A8) |
| Plattform | alle Claude-Oberflächen, ein Skill im Agent-Skills-Format (A5 a). Ein Kern läuft überall, Werkzeuge werden genutzt, wo sie da sind (A6 b) |
| Nutzer | Owner der Marken der Gruppe (meist ohne Design-Erfahrung), Max und Team für externe Kunden (A2, A7) |
| Zweck | intern genutzt, Grundlage für Kunden-Websites mit Claude Code und Sanity (A4) |
| Input | Pflicht: Quelle zur Marke, Briefing, Logo als Vektor. Optional: Vorgaben, Wettbewerber, Vorbild-Websites für digitale Designsysteme, Wissen als lokale Dateien (B1, B5, F4) |
| Einlesen | Tavily, wo vorhanden (nur Max), sonst Headless Chrome, sonst hochgeladene Screenshots (B2) |
| Vertraulichkeit | keine Sonderregel (B3 a) |
| Neue Marke | Markenkern-Interview (B4 b) |
| Output | Markdown + PDF aus HTML, Web-Seite optional; Tokens, Komponenten-Code, Leitplanken; Regeldatei für Coding-Agenten (C1, C2, C8) |
| Stack | Standard Next.js, Tailwind v4, Sanity, abschaltbar (C7 c) |
| Sprache | Sprache der Marke, Standard Deutsch (C3) |
| Layout des Guides | in der Gestaltung der Marke (C4) |
| Schriften | Kunde liefert Dateien, freie Ersatzschrift nur für Entwürfe (C5) |
| Ablage | je Lauf erfragt, Vorschlag `~/Documents/Building/Brand-Guides/<marke>/` (C6) |
| Umfang | Pflicht-Kern + Kanal-Module, Markenkern auf einer Seite, Regeln + Anwendungsbeispiele, Logo nie neu zeichnen, keine Bestandsbilanz als Lieferung, Auswertung als Arbeitsdatei (D1–D5) |
| Entscheidungen | Text + Bild mit Fundstelle, drei kurze Runden, „mach du“ wird als vorläufig markiert; Version + Freigabevermerk je Version, kein Protokoll je Entscheidung (E1–E5) |
| Differenzierung | Herleitung + Blindtest + Achsenprofil, 2–3 Stilrichtungen, Ablenker statt dritter Testmarke (F1, F2, F6) |
| Vier Design-Skills | mitgeliefert in `vendor/` mit Lizenzen, Versionen fest, deutsche Kurzfassung; Mindeststandards gelten immer, bei Stilregeln gewinnt die Marke; ui-ux-pro-max als Quelle und Prüfung (G1–G4) |
| Qualität | alle Pflichtprüfungen, Prüfer getrennt vom Ersteller, höchstens 2 Runden; Evals bewertet Max (H1–H3) |
| Pflege | Versionierung ja, kein Nachziehen an mehrere Orte, Fortschreiben wird ein eigener Skill nach v1, Hausprofil „falkemedia“ ja (I1–I4, J1) |
| Projekt | `~/Documents/Building/brand-styleguide-skill` (lokal angelegt), GitHub privat in AI-Ready-GmbH erst nach Go (I3, I5) |

---

## 2 · Ablauf: Phasen mit Ein- und Ausgaben

Jeder Lauf hat einen eigenen Ordner (Abschnitt 8.2). Was der Skill erarbeitet, steht dort als Datei. So kann ein Lauf unterbrochen und fortgesetzt werden, und jede Aussage im Guide lässt sich bis zur Fundstelle zurückverfolgen.

| Phase | Eingabe | Was passiert | Ausgabe |
|---|---|---|---|
| **P0 Start** | Auftrag | Oberfläche und Werkzeuge erkennen (Dateizugriff, Skripte, Browser, Tavily, Subagenten). Marke der Gruppe? Dann Hausprofil laden. Ablageort erfragen | `lauf.json`, Hinweis, welche Werkzeuge fehlen und wie der User sie ersetzt |
| **P1 Briefing** | Antworten des Users | Höchstens 10 Fragen: Marke, Zweck, Zielgruppe, Kanäle (daraus die Module), wer freigibt, Sprache, Stack ja/nein, Quellen, Schriftdateien, Wettbewerber, Vorbilder | `00-briefing.md` |
| **P2 Einlesen** | Website, Dateien | Texte und Struktur der Website; Screenshots bei 375 und 1440 px, hell und dunkel; berechnete Stile (Farben mit Häufigkeit, Schriften, Größen, Radien, Schatten, Abstände, Bewegung); Logos inventarisieren (Vektor? Varianten?); Vorgaben lesen | `arbeit/01-fakten.md` (jede Aussage mit Fundstelle), `arbeit/01-messung.json`, `arbeit/quellen/` |
| **P3 Auswertung** | Faktenblatt, Messung | Was trägt, was nicht; gezählte Befunde; Widersprüche zwischen den Quellen und gegen die Mindeststandards (Kontrast, Größen) | `arbeit/02-auswertung.md` (Arbeitsdatei, nicht Teil des Guides) |
| **P4 Markenkern** | Fakten, Auswertung, ggf. Interview | Werte, Persönlichkeit („wir sind / wir sind nicht“), Positionierung, Zielgruppe, Ton. Soll-Achsenprofil | `arbeit/03-markenkern.md` (eine Seite) |
| ⟶ **Runde 1** | | Markenkern bestätigen, Widersprüche entscheiden (Text, mit Fundstelle) | Entscheidungen in `lauf.json` |
| **P5 Richtungen** | Markenkern, Entscheidungen | 4–6 Gestaltungsprinzipien, je aus einem Wert. 2–3 Stilrichtungen: „nah am Bestand“, „mutiger“, ggf. eine dritte. Jede als Bildtafel mit gleichem Inhalt (Hero, Karte, Buttons, Schriftskala, Palette mit Rollen, Formensprache, Bewegung, Signatur-Element) und eigenem Achsenprofil | `arbeit/04-richtungen/*.png`, `richtungen.md` |
| ⟶ **Runde 2** | | Richtung wählen oder kombinieren (Bild) | Entscheidung |
| **P6 Ausarbeitung** | gewählte Richtung | Tokens zuerst, dann Guide-Kapitel, Bausteine und Leitplanken (falls Stack), Regeldatei, Anwendungsbeispiele | `tokens/`, `guide/` (MD, HTML), `code/`, `DESIGN.md`, `beispiele/` |
| **P7 Prüfung** | alles aus P6 | Skripte (Kontrast, Tokens, Größen, Render), dann ein getrennter Prüfer (Herleitung, Anti-Patterns, technische Regeln, Achsenprofil, Blindtest). Höchstens 2 Überarbeitungen | `arbeit/05-pruefung.md` (PASS/FAIL mit Befunden) |
| ⟶ **Runde 3** | | Entwurf als PDF, offene und vorläufige Punkte | Freigabe |
| **P8 Übergabe** | Freigabe | Version 1.0 mit Freigabevermerk, PDF, Liste „nicht übernommen, weil …“, Einbau-Hinweis für das Website-Repo | fertiger Ordner |

---

## 3 · Wo der User entscheidet und in welcher Form

| Stelle | Inhalt | Form |
|---|---|---|
| Briefing (P1) | Rahmen des Laufs | nummerierte Fragen mit Optionen und Empfehlung |
| Runde 1 (nach P4) | Markenkern (M1 …), Widersprüche (W1 …) | Text. Jeder Widerspruch mit Fundstellen (Quelle, URL oder Seite, Bildausschnitt), Optionen a/b/c, Empfehlung mit einem Satz Grund |
| Runde 2 (nach P5) | Stilrichtung (S1 …) | Bildtafeln, dazu Achsenprofil und Herleitung je Richtung. Kombinieren ist erlaubt („Schrift aus A, Farbe aus B“), der Skill prüft die Kombination und sagt, was dabei bricht |
| Runde 3 (nach P7) | Entwurf zur Freigabe (F1 …), vorläufige Punkte (V1 …) | PDF des Guides und der Anwendungsbeispiele, darunter die offenen Punkte |

**Regeln für alle Runden**

- Höchstens etwa 10 Fragen je Runde, gebündelt und nummeriert. Antwort knapp möglich („W2 b, Rest wie empfohlen“).
- Für Owner ohne Design-Erfahrung: jede Gestaltungsfrage mit Bild, keine Fachbegriffe ohne Erklärung, die Empfehlung in Alltagssprache begründet.
- Eine Empfehlung ist keine Entscheidung. Antwortet der User mit „mach du“, setzt der Skill die Empfehlung ein und markiert sie im Guide sichtbar als **vorläufig**. Alle vorläufigen Punkte stehen gesammelt in Kapitel 15 und in Runde 3.
- Werfen Antworten neue Fragen auf, gibt es eine Zusatzrunde, keine stille Annahme.
- **Dokumentation (E5 b):** Version, Datum, was sich geändert hat, und je Version ein Freigabevermerk (wer, wann). Kein Protokoll je Einzelentscheidung.

---

## 4 · Die vier Design-Skills: Rollen und Konflikte

### 4.1 Rollen im Ablauf

| Skill | Rolle | Phase | Was der Skill daraus nutzt |
|---|---|---|---|
| **frontend-design** (Anthropic, Apache 2.0) | Haltung gegen austauschbares Design | P5, P6 | Erst Absicht und Designplan, dann Umsetzung. Eine klare, mutige Richtung statt Mittelmaß. Prüffrage „Was macht das hier unverwechselbar?“ |
| **Web Interface Guidelines** (Vercel, MIT) | technische Qualität | P6, P7 | Regeln für Tastatur, Fokus, Formulare, Animation, Typografie, Bilder, Performance, Touch, Dark Mode, Lokalisierung. Fließt in Bausteine, Leitplanken, Regeldatei und Checkliste |
| **Impeccable** (Paul Bakaus, Apache 2.0) | Anti-Patterns und Gestaltungskritik | P5, P7 | Der Katalog der Verbote und Reflexe (`craft-floor`), Kritik und Audit, die Vertiefungen zu Typografie, Farbe, Layout und Bewegung. Format der Regeldatei `DESIGN.md` (Abschnitt 6.3) |
| **ui-ux-pro-max** (nextlevelbuilder, MIT) | Grenzwerte und Kandidaten | P5, P7 | Grenzwerte (Kontrast, Größen, Trefferflächen, Dauern). Kataloge (Paletten, Schriftpaare, Stile) nur als Kandidaten, jede Übernahme mit Herleitung aus der Marke (G4) |

Mitgeliefert wird je Skill nur, was der Ablauf braucht, mit Lizenz und festem Stand (`vendor/VERSIONEN.md`). Der Ablauf arbeitet mit einer deutschen Kurzfassung je Skill (`references/regeln-*.md`, mit Quellenangabe). Der Prüfer bekommt zusätzlich die Originale.

**Impeccable nur als Regelwerk:** Impeccable startet im Original ein eigenes Programm, das beim ersten Lauf ein Binary aus dem Netz lädt. Das widerspricht der Plattformneutralität. Der Skill übernimmt deshalb nur die Regeltexte (SKILL.md und `reference/`), nicht das Programm (Frage K3).

### 4.2 Konflikte zwischen Skill und Marke (G3 b)

| Klasse | Beispiele | Regel |
|---|---|---|
| **1 · Mindeststandards** | Kontrast nach WCAG 2.2 AA (Text 4,5 : 1, große Schrift und Linien 3 : 1), Fließtext mindestens 16 px, Trefferflächen 44 px, sichtbarer Fokus, Tastatur, reduzierte Bewegung | gelten immer. Verletzt die Marke sie (z. B. Markenfarbe als Schrift zu hell), legt der Skill das als Widerspruch vor und schlägt eine Lösung in der Marke vor (wie bei uns Gold-Ink statt Gold). Eine Abweichung gibt es nur als ausdrückliche Entscheidung, sichtbar vermerkt |
| **2 · Stil und Geschmack** | „keine Inter“, „keine Eyebrows“, „keine Verläufe“, „Dunkel ist eleganter“ | Die Marke gewinnt. Die Abweichung steht begründet in Kapitel 0 („Wie dieser Guide entstanden ist“), wie bei AI READY |
| **3 · Widersprüche der Skills untereinander** | ein Skill empfiehlt, was ein anderer verbietet | Klasse 1 vor Klasse 2. Sonst entscheidet die Herleitung aus der Marke, im Zweifel als Frage in der nächsten Runde |

---

## 5 · Wie der Skill verhindert, dass jede Marke dasselbe System bekommt

**1 · Keine Standardwerte im Skill.** Der Skill enthält Struktur und Methode, aber keine Gestaltung: keine Palette, keine Schrift, keinen Radius, kein Raster, keinen Standardmodus (hell oder dunkel), keine Signatur. Auch der AI-READY-Guide liegt nicht als Vorlage bei (Frage K1). Die Vorlage für die PDF-Seiten liefert nur Seitenformat, Satzspiegel und Mechanik. Cover, Kapitelauftakt und Anwendungsbeispiele gestaltet der Lauf je Marke.

**2 · Herleitungskette als Pflicht.** Jedes Prinzip verweist auf einen Markenwert, jede Regel auf ein Prinzip, einen Befund oder eine Entscheidung, jedes Signatur-Element auf Material der Marke (Logoform, Herkunft, Produkt, Sprache, Bestand). Eine Regel ohne Herleitung meldet der Prüfer, und sie fliegt raus.

**3 · Achsenprofil.** Acht Achsen, je fünf Stufen:

| Achse | Woran gemessen |
|---|---|
| hell ↔ dunkel | Standardmodus, Flächenanteile |
| kühl ↔ warm | Temperatur der Neutralfarben |
| zurückhaltend ↔ farbig | Zahl und Sättigung der Akzente |
| eckig ↔ rund | Radien |
| luftig ↔ dicht | Abstände, Elemente je Ansicht |
| leise ↔ laut | Verhältnis Display zu Fließtext, Gewichte |
| sachlich ↔ verspielt | Schriftcharakter, Ornament, Illustration |
| still ↔ lebendig | Zahl und Art der Bewegungen |

Das Soll-Profil entsteht im Markenkern (P4) und wird in Runde 1 bestätigt. Die Stilrichtungen in P5 müssen sich auf mindestens drei Achsen unterscheiden. In P7 misst ein Skript das Ist-Profil aus den Tokens. Weicht es um mehr als eine Stufe ab, ist das ein Befund.

**4 · Blindtest mit Ablenkern in jedem Lauf (F6 a).** Ein eigener Agent schreibt zwei erfundene, plausible Markenkerne aus derselben Branche. Der Prüfer bekommt den anonymisierten Guide (ohne Logo, Name und Wortlaut: Prinzipien, Farb- und Schrifttafel, Signaturen, Musterseite) und die drei Markenkerne in zufälliger Reihenfolge. Er muss die echte Marke finden und begründen. Liegt er falsch oder rät er, ist das System nicht eigen genug: Überarbeitung mit seinen Gründen.

**5 · Abgleich mit früheren Läufen und Wettbewerbern.** Liegen im Ablageort andere Guides, vergleicht der Prüfer Achsenprofil, Signaturen und Tokens. Zu nah beieinander ist ein Befund. Sind Wettbewerber angegeben, gilt dasselbe gegen deren gemessenes Profil.

**6 · Katalog-Bremse.** Paletten, Schriftpaare und Stile aus ui-ux-pro-max sind Kandidaten. Vorrang hat der Bestand der Marke. Jede Übernahme aus dem Katalog braucht eine Herleitung und steht als solche im Guide.

---

## 6 · Ergebnis

### 6.1 Der Guide

Pflicht-Kern (D1 b), Kapitel übernommen aus der Machart des AI-READY-Guides, die Inhalte entstehen je Marke:

| Nr. | Kapitel | Pflichtinhalt |
|---|---|---|
| 0 | Über diesen Guide | Quellen, Entstehung, vier Skills und begründete Abweichungen, Rangfolge bei Widersprüchen, Version und Freigabe |
| 1 | Markenkern | Werte, Persönlichkeit, Positionierung, Zielgruppe (eine Seite) |
| 2 | Gestaltungsprinzipien | 4–6 Prinzipien, je mit Wert |
| 3 | Logo | Aufbau, Dateien, Schutzraum, Mindestgröße, Hintergründe, Fehlanwendungen. Nur vorhandene Dateien, fehlende Originale als Befund |
| 4 | Farbe | Rollen, Tokens, Anteile je Ansicht, Regel für Verläufe, Kontrasttabelle (vom Skript erzeugt), Modi |
| 5 | Typografie | Schriften mit Lizenzstatus, Skala Web und Druck, Satzregeln, typografische Zeichen |
| 6 | Raster, Raum, Form | Container, Spalten, Breakpoints, Abstände, Radien, Tiefe, Linien |
| 7 | Signatur-Elemente | je Element Aufgabe, Grenze, Herleitung |
| 8 | Komponenten | Grundsätze, Bausteine (mit Stack: Tabelle der Bausteine im Code) |
| 9 | Ikonografie | Stil, Raster, Strich, Regeln |
| 10 | Bildwelt | Bildarten, Regeln, „Nie“-Liste |
| 11 | Bewegung | Ebenen, Dauern und Kurven als Tokens, reduzierte Bewegung |
| 12 | Text im Design | Anrede, Schreibweisen, Buttons, Zahlen (Kurzfassung, kein ToV-Ersatz) |
| 13 | Checkliste vor dem Livegang | Inhalt, Gestaltung, Zugänglichkeit, Leitplanken |
| 14 | Do und Don’t | aus Anti-Patterns und Entscheidungen |
| 15 | Pflege und Versionen | Änderungsverlauf, Freigabevermerk, vorläufige Punkte |

Module nach Kanälen aus dem Briefing: Web (hell und dunkel), Druck, Social, Präsentationen, Bewegtbild, Mail, digitale Formate (OG-Bilder), Verpackung und Merch. Anhang: Anwendungsbeispiele (D3 b), Token-Übersicht, Kolophon mit Absender AI READY.

Regeln stehen als Zahl und Grenze, nicht als Adjektiv („höchstens eine primäre Handlung je Ansicht“, „Akzentfarbe höchstens 5 % der Fläche“), jedes Signatur-Element mit Aufgabe und Grenze. Das ist die Machart unseres Guides, nicht sein Inhalt.

### 6.2 Tokens und Code

- **Tokens** als eine Quelle im W3C-Format (`tokens.json`): Farbrollen je Modus, Schriftskala Web und Druck, Abstände, Radien, Schatten, Bewegung. Ein Skript erzeugt daraus `tokens.css` (CSS-Variablen, hell und dunkel), `theme.css` (Tailwind v4 `@theme`) und `druck.css` (pt und mm).
- **Bausteine** (Stack Next.js, Tailwind v4, Sanity, abschaltbar): ein funktionaler Grundsatz (Button, Textlink, Karte, Sektionskopf, Kennzahl, Zitat, Badge, Eingabefelder, Logo), Optik ausschließlich aus Tokens, dazu 1–3 Bausteine für die Signatur-Elemente der Marke. Vor dem Einsatz in einem Kunden-Repo liest Claude Code die Doku der dort installierten Next-Version.
- **Leitplanken:** ESLint-Regeln gegen freie Farben, Größen und Radien (aus den Tokens erzeugt), Sanity-Validierungen (z. B. eine primäre Handlung je Block, Alt-Text Pflicht, Autoplay aus). Muster: unsere `eslint.leitplanken.mjs` und `sanity/schemaTypes/leitplanken.ts`.

### 6.3 Regeldatei für Coding-Agenten (C8)

`DESIGN.md`: kompakt, für Claude Code geschrieben, eingebunden über `CLAUDE.md` bzw. `AGENTS.md` im Website-Repo. Inhalt: Tokens und ihre Namen, Bausteine und wann welcher, Verbote, Mindeststandards, Checkliste, Verweis auf den Guide. Aufbau kompatibel zur `DESIGN.md` von Impeccable, damit dessen Kritik-Befehle im Kunden-Repo direkt darauf arbeiten können. Optional dazu `PRODUCT.md` aus dem Markenkern (Frage K4).

### 6.4 Anwendungsbeispiele

Musterseite Web (in beiden Modi, falls die Marke beide hat), Social-Kachel, Cover eines Druckstücks. Alle aus den Tokens und Bausteinen gebaut, als PNG im Guide. Sie sind zugleich Beweis, dass das System trägt, und Material für den Blindtest.

---

## 7 · Qualitätsprüfungen

**Skripte (gleiches Ergebnis bei jedem Lauf)**

| Prüfung | Was | Grenze |
|---|---|---|
| Kontrast | jede Text-/Grund-Kombination der Tokens, beide Modi, auch Buttons und Links | Text 4,5 : 1, große Schrift, Linien, Icons 3 : 1 |
| Tokens | gültiges Format, jede Farbe im Guide ist ein Token, keine Dubletten (fast gleiche Farben), keine Waisen, Schriftskala mit festen Stufen | 0 Befunde |
| Größen | Fließtext, Labels, Eingabefelder, Trefferflächen der Bausteine | 16 px / 12 px / 16 px / 44 px |
| Achsenprofil | Ist aus Tokens gegen Soll aus dem Markenkern | höchstens 1 Stufe Abweichung |
| Render | PDF und Kontaktbogen: abgeschnittene Texte, Überläufe, leere Seiten | 0 Befunde, Kontaktbogen wird gelesen |
| Code | Leitplanken laufen gegen die Bausteine (nur mit Stack) | 0 Fehler |

**Prüfer (getrennt vom Ersteller, eigener Agent; im claude.ai-Chat über ein Prüfpaket in einem neuen Chat, Abschnitt 9)**

Bekommt Guide, Tokens, Markenkern, Faktenblatt, die Prüfliste und die Originale der vier Skills, nicht den Gesprächsverlauf. Prüft: Herleitungskette, Anti-Patterns (Impeccable), technische Regeln (Vercel), Widerspruchsfreiheit des Guides in sich, Fakten nur mit Fundstelle, Logo unverändert, Blindtest (Abschnitt 5). Antwort PASS oder FAIL mit Kapitel, Problem, Vorschlag. Höchstens zwei Überarbeitungen, danach gehen die offenen Punkte an den User. Ein Befund zu einer Tatsache wird nie wegformuliert: belegen oder streichen.

---

## 8 · Dateistruktur

### 8.1 Der Skill

```
brand-styleguide/
├── SKILL.md                  Ablauf P0–P8, Entscheidungsformat, Verweise
├── references/
│   ├── ablauf.md             Phasen im Detail, Ein- und Ausgaben, Wiederaufnahme
│   ├── einlesen.md           Werkzeug-Erkennung, Tavily, Chrome, Ersatzwege, Faktenblatt
│   ├── entscheidungen.md     Format der Runden, „mach du“, Bildfragen für Laien
│   ├── markenkern.md         Interview, eine Seite, Soll-Achsenprofil
│   ├── kapitel.md            Pflicht-Kern und Module: Zweck, Pflichtinhalt, Machart je Kapitel
│   ├── herleitung.md         Werte → Prinzipien → Regeln, Signaturen aus Markenmaterial
│   ├── differenzierung.md    Achsenprofil, Blindtest mit Ablenkern, Abgleich, Katalog-Bremse
│   ├── tokens.md             Token-Schema, Ableitungen CSS, Tailwind, Druck
│   ├── stack-next-sanity.md  Bausteine, Leitplanken, DESIGN.md, Einbau im Repo
│   ├── pruefung.md           Prüfliste, Mindeststandards, Ablauf Prüfer
│   ├── profil-falkemedia.md  Hausprofil: wann laden, was gilt, nie bei externen Marken
│   └── regeln-*.md           deutsche Kurzfassungen der vier Design-Skills mit Quellen
├── vendor/
│   ├── frontend-design/      SKILL.md, LICENSE.txt
│   ├── web-interface-guidelines/  command.md, AGENTS.md, LICENSE
│   ├── impeccable/           SKILL.md, reference/, LICENSE, NOTICE.md (ohne Programm)
│   ├── ui-ux-pro-max/        SKILL.md, data/, scripts/, LICENSE
│   └── VERSIONEN.md          Quelle, Commit, Datum, Lizenz je Skill
├── assets/
│   ├── guide/                HTML/CSS-Gerüst für den Guide, nur Mechanik, Gestaltung aus Tokens
│   ├── richtungen/           Bildtafel für Stilrichtungen
│   ├── beispiele/            Musterseite, Social-Kachel, Cover
│   └── code/                 Bausteine, ESLint- und Sanity-Leitplanken (Vorlagen)
├── scripts/                  Python, nur Standardbibliothek: werkzeuge, messen, tokens,
│                             kontrast, pruefen, achsen, profil, render
└── evals/                    Fälle und Erwartungen im Format von skill-creator
```

### 8.2 Ein Lauf

```
<ablage>/<marke>/
├── lauf.json                 Marke, Werkzeuge, Entscheidungen, Stand
├── 00-briefing.md
├── arbeit/                   01-fakten, 01-messung, 02-auswertung, 03-markenkern,
│                             04-richtungen/, 05-pruefung, quellen/
├── guide/                    <MARKE>_Brand-Style-Guide_v1.0 (.md, .html, .pdf)
├── tokens/                   tokens.json, tokens.css, theme.css, druck.css
├── code/                     components/ui/…, eslint.leitplanken.mjs, sanity/leitplanken.ts
├── DESIGN.md                 (optional PRODUCT.md)
└── beispiele/                Musterseite, Social-Kachel, Cover (PNG)
```

### 8.3 Das Projekt

`~/Documents/Building/brand-styleguide-skill/`: `skill/brand-styleguide/` (der Skill), `docs/` (dieses Konzept, Entscheidungen), `evals/` (Arbeitsbereich der Testläufe, ohne Kundendaten im Repo, Frage K6). Second Brain: `30 Projekte/21 Aktiv/Brand-Styleguide-Skill.md`.

---

## 9 · Plattformen

Stand laut offizieller Doku (Oktober 2026, Quellen in `docs/plattformen.md`). Was die Doku offen lässt, klärt der Plattformtest.

| Fähigkeit | Claude Code | Cowork (Desktop) | claude.ai-Chat |
|---|---|---|---|
| Skill bereitstellen | Ordner oder Plugin | ZIP-Upload, org-weit durch einen Owner der Organisation | wie Cowork |
| Skripte ausführen | ja | ja (lokale VM) | ja (Python, JavaScript) |
| Fremde Website abrufen | ja | per Skript nur, wenn die Org den Netzzugang freigibt; Web-Fetch und Suche gehen auch ohne | per Skript wie Cowork; Websuche ja |
| Browser für Screenshots und Stile | ja (lokaler Chrome) | eingebauter Browser bzw. Claude in Chrome; Headless Chrome in der VM offen | nicht dokumentiert |
| PDF aus HTML | ja (Chrome) | offen | offen |
| Getrennter Prüfer als Subagent | ja | ja | **nein** |
| Ergebnisdateien | lokaler Ordner | verbundener Ordner | Download, höchstens 30 MB je Datei |

**Was daraus für den Bau folgt**

1. **Skripte in Python, nur Standardbibliothek.** Python läuft auf allen drei Oberflächen ohne Installation, ob Node in Chat und Cowork verfügbar ist, ist offen.
2. **Nur Standardfelder im Kopf der SKILL.md**, Beschreibung unter 200 Zeichen, Pfade relativ zum Skill-Ordner. Was nur Claude Code kennt (z. B. `context: fork`), ist Komfort, keine Voraussetzung.
3. **Messen und Rendern stufenweise:** Chrome über das DevTools-Protokoll (Claude Code, ohne Zusatzpakete), sonst der eingebaute Browser (Desktop), sonst hochgeladene Screenshots. Werte aus Bildern stehen im Faktenblatt als „geschätzt“. Ohne Renderer liefert der Skill die HTML-Fassung mit Druck-CSS, und der User speichert sie im Browser als PDF.
4. **Prüfer überall getrennt:** als Subagent in Claude Code und Cowork. Im claude.ai-Chat erzeugt der Skill ein Prüfpaket, das der User in einem neuen Chat prüfen lässt. So kennt der Prüfer den Verlauf nicht, auch beim Blindtest.
5. **Die Claude-API ist kein Ziel** (kein Netz, kein Browser, nur Python).
6. **Verteilung:** an die Owner über die Org-Bereitstellung in claude.ai, für Claude Code aus dem Repo. Die Oberflächen gleichen Skills nicht untereinander ab, deshalb hat jede Fassung eine Versionsnummer in der SKILL.md.

**Plattformtest** (Bauplan Schritt 7): Node und Chromium in der Chat-Sandbox und der Cowork-VM, HTML zu PDF dort, Größengrenze des Skill-ZIPs, Netzstufe und Cowork-Modus in der falkemedia-Org (Frage K7).

---

## 10 · Evals

| Fall | Input | Woran wir ein gutes Ergebnis erkennen |
|---|---|---|
| **E1 AI READY blind** | ai-ready.de, Markenidentität v4.3, ToV v4.2, Logos. Als „Vorgaben“ zusätzlich Altmaterial aus `alt/` (Paper mit altem Logo, Workbook-Entwurf mit Fira Sans, Caveat und Space Grotesk), damit es echte Widersprüche gibt. Der Guide v1.4 bleibt verborgen | findet die Farbrollen (Nachtgrund, Warmweiß, Gold als Bedeutung, ein Akzent für die Handlung), die Schriften, die Signaturen aus dem Bestand; legt das alte Logo und die Fremdschriften als Widersprüche vor; erkennt Gold als Schrift auf Weiß als Kontrastproblem und schlägt eine Lösung in der Marke vor. Abgleich gegen v1.4 mit einer Kriterienliste |
| **E2 Kunde** | nennst du separat | Guide, den du so freigeben würdest |
| **E3 Unterscheidbarkeit** | Ergebnisse E1 und E2, dazu Ablenker | Blindtest ordnet beide richtig zu, Achsenprofile unterscheiden sich auf mindestens drei Achsen |
| **E4 Vergleich ohne Skill** | gleicher Input, nur „Erstelle einen Brand & Style Guide“ | der Skill ist sichtbar besser (Herleitung, Prüfungen, Unterscheidbarkeit). Zeigt, wofür es den Skill braucht |

Feste Prüfungen in jedem Fall: alle Dateien da, Tokens gültig, Kontraste grün, keine Aussage ohne Fundstelle, PDF gerendert. Bewertung: du (H3 a), je Guide „würde ich so freigeben“ auf einer Skala von 1 bis 5 und die gefundenen Kernentscheidungen. Testläufe kommen als PDF und PNG zu dir. Läufe nacheinander, nie parallel (16 GB RAM).

---

## 11 · Zur Freigabe

**Downloads (G1, nur mit deinem Go)**

| Skill | Quelle | Was | Größe | Lizenz |
|---|---|---|---|---|
| frontend-design | github.com/anthropics/skills, `skills/frontend-design` | SKILL.md, LICENSE.txt | 20 KB | Apache 2.0 |
| Web Interface Guidelines | github.com/vercel-labs/web-interface-guidelines | command.md, AGENTS.md, LICENSE | 17 KB | MIT |
| Impeccable | github.com/pbakaus/impeccable, `.claude/skills/impeccable` | SKILL.md, `reference/` (45 Dateien), LICENSE, NOTICE.md; ohne Programm, Browser-Skripte und Schriftindex | ca. 470 KB | Apache 2.0 |
| ui-ux-pro-max | lokal `~/.claude/skills/ui-ux-pro-max` (Kopie), Lizenzdatei aus github.com/nextlevelbuilder/ui-ux-pro-max-skill | Kopie wie installiert + LICENSE | 1,8 MB | MIT |

Der Commit-Stand wird beim Download in `vendor/VERSIONEN.md` festgehalten. Impeccable und ui-ux-pro-max ändern sich fast täglich, wir aktualisieren nur bewusst.

**Offene Punkte**

- **K1 · AI-READY-Guide im Skill:** gar nicht, die Machart steht abstrakt in `kapitel.md`. **Entschieden (Max, 23.10.).**
- **K2 · Hausprofil „falkemedia“:** Schnappschuss im Skill mit Stand-Datum, nur die nötigen Felder aus `markenhaus.md` (Schreibweisen, Ansprache, Gendern, Owner, Verweise auf Marken-ToV), per Skript aus dem Vault erneuert; bei externen Marken nie geladen. **Entschieden.**
- **K3 · Impeccable nur als Regelwerk** ohne sein Programm (Abschnitt 4.1). **Entschieden.**
- **K4 · Zusätzlich `PRODUCT.md`** aus dem Markenkern, im Format von Impeccable. **Entschieden.**
- **K5 · Testkunde** (E2): nennt Max separat.
- **K6 · Kundendaten:** Läufe mit echten Kunden liegen nur lokal unter `evals/`, nicht im GitHub-Repo. **Entschieden.**
- **K7 · Netzzugang in der falkemedia-Org:** Ob Owner im Chat und in Cowork eine Website per Skript abrufen können, hängt an der Netzstufe, die ein Owner der Organisation einstellt (aus, nur Paketmanager, einzelne Domains, alle Domains). Standard ist „nur Paketmanager“. **Entschieden (26.10.): „Paketmanager und einzelne Domains“** mit den Domains der Gruppenmarken auf der Liste (aus dem Hausprofil), nicht „alle Domains“: Anthropic nennt das die riskanteste Stufe, weil eine manipulierte Seite Claude dazu bringen kann, Daten nach außen zu senden. Einstellen kann das nur ein Owner der Organisation unter claude.ai/admin-settings/capabilities. Nötig erst vor dem Plattformtest. Ohne Freigabe liest der Skill Texte über Web-Fetch und nimmt für die Gestaltung hochgeladene Screenshots. Claude Code (Max und Team) betrifft die Einstellung nicht.

**Bauplan nach Go**

1. Downloads nach `vendor/`, Stände festhalten.
2. Gerüst mit `skill-creator`: SKILL.md und `references/`.
3. Skripte: Tokens, Kontrast, Prüfung, Achsenprofil, Messen, Render.
4. Vorlagen: Guide-Gerüst, Bildtafel, Anwendungsbeispiele, Code.
5. E1 AI READY blind, Ergebnis als PDF an dich. Danach Überarbeitung.
6. E2 mit dem Kunden, E3 und E4.
7. Plattformtest in Cowork und im claude.ai-Chat (Abschnitt 9). Den Skill dort hochladen machst du, oder ich mit deinem Go.
8. GitHub-Repo erst nach deinem ausdrücklichen Go.
