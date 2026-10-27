# Stack Next.js, Tailwind v4, Sanity (P6, P7, P8)

Mit Stack liefert der Lauf neben Guide und Tokens Bausteine, Leitplanken und zwei Regeldateien, mit denen Claude Code die Website gleich im System der Marke baut. Die Vorlagen in `assets/code/` enthalten **keine Gestaltung**: keine Farbe, Schrift, Größe, Radius, Dauer, keine Signatur. Alle Optik kommt aus Token-Klassen, `var(--m-…)` und der Datei `marke.css`. Stellen, an denen die Marke entscheidet, tragen `/* MARKE: … */`.

## Inhalt
1. Wann der Stack aktiv ist
2. Was der Lauf erzeugt und wohin es im Repo gehört
3. Bausteine an die Marke anpassen
4. Leitplanken einbinden
5. DESIGN.md und PRODUCT.md
6. Prüfung (P7)
7. Einbau-Hinweis für die Übergabe (P8)
8. Offene Punkte

## 1 · Wann der Stack aktiv ist

Briefing-Frage B7 (`lauf.json` → `"stack": true`), Standard ja. Antwortet der User „nein“ oder baut die Website anders: kein Ordner `code/`. `DESIGN.md` und `PRODUCT.md` entstehen trotzdem; in `DESIGN.md` entfallen die Ergänzungen „Tokens im Code“ und „Bausteine“, Werte stehen dann als `var(--m-…)`.

**Vor jedem Einbau** (auch beim Testen der Vorlagen) die Doku der im Repo installierten Next-Version lesen: `node_modules/next/dist/docs/`. Die Vorlagen sind für Next 16, React 19, Tailwind 4.3 geschrieben. Bekannte Stellen: `next/image` heißt `preload` ab 16, davor `priority`; `useId` in Server Components braucht React 19.

## 2 · Was der Lauf erzeugt und wohin es gehört

| Im Lauf | Herkunft | Im Website-Repo |
|---|---|---|
| `tokens/tokens.css`, `tokens/theme.css` | `scripts/tokens.py` | `app/tokens.css`, `app/theme.css` |
| `code/marke.css` | P6, neu je Marke | `app/marke.css` |
| `code/components/ui/*.tsx`, `index.ts` | `assets/code/components/ui/`, MARKE-Stellen gefüllt | `components/ui/` |
| `code/components/ui/<signatur>.tsx` | `signatur.tsx.vorlage`, 1–3 Stück | `components/ui/` |
| `code/eslint.leitplanken.mjs` | `assets/code/` | Repo-Wurzel |
| `code/sanity/leitplanken.ts` | `assets/code/sanity/`, MARKE-Blöcke gefüllt | neben den Schemas, z. B. `sanity/schemaTypes/` |
| `DESIGN.md`, `PRODUCT.md` | `DESIGN.vorlage.md`, `PRODUCT.vorlage.md` | Repo-Wurzel |

`code/marke.css` ist nicht `guide/marke.css`: Die eine gestaltet Website-Bausteine, die andere die Seiten des Guides.

**`app/globals.css`** (Reihenfolge wichtig, das Zurücksetzen muss vor `theme.css` stehen; geprüft mit Tailwind 4.3):

```css
@import "tailwindcss";
/* Tailwind-Standardwerte aus, die die Tokens ersetzen (Breakpoints, Gewichte, Container bleiben) */
@theme {
  --color-*: initial; --font-*: initial; --text-*: initial; --leading-*: initial; --tracking-*: initial;
  --radius-*: initial; --shadow-*: initial; --inset-shadow-*: initial; --drop-shadow-*: initial;
  --text-shadow-*: initial; --ease-*: initial; --animate-*: initial;
}
@import "./tokens.css";
@import "./theme.css";
@import "./marke.css";

/* nur, wenn die Marke den Modus dunkel hat; den @media-Teil nur bei folgt_system */
@custom-variant dunkel {
  &:where([data-modus="dunkel"], [data-modus="dunkel"] *) { @slot; }
  @media (prefers-color-scheme: dark) { &:where(:root:not([data-modus]), :root:not([data-modus]) *) { @slot; } }
}

@layer base {
  html { color-scheme: {{hell: light | dunkel: dark | beide: light dark}}; }
  body {
    background-color: --theme(--color-grund); color: --theme(--color-text); font-family: --theme(--font-text);
    font-size: --theme(--text-fliesstext); line-height: --theme(--text-fliesstext--line-height);
  }
  /* Rückfall für alles, was nicht aus den Bausteinen kommt; 2 px ist Mindeststandard, keine Gestaltung */
  :focus-visible { outline: 2px solid --theme(--color-fokus); outline-offset: 2px; }
  /* Rückfall bei reduzierter Bewegung: Effekte springen in ihren Endzustand. Wo ein Zustandswechsel Bedeutung
     trägt (geöffnet, gewählt), erlaubt der Baustein selbst eine kurze Überblendung (opacity), siehe pruefung.md. */
  @media (prefers-reduced-motion: reduce) {
    *, ::before, ::after { animation-duration: 0.01ms !important; animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important; scroll-behavior: auto !important; }
  }
}
```

