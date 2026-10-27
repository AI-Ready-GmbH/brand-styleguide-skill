# Regeln: Web Interface Guidelines (Kurzfassung)

| | |
|---|---|
| Quelle | github.com/vercel-labs/web-interface-guidelines (Vercel) |
| Stand | Commit `434b7f91364665f2f733b310ec54809bf8f37937` vom 05.10.2026 |
| Lizenz | MIT, `vendor/web-interface-guidelines/LICENSE` |
| Original | `vendor/web-interface-guidelines/AGENTS.md` (Regeln mit MUST, SHOULD, NEVER) und `command.md` (Review-Befehl mit Regelliste und Ausgabeformat) |

Eigene deutsche Kurzfassung mit Fundstellen, keine Übersetzung. Im Zweifel gilt das Original.

**Klassen:** K1 Mindeststandard (gilt immer, Abweichung nur als ausdrückliche Entscheidung des Users), K2 Stil (die Marke gewinnt, Abweichung begründet in Kapitel 0), K3 Handwerk (Standard, Ausnahme mit Begründung).

**Fundstellen:** **A** = `AGENTS.md`, **C** = `command.md`, dahinter die Überschrift des Abschnitts im Original.

## Wofür der Skill es nutzt

**P6 Ausarbeitung:** Die Regeln bestimmen, wie die Bausteine (Button, Textlink, Karte, Eingabefelder, Logo …) technisch gebaut werden, welche ESLint- und Sanity-Leitplanken entstehen (z. B. `transition: all`, `outline: none` ohne Ersatz, Bild ohne Maße oder Alt-Text), was in `DESIGN.md` unter Verboten und Mindeststandards steht und was in Kapitel 13 (Checkliste vor dem Livegang) landet.

**P7 Prüfung:** Der Prüfer geht Bausteine und Musterseite mit dieser Liste durch. Für Code-Befunde übernimmt er das Format aus `command.md`: gruppiert nach Datei, `datei:zeile`, knapp, ohne Vorrede. Gestaltungsfragen wie Farb- oder Schriftwahl regelt die Quelle kaum.

## Regeln

### Tastatur und Fokus

| Regel | Klasse | Fundstelle |
|---|---|---|
| Vollständige Tastaturbedienung nach den WAI-ARIA-APG-Mustern, Fokus fangen, versetzen und zurückgeben wie dort beschrieben | K1 | A Keyboard; C Accessibility |
| Fokus sichtbar über `:focus-visible` (nicht `:focus`, damit beim Klick kein Ring erscheint), zusammengesetzte Steuerungen über `:focus-within` | K1 | A Keyboard; C Focus States |
| Sticky Header, Footer und Overlays verdecken das fokussierte Element nie | K1 | A Keyboard; C Focus States |
| Nie `outline: none` ohne sichtbaren Ersatz | K1 | A Keyboard; C Anti-patterns |

### Trefferflächen, Zoom, Touch

| Regel | Klasse | Fundstelle |
|---|---|---|
| Trefferfläche mindestens 24 px, mobil mindestens 44 px. Ist das Sichtbare kleiner, die Trefferfläche vergrößern | K1 | A Targets & Input |
| Eingabefelder mobil mit Schriftgröße mindestens 16 px, sonst zoomt iOS | K1 | A Targets & Input |
| Browser-Zoom nie sperren (`user-scalable=no`, `maximum-scale=1`) | K1 | A Targets & Input; C Anti-patterns |
| Gesten (Ziehen, Wischen, Pinch, Pfad) haben eine Klick- und eine Tastatur-Alternative, außer die Geste ist wesentlich | K1 | A Touch & Drag; C Touch & Interaction |
| `touch-action: manipulation` gegen Doppeltipp-Verzögerung, `-webkit-tap-highlight-color` bewusst zur Gestaltung setzen | K3 | A Targets & Input; C Touch & Interaction |
| Was klickbar aussieht, ist klickbar. Großzügige Ziele, klare Affordanz, keine fummeligen Interaktionen | K3 | A Touch & Drag |
| Beim Ziehen Textauswahl aus und gezogenes Element `inert`. In Modals, Drawern und Sheets `overscroll-behavior: contain` | K3 | A Touch & Drag; C Touch & Interaction |
| Gummiband-Effekt der Seite nur bei feinem Zeiger unterdrücken (`overscroll-behavior: none` in `@media (pointer: fine)`), auf Hybridgeräten testen | K3 | A Touch & Drag; C Touch & Interaction |
| Erster Tooltip verzögert, folgende in derselben Gruppe sofort | K3 | A Touch & Drag |
| Autofokus nur am Desktop bei einem einzigen Haupteingabefeld, mobil kaum | K3 | A Autofocus; C Touch & Interaction |

