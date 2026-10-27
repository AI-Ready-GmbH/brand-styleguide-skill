#!/usr/bin/env python3
"""Prüft einen Lauf gegen Pflichtinhalte, Herleitung, Belege, Tokens und offene Platzhalter.

Was ein Skript zählen kann, prüft dieses Skript. Urteil (Blindtest, Anti-Patterns, Lesbarkeit) macht der Prüfer
(references/pruefung.md).

Aufruf:
  python3 scripts/pruefen.py <lauf>          → arbeit/05-skripte.json und Liste in der Konsole

Exit 0: keine Befunde · 1: Befunde · 3: Lauf-Ordner oder Pflichtdateien fehlen
"""
import argparse
import json
import pathlib
import re
import sys

HIER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HIER))
import tokenlib as tl  # noqa: E402
import tokens as tokmod  # noqa: E402

KERN = ["ueber", "markenkern", "prinzipien", "logo", "farbe", "typografie", "raster", "signatur", "komponenten",
        "ikonografie", "bildwelt", "bewegung", "text", "checkliste", "dodont", "pflege"]
MODULE = {"web", "druck", "social", "praesentation", "bewegtbild", "mail", "digital", "verpackung"}
SKILLS = ["frontend-design", "Web Interface Guidelines", "Impeccable", "ui-ux-pro-max"]
PLATZHALTER = re.compile(r"\{\{(?!\s*(farbtafel|kontrasttabelle|schriftmuster|abstaende|radien|tokens-uebersicht|bild|beispiel|logo)\b)[^}]*\}\}|\bTODO\b|\bXXX\b|[Ll]orem ipsum")


def kapitel(md):
    """Kennung → Text des Kapitels (bis zur nächsten Überschrift zweiter Ebene)."""
    teile, aktuell, buf = {}, None, []
    for z in md.splitlines():
        m = re.match(r"##\s+.*\{#([a-z0-9-]+)\}\s*$", z)
        if m or z.startswith("## "):
            if aktuell:
                teile[aktuell] = "\n".join(buf)
            aktuell, buf = (m.group(1) if m else None), []
        elif aktuell:
            buf.append(z)
    if aktuell:
        teile[aktuell] = "\n".join(buf)
    return teile


