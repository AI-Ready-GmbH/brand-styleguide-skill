# Plattformen: was ein Skill wo kann

> Recherche 23.10.2026 aus offizieller Doku (Anthropic, Claude Help Center, agentskills.io). B = belegt, U = unklar. Grundlage für Abschnitt 9 des Konzepts.

CC = Claude Code · CW = Cowork (Desktop) · Web = claude.ai-Chat (Web und Desktop-Chat) · API = Claude-API mit Skills

| | CC | CW | Web | API |
|---|---|---|---|---|
| Bereitstellen | Ordner `~/.claude/skills/`, `.claude/skills/`, Plugin, Enterprise-managed (B) | ZIP-Upload unter Customize > Skills, org-weit „Publish to org“ durch Owner (B) | wie CW (B) | `/v1/skills`, Workspace, unter 30 MB (B) |
| Skripte | alles Lokale (B) | VM auf dem Rechner (B), Laufzeiten U | Sandbox Python oder JavaScript (B), Node-Version U | Python 3.11, feste Bibliotheken (B) |
| Pakete installieren | ja (B) | nur mit Netz | nur mit Netz (B) | nein (B) |
| Netz | voll (B) | Einstellung der Org; aus = nur anthropic.com, claude.com (B) | vier Stufen: aus, Paketmanager, einzelne Domains, alle (B) | keins (B) |
| Browser | lokaler Chrome; WebFetch, WebSearch (B), Playwright/Puppeteer zu testen | eingebauter Browser bzw. Claude in Chrome; Web-Fetch/Suche außerhalb der Netz-Regeln (B); Headless in VM U | Websuche (B), Browser in der Sandbox U | keiner (B) |
| Subagent (Prüfer) | ja: Agent-Tool, `.claude/agents/`, `context: fork` (B) | ja, Plugin-Agents (B); `context: fork` U | nein, Plugin-Agents werden ignoriert (B) | nur Agent SDK / Managed Agents |
| Ergebnisdateien | Arbeitsordner | verbundene Ordner, Standard `~/Claude` (B) | Download oder Drive, max. 30 MB je Datei (B) | Files API |

**Übertragbarkeit des Skill-Ordners**
- Agent Skills ist ein offener Standard (agentskills.io).
- Außerhalb von CC gelten nur die Frontmatter-Felder `name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`. `context: fork`, `agent` und Befehls-Einschübe wirken nur in CC.
- `${CLAUDE_SKILL_DIR}` wird nur in CC und CW ersetzt; im Chat liegt der Ordner in der Sandbox, deshalb zusätzlich relative Pfade.
- Länge der `description`: Doku 1.024 Zeichen, Help-Artikel 200. Unter 200 bleiben.
- Die Oberflächen gleichen Skills nicht untereinander ab.

**Nur ein Test klärt**
1. Node (Version) in Chat-Sandbox und CW-VM
2. Playwright/Chromium in Chat und CW installierbar und startbar
3. HTML zu PDF in Chat (pdfkit ist vorinstalliert, Renderer unklar)
4. Größengrenze eines Skill-ZIPs auf claude.ai
5. `context: fork` in Cowork
6. Cowork-Modus und Netzstufe in der falkemedia-Org

**Quellen**
- https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- https://code.claude.com/docs/en/skills
- https://support.claude.com/en/articles/12512180-using-skills-in-claude
- https://claude.com/docs/skills/how-to.md
- https://claude.com/docs/plugins/platform-support.md
- https://support.claude.com/en/articles/12111783-create-and-edit-files-with-claude
- https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool
- https://platform.claude.com/docs/en/build-with-claude/skills-guide
- https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork
- https://claude.com/docs/cowork/hipaa-setup.md
- https://code.claude.com/docs/en/tools-reference
- https://code.claude.com/docs/en/sub-agents
- https://support.claude.com/en/articles/13837440-use-plugins-in-claude
- https://agentskills.io
- https://platform.claude.com/docs/en/managed-agents/cloud-sandboxes-reference
- https://code.claude.com/docs/en/agent-sdk/subagents
- https://support.claude.com/en/articles/13364135-use-claude-cowork-safely
