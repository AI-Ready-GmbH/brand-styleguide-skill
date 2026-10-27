# Mitgelieferte Design-Skills: Quellen und Stände

Geladen am 26.10.2026 (Go Max, Konzept 0.2 Abschnitt 11). Aktualisiert wird nur bewusst: neuen Stand laden, Unterschiede lesen, `references/regeln-*.md` abgleichen, hier eintragen.

| Ordner | Quelle | Commit / Stand | Dateien | Lizenz |
|---|---|---|---|---|
| `frontend-design/` | github.com/anthropics/skills, `skills/frontend-design` | `dbd4588f9e1033efb41dad4bef2f7947c8993d44` (09.10.2026) | SKILL.original.md, LICENSE.txt | Apache 2.0 |
| `web-interface-guidelines/` | github.com/vercel-labs/web-interface-guidelines | `434b7f91364665f2f733b310ec54809bf8f37937` (05.10.2026) | command.md, AGENTS.md, LICENSE | MIT |
| `impeccable/` | github.com/pbakaus/impeccable, `.claude/skills/impeccable` | `3671d50f0ac9a662ce0615e85a256110c9cd720b` (25.10.2026) | SKILL.original.md, `reference/` (41 Dateien), `reference/degraded/` (4), LICENSE, NOTICE.md. **Ohne** Programm, Browser-Skripte und Schriftindex (K3) | Apache 2.0 |
| `ui-ux-pro-max/` | lokale Installation `~/.claude/skills/ui-ux-pro-max` (Stand 10.04.2026), Original github.com/nextlevelbuilder/ui-ux-pro-max-skill | Lizenzdatei aus `1f8857914da3c723d58dab1d609dd0d55a86bf51` (26.10.2026) | SKILL.original.md, `data/`, `scripts/`, LICENSE | MIT |

## Was geändert wurde (Apache 2.0, Abschnitt 4b)

Keine Datei in den vier Ordnern ist inhaltlich verändert. Umbenannt: `SKILL.md` → `SKILL.original.md` in drei Ordnern, weil claude.ai und die Skills-API nur eine `SKILL.md` je Skill annehmen. Weggelassen wurden bei Impeccable alle Dateien außerhalb der oben genannten. Die deutschen Kurzfassungen in `references/regeln-*.md` sind eigene Texte mit Quellenangabe, keine Übersetzungen.

## Wie der Skill sie nutzt

Die Originale sind **Nachschlagewerk**, keine Ablaufanweisung für diesen Skill. Der Ablauf folgt `SKILL.md` und `references/`. Aufrufe von Programmen, Befehlen oder Installationen in den Originalen (z. B. `scripts/impeccable`, `install.sh`, Slash-Befehle) gelten hier nicht. Der Prüfer liest die Originale, um Regeln nachzuschlagen.
