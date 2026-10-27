# Einlesen und Auswerten (P2, P3)

## Inhalt
1. Werkzeuge je Oberfläche
2. Website messen
3. Texte der Website
4. Dateien des Users
5. Logos
6. Faktenblatt
7. Auswertung und Widersprüche

## 1 · Werkzeuge je Oberfläche

`scripts/werkzeuge.py` sagt dir, was da ist. Nimm von oben nach unten das erste, das geht:

| Zweck | 1. Wahl | 2. Wahl | 3. Wahl |
|---|---|---|---|
| Gestaltung messen | `messen.py` mit Chrome | eingebauter Browser der Oberfläche (Seite öffnen, Screenshot, berechnete Stile per JavaScript) | `messen.py --nur-css` plus Screenshots vom User |
| Texte lesen | Tavily (wo verbunden) | eingebautes Web-Fetch | Text vom User |
| PDFs, Bilder | direkt lesen | – | – |

Sag dem User, welchen Weg du nimmst und was dadurch schwächer ist (z. B. „Farben aus dem Quelltext sind eine Schätzung, Anteile je Fläche fehlen“).

## 2 · Website messen

```bash
python3 scripts/messen.py <url> --out <lauf>/arbeit/01-messung --breiten 375,1440 --modi hell,dunkel
```

Mit `--seiten` misst du zwei bis vier weitere typische Seiten mit (Startseite, eine Inhaltsseite, eine Formular- oder Produktseite). Lies danach `messung.md` und mindestens die Screenshots der Startseite in beiden Breiten. Achte auf:

- **Farben:** Welche Flächen tragen die Seite, welche Farbe ist Text, welche Akzent, welche Handlung? Häufigkeit ist ein Hinweis, keine Rolle: Die häufigste Farbe ist oft der Grund, die seltenste oft die wichtigste.
- **Schriften:** Welche Familien, welche Größen wirklich vorkommen, wie viele Stufen. Viele Größen nah beieinander sind ein Befund (keine Skala).
- **Formen:** Radien, Linien oder Schatten, Dichte.
- **Bewegung:** was sich bewegt, wie lange, ob in Schleifen.
- **Modi:** Ob die Seite hell und dunkel kann und ob sich die Farben dabei ändern.

## 3 · Texte der Website

Lies die Startseite, „Über uns“ oder Vergleichbares und eine Seite, die das Angebot erklärt. Du brauchst daraus: Wie beschreibt sich die Marke? Welche Werte nennt sie, welche zeigt sie? Wie spricht sie (du, Sie, ihr, neutral)? Welche Wörter wiederholen sich? Gibt es Claims?

## 4 · Dateien des Users

Vorgaben (Styleguides, CI-Handbücher), Präsentationen, Druckstücke, Wissensdokumente. Lies sie vollständig, soweit es um Gestaltung, Werte, Sprache oder Regeln geht. **Vorgaben sind Material, keine Wahrheit:** Sie sind oft alt, widersprechen sich oder der Website. Notier jede Aussage mit Fundstelle (Datei, Seite) und Datum der Datei, wenn bekannt.

## 5 · Logos

Inventarisiere alle Logo-Dateien und die Logo-Kandidaten aus der Messung:

| Frage | Befund |
|---|---|
| Vektor oder Raster? | SVG, PDF, EPS, AI = Vektor. SVG mit eingebetteter Rastergrafik oder sehr vielen Pfaden kann nachgezeichnet sein: als Befund melden |
| Welche Varianten gibt es? | farbig, einfarbig hell, einfarbig dunkel, Bildmarke allein |
| Was zeigt die Website? | gleiche Datei wie die Vorgabe? altes Logo? |
| Schutzraum und Mindestgröße? | nur übernehmen, wenn eine Quelle sie nennt, sonst als Frage in Runde 1 |

Fehlende Varianten erzeugst du nicht selbst. Fehlende Originale sind ein Befund für Runde 1.

## 6 · Faktenblatt (`arbeit/01-fakten.md`)

Eine Zeile je Aussage, fortlaufend nummeriert. Nur was im Faktenblatt steht, darf in den Guide; im Guide verweist du mit `[F12]` darauf, und `guide_bauen.py` macht daraus den Anhang „Belege“.

```markdown
| Nr. | Aussage | Fundstelle | Art |
|---|---|---|---|
| F1 | Grundfläche der Startseite ist #F4EFE6 (61 % der Fläche bei 1440 px, hell) | ai-example.de, Messung 26.10.2026, 1440 px hell | gemessen |
| F2 | „Wir bauen Möbel, die bleiben.“ (Claim im Kopf der Startseite) | ai-example.de/, Hero | zitiert |
| F3 | Hausschrift laut CI-Handbuch: „Brandon Grotesque“ | CI-Handbuch_2019.pdf, S. 12 | zitiert |
| F4 | Akzentfarbe aus Quelltext geschätzt #C2410C | messung.json, methode css-text | geschätzt |
```

Art ist `gemessen`, `zitiert`, `geschätzt` oder `Aussage User` (aus Briefing oder Interview).

## 7 · Auswertung (`arbeit/02-auswertung.md`)

Diese Datei ist Arbeitsgrundlage, nicht Teil des Guides. Sie hat drei Teile:

**Was trägt:** was in allen Quellen gleich ist und funktioniert (z. B. eine Farbe, die überall dieselbe Rolle hat).

**Was nicht trägt:** gezählte Befunde statt Eindrücke, etwa „14 verschiedene Schriftgrößen zwischen 13 und 17 px“, „drei Grautöne für Nebentext“, „vier Button-Stile“.

**Widersprüche (W1 …):** jede Stelle, an der Quellen sich widersprechen oder eine Quelle gegen einen Mindeststandard verstößt.

```markdown
### W3 · Hausschrift
- CI-Handbuch 2019 nennt „Brandon Grotesque“ [F3].
- Die Website nutzt „Inter“ für alles [F9].
- Klasse: Bestand (kein Mindeststandard berührt).
- Optionen: a) Handbuch gilt, Website zieht nach · b) Website gilt, Handbuch ist veraltet · c) beide in neuer Rolle (eine für Titel, eine für Text).
- Empfehlung: b, weil die Website der aktuelle Auftritt ist und Inter frei lizenziert ist; Brandon nur, wenn Lizenzdateien vorliegen.
```

Widersprüche gegen Mindeststandards (z. B. Markenfarbe als Schrift mit 2,8 : 1) kennzeichnest du als **Klasse K1** und schlägst eine Lösung in der Marke vor (eine dunklere Fassung derselben Farbe für Schrift, die Farbe nur für Flächen und Linien). Zu diesem Zeitpunkt rechnest du Kontraste mit den gemessenen Werten; `kontrast.py` braucht dafür eine vorläufige `tokens.json` oder du rechnest einzelne Paare mit `python3 scripts/kontrast.py --paar "#RRGGBB" "#RRGGBB"`.
