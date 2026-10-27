# Regeln: frontend-design (Kurzfassung)

| | |
|---|---|
| Quelle | github.com/anthropics/skills, Ordner `skills/frontend-design` (Anthropic) |
| Stand | Commit `dbd4588f9e1033efb41dad4bef2f7947c8993d44` vom 09.10.2026 |
| Lizenz | Apache 2.0, `vendor/frontend-design/LICENSE.txt` |
| Original | `vendor/frontend-design/SKILL.original.md` |

Eigene deutsche Kurzfassung mit Fundstellen, keine Übersetzung. Im Zweifel gilt das Original.

**Klassen:** K1 Mindeststandard (gilt immer, Abweichung nur als ausdrückliche Entscheidung des Users), K2 Stil (die Marke gewinnt, Abweichung begründet in Kapitel 0), K3 Handwerk (Standard, Ausnahme mit Begründung). Arbeitsregeln zum Vorgehen führt diese Datei als K3.

**Fundstellen** (alle in `SKILL.original.md`): **Einl.** = Einleitung vor dem ersten Abschnitt · **Subject** = „Ground your designs in the subject matter“ · **Principles** = „Design principles“ · **Process** = „Process: plan, review against the brief, build, critique“ · **Restraint** = „Restraint and self-critique“ · **Writing** = „More on writing in design“.

## Wofür der Skill es nutzt

**P5 Richtungen:** Der Skill übernimmt die Haltung gegen austauschbares Design. Jede Stilrichtung entsteht aus der Welt der Marke (Branche, Material, Sprache), nicht aus Gewohnheit. Der Plan in zwei Durchgängen (erst kompakter Plan, dann Gegenprobe gegen Briefing und gegen die fünf typischen KI-Looks) ist das Muster für die Bildtafeln und die Prüfung vor Runde 2.

**P6 Ausarbeitung:** Die Regeln zu Hero, Typografie, Struktur, Bewegung und Text fließen in die Anwendungsbeispiele (Musterseite, Social-Kachel, Cover), in Kapitel 11 (Bewegung), 12 (Text im Design) und 14 (Do und Don’t). Grenzwerte liefert frontend-design kaum, die kommen aus den anderen drei Skills.

## Regeln

### Haltung und Herkunft der Gestaltung

| Regel | Klasse | Fundstelle |
|---|---|---|
| Jede Marke bekommt eine eigene, nicht verwechselbare Handschrift: bewusste, auf das Briefing bezogene Entscheidungen zu Farbe, Schrift und Layout, ästhetisches Risiko, wo es begründet ist | K2 | Einl. |
| Unterscheidende Gestaltung kommt aus dem Gegenstand: Branche, Thema, Material und Fachsprache der Marke | K3 | Subject |
| Nennt das Briefing Gegenstand, Zielgruppe oder Hauptaufgabe nicht, schlägt man sie vor und lässt sie bestätigen | K3 | Subject |
| Durchgehend mit dem echten Inhalt und Gegenstand des Briefings arbeiten | K3 | Subject |
| Legt das Briefing eine Richtung fest, gilt sie genau, auch wenn sie einem typischen KI-Look entspricht. Ist eine Achse frei, wird sie nicht für einen Standard-Look verbraucht | K2 | Process |

### Seitenkopf (Hero)

| Regel | Klasse | Fundstelle |
|---|---|---|
| Der Hero zeigt zuerst das Charakteristischste aus der Welt des Gegenstands, in der passenden Form (Headline, Bild, Animation, Live-Demo, Interaktion) | K2 | Principles |
| Große Zahl mit kleinem Label, Kennzahlenreihe und Verlaufsakzent ist die Standardlösung: nur, wenn sie wirklich die beste ist | K2 | Principles |

### Typografie

| Regel | Klasse | Fundstelle |
|---|---|---|
| Typografie trägt die Persönlichkeit. Eine oder zwei Familien, bei zwei klar unterscheidbar | K2 | Principles |
| Schriften bewusst wählen, nicht die Familien, die man bei jedem Projekt nehmen würde | K2 | Principles |
| Klare Schriftskala nach den Grundsätzen von „The Elements of Typographic Style“, mit bewusst gesetzten Gewichten, Breiten und Abständen | K3 | Principles |
| Headline-Satz ist aktiver Teil der Gestaltung, kein neutrales Transportmittel | K2 | Principles |
| Zeilen unter 80 Zeichen. Serifenschriften dürfen etwas länger laufen und bekommen etwas mehr Zeilenabstand als Groteske | K3 | Principles |
| Vermeiden: ein einzelnes Wort oder eine Wendung in der Headline hervorheben (kursiv, fett, andere Farbe) | K2 | Principles |
| Vermeiden: Labels in Versalien | K2 | Principles |
| Vermeiden: überflüssige typografische Labels über Inhalten | K2 | Principles |