def bloecke(text):
    """Abschnitte dritter Ebene: Titel → Text."""
    raus, titel, buf = [], None, []
    for z in text.splitlines():
        if z.startswith("### "):
            if titel:
                raus.append((titel, "\n".join(buf)))
            titel, buf = z[4:].strip(), []
        elif titel:
            buf.append(z)
    if titel:
        raus.append((titel, "\n".join(buf)))
    return raus


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lauf")
    a = ap.parse_args()
    lauf = pathlib.Path(a.lauf)
    befunde = []
    b = lambda art, text: befunde.append({"art": art, "befund": text})

    pflicht = ["lauf.json", "tokens/tokens.json", "guide/guide.md", "arbeit/01-fakten.md", "arbeit/03-markenkern.md"]
    fehlend = [p for p in pflicht if not (lauf / p).exists()]
    if fehlend:
        print("Pflichtdateien fehlen: " + ", ".join(fehlend), file=sys.stderr)
        return 3
    lj = json.loads((lauf / "lauf.json").read_text(encoding="utf-8"))
    md = (lauf / "guide" / "guide.md").read_text(encoding="utf-8")
    fakten = (lauf / "arbeit" / "01-fakten.md").read_text(encoding="utf-8")
    entsch = lj.get("entscheidungen", {})

    # Tokens und Kontrast
    try:
        t = tl.laden(lauf / "tokens" / "tokens.json")
        fehler, hinweise = tokmod.pruefen(t)
        for f in fehler:
            b("Tokens", f)
        for h in hinweise:
            b("Herleitung", h)
        import kontrast
        ausnahmen = {(x.get("paar"), x.get("modus")) for x in lj.get("ausnahmen_k1", [])}
        for e in kontrast.messen(t):
            for m, d in e["modi"].items():
                if not d.get("ok") and (f"{e['vorne']}/{e['hinten']}", m) not in ausnahmen:
                    b("K1 Kontrast", f"{e['vorne']} auf {e['hinten']} ({m}): {d.get('kontrast', '?')} : 1 < {e['grenze']} : 1")
    except tl.TokenFehler as e:
        b("Tokens", str(e))
        t = None

    # Kapitel
    kap = kapitel(md)
    for k in KERN:
        if k not in kap:
            b("Vollständigkeit", f"Pflichtkapitel fehlt oder ohne Kennung: {{#{k}}}")
    for m in lj.get("module", []):
        if m in MODULE and m not in kap:
            b("Vollständigkeit", f"Modul aus dem Briefing fehlt: {{#{m}}}")
    for k, text in kap.items():
        if len(re.sub(r"\s+", " ", text).strip()) < 120 and k not in ("markenkern",):
            b("Vollständigkeit", f"Kapitel {{#{k}}} ist fast leer")

    # Prinzipien: 4–6, je mit Wert
    if "prinzipien" in kap:
        pr = bloecke(kap["prinzipien"])
        if not 4 <= len(pr) <= 6:
            b("Herleitung", f"{len(pr)} Prinzipien (### …) gefunden, erwartet 4–6")
        for titel, text in pr:
            if not re.search(r"^\s*\**Wert:?\**\s*:?", text, re.M):
                b("Herleitung", f"Prinzip „{titel}“ ohne Zeile „Wert: …“")

    # Signatur: je Aufgabe, Grenze, Herleitung
    if "signatur" in kap:
        sig = bloecke(kap["signatur"])
        if not 2 <= len(sig) <= 5:
            b("Herleitung", f"{len(sig)} Signatur-Elemente (### …) gefunden, erwartet 2–5")
        for titel, text in sig:
            for feld in ("Aufgabe", "Grenze", "Herleitung"):
                if not re.search(rf"^\s*\**{feld}:?\**\s*:?", text, re.M):
                    b("Herleitung", f"Signatur „{titel}“ ohne Zeile „{feld}: …“")

    # Kapitel 0 nennt die vier Skills
    if "ueber" in kap:
        for s in SKILLS:
            if s.lower() not in kap["ueber"].lower():
                b("Vollständigkeit", f"Kapitel 0 nennt den Design-Skill „{s}“ nicht")

    # Belege und Entscheidungen
    f_nummern = set(re.findall(r"^\|\s*(F\d+)\s*\|", fakten, re.M))
    for ref in sorted(set(re.findall(r"\[((?:[FWSMQ]\d+)(?:\s*,\s*[FWSMQ]\d+)*)\]", md))):
        for x in [y.strip() for y in ref.split(",")]:
            if x.startswith("F") and x not in f_nummern:
                b("Fakt", f"Beleg {x} steht im Guide, aber nicht im Faktenblatt")
            if x[0] in "WSM" and x not in entsch:
                b("Entscheidung", f"Verweis {x} hat keinen Eintrag in lauf.json → entscheidungen")
            if x.startswith("Q") and x not in {q.get("id") for q in lj.get("quellen", [])}:
                b("Fakt", f"Quelle {x} steht im Guide, aber nicht in lauf.json → quellen")
    vorl = set(re.findall(r"\[vorläufig:\s*([A-Z]\d+)\]", md))
    for x in sorted(vorl):
        if x not in entsch:
            b("Entscheidung", f"vorläufig {x} hat keinen Eintrag in lauf.json")
        if "pflege" in kap and x not in kap["pflege"]:
            b("Vollständigkeit", f"vorläufiger Punkt {x} fehlt in der Liste im Kapitel Pflege")
    for k, v in entsch.items():
        if v.get("vorlaeufig") and k not in vorl and k not in md:
            b("Entscheidung", f"{k} ist vorläufig entschieden, im Guide aber nicht markiert")

    # Farben außerhalb der Tokens
    if t:
        bekannte = set()
        for p in t.flach:
            if p.startswith("farbe."):
                for m in t.modi:
                    try:
                        bekannte.add(tl.hex_von(tl.farbe(t.wert(p, m))))
                    except tl.TokenFehler:
                        pass
        for hx in sorted(set(h.upper() for h in re.findall(r"#[0-9A-Fa-f]{6}\b", md))):
            if hx not in bekannte:
                b("Tokens", f"Farbe {hx} steht im Guide, aber nicht in den Tokens")

    # Platzhalter
    for m in PLATZHALTER.finditer(md):
        b("Platzhalter", f"offener Platzhalter im Guide: {m.group(0)[:40]}")

    # Ergebnisse des Laufs
    if not (lauf / "guide" / "marke.css").exists():
        b("Vollständigkeit", "guide/marke.css fehlt (Guide ohne Gestaltung der Marke)")
    if not (lauf / "beispiele").exists() or not list((lauf / "beispiele").glob("*.png")):
        b("Vollständigkeit", "keine Anwendungsbeispiele als PNG in beispiele/")
    for datei in ("DESIGN.md", "PRODUCT.md"):
        p = lauf / datei
        if not p.exists():
            b("Vollständigkeit", f"{datei} fehlt")
        elif "{{" in p.read_text(encoding="utf-8"):
            b("Platzhalter", f"{datei} enthält noch Platzhalter {{{{…}}}}")
    if lj.get("stack") and not (lauf / "code").exists():
        b("Vollständigkeit", "Stack aktiv, aber code/ fehlt")
    if not lj.get("achsen_soll"):
        b("Herleitung", "lauf.json ohne achsen_soll (Markenkern, P4)")

    (lauf / "arbeit").mkdir(exist_ok=True)
    (lauf / "arbeit" / "05-skripte.json").write_text(json.dumps(befunde, ensure_ascii=False, indent=2), encoding="utf-8")
    for x in befunde:
        print(f"{x['art']:<15} {x['befund']}")
    print(f"{len(befunde)} Befunde." if befunde else "Keine Befunde.")
    return 1 if befunde else 0


if __name__ == "__main__":
    sys.exit(main())
