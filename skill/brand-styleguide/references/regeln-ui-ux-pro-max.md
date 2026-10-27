# Regeln: ui-ux-pro-max (Kurzfassung)

| | |
|---|---|
| Quelle | lokale Installation `~/.claude/skills/ui-ux-pro-max` (Stand 10.04.2026), Original github.com/nextlevelbuilder/ui-ux-pro-max-skill |
| Stand | Inhalt aus der lokalen Installation; Lizenzdatei aus Commit `1f8857914da3c723d58dab1d609dd0d55a86bf51` vom 26.10.2026 |
| Lizenz | MIT, `vendor/ui-ux-pro-max/LICENSE` |
| Original | `vendor/ui-ux-pro-max/SKILL.original.md`, Kataloge in `data/`, Suche in `scripts/` |

Eigene deutsche Kurzfassung mit Fundstellen, keine Übersetzung. Im Zweifel gilt das Original.

**Klassen:** K1 Mindeststandard (gilt immer, Abweichung nur als ausdrückliche Entscheidung des Users), K2 Stil (die Marke gewinnt, Abweichung begründet in Kapitel 0), K3 Handwerk (Standard, Ausnahme mit Begründung). Zahlenwerte, die nicht der Barrierefreiheit dienen (Dauern, Zeilenlänge, Raster), führt diese Datei als K3. Beispielwerte für Gestaltung (Skalen, Gewichte, Containerbreiten) sind K2.

**Fundstellen:** **§1–§10** = Abschnitte der „Quick Reference“ in `SKILL.original.md`, mit dem Regelnamen in Backticks. **Kategorien** = Tabelle „Rule Categories by Priority“. **App-Regeln** = „Common Rules for Professional UI“ und die zweite „Pre-Delivery Checklist“; beide gelten laut Quelle für App-Oberflächen (iOS, Android, React Native, Flutter), nicht für Desktop-Web. **ux Nr.** = Zeile in `data/ux-guidelines.csv`.

## Wofür der Skill es nutzt

**P7 Prüfung:** Die Grenzwerte unten sind die Zahlen, gegen die Prüfskripte und Prüfer messen, soweit `tokens.md` und `pruefung.md` sie nicht schon festlegen.

**P5 Richtungen:** Die Kataloge (Paletten, Schriftpaare, Stile, Produkttypen, Landingpage-Muster) liefern Kandidaten neben dem Bestand der Marke, nie ein fertiges System. Jede Übernahme läuft durch die Katalog-Bremse. Die Google-Fonts-Liste hilft, eine freie Ersatzschrift für Entwürfe zu finden, wenn die Dateien der Hausschrift fehlen (Konzept C5); die Lizenz prüft der Skill trotzdem.

## Kataloge abfragen

Im Skill-Ordner (dem Ordner mit `SKILL.md`) ausführen. Nur lesend, Python 3 ohne Zusatzpakete. Geprüft am 26.10.2026 mit Python 3.14.

```bash
python3 -B vendor/ui-ux-pro-max/scripts/search.py "<englische Suchbegriffe>" --domain <domain> -n 5
```

- `-B` verhindert, dass Python einen `__pycache__`-Ordner in `vendor/` schreibt.
- `-n` ist die Zahl der Treffer (Standard 3), `--json` liefert maschinenlesbare Ausgabe.
- Die Suche (BM25 über Stichworte) arbeitet auf englischen Daten. Deutsche Begriffe treffen nur zufällig; Suchbegriffe deshalb englisch und mehrteilig wählen (Produkt, Branche, Ton, Dichte).

| Frage | Domain | Datei | Beispiel |
|---|---|---|---|
| Farbe: Paletten nach Produkttyp mit Rollen (Primary, Accent, Background, Muted, Border, Ring …) | `color` | `colors.csv` (161) | `"fintech trust"` |
| Schrift: Schriftpaare mit Stimmung und Eignung | `typography` | `typography.csv` (73) | `"editorial serif"` |
| Schrift: einzelne Google Fonts (Kategorie, Achsen, Schnitte, Popularität) | `google-fonts` | `google-fonts.csv` (1.923) | `"humanist sans variable"` |
| Stil: Stilrichtungen mit Effekten, Eignung, Barrierefreiheit | `style` | `styles.csv` (84) | `"swiss minimalism"` |
| Produkttyp: empfohlene Stile und Farbfokus | `product` | `products.csv` (161) | `"b2b consulting"` |
| Aufbau von Landingpages, Platz der Handlung | `landing` | `landing.csv` (34) | `"hero social-proof"` |
| UX-Regeln mit Schweregrad | `ux` | `ux-guidelines.csv` (99) | `"touch target contrast"` |
| Icons, Diagramme | `icons`, `chart` | `icons.csv`, `charts.csv` | `"trend comparison"` |
| App-Oberflächen, React-Performance | `web`, `react` | `app-interface.csv`, `react-performance.csv` | für Websites selten nötig |