### Struktur

| Regel | Klasse | Fundstelle |
|---|---|---|
| Strukturmittel (Rahmen, Linien, Nummern, Eyebrows, Trenner, Labels) tragen Information über den Inhalt, keine Dekoration | K2 | Principles |
| Nummerierung 01 / 02 / 03 nur, wenn der Inhalt wirklich eine Abfolge ist (Prozess in Schritten, Zeitleiste) | K2 | Principles |

### Bewegung

| Regel | Klasse | Fundstelle |
|---|---|---|
| Bewegung, die nicht von der Person ausgelöst wird, sparsam und nur, um Aufmerksamkeit zu lenken | K2 | Principles |
| Ein orchestrierter Moment (eine Ladesequenz oder ein Reveal) statt verstreuter Effekte. Einblenden mit Hochgleiten je Sektion und Hover-Effekt auf jeder Karte gelten als generisch | K2 | Principles |
| Bewegung als Antwort auf eine Handlung (öffnen, aufklappen, bestätigen) ist erwünscht, wenn sie zeigt, was sich geändert hat | K3 | Principles |

### Kalibrierung: fünf typische KI-Looks

Alle fünf sind für manche Briefings richtig, aber sie sind Standard statt Entscheidung und tauchen unabhängig vom Thema auf (Process). Klasse jeweils **K2**.

| Nr. | Look |
|---|---|
| 1 | warmer Cremegrund (um `#F4F1EA`), kontraststarke Serifen-Display, Terrakotta- oder Tonakzent (um `#D97757`, die Akzentfarbe von Anthropic selbst) |
| 2 | fast schwarzer Grund mit einem einzigen grellen Akzent (Säuregrün oder Zinnober) |
| 3 | Zeitungslayout: Haarlinien, Radius null, dichte Spalten |
| 4 | SaaS-Kartenbaukasten: Inhalt in gleiche runde Karten zerteilt, ein Radius für alles, derselbe weiche Grauschatten (`rgba(0,0,0,.1)`), Verläufe als Dekoration |
| 5 | Vorlagen-Chrom: gesperrte Versalien-Eyebrow über jeder Überschrift, Metazeilen mit Mittelpunkt („A · B · C“), Labels aus Wort, Geviertstrich mit Leerzeichen und Fragment, getöntes Fast-Schwarz (`#0B0B0B`, `#111`) statt Schwarz, Monospace für kleine Datenlabels, „→“ an Link- und Buttontexten |

### Vorgehen

| Regel | Klasse | Fundstelle |
|---|---|---|
| Zwei Durchgänge. Zuerst ein kompakter Plan: Farbe als 4–6 benannte Hexwerte, Schriften mit Rollen, Layoutkonzept in je einem Satz plus ASCII-Skizzen samt Ausrichtung (links, zentriert, Blocksatz), Prinzipien für das Eigene | K3 | Process |
| Den Plan vor dem Bauen gegen das Briefing prüfen. Was wie der Standard für jede ähnliche Seite wirkt (Gegenprobe: ähnlichen Auftrag durchdenken), wird überarbeitet, mit Angabe, was und warum | K3 | Process |
| Erst nach dieser Prüfung Code schreiben, nach dem überarbeiteten Plan | K3 | Process |
| CSS-Spezifität im Blick behalten: keine Klassen, die sich gegenseitig aufheben, häufig bei Abständen zwischen Sektionen | K3 | Process |

### Zurückhaltung und Selbstkritik

| Regel | Klasse | Fundstelle |
|---|---|---|
| Mut an einer Stelle ausgeben: ein Element, das man sich merkt, alles darum ruhig und diszipliniert | K2 | Restraint |
| Dekoration streichen, die dem Briefing nicht dient. Vor dem Abschluss ein Accessoire abnehmen (Rat von Chanel) | K2 | Restraint |
| Qualitätsboden ohne Ankündigung: responsiv bis Mobil, sichtbarer Tastaturfokus, reduzierte Bewegung respektiert, visuell zugänglich | K1 | Restraint |
| Harmonische Farbpaletten (ebenfalls Teil des Qualitätsbodens) | K2 | Restraint |
| Beim Bauen selbst kritisieren, mit Screenshots, wo die Umgebung es erlaubt | K3 | Restraint |
| Notizen führen, was schon versucht wurde, damit spätere Durchgänge Neues probieren | K3 | Restraint |

