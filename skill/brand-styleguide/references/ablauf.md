# Ablauf: Start, Briefing, Lauf-Ordner, Übergabe

## Inhalt
1. Der Lauf-Ordner
2. `lauf.json`
3. P0 Start
4. P1 Briefing
5. Wiederaufnahme
6. Autopilot
7. P8 Übergabe

## 1 · Der Lauf-Ordner

Frag zu Beginn, wo der Lauf liegen soll. Schlag `~/Documents/Building/Brand-Guides/<marke>/` vor, wenn es ein lokales Dateisystem gibt; im claude.ai-Chat ist es das Arbeitsverzeichnis der Sitzung, und die Dateien bekommt der User als Download.

```
<ablage>/<marke>/
├── lauf.json                 Stand, Werkzeuge, Entscheidungen
├── 00-briefing.md
├── arbeit/                   Arbeitsdateien, nicht Teil des Guides
│   ├── 01-fakten.md          Faktenblatt (F1 …) mit Fundstellen
│   ├── 01-messung/           messung.json, messung.md, Screenshots
│   ├── 02-auswertung.md      was trägt, was nicht, Widersprüche (W1 …)
│   ├── 03-markenkern.md      eine Seite, Soll-Achsenprofil
│   ├── 04-richtungen/        Tafeln je Richtung (Tokens, CSS, PNG), richtungen.md
│   ├── 05-pruefung.md        Ergebnis der Skripte und des Prüfers
│   └── quellen/              Dateien des Users (Vorgaben, Logos, PDFs)
├── guide/                    guide.md, marke.css, guide.html, <MARKE>_Brand-Style-Guide_v<x>.pdf
├── tokens/                   tokens.json und daraus erzeugte Dateien
├── code/                     Bausteine und Leitplanken (nur mit Stack)
├── DESIGN.md, PRODUCT.md
└── beispiele/                Musterseite, Social-Kachel, Cover (HTML und PNG)
```

Der Slug `<marke>` ist der Markenname in Kleinbuchstaben mit Bindestrichen, ohne Umlaute (ä → ae).

## 2 · `lauf.json`

```json
{
  "skill_version": "0.1.0",
  "marke": "Name wie verbindlich geschrieben",
  "slug": "name",
  "phase": "P0",
  "autopilot": false,
  "sprache": "de",
  "freigabe_durch": "Name, Rolle",
  "module": ["web"],
  "stack": true,
  "profil": null,
  "werkzeuge": {},
  "quellen": [{ "id": "Q1", "art": "website | datei | interview", "ort": "URL oder Pfad", "hinweis": "" }],
  "achsen_soll": {},
  "entscheidungen": {
    "W1": { "runde": 1, "frage": "…", "optionen": ["a …", "b …"], "empfehlung": "b", "antwort": "b", "vorlaeufig": false }
  },
  "ausnahmen_k1": [{ "paar": "akzent-text/grund", "modus": "hell", "entscheidung": "W2" }],
  "versionen": [{ "version": "1.0", "datum": "TT.MM.JJJJ", "aenderung": "Erstfassung", "freigabe": "Name, Datum" }]
}
```

Halte `phase` aktuell. Trag jede Antwort sofort ein, mit `vorlaeufig: true`, wenn der User nicht selbst entschieden hat. `ausnahmen_k1` enthält nur Abweichungen von Mindeststandards, die der User ausdrücklich entschieden hat (`entscheidungen.md`, Abschnitt 6); `freigabe` in `versionen` bleibt leer, bis der User in Runde 3 freigibt.

## 3 · P0 Start

1. **Werkzeuge:** `python3 scripts/werkzeuge.py --lauf <ordner>` (schreibt `werkzeuge` in `lauf.json`). Sag dem User in einem Satz, was fehlt und was das bedeutet, etwa: „Hier gibt es keinen Browser. Ich lese die Website aus dem Quelltext und bitte dich um zwei Screenshots.“
2. **Fortsetzen oder neu:** Liegt im Ordner schon eine `lauf.json`, lies sie und mach in der dort genannten Phase weiter (Abschnitt 5).
3. **Hausprofil:** Gehört die Marke zur falkemedia Gruppe (Liste in `profil-falkemedia.md`), lies das Profil und trag `"profil": "falkemedia"` ein. Bei allen anderen Marken lädst du es nie, auch nicht auszugsweise.

## 4 · P1 Briefing