Dazu im Layout `<html lang="{{sprache}}">` und `<meta name="theme-color">` mit dem Wert von `grund` je Modus.

## 3 · Bausteine an die Marke anpassen

Erlaubt sind genau drei Wege, in dieser Reihenfolge:
1. **Tokens.** Was sich über eine Rolle, Stufe, einen Radius oder eine Dauer sagen lässt, kommt in `tokens.json`. Neue Werte entstehen nie im Code.
2. **MARKE-Stellen in den Bausteinen.** Nur Token-Klassen tauschen (z. B. `text-label` statt `text-fliesstext`, `rounded-pille` statt `rounded-steuerung`), Abstände in Rasterschritten, Varianten nach Guide 8. Den Kommentar stehen lassen und `Guide 8.x` durch die echte Stelle ersetzen. Struktur, Semantik, Fokus, Trefferflächen, `motion-reduce` und die `data-`-Attribute bleiben.
3. **`marke.css`** für alles, was kein Token abbildet: Versalien, Unterstreichung (Dicke, Abstand), Pfeil oder Lader am Button, Pfeil im Select, Anker-Abstand (`scroll-margin-top`), Keyframes. Nur `var(--m-…)` und Selektoren auf die Attribute der Bausteine:

| `data-baustein` | weitere Attribute |
|---|---|
| `button` | `data-variante` (primaer, sekundaer), `data-laedt` |
| `textlink` | `data-art` (im-text, eigenstaendig) |
| `karte` | `data-variante` |
| `sektionskopf`, `kennzahl`, `zitat`, `logo` | – |
| `badge` | `data-ton` |
| `feld` | `data-pflicht`, `data-fehler`; Fehlertext `data-teil="fehler"` |

**Signatur-Bausteine:** je Signatur-Element aus Guide 7, das auf der Website vorkommt, ein Baustein nach `signatur.tsx.vorlage` (insgesamt 1–3). Aufgabe, Grenze und Herleitung stehen wörtlich im JSDoc; ohne Herleitung kein Baustein. Export in `index.ts`, Eintrag in `DESIGN.md`.

Nie: Werte in einer Seite, eine vierte Kartenvariante ohne Guide, ein Baustein, der eine Gestaltung fest einbaut, die nicht aus den Tokens kommt.

## 4 · Leitplanken einbinden

**ESLint** (`eslint.config.mjs`, nach den Next-Einträgen):

```js
import {leitplanken} from './eslint.leitplanken.mjs'
export default defineConfig([...nextVitals, ...nextTs, ...leitplanken, globalIgnores([...])])
```

Die Regel prüft `app/` und `components/` (TS, TSX). `AUSNAHMEN` bleibt leer; ein Eintrag nur mit Begründung daneben (typisch: OG-Bilder über Satori, die keine CSS-Variablen kennen und Farben aus `tokens.json` importieren). Hat das Repo eigene `no-restricted-syntax`-Selektoren, mit `SELEKTOREN` zusammenführen, sonst überschreibt die eine Regel die andere.

**Sanity:** Prüfungen in die Schemas hängen, Beispiele im Kopf von `leitplanken.ts`. Vorher füllen: `HANDLUNG` (Feldnamen der Handlung im Projekt), `GRENZEN` (Zeichen aus Guide 12), `HERVORHEBUNG` (nur wenn die Marke eine Syntax hat, sonst `null`). Jeder Block bekommt `hoechstensEinePrimaereHandlung` als Fehler; jedes Bild- und Logo-Feld `altTextFeld()`; jedes Video `autoplayFeld()`.

## 5 · DESIGN.md und PRODUCT.md