### Formulare

| Regel | Klasse | Fundstelle |
|---|---|---|
| Jedes Feld hat ein Label (`<label>` oder `aria-label`), Labels sind klickbar | K1 | C Accessibility, Forms |
| `autocomplete` und sprechender `name`, passender `type` und `inputmode` | K1 | A Forms; C Forms |
| Einfügen nie blockieren. Verträglich mit Passwortmanagern und 2FA, Codes lassen sich einfügen | K1 | A Forms; C Forms |
| Checkbox und Radio: Label und Steuerelement bilden eine Trefferfläche ohne tote Zonen | K1 | A Forms; C Forms |
| Fehler inline am Feld, beim Absenden Fokus auf den ersten Fehler, Meldungen über `aria-live="polite"` | K1 | A Forms, Feedback; C Forms, Accessibility |
| Absenden bleibt aktiv, bis die Anfrage startet, dann gesperrt mit Spinner. Der Ladebutton behält sein Label | K3 | A Forms; C Forms |
| Freie Eingabe annehmen und danach prüfen. Unvollständiges Absenden erlaubt, damit die Prüfhinweise erscheinen | K3 | A Forms |
| Enter sendet ab, in `<textarea>` ⌘/Strg+Enter | K3 | A Forms |
| Platzhalter enden mit „…“ und zeigen ein Beispielmuster | K3 | A Forms; C Forms |
| Rechtschreibprüfung aus bei E-Mail, Codes und Nutzernamen. Werte trimmen. `autocomplete="off"` bei Feldern ohne Anmeldung | K3 | A Forms; C Forms |
| Vor dem Verlassen mit ungespeicherten Änderungen warnen | K3 | A Forms; C Forms |

### Zustand, Navigation, Rückmeldung

| Regel | Klasse | Fundstelle |
|---|---|---|
| Navigation über `<a>`/`<Link>` (Strg/⌘-Klick, Mittelklick), nie `<div onClick>`. Aktionen über `<button>` | K3 | A State & Navigation; C Accessibility, Anti-patterns |
| URL bildet den Zustand ab (Filter, Tabs, Seiten, aufgeklappte Bereiche). Zurück und Vor stellen die Scrollposition her | K3 | A State & Navigation; C Navigation & State |
| Destruktive Aktionen bestätigen oder ein Rückgängig-Fenster anbieten, nie sofort | K3 | A Feedback; C Navigation & State |
| Optimistisch aktualisieren, bei Fehler zurückrollen oder Rückgängig anbieten | K3 | A Feedback |
| „…“ bei Optionen mit Folgeschritt („Umbenennen…“) und bei Ladezuständen („Lädt…“) | K3 | A Feedback; C Typography |
| Keine Sackgassen, immer ein nächster Schritt. Leere, spärliche, dichte und Fehlerzustände gestalten | K3 | A Content & Accessibility |
| Skeletons spiegeln den späteren Inhalt, damit nichts springt | K3 | A Content & Accessibility |
| Buttons und Links haben einen Hover-Zustand. Hover, Aktiv und Fokus sind kontraststärker als der Ruhezustand | K3 | C Hover & Interactive States; A Design |

### Bewegung

| Regel | Klasse | Fundstelle |
|---|---|---|
| `prefers-reduced-motion` beachten: reduzierte Fassung oder aus | K1 | A Animation; C Animation |
| Automatische Bewegung über 5 s neben anderem Inhalt braucht Pause, Stopp oder Ausblenden. Stumme Deko-Schleifen stoppen bei reduzierter Bewegung | K1 | A Animation; C Animation |
| Nur `transform` und `opacity` animieren, nie Layout-Eigenschaften (`top`, `left`, `width`, `height`) | K3 | A Animation; C Animation |
| Nie `transition: all`, Eigenschaften einzeln nennen | K3 | A Animation; C Anti-patterns |
| CSS vor Web Animations API vor JS-Bibliotheken | K3 | A Animation |
| Animationen unterbrechbar und von Eingaben gesteuert. Autoplay nur für stumme, nicht wesentliche Schleifen | K3 | A Animation; C Animation |
| Richtiger `transform-origin`. SVG-Transforms auf einer `<g>`-Hülle mit `transform-box: fill-box` | K3 | A Animation; C Animation |
| Nur animieren, um Ursache und Wirkung zu klären oder für bewusste Freude. Kurve passend zu Größe, Weg und Auslöser | K2 | A Animation |

### Layout

