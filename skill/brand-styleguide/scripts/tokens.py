#!/usr/bin/env python3
"""Prüft tokens.json und erzeugt daraus tokens.css, theme.css (Tailwind v4), druck.css und die Token-Übersicht.

Format: references/tokens.md. Ausgaben liegen neben tokens.json.

Aufruf:
  python3 scripts/tokens.py <lauf>/tokens/tokens.json
  python3 scripts/tokens.py <richtung>.tokens.json --nur-css     (für Stilrichtungen: nur tokens.css)

Exit 0: in Ordnung · 1: Fehler (fehlende Pflicht-Tokens, Verweise ins Leere, Mindestgrößen) · 3: Datei fehlt
"""
import argparse
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import tokenlib as tl  # noqa: E402

HERKUNFT = re.compile(r"\b([FWSMQ]\d+|Entscheidung|Katalog|Bestand|Logo)\b")


def var_name(pfad):
    teile = pfad.split(".")
    if teile[:2] == ["farbe", "basis"]:
        return "--m-basis-" + "-".join(teile[2:])
    if teile[:2] == ["farbe", "rolle"]:
        return "--m-farbe-" + "-".join(teile[2:])
    if teile[:2] == ["schrift", "familie"]:
        return "--m-schrift-" + "-".join(teile[2:])
    if teile[:2] == ["bewegung", "dauer"]:
        return "--m-dauer-" + "-".join(teile[2:])
    if teile[:2] == ["bewegung", "kurve"]:
        return "--m-kurve-" + "-".join(teile[2:])
    return "--m-" + "-".join(teile)


def familie_css(liste):
    if isinstance(liste, str):
        return liste
    raus = []
    for n in liste:
        n = str(n).strip()
        generisch = n in ("serif", "sans-serif", "monospace", "system-ui", "cursive", "ui-sans-serif", "ui-serif")
        raus.append(n if generisch or re.fullmatch(r"[A-Za-z-]+", n) else f'"{n}"')
    return ", ".join(raus)


def css_wert(t, pfad, modus):
    """CSS-Ausdruck für einen Token: Verweise werden zu var(), sonst Literal."""
    roh = t.roh(pfad, modus)
    if isinstance(roh, str):
        m = tl.VERWEIS.fullmatch(roh.strip())
        if m:
            return f"var({var_name(m.group(1))})"
        return tl.VERWEIS.sub(lambda m: f"var({var_name(m.group(1))})", roh)
    if isinstance(roh, list):
        return familie_css(roh)
    if isinstance(roh, (int, float)):
        return str(roh)
    return None


def typo_zeilen(t, gruppe, modus=None):
    zeilen = []
    for stufe in t.gruppe(gruppe):
        pfad = f"{gruppe}.{stufe}"
        roh = t.roh(pfad, modus)
        if not isinstance(roh, dict):
            continue
        fam = roh.get("fontFamily")
        if isinstance(fam, str) and tl.VERWEIS.fullmatch(fam.strip()):
            fam_css = f"var({var_name(tl.VERWEIS.fullmatch(fam.strip()).group(1))})"
        else:
            fam_css = familie_css(fam) if fam else None
        for schluessel, name in (("fontSize", "groesse"), ("lineHeight", "zeilenhoehe"),
                                 ("letterSpacing", "laufweite"), ("fontWeight", "gewicht")):
            if schluessel in roh:
                zeilen.append(f"  --m-text-{stufe}-{name}: {roh[schluessel]};")
        if fam_css:
            zeilen.append(f"  --m-text-{stufe}-familie: {fam_css};")
        if (t.flach[pfad].get("$extensions") or {}).get("versalien"):
            zeilen.append(f"  --m-text-{stufe}-versalien: uppercase;")
    return zeilen