Höchstens zehn Fragen, nummeriert (B1 …), mit Optionen und Empfehlung. Was die Quellen schon beantworten, fragst du nicht, sondern bestätigst es in einem Satz. Typische Fragen:

| Nr. | Frage | Warum |
|---|---|---|
| B1 | Wie heißt die Marke, genau so geschrieben, wie sie erscheinen soll? | Schreibweise im ganzen Guide |
| B2 | Wofür ist der Guide da: neue Website, Relaunch, Ordnung im Bestand? | bestimmt Tiefe und Beispiele |
| B3 | Für wen ist die Marke da (Zielgruppe in einem Satz)? | Markenkern, Lesbarkeit, Ton |
| B4 | Welche Kanäle braucht ihr? Web (hell, dunkel, beides), Druck, Social, Präsentationen, Bewegtbild, Mail, Verpackung | wählt die Module (`kapitel.md`) |
| B5 | Wer gibt den Guide frei (Name, Rolle)? | Freigabevermerk |
| B6 | In welcher Sprache soll der Guide sein? | Standard: Sprache der Marke |
| B7 | Wird die Website mit Next.js, Tailwind und Sanity gebaut? | schaltet Bausteine und Leitplanken an oder ab |
| B8 | Welche Quellen gibt es? Website-URL, vorhandene Vorgaben (Styleguide, CI-Handbuch, Präsentationen, Druckstücke), Logos als Vektordatei (SVG, PDF, EPS, AI), Schriftdateien | Pflicht: mindestens eine Quelle zur Marke und das Logo als Vektor |
| B9 | Gibt es Wettbewerber oder Vorbild-Websites, an denen ihr euch messt oder die ihr mögt? (optional) | Abgrenzung, Vorbilder für Aufbau |
| B10 | Gibt es etwas, das auf keinen Fall passieren darf? | Tabus früh kennen |

**Pflicht-Input:** mindestens eine Quelle zur Marke, das Briefing und das Logo als Vektordatei. Fehlt das Logo als Vektor, sag es sofort und frag nach der Originaldatei. Zeichne nie ein Logo nach und verwende keine Rastergrafik als Ersatz, ohne dass der User es ausdrücklich entscheidet.

**Bilder im Chat sind keine Dateien.** Schickt der User ein Bild in den Chat und du brauchst die Datei (Logo, Vorlage), sag das sofort.

**Neue Marke ohne Bestand:** führe das Markenkern-Interview (`markenkern.md`) und kennzeichne das Ergebnis als „Startfassung ohne Bestand“.

Schreib das Ergebnis in `00-briefing.md`.

## 5 · Wiederaufnahme

Ein Lauf kann über mehrere Sitzungen gehen. Beim Fortsetzen liest du `lauf.json`, die letzte Arbeitsdatei der Phase und offene Fragen. Fass für den User in zwei Sätzen zusammen, wo der Lauf steht, und mach weiter. Frag keine Entscheidung erneut, die in `lauf.json` steht.

## 6 · Autopilot

Für Testläufe oder wenn der User es ausdrücklich will („mach alles ohne Rückfragen“, „mach du“): Stelle die Fragen trotzdem zusammen und schreib sie in die Arbeitsdateien, setz deine Empfehlung als Antwort ein und markiere sie als vorläufig (`"vorlaeufig": true`, im Guide `[vorläufig: W2]`). Autopilot ändert nichts an den Mindeststandards, an den Fundstellen und an der Prüfung. Er überspringt nur das Warten.

## 7 · P8 Übergabe

1. Version und Datum in `lauf.json` und auf dem Cover, Freigabevermerk (wer, wann) je Version. Kein Protokoll je Einzelentscheidung im Guide; Entscheidungen fließen als Regel ein, der Änderungsverlauf sagt, was sich je Version geändert hat.
2. PDF rendern (`render.py pdf`), Kontaktbogen lesen, PDF und Beispiele an den User schicken.
3. In der Nachricht an den User:
   - die Dateien mit Pfad,
   - die vorläufigen Punkte (V1 …),
   - **nicht übernommen, weil …**: was in den Quellen stand und bewusst nicht in den Guide kam (unbelegt, widersprüchlich und anders entschieden, gegen Mindeststandard),
   - mit Stack: der Einbau-Hinweis aus `stack-next-sanity.md` (wohin `tokens.css`, `theme.css`, Bausteine, Leitplanken, `DESIGN.md` gehören).
4. Den Guide fortschreiben (neue Version) ist eine eigene Aufgabe, nicht Teil dieses Laufs.
