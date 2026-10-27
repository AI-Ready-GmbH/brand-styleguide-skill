#!/usr/bin/env python3
"""Erkennt, was in dieser Umgebung geht: Dateizugriff, Chrome, Netz, Python, Node. Schreibt das Ergebnis in lauf.json.

Aufruf:
  python3 scripts/werkzeuge.py                       → nur anzeigen
  python3 scripts/werkzeuge.py --lauf <ordner>       → zusätzlich in <ordner>/lauf.json unter "werkzeuge"
  python3 scripts/werkzeuge.py --url https://…       → prüft, ob genau diese Website per Skript erreichbar ist

Tavily, eingebauter Browser, Web-Fetch und Subagenten sind Werkzeuge der Oberfläche, kein Skript kann sie sehen:
Prüf sie selbst in deiner Werkzeugliste und trag sie bei Bedarf in lauf.json nach.
"""
import argparse
import json
import os
import pathlib
import platform
import shutil
import subprocess
import sys
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))


def netz(url, sekunden=6):
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "brand-styleguide/0.1"})
        with urllib.request.urlopen(req, timeout=sekunden) as r:
            return r.status < 500
    except Exception as e:  # noqa: BLE001
        return f"nein ({type(e).__name__})"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lauf")
    ap.add_argument("--url", default="https://example.com")
    a = ap.parse_args()
    try:
        from cdp import finde_chrome  # noqa: WPS433
        chrome = finde_chrome()
    except Exception:  # noqa: BLE001
        chrome = None
    node = shutil.which("node")
    node_v = None
    if node:
        try:
            node_v = subprocess.run([node, "--version"], capture_output=True, text=True, timeout=5).stdout.strip()
        except Exception:  # noqa: BLE001
            node_v = "?"
    w = {
        "system": f"{platform.system()} {platform.release()}",
        "python": platform.python_version(),
        "node": node_v,
        "chrome": chrome,
        "netz_website": netz(a.url),
        "claude_code": bool(os.environ.get("CLAUDE_SKILL_DIR") or os.environ.get("CLAUDECODE")),
        "schreibbar": os.access(a.lauf or ".", os.W_OK),
    }
    w["empfehlung"] = []
    if not chrome:
        w["empfehlung"].append("Kein Chrome: messen.py --nur-css nutzen und Screenshots beim User erfragen; PDF über den Browser des Users.")
    if w["netz_website"] is not True:
        w["empfehlung"].append("Website per Skript nicht erreichbar: eingebautes Web-Fetch der Oberfläche nutzen oder Netzfreigabe klären.")
    if not w["empfehlung"]:
        w["empfehlung"].append("Alles da: messen.py und render.py mit Chrome nutzen.")
    print(json.dumps(w, ensure_ascii=False, indent=2))
    if a.lauf:
        p = pathlib.Path(a.lauf) / "lauf.json"
        p.parent.mkdir(parents=True, exist_ok=True)
        daten = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        daten["werkzeuge"] = w
        p.write_text(json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
