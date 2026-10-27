# Entscheidungsrunden

Der User entscheidet, nicht der Skill. Deine Aufgabe ist, Entscheidungen so vorzubereiten, dass sie in Minuten möglich sind: klare Frage, Beleg, wenige Optionen, eine begründete Empfehlung.

## Inhalt
1. Format einer Frage
2. Runde 1: Markenkern und Widersprüche
3. Runde 2: Stilrichtung
4. Runde 3: Freigabe
5. Für Leute ohne Design-Erfahrung
6. Antworten verarbeiten

## 1 · Format einer Frage

```markdown
**W2 · Akzentfarbe als Schrift**
Das Orange der Marke (#E07B39) erreicht als Schrift auf Weiß nur 2,9 : 1 [F6]. Lesbar ist Schrift ab 4,5 : 1.
- a) Orange bleibt Schrift, wir nehmen schlechte Lesbarkeit in Kauf (gegen den Mindeststandard, wird im Guide vermerkt)
- b) Orange nur für Flächen, Linien und Icons; für Schrift eine dunklere Fassung desselben Orange (#A8501A, 5,1 : 1)
- c) Schrift immer in der Textfarbe, Orange nur als Fläche
**Empfehlung b:** Das Orange bleibt überall erkennbar, und Texte sind lesbar.
```

- **Nummern** je Runde mit Buchstaben: M (Markenkern), W (Widerspruch), S (Stilrichtung), F (Freigabe), V (vorläufig). Sie bleiben über den ganzen Lauf gleich.
- **Belege** in eckigen Klammern aus dem Faktenblatt. Bei Gestaltungsfragen ein Bildausschnitt (Screenshot aus der Messung oder Tafel).
- **Zwei bis vier Optionen.** Eine Option darf „so lassen“ sein, wenn das ehrlich eine Option ist.
- **Empfehlung mit einem Satz Grund**, in Alltagssprache.
- **Höchstens etwa zehn Fragen je Runde.** Bündle Kleinkram („W7–W9: Schreibweisen wie in der Website, ok?“).
- Am Ende: „Antwort gern knapp, z. B. ‚W2 b, Rest wie empfohlen‘.“

## 2 · Runde 1: Markenkern und Widersprüche (nach P4)

Inhalt: der Markenkern als eine Seite zum Bestätigen (M1: stimmt das so?), das Soll-Achsenprofil in Worten (M2), die Widersprüche aus der Auswertung (W …), offene Fakten (z. B. fehlende Logo-Originale). Reihenfolge: zuerst, was das System am stärksten prägt (Werte, Farbe, Schrift), dann Details.

## 3 · Runde 2: Stilrichtung (nach P5)

Inhalt: 2–3 Bildtafeln, je Richtung zwei bis drei Sätze, was sie ausmacht, ihr Achsenprofil im Vergleich zum Soll, und welche Werte sie wie umsetzt.

```markdown
**S1 · Welche Richtung?**
- a) **„Werkstatt“** (nah am Bestand): … [Tafel a]
- b) **„Lichtung“** (mutiger): … [Tafel b]
- c) Kombination, z. B. Schrift aus a, Farbe aus b
**Empfehlung a**, weil …
```

Kombiniert der User, prüf die Kombination (Kontrast, Achsenprofil, passt die Signatur noch?) und sag in einem Satz, was dabei bricht, bevor du ausarbeitest.

## 4 · Runde 3: Freigabe (nach P7)

Inhalt: das PDF des Guides und der Anwendungsbeispiele, das Ergebnis der Prüfung in drei Zeilen, die vorläufigen Punkte (V1 …) mit der Bitte, sie zu entscheiden, und die Frage nach der Freigabe:

```markdown
**F1 · Freigabe:** Gibst du den Guide als Version 1.0 frei? Falls ja: Name und Rolle für den Freigabevermerk.
```

## 5 · Für Leute ohne Design-Erfahrung

- Kein Fachbegriff ohne Erklärung in derselben Zeile: „Kontrast (wie gut sich Schrift vom Hintergrund abhebt)“.
- Zeig statt zu beschreiben: Ausschnitt aus der Messung, kleine Tafel, Vorher/Nachher.
- Erklär Folgen, nicht Theorie: „Mit a ist der Button auf dem Handy kleiner als ein Daumen.“
- Frag nie nach Werten („Welcher Radius?“), sondern nach Wirkung mit Bild („eher weich wie b oder klar wie c?“).

## 6 · Antworten verarbeiten

- Trag jede Antwort sofort in `lauf.json` ein.
- „Wie empfohlen“ für eine Frage zählt als Entscheidung des Users, nicht als vorläufig.
- „Mach du“ oder keine Antwort auf eine Frage: Empfehlung einsetzen, `vorlaeufig: true`, im Guide `[vorläufig: W4]`.
- Widerspricht eine Antwort einem Mindeststandard, sag einmal klar, was das bedeutet, und übernimm sie dann, wenn der User dabei bleibt. Im Guide steht dann bei der Regel: „Abweichung vom Mindeststandard, entschieden von … am …“. In `lauf.json` trägst du sie unter `ausnahmen_k1` ein (`{"paar": "akzent-text/grund", "modus": "hell", "entscheidung": "W2"}`), damit die Prüfung sie als entschieden erkennt.
- Wirft eine Antwort eine neue Frage auf, stell sie in einer kurzen Zusatzrunde, statt sie selbst zu beantworten.