def pruefen(t):
    fehler, hinweise = [], []
    for p in t.fehlende_pflicht():
        fehler.append(f"Pflicht-Token fehlt: {p}")
    if t.marke.get("standardmodus") and t.marke["standardmodus"] != t.modi[0]:
        fehler.append("$marke.standardmodus muss der erste Eintrag in $marke.modi sein")
    for pfad in t.flach:
        for modus in t.modi:
            try:
                v = t.wert(pfad, modus)
            except tl.TokenFehler as e:
                fehler.append(f"{pfad} ({modus}): {e}")
                continue
            if pfad.startswith("farbe."):
                try:
                    tl.farbe(v)
                except tl.TokenFehler as e:
                    fehler.append(f"{pfad} ({modus}): {e}")
    for name in t.gruppe("farbe.basis"):
        tok = t.flach[f"farbe.basis.{name}"]
        if not HERKUNFT.search(str(tok.get("$description", ""))):
            hinweise.append(f"farbe.basis.{name}: Herkunft fehlt in $description (Fundstelle F…, Entscheidung W…/S…, „Katalog …“)")
    grenzen = {"fliesstext": 16, "label": 12}
    for stufe in t.gruppe("schrift.web"):
        try:
            v = t.wert(f"schrift.web.{stufe}")
        except tl.TokenFehler:
            continue
        groesse = tl.px(v.get("fontSize", "")) if isinstance(v, dict) else None
        if groesse is None:
            fehler.append(f"schrift.web.{stufe}: fontSize nicht lesbar ({v.get('fontSize') if isinstance(v, dict) else v})")
            continue
        g = grenzen.get(stufe, 12)
        if groesse + 0.01 < g:
            fehler.append(f"schrift.web.{stufe}: {tl.zahl_de(groesse)} px liegt unter dem Mindeststandard {g} px (Klasse K1)")
    for name in t.gruppe("schrift.familie"):
        ext = t.flach[f"schrift.familie.{name}"].get("$extensions") or {}
        if not ext.get("lizenz"):
            hinweise.append(f"schrift.familie.{name}: Lizenzstatus fehlt ($extensions.lizenz)")
    for name in t.gruppe("bewegung.dauer"):
        d = tl.ms(t.wert(f"bewegung.dauer.{name}"))
        if d is None:
            fehler.append(f"bewegung.dauer.{name}: Dauer nicht lesbar (ms oder s)")
    for name in t.gruppe("radius"):
        if tl.px(t.wert(f"radius.{name}")) is None:
            fehler.append(f"radius.{name}: Wert nicht lesbar (px oder rem)")
    return fehler, hinweise


def tokens_css(t, nur_farben_modus=None):
    erster = t.modi[0]
    zeilen = [f"/* Tokens {t.marke.get('name', '')} v{t.marke.get('version', '')}: erzeugt von scripts/tokens.py, nicht von Hand ändern. */",
              ":root {", f"  color-scheme: {'dark' if erster == 'dunkel' else 'light'};"]
    for pfad in t.flach:
        if pfad.startswith("schrift.web.") or pfad.startswith("schrift.druck."):
            continue
        w = css_wert(t, pfad, erster)
        if w is not None and not isinstance(t.roh(pfad, erster), dict):
            zeilen.append(f"  {var_name(pfad)}: {w};")
    zeilen += typo_zeilen(t, "schrift.web")
    zeilen.append("}")
    for modus in t.modi[1:]:
        block = []
        for pfad in t.flach:
            ext = (t.flach[pfad].get("$extensions") or {}).get("modi") or {}
            if modus in ext:
                block.append(f"  {var_name(pfad)}: {css_wert(t, pfad, modus)};")
        kopf = f"[data-modus=\"{modus}\"]"
        zeilen += ["", kopf + " {", f"  color-scheme: {'dark' if modus == 'dunkel' else 'light'};"] + block + ["}"]
        if t.marke.get("folgt_system") and modus in ("hell", "dunkel"):
            schema = "dark" if modus == "dunkel" else "light"
            zeilen += ["", f"@media (prefers-color-scheme: {schema}) {{", "  :root:not([data-modus]) {",
                       f"    color-scheme: {schema};"] + ["  " + z for z in block] + ["  }", "}"]
    return "\n".join(zeilen) + "\n"


def theme_css(t):
    z = ["/* Tailwind v4: Klassen aus den Marken-Tokens. Nach tokens.css importieren. Erzeugt von scripts/tokens.py. */",
         "@theme inline {"]
    for r in t.gruppe("farbe.rolle"):
        z.append(f"  --color-{r}: var(--m-farbe-{r});")
    for f in t.gruppe("schrift.familie"):
        z.append(f"  --font-{f}: var(--m-schrift-{f});")
    for s in t.gruppe("schrift.web"):
        roh = t.roh(f"schrift.web.{s}")
        z.append(f"  --text-{s}: var(--m-text-{s}-groesse);")
        for k, n, tw in (("lineHeight", "zeilenhoehe", "line-height"), ("letterSpacing", "laufweite", "letter-spacing"),
                         ("fontWeight", "gewicht", "font-weight")):
            if isinstance(roh, dict) and k in roh:
                z.append(f"  --text-{s}--{tw}: var(--m-text-{s}-{n});")
    for r in t.gruppe("radius"):
        z.append(f"  --radius-{r}: var(--m-radius-{r});")
    for s in t.gruppe("schatten"):
        z.append(f"  --shadow-{s}: var(--m-schatten-{s});")
    for k in t.gruppe("bewegung.kurve"):
        z.append(f"  --ease-{k}: var(--m-kurve-{k});")
    for d in t.gruppe("bewegung.dauer"):
        z.append(f"  --transition-duration-{d}: var(--m-dauer-{d});")
    if "layout.container" in t.flach:
        z.append("  --container-inhalt: var(--m-layout-container);")
    if "layout.lesebreite" in t.flach:
        z.append("  --container-lese: var(--m-layout-lesebreite);")
    abstaende = [tl.px(t.wert(f"abstand.{a}")) for a in t.gruppe("abstand")]
    abstaende = [a for a in abstaende if a]
    if abstaende:
        z.append(f"  --spacing: {min(abstaende) / 16:g}rem;")
    if "layout.breakpoints" in t.flach:
        bp = t.wert("layout.breakpoints")
        if isinstance(bp, dict):
            for k, v in bp.items():
                z.append(f"  --breakpoint-{k}: {v};")
    z.append("}")
    return "\n".join(z) + "\n"


