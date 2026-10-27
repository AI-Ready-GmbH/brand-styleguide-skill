#!/usr/bin/env python3
"""Baut guide/guide.html aus guide/guide.md: Cover, Inhalt, Kapitel je Seite, Tafeln aus den Tokens, Belege, Kolophon.

Gestaltung kommt aus tokens/tokens.css und guide/marke.css (vom Lauf geschrieben), die Mechanik aus
assets/guide/basis.css. Markdown-Regeln und Kurzbefehle: references/kapitel.md.

Aufruf:
  python3 scripts/guide_bauen.py <lauf>
  python3 scripts/guide_bauen.py <lauf> --entwurf      (Wasserzeichen „Entwurf“, z. B. für Runde 3)

Danach: python3 scripts/render.py pdf <lauf>/guide/guide.html <lauf>/guide/<MARKE>_Brand-Style-Guide_v<x>.pdf
Exit 0: gebaut · 1: gebaut mit Befunden (fehlende Belege, unbekannte Kurzbefehle) · 3: Dateien fehlen
"""
import argparse
import datetime as dt
import html
import json
import pathlib
import re
import shutil
import sys

HIER = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HIER))
import tokenlib as tl  # noqa: E402

BEFUNDE = []


# ---------- Markdown (bewusst klein: Absätze, Überschriften, Listen, Tabellen, Zitate, Code, Inline) ----------

def inline(text):
    t = html.escape(text, quote=False)
    t = re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*([^*\n]+)\*(?![*\w])", r"<em>\1</em>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', t)
    t = re.sub(r"\[vorläufig:\s*([A-Z]\d+)\]", r'<span class="vorlaeufig" title="nicht vom User entschieden">vorläufig · \1</span>', t)
    def verweis(x):
        x = x.strip()
        if x.startswith("F"):
            return f'<sup class="beleg"><a href="#beleg-{x}">{x}</a></sup>'
        return f'<sup class="beleg">{x}</sup>'  # Q: Quellen in Kapitel 0, W/S/M: Entscheidungen
    t = re.sub(r"\[((?:[FWSMQ]\d+)(?:\s*,\s*[FWSMQ]\d+)*)\]",
               lambda m: "".join(verweis(x) for x in m.group(1).split(",")), t)
    return t


