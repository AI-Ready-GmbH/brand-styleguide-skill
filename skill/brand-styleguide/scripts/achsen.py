#!/usr/bin/env python3
"""Ist-Achsenprofil aus den Tokens, Vergleich mit dem Soll aus lauf.json (references/differenzierung.md).

Aufruf:
  python3 scripts/achsen.py <lauf>                              → arbeit/achsen.md, arbeit/achsen.json
  python3 scripts/achsen.py --tokens <richtung>.tokens.json     → Profil einer Stilrichtung ausgeben
  python3 scripts/achsen.py --vergleich a.tokens.json b.tokens.json …   → Unterschiede zwischen Richtungen

Die Messung ist eine Näherung. Werte in $marke.achsen_ist (mit Grund) überschreiben sie.
Exit 0: Ist passt zum Soll (höchstens 1 Stufe Abstand) · 1: Abweichung oder Richtungen zu ähnlich · 3: Datei fehlt
"""
import argparse
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import tokenlib as tl  # noqa: E402

ACHSEN = [
    ("hell_dunkel", "hell", "dunkel"),
    ("kuehl_warm", "kühl", "warm"),
    ("zurueckhaltend_farbig", "zurückhaltend", "farbig"),
    ("eckig_rund", "eckig", "rund"),
    ("luftig_dicht", "luftig", "dicht"),
    ("leise_laut", "leise", "laut"),
    ("sachlich_verspielt", "sachlich", "verspielt"),
    ("still_lebendig", "still", "lebendig"),
]


def stufe(wert, grenzen):
    """Ordnet einen Wert über aufsteigende Grenzen den Stufen 1–5 zu."""
    for i, g in enumerate(grenzen):
        if wert <= g:
            return i + 1
    return 5


def profil(t):
    m = t.modi[0]
    farbe = lambda r: tl.farbe(t.wert(f"farbe.rolle.{r}", m))
    p = {}
    # hell ↔ dunkel: Leuchtdichte des Grundes
    l = tl.leuchtdichte(farbe("grund"))
    p["hell_dunkel"] = {"stufe": 6 - stufe(l, [0.02, 0.08, 0.3, 0.7]), "messung": f"Leuchtdichte Grund {l:.2f}"}
    # kühl ↔ warm: b* (gelb-blau) plus halbes a* der Neutralflächen
    werte = []
    for r in ("grund", "flaeche", "text"):
        _, a_, b_ = tl.lab(farbe(r))
        werte.append(b_ + a_ * 0.5)
    w = sum(werte) / len(werte)
    p["kuehl_warm"] = {"stufe": stufe(w, [-6, -2, 2, 6]), "messung": f"Wärme {w:+.1f} (Lab b*+a*/2 von Grund, Fläche, Text)"}
    # zurückhaltend ↔ farbig: deutlich bunte Basisfarben (Buntheit > 25), untereinander unterscheidbar
    bunt = []  # Rollen, die die Gestaltung tragen; Fehler- und Statusfarben zählen nicht
    for r in t.gruppe("farbe.rolle"):
        if r.startswith(("fehler", "erfolg", "hinweis", "linie", "text-leise", "fokus")):
            continue
        f = tl.farbe(t.wert(f"farbe.rolle.{r}", m))
        if f[3] < 1:
            f = tl.auf_grund(f, farbe("grund"))
        if tl.buntheit(f) > 25 and all(tl.delta_e(f, x) > 15 for x in bunt):
            bunt.append(f)
    max_b = max([tl.buntheit(f) for f in bunt], default=0)
    s = 1 if not bunt else (2 if len(bunt) == 1 and max_b < 45 else (3 if len(bunt) <= 2 else (4 if len(bunt) == 3 else 5)))
    p["zurueckhaltend_farbig"] = {"stufe": s, "messung": f"{len(bunt)} deutlich bunte Rollenfarben, größte Buntheit {max_b:.0f}"}
    # eckig ↔ rund
    r = tl.px(t.wert("radius.karte")) or 0
    p["eckig_rund"] = {"stufe": stufe(r, [0.5, 4, 10, 20]), "messung": f"Radius Karte {r:g} px"}
    # luftig ↔ dicht: größter Abstand und Zeilenhöhe des Fließtexts
    abst = [tl.px(t.wert(f"abstand.{a}")) or 0 for a in t.gruppe("abstand")]
    groesster = max(abst, default=0)
    zh = 1.5
    if "schrift.web.fliesstext" in t.flach:
        v = t.wert("schrift.web.fliesstext", m)
        zh = float(v.get("lineHeight", 1.5)) if isinstance(v, dict) else 1.5
    s = 6 - stufe(groesster, [40, 64, 96, 128])
    s = max(1, min(5, s + (1 if zh < 1.45 else (-1 if zh > 1.7 else 0))))
    p["luftig_dicht"] = {"stufe": s, "messung": f"größter Abstand {groesster:g} px, Zeilenhöhe Fließtext {zh:g}"}
    # leise ↔ laut: Verhältnis größte Stufe zu Fließtext, Gewicht der Titel
    gross = 0
    for st in t.gruppe("schrift.web"):
        v = t.wert(f"schrift.web.{st}", m)
        if isinstance(v, dict):
            gross = max(gross, tl.px(v.get("fontSize", "0"), minimum=False) or 0)
    basis = 16
    if "schrift.web.fliesstext" in t.flach:
        basis = tl.px(t.wert("schrift.web.fliesstext", m).get("fontSize", "16px")) or 16
    verh = gross / basis if basis else 0
    gew = 400
    for st in ("display", "titel-1"):
        if f"schrift.web.{st}" in t.flach:
            gew = max(gew, int(t.wert(f"schrift.web.{st}", m).get("fontWeight", 400)))
    s = stufe(verh, [2.5, 3.5, 4.5, 5.5]) + (1 if gew >= 800 else 0)
    p["leise_laut"] = {"stufe": min(5, s), "messung": f"größte Schrift / Fließtext {verh:.1f}, Titelgewicht {gew}"}
    # sachlich ↔ verspielt: nicht messbar
    p["sachlich_verspielt"] = {"stufe": None, "messung": "nicht messbar, Eintrag in $marke.achsen_ist nötig"}
    # still ↔ lebendig: längste Dauer
    dauern = [tl.ms(t.wert(f"bewegung.dauer.{d}")) or 0 for d in t.gruppe("bewegung.dauer")]
    lang = max(dauern, default=0)
    p["still_lebendig"] = {"stufe": stufe(lang, [200, 300, 500, 1000]), "messung": f"längste Dauer {lang:g} ms"}
    for k, v in (t.marke.get("achsen_ist") or {}).items():
        if k in p:
            p[k] = {"stufe": v.get("stufe"), "messung": f"gesetzt: {v.get('grund', 'ohne Grund')}", "gesetzt": True}
    return p


