#!/usr/bin/env python3
"""Kontrasttabelle aller Pflichtpaare in allen Modi (WCAG 2.2 AA).

Aufruf:
  python3 scripts/kontrast.py <lauf>/tokens/tokens.json        → kontrast.md, kontrast.json neben der Datei
  python3 scripts/kontrast.py --paar "#E07B39" "#FFFFFF"       → einzelnes Paar

Grenzen: Text 4,5 : 1 · große Schrift 3 : 1 · Grafik (Ränder, Fokus, Icons) 3 : 1.
Exit 0: alle Paare erfüllt · 1: mindestens ein Verstoß (Klasse K1) · 3: Datei fehlt
"""
import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import tokenlib as tl  # noqa: E402

GRENZE = {"text": 4.5, "gross": 3.0, "grafik": 3.0}
NAME = {"text": "Text", "gross": "große Schrift", "grafik": "Grafik"}


def paare(t):
    rollen = set(t.gruppe("farbe.rolle"))
    gruende = [g for g in ("grund", "flaeche", "flaeche-2", "flaeche-akzent") if g in rollen]
    liste = []
    for vorne in ("text", "text-leise", "akzent-text", "fehler"):
        if vorne in rollen:
            liste += [(vorne, g, "text") for g in gruende]
    for h in ("handlung", "handlung-hover"):
        if h in rollen and "handlung-text" in rollen:
            liste.append(("handlung-text", h, "text"))
    for vorne in ("linie-stark", "fokus", "akzent"):
        if vorne in rollen and "grund" in rollen:
            liste.append((vorne, "grund", "grafik"))
    for eintrag in t.marke.get("kontrastpaare", []):
        a, b, art = eintrag
        liste.append((a.replace("farbe.rolle.", ""), b.replace("farbe.rolle.", ""), art))
    gesehen, eindeutig = set(), []
    for p in liste:
        if p[:2] not in gesehen:
            gesehen.add(p[:2])
            eindeutig.append(p)
    return eindeutig


def deckend(t, rolle, modus):
    """Farbe einer Rolle als deckende Farbe; Transparenz wird auf den Grund gemischt."""
    f = tl.farbe(t.wert(f"farbe.rolle.{rolle}", modus))
    if f[3] < 1 and rolle != "grund":
        f = tl.auf_grund(f, tl.farbe(t.wert("farbe.rolle.grund", modus)))
    return f


def messen(t):
    ergebnisse = []
    for vorne, hinten, art in paare(t):
        zeile = {"vorne": vorne, "hinten": hinten, "art": art, "grenze": GRENZE[art], "modi": {}}
        for modus in t.modi:
            try:
                h = deckend(t, hinten, modus)
                v = tl.farbe(t.wert(f"farbe.rolle.{vorne}", modus))
                v = tl.auf_grund(v, h) if v[3] < 1 else v
                k = tl.kontrast(v, h)
                zeile["modi"][modus] = {"kontrast": round(k, 2), "ok": k + 1e-9 >= GRENZE[art],
                                        "vorne": tl.hex_von(v), "hinten": tl.hex_von(h)}
            except tl.TokenFehler as e:
                zeile["modi"][modus] = {"fehler": str(e)}
        ergebnisse.append(zeile)
    return ergebnisse


def tabelle(t, ergebnisse):
    z = ["| Vordergrund | Hintergrund | " + " | ".join(t.modi) + " | Grenze |",
         "|---|---|" + "---|" * len(t.modi) + "---|"]
    for e in ergebnisse:
        zellen = []
        for m in t.modi:
            d = e["modi"][m]
            if "fehler" in d:
                zellen.append("Fehler")
            else:
                zellen.append(f"{'✓' if d['ok'] else '✗'} {tl.zahl_de(d['kontrast'])} : 1")
        z.append(f"| `{e['vorne']}` | `{e['hinten']}` | " + " | ".join(zellen) +
                 f" | {tl.zahl_de(e['grenze'])} : 1 ({NAME[e['art']]}) |")
    return "\n".join(z) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tokens", nargs="?")
    ap.add_argument("--paar", nargs=2, metavar=("VORNE", "HINTEN"))
    a = ap.parse_args()
    if a.paar:
        v, h = tl.farbe(a.paar[0]), tl.farbe(a.paar[1])
        v = tl.auf_grund(v, h) if v[3] < 1 else v
        k = tl.kontrast(v, h)
        urteil = "Text ✓" if k >= 4.5 else ("nur große Schrift und Grafik ✓" if k >= 3 else "✗ unter 3 : 1")
        print(f"{tl.zahl_de(k, 2)} : 1 · {urteil}")
        return 0
    if not a.tokens or not pathlib.Path(a.tokens).exists():
        print("tokens.json fehlt (oder --paar nutzen)", file=sys.stderr)
        return 3
    t = tl.laden(a.tokens)
    erg = messen(t)
    ziel = pathlib.Path(a.tokens).parent
    stamm = pathlib.Path(a.tokens).name.replace(".tokens.json", ".") if a.tokens.endswith(".tokens.json") else ""
    (ziel / f"{stamm}kontrast.md").write_text(tabelle(t, erg), encoding="utf-8")
    (ziel / f"{stamm}kontrast.json").write_text(json.dumps(erg, ensure_ascii=False, indent=2), encoding="utf-8")
    verstoesse = [(e, m, d) for e in erg for m, d in e["modi"].items() if not d.get("ok")]
    for e, m, d in verstoesse:
        wert = d.get("fehler") or f"{tl.zahl_de(d['kontrast'], 2)} : 1 < {tl.zahl_de(e['grenze'])} : 1"
        print(f"K1 VERSTOSS  {e['vorne']} auf {e['hinten']} ({m}): {wert}")
    print(f"{len(erg)} Paare × {len(t.modi)} Modi geprüft, {len(verstoesse)} Verstöße. Tabelle: {ziel / (stamm + 'kontrast.md')}")
    return 1 if verstoesse else 0


if __name__ == "__main__":
    sys.exit(main())
