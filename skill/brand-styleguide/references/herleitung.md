# Herleitung: von den Werten zur Regel

Jede Regel im Guide muss sich bis zu einem Markenwert, einem Befund oder einer Entscheidung zurückführen lassen. Das ist der wichtigste Schutz gegen das Einheitssystem: Eine Regel, die zu jeder Marke passen würde, hat keine Herleitung aus dieser Marke, und der Prüfer streicht sie.

## Inhalt
1. Die Kette
2. Gestaltungsprinzipien aus Werten
3. Signatur-Elemente aus Markenmaterial
4. Wie Herleitung im Guide steht
5. Was keine Herleitung braucht

## 1 · Die Kette

```
Markenwert (Markenkern)  →  Gestaltungsprinzip (Kapitel 2)  →  Regel mit Zahl und Grenze (Kapitel 3–14)
Befund (Faktenblatt)     ↗
Entscheidung (W/S …)     ↗
Markenmaterial (Herkunft, Logo, Produkt)  →  Signatur-Element (Kapitel 7)
```

## 2 · Gestaltungsprinzipien aus Werten (P5)

Vier bis sechs Prinzipien. Jedes Prinzip:
- übersetzt einen Wert in eine Haltung für Gestaltung, nicht in eine Wiederholung des Werts („Ehrlich“ → „Material zeigt sich, wie es ist: Fotos ohne Filter, Flächen ohne Verläufe“),
- ist prüfbar: Man kann an einer Ansicht sagen, ob sie dem Prinzip folgt,
- nennt den Wert, aus dem es kommt (`Wert: <Name>`),
- passt nicht wortgleich zu jeder anderen Marke. Test: Würde das Prinzip im Guide eines Wettbewerbers genauso stehen? Dann ist es zu allgemein.

Prinzipien, die fast jede Marke hätte (Lesbarkeit, Einheitlichkeit über Kanäle), gehören nicht in Kapitel 2. Sie sind Mindeststandard bzw. Ziel jedes Guides und stehen in der Checkliste.

## 3 · Signatur-Elemente aus Markenmaterial

Ein Signatur-Element ist das, woran man die Marke ohne Logo erkennt. Es kommt **aus dem, was die Marke schon hat**, nicht aus einem Katalog von Gestaltungsideen:

| Material | Wie daraus eine Signatur werden kann |
|---|---|
| Logoform | eine Linie, Ecke, Kurve oder ein Winkel aus dem Zeichen als wiederkehrendes Formelement |
| Herkunft, Ort | Farbe, Textur oder Raster aus dem Ort, der Region, dem Gebäude |
| Produkt, Handwerk | ein Detail des Produkts als grafisches Motiv; Maße, Raster, Materialien |
| Sprache | ein wiederkehrendes Satzmuster, eine Hervorhebung, eine Zählweise |
| Bestand | was auf der Website oder in Vorgaben schon wiedererkennbar ist und trägt |

Je Signatur-Element im Guide: **Aufgabe** (was es leistet), **Grenze** (wo und wie oft es vorkommt, wo nie), **Herleitung** (Material und Beleg). Zwei bis fünf Signatur-Elemente reichen; mehr verwässert.

## 4 · Wie Herleitung im Guide steht

- Prinzipien: Zeile `Wert: <Name>` unter jedem Prinzip.
- Signatur-Elemente: Zeilen `Aufgabe:`, `Grenze:`, `Herleitung:`.
- Regeln in Kapitel 3–14: am Ende in Klammern das Prinzip (`(Prinzip 2)`), der Beleg (`[F12]`) oder die Entscheidung (`[W3]`).
- Übernahmen aus dem Katalog von ui-ux-pro-max: `Katalog: <Quelle>, gewählt weil …`.
- Abweichungen von Stilregeln der vier Design-Skills: in Kapitel 0 mit Grund.

`pruefen.py` prüft, dass jedes Prinzip einen Wert, jedes Signatur-Element Aufgabe, Grenze und Herleitung hat und dass jeder Verweis `[F…]` im Faktenblatt existiert.

## 5 · Was keine Herleitung braucht

Mindeststandards (Kontrast, Größen, Trefferflächen, Fokus, reduzierte Bewegung) und Handwerksregeln (z. B. nur `transform` und `opacity` animieren, Links als Links). Sie stehen mit Verweis auf die Kurzfassung des jeweiligen Design-Skills im Guide.