| Regel | Klasse | Fundstelle |
|---|---|---|
| Bewusste Ausrichtung an Raster, Grundlinie und Kanten. Optische Korrektur um ±1 px, wo die Wahrnehmung es verlangt | K3 | A Layout |
| Icon-Text-Kombinationen ausbalancieren (Gewicht, Größe, Abstand, Farbe) | K3 | A Layout |
| Prüfen auf Mobil, Laptop und Ultra-Wide (Ultra-Wide bei 50 % Zoom simulieren) | K3 | A Layout |
| Safe Areas über `env(safe-area-inset-*)`, keine ungewollten Scrollbalken, Flex und Grid statt Messen per JS | K3 | A Layout; C Safe Areas & Layout |
| Verschachtelte Radien: innen kleiner oder gleich außen, konzentrisch | K3 | A Design |

### Typografie und Text

| Regel | Klasse | Fundstelle |
|---|---|---|
| „…“ statt drei Punkten, typografische statt gerader Anführungszeichen | K3 | A Content & Accessibility; C Typography |
| Geschützte Leerzeichen zwischen Zahl und Einheit (`10&nbsp;MB`), in Tastenkürzeln und Markennamen | K3 | A Content & Accessibility; C Typography |
| `font-variant-numeric: tabular-nums` für Zahlenspalten und Vergleiche | K3 | A Content & Accessibility; C Typography |
| `text-wrap: balance` oder `pretty` gegen Hurenkinder und Schusterjungen | K3 | A Content & Accessibility; C Typography |
| Lange Inhalte abfangen (`truncate`, `line-clamp`, `break-words`, `min-w-0` in Flex). Kurze, mittlere und sehr lange Nutzereingaben aushalten, leere Werte ohne kaputte Oberfläche | K3 | A Content Handling; C Content Handling |
| Aktiv formulieren, konkrete Buttonbeschriftung, Fehlermeldung mit Lösung oder nächstem Schritt | K3 | C Content & Copy |
| Title Case für Überschriften und Buttons (Chicago) | K2 | C Content & Copy |
| Ziffern für Mengen, zweite Person statt erster, „&“ statt „and“ bei Platzmangel | K2 | C Content & Copy |

### Zugänglichkeit von Inhalten

| Regel | Klasse | Fundstelle |
|---|---|---|
| Bilder mit `alt` (dekorativ `alt=""`), dekorative Icons und Elemente `aria-hidden` | K1 | A Content & Accessibility; C Accessibility |
| Icon-Buttons mit beschreibendem `aria-label`. Zugängliche Namen auch dort, wo das Sichtbare kein Label zeigt | K1 | A Content & Accessibility; C Accessibility |
| Überschriften h1–h6 in Reihenfolge, Skip-Link zum Inhalt, `scroll-margin-top` an Überschriften-Ankern | K1 | A Content & Accessibility; C Accessibility |
| Status nie nur über Farbe, Icons mit Textlabel | K1 | A Content & Accessibility |
| Medien mit Untertiteln, Transkript oder Beschreibung, Steuerung per Tastatur. Dekorative Medien für Hilfstechnik verbergen | K1 | A Content & Accessibility; C Accessibility |
| Diagramme mit Paletten, die Farbfehlsichtige unterscheiden können | K1 | A Design |
| Kontrast einhalten. Die Quelle bevorzugt APCA vor WCAG 2 | K1 | A Design |
| Native Semantik (`button`, `a`, `label`, `table`) vor ARIA | K3 | A Content & Accessibility; C Accessibility |
| `<title>` passt zum aktuellen Kontext. Hilfe zuerst inline, Tooltips zuletzt | K3 | A Content & Accessibility |

### Bilder, Schriften, Performance

| Regel | Klasse | Fundstelle |
|---|---|---|
| `<img>` mit `width` und `height` gegen Layoutsprünge. Oberhalb der Falz vorladen (`priority`, `fetchpriority="high"`), darunter `loading="lazy"` | K3 | A Performance; C Images |
| Kritische Schriften per `<link rel="preload" as="font">` mit `font-display: swap`, `preconnect` zu CDN- und Asset-Domains | K3 | A Performance; C Performance |
| Video (`autoplay muted loop playsinline`) statt animiertem GIF, mit Standbild. Kurze Schleifen mit H.264-MP4 für Safari, Bedingung für reduzierte Bewegung und Standbild | K3 | A Performance; C Performance |
| Listen über 50 Einträge virtualisieren. Layout-Lesen und -Schreiben bündeln, kein Layout-Lesen im Render | K3 | A Performance; C Performance |
| Mutationen (`POST`, `PATCH`, `DELETE`) unter 500 ms. Mit Drosselung messen, Re-Renders klein halten, iOS-Stromsparmodus und Safari testen | K3 | A Performance |

### Dunkler Modus, Lokalisierung, Hydration

