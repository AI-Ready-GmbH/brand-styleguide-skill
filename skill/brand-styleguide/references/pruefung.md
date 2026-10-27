# Prüfung (P7)

Zwei Stufen: Skripte prüfen, was sich zählen lässt. Dann prüft ein Prüfer, der den Guide nicht geschrieben hat, was Urteil braucht. Erst danach geht der Entwurf an den User. Höchstens zwei Überarbeitungsrunden; was danach offen ist, legst du in Runde 3 vor.

## Inhalt
1. Mindeststandards (Klasse K1)
2. Skripte
3. Der Prüfer
4. Prüfliste für den Prüfer
5. Prüfpaket für den claude.ai-Chat
6. Ergebnis

## 1 · Mindeststandards (K1)

Gelten für jede Marke. Abweichung nur als ausdrückliche Entscheidung des Users, sichtbar im Guide.

| Thema | Grenze |
|---|---|
| Kontrast Text | 4,5 : 1 (WCAG 2.2 AA), große Schrift (ab 24 px oder 19 px fett) 3 : 1 |
| Kontrast Grafik | Ränder von Steuerelementen, Fokusring, Icons mit Bedeutung 3 : 1 |
| Schriftgröße | Fließtext mindestens 16 px, Labels mindestens 12 px, Eingabefelder mindestens 16 px |
| Trefferfläche | mindestens 44 × 44 px, Abstand zwischen Treffern mindestens 8 px |
| Fokus | immer sichtbar, nie ohne Ersatz entfernt |
| Tastatur | alles erreichbar, sinnvolle Reihenfolge |
| Bewegung | bei reduzierter Bewegung entfallen Wege, Parallaxe, Schleifen und Zeichnen; Effekte zeigen ihren Endzustand. Zustandswechsel (geöffnet, gewählt, Fehler) bleiben sichtbar, notfalls als kurze Überblendung. Nicht pauschal alles auf 0 setzen, wenn dabei Bedeutung verloren geht |
| Formulare | sichtbares Label über jedem Feld, Fehler am Feld |
| Bilder | Alt-Text für inhaltliche Bilder, Icons nie allein für eine Aussage |

## 2 · Skripte

In dieser Reihenfolge, jeweils Befunde beheben, bevor es weitergeht:

```bash
python3 scripts/tokens.py   <lauf>/tokens/tokens.json
python3 scripts/kontrast.py <lauf>/tokens/tokens.json
python3 scripts/achsen.py   <lauf>
python3 scripts/guide_bauen.py <lauf>
python3 scripts/pruefen.py  <lauf>
python3 scripts/render.py pruefen <lauf>/guide/guide.html
python3 scripts/render.py bogen   <lauf>/guide/guide.html <lauf>/arbeit/05-bogen
```

Lies den Kontaktbogen mit eigenen Augen: Überlappungen, abgeschnittene Texte, leere Seiten, Tafeln ohne Inhalt, ein Cover, das nicht nach der Marke aussieht. Mit Stack zusätzlich die Leitplanken gegen die Bausteine (`stack-next-sanity.md`).

## 3 · Der Prüfer

Ein eigener Agent, der den Gesprächsverlauf nicht kennt. In Claude Code und Cowork startest du ihn als Subagenten. Er bekommt:
- `guide/guide.md`, `tokens/tokens.json`, `tokens/kontrast.md`, `arbeit/03-markenkern.md`, `arbeit/01-fakten.md`, die Ausgaben der Skripte, den Kontaktbogen,
- diese Datei (Abschnitt 4),
- die Kurzfassungen `regeln-*.md` und den Pfad zu `vendor/` zum Nachschlagen (besonders `vendor/impeccable/reference/craft-floor.md`, `critique.md`, `audit.md` und `vendor/web-interface-guidelines/command.md`),
- für den Blindtest das anonymisierte Testpaket und drei Markenkerne (`differenzierung.md`, Abschnitt 3); den Blindtest macht er **zuerst**, bevor er den echten Markenkern liest.

