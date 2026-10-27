# Markenkern (P4)

Der Markenkern ist die Grundlage für alles Visuelle: Aus den Werten werden die Gestaltungsprinzipien, aus der Persönlichkeit das Achsenprofil, aus der Herkunft oft die Signatur. Ohne Markenkern kann der Skill nichts herleiten und landet beim Einheitssystem. Er ist kein Ersatz für eine Markenstrategie und keine Tone-of-Voice. Er passt auf eine Seite.

## Inhalt
1. Woher der Markenkern kommt
2. Die eine Seite
3. Soll-Achsenprofil
4. Interview, wenn es keinen Bestand gibt

## 1 · Woher er kommt

Zuerst aus den Quellen: Selbstbeschreibung auf der Website, Werte aus Vorgaben, Wissensdokumente, Briefing. Jeder Satz im Markenkern hat einen Beleg `[F…]`. Wo die Quellen nichts sagen, fragst du (Abschnitt 4), statt zu erfinden. Gibt es eine ausgearbeitete Markenidentität beim User, übernimm sie und kürze nur.

## 2 · Die eine Seite (`arbeit/03-markenkern.md`)

```markdown
# Markenkern <Marke>

**In einem Satz:** Wer die Marke ist und für wen, ohne Werbesprache. [F…]

**Werte** (3–6, je ein Satz, woran man den Wert im Alltag erkennt)
1. <Wert>: … [F…]

**Persönlichkeit**
| Wir sind | Wir sind nicht |
|---|---|
| … | … |

**Zielgruppe:** wer, was sie vorher denken, was sie nachher sagen sollen. [F…]

**Positionierung:** wogegen die Marke sich abgrenzt (Wettbewerber, Klischees der Branche). [F…]

**Herkunft und Material:** was die Marke an Eigenem mitbringt: Logoform, Ort, Geschichte, Produkt, Handwerk, Sprache. Daraus entstehen später Signatur-Elemente. [F…]

**Ton in drei Reglern:** z. B. förmlich ↔ nahbar, sachlich ↔ emotional, ruhig ↔ energisch, je mit Position und einem Beispielsatz aus den Quellen.

**Tabus:** was die Marke nie sein oder zeigen will. [F…]
```

Schreib konkret. „Qualität“ oder „Innovation“ sind keine Werte, die etwas unterscheiden; frag nach, woran man sie erkennt („Wir reparieren, bevor wir ersetzen“).

## 3 · Soll-Achsenprofil

Aus Persönlichkeit, Zielgruppe und Bestand leitest du für jede der acht Achsen eine Stufe von 1 bis 5 ab (Achsen und Messung: `differenzierung.md`). Je Achse ein Satz Begründung mit Beleg. Trag das Profil in `lauf.json` unter `achsen_soll` ein:

```json
"achsen_soll": {
  "hell_dunkel": { "stufe": 2, "grund": "Die Marke zeigt Handwerk bei Tageslicht [F2, F14]" }
}
```

Die Achsen beschreiben Wirkung, nicht Geschmack: Eine dunkle Marke ist nicht edler, eine runde nicht freundlicher. Begründe jede Stufe aus der Marke. In Runde 1 legst du das Profil in Worten vor (M2), mit dem Hinweis, dass es die Stilrichtungen steuert.

## 4 · Interview ohne Bestand

Für neue Marken oder wenn die Quellen nichts zu Werten sagen. Höchstens acht Fragen, eine nach der anderen oder gebündelt, je nach Wunsch des Users:

1. Was macht ihr, für wen, in einem Satz?
2. Woran merkt ein Kunde nach einem Jahr, dass er bei euch richtig ist?
3. Welche drei Wörter sollen Leute über euch sagen, welche drei auf keinen Fall?
4. Wer sind eure zwei wichtigsten Wettbewerber, und was macht ihr anders?
5. Wo kommt ihr her (Ort, Geschichte, Handwerk, Gründer)? Was davon soll man sehen?
6. Wenn eure Marke ein Ort wäre: welcher?
7. Gibt es Farben, Formen oder Bilder, die schon „eure“ sind, oder die ihr nie wollt?
8. Wie sprecht ihr eure Kunden an (du, Sie, ihr)?

Antworten sind Belege der Art „Aussage User“ im Faktenblatt.
