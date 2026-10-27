# Kapitel des Guides (P6)

Der Guide hat einen festen Kern und Module je Kanal aus dem Briefing. Die Struktur ist für jede Marke gleich, damit Leser sich zurechtfinden und Skripte prüfen können. **Der Inhalt jedes Kapitels entsteht aus der Marke.** Diese Datei sagt, was in ein Kapitel gehört und wie es geschrieben ist, nie welche Werte darin stehen.

## Inhalt
1. Machart: wie Regeln geschrieben werden
2. Aufbau von `guide.md`
3. Kern-Kapitel
4. Module je Kanal
5. Kurzbefehle für Tafeln und Bilder
6. Layout des Guides in der Marke

## 1 · Machart

- **Zahl und Grenze statt Adjektiv.** Nicht „sparsam einsetzen“, sondern „höchstens ein Element je Ansicht“. Nicht „großzügige Abstände“, sondern „Sektionen 96 px oben und unten, mobil 64 px“.
- **Jede Regel hat einen Grund** (Prinzip, Beleg oder Entscheidung, `herleitung.md`).
- **Jedes Signatur-Element hat Aufgabe und Grenze.** Was es leistet, und wo es aufhört.
- **Tabellen für Werte, Sätze für Haltung.** Rollen, Skalen, Größen gehören in Tabellen; warum etwas so ist, in einen Satz darunter.
- **Do und Don't konkret**, aus echten Befunden und Entscheidungen dieser Marke, nicht aus einer allgemeinen Liste.
- **Kurz.** Ein Kapitel, das niemand zu Ende liest, regelt nichts. Lieber eine Regel weniger als eine, die keiner braucht.
- **Für Leute ohne Design-Erfahrung lesbar.** Fachbegriffe beim ersten Auftreten erklären.

## 2 · Aufbau von `guide.md`

- Keine Titelseite im Markdown: Cover, Inhaltsverzeichnis, Belege-Anhang und Kolophon erzeugt `guide_bauen.py` aus `lauf.json`.
- Jedes Kapitel ist eine Überschrift zweiter Ebene mit Nummer und Kennung: `## 4 · Farbe {#farbe}`. Die Kennung (in geschweiften Klammern) ist in jeder Sprache gleich; daran erkennen Skripte die Pflichtkapitel. Jedes Kapitel beginnt im PDF auf einer neuen Seite.
- Abschnitte als dritte Ebene: `### 4.2 Kontraste`.
- Verweise: `[F12]` (Faktenblatt), `[W3]` (Entscheidung), `[vorläufig: W3]` (nicht vom User entschieden), `(Prinzip 2)`.
- Erlaubt sind normales Markdown (Absätze, Listen, Tabellen, **fett**, *kursiv*, `Code`) und die Kurzbefehle aus Abschnitt 5. Eigenes HTML nur, wenn ein Kurzbefehl nicht reicht.

## 3 · Kern-Kapitel

