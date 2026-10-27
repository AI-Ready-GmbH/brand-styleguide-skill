---
name: "{{Marke}}"
description: "{{ein Satz aus dem Markenkern, ohne Werbesprache}}"
colors:
  grund: "{{farbe.rolle.grund}}"
  flaeche: "{{farbe.rolle.flaeche}}"
  text: "{{farbe.rolle.text}}"
  text-leise: "{{farbe.rolle.text-leise}}"
  linie: "{{farbe.rolle.linie}}"
  linie-stark: "{{farbe.rolle.linie-stark}}"
  akzent: "{{farbe.rolle.akzent}}"
  akzent-text: "{{farbe.rolle.akzent-text}}"
  handlung: "{{farbe.rolle.handlung}}"
  handlung-hover: "{{farbe.rolle.handlung-hover}}"
  handlung-text: "{{farbe.rolle.handlung-text}}"
  fokus: "{{farbe.rolle.fokus}}"
  fehler: "{{farbe.rolle.fehler}}"
typography:
  display:
    fontFamily: "{{Familie, Ersatz}}"
    fontSize: "{{Größe oder clamp(…)}}"
    fontWeight: {{Gewicht}}
    lineHeight: {{Zeilenhöhe}}
    letterSpacing: "{{Laufweite}}"
  # ebenso: titel-1, titel-2, titel-3, lead, fliesstext, klein, label
rounded:
  steuerung: "{{radius.steuerung}}"
  karte: "{{radius.karte}}"
  pille: "{{radius.pille}}"
spacing:
  "{{n}}": "{{abstand.n}}"
components:
  button-primaer:
    backgroundColor: "{colors.handlung}"
    textColor: "{colors.handlung-text}"
    typography: "{typography.{{stufe}}}"
    rounded: "{rounded.steuerung}"
    padding: "{{Innenabstand}}"
  button-primaer-hover:
    backgroundColor: "{colors.handlung-hover}"
  button-sekundaer:
    textColor: "{colors.text}"
    rounded: "{rounded.steuerung}"
    padding: "{{Innenabstand}}"
  karte:
    backgroundColor: "{colors.flaeche}"
    rounded: "{rounded.karte}"
    padding: "{{Innenabstand}}"
  feld:
    backgroundColor: "{colors.flaeche}"
    textColor: "{colors.text}"
    typography: "{typography.fliesstext}"
    rounded: "{rounded.steuerung}"
---
<!-- Vorlage des Skills brand-styleguide. Der Lauf füllt {{…}} aus tokens/tokens.json (Werte des Standardmodus),
     guide.md und lauf.json, streicht Zeilen ohne Inhalt und löscht diesen Kommentar. Kopf: nur Gruppen und Namen wie
     oben (deutsche Token-Namen sind die echten Namen im Code), optionale Rollen nur, wenn es sie gibt.
     Die acht Hauptabschnitte mit genau diesen englischen Überschriften und in dieser Reihenfolge (Impeccable);
     Inhalte in der Sprache der Marke, beschreibend, der Wert in Klammern, keine Klassennamen. Unsere Zusätze stehen
     danach, als Ergänzung markiert. Ziel: Textteil ohne Kopf unter 150 Zeilen. -->

# Design System: {{Marke}}

Regeldatei für Coding-Agenten. Lies sie ganz, bevor du Oberfläche baust oder änderst. Die Ergänzungen nach den acht Hauptabschnitten (Tokens im Code, Bausteine, Mindeststandards, Checkliste) gelten genauso. Werte: `{{pfad}}/tokens.json`, Guide {{Version}}, freigegeben {{Datum}} von {{Name}}.

## Overview

**Creative North Star: "{{Leitbild in zwei bis vier Wörtern}}"**

{{Zwei bis drei Sätze: Haltung des Systems aus den Gestaltungsprinzipien, Dichte, Modus (hell, dunkel, beide). Nur bestätigte Ablehnungen.}}

**Key Characteristics:**
- {{Prinzip}} ({{Wert aus dem Markenkern}})
- {{4–6 Prinzipien aus Guide 2}}

## Colors

{{Ein Satz zum Charakter der Palette.}} Werte im Kopf gelten für den Modus {{standardmodus}}; {{Modus dunkel: Werte in der Ergänzung „Tokens im Code“}}.

### Primary
- **{{beschreibender Name}}** (handlung, {{Wert}}): nur die primäre Handlung, Hover {{Wert}}, Schrift darauf {{Wert}}.
- **{{beschreibender Name}}** (akzent, {{Wert}}): {{Flächen, Linien, Icons}}; als Schrift die Fassung akzent-text ({{Wert}}).

