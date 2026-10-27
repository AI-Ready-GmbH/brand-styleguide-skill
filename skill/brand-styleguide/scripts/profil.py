#!/usr/bin/env python3
"""Erneuert das Hausprofil falkemedia (references/profil-falkemedia.md) aus dem Markenhaus.

Nur für die Pflege des Skills, nicht für Läufe. Übernimmt aus markenhaus.md die Abschnitte
Markenliste, Schreibweisen, Ansprache, Gender-Regeln, Owner und Quellenhierarchie,
ohne Mail-Adressen und Drive-IDs (Datensparsamkeit: für Freigabevermerke reichen Namen).

Aufruf:
  python3 scripts/profil.py "<pfad>/markenhaus.md"
  python3 scripts/profil.py "<pfad>/markenhaus.md" --out references/profil-falkemedia.md
"""
import argparse
import datetime as dt
import pathlib
import re
import sys

ABSCHNITTE = [  # Überschriften-Anfang im Markenhaus → übernehmen
    "## 1. Markenliste",
    "## 2. Verbindliche Schreibweisen",
    "## 3. Ansprache",
    "## 4. Gender-Regeln",
    "## 5. Owner je Marke und Einheit",
    "## Quellenhierarchie bei Widersprüchen",
]

KOPF = """# Hausprofil falkemedia

> **Schnappschuss** aus dem Markenhaus der falkemedia Gruppe (Stand Markenhaus: {stand}, übernommen am {heute} mit `scripts/profil.py`).
> Führende Quelle bleibt das Markenhaus im Wissensbestand der Gruppe. Bei Zweifel: beim Owner der Marke nachfragen.

## Wann dieses Profil gilt

- **Nur für Marken der falkemedia Gruppe** (Markenliste unten). Bei allen anderen Marken wird es nicht geladen, auch nicht auszugsweise, und nichts daraus fließt in deren Guide.
- **Tochtergesellschaften mit eigener Markenidentität** (z. B. AI READY, AI-Ready GmbH) stehen nicht in der Markenliste. Frag im Briefing, ob das Profil gelten soll; ohne Antwort gilt es nicht (vorläufig markieren).
- Es ersetzt keine Quelle der Marke, sondern ergänzt sie: Schreibweisen, Ansprache, Gender-Regel und Owner gelten verbindlich. Widerspricht eine Quelle der Marke (Website, alte Vorgabe) dem Profil, ist das ein Widerspruch für Runde 1 mit der Empfehlung, dem Profil zu folgen.
- **Freigabe:** Den Guide gibt der Owner der Marke frei (Abschnitt 5) oder wer laut Quellenhierarchie zuständig ist. Frag im Briefing nach, wenn der User jemand anderes ist.
- **Verweise auf Dateien** (z. B. `marken/…/tone-of-voice.md`) zeigen in den Wissensbestand der Gruppe. Der User hat sie oft nicht; frag danach, statt sie vorauszusetzen.
- Mail-Adressen und interne Ablage-IDs sind bewusst entfernt.

"""


def abschnitte(text):
    """Teilt das Markdown an Überschriften zweiter Ebene."""
    teile, aktuell, titel = {}, [], None
    for zeile in text.splitlines():
        if zeile.startswith("## "):
            if titel:
                teile[titel] = "\n".join(aktuell).strip()
            titel, aktuell = zeile, [zeile]
        elif titel:
            aktuell.append(zeile)
    if titel:
        teile[titel] = "\n".join(aktuell).strip()
    return teile


def bereinigen(text):
    mail = r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+"
    text = re.sub(r"\s*\(\s*" + mail + r"\s*\)", "", text)  # „(adresse)“
    text = re.sub(r"\(\s*" + mail + r"\s*[,;]\s*", "(", text)  # „(adresse, Rolle)“
    # allein stehende Adresse statt Name: „r.bienge@…“ → „R. Bienge“
    text = re.sub(mail, lambda m: " ".join(t.capitalize() + ("." if len(t) == 1 else "")
                                            for t in m.group(0).split("@")[0].split(".")), text)
    text = re.sub(r"drive_id:\s*\S+", "", text)
    text = re.sub(r"\(\s*\)", "", text)
    text = re.sub(r"[ \t]+\|", " |", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)  # Obsidian-Links
    return text


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("markenhaus")
    ap.add_argument("--out", default=str(pathlib.Path(__file__).resolve().parent.parent / "references" / "profil-falkemedia.md"))
    a = ap.parse_args()
    quelle = pathlib.Path(a.markenhaus)
    if not quelle.exists():
        print(f"Markenhaus nicht gefunden: {quelle}", file=sys.stderr)
        return 3
    text = quelle.read_text(encoding="utf-8")
    stand = re.search(r"^stand:\s*(\S+)", text, re.M)
    teile = abschnitte(text)
    fehlend, raus = [], []
    for kopf in ABSCHNITTE:
        treffer = [t for t in teile if t.startswith(kopf)]
        if not treffer:
            fehlend.append(kopf)
            continue
        raus.append(bereinigen(teile[treffer[0]]))
    if fehlend:
        print("Abschnitte nicht gefunden: " + ", ".join(fehlend), file=sys.stderr)
        return 1
    kopf = KOPF.format(stand=stand.group(1) if stand else "unbekannt", heute=dt.date.today().strftime("%d.%m.%Y"))
    pathlib.Path(a.out).write_text(kopf + "\n\n".join(raus) + "\n", encoding="utf-8")
    print(f"Hausprofil geschrieben: {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