Stack-Regeln gibt es über `--stack` statt `--domain`, etwa `--stack nextjs`, `--stack html-tailwind` oder `--stack shadcn`. Das gehört nicht zur Rolle im Konzept, ist aber zum Nachschlagen in P6 lesend möglich.

**Nicht verwenden:**
- `--persist` schreibt einen Ordner `design-system/` ins aktuelle Verzeichnis.
- `--design-system` bündelt Muster, Stil, Palette, Schriftpaar, Effekte und Anti-Patterns zu einem fertigen System, samt Google-Fonts-Import. Höchstens als Kandidatenliste lesen, nie als Ganzes übernehmen.
- `--domain prompt` steht im Original, das Skript kennt die Domain nicht und bricht ab.
- Die Pfade `skills/ui-ux-pro-max/…` und der Hinweis auf React Native als einzigen Stack im Original passen nicht zu diesem Skill.
- `data/design.csv` (chinesische Stilbeschreibungen) und `data/draft.csv` (Entwurf) liest das Skript nicht.

## Katalog-Bremse

- Vorrang hat der Bestand der Marke laut Faktenblatt. Katalogeinträge sind Kandidaten (Konzept Abschnitt 5, Punkt 6).
- Jede Übernahme braucht eine Herleitung aus Markenwert, Befund oder Entscheidung und steht als Übernahme im Guide, mit Katalog und Eintrag.
- Die Kataloge ordnen nach Produkttyp und Branche (`color-palette-from-product`, §4). Genau diese Zuordnung lehnen frontend-design und Impeccable als Begründung ab. Branche allein ist deshalb keine Herleitung.
- 32 der 73 Schriftpaare enthalten mindestens eine Schrift aus Impeccables Liste der Trainings-Standards (am häufigsten Inter, Space Grotesk, Plus Jakarta Sans). Solche Kandidaten brauchen den Grund, den `regeln-impeccable.md` verlangt.
- Katalogwerte sind ungeprüft. Jedes übernommene Farbpaar läuft durch `kontrast.py`.

## Grenzwerte

### Kontrast

| Grenzwert | Klasse | Fundstelle |
|---|---|---|
| Normaler Text mindestens 4,5 : 1, große Schrift mindestens 3 : 1 | K1 | §1 `color-contrast`; ux Nr. 36 |
| Paare aus Vorder- und Hintergrund 4,5 : 1 (AA). 7 : 1 (AAA) ist eine höhere Stufe, kein Mindeststandard | K1 | §6 `color-accessible-pairs` |
| Fehler- und Erfolgsfarben mindestens 4,5 : 1 | K1 | §8 `contrast-feedback` |
| Icons: kleine Elemente 4,5 : 1, größere Glyphen mindestens 3 : 1 | K1 | App-Regeln, Icons |
| Diagramme: Linien und Balken mindestens 3 : 1 zum Grund, Datenbeschriftungen mindestens 4,5 : 1 | K1 | §10 `contrast-data` |
| Nebentext im Dunkelmodus mindestens 3 : 1 | K1, aber `tokens.md` verlangt für `text-leise` 4,5 : 1; die strengere Grenze gilt | App-Regeln, Light/Dark |
| Fokusring sichtbar, 2–4 px | K1 | §1 `focus-states` |
| Farbe nie allein als Information, immer mit Icon oder Text | K1 | §1 `color-not-only`; ux Nr. 37 |

### Größen

| Grenzwert | Klasse | Fundstelle |
|---|---|---|
| Fließtext mindestens 16 px (mobil, verhindert den Auto-Zoom in iOS) | K1 | §5 `readable-font-size`; ux Nr. 67 |
| Kein Fließtext unter 12 px | K1 | Kategorien, Priorität 6 |
| Zeilenhöhe im Fließtext 1,5–1,75 | K3 | §6 `line-height`; ux Nr. 72 |
| Gewichte: Überschriften 600–700, Fließtext 400, Labels 500 | K2 | §6 `weight-hierarchy` |
| Feste Schriftskala, Beispiel 12 / 14 / 16 / 18 / 24 / 32 | K3 für „feste Skala“, K2 für die Werte | §6 `font-scale` |
| Deaktivierte Elemente mit Deckkraft 0,38–0,5, Cursor und semantischem Attribut | K3 | §8 `disabled-states` |
| Icon-Größen als Tokens (Beispiel `icon-md` = 24 pt), gleicher Strich je Ebene (Beispiel 1,5 oder 2 px) | K3 | App-Regeln, Icons |

