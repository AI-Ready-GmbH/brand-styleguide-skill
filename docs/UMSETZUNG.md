# Umsetzung: was beim Bauen vom Konzept 0.2 abweicht oder dazukam

Stand 26.10.2026. Nichts davon ändert eine Entscheidung von Max; es sind technische Folgen oder Präzisierungen.

| Nr. | Thema | Was | Grund |
|---|---|---|---|
| U1 | `SKILL.md` der Design-Skills | In `vendor/` heißen sie `SKILL.original.md` | claude.ai und die Skills-API nehmen nur eine `SKILL.md` je Skill an |
| U2 | Schriftstufe Fließtext | heißt `fliesstext`, nicht `text` | in Tailwind v4 erzeugen Farbe `text` und Stufe `text` sonst dieselbe Klasse `text-text` |
| U3 | Konfliktklassen | K1 Mindeststandard, K2 Stil, **K3 Handwerk** (technische Sauberkeit ohne Grenzwert, z. B. nur transform/opacity animieren). Widersprüche der Skills untereinander: K1 vor K3 vor K2, sonst Herleitung oder Frage | Konzept 4.2 hatte als Klasse 3 „Widersprüche der Skills untereinander“; in den Quellen gibt es viele Regeln, die weder Barrierefreiheit noch Geschmack sind |
| U4 | Hausprofil | Schnappschuss ohne Mail-Adressen und Ablage-IDs, Namen bleiben; erneuert mit `scripts/profil.py` | Datensparsamkeit, für Freigabevermerke reichen Namen |
| U5 | Impeccable | nur Regeltexte, kein Programm; Hinweis in `vendor/VERSIONEN.md`, dass Befehle der Originale nicht gelten | K3, Plattformneutralität |
| U6 | ui-ux-pro-max | Abfrage mit `python3 -B vendor/ui-ux-pro-max/scripts/search.py … --domain …` (`-B` verhindert Cache-Dateien im Skill) | geprüft 26.10. |
| U7 | Kontrast-Ausnahmen | in `lauf.json` unter `ausnahmen_k1`, damit die Prüfung entschiedene Abweichungen erkennt | Prüfbarkeit |
| U8 | Guide-Bau | `guide.md` mit Kapitel-Kennungen `{#farbe}` und Kurzbefehlen `{{farbtafel}}` usw.; `guide_bauen.py` erzeugt Cover, Inhalt, Belege-Anhang und Kolophon | Werte stehen nie doppelt im Guide; Prüfung unabhängig von der Sprache |

## Befunde aus den Quellen (Auswertung der vier Skills)

- Impeccable verbietet Eyebrows absolut und auch als Regel in `DESIGN.md`. Bei uns K2: Die Marke darf sie haben, mit Begründung.
- Vercel erlaubt nur `transform` und `opacity` für Animation, Impeccable mehr. Bei uns K3 nach Vercel, Ausnahme mit Begründung.
- Kontrast: Vercel bevorzugt APCA, ui-ux-pro-max lässt Nebentext im Dunkelmodus mit 3 : 1 zu. Bei uns gilt WCAG 2.2 AA (4,5 : 1 für jeden Text).
- Trefferflächen 24, 44 oder 48 px je nach Quelle; bei uns 44 px.
- `DESIGN.md` nach Impeccable braucht exakt die englischen Abschnittsüberschriften; unsere Zusätze (Mindeststandards, Checkliste) hängen danach.
- ui-ux-pro-max: 32 von 73 Schriftpaaren enthalten Schriften, die Impeccable als typische KI-Standardschriften führt. Das bestätigt die Katalog-Bremse.