### Neutral
- **{{Name}}** (grund, {{Wert}}) · **{{Name}}** (flaeche, {{Wert}}): {{Seite, Karten, Felder}}.
- **{{Name}}** (text, {{Wert}}) · **{{Name}}** (text-leise, {{Wert}}): Fließtext und Titel, Nebentext.
- **{{Name}}** (linie, {{Wert}}) · **{{Name}}** (linie-stark, {{Wert}}): Trennlinien, Ränder von Steuerelementen.
- **{{Name}}** (fokus, {{Wert}}) · **{{Name}}** (fehler, {{Wert}}): Fokusring, Fehlermeldungen.

**Die {{Name}}-Regel.** {{Anteil oder Grenze aus Guide 4, z. B. Akzent höchstens x % der Fläche je Ansicht.}}

## Typography

**Display Font:** {{Familie}} (mit {{Ersatz}}) · **Body Font:** {{Familie}} (mit {{Ersatz}}) · Lizenz: {{Status}}, nur die gelieferten Schnitte.

**Character:** {{ein Satz zur Paarung}}

### Hierarchy
- **display** ({{Gewicht}}, {{Größe}}, {{Zeilenhöhe}}): {{höchstens einmal je Seite}}
- **titel-1 · titel-2 · titel-3** ({{…}}): Überschriften; Ebene (h1–h3) und Stufe sind getrennt wählbar.
- **lead** ({{…}}): ein Satz unter dem Sektionstitel.
- **fliesstext** ({{…, mindestens 16 px}}): Fließtext und Eingabefelder, Zeilenlänge {{lesebreite}}.
- **klein · label** ({{…, label mindestens 12 px}}): Nebentexte · Badges und Beschriftungen{{, Versalien}}.

**Die {{Name}}-Regel.** {{Satzregel aus Guide 5: Hervorhebung, Versalien, typografische Zeichen der Sprache.}}

## Layout

{{Container, Rand, Spalten, Breakpoints, Lesebreite in Worten mit Wert.}} Abstände nur in Schritten des Grundrasters ({{Wert}}), Reihe {{Schritte}}; {{Sektionsabstand mobil und Desktop}}. Mobil zuerst.

## Elevation & Depth

{{Flach mit Linien, oder: Schatten schwebend ({{Wert}}) nur für …}}. Keine weiteren Schatten.

## Shapes

{{Formensprache aus dem Logo, ein Satz.}} Steuerelemente {{beschrieben}} ({{radius.steuerung}}), Karten ({{radius.karte}}), Badges als Pille. Innen kleiner als außen.

## Components

- **Buttons:** {{Charakter}}. Primär auf handlung, höchstens einer je Ansicht; sekundär mit Rand in linie-stark. Hover {{…}}, Fokusring in fokus, beim Absenden Ladetext mit „…“.
- **Links:** unterstrichen, Farbe akzent-text, Hover {{…}}.
- **Karten:** {{Varianten und wann welche}}. Verlinkte Karte ist genau ein Link, keine Karte in einer Karte.
- **Felder:** Label sichtbar darüber, Rand in linie-stark, Fehler darunter in fehler, Fokusring in fokus.
- **Kennzahlen · Zitate · Badges:** {{je ein Satz: Stufe, Farbe, Grenze}}.
- **{{Signatur-Element}}:** {{Aufgabe}}. Grenze: {{…}}.
<!-- Eyebrow oder Kicker über Überschriften: Impeccable bannt sie, bei uns Stilregel (Klasse K2). Nur eintragen,
     wenn die Marke sie nutzt und Guide 0 das begründet, dann mit Begründung. Sonst weglassen. -->

## Do's and Don'ts

### Do:
- **Do** {{Regeln aus Befunden und Entscheidungen dieser Marke, mit Zahl und Grenze}}

### Don't:
- **Don't** {{Verbote aus Guide 14 und den Anti-Patterns, die diese Marke betreffen; kein Verbot gegen ein Mittel, das die Marke selbst nutzt}}
- **Don't** zeichne, färbe oder verzerre das Logo.
- **Don't** setze eine zweite primäre Handlung in dieselbe Ansicht.

---

## Tokens im Code (Ergänzung brand-styleguide)

Quelle `tokens.json`, im Repo `app/tokens.css` (Variablen `--m-…`) und `app/theme.css` (Tailwind). Nur diese Klassen:

