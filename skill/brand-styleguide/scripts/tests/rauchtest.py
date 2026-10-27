#!/usr/bin/env python3
"""Rauchtest: baut einen Mini-Lauf der erfundenen Testmarke und lässt alle Skripte einmal laufen.

Prüft nur, dass die Kette funktioniert (keine Abstürze, erwartete Exit-Codes), nicht die Qualität eines Guides.
Nutzt Chrome, wenn vorhanden; sonst werden die Render-Schritte übersprungen.

Aufruf (aus dem Skill-Ordner):  python3 -B scripts/tests/rauchtest.py
Exit 0: alles wie erwartet · 1: mindestens ein Schritt anders als erwartet
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

SKILL = pathlib.Path(__file__).resolve().parents[2]
S = SKILL / "scripts"

GUIDE = """## 0 · Über diesen Guide {#ueber}
Rauchtest. Quellen: Website [F1], Claim [F2], Quelle [Q1]. Eingeflossen sind frontend-design, Web Interface Guidelines, Impeccable und ui-ux-pro-max.

## 4 · Farbe {#farbe}
Grundfläche Kalk #F3F0EA [F1]. Akzent als Schrift auf hell ist vorläufig [vorläufig: W2].
{{farbtafel}}
### 4.2 Kontraste
{{kontrasttabelle}}

## 5 · Typografie {#typografie}
{{schriftmuster}}

## 6 · Raster, Raum und Form {#raster}
{{abstaende}}
{{radien}}
"""


def lauf(name, befehl, erwartet):
    r = subprocess.run([sys.executable, "-B"] + befehl, capture_output=True, text=True, timeout=600)
    ok = r.returncode in erwartet
    print(f"{'✓' if ok else '✗'} {name:<22} Exit {r.returncode} (erwartet {'/'.join(map(str, erwartet))})")
    if not ok:
        print("   " + (r.stderr or r.stdout).strip().replace("\n", "\n   ")[:1200])
    return ok


def main():
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="bsg-rauchtest-"))
    try:
        for d in ("tokens", "guide", "arbeit", "beispiele"):
            (tmp / d).mkdir()
        shutil.copy(S / "tests" / "testmarke.tokens.json", tmp / "tokens" / "tokens.json")
        (tmp / "lauf.json").write_text(json.dumps({
            "marke": "Kieselwerk", "slug": "kieselwerk", "module": [], "stack": False, "sprache": "de",
            "quellen": [{"id": "Q1", "art": "website", "ort": "https://kieselwerk.example"}],
            "achsen_soll": {"hell_dunkel": {"stufe": 1}},
            "entscheidungen": {"W2": {"runde": 1, "frage": "Akzent hell", "antwort": "b", "vorlaeufig": True}},
            "versionen": [{"version": "0.9", "datum": "01.01.2026", "aenderung": "Rauchtest"}]}), encoding="utf-8")
        (tmp / "arbeit" / "01-fakten.md").write_text(
            "| Nr. | Aussage | Fundstelle | Art |\n|---|---|---|---|\n| F1 | Kalk #F3F0EA | Test | gemessen |\n| F2 | Claim | Test | zitiert |\n",
            encoding="utf-8")
        (tmp / "arbeit" / "03-markenkern.md").write_text("# Markenkern\n", encoding="utf-8")
        (tmp / "guide" / "guide.md").write_text(GUIDE, encoding="utf-8")
        (tmp / "guide" / "marke.css").write_text(".cover{background:var(--m-farbe-akzent);color:var(--m-farbe-handlung-text)}", encoding="utf-8")
        tok = str(tmp / "tokens" / "tokens.json")
        ergebnisse = [
            lauf("werkzeuge", [str(S / "werkzeuge.py"), "--lauf", str(tmp)], {0}),
            lauf("tokens", [str(S / "tokens.py"), tok], {0}),
            lauf("kontrast (1 Verstoß)", [str(S / "kontrast.py"), tok], {1}),
            lauf("kontrast --paar", [str(S / "kontrast.py"), "--paar", "#8A660F", "#FFFFFF"], {0}),
            lauf("achsen", [str(S / "achsen.py"), str(tmp)], {0, 1}),
            lauf("guide_bauen", [str(S / "guide_bauen.py"), str(tmp)], {0}),
            lauf("pruefen (Befunde)", [str(S / "pruefen.py"), str(tmp)], {1}),
        ]
        sys.path.insert(0, str(S))
        from cdp import finde_chrome  # noqa: E402
        if finde_chrome():
            html_pfad, pdf = str(tmp / "guide" / "guide.html"), str(tmp / "guide" / "test.pdf")
            ergebnisse += [
                lauf("render pdf", [str(S / "render.py"), "pdf", html_pfad, pdf], {0}),
                lauf("render png", [str(S / "render.py"), "png", html_pfad, str(tmp / "test.png"), "--breite", "800"], {0}),
                lauf("render pruefen", [str(S / "render.py"), "pruefen", html_pfad], {0, 1}),
                lauf("render bogen (HTML)", [str(S / "render.py"), "bogen", html_pfad, str(tmp / "bogen")], {0}),
            ]
            if shutil.which("pdftoppm"):
                ergebnisse.append(lauf("render bogen (PDF)", [str(S / "render.py"), "bogen", pdf, str(tmp / "bogen-pdf")], {0}))
        else:
            print("– Chrome fehlt: Render-Schritte übersprungen")
        print(f"{sum(ergebnisse)}/{len(ergebnisse)} Schritte wie erwartet")
        return 0 if all(ergebnisse) else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
