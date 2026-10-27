# Tokens: eine Quelle für Guide, Web, Druck und Code

Alle Werte des Systems stehen genau einmal in `tokens/tokens.json` des Laufs. Guide, Bausteine, Leitplanken und Druck lesen von dort. Wer eine Farbe, Größe oder Dauer braucht, die nicht in den Tokens steht, nimmt einen bestehenden Token (bei Farben mit anderer Deckkraft über `color-mix`) oder legt die Frage in der nächsten Runde vor. So bleibt das System prüfbar: Ein Skript kann Kontraste, Dubletten und Mindestgrößen nur prüfen, wenn es keine Werte außerhalb der Tokens gibt.

**Die Namen sind Struktur, keine Gestaltung.** Jede Marke hat eine Rolle `farbe.rolle.handlung`, aber welche Farbe das ist, ob es sie als Fläche oder als Linie gibt und wie sie wirkt, entscheidet die Marke. Es gibt im Skill keinen Standardwert für irgendeinen Token.

## Inhalt
1. Format
2. Pflichtgruppen und Namen
3. Modi (hell, dunkel, Druck)
4. Was das Skript daraus erzeugt
5. Kontrastpaare
6. Regeln für Skalen

## 1 · Format

Angelehnt an das Format der W3C Design Tokens Community Group: jeder Token ist ein Objekt mit `$value`, `$type` und optional `$description` und `$extensions`. Verweise auf andere Tokens stehen in geschweiften Klammern: `"{farbe.basis.tinte}"`.

```json
{
  "$marke": { "name": "…", "version": "1.0", "modi": ["hell"], "standardmodus": "hell", "folgt_system": false },
  "farbe": {
    "basis": {
      "<name>": { "$type": "color", "$value": "#RRGGBB", "$description": "Rolle in Worten, Herkunft (Fundstelle oder Entscheidung)" }
    },
    "rolle": {
      "grund": { "$type": "color", "$value": "{farbe.basis.<name>}", "$extensions": { "modi": { "dunkel": "{farbe.basis.<name>}" } } }
    }
  }
}
```

- `$marke.modi`: welche Modi die Marke hat (`hell`, `dunkel`, beide). `standardmodus` ist der Modus ohne Umschalter. `folgt_system: true` heißt: Ohne Wahl des Users folgt die Seite der Systemeinstellung.
- **Basis** sind die Markenfarben als Rohwerte, frei benannt in der Sprache der Marke. **Rollen** verweisen auf Basisfarben. Komponenten und Guide nutzen nur Rollen.
- Farben als `#RRGGBB`. Deckkraft nur über `color-mix(in srgb, <farbe> x%, transparent)` als Wert einer Rolle, nie als `rgba()`.
- `$description` jeder Basisfarbe nennt die Herkunft: Fundstelle aus dem Faktenblatt (`F12`) oder Entscheidung (`W3`). Eine Farbe ohne Herkunft meldet die Prüfung.

## 2 · Pflichtgruppen und Namen

| Gruppe | Pflicht-Tokens | Optional |
|---|---|---|
| `farbe.rolle` | `grund`, `flaeche`, `text`, `text-leise`, `linie`, `linie-stark`, `akzent`, `akzent-text`, `handlung`, `handlung-hover`, `handlung-text`, `fokus`, `fehler` | `flaeche-2`, `flaeche-akzent`, `erfolg`, `hinweis`, `auf-bild-text` |
| `schrift.familie` | `titel`, `text` | `akzent`, `mono` |
| `schrift.web` | `display`, `titel-1`, `titel-2`, `titel-3`, `lead`, `fliesstext`, `klein`, `label` | weniger Stufen erlaubt, wenn die Marke sie nicht braucht (dann im Guide begründen) |
| `schrift.druck` | wie Web, Werte in `pt` | nur, wenn Modul Druck gewählt |
| `abstand` | eine Reihe auf einem Grundraster, z. B. `1`…`12` | – |
| `radius` | `steuerung` (Buttons, Felder), `karte`, `pille` | `gross` |
| `schatten` | – | `schwebend`, weitere nur mit Begründung |
| `bewegung.dauer` | `kurz`, `mittel`, `lang` | `weg`, ein Sonderwert für den einen orchestrierten Moment |
| `bewegung.kurve` | `standard` | `weg` |
| `layout` | `container`, `rand`, `lesebreite`, `breakpoints` | `spalten` |
| `druck` | – | `rand`, `raster`, `format` (nur Modul Druck) |

**Was die Rollen bedeuten**

| Rolle | Bedeutung |
|---|---|
| `grund` | Grundfläche der Seite |
| `flaeche` | Karten, Panels, Felder auf dem Grund |
| `text` | Fließtext und Titel |
| `text-leise` | Nebentext, muss trotzdem 4,5 : 1 erreichen |
| `linie` | dezente Trennlinien (Dekoration, kein Kontrastzwang) |
| `linie-stark` | Ränder von Steuerelementen (Felder, Zweitbutton), mindestens 3 : 1 |
| `akzent` | die Markenfarbe für Flächen, Linien, Icons |
| `akzent-text` | die Markenfarbe als Schrift (oft dunkler oder heller als `akzent`, damit 4,5 : 1 erreicht wird) |
| `handlung` | Fläche der primären Handlung (Primärbutton) |
| `handlung-hover` | dieselbe im Hover |
| `handlung-text` | Schrift auf `handlung` |
| `fokus` | Fokusring, mindestens 3 : 1 gegen `grund` |
| `fehler` | Fehlermeldungen als Schrift |