def zeile(name, links, rechts, ist, soll=None):
    s_ist = ist.get("stufe")
    s_soll = soll.get("stufe") if soll else None
    diff = abs(s_ist - s_soll) if (s_ist and s_soll) else None
    urteil = "–" if diff is None else ("✓" if diff <= 1 else f"✗ {diff} Stufen")
    return f"| {links} ↔ {rechts} | {s_soll or '–'} | {s_ist or '?'} | {urteil} | {ist['messung']} |", diff


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lauf", nargs="?")
    ap.add_argument("--tokens")
    ap.add_argument("--vergleich", nargs="+")
    a = ap.parse_args()

    if a.vergleich:
        profile = {pathlib.Path(p).name: profil(tl.laden(p)) for p in a.vergleich}
        namen = list(profile)
        print("| Achse | " + " | ".join(namen) + " |")
        print("|---|" + "---|" * len(namen))
        for k, l, r in ACHSEN:
            print(f"| {l} ↔ {r} | " + " | ".join(str(profile[n][k]["stufe"] or "?") for n in namen) + " |")
        zu_aehnlich = []
        for i in range(len(namen)):
            for j in range(i + 1, len(namen)):
                unterschiede = sum(1 for k, _, _ in ACHSEN if profile[namen[i]][k]["stufe"] and profile[namen[j]][k]["stufe"]
                                   and abs(profile[namen[i]][k]["stufe"] - profile[namen[j]][k]["stufe"]) >= 1)
                print(f"{namen[i]} ↔ {namen[j]}: {unterschiede} Achsen verschieden")
                if unterschiede < 3:
                    zu_aehnlich.append((namen[i], namen[j]))
        if zu_aehnlich:
            print("Zu ähnlich (weniger als 3 Achsen verschieden): " + "; ".join(f"{x} / {y}" for x, y in zu_aehnlich))
            return 1
        return 0

    if a.tokens:
        p = profil(tl.laden(a.tokens))
        for k, l, r in ACHSEN:
            print(f"{l} ↔ {r}: {p[k]['stufe'] or '?'}  ({p[k]['messung']})")
        return 0

    if not a.lauf:
        ap.print_help()
        return 3
    lauf = pathlib.Path(a.lauf)
    tok, lj = lauf / "tokens" / "tokens.json", lauf / "lauf.json"
    if not tok.exists():
        print(f"Datei fehlt: {tok}", file=sys.stderr)
        return 3
    soll = json.loads(lj.read_text(encoding="utf-8")).get("achsen_soll", {}) if lj.exists() else {}
    ist = profil(tl.laden(tok))
    z = ["| Achse | Soll | Ist | Urteil | Messung |", "|---|---|---|---|---|"]
    abweichungen = []
    for k, l, r in ACHSEN:
        text, diff = zeile(k, l, r, ist[k], soll.get(k))
        z.append(text)
        if diff is not None and diff > 1:
            abweichungen.append(f"{l} ↔ {r}: Soll {soll[k]['stufe']}, Ist {ist[k]['stufe']}")
        if ist[k]["stufe"] is None:
            abweichungen.append(f"{l} ↔ {r}: Ist fehlt (in $marke.achsen_ist mit Grund eintragen)")
    (lauf / "arbeit").mkdir(exist_ok=True)
    (lauf / "arbeit" / "achsen.md").write_text("\n".join(z) + "\n", encoding="utf-8")
    (lauf / "arbeit" / "achsen.json").write_text(json.dumps({"ist": ist, "soll": soll}, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\n".join(z))
    if not soll:
        print("Hinweis: lauf.json hat kein achsen_soll (P4).")
    for x in abweichungen:
        print("BEFUND  " + x)
    return 1 if abweichungen else 0


if __name__ == "__main__":
    sys.exit(main())
