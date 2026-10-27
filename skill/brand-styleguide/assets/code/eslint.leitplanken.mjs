// Leitplanken für den Komponenten-Code · Guide 4.x (Farbe), 5.x (Typografie), 6.x (Form), 11.x (Bewegung)
//
// Verboten in TSX/TS unter app/ und components/: freie Schriftgrößen, freie Radien, Farben als Hex-Wert,
// rgb, rgba, hsl und andere Farbfunktionen, Tailwind-Standardpaletten und freie Dauern. Erlaubt sind nur Token-Klassen
// aus theme.css (bg-<rolle>, text-<rolle>, text-<stufe>, rounded-<radius>, ease-<kurve>) und var(--m-…),
// Dauern als duration-(--m-dauer-<name>).
//
// Einbinden in eslint.config.mjs:  import {leitplanken} from './eslint.leitplanken.mjs'  …  ...leitplanken,
// Achtung: no-restricted-syntax überschreibt eine gleichnamige Regel aus früheren Einträgen. Hat das Projekt
// eigene Selektoren, SELEKTOREN hier importieren und zusammenführen.

const ROLLEN = 'bg-<rolle>, text-<rolle>, border-<rolle> (z. B. bg-handlung, text-text-leise, border-linie-stark)'
const STUFEN = 'text-display, text-titel-1 … text-titel-3, text-lead, text-fliesstext, text-klein, text-label'
const PALETTE = 'slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose'
const FARB_PRAEFIX = 'bg|text|border|ring|outline|fill|stroke|from|via|to|decoration|divide|placeholder|caret|accent|shadow'
// ohne text- und shadow-: deren […]-Formen haben eigene Regeln unten
const FARB_PRAEFIX_FREI = 'bg|border|ring|outline|fill|stroke|from|via|to|decoration|divide|placeholder|caret|accent'

/** [Muster für Klassen und Zeichenketten, Meldung] */
const MUSTER = [
  // Farbe (Guide 4.x)
  [String.raw`#(?:[0-9a-fA-F]{3,4}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b`, `Hex-Farbe: Farbrolle als Token nutzen, ${ROLLEN}, oder var(--m-farbe-<rolle>).`],
  [String.raw`\b(?:rgba?|hsla?|hwb|lab|lch|oklab|oklch)\(`, `Farbfunktion: Farbrolle als Token nutzen; Deckkraft über color-mix(in srgb, var(--m-farbe-<rolle>) x%, transparent) oder bg-<rolle>/x.`],
  [String.raw`\b(?:${FARB_PRAEFIX})-(?:(?:${PALETTE})-\d{2,3}|white|black)\b`, `Tailwind-Standardfarbe: gilt nicht in diesem System. Farbrolle nutzen, ${ROLLEN}.`],
  [String.raw`\b(?:${FARB_PRAEFIX_FREI})-\[(?!url\()`, `Freier Wert in Klammern bei einer Farbklasse: Farbrolle nutzen, ${ROLLEN}.`],
  // Schrift (Guide 5.x)
  [String.raw`\btext-(?:\[|\()`, `Freie Schriftgröße oder Farbe (text- mit Klammerwert): Schriftstufe (${STUFEN}) oder Farbrolle (text-<rolle>) nutzen.`],
  [String.raw`\btext-(?:xs|sm|base|lg|xl|[2-9]xl)\b`, `Tailwind-Schriftgröße: gilt nicht in diesem System. Schriftstufe nutzen: ${STUFEN}.`],
  [String.raw`\b(?:leading|tracking)-(?:\[|\(|tight|tighter|snug|normal|relaxed|loose|wide|wider|widest)`, `Zeilenhöhe und Laufweite gehören zur Schriftstufe (${STUFEN}); eine neue Stufe kommt in tokens.json.`],
  [String.raw`\bfont-(?:\[|\(|sans\b|serif\b)`, 'Freie Schrift: Schriftfamilie als Token nutzen (font-titel, font-text, ggf. font-akzent, font-mono).'],
  // Form (Guide 6.x)
  [String.raw`\brounded(?:-[a-z]{1,2})?-[\[(]`, 'Freier Radius: rounded-steuerung (Buttons, Felder), rounded-karte oder rounded-pille nutzen.'],
  [String.raw`\brounded(?:-[a-z]{1,2})?-(?:xs|sm|md|lg|xl|[2-4]xl)\b|\brounded(?![-\w])`, 'Tailwind-Radius: gilt nicht in diesem System. rounded-steuerung, rounded-karte oder rounded-pille nutzen.'],
  [String.raw`\bshadow-(?:2xs|xs|sm|md|lg|xl|2xl|inner|\[|\()`, 'Freier oder Tailwind-Schatten: Schatten-Token nutzen (shadow-<name> aus theme.css), sonst flach bleiben.'],
  // Bewegung (Guide 11.x)
  [String.raw`\b(?:duration|delay)-(?:\d|\[|\((?!--m-dauer-))`, 'Freie Dauer: Dauer-Token nutzen, duration-(--m-dauer-kurz | mittel | lang).'],
  [String.raw`\bease-(?:\[|\((?!--m-kurve-)|in\b|out\b|in-out\b)`, 'Freie Kurve: Kurven-Token nutzen, ease-standard (ggf. ease-weg).'],
  [String.raw`\banimate-(?:\[|\()|\[(?:transition|animation)[-:]`, 'Freie Animation: Bewegung nur mit Dauer- und Kurven-Token (Guide 11.x), Keyframes in marke.css.'],
]

/** Selektoren für style={{…}}: nur var(--m-…) ist erlaubt */
const STIL = (eigenschaften, meldung) => ({
  selector: `JSXAttribute[name.name="style"] Property[key.name=/^(?:${eigenschaften})$/] > Literal:not([value=/^var\\(--m-/])`,
  message: meldung,
})

export const SELEKTOREN = [
  ...MUSTER.flatMap(([re, message]) => [
    {selector: `Literal[value=/${re}/]`, message},
    {selector: `TemplateElement[value.raw=/${re}/]`, message},
  ]),
  STIL('fontSize|fontFamily|fontWeight|lineHeight|letterSpacing', `Schrift im style-Attribut: Schriftstufe als Klasse nutzen (${STUFEN}).`),
  STIL('borderRadius|borderTopLeftRadius|borderTopRightRadius|borderBottomLeftRadius|borderBottomRightRadius', 'Radius im style-Attribut: rounded-steuerung, rounded-karte oder rounded-pille nutzen.'),
  STIL('color|background|backgroundColor|borderColor|outlineColor|fill|stroke|boxShadow', `Farbe im style-Attribut: Farbrolle als Klasse (${ROLLEN}) oder var(--m-farbe-<rolle>).`),
  STIL('transition|transitionDuration|transitionDelay|transitionTimingFunction|animation|animationDuration|animationDelay', 'Bewegung im style-Attribut: duration-(--m-dauer-<name>) und ease-standard als Klasse nutzen.'),
]

/**
 * Ausnahmen (Pfade als Glob). Nur mit Begründung im Kommentar daneben, sonst gilt die Regel.
 * Beispiel: 'app/opengraph-image.tsx' // OG-Bild über Satori: kennt keine CSS-Variablen, Farben aus tokens.json importiert
 */
export const AUSNAHMEN = []

export const leitplanken = [
  {
    files: ['app/**/*.{ts,tsx}', 'components/**/*.{ts,tsx}'],
    ignores: AUSNAHMEN,
    rules: {'no-restricted-syntax': ['error', ...SELEKTOREN]},
  },
]
