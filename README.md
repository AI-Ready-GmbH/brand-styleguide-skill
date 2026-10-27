# brand-styleguide · Skill für Brand & Style Guides

Ein Agent Skill von AI READY: Er erstellt für eine Marke einen kompletten Brand & Style Guide als eigenes Design System. Aus Website, Logo und vorhandenen Vorgaben entstehen ein Guide im Layout der Marke (PDF), Design Tokens, Bausteine für Next.js, Tailwind und Sanity sowie eine `DESIGN.md` für Claude Code. Widersprüche in den Quellen entscheidet der User, nicht der Skill.

**Stand: v0.1.0, Testversion (27.10.2026).** Intern, nicht weitergeben.

## Installieren

**Claude Code** (empfohlen, hier läuft alles: Website messen, PDF rendern, getrennter Prüfer):

```bash
git clone https://github.com/AI-Ready-GmbH/brand-styleguide-skill.git
ln -s "$(pwd)/brand-styleguide-skill/skill/brand-styleguide" ~/.claude/skills/brand-styleguide
```

Danach Claude Code neu starten. Voraussetzungen: Python 3.9 oder neuer (ohne Zusatzpakete), Google Chrome für Messung und PDF. Ohne Chrome läuft der Skill auch, liest die Website dann aus dem Quelltext und bittet um Screenshots.

**Claude Desktop oder claude.ai:** die Datei `brand-styleguide.skill` aus dem [Release](https://github.com/AI-Ready-GmbH/brand-styleguide-skill/releases) laden und unter Einstellungen → Skills hochladen. Dort gibt es keine Subagenten und oft keinen Browser: Der Skill schnürt dann für die Prüfung ein Prüfpaket, das in einem neuen Chat geprüft wird, und liefert den Guide als HTML zum Speichern als PDF. Diese Wege sind noch nicht getestet.

## Benutzen

Einfach beschreiben, was gebraucht wird, zum Beispiel:

> Erstelle einen Brand & Style Guide für unsere Marke Beispiel GmbH. Website: https://beispiel.de. Das Logo und unser altes CI-Handbuch liegen im Ordner.

Gut vorzubereiten:
- die Website-URL,
- das Logo als Vektordatei (SVG, PDF, EPS oder AI),
- vorhandene Vorgaben (Styleguide, CI-Handbuch, Präsentationen, Druckstücke), auch wenn sie alt oder widersprüchlich sind,
- wer den Guide freigibt.

Der Skill fragt zuerst ein kurzes Briefing ab und legt danach drei kurze Entscheidungsrunden vor: Markenkern und Widersprüche, Stilrichtung als Bild, Entwurf als PDF zur Freigabe. Wer keine Zeit für Rückfragen hat, schreibt „mach alles im Autopilot“. Dann setzt der Skill seine Empfehlungen ein und markiert sie im Guide sichtbar als vorläufig. Ein vollständiger Lauf dauert etwa eine Stunde.

Ergebnis: ein Lauf-Ordner (Ablageort fragt der Skill) mit `guide/` (PDF, HTML, Markdown), `tokens/`, `code/`, `DESIGN.md`, `PRODUCT.md`, `beispiele/` und den Arbeitsdateien in `arbeit/` (Faktenblatt mit Fundstellen, Auswertung, Stilrichtungen, Prüfbericht).

## Bekannte Grenzen von v0.1

- Das PDF fließt als Text und wird lang (Test AI READY: 72 Seiten). Seiten je Thema, Status je Regel und ein Zielumfang sind für v0.2 vorgeschlagen.
- Claude Desktop und claude.ai sind noch nicht getestet (Plattformtest offen).
- ESLint und TypeScript-Prüfung der Bausteine laufen nur in einem Repo mit installierten Paketen.
- Cookie-Banner der gemessenen Website erscheinen auf den Screenshots.

Rückmeldungen bitte an Max Kleinsorg: was gut war, wo der Skill unklar geführt hat, was im Guide fehlt oder falsch ist.

## Aufbau

| Ordner | Inhalt |
|---|---|
| `skill/brand-styleguide/` | der Skill: `SKILL.md`, `references/`, `scripts/`, `assets/`, `vendor/` |
| `skill/brand-styleguide/evals/` | Testfälle (nicht Teil des installierten Skills) |
| `docs/` | Konzept 0.2, Abweichungen beim Bau, Recherche zu den Plattformen |

Rauchtest der Skripte (aus `skill/brand-styleguide/`): `python3 -B scripts/tests/rauchtest.py`

## Lizenzen

Der Skill ist von AI READY. In `vendor/` liegen vier Design-Skills unter eigener Lizenz (Apache 2.0 und MIT), Quellen und Stände in `skill/brand-styleguide/vendor/VERSIONEN.md`.
