#!/usr/bin/env python3
"""HTML-Dateien mit Headless-Chrome zu PDF/PNG rendern und prüfen.

Aufruf:
    python3 scripts/render.py pdf guide.html guide.pdf
    python3 scripts/render.py png guide.html guide.png --breite 1440 --hoehe 900 --voll --modus dunkel
    python3 scripts/render.py bogen druck.html bilder/ --selektor .seite
    python3 scripts/render.py pruefen druck.html --selektor .seite [--druck]

pdf      PDF mit CSS-Seitengröße (@page) und Hintergründen, wartet auf Schriften.
png      Screenshot; --modus setzt data-modus="hell|dunkel" am html-Element und das Farbschema.
bogen    Jedes Element (Standard .seite) einzeln als seite-01.png …, dazu kontaktbogen.png.
pruefen  Schreibt render-befunde.json neben die Eingabe: abgeschnittener Inhalt, Text über
         dem Seitenrand, leere Seiten, fehlende Bilder und Schriften. Exit 1 bei Befunden.

Exit-Codes: 0 ok, 1 Befunde (pruefen), 2 falscher Aufruf, 3 kein Chrome / Render-Fehler.
"""

import argparse
import datetime
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp import CDPFehler, Chrome, ChromeFehlt, datei_url, finde_chrome  # noqa: E402

ERSATZ = ("Ersatzweg ohne Chrome: die HTML-Datei in einem Browser öffnen und über "
          "„Drucken → Als PDF speichern“ (Hintergrundgrafiken an, Ränder „Keine“) ausgeben "
          "bzw. einen Screenshot machen.")

# Lazy-Bilder laden, auf Bilder und Schriften warten
LADEN_JS = r"""
(async () => {
  for (const img of document.images) if (img.loading === 'lazy') img.loading = 'eager';
  await Promise.all([...document.images].filter(i => !i.complete).map(i =>
    new Promise(r => { i.addEventListener('load', r); i.addEventListener('error', r); setTimeout(r, 8000); })));
  await document.fonts.ready;
  return document.images.length;
})()
"""

RECHTECKE_JS = r"""
((sel) => {
  scrollTo({top: 0, behavior: 'instant'});
  return [...document.querySelectorAll(sel)].map(e => {
    const r = e.getBoundingClientRect();
    return {x: r.left + scrollX, y: r.top + scrollY, width: r.width, height: r.height};
  });
})
"""