`akzent` und `handlung` dürfen dieselbe Farbe sein. Ob sie es sind, ist eine Gestaltungsentscheidung der Marke, keine Vorgabe.

**Schriftstufen** sind Tokens vom Typ `typography`:

```json
"titel-1": { "$type": "typography", "$value": {
  "fontFamily": "{schrift.familie.titel}", "fontSize": "clamp(2rem, 4vw, 3.25rem)",
  "fontWeight": 700, "lineHeight": 1.1, "letterSpacing": "-0.02em" },
  "$extensions": { "versalien": false } }
```

`fontSize` als `px`, `rem` oder `clamp(min, …, max)`. Das Prüfskript liest bei `clamp` den kleinsten Wert (1 rem = 16 px).

**Schriftfamilien** tragen ihre Lizenz:

```json
"titel": { "$type": "fontFamily", "$value": ["Name", "Ersatz", "sans-serif"],
  "$extensions": { "lizenz": "OFL | kommerziell, Dateien vom Kunden | unklar", "quelle": "F7", "ersatz_fuer_entwurf": "Name oder null" } }
```

## 3 · Modi

- Ein Rollen-Token hat in `$value` den Wert für den **ersten** Modus aus `$marke.modi`, die anderen stehen in `$extensions.modi`.
- Hat die Marke nur einen Modus, gibt es keine `$extensions.modi`.
- **Druck** ist kein Modus der Website. Druckwerte stehen, wo sie abweichen, unter `$extensions.modi.druck` (z. B. dunklere Akzentschrift für Papier). Fehlt der Eintrag, gilt der Wert des hellen Modus.

## 4 · Was das Skript erzeugt

```bash
python3 scripts/tokens.py <lauf>/tokens/tokens.json
```

| Datei | Inhalt |
|---|---|
| `tokens.css` | CSS-Variablen mit Präfix `--m-`: `--m-farbe-grund`, `--m-schrift-titel`, `--m-text-titel-1-groesse` usw. Standardmodus in `:root`, weitere in `[data-modus="…"]`, bei `folgt_system` zusätzlich `@media (prefers-color-scheme: …)` |
| `theme.css` | Tailwind v4 `@theme inline` auf diese Variablen: `--color-<rolle>`, `--font-<familie>`, `--text-<stufe>` mit Zeilenhöhe, Laufweite und Gewicht, `--radius-<name>`, `--shadow-<name>`, `--ease-<name>`, `--spacing` aus dem Grundraster |
| `druck.css` | dieselben Variablen mit Druckwerten, Schriftstufen in `pt` |
| `tokens-uebersicht.md` | Tabelle aller Tokens für den Guide (Anhang) |
| `tokens-befunde.json` | Fehler: fehlende Pflicht-Tokens, kaputte Verweise, Farben ohne Herkunft, unlesbare Werte |

Das Skript bricht mit Exit 1 ab, wenn Pflicht-Tokens fehlen oder Verweise ins Leere zeigen.

## 5 · Kontrastpaare

```bash
python3 scripts/kontrast.py <lauf>/tokens/tokens.json
```

Prüft in jedem Modus diese Paare und schreibt `kontrast.md` (fertige Tabelle für Kapitel Farbe) und `kontrast.json`:

| Vordergrund | Hintergrund | Grenze |
|---|---|---|
| `text`, `text-leise`, `akzent-text`, `fehler` | `grund`, `flaeche` (und `flaeche-2`, `flaeche-akzent`, falls vorhanden) | 4,5 : 1 |
| `handlung-text` | `handlung`, `handlung-hover` | 4,5 : 1 |
| `linie-stark`, `fokus`, `akzent` | `grund` | 3 : 1 |

Weitere Paare, die die Marke wirklich einsetzt (z. B. Schrift auf einer Signaturfläche), stehen in `$marke.kontrastpaare` als `["farbe.rolle.x", "farbe.rolle.y", "text" | "gross" | "grafik"]` (Grenzen 4,5 / 3 / 3). Farben mit Deckkraft werden gegen ihren Hintergrund gemischt, bevor gerechnet wird.

Ein Paar unter der Grenze ist ein Verstoß gegen einen Mindeststandard (Klasse 1, `pruefung.md`). Er wird nicht weggeredet, sondern als Widerspruch vorgelegt, mit einem Vorschlag in der Marke (z. B. eine dunklere Fassung der Akzentfarbe für Schrift).

## 6 · Regeln für Skalen

- **Schrift:** feste Stufen, keine freien Größen. Fließtext (`fliesstext`; nicht `text`, weil Tailwind sonst die Farbe `text` und die Stufe `text` zu derselben Klasse macht) mindestens 16 px, `label` mindestens 12 px, Eingabefelder mindestens 16 px. Wie viele Stufen und welches Verhältnis zwischen ihnen, folgt aus dem Achsenprofil (leise ↔ laut), nicht aus einer Vorlage.
- **Abstände:** eine Reihe auf einem Grundraster (z. B. 4 oder 8 px oder ein Raster aus dem Bestand). Welche Reihe, folgt aus luftig ↔ dicht.
- **Radien:** innen kleiner als außen. Welche Werte, folgt aus eckig ↔ rund und aus der Formensprache des Logos.
- **Bewegung:** Rückmeldung (Hover, Öffnen) zwischen 150 und 300 ms, größere Wege bis etwa 500 ms. Ein orchestrierter Moment darf länger sein, wenn er als eigener Token benannt und im Guide begründet ist.