def tabelle(zeilen):
    zellen = [[z.strip() for z in re.split(r"(?<!\\)\|", r.strip().strip("|"))] for r in zeilen]
    kopf, rumpf = zellen[0], [z for z in zellen[2:]]
    h = ["<table>", "<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in kopf) + "</tr></thead>", "<tbody>"]
    for r in rumpf:
        h.append("<tr>" + "".join(f"<td>{inline(c.replace(chr(92) + '|', '|'))}</td>" for c in r) + "</tr>")
    h += ["</tbody>", "</table>"]
    return "\n".join(h)


def markdown(text, kurzbefehl):
    zeilen = text.splitlines()
    raus, i = [], 0
    absatz = []

    def absatz_ende():
        if absatz:
            raus.append("<p>" + inline(" ".join(absatz)) + "</p>")
            absatz.clear()

    while i < len(zeilen):
        z = zeilen[i]
        s = z.strip()
        if not s:
            absatz_ende(); i += 1; continue
        m = re.fullmatch(r"\{\{\s*(.+?)\s*\}\}", s)
        if m:
            absatz_ende(); raus.append(kurzbefehl(m.group(1))); i += 1; continue
        if s.startswith("```"):
            absatz_ende(); j = i + 1; code = []
            while j < len(zeilen) and not zeilen[j].strip().startswith("```"):
                code.append(zeilen[j]); j += 1
            raus.append("<pre><code>" + html.escape("\n".join(code)) + "</code></pre>"); i = j + 1; continue
        if s.startswith("<"):
            absatz_ende(); j = i; block = []
            while j < len(zeilen) and zeilen[j].strip():
                block.append(zeilen[j]); j += 1
            raus.append("\n".join(block)); i = j; continue
        m = re.match(r"(#{2,4})\s+(.*)", s)
        if m:
            absatz_ende(); ebene = len(m.group(1))
            titel, kennung = m.group(2), None
            k = re.search(r"\s*\{#([a-z0-9-]+)\}\s*$", titel)
            if k:
                kennung, titel = k.group(1), titel[: k.start()]
            raus.append(("KAPITEL", ebene, titel.strip(), kennung)); i += 1; continue
        if s.startswith("|") and i + 1 < len(zeilen) and re.match(r"^\s*\|?\s*:?-{2,}", zeilen[i + 1]):
            absatz_ende(); j = i; block = []
            while j < len(zeilen) and zeilen[j].strip().startswith("|"):
                block.append(zeilen[j]); j += 1
            raus.append(tabelle(block)); i = j; continue
        if re.match(r"([-*]|\d+\.)\s+", s):
            absatz_ende(); geordnet = bool(re.match(r"\d+\.", s)); j = i; punkte = []
            while j < len(zeilen) and re.match(r"\s*([-*]|\d+\.)\s+", zeilen[j]):
                p = re.sub(r"^\s*([-*]|\d+\.)\s+", "", zeilen[j])
                p = re.sub(r"^\[ \]\s*", '<span class="kasten" aria-hidden="true"></span>', html.escape(p, quote=False)) if p.startswith("[ ]") else inline(p)
                punkte.append(p); j += 1
                while j < len(zeilen) and zeilen[j].startswith("  ") and zeilen[j].strip() and not re.match(r"\s*([-*]|\d+\.)\s+", zeilen[j]):
                    punkte[-1] += " " + inline(zeilen[j].strip()); j += 1
            tag = "ol" if geordnet else "ul"
            raus.append(f"<{tag}>" + "".join(f"<li>{p}</li>" for p in punkte) + f"</{tag}>"); i = j; continue
        if s.startswith(">"):
            absatz_ende(); j = i; block = []
            while j < len(zeilen) and zeilen[j].strip().startswith(">"):
                block.append(zeilen[j].strip()[1:].strip()); j += 1
            raus.append("<blockquote><p>" + inline(" ".join(block)) + "</p></blockquote>"); i = j; continue
        if s.startswith("# "):
            i += 1; continue  # Haupttitel kommt vom Cover
        absatz.append(s); i += 1
    absatz_ende()
    return raus


# ---------- Kurzbefehle ----------

class Tafeln:
    def __init__(self, lauf, t):
        self.lauf, self.t = lauf, t

    def __call__(self, befehl):
        name, _, arg = befehl.partition(":")
        name, arg = name.strip(), arg.strip()
        f = getattr(self, "k_" + name.replace("-", "_"), None)
        if not f:
            BEFUNDE.append(f"Unbekannter Kurzbefehl {{{{{befehl}}}}}")
            return f'<p class="befund">Unbekannter Kurzbefehl: {html.escape(befehl)}</p>'
        if self.t is None and name not in ("bild", "beispiel", "logo"):
            BEFUNDE.append(f"{{{{{befehl}}}}} braucht tokens/tokens.json")
            return '<p class="befund">Tokens fehlen</p>'
        return f(arg)

    def _md_datei(self, rel):
        p = self.lauf / rel
        if not p.exists():
            BEFUNDE.append(f"Datei fehlt für Tafel: {rel}")
            return '<p class="befund">fehlt: ' + html.escape(rel) + "</p>"
        zeilen = [z for z in p.read_text(encoding="utf-8").splitlines() if z.strip().startswith("|")]
        return tabelle(zeilen) if len(zeilen) >= 2 else ""

    def k_kontrasttabelle(self, _):
        return '<div class="tafel tafel-kontrast">' + self._md_datei("tokens/kontrast.md") + "</div>"

    def k_tokens_uebersicht(self, _):
        return '<div class="tafel tafel-tokens">' + self._md_datei("tokens/tokens-uebersicht.md") + "</div>"

    def k_farbtafel(self, _):
        t = self.t
        teile = ['<div class="tafel farbtafel">', '<h4 class="tafel-titel">Basisfarben</h4>', '<div class="farben">']
        for n in t.gruppe("farbe.basis"):
            tok = t.flach[f"farbe.basis.{n}"]
            wert = t.wert(f"farbe.basis.{n}")
            teile.append(f'<figure class="farbe"><span class="feld" style="background:{wert}"></span>'
                         f'<figcaption><strong>{html.escape(n)}</strong><span>{wert}</span>'
                         f'<span class="leise">{inline(str(tok.get("$description", "")))}</span></figcaption></figure>')
        teile.append("</div>")
        for modus in t.modi:
            teile.append(f'<h4 class="tafel-titel">Rollen · {html.escape(modus)}</h4><div class="farben farben-rollen">')
            for r in t.gruppe("farbe.rolle"):
                try:
                    f = tl.farbe(t.wert(f"farbe.rolle.{r}", modus))
                    grund = tl.farbe(t.wert("farbe.rolle.grund", modus))
                    hx = tl.hex_von(tl.auf_grund(f, grund) if f[3] < 1 else f)
                except tl.TokenFehler:
                    hx = "?"
                teile.append(f'<figure class="farbe"><span class="feld" style="background:{hx}"></span>'
                             f'<figcaption><strong>{html.escape(r)}</strong><span>{hx}</span></figcaption></figure>')
            teile.append("</div>")
        teile.append("</div>")
        return "\n".join(teile)

    def k_schriftmuster(self, arg):
        gruppe = "schrift.druck" if arg == "druck" else "schrift.web"
        t = self.t
        teile = ['<div class="tafel schriftmuster">']
        for st in t.gruppe(gruppe):
            v = t.wert(f"{gruppe}.{st}")
            if not isinstance(v, dict):
                continue
            fam = v.get("fontFamily")
            fam_css = fam if isinstance(fam, str) else ", ".join(f'"{x}"' if " " in x else x for x in (fam or []))
            versal = (t.flach[f"{gruppe}.{st}"].get("$extensions") or {}).get("versalien")
            stil = (f"font-family:{fam_css};font-size:{v.get('fontSize')};font-weight:{v.get('fontWeight', 400)};"
                    f"line-height:{v.get('lineHeight', 1.3)};letter-spacing:{v.get('letterSpacing', 'normal')};"
                    + ("text-transform:uppercase;" if versal else ""))
            angabe = " · ".join(str(x) for x in (v.get("fontSize"), v.get("fontWeight"), v.get("lineHeight"), v.get("letterSpacing")) if x)
            erste = fam[0] if isinstance(fam, list) and fam else fam_css
            teile.append(f'<div class="muster"><div class="muster-meta"><strong>{st}</strong><span>{html.escape(str(erste))}</span>'
                         f'<span>{html.escape(angabe)}</span></div><div class="muster-text" style="{html.escape(stil)}">'
                         f'{html.escape(self.beispielsatz(st))}</div></div>')
        teile.append("</div>")
        return "\n".join(teile)

    def beispielsatz(self, stufe):
        saetze = (self.t.marke.get("beispielsaetze") or {})
        return saetze.get(stufe) or saetze.get("standard") or "Gestaltung, die man wiedererkennt"

    def k_abstaende(self, _):
        teile = ['<div class="tafel abstaende">']
        for a in self.t.gruppe("abstand"):
            w = self.t.wert(f"abstand.{a}")
            teile.append(f'<div class="abstand"><span class="balken" style="width:{w}"></span><span>{a} · {w}</span></div>')
        return "\n".join(teile + ["</div>"])

    def k_radien(self, _):
        teile = ['<div class="tafel radien">']
        for r in self.t.gruppe("radius"):
            w = self.t.wert(f"radius.{r}")
            teile.append(f'<figure class="radius"><span class="form" style="border-radius:{w}"></span><figcaption>{r} · {w}</figcaption></figure>')
        return "\n".join(teile + ["</div>"])

    def k_bild(self, arg):
        pfad, _, unterschrift = arg.partition("|")
        rel = self._kopieren(pfad.strip())
        return (f'<figure class="bild"><img src="{html.escape(rel)}" alt="{html.escape(unterschrift.strip())}">'
                f'<figcaption>{inline(unterschrift.strip())}</figcaption></figure>')

    def k_beispiel(self, arg):
        rel = self._kopieren(f"beispiele/{arg.strip()}.png")
        return f'<figure class="beispiel"><img src="{html.escape(rel)}" alt="Anwendungsbeispiel {html.escape(arg)}"></figure>'

    def k_logo(self, arg):
        pfad, _, rolle = arg.partition("|")
        rel = self._kopieren(pfad.strip())
        rolle = rolle.strip() or "grund"
        return (f'<figure class="logo-feld" style="background:var(--m-farbe-{html.escape(rolle)})">'
                f'<img src="{html.escape(rel)}" alt="Logo auf {html.escape(rolle)}"><figcaption>auf {html.escape(rolle)}</figcaption></figure>')

    def _kopieren(self, rel):
        quelle = self.lauf / rel
        if not quelle.exists():
            BEFUNDE.append(f"Bild fehlt: {rel}")
            return rel
        return "../" + rel


# ---------- Seiten ----------

def belege(lauf, md):
    """Belege-Anhang: alle im Guide genannten F-Nummern mit Aussage und Fundstelle aus dem Faktenblatt."""
    genannt = sorted(set(re.findall(r"\bF(\d+)\b", " ".join(re.findall(r"\[([^\]]+)\]", md)))), key=int)
    fakten = {}
    blatt = lauf / "arbeit" / "01-fakten.md"
    if blatt.exists():
        for z in blatt.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\|\s*F(\d+)\s*\|(.*)\|\s*$", z)
            if m:
                fakten[m.group(1)] = [c.strip() for c in m.group(2).split("|")]
    zeilen = []
    for n in genannt:
        if n not in fakten:
            BEFUNDE.append(f"Beleg F{n} steht im Guide, aber nicht im Faktenblatt")
            zeilen.append(f'<tr id="beleg-F{n}"><td>F{n}</td><td class="befund">fehlt im Faktenblatt</td><td></td></tr>')
            continue
        f = fakten[n] + ["", "", ""]
        zeilen.append(f'<tr id="beleg-F{n}"><td>F{n}</td><td>{inline(f[0])}</td><td>{inline(f[1])}</td></tr>')
    if not zeilen:
        return ""
    return ('<section class="seite anhang" id="belege"><h2 class="kapitel-titel">Belege</h2>'
            '<p class="leise">Aussagen über die Marke und ihre Fundstellen (Faktenblatt des Laufs).</p>'
            '<table><thead><tr><th>Nr.</th><th>Aussage</th><th>Fundstelle</th></tr></thead><tbody>'
            + "".join(zeilen) + "</tbody></table></section>")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("lauf")
    ap.add_argument("--entwurf", action="store_true")
    a = ap.parse_args()
    lauf = pathlib.Path(a.lauf).resolve()
    md_pfad = lauf / "guide" / "guide.md"
    if not md_pfad.exists():
        print(f"Datei fehlt: {md_pfad}", file=sys.stderr)
        return 3
    lj = json.loads((lauf / "lauf.json").read_text(encoding="utf-8")) if (lauf / "lauf.json").exists() else {}
    tok_pfad = lauf / "tokens" / "tokens.json"
    t = tl.laden(tok_pfad) if tok_pfad.exists() else None
    md = md_pfad.read_text(encoding="utf-8")

    # Basis-CSS neben den Guide kopieren, damit HTML und PDF allein funktionieren
    shutil.copy(HIER.parent / "assets" / "guide" / "basis.css", lauf / "guide" / "basis.css")
    if not (lauf / "guide" / "marke.css").exists():
        BEFUNDE.append("guide/marke.css fehlt: der Guide hat noch keine Gestaltung der Marke (kapitel.md, Abschnitt 6)")

    teile = markdown(md, Tafeln(lauf, t))
    marke = lj.get("marke") or (t.marke.get("name") if t else "Marke")
    versionen = lj.get("versionen") or []
    v = versionen[-1] if versionen else {"version": (t.marke.get("version") if t else "0.1"), "datum": dt.date.today().strftime("%d.%m.%Y")}
    freigabe = v.get("freigabe") or ("Entwurf, nicht freigegeben" if a.entwurf or not v.get("freigabe") else "")

    # Kapitel in Seiten gliedern, Inhaltsverzeichnis sammeln
    seiten, inhalt, aktuell = [], [], None
    for teil in teile:
        if isinstance(teil, tuple):
            _, ebene, titel, kennung = teil
            if ebene == 2:
                if aktuell:
                    seiten.append(aktuell)
                nr, _, name = titel.partition("·")
                nr, name = (nr.strip(), name.strip()) if name else ("", titel)
                kid = kennung or re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
                inhalt.append((nr, name, kid))
                aktuell = [f'<section class="seite kapitel-seite" id="{kid}" data-kapitel="{kid}">',
                           f'<header class="kapitel"><span class="kapitel-nr">{html.escape(nr)}</span>'
                           f'<h2 class="kapitel-titel">{inline(name)}</h2></header>']
            else:
                if aktuell is None:
                    aktuell = ['<section class="seite">']
                aktuell.append(f"<h{ebene}>{inline(titel)}</h{ebene}>")
        else:
            if aktuell is None:
                aktuell = ['<section class="seite">']
            aktuell.append(teil)
    if aktuell:
        seiten.append(aktuell)

    kopfzeile = f'<div class="laufkopf"><span>{html.escape(marke)} · Brand &amp; Style Guide</span><span>Version {html.escape(str(v.get("version", "")))}</span></div>'
    cover = (f'<section class="seite cover"><div class="cover-marke">{html.escape(marke)}</div>'
             f'<h1 class="cover-titel">Brand &amp; Style Guide</h1>'
             f'<div class="cover-meta"><span>Version {html.escape(str(v.get("version", "")))} · {html.escape(str(v.get("datum", "")))}</span>'
             f'<span>{html.escape(freigabe)}</span></div></section>')
    toc = ['<section class="seite inhalt"><h2 class="kapitel-titel">Inhalt</h2><ol class="inhaltsliste">']
    for nr, name, kid in inhalt:
        toc.append(f'<li><a href="#{kid}"><span class="nr">{html.escape(nr)}</span><span>{inline(name)}</span></a></li>')
    toc.append("</ol></section>")
    kolophon = ('<section class="seite kolophon"><div class="kolophon-text">'
                f'<p><strong>{html.escape(marke)} · Brand &amp; Style Guide</strong>, Version {html.escape(str(v.get("version", "")))}, {html.escape(str(v.get("datum", "")))}</p>'
                f'<p>{html.escape(freigabe)}</p>'
                '<p>Erstellt mit dem Skill brand-styleguide von AI READY. Gestaltungsregeln der Design-Skills frontend-design (Anthropic), '
                'Web Interface Guidelines (Vercel), Impeccable (Paul Bakaus) und ui-ux-pro-max sind eingeflossen, wo sie zur Marke passen; '
                'Abweichungen stehen in Kapitel 0.</p></div></section>')

    rumpf = [cover, "\n".join(toc)] + ["\n".join(s + ["</section>"]) for s in seiten]
    rumpf.append(belege(lauf, md))
    rumpf.append(kolophon)
    modus = (t.modi[0] if t else "hell")
    sprache = lj.get("sprache", "de")
    dokument = f"""<!doctype html>
<html lang="{sprache}" data-modus="{modus}"{' data-entwurf' if a.entwurf else ''}>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(marke)} · Brand &amp; Style Guide</title>
<link rel="stylesheet" href="../tokens/tokens.css">
<link rel="stylesheet" href="basis.css">
<link rel="stylesheet" href="marke.css">
</head>
<body>
{kopfzeile}
{chr(10).join(x for x in rumpf if x)}
</body>
</html>
"""
    ziel = lauf / "guide" / "guide.html"
    ziel.write_text(dokument, encoding="utf-8")
    for b in BEFUNDE:
        print("BEFUND  " + b)
    print(f"Guide gebaut: {ziel} ({len(inhalt)} Kapitel)")
    return 1 if BEFUNDE else 0


if __name__ == "__main__":
    sys.exit(main())