PRUEFEN_JS = r"""
(async (sel) => {
  const TOL = 1;
  const befunde = [], hinweise = [];
  let seiten = [...document.querySelectorAll(sel)];
  let ganzeSeite = false;
  if (!seiten.length) {
    hinweise.push('Kein Element passt auf „' + sel + '“, geprüft wurde die ganze Seite.');
    seiten = [document.body]; ganzeSeite = true;
  }
  const rund = (x) => Math.round(x * 10) / 10;
  const pfad = (el) => {
    const teile = []; let e = el;
    while (e && e.nodeType === 1 && e !== document.body && teile.length < 4) {
      let s = e.tagName.toLowerCase();
      if (e.id) { teile.unshift(s + '#' + e.id); break; }
      const kl = [...e.classList].slice(0, 2).join('.');
      teile.unshift(kl ? s + '.' + kl : s);
      e = e.parentElement;
    }
    return teile.join(' > ') || el.tagName.toLowerCase();
  };
  const textVon = (el) => (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 80);
  const seiteVon = (el) => { const i = seiten.findIndex(s => s.contains(el)); return i < 0 ? null : i + 1; };
  const sichtbar = (el) => !el.checkVisibility || el.checkVisibility({checkOpacity: true, checkVisibilityCSS: true, opacityProperty: true, visibilityProperty: true});
  const textRects = (wurzel) => {
    const aus = [];
    const w = document.createTreeWalker(wurzel, NodeFilter.SHOW_TEXT, {acceptNode: n => n.textContent.trim() ? 1 : 2});
    let n;
    while ((n = w.nextNode())) {
      if (!n.parentElement || !sichtbar(n.parentElement)) continue;
      const r = document.createRange(); r.selectNodeContents(n);
      for (const q of r.getClientRects()) if (q.width > 0 && q.height > 0) aus.push([n, q]);
    }
    return aus;
  };
  const ueberstand = (innen, aussen) => ({links: rund(aussen.left - innen.left), rechts: rund(innen.right - aussen.right),
    oben: rund(aussen.top - innen.top), unten: rund(innen.bottom - aussen.bottom)});
  const nurPositiv = (u) => Object.fromEntries(Object.entries(u).filter(([, v]) => v > TOL));

  // 1. Abgeschnittener Inhalt bei overflow hidden/clip
  for (const el of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(el);
    const hx = cs.overflowX === 'hidden' || cs.overflowX === 'clip';
    const hy = cs.overflowY === 'hidden' || cs.overflowY === 'clip';
    if (!hx && !hy) continue;
    if (el.clientWidth <= 1 || el.clientHeight <= 1 || !sichtbar(el)) continue;  // sr-only u. Ä.
    const ux = hx ? el.scrollWidth - el.clientWidth : 0, uy = hy ? el.scrollHeight - el.clientHeight : 0;
    if (ux <= TOL && uy <= TOL) continue;
    const box = el.getBoundingClientRect();
    const innenBox = {left: box.left + el.clientLeft, top: box.top + el.clientTop,
      right: box.left + el.clientLeft + el.clientWidth, bottom: box.top + el.clientTop + el.clientHeight};
    const versteckt = textRects(el).filter(([, q]) => Object.keys(nurPositiv(ueberstand(q, innenBox))).length);
    const eintrag = {art: 'abgeschnitten', seite: seiteVon(el), element: pfad(el), ueberstand_px: {x: rund(Math.max(0, ux)), y: rund(Math.max(0, uy))}};
    if (versteckt.length) {
      eintrag.text = versteckt.slice(0, 3).map(([n]) => n.textContent.trim().slice(0, 60)).join(' … ');
      befunde.push(eintrag);
    } else {
      hinweise.push('Überstand ohne Text (vermutlich Deko) in ' + eintrag.element + ' auf Seite ' + eintrag.seite + ': ' + JSON.stringify(eintrag.ueberstand_px));
    }
  }

  // 2. Text über den Rand seiner Seite
  if (!ganzeSeite) seiten.forEach((s, i) => {
    const sr = s.getBoundingClientRect();
    const gemeldet = new Set();
    for (const [n, q] of textRects(s)) {
      const u = nurPositiv(ueberstand(q, sr));
      if (!Object.keys(u).length || gemeldet.has(n.parentElement)) continue;
      gemeldet.add(n.parentElement);
      befunde.push({art: 'text_ueber_seitenrand', seite: i + 1, element: pfad(n.parentElement), text: n.textContent.trim().slice(0, 80), ueberstand_px: u});
    }
  });

  // 3. Leere Seiten
  if (!ganzeSeite) seiten.forEach((s, i) => {
    const text = (s.innerText || '').trim();
    const medien = [...s.querySelectorAll('img, svg, canvas, video, picture, object, iframe')].some(m => {
      const r = m.getBoundingClientRect(); return r.width > 2 && r.height > 2;
    });
    if (!text && !medien) befunde.push({art: 'leere_seite', seite: i + 1, element: pfad(s)});
  });

  // 4. Bilder ohne Daten
  for (const img of document.images) {
    if (!img.complete || img.naturalWidth === 0)
      befunde.push({art: 'bild_nicht_geladen', seite: seiteVon(img), element: pfad(img), src: (img.currentSrc || img.getAttribute('src') || '').slice(0, 200)});
  }

  // 5. Schriften: geladen? vorhanden? Schnitt vorhanden?
  const GENERISCH = /^(serif|sans-serif|monospace|cursive|fantasy|system-ui|ui-serif|ui-sans-serif|ui-monospace|ui-rounded|emoji|math|fangsong|-apple-system|blinkmacsystemfont|inherit|initial)$/i;
  const genutzt = new Map();
  for (const el of document.querySelectorAll('body, body *')) {
    let hatText = false;
    for (const n of el.childNodes) if (n.nodeType === 3 && n.textContent.trim()) { hatText = true; break; }
    if (!hatText || !sichtbar(el)) continue;
    const cs = getComputedStyle(el);
    const fam = cs.fontFamily.split(',')[0].trim().replace(/^["']|["']$/g, '');
    if (!genutzt.has(fam)) genutzt.set(fam, new Set());
    genutzt.get(fam).add(cs.fontWeight + '|' + cs.fontStyle);
  }
  const ctx = document.createElement('canvas').getContext('2d');
  const PROBE = 'mmmmmmmmmmlli WQ@#äöüß 0123456789';
  const breite = (f) => { ctx.font = '72px ' + f; return ctx.measureText(PROBE).width; };
  const installiert = (fam) => ['monospace', 'serif', 'sans-serif'].some(g => breite('"' + fam + '", ' + g) !== breite(g));
  const faces = [...document.fonts];
  const gewichtPasst = (ff, w) => {
    const t = String(ff.weight).replace('normal', '400').replace('bold', '700').split(/\s+/).map(Number);
    return t.length > 1 ? (w >= t[0] && w <= t[1]) : t[0] === w;
  };
  const schriften = [];
  for (const [fam, schnitte] of genutzt) {
    if (GENERISCH.test(fam)) { schriften.push({familie: fam, status: 'generisch'}); continue; }
    const passend = faces.filter(ff => ff.family.replace(/["']/g, '') === fam);
    if (!passend.length) {
      const da = installiert(fam);
      schriften.push({familie: fam, status: da ? 'lokal installiert' : 'fehlt'});
      if (!da) befunde.push({art: 'schrift_fehlt', familie: fam, hinweis: 'weder @font-face noch lokal installiert, Ersatzschrift wird genutzt'});
      continue;
    }
    let ok = true;
    for (const s of schnitte) {
      const [w, st] = s.split('|');
      const spec = (st === 'normal' ? '' : st + ' ') + w + ' 16px "' + fam + '"';
      try { await document.fonts.load(spec); } catch (e) {}
      const kandidaten = passend.filter(ff => (st === 'normal') === (ff.style === 'normal'));
      const geladen = kandidaten.filter(ff => ff.status === 'loaded');
      if (!geladen.length || !document.fonts.check(spec)) {
        ok = false;
        befunde.push({art: 'schrift_nicht_geladen', familie: fam, gewicht: w, stil: st,
          status: [...new Set(kandidaten.map(ff => ff.status))].join(', ') || 'kein passender Schnitt'});
      } else if (!geladen.some(ff => gewichtPasst(ff, Number(w)))) {
        ok = false;
        befunde.push({art: 'schriftschnitt_fehlt', familie: fam, gewicht: w, stil: st,
          hinweis: 'Gewicht nicht als Datei vorhanden, Chrome berechnet Ersatz (faux bold) oder nimmt den nächsten Schnitt'});
      }
    }
    schriften.push({familie: fam, status: ok ? 'geladen' : 'Problem', schnitte: [...schnitte]});
  }
  return {seitenzahl: ganzeSeite ? 0 : seiten.length, befunde, hinweise, schriften};
})
"""