| Regel | Klasse | Fundstelle |
|---|---|---|
| Dunkle Themes: `color-scheme: dark` am `<html>`. `<meta name="theme-color">` passt zum Seitengrund. Natives `<select>` mit expliziter Hinter- und Vordergrundfarbe | K3 | A Dark Mode & Theming; C Dark Mode & Theming |
| Datum, Zeit, Zahlen und Währung über `Intl.*`, keine festen Formate. Sprache über `Accept-Language`, nicht über die IP | K3 | A Content & Accessibility; C Locale & i18n |
| Markennamen, Code und Kennungen mit `translate="no"` | K3 | A Content & Accessibility; C Locale & i18n |
| Felder mit `value` brauchen `onChange` (sonst `defaultValue`). Datumsanzeige gegen Abweichung zwischen Server und Client absichern | K3 | A Hydration; C Hydration Safety |

### Gestaltung

| Regel | Klasse | Fundstelle |
|---|---|---|
| Geschichtete Schatten (Umgebung plus direkt), klare Kanten über halbtransparente Ränder plus Schatten | K2 | A Design |
| Ränder, Schatten und Text zum Farbton des Grunds tönen | K2 | A Design |
| Browser-Oberfläche an den Grund anpassen, Banding bei dunklen Verläufen vermeiden | K3 | A Design |

### Anti-Pattern-Liste für die Prüfung

`command.md` nennt unter „Anti-patterns“ 14 Muster, die der Prüfer immer meldet: Zoom gesperrt, Einfügen blockiert, `transition: all`, `outline-none` ohne Ersatz, Navigation per `onClick` ohne `<a>`, klickbare `div` oder `span`, Bilder ohne Maße, große Listen ohne Virtualisierung, Felder ohne Label, Icon-Buttons ohne `aria-label`, feste Datums- und Zahlenformate, `autoFocus` ohne Grund, animiertes GIF statt Video, Geste ohne Klick- und Tastatur-Alternative.

### Nicht geregelt

Farbwahl, Schriftwahl, Logo, Abstandsskala, Radien als Werte, Bildwelt, Ikonografie (außer Zugänglichkeit), Druck. Kein Zahlenwert für Kontrast (nur „einhalten“, APCA bevorzugt) und keine Mindestgröße für Fließtext außerhalb von Eingabefeldern.

## Typische Konflikte mit Marken

| Fall | Regel | Behandlung |
|---|---|---|
| Kontrastmaß | APCA bevorzugt (A Design) | Der Skill prüft nach WCAG 2.2 AA mit 4,5 : 1 und 3 : 1 (Konzept 4.2, `tokens.md` Abschnitt 5). APCA ist im Konzept nicht vorgesehen |
| Trefferflächen | 24 px am Desktop, 44 px mobil (A Targets & Input) | Das Konzept setzt 44 px für alle Bausteine (Abschnitt 7). Es gilt die strengere Grenze, K1 |
| Hover, der den Kontrast senkt (z. B. hellerer Button) | Hover kontraststärker als Ruhe (A Design) | K3, Ausnahme mit Begründung möglich. Der Kontrast im Hover bleibt K1 (`handlung-text` auf `handlung-hover`, 4,5 : 1) |
| Markenbewegung mit Höhe, Clip-Path oder Blur | nur `transform` und `opacity` (A Animation) | K3, Ausnahme mit Begründung und Messung. Impeccable erlaubt hier ausdrücklich mehr (`regeln-impeccable.md`) |
| Autoplay-Video im Hero, Laufband, bewegte Logo-Leiste | Steuerung ab 5 s (A Animation) | K1. Als Widerspruch vorlegen, mit Optionen wie statisch, mit Steuerung oder nach höchstens 5 s stehend |
| Title Case, „&“, Ziffern, Ansprache | C Content & Copy | K2. Sprache und Tonalität der Marke gewinnen, im Deutschen gilt die Rechtschreibung. Spricht die Marke als „wir“, bleibt das |
| Anführungszeichen | typografisch statt gerade | K3, aber in der Sprache der Marke: „…“ im Deutschen, «…» in der Schweiz |
| flache Marke ohne Schatten oder mit harten Kanten | geschichtete Schatten, getönte Ränder (A Design) | K2. Die Schattenregeln entfallen, wenn die Formensprache der Marke keine Schatten hat |
| dezenter Fokusring passend zur Marke | sichtbarer Fokus (A Keyboard) | K1. Der Ring bleibt sichtbar und erreicht 3 : 1 gegen den Grund (`farbe.rolle.fokus`, `tokens.md`) |
| feste Datums- oder Preisformate im Bestand | `Intl.*` (A Content & Accessibility) | K3. In Bausteinen über `Intl` lösen, Ausnahme nur begründet |