### Trefferflächen

| Grenzwert | Klasse | Fundstelle |
|---|---|---|
| Mindestens 44 × 44 px (Apple, pt) bzw. 48 × 48 dp (Material). Die Trefferfläche über das Sichtbare hinaus erweitern | K1 | §2 `touch-target-size`; ux Nr. 22 |
| Mindestens 8 px Abstand zwischen Trefferflächen | K1 | §2 `touch-spacing`; ux Nr. 23 |
| Eingabefelder mobil mindestens 44 px hoch | K1 | §8 `touch-friendly-input` |
| Interaktive Diagrammelemente mindestens 44 pt Trefferfläche | K1 | §10 `touch-target-chart` |

### Dauern und Bewegung

| Grenzwert | Klasse | Fundstelle |
|---|---|---|
| Mikro-Interaktionen 150–300 ms, komplexe Übergänge höchstens 400 ms, nichts über 500 ms | K3 | §7 `duration-timing`; ux Nr. 8 |
| Ausgang etwa 60–70 % der Eingangsdauer | K3 | §7 `exit-faster-than-enter` |
| Staffelung 30–50 ms je Element | K3 | §7 `stagger-sequence` |
| Höchstens 1–2 animierte Schlüsselelemente je Ansicht | K2 | §7 `excessive-motion`; ux Nr. 7 |
| Ladeanzeige ab 300 ms, Skeleton statt Spinner ab 1 s | K3 | §7 `loading-states`; §3 `progressive-loading`; ux Nr. 78 |
| Rückmeldung auf Tippen binnen 100 ms (App-Regeln: 80–150 ms), Eingabelatenz unter 100 ms | K3 | §3 `tap-feedback-speed`, `input-latency`; App-Regeln, Interaction |
| Toasts schließen nach 3–5 s | K3 | §8 `toast-dismiss`; ux Nr. 82 |
| Ausblendungen nicht unter Deckkraft 0,2 stehen lassen | K3 | §7 `opacity-threshold` |
| Skalierung beim Drücken 0,95–1,05 | K2 | §7 `scale-feedback` |
| Reduzierte Bewegung beachten | K1 | §1 `reduced-motion`; ux Nr. 9, 99 |
| Nur `transform` und `opacity` animieren, nicht Breite, Höhe, Position | K3 | §7 `transform-performance`; ux Nr. 13 |

### Zeilenlänge

| Grenzwert | Klasse | Fundstelle |
|---|---|---|
| 65–75 Zeichen je Zeile, Textcontainer entsprechend begrenzen | K3 | §6 `line-length`; ux Nr. 21, 73 |
| Mobil 35–60, Desktop 60–75 Zeichen | K3 | §5 `line-length-control` |

### Abstände, Raster, Layout

| Grenzwert | Klasse | Fundstelle |
|---|---|---|
| Abstände in 4er- oder 8er-Schritten | K3 für „eine Skala“, K2 für das Raster | §5 `spacing-scale` |
| Abschnittsabstände in Stufen, Beispiel 16 / 24 / 32 / 48 | K2 | App-Regeln, Layout & Spacing |
| Breakpoints systematisch, Beispiel 375 / 768 / 1024 / 1440. Testen bei 320 / 375 / 414 / 768 / 1024 / 1440 | K3 | §5 `breakpoint-consistency`; ux Nr. 65 |
| z-Index als Skala, Beispiel 0 / 10 / 20 / 40 / 100 / 1000 (ux Nr. 15: 10 / 20 / 30 / 50) | K3 | §5 `z-index-management`; ux Nr. 15 |
| Einheitliche Containerbreite am Desktop, Beispiel `max-w-6xl` oder `max-w-7xl` | K2 | §5 `container-width` |
| Abdunklung hinter Modals 40–60 % Schwarz | K3 | App-Regeln, Light/Dark |
| Layoutverschiebung CLS unter 0,1 | K3 | Kategorien, Priorität 3 |
| Navigation unten höchstens 5 Einträge, Breadcrumbs ab 3 Ebenen | K3 | §9 `bottom-nav-limit`, `breadcrumb-web`; ux Nr. 6 |
| Kreis- und Ringdiagramme höchstens 5 Kategorien | K3 | §10 `no-pie-overuse` |