def eingabe_pruefen(pfad):
    p = Path(pfad).expanduser()
    if not p.is_file():
        print("Eingabe nicht gefunden: {}".format(p), file=sys.stderr)
        sys.exit(2)
    return p.resolve()


def laden(c, html_pfad, warten):
    c.navigiere(datei_url(html_pfad), warten_s=warten)
    c.auswerten(LADEN_JS, timeout=30)


def modus_vorbereiten(c, modus):
    """Farbschema emulieren und data-modus schon vor den Skripten der Seite setzen."""
    if not modus:
        return
    c.farbschema("dark" if modus == "dunkel" else "light")
    # Das html-Element existiert beim Start des Dokuments noch nicht: per Observer setzen
    c.send("Page.addScriptToEvaluateOnNewDocument", {"source": """(() => {
  const setzen = () => document.documentElement ? (document.documentElement.setAttribute('data-modus', %s), true) : false;
  if (!setzen()) { const o = new MutationObserver(() => { if (setzen()) o.disconnect(); }); o.observe(document, {childList: true}); }
})();""" % json.dumps(modus)})


def modus_sichern(c, modus):
    """Nach dem Laden erneut setzen, falls ein Skript der Seite den Wert geändert hat."""
    if modus:
        c.auswerten("document.documentElement.getAttribute('data-modus') === {0} || "
                    "(document.documentElement.setAttribute('data-modus', {0}), "
                    "new Promise(r => setTimeout(r, 400)))".format(json.dumps(modus)))