| Nr. | Kapitel, Kennung | Pflichtinhalt | Typischer Fehler |
|---|---|---|---|
| 0 | Über diesen Guide `{#ueber}` | wofür und für wen; Quellen (Q1 …); Rangfolge bei Widersprüchen (z. B. Markenidentität vor Guide); die vier Design-Skills und **begründete Abweichungen** von ihren Stilregeln; Version und Freigabe | Abweichungen fehlen, obwohl die Marke Stilregeln bricht |
| 1 | Markenkern `{#markenkern}` | die eine Seite aus `markenkern.md` (ohne Interview-Notizen) | Werte, die jede Marke hätte |
| 2 | Gestaltungsprinzipien `{#prinzipien}` | 4–6 Prinzipien, je als `### 2.x <Name>`, zwei bis drei Sätze, dann eine Zeile `Wert: …` | Prinzipien, die nur Werte wiederholen |
| 3 | Logo `{#logo}` | Aufbau, Dateien und Einsatz je Datei, Schutzraum, Mindestgröße (Bildschirm und Druck), Hintergründe, Fehlanwendungen, fremde Logos. Nur vorhandene Dateien; fehlende Originale als offener Punkt | erfundene Varianten, Mindestgrößen ohne Quelle |
| 4 | Farbe `{#farbe}` | Basisfarben mit Herkunft, Rollen je Modus (`{{farbtafel}}`), Anteile je Ansicht, Regel für Verläufe und Deckkraft, Kontrasttabelle (`{{kontrasttabelle}}`), Modi und wann welcher | Farben ohne Rolle; Akzentfarbe als Schrift ohne Kontrastprüfung |
| 5 | Typografie `{#typografie}` | Schriften mit Rolle und **Lizenzstatus**, Skala Web (`{{schriftmuster}}`) und ggf. Druck, Satzregeln (Zeilenlänge, Ausrichtung, Versalien, Hervorhebung, Zahlen, typografische Zeichen der Sprache) | freie Größen, Lizenz ungeklärt |
| 6 | Raster, Raum und Form `{#raster}` | Container, Spalten, Breakpoints, Abstandsreihe (`{{abstaende}}`), Radien (`{{radien}}`), Tiefe (Linie oder Schatten, wofür), Linien | Werte außerhalb der Reihe |
| 7 | Signatur-Elemente `{#signatur}` | 2–5 Elemente, je als `### 7.x <Name>` mit den Zeilen `Aufgabe:`, `Grenze:`, `Herleitung:` und einem Bild | Ornamente ohne Aufgabe |
| 8 | Komponenten `{#komponenten}` | Grundsätze (eine primäre Handlung je Ansicht, welche Karten es gibt und wann), Buttons, Links, Karten, Formulare, Kennzahlen, Zitate; mit Stack die Tabelle der Bausteine im Code | jede Karte eine eigene Optik |
| 9 | Ikonografie `{#ikonografie}` | Stil, Raster, Strich, Farbe, Regeln (nie allein für eine Aussage) | Emojis oder gemischte Icon-Sets |
| 10 | Bildwelt `{#bildwelt}` | Bildarten mit Einsatz und Regeln, „Nie“-Liste aus dem Markenkern (Tabus), Umgang mit KI-Bildern, Formate | allgemeine Stock-Regeln ohne Bezug zur Marke |
| 11 | Bewegung `{#bewegung}` | Ebenen (Seite, Rückmeldung, Schleifen), Dauern und Kurven als Tokens, der eine orchestrierte Moment je Seite (falls die Marke ihn will), reduzierte Bewegung als Pflicht | Bewegung als Deko auf jeder Sektion |
| 12 | Text im Design `{#text}` | Anrede, verbindliche Schreibweisen, Buttons (Verb + Objekt), Zahlen und Einheiten, Füllwörter. Kurzfassung, kein Ersatz für eine Tone-of-Voice | erfundene Tonalität ohne Beleg |
| … | Module (Abschnitt 4) | | |
| n | Checkliste vor dem Livegang `{#checkliste}` | Inhalt, Gestaltung, Zugänglichkeit, Leitplanken; als abhakbare Liste | allgemeine Checkliste ohne Bezug zu den Regeln dieses Guides |
| n+1 | Do und Don't `{#dodont}` | 8–12 Paare aus Befunden und Entscheidungen dieser Marke | Allgemeinplätze |
| n+2 | Pflege und Versionen `{#pflege}` | wer ändert, wie neue Bausteine entstehen, Änderungsverlauf je Version mit Freigabevermerk, Liste der vorläufigen Punkte | fehlt |

Anhang (von `guide_bauen.py`): Anwendungsbeispiele (wenn im Text eingebunden), Token-Übersicht (`{{tokens-uebersicht}}`), Belege, Kolophon mit Absender AI READY.

## 4 · Module je Kanal

Nur die Module, die im Briefing gewählt wurden. Nummern laufen nach Kapitel 12 weiter.

