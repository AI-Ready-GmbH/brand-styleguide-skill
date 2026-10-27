# Differenzierung: kein Einheitssystem

Das größte Risiko dieser Aufgabe: Jede Marke bekommt dasselbe gefällige System (ruhige Fläche, eine Akzentfarbe, serifenlose Schrift, mittlere Rundung, Karten mit dünner Linie) in anderen Farben. Fünf Werkzeuge arbeiten dagegen: Achsenprofil, echte Stilrichtungen, Blindtest mit Ablenkern, Abgleich mit anderen Läufen und die Katalog-Bremse.

## Inhalt
1. Achsenprofil
2. Stilrichtungen (P5)
3. Blindtest mit Ablenkern (P7)
4. Abgleich mit anderen Läufen und Wettbewerbern
5. Katalog-Bremse

## 1 · Achsenprofil

Acht Achsen, je Stufe 1 bis 5. Stufe 1 ist der linke Pol, 5 der rechte.

| Achse (Schlüssel) | 1 | 5 | Wie `achsen.py` misst (Näherung) |
|---|---|---|---|
| `hell_dunkel` | hell | dunkel | Helligkeit von `grund` im Standardmodus |
| `kuehl_warm` | kühl | warm | Farbtemperatur von `grund`, `flaeche`, `text` (Gelb-Blau-Achse im Lab-Raum) |
| `zurueckhaltend_farbig` | zurückhaltend | farbig | Zahl der deutlich bunten Basisfarben und ihre Sättigung |
| `eckig_rund` | eckig | rund | `radius.karte` |
| `luftig_dicht` | luftig | dicht | größter Abstand der Reihe und Zeilenhöhe des Fließtexts |
| `leise_laut` | leise | laut | Verhältnis `display` zu `text`, Gewicht der Titelschrift |
| `sachlich_verspielt` | sachlich | verspielt | nicht messbar, wird mit Begründung in `$marke.achsen_ist` eingetragen |
| `still_lebendig` | still | lebendig | längste Dauer in `bewegung.dauer`, überschreibbar mit Begründung |

- **Soll** entsteht im Markenkern (P4), wird in Runde 1 bestätigt und steht in `lauf.json`.
- **Ist** misst `python3 scripts/achsen.py <lauf>` aus den Tokens. Weicht eine Achse um mehr als eine Stufe vom Soll ab, ist das ein Befund. Entweder passt das System nicht zur Marke, oder das Soll war falsch; beides gehört in die nächste Runde, nicht in eine stille Korrektur.
- Die Messung ist eine Näherung. Wo sie offensichtlich danebenliegt (z. B. eine dunkle Signaturfläche auf heller Seite), überschreibst du den Wert in `$marke.achsen_ist` mit Begründung.

## 2 · Stilrichtungen (P5)

Zwei bis drei Richtungen, bevor ausgearbeitet wird.

- **„Nah am Bestand“:** behält, was laut Auswertung trägt, ordnet den Rest zu einem System. Für Marken mit gutem Bestand oft die Empfehlung.
- **„Mutiger“:** setzt den Markenkern konsequenter um: zwei bis drei Achsen weiter Richtung des Pols, den der Markenkern nahelegt, oder ein stärkeres Signatur-Element aus dem Markenmaterial.
- **Optional eine dritte**, wenn der Markenkern zwei Lesarten zulässt.

Regeln:
- Die Richtungen unterscheiden sich auf **mindestens drei Achsen** um mindestens eine Stufe. Sonst sind es keine Richtungen, sondern Varianten.
- Jede Richtung hat einen Namen aus der Welt der Marke (kein „Modern“, „Klassisch“), zwei bis drei Sätze, ihr Achsenprofil und ihre Herleitung (welche Werte sie wie umsetzt).
- Jede Richtung ist eine vollständige Mini-Token-Datei (`arbeit/04-richtungen/<name>.tokens.json`, Format wie `tokens.md`, Pflicht-Tokens genügen) plus eine kleine CSS-Datei für ihr Signatur-Element. Gerendert wird mit der Tafel `assets/richtungen/tafel.html` (Anleitung im Kopf der Datei): gleicher Inhalt für alle Richtungen, damit man nur die Gestaltung vergleicht.
- Haltung aus `regeln-frontend-design.md`: Entscheide dich je Richtung klar, statt alle Richtungen in die Mitte zu ziehen. Anti-Patterns aus `regeln-impeccable.md` gelten schon hier.
- Leg je Richtung `kontrast.py` und `achsen.py` an, bevor du sie zeigst. Eine Richtung, die Mindeststandards verletzt, zeigst du nicht.