def pdf_seiten(daten):
    return len(re.findall(rb"/Type\s*/Page[^s]", daten))


def befehl_pdf(args):
    eingabe = eingabe_pruefen(args.eingabe)
    with Chrome(datei_zugriff=True) as c:
        laden(c, eingabe, args.warten)
        info = c.pdf(args.ausgabe, querformat=True if args.querformat else None)
    with open(args.ausgabe, "rb") as f:
        seiten = pdf_seiten(f.read())
    print("PDF geschrieben: {} ({} Seiten, {} KB)".format(args.ausgabe, seiten, info["bytes"] // 1024))
    return 0


def befehl_png(args):
    eingabe = eingabe_pruefen(args.eingabe)
    with Chrome(datei_zugriff=True) as c:
        c.viewport(args.breite, args.hoehe, dpr=args.dpr)
        modus_vorbereiten(c, args.modus)
        laden(c, eingabe, args.warten)
        modus_sichern(c, args.modus)
        info = c.screenshot(args.ausgabe, voll=args.voll, max_hoehe=args.max_hoehe)
    print("PNG geschrieben: {} ({} × {} px){}".format(
        args.ausgabe, round(info.get("breite", args.breite) * args.dpr), round(info.get("hoehe", args.hoehe) * args.dpr),
        " – bei {} px abgeschnitten".format(args.max_hoehe) if info.get("abgeschnitten") else ""))
    return 0


def kontaktbogen_html(bilder, titel, spalten, miniatur):
    kacheln = "\n".join(
        '<figure><img src="{}" alt=""><figcaption>Seite {}</figcaption></figure>'.format(
            html.escape(datei_url(b)), i + 1) for i, b in enumerate(bilder))
    return """<!doctype html><html lang="de"><meta charset="utf-8"><style>
body {{ margin: 0; padding: 24px; background: #E9E9E9; color: #333; font: 13px/1.3 -apple-system, system-ui, sans-serif; }}
h1 {{ font-size: 14px; font-weight: 600; margin: 0 0 16px; }}
.raster {{ display: grid; grid-template-columns: repeat({spalten}, {miniatur}px); gap: 20px; align-items: start; }}
figure {{ margin: 0; }}
img {{ display: block; width: {miniatur}px; height: auto; background: #FFF; box-shadow: 0 1px 3px rgba(0,0,0,.2); }}
figcaption {{ margin-top: 6px; }}
</style><h1>{titel} · {n} Seiten</h1><div class="raster">{kacheln}</div></html>""".format(
        spalten=spalten, miniatur=miniatur, titel=html.escape(titel), n=len(bilder), kacheln=kacheln)


def pdf_rastern(eingabe, ziel, dpi=40):
    """Druckseiten eines PDFs als PNG über pdftoppm (Poppler). None, wenn pdftoppm fehlt."""
    werkzeug = shutil.which("pdftoppm")
    if not werkzeug:
        return None
    for alt in ziel.glob("seite-*.png"):
        alt.unlink()
    subprocess.run([werkzeug, "-r", str(dpi), "-png", str(eingabe), str(ziel / "seite")], check=True,
                   capture_output=True, timeout=600)
    return sorted(p.resolve() for p in ziel.glob("seite-*.png"))


def befehl_bogen(args):
    eingabe = eingabe_pruefen(args.eingabe)
    ziel = Path(args.ausgabeordner)
    ziel.mkdir(parents=True, exist_ok=True)
    bilder = []
    if eingabe.suffix.lower() == ".pdf":
        # Echte Druckseiten: zeigt halbleere Seiten und Umbrüche, die die HTML-Abschnitte nicht zeigen
        bilder = pdf_rastern(eingabe, ziel)
        if bilder is None:
            print("Für Druckseiten fehlt pdftoppm (Poppler). Ersatz: Kontaktbogen aus der HTML-Datei "
                  "(Abschnitte statt Druckseiten) oder das PDF selbst durchblättern.", file=sys.stderr)
            return 3
        with Chrome(datei_zugriff=True) as c:
            spalten = max(1, min(args.spalten, len(bilder)))
            tmp = tempfile.mkdtemp(prefix="bsg-bogen-")
            try:
                bogen = Path(tmp) / "kontaktbogen.html"
                bogen.write_text(kontaktbogen_html(bilder, eingabe.name, spalten, args.miniatur), encoding="utf-8")
                c.viewport(48 + spalten * args.miniatur + (spalten - 1) * 20, 600)
                laden(c, bogen, 0.2)
                c.screenshot(str(ziel / "kontaktbogen.png"), voll=True, max_hoehe=30000)
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
        print("{} Druckseiten als PNG und kontaktbogen.png in {}".format(len(bilder), ziel))
        return 0
    with Chrome(datei_zugriff=True) as c:
        c.viewport(args.breite, args.hoehe)
        modus_vorbereiten(c, args.modus)
        laden(c, eingabe, args.warten)
        modus_sichern(c, args.modus)
        rechtecke = c.auswerten(RECHTECKE_JS + "(" + json.dumps(args.selektor) + ")")
        if not rechtecke:
            print("Kein Element passt auf „{}“.".format(args.selektor), file=sys.stderr)
            return 2
        for i, r in enumerate(rechtecke, 1):
            if r["width"] < 1 or r["height"] < 1:
                print("Element {} hat keine Größe, übersprungen.".format(i), file=sys.stderr)
                continue
            pfad = ziel / "seite-{:02d}.png".format(i)
            c.screenshot(str(pfad), clip=r)
            bilder.append(pfad.resolve())
        # Kontaktbogen als temporäre Seite in derselben Chrome-Instanz
        spalten = max(1, min(args.spalten, len(bilder)))
        tmp = tempfile.mkdtemp(prefix="bsg-bogen-")
        try:
            bogen = Path(tmp) / "kontaktbogen.html"
            bogen.write_text(kontaktbogen_html(bilder, eingabe.name, spalten, args.miniatur), encoding="utf-8")
            c.viewport(48 + spalten * args.miniatur + (spalten - 1) * 20, 600)
            c.farbschema(None)
            laden(c, bogen, 0.2)
            c.screenshot(str(ziel / "kontaktbogen.png"), voll=True, max_hoehe=30000)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    print("{} Seiten als PNG und kontaktbogen.png in {}".format(len(bilder), ziel))
    return 0


def befehl_pruefen(args):
    eingabe = eingabe_pruefen(args.eingabe)
    with Chrome(datei_zugriff=True) as c:
        c.viewport(args.breite, args.hoehe)
        if args.druck:
            c.medientyp("print")
        laden(c, eingabe, args.warten)
        ergebnis = c.auswerten(PRUEFEN_JS + "(" + json.dumps(args.selektor) + ")", timeout=90)
        hinweise = ergebnis["hinweise"] + c.hinweise
    bericht = {"datei": str(eingabe),
               "zeit": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
               "selektor": args.selektor, "breite": args.breite, "medien": "print" if args.druck else "screen",
               "seitenzahl": ergebnis["seitenzahl"], "befunde": ergebnis["befunde"],
               "hinweise": hinweise, "schriften": ergebnis["schriften"]}
    aus = eingabe.parent / "render-befunde.json"
    with open(aus, "w", encoding="utf-8") as f:
        json.dump(bericht, f, ensure_ascii=False, indent=1)
    print("{} Abschnitte ({}) geprüft, {} Befunde → {}".format(bericht["seitenzahl"], args.selektor, len(bericht["befunde"]), aus))
    print("  Hinweis: geprüft werden HTML-Abschnitte, nicht Druckseiten. Halbleere Druckseiten zeigt: render.py bogen <guide>.pdf <ordner>")
    for b in bericht["befunde"]:
        details = {k: v for k, v in b.items() if k not in ("art", "seite")}
        print("  Seite {}: {} {}".format(b.get("seite") or "–", b["art"], json.dumps(details, ensure_ascii=False)))
    for h in hinweise:
        print("  Hinweis: " + h)
    return 1 if bericht["befunde"] else 0


def main():
    ap = argparse.ArgumentParser(description="HTML mit Headless-Chrome rendern und prüfen.")
    sub = ap.add_subparsers(dest="befehl")
    sub.required = True

    p = sub.add_parser("pdf", help="HTML → PDF")
    p.add_argument("eingabe")
    p.add_argument("ausgabe")
    p.add_argument("--querformat", action="store_true", help="nur nötig, wenn @page keine Größe setzt")
    p.add_argument("--warten", type=float, default=0.5)
    p.set_defaults(fn=befehl_pdf)

    p = sub.add_parser("png", help="HTML → PNG")
    p.add_argument("eingabe")
    p.add_argument("ausgabe")
    p.add_argument("--breite", type=int, default=1440)
    p.add_argument("--hoehe", type=int, default=900)
    p.add_argument("--voll", action="store_true", help="ganze Seite statt nur Viewport")
    p.add_argument("--max-hoehe", type=int, default=20000)
    p.add_argument("--modus", choices=["hell", "dunkel"])
    p.add_argument("--dpr", type=float, default=1, help="Pixeldichte, z. B. 2 für Retina")
    p.add_argument("--warten", type=float, default=0.5)
    p.set_defaults(fn=befehl_png)

    p = sub.add_parser("bogen", help="Elemente einzeln als PNG + Kontaktbogen")
    p.add_argument("eingabe")
    p.add_argument("ausgabeordner")
    p.add_argument("--selektor", default=".seite")
    p.add_argument("--breite", type=int, default=1440)
    p.add_argument("--hoehe", type=int, default=900)
    p.add_argument("--modus", choices=["hell", "dunkel"])
    p.add_argument("--spalten", type=int, default=4)
    p.add_argument("--miniatur", type=int, default=320, help="Breite je Miniatur in px")
    p.add_argument("--warten", type=float, default=0.5)
    p.set_defaults(fn=befehl_bogen)

    p = sub.add_parser("pruefen", help="Überlauf, leere Seiten, Bilder, Schriften prüfen")
    p.add_argument("eingabe")
    p.add_argument("--selektor", default=".seite")
    p.add_argument("--breite", type=int, default=1440)
    p.add_argument("--hoehe", type=int, default=900)
    p.add_argument("--druck", action="store_true", help="Druckmedien emulieren (@media print)")
    p.add_argument("--warten", type=float, default=0.5)
    p.set_defaults(fn=befehl_pruefen)

    args = ap.parse_args()
    if not finde_chrome():
        print("Kein Chrome, Chromium oder Edge gefunden (Pfad über CHROME_PATH setzbar). " + ERSATZ, file=sys.stderr)
        return 3
    try:
        return args.fn(args)
    except ChromeFehlt as e:
        print("{} {}".format(e, ERSATZ), file=sys.stderr)
        return 3
    except CDPFehler as e:
        print("Rendern fehlgeschlagen: {}".format(e), file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