Er antwortet mit `PASS` oder `FAIL` und einer Liste: Kapitel, Problem, Klasse (K1, K2, K3, Herleitung, Fakt, Blindtest), Vorschlag.

Ein Befund zu einer Tatsache (Aussage ohne Beleg, falscher Beleg) wird nie umformuliert, bis er nicht mehr auffällt: Du belegst die Aussage oder streichst sie.

## 4 · Prüfliste für den Prüfer

1. **Blindtest** (zuerst): Welcher der drei Markenkerne gehört zu diesem System? Sicherheit? Woran erkennbar?
2. **Herleitung:** Hat jedes Prinzip einen Wert, jedes Signatur-Element Aufgabe, Grenze, Herleitung? Gibt es Regeln, die genauso im Guide jeder anderen Marke stehen könnten?
3. **Fakten:** Steht jede Aussage über die Marke im Faktenblatt? Stimmen die Verweise?
4. **Mindeststandards:** Kontrasttabelle ohne Verstoß oder mit sichtbar entschiedener Ausnahme? Größen, Trefferflächen, Fokus, reduzierte Bewegung geregelt?
5. **Anti-Patterns** (Impeccable): Karten in Karten, graue Schrift auf farbigen Flächen, Verläufe als Dekoration, Bounce-Easing, Icon-Kacheln über jedem Titel, Effekte auf jeder Sektion und alles weitere aus `craft-floor.md`, soweit es auf diesen Guide und die Beispiele zutrifft.
6. **Technik** (Vercel): Regeln zu Fokus, Formularen, Animation (nur transform/opacity), Bildern, Zahlen und Einheiten in Komponenten und DESIGN.md enthalten?
7. **Widerspruchsfreiheit:** Sagen zwei Kapitel Verschiedenes (z. B. Anteil der Akzentfarbe in 4 und 14)? Hält sich der Guide selbst an seine Regeln (Layout, Beispiele)?
8. **Vollständigkeit:** Alle Pflichtkapitel und gewählten Module da? Vorläufige Punkte gesammelt in Pflege?
9. **Lesbarkeit für Laien:** Versteht jemand ohne Design-Erfahrung, was zu tun ist?
10. **Achsenprofil:** Passt das Ist zum Soll (`achsen.py`)? Wenn nicht: liegt es am System oder am Soll?

## 5 · Prüfpaket für den claude.ai-Chat

Im Chat gibt es keine Subagenten. Damit der Prüfer trotzdem getrennt bleibt:
1. Pack die Dateien aus Abschnitt 3 und das Blindtest-Paket in einen Ordner `pruefpaket/` und als ZIP zum Download.
2. Schreib eine kurze Anleitung `pruefpaket/LIES-MICH.md`: „Neuen Chat öffnen, Skill brand-styleguide ist aktiv, ZIP hochladen, schreiben: ‚Prüfe dieses Prüfpaket nach references/pruefung.md, Blindtest zuerst.‘ Antwort hier einfügen.“
3. Bitte den User darum und warte auf das Ergebnis. Arbeitet der User lieber ohne getrennten Prüfer weiter, prüfst du selbst, sagst aber offen, dass Ersteller und Prüfer dann dieselbe Instanz sind, und vermerkst es in `05-pruefung.md`.

## 6 · Ergebnis (`arbeit/05-pruefung.md`)

```markdown
# Prüfung <Marke>, Runde <1|2>
Skripte: tokens ✓ · kontrast ✓ (0 Verstöße) · achsen ✓ (1 Abweichung, begründet) · pruefen ✓ · render ✓
Prüfer: PASS | FAIL (Agent | Prüfpaket | selbst)
Blindtest: richtig, „eher“, Begründung: …
| Nr. | Kapitel | Problem | Klasse | Vorschlag | erledigt |
```

In Runde 3 nennst du dem User das Ergebnis in drei Zeilen.