## 3 · Blindtest mit Ablenkern (P7)

Prüft in jedem Lauf, ob das System erkennbar zu genau dieser Marke gehört.

1. **Ablenker:** Ein eigener Agent (in Claude Code und Cowork ein Subagent) schreibt zwei erfundene, plausible Markenkerne aus derselben Branche und für eine ähnliche Zielgruppe. Sie sollen **nah dran** sein: gleiche Branche, ähnliche Größe, ähnliches Angebot, aber andere Werte und Persönlichkeit, sodass ihr Soll-Achsenprofil auf zwei bis vier Achsen um eine bis zwei Stufen abweicht. Weit entfernte Ablenker machen den Test wertlos. Er bekommt dafür den echten Markenkern und das Format aus `markenkern.md`. Keine Karikaturen: Die Ablenker müssen echte Marken sein können.
   **Alle drei Kerne für den Prüfer ohne Gestaltung:** Für den Test kürzt du jeden Kern (auch den echten) auf Werte, Persönlichkeit, Zielgruppe, Positionierung und Ton. Streiche Abschnitt „Herkunft und Material“, Farben, Schriften, Formen, Signaturen, Claims und Markennamen. Sonst erkennt der Prüfer die Marke am wiederholten Wort statt am System.
2. **Anonymisieren:** Erzeuge ein Testpaket ohne Name, Logo, Claim und wörtliche Zitate: die Farbtafel, die Schriftmuster, die Signatur-Elemente mit Aufgabe und Grenze (ohne Herleitung), die Musterseite als PNG mit ausgeblendetem Logo und Platzhaltertexten (`render.py png … --modus …` auf `beispiele/musterseite.html?blindtest=1`, siehe Kopf der Vorlage). Prinzipien ohne die Zeile `Wert:`.
3. **Prüfen:** Der Prüfer (ein anderer Agent als der Ersteller und der Ablenker-Schreiber) bekommt das Testpaket und die drei Markenkerne in zufälliger Reihenfolge (A, B, C). Er nennt, zu welchem Markenkern das System gehört, mit Begründung aus konkreten Merkmalen und einer Sicherheit (sicher, eher, geraten).
4. **Bewerten:** richtig und „sicher“ oder „eher“ = bestanden. Falsch oder „geraten“ = Befund: Das System ist nicht eigen genug. Die Begründung des Prüfers sagt meist, woran es liegt (z. B. „A und C könnten beide diese Palette haben“). Überarbeite das, nicht den Test. Stützt sich die Begründung vor allem auf ein Wort, das im Kern und im System gleich vorkommt, war die Anonymisierung undicht: Kerne nach Schritt 1 neu kürzen und den Test wiederholen.

Im claude.ai-Chat ohne Subagenten gehört der Blindtest ins Prüfpaket für einen neuen Chat (`pruefung.md`).

## 4 · Abgleich mit anderen Läufen und Wettbewerbern

- Liegen im Ablageort weitere Läufe, vergleiche ihr `achsen_soll`, die Ist-Profile, die Rollenfarben (`akzent`, `handlung`, `grund`) und die Signatur-Elemente. Zeigen sieben oder acht Achsen dieselbe Stufe und die Akzentfarben sind kaum unterscheidbar, ist das ein Befund für Runde 3.
- Hat der User Wettbewerber genannt, miss deren Startseite mit `messen.py` und leite ein grobes Profil ab. Das System der Marke soll sich vom Wettbewerb unterscheiden, wo der Markenkern Abgrenzung verlangt, oder es nennt den Grund für die Nähe.

## 5 · Katalog-Bremse

Die Kataloge von ui-ux-pro-max (Paletten, Schriftpaare, Stile, Produkttypen) sind verführerisch, weil sie schnell gute Ergebnisse liefern. Gerade deshalb führen sie zum Einheitssystem.

- Reihenfolge: zuerst der Bestand der Marke, dann Material aus dem Markenkern, erst dann der Katalog.
- Höchstens zwei Kandidaten je Frage aus dem Katalog, beide mit Herleitung (welcher Wert, welches Merkmal), und als Kandidaten gekennzeichnet.
- Im Guide steht jede Übernahme mit `Katalog: <Datei/Eintrag>, gewählt weil …`.
- Für neue Marken ohne Bestand ist der Katalog als Ideengeber erlaubt, die Herleitungspflicht gilt trotzdem.
- Abfrage: siehe `regeln-ui-ux-pro-max.md`.