def druck_css(t):
    z = ["/* Druckwerte: nach tokens.css laden, gilt nur im Druck. Erzeugt von scripts/tokens.py. */",
         "@media print {", "  :root, [data-modus] {", "    color-scheme: light;"]
    for pfad in t.flach:
        ext = (t.flach[pfad].get("$extensions") or {}).get("modi") or {}
        if "druck" in ext:
            z.append(f"    {var_name(pfad)}: {css_wert(t, pfad, 'druck')};")
        elif pfad.startswith("farbe.rolle.") and ("hell" in ext or t.modi[0] == "hell"):
            # Druck ist hell: auch eine dunkel angezeigte Seite druckt mit den hellen Werten
            z.append(f"    {var_name(pfad)}: {css_wert(t, pfad, 'hell')};")
    z += ["    " + x.strip() for x in typo_zeilen(t, "schrift.druck")]
    z += ["  }", "}"]
    return "\n".join(z) + "\n"


def uebersicht(t):
    kopf = "| Token | " + " | ".join(t.modi) + " | Beschreibung |"
    z = [kopf, "|" + "---|" * (len(t.modi) + 2)]
    for pfad, tok in t.flach.items():
        werte = []
        for m in t.modi:
            try:
                v = t.wert(pfad, m)
            except tl.TokenFehler:
                v = "?"
            if isinstance(v, dict):
                v = " · ".join(f"{k} {x}" for k, x in v.items() if k != "fontFamily")
            elif isinstance(v, list):
                v = ", ".join(map(str, v))
            if pfad.startswith("farbe.") and isinstance(v, str) and v.startswith("color-mix"):
                try:
                    f = tl.farbe(v)
                    if f[3] < 1:
                        f = tl.auf_grund(f, tl.farbe(t.wert("farbe.rolle.grund", m)))
                    v = f"{v} (≈ {tl.hex_von(f)} auf grund)" if tl.farbe(v)[3] < 1 else f"{v} (≈ {tl.hex_von(f)})"
                except tl.TokenFehler:
                    pass
            werte.append(f"`{v}`")
        beschr = str(tok.get("$description", "")).replace("|", "/")
        z.append(f"| `{pfad}` | " + " | ".join(werte) + f" | {beschr} |")
    return "\n".join(z) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("tokens")
    ap.add_argument("--nur-css", action="store_true", help="nur tokens.css erzeugen (Stilrichtungen)")
    a = ap.parse_args()
    pfad = pathlib.Path(a.tokens)
    if not pfad.exists():
        print(f"Datei fehlt: {pfad}", file=sys.stderr)
        return 3
    try:
        t = tl.laden(pfad)
    except tl.TokenFehler as e:
        print(f"Fehler: {e}", file=sys.stderr)
        return 1
    fehler, hinweise = pruefen(t)
    ziel = pfad.parent
    stamm = pfad.name[: -len(".tokens.json")] if pfad.name.endswith(".tokens.json") else None
    (ziel / "tokens-befunde.json" if not stamm else ziel / f"{stamm}.befunde.json").write_text(
        json.dumps({"fehler": fehler, "hinweise": hinweise}, ensure_ascii=False, indent=2), encoding="utf-8")
    if not fehler or a.nur_css:
        try:
            (ziel / (f"{stamm}.css" if stamm else "tokens.css")).write_text(tokens_css(t), encoding="utf-8")
            if not a.nur_css:
                (ziel / "theme.css").write_text(theme_css(t), encoding="utf-8")
                (ziel / "druck.css").write_text(druck_css(t), encoding="utf-8")
                (ziel / "tokens-uebersicht.md").write_text(uebersicht(t), encoding="utf-8")
        except tl.TokenFehler as e:
            fehler.append(str(e))
    for f in fehler:
        print("FEHLER   " + f)
    for h in hinweise:
        print("HINWEIS  " + h)
    if fehler:
        print(f"{len(fehler)} Fehler. Erst beheben, dann weiter.")
        return 1
    print(f"Tokens in Ordnung ({len(t.flach)} Tokens, Modi: {', '.join(t.modi)}). Dateien in {ziel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