| Gruppe | Klassen |
|---|---|
| Farbe | `bg-`, `text-`, `border-`, `outline-` + Rolle: `grund`, `flaeche`, `text`, `text-leise`, `linie`, `linie-stark`, `akzent`, `akzent-text`, `handlung`, `handlung-hover`, `handlung-text`, `fokus`, `fehler`{{, optionale}}; Deckkraft `bg-<rolle>/x` |
| Schrift | `font-titel`, `font-text`{{, font-akzent, font-mono}}; `text-display`, `text-titel-1` … `text-titel-3`, `text-lead`, `text-fliesstext`, `text-klein`, `text-label` (`text-text` ist die Farbe) |
| Form | `rounded-steuerung`, `rounded-karte`, `rounded-pille`{{, shadow-…}} |
| Abstand | `p-n`, `gap-n` usw. in Rasterschritten |
| Bewegung | `duration-(--m-dauer-kurz)`, `…-mittel`, `…-lang`, `ease-standard`, immer mit `motion-reduce:transition-none` |
| Modus | {{`data-modus="dunkel"` am html; Variante `dunkel:` nur für Dateien wie das Logo}} |

Verboten (ESLint meldet es): Hex-, rgb-, hsl-Werte, Tailwind-Standardfarben, -größen, -radien und -schatten, Klammerwerte für Größe, Radius, Farbe oder Dauer, Schrift, Farbe, Radius und Bewegung im `style`-Attribut, `transition: all`. Fehlt ein Wert, ist das eine Frage an die Marke, kein neuer Wert im Code.

## Bausteine (Ergänzung brand-styleguide)

Import aus `@/components/ui`. Mit `href` werden Button, Textlink und Karte zum Link.

| Baustein | Wann | Regel |
|---|---|---|
| `Button` | Handlung; `primaer` höchstens einmal je Ansicht, sonst `sekundaer` | Verb + Objekt, `laedt` beim Absenden |
| `TextLink` | Verweis; `art="eigenstaendig"` außerhalb von Fließtext | Linktext nennt das Ziel |
| `Card` | {{Varianten}} | mit `href` braucht sie `titel`, sonst nichts Klickbares darin |
| `SectionHead` | Kopf jeder Sektion | eine h1 je Seite, keine Ebene überspringen |
| `Kennzahl` | belegte Zahl mit Bedeutung | `label` Pflicht |
| `Zitat` | echtes, freigegebenes Zitat | nie erfunden oder umformuliert |
| `Badge` | Status, Art | kein Bedienelement |
| `Input`, `Textarea`, `Select` | Formulare | `label`, `name`, bei Input `autoComplete`; Fehler über `fehler` |
| `Logo` | Kopf, Fuß | Originaldatei, `alt` = Name der Marke |
| `{{Signatur}}` | {{Aufgabe}} | {{Grenze}} |

Was kein Token abbildet (Versalien, Pfeil, Lader, Unterstreichung, Anker-Abstand), steht in `app/marke.css` unter `[data-baustein="…"]`, nie in einer Seite.

## Mindeststandards (Ergänzung brand-styleguide)

Gelten immer, auch gegen eine Gestaltung. Ausnahme nur als Entscheidung im Guide.
- **Kontrast:** Text 4,5 : 1; große Schrift, Ränder von Steuerelementen, Icons, Fokus 3 : 1.
- **Größen:** Fließtext und Felder mindestens 16 px, Labels mindestens 12 px, Zoom nie sperren.
- **Trefferflächen:** mindestens 44 × 44 px für alles Bedienbare außerhalb von Fließtext.
- **Fokus und Tastatur:** Fokus sichtbar (`:focus-visible`), nie `outline-none` ohne Ersatz; `button` für Handlungen, `a`/`Link` für Ziele, kein `div` mit Klick.
- **Bewegung:** nur transform und opacity, Dauern aus Tokens, bei reduzierter Bewegung still; Autoplay über 5 s nur mit Pause.
- **Inhalt:** Bilder mit `alt` und Maßen, Überschriften ohne Sprung, Zahlen und Daten über `Intl`, typografische Anführungszeichen und „…“.

## Checkliste vor dem Commit (Ergänzung brand-styleguide)

- [ ] `npx eslint .` (mit Leitplanken) und `npx tsc --noEmit` ohne Fehler
- [ ] nur Bausteine und Token-Klassen, keine neuen Werte
- [ ] eine primäre Handlung je Ansicht
- [ ] bei 375 und 1440 px angesehen{{, hell und dunkel}}
- [ ] einmal mit der Tastatur durch, Fokus überall sichtbar; reduzierte Bewegung geprüft
- [ ] Texte: {{Anrede}}, Schreibweisen der Marke ({{Beispiele}}), Buttons Verb + Objekt

## Quellen und Einbindung (Ergänzung brand-styleguide)

- Guide: `{{pfad}}/{{MARKE}}_Brand-Style-Guide_v{{Version}}.pdf` (Kapitel 4 Farbe, 5 Typografie, 8 Komponenten, 11 Bewegung)
- Produkt: `PRODUCT.md`
- Eingebunden in `CLAUDE.md` mit der Zeile `@DESIGN.md`, in `AGENTS.md` mit dem Satz „Vor jeder Arbeit an der Oberfläche DESIGN.md lesen.“