- **`DESIGN.md`** aus `DESIGN.vorlage.md`: Kopf aus `tokens.json` (Standardmodus, deutsche Token-Namen), die acht Hauptabschnitte mit den englischen Überschriften von Impeccable in fester Reihenfolge, Inhalt in der Sprache der Marke, danach unsere Ergänzungen (Tokens im Code, Bausteine, Mindeststandards, Checkliste, Quellen). Textteil ohne YAML-Kopf unter 150 Zeilen, damit eine Agentin sie ganz liest.
- **`PRODUCT.md`** aus `PRODUCT.vorlage.md`: nur Fakten aus Markenkern und Briefing mit Beleg, keine Gestaltung.
- **Einbinden:** in `CLAUDE.md` die Zeilen `@DESIGN.md` und `@PRODUCT.md`; in `AGENTS.md` den Satz „Vor jeder Arbeit an der Oberfläche DESIGN.md und PRODUCT.md lesen.“ Gibt es im Repo schon eine `DESIGN.md` oder `PRODUCT.md`: nie still überschreiben, zeigen und fragen (auffrischen, ersetzen, zusammenführen).

## 6 · Prüfung (P7, Code)

| Prüfung | Wie | Grenze |
|---|---|---|
| Leitplanken | ESLint mit `eslint.leitplanken.mjs` über `code/` (siehe unten) | 0 Fehler |
| Typen | `tsc --noEmit` mit `strict` | 0 Fehler |
| Klassen | jede Klasse der Bausteine erzeugt CSS mit `theme.css` (Tailwind `compile`, wie unten) | 0 ohne Wirkung |
| Platzhalter | `grep -rn "{{\|Guide [0-9]*\.x" code/ DESIGN.md PRODUCT.md`, `GRENZEN` ohne `null` | 0 Funde |
| Gestaltung im Code | `grep -rnE '#[0-9a-fA-F]{3,8}\b\|\b(rgba?\|hsla?)\(\|text-\[\|rounded(-[a-z]{1,2})?-\[\|duration-[0-9[]' code/components` | 0 Funde |

**Ohne eigenes `node_modules`:** Liegt ein Next-Repo mit installierten Paketen vor (Kunden-Repo oder Vorbild), ESLint und `tsc` von dort benutzen, ohne dort etwas zu ändern: Bausteine in einen Ordner im Scratchpad kopieren, daneben eine `eslint.config.mjs`, die den Parser `@typescript-eslint/parser` per absolutem Pfad aus dem fremden `node_modules` lädt und `leitplanken` einbindet, und eine `tsconfig.json` mit `paths` auf `<repo>/node_modules/@types/*` und `<repo>/node_modules/*`. Nichts installieren. Gibt es kein solches Repo, laufen nur die grep-Prüfungen; das steht als Befund in `arbeit/05-pruefung.md`.

## 7 · Einbau-Hinweis für die Übergabe (P8)

In die Nachricht an den User, mit den echten Pfaden des Laufs:
1. Im Website-Repo einen Branch anlegen und die Doku der installierten Next-Version lesen (`node_modules/next/dist/docs/`).
2. `tokens.css`, `theme.css`, `marke.css` nach `app/`; `globals.css` nach Abschnitt 2 anpassen.
3. `components/ui/` übernehmen (bestehende Bausteine gleichen Namens erst vergleichen, nicht überschreiben).
4. `eslint.leitplanken.mjs` in die Wurzel, in `eslint.config.mjs` einbinden; `npx eslint .` zeigt, wo alter Code Werte außerhalb der Tokens hat.
5. `leitplanken.ts` neben die Sanity-Schemas, in die Block-, Bild- und Video-Schemas einhängen.
6. `DESIGN.md` und `PRODUCT.md` in die Wurzel, in `CLAUDE.md` und `AGENTS.md` einbinden.
7. `npx tsc --noEmit`, `npx eslint .`, Build; Startseite bei 375 und 1440 px{{, hell und dunkel}} ansehen.

## 8 · Offene Punkte

- **Deutsche Token-Namen im YAML-Kopf von `DESIGN.md`:** Impeccable nennt Skalen-Schlüssel offen, zeigt aber englische Rollen. Wir behalten die deutschen Namen, weil sie die echten Namen im Code sind; ob Impeccables Werkzeuge damit voll arbeiten, ist ungeprüft (Plattformtest).
- **Named Rules** stehen deutsch als „Die …-Regel.“ statt `**The … Rule.**`; Verträglichkeit wie oben.
- **Eyebrow/Kicker:** bei Impeccable ein Bann, bei uns Stilregel K2. Nutzt die Marke sie begründet, melden Impeccable-Werkzeuge im Kunden-Repo sie trotzdem weiter.
- **`theme.css`** bildet seit 26.10. auch Layout und Dauern ab: `max-w-inhalt` (Container), `max-w-lese` (Lesebreite), `duration-kurz|mittel|lang` (Namensraum `--transition-duration-*`), Breakpoints als `--breakpoint-<name>` mit festen Werten. Die Bausteine nutzen weiter `duration-(--m-dauer-…)`; beides funktioniert.