### Text im Design

| Regel | Klasse | Fundstelle |
|---|---|---|
| Wörter machen eine Oberfläche verständlich und benutzbar. Vor dem Schreiben klären, was die Gestaltung sagen muss | K3 | Writing |
| Aus Sicht der Nutzer schreiben: Dinge so benennen, wie Nutzer sie verstehen, nicht wie das System gebaut ist | K3 | Writing |
| Beschreiben, was etwas ist oder tut, statt es zu verkaufen. Konkret und verständlich vor clever | K2 | Writing |
| Aktiv formulieren. Ein Button sagt genau, was passiert („Änderungen speichern“, nicht „Absenden“) | K3 | Writing |
| Eine Handlung heißt im ganzen Ablauf gleich (Button „Veröffentlichen“, Meldung „Veröffentlicht“) | K3 | Writing |
| Fehler sagen, was passiert ist und wie man es behebt, in der Stimme der Oberfläche. Keine Entschuldigung, nie vage | K3 | Writing |
| Ein leerer Zustand ist eine Einladung zu handeln | K3 | Writing |
| Ton wie im Gespräch: einfache Verben, Satzschreibung, keine Füllwörter, passend zu Marke und Zielgruppe | K2 | Writing |
| Jedes Textelement hat genau eine Aufgabe | K3 | Writing |

### Nicht geregelt

Logo, Bildwelt, Ikonografie, Druck, Raster und Abstände als Werte, Radien, Wahl von hell oder dunkel, konkrete Grenzwerte (Kontrast, Größen, Trefferflächen, Dauern). Dafür gelten `regeln-impeccable.md`, `regeln-web-interface-guidelines.md`, `regeln-ui-ux-pro-max.md` und `tokens.md`.

## Typische Konflikte mit Marken

frontend-design sagt selbst, dass festgelegte Vorgaben des Briefings gewinnen (Process). Deshalb sind fast alle Konflikte K2: Der Bestand der Marke gewinnt, die Abweichung steht begründet in Kapitel 0.

| Bestand der Marke | Betroffene Regel | Behandlung |
|---|---|---|
| Eyebrows, Versalien-Labels, Monospace-Datenlabels, „→“ an Buttons, Metazeilen mit Mittelpunkt | Vorlagen-Chrom, Versalien-Labels, Strukturmittel | K2. Gehören die Elemente zum Bestand, bleiben sie. Die Begründung nennt, welche Information sie tragen. Neue Elemente dieser Art nur mit Herleitung |
| hervorgehobenes Einzelwort in Headlines (häufig in Kampagnen) | Typografie, Vermeiden-Liste | K2. Bestand gewinnt, Regel für den Einsatz im Guide als Zahl und Grenze festhalten |
| Cremegrund mit Serife und warmem Akzent, oder Dunkel mit einem Neonakzent | Kalibrierung Look 1 und 2 | K2. Bestand gewinnt. Weil diese Looks bei vielen Marken vorkommen, muss das Eigene aus Signatur-Elementen und Markenmaterial kommen (Konzept Abschnitt 5, Blindtest) |
| nummerierte Abschnitte ohne echte Abfolge | Struktur | K2. Bleibt, wenn die Marke es begründet; sonst als Vorschlag in Runde 1 oder 2 |
| werbender Ton statt Beschreibung | Text im Design | K2. Tonalität der Marke gewinnt. Für Buttons, Fehlermeldungen und leere Zustände bleiben die K3-Regeln Standard |
| Groß- und Kleinschreibung | Satzschreibung (hier) gegen Title Case (Vercel) | K2. Im Deutschen folgt die Schreibung der Rechtschreibung, in anderen Sprachen der Marke |
| viele verstreute Animationen auf der bestehenden Website | Bewegung | K2. Die Marke kann sie begründen. Der Prüfer fragt nach dem einen Moment, der bleiben soll |
| Markenfarbe als Schrift zu hell | Qualitätsboden „visuell zugänglich“ | K1. Widerspruch in Runde 1 mit Vorschlag in der Marke, etwa eine dunklere Schriftfassung als `farbe.rolle.akzent-text` |
| Bestandsschrift ist eine Standardschrift | Schriften bewusst wählen | K2. Bestand gewinnt, wenn die Schrift Teil der Marke ist. Eine neue Schrift braucht eine Herleitung, keine Gewohnheit |