| Modul, Kennung | Pflichtinhalt |
|---|---|
| Web `{#web}` | Seitenmuster (Ablauf einer typischen Seite), Hell und Dunkel (falls beide), Breakpoints in der Praxis, Navigation, Formulare, Leistung (Bildformate, Schriften laden) |
| Druck `{#druck}` | Formate, Ränder in mm, Druckskala in pt, Farben im Druck (RGB-PDF für Bürodrucker, Offset nur mit Proof der Druckerei), Cover, Innenseite, Rückseite, Fußzeile, Dateinamen |
| Social `{#social}` | Formate (1:1, 4:5, 9:16), Logo-Platz, Schrift- und Farbregeln, Textmenge je Bild |
| Präsentationen `{#praesentation}` | Format, Titelfolie, Inhaltsfolie, ein Gedanke je Folie, Schriftgrößen |
| Bewegtbild `{#bewegtbild}` | Formate, Dramaturgie, Mindestschrift, Schlussbild, Untertitel |
| Mail `{#mail}` | Absender, Aufbau, ein Button, Schriften-Ersatz in Mailprogrammen |
| Digitale Formate `{#digital}` | Vorschaubilder (OG 1200 × 630), Favicon, App-Icon, Profilbilder |
| Verpackung und Merch `{#verpackung}` | Materialien, Farben auf Material, Logo-Anwendung, Fertigungsgrenzen (nur mit Belegen) |

## 5 · Kurzbefehle für Tafeln und Bilder

`guide_bauen.py` ersetzt diese Zeilen (jeweils allein in einer Zeile) durch fertige Tafeln aus den Tokens. So stehen Werte nie doppelt im Guide.

| Kurzbefehl | Ergebnis |
|---|---|
| `{{farbtafel}}` | Basisfarben und Rollen als Farbfelder mit Name, Hex, Token, Rolle, je Modus |
| `{{kontrasttabelle}}` | Tabelle aus `tokens/kontrast.md` |
| `{{schriftmuster}}` | jede Stufe der Web-Skala als Muster in ihrer Schrift mit Größe, Gewicht, Zeilenhöhe |
| `{{schriftmuster: druck}}` | dasselbe für die Druckskala |
| `{{abstaende}}` | Abstandsreihe als Balken |
| `{{radien}}` | Radien als Formen |
| `{{tokens-uebersicht}}` | Tabelle aus `tokens/tokens-uebersicht.md` |
| `{{bild: <pfad> \| <Bildunterschrift>}}` | Bild mit Unterschrift, Pfad relativ zum Lauf-Ordner |
| `{{logo: <pfad> \| <hintergrund-rolle>}}` | Logo auf einer Fläche in der genannten Rolle (z. B. `grund`, `akzent`) |
| `{{beispiel: <name>}}` | PNG aus `beispiele/<name>.png` in voller Breite |

## 6 · Layout des Guides in der Marke

Der Guide erscheint in der Gestaltung der Marke: ihre Schriften, ihre Farben, ihre Formen, ihre Signatur. `assets/guide/basis.css` liefert nur die Mechanik (Seitenformat A4 quer, Ränder, Umbrüche, Druckfarben). Alles Sichtbare schreibst du in `guide/marke.css`, nur mit den Variablen aus `tokens.css`:

- **Cover:** Markenname, „Brand & Style Guide“, Version, Datum, Freigabe. Gestalte es wie ein Anwendungsbeispiel der Marke, mit ihrem stärksten Signatur-Element. Klassen: `.cover`, `.cover-marke`, `.cover-titel`, `.cover-meta`.
- **Kapitelanfang:** Nummer und Titel (`.kapitel`, `.kapitel-nr`, `.kapitel-titel`). Hier darf die Marke laut sein, wenn ihr Achsenprofil das hergibt.
- **Fließtext, Tabellen, Tafeln:** ruhig und lesbar; Schriftgrößen aus der Druckskala oder angepasst an A4 quer, nie kleiner als 8 pt für Text.
- **Schriften:** Der Guide braucht die echten Schriftdateien, sonst rendert Chrome eine Ersatzschrift und `render.py pruefen` meldet `schrift_fehlt`. Leg die Dateien unter `guide/schriften/` ab und binde sie in `marke.css` per `@font-face` ein (Pfad relativ zu `guide/`). Lizenzpflichtige Schriften nur aus Dateien des Users. Freie Schriften (OFL) darfst du laden, wenn Netz da ist; sag dem User, woher sie kommen. Ohne Dateien: freie Ersatzschrift für den Entwurf, im Guide als Ersatz gekennzeichnet (Konzept C5).
- Kein Element im Guide verletzt die Regeln, die der Guide selbst aufstellt. Das ist der erste Beweis, dass das System trägt.