## Weitere Regeln ohne Zahl

| Regel | Klasse | Fundstelle |
|---|---|---|
| Ein primärer Call-to-Action je Ansicht, weitere Handlungen sichtbar untergeordnet | K2 | §4 `primary-action` |
| SVG-Icons aus einer Familie mit einheitlichem Strich, keine Emoji als Icons | K3 | §4 `no-emoji-icons`, `icon-style-consistent` |
| Offizielle Logodateien nach ihren Vorgaben (Proportionen, Schutzraum), nie umfärben oder verzerren. Deckt sich mit dem Konzept: Logo nie neu zeichnen | K3 | App-Regeln, Icons & Visual Elements |
| Semantische Farbtokens statt Hexwerten in Komponenten | K3 | §6 `color-semantic` |
| Hell und dunkel gemeinsam gestalten, dunkel mit entsättigten, helleren Tönen statt Invertierung, Kontrast je Modus prüfen | K3 | §4 `dark-mode-pairing`; §6 `color-dark-mode` |
| Eine Schattenskala für Karten, Sheets und Modals, keine Zufallswerte | K3 | §4 `elevation-consistent` |
| Blur nur, um Hintergrund abzusetzen (Modal, Sheet), nicht als Dekoration | K2 | §4 `blur-purpose` |
| Federkurven bevorzugen statt linear oder cubic-bezier | K2 | §7 `spring-physics` |
| Sichtbare Labels statt Platzhalter, Fehler unter dem Feld, Fokus auf das erste fehlerhafte Feld | K1 | §8 `input-labels`, `error-placement`, `focus-management` |

### Nicht geregelt

Druckwerte (pt, mm, Satzspiegel), Mindestgröße und Schutzraum des Logos als Zahl, Bildwelt, Anteile von Farben je Ansicht, Lesebreite im Druck, Kontrast von Linien ohne Steuerfunktion.

## Typische Konflikte mit Marken

| Fall | Regel | Behandlung |
|---|---|---|
| Katalogpalette passt „zur Branche“, Bestand sieht anders aus | §4 `color-palette-from-product` | K2 plus Katalog-Bremse: Der Bestand gewinnt, Branche ist keine Herleitung |
| Katalog-Schriftpaar mit Trainings-Standard oder Monospace-Labels in Versalien (z. B. das Paar „Minimalist Monochrome Editorial“) | `typography.csv`, gegen frontend-design und Impeccable | K2. Nur mit Herleitung aus der Marke, sonst nicht übernehmen |
| Nebentext im Dunkelmodus unter 4,5 : 1 | App-Regeln erlauben 3 : 1 | K1, die strengere Grenze aus `tokens.md` gilt |
| Trefferflächen 44 px, 48 dp, 24 px (Vercel) | §2 | K1. Der Skill setzt 44 px für alle Bausteine (Konzept Abschnitt 7) |
| Zeilenhöhe der Marke außerhalb von 1,5–1,75 | §6 `line-height` | K3. Ausnahme mit Begründung. Impeccable lehnt ein Einheitsverhältnis ab und stimmt auf Schrift und Breite ab |
| langsame, ruhige Markenbewegung über 500 ms | §7 `duration-timing` | K3. Ein benannter Sonder-Token mit Begründung (`tokens.md` Abschnitt 6). Impeccable erlaubt 500–800 ms für einen gestalteten Auftritt |
| gestaffelte Einblendungen bei jeder Sektion | §7 `stagger-sequence` gegen frontend-design und Impeccable | K2. Staffelung nur für echte Listen, sonst Begründung im Guide |
| federnde Kurven | §7 `spring-physics` gegen Impeccable (kein Federn aus Reflex) | K2. Die Formensprache der Marke entscheidet, Herleitung im Kapitel Bewegung |
| Raster der Marke weder 4 noch 8 px | §5 `spacing-scale` | K2. Das Raster kommt aus dem Bestand, eine Skala braucht es trotzdem (K3) |
| mehrere gleichrangige Calls-to-Action im Bestand | §4 `primary-action` | K2. Als Vorschlag in Runde 1, die Regel steht im Guide als Zahl |
