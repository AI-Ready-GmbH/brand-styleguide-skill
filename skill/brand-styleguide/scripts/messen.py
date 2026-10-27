#!/usr/bin/env python3
"""Misst eine Website: Farben, Schriften, Radien, Schatten, Abstände, Bewegung,
CSS-Variablen, Schriftdateien, Logo-Kandidaten. Ergebnis: messung.json + messung.md
(Faktenblatt-Grundlage) und Screenshots je Breite und Modus.

Aufruf:
    python3 scripts/messen.py https://example.org --out lauf/messung
    python3 scripts/messen.py https://example.org --out lauf/messung --breiten 375,1440 --modi hell,dunkel
    python3 scripts/messen.py https://example.org --out lauf/messung --seiten https://example.org/preise,https://example.org/blog
    python3 scripts/messen.py https://example.org --out lauf/messung --nur-css    # ohne Browser, Schätzung

Ohne Chrome (oder mit --nur-css) liest das Skript HTML und CSS als Text (methode "css-text").
Exit-Codes: 0 ok, 2 falscher Aufruf, 3 weder Chrome-Messung noch Netz möglich.
"""

import argparse
import colorsys
import datetime
import json
import math
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cdp import CDPFehler, Chrome, finde_chrome  # noqa: E402

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36 brand-styleguide-messung")

# ---------------------------------------------------------------- JavaScript im Seitenkontext

# Einmal je Seite: Stylesheets lesen (Variablen, @font-face, Dunkel-Regeln)
SCAN_JS = r"""
(() => {
  const SEL = /^(?:html|:root|:host)?(?:\.(?:dark|light|theme-dark|theme-light)|\[data-(?:theme|modus|mode)[^\]]*\]|:root)*$/i;
  const variablen = [], fontface = [], nichtLesbar = [];
  const klassen = {};
  let mediaDunkel = 0;
  const bedingung = (rule) => {
    const t = []; let p = rule.parentRule;
    while (p) {
      const typ = p.constructor.name;
      if (typ === 'CSSMediaRule') t.unshift('@media ' + p.conditionText);
      else if (typ === 'CSSSupportsRule') t.unshift('@supports ' + p.conditionText);
      else if (typ === 'CSSContainerRule') t.unshift('@container ' + p.conditionText);
      else if (typ === 'CSSLayerBlockRule') t.unshift('@layer ' + p.name);
      else if (p.selectorText) t.unshift(p.selectorText);
      p = p.parentRule;
    }
    return t.join(' ');
  };
  const lauf = (rules, quelle) => {
    for (const rule of rules) {
      const typ = rule.constructor.name;
      if (typ === 'CSSImportRule') {
        try { if (rule.styleSheet) lauf(rule.styleSheet.cssRules, rule.href); }
        catch (e) { nichtLesbar.push(rule.href); }
        continue;
      }
      if (typ === 'CSSFontFaceRule') {
        const s = rule.style;
        fontface.push({familie: s.getPropertyValue('font-family').replace(/["']/g, '').trim(),
          src: s.getPropertyValue('src').slice(0, 400), gewicht: s.getPropertyValue('font-weight') || '',
          stil: s.getPropertyValue('font-style') || '', quelle});
        continue;
      }
      if (typ === 'CSSMediaRule' && /prefers-color-scheme/.test(rule.conditionText || '')) mediaDunkel++;
      if (rule.selectorText !== undefined) {
        const sel = rule.selectorText;
        for (const [k, re] of [['.dark', /\.dark(?![-\w])/], ['.light', /\.light(?![-\w])/], ['.theme-dark', /\.theme-dark(?![-\w])/],
                               ['.theme-light', /\.theme-light(?![-\w])/], ['[data-theme', /\[data-theme/], ['[data-modus', /\[data-modus/], ['[data-mode', /\[data-mode\b/]])
          if (re.test(sel)) klassen[k] = (klassen[k] || 0) + 1;
        const teile = sel.split(/,(?![^(]*\))/).map(s => s.trim());
        if (teile.some(t => t && SEL.test(t))) {
          const vars = {}; let n = 0;
          for (let i = 0; i < rule.style.length; i++) {
            const name = rule.style[i];
            if (name.startsWith('--')) { vars[name] = rule.style.getPropertyValue(name).trim(); n++; }
          }
          if (n) variablen.push({selektor: sel.slice(0, 160), bedingung: bedingung(rule), quelle, variablen: vars});
        }
      }
      if (rule.cssRules && rule.cssRules.length) lauf(rule.cssRules, quelle);
    }
  };
  const blaetter = [...document.styleSheets, ...(document.adoptedStyleSheets || [])];
  for (const sheet of blaetter) {
    const quelle = sheet.href || 'inline <style>';
    let rules;
    try { rules = sheet.cssRules; } catch (e) { nichtLesbar.push(sheet.href); continue; }
    if (sheet.media && /prefers-color-scheme/.test(sheet.media.mediaText)) mediaDunkel++;
    lauf(rules, quelle);
  }
  const namen = [...new Set(variablen.flatMap(v => Object.keys(v.variablen)))];
  return {variablen, fontface, nicht_lesbar: nichtLesbar.filter(Boolean), media_dunkel: mediaDunkel,
          klassen_dunkel: klassen, variablen_namen: namen.slice(0, 600)};
})()
"""

ZUSTAND_JS = r"""
(() => {
  const h = document.documentElement;
  // Wirksamer Seitengrund: html, body, dann vom Element in der Bildmitte aufwärts
  const cv = document.createElement('canvas'); cv.width = cv.height = 1;
  const ctx = cv.getContext('2d', {willReadFrequently: true});
  const rgba = (w) => { ctx.clearRect(0, 0, 1, 1); ctx.fillStyle = 'rgba(0,0,0,0)'; ctx.fillStyle = w; ctx.fillRect(0, 0, 1, 1); return ctx.getImageData(0, 0, 1, 1).data; };
  const kette = [h, document.body];
  let el = document.elementFromPoint(innerWidth / 2, innerHeight * 0.75);
  const innen = []; while (el && el !== document.body && el !== h) { innen.push(el); el = el.parentElement; }
  kette.push(...innen.reverse());
  let grund = null;
  for (const e of kette) { const d = rgba(getComputedStyle(e).backgroundColor); if (d[3] > 128) { grund = d; } }
  if (!grund) grund = matchMedia('(prefers-color-scheme: dark)').matches && getComputedStyle(h).colorScheme.includes('dark') ? [18, 18, 18, 255] : [255, 255, 255, 255];
  const lin = (c) => { c /= 255; return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; };
  const lum = 0.2126 * lin(grund[0]) + 0.7152 * lin(grund[1]) + 0.0722 * lin(grund[2]);
  return {klasse: (h.getAttribute('class') || '').slice(0, 200), data_theme: h.dataset.theme || null,
    data_modus: h.dataset.modus || null, data_mode: h.dataset.mode || null,
    grund: '#' + [grund[0], grund[1], grund[2]].map(v => v.toString(16).padStart(2, '0')).join('').toUpperCase(),
    grund_luminanz: Math.round(lum * 1000) / 1000, dunkel: lum < 0.2,
    media_dunkel: matchMedia('(prefers-color-scheme: dark)').matches};
})()
"""

# Modus per Klasse/Attribut erzwingen (für Seiten mit Umschalter statt Medienregel)
MODUS_SETZEN_JS = r"""
((dunkel, klassen) => {
  const h = document.documentElement;
  if (klassen['.dark']) h.classList.toggle('dark', dunkel);
  if (klassen['.light']) h.classList.toggle('light', !dunkel);
  if (klassen['.theme-dark']) h.classList.toggle('theme-dark', dunkel);
  if (klassen['.theme-light']) h.classList.toggle('theme-light', !dunkel);
  if (klassen['[data-theme']) h.setAttribute('data-theme', dunkel ? 'dark' : 'light');
  if (klassen['[data-mode']) h.setAttribute('data-mode', dunkel ? 'dark' : 'light');
  if (klassen['[data-modus']) h.setAttribute('data-modus', dunkel ? 'dunkel' : 'hell');
  return true;
})
"""

DURCHSCROLLEN_JS = r"""
(async (maxH) => {
  const se = document.scrollingElement || document.documentElement;
  for (const img of document.images) { if (img.loading === 'lazy') img.loading = 'eager'; }
  const h = Math.min(se.scrollHeight, maxH);
  const schritt = Math.max(200, innerHeight * 0.8);
  for (let y = 0; y < h; y += schritt) {
    scrollTo({top: y, behavior: 'instant'});
    await new Promise(r => setTimeout(r, 120));
  }
  scrollTo({top: 0, behavior: 'instant'});
  await Promise.all([...document.images].filter(i => !i.complete).map(i =>
    new Promise(r => { i.addEventListener('load', r); i.addEventListener('error', r); setTimeout(r, 3000); })));
  await new Promise(r => setTimeout(r, 500));
  return se.scrollHeight;
})
"""

MESS_JS = r"""
(async (opt) => {
  const MAX = opt.max_elemente;
  const rund = (x, n = 1) => Math.round(x * 10 ** n) / 10 ** n;
  // Farben auf #RRGGBB + Deckkraft bringen (auch oklch, color-mix usw. über Canvas)
  const cv = document.createElement('canvas'); cv.width = cv.height = 1;
  const ctx = cv.getContext('2d', {willReadFrequently: true});
  const cache = new Map();
  const zuHex = (a) => '#' + a.map(v => Math.round(Math.max(0, Math.min(255, v))).toString(16).padStart(2, '0')).join('').toUpperCase();
  const pixel = (wert) => {
    ctx.clearRect(0, 0, 1, 1); ctx.fillStyle = '#000'; ctx.fillStyle = wert; ctx.fillRect(0, 0, 1, 1);
    return ctx.getImageData(0, 0, 1, 1).data;
  };
  const farbe = (wert) => {
    if (!wert || wert === 'none' || wert === 'transparent' || /^(url|var)\(/.test(wert)) return null;
    if (cache.has(wert)) return cache.get(wert);
    let erg = null;
    const m = wert.match(/^rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)(?:\s*[,\/]\s*([\d.]+%?))?\s*\)$/);
    if (m) {
      const a = m[4] === undefined ? 1 : (m[4].endsWith('%') ? parseFloat(m[4]) / 100 : parseFloat(m[4]));
      erg = {hex: zuHex([m[1], m[2], m[3]].map(parseFloat)), alpha: rund(a, 2)};
    } else if (CSS.supports('color', wert)) {
      let d = pixel(wert);
      const alpha = rund(d[3] / 255, 2);
      if (alpha < 1 && /\/\s*[\d.]+%?\s*\)$/.test(wert)) d = pixel(wert.replace(/\/\s*[\d.]+%?\s*\)$/, ')'));
      erg = {hex: zuHex([d[0], d[1], d[2]]), alpha};
    }
    cache.set(wert, erg);
    return erg;
  };
  // Farbfunktionen in Schatten/Verläufen durch #RRGGBB (bzw. #RRGGBB/xx %) ersetzen
  const FARB_FN = /(?:color|rgba?|hsla?|oklch|oklab|lab|lch|hwb)\([^()]*\)/g;
  const farbenErsetzen = (t) => t.replace(FARB_FN, (m) => { const f = farbe(m); return f ? f.hex + (f.alpha < 1 ? '/' + Math.round(f.alpha * 100) + '%' : '') : m; });
  const nurTransparent = (t) => { const fs = t.match(FARB_FN) || []; return fs.length > 0 && fs.every(m => { const f = farbe(m); return f && f.alpha === 0; }); };
  const neu = () => new Map();
  const add = (map, k, w = 1) => map.set(k, (map.get(k) || 0) + w);
  const summe = (map) => [...map.values()].reduce((a, b) => a + b, 0) || 1;
  const farbListe = (map, n = 20) => { const g = summe(map); return [...map.entries()].sort((a, b) => b[1] - a[1]).slice(0, n)
      .map(([k, v]) => { const [hex, alpha] = k.split('@'); return {hex, deckkraft: parseFloat(alpha), anteil: rund(v / g * 100)}; }); };
  const zaehlListe = (map, n = 20, schluessel = 'wert') => [...map.entries()].sort((a, b) => b[1] - a[1]).slice(0, n)
      .map(([k, v]) => ({[schluessel]: k, anzahl: v}));
  const erste = (familie) => familie.split(',')[0].trim().replace(/^["']|["']$/g, '');
  const sichtbarOk = (el) => !el.checkVisibility || el.checkVisibility({checkOpacity: true, checkVisibilityCSS: true, opacityProperty: true, visibilityProperty: true});
  const ms = (d) => d.endsWith('ms') ? parseFloat(d) : parseFloat(d) * 1000;

  const SKIP = new Set(['script', 'style', 'noscript', 'template', 'link', 'meta', 'head', 'title', 'br', 'wbr', 'source', 'track', 'param']);
  const SVG_FORM = new Set(['path', 'rect', 'circle', 'ellipse', 'polygon', 'polyline', 'line', 'text', 'tspan', 'use']);
  const docBreite = document.documentElement.scrollWidth;

  const text = neu(), flaechen = neu(), raender = neu(), svg = neu(), verlaeufe = neu();
  const schriften = new Map();
  const radien = neu(), schatten = neu(), padding = neu(), margin = neu(), gap = neu();
  const dauer = neu(), kurven = neu(), eigenschaften = neu(), animationen = neu();
  let pillen = 0, gesamt = 0, gemessen = 0;

  const alle = [document.documentElement, document.body, ...document.body.querySelectorAll('*')];
  for (const el of alle) {
    const tag = el.tagName.toLowerCase();
    if (SKIP.has(tag)) continue;
    gesamt++;
    if (gemessen >= MAX) continue;
    const r = el.getBoundingClientRect();
    if (r.width <= 1 && r.height <= 1) continue;
    if (r.width <= 0 || r.height <= 0) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility !== 'visible' || parseFloat(cs.opacity) === 0) continue;
    if (!sichtbarOk(el)) continue;
    gemessen++;
    let zeichen = 0;
    for (const n of el.childNodes) if (n.nodeType === 3) zeichen += n.textContent.trim().length;

    // Farben
    if (zeichen > 0) { const f = farbe(cs.color); if (f && f.alpha > 0) add(text, f.hex + '@' + f.alpha, zeichen); }
    const flaeche = Math.min(r.width, docBreite) * r.height;
    const bg = farbe(cs.backgroundColor);
    if (bg && bg.alpha > 0) add(flaechen, bg.hex + '@' + bg.alpha, flaeche);
    if (cs.backgroundImage && cs.backgroundImage.includes('gradient')) add(verlaeufe, farbenErsetzen(cs.backgroundImage).slice(0, 240), flaeche);
    for (const S of ['Top', 'Right', 'Bottom', 'Left']) {
      const w = parseFloat(cs['border' + S + 'Width']), st = cs['border' + S + 'Style'];
      if (w > 0 && st !== 'none' && st !== 'hidden') {
        const f = farbe(cs['border' + S + 'Color']);
        if (f && f.alpha > 0) add(raender, f.hex + '@' + f.alpha, (S === 'Top' || S === 'Bottom') ? r.width : r.height);
      }
    }
    if (el instanceof SVGElement) {
      if (SVG_FORM.has(tag)) {
        const f = farbe(cs.fill); if (f && f.alpha > 0) add(svg, f.hex + '@' + f.alpha);
        if (parseFloat(cs.strokeWidth) > 0) { const s = farbe(cs.stroke); if (s && s.alpha > 0) add(svg, s.hex + '@' + s.alpha); }
      } else if (tag === 'stop') { const f = farbe(cs.stopColor); if (f) add(svg, f.hex + '@' + f.alpha); }
    }

    // Schrift
    if (zeichen > 0) {
      const fam = erste(cs.fontFamily);
      if (!schriften.has(fam)) schriften.set(fam, {zeichen: 0, elemente: 0, stapel: neu(), groessen: neu(), gewichte: neu(), zeilenhoehen: neu(), laufweiten: neu(), transform: neu()});
      const s = schriften.get(fam);
      const gr = parseFloat(cs.fontSize);
      s.zeichen += zeichen; s.elemente++;
      add(s.stapel, cs.fontFamily);
      add(s.groessen, rund(gr));
      add(s.gewichte, cs.fontWeight);
      add(s.zeilenhoehen, cs.lineHeight === 'normal' ? 'normal' : rund(parseFloat(cs.lineHeight)) + 'px / ' + rund(parseFloat(cs.lineHeight) / gr, 2));
      add(s.laufweiten, cs.letterSpacing === 'normal' ? '0' : rund(parseFloat(cs.letterSpacing) / gr, 3) + 'em');
      add(s.transform, cs.textTransform);
    }

    // Radien, Schatten, Abstände, Bewegung
    const rr = [cs.borderTopLeftRadius, cs.borderTopRightRadius, cs.borderBottomRightRadius, cs.borderBottomLeftRadius];
    if (rr.some(v => parseFloat(v) > 0)) {
      const rn = rr.map(v => parseFloat(v) >= 1e5 ? 'unendlich' : v);  // calc(infinity * 1px)
      add(radien, rn.every(v => v === rn[0]) ? rn[0] : rn.join(' '));
      if (rr[0].endsWith('px') && parseFloat(rr[0]) >= Math.min(r.width, r.height) / 2 - 0.5) pillen++;
    }
    if (cs.boxShadow && cs.boxShadow !== 'none' && !nurTransparent(cs.boxShadow)) add(schatten, farbenErsetzen(cs.boxShadow).slice(0, 240));
    for (const S of ['Top', 'Right', 'Bottom', 'Left']) {
      const p = parseFloat(cs['padding' + S]); if (p > 0) add(padding, rund(p));
      const m = parseFloat(cs['margin' + S]); if (m > 0) add(margin, rund(m));
    }
    if (/flex|grid/.test(cs.display)) for (const g of [cs.rowGap, cs.columnGap]) { const v = parseFloat(g); if (v > 0) add(gap, rund(v)); }
    const durs = cs.transitionDuration.split(',').map(s => s.trim());
    const fns = cs.transitionTimingFunction.split(/,(?![^(]*\))/).map(s => s.trim());
    const props = cs.transitionProperty.split(',').map(s => s.trim());
    durs.forEach((d, i) => { if (parseFloat(d) > 0) { add(dauer, ms(d) + 'ms'); add(kurven, fns[i % fns.length]); add(eigenschaften, props[i % props.length]); } });
    if (cs.animationName && cs.animationName !== 'none') {
      const ad = cs.animationDuration.split(',');
      cs.animationName.split(',').forEach((n, i) => add(animationen, n.trim() + ' (' + ms((ad[i] || ad[0]).trim()) + 'ms)'));
    }
  }

  const gesZeichen = [...schriften.values()].reduce((a, s) => a + s.zeichen, 0) || 1;
  const schriftListe = [...schriften.entries()].sort((a, b) => b[1].zeichen - a[1].zeichen).slice(0, 12).map(([fam, s]) => ({
    familie: fam, stapel: zaehlListe(s.stapel, 1)[0].wert, anteil_zeichen: rund(s.zeichen / gesZeichen * 100), elemente: s.elemente,
    groessen_px: zaehlListe(s.groessen, 16, 'px'), gewichte: zaehlListe(s.gewichte, 8), zeilenhoehen: zaehlListe(s.zeilenhoehen, 8),
    laufweiten: zaehlListe(s.laufweiten, 6), text_transform: zaehlListe(s.transform, 4)}));

  const ueberschriften = {};
  for (const tag of ['h1', 'h2', 'h3']) {
    ueberschriften[tag] = [...document.querySelectorAll(tag)].filter(h => h.getBoundingClientRect().height > 0 && sichtbarOk(h)).slice(0, 6).map(h => {
      const cs = getComputedStyle(h), gr = parseFloat(cs.fontSize);
      const f = farbe(cs.color);
      return {text: (h.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 70), groesse_px: rund(gr), gewicht: cs.fontWeight,
        familie: erste(cs.fontFamily), zeilenhoehe: cs.lineHeight === 'normal' ? 'normal' : rund(parseFloat(cs.lineHeight) / gr, 2),
        laufweite_em: cs.letterSpacing === 'normal' ? 0 : rund(parseFloat(cs.letterSpacing) / gr, 3),
        farbe: f ? f.hex : null, text_transform: cs.textTransform};
    });
  }

  // CSS-Variablen im aktuellen Modus aufgelöst (am html-Element)
  const hcs = getComputedStyle(document.documentElement);
  const variablenFarben = [];
  for (const name of opt.var_namen) {
    const wert = hcs.getPropertyValue(name).trim();
    if (!wert || /^-?[\d.]+(px|rem|em|%|ms|s|deg)?$/.test(wert) || !CSS.supports('color', wert)) continue;
    const f = farbe(wert);
    if (f) variablenFarben.push({name, wert: wert.slice(0, 120), hex: f.hex, deckkraft: f.alpha});
  }

  // Logo-Kandidaten
  const endung = (u) => {
    try {
      if (u.startsWith('data:')) { const m = u.match(/^data:image\/([\w+.-]+)/); return m ? m[1] : 'data'; }
      const x = new URL(u, location.href); let p = x.pathname;
      const innen = x.searchParams.get('url'); if (innen) p = new URL(innen, location.href).pathname;
      const m = p.toLowerCase().match(/\.(svg|png|jpe?g|webp|gif|avif|ico)$/); return m ? m[1] : 'unbekannt';
    } catch (e) { return 'unbekannt'; }
  };
  const ARTEN = {svg: 'svg-datei', 'svg+xml': 'svg-datei', png: 'png', jpg: 'jpg', jpeg: 'jpg', webp: 'webp', gif: 'gif', avif: 'avif', ico: 'ico'};
  const logos = [];
  for (const el of document.querySelectorAll('img, svg')) {
    const tag = el.tagName.toLowerCase();
    if (tag === 'svg' && el.parentElement && el.parentElement.closest('svg')) continue;
    const a = el.closest('a');
    const merkmale = [el.getAttribute('alt'), el.getAttribute('class'), el.id, el.getAttribute('src'), el.getAttribute('aria-label'),
      el.getAttribute('title'), a && a.getAttribute('aria-label'), a && a.getAttribute('class'),
      tag === 'svg' && el.querySelector('title') ? el.querySelector('title').textContent : ''].filter(Boolean).join(' ');
    const imKopf = !!el.closest('header, nav, [role=banner]');
    const href = a ? a.getAttribute('href') || '' : '';
    const startLink = !!a && (href === '/' || href === './' || href === location.origin || href === location.origin + '/');
    const logoWort = /logo|brand|\bmarke\b|wortmarke|bildmarke|signet/i.test(merkmale);
    if (!(imKopf || logoWort || startLink)) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 8 || r.height < 8 || !sichtbarOk(el)) continue;
    if (!logoWort && !startLink && Math.max(r.width, r.height) < 32) continue;  // Symbole im Menü
    const e = {art: '', src: null, alt: el.getAttribute('alt') || el.getAttribute('aria-label') || (a && a.getAttribute('aria-label')) || null,
      breite: rund(r.width), hoehe: rund(r.height), ort: imKopf ? 'kopf/navigation' : (el.closest('footer') ? 'fuss' : 'seite'),
      startseiten_link: startLink, grund: [logoWort && 'Wort „logo/brand“', imKopf && 'im Kopf', startLink && 'Link zur Startseite'].filter(Boolean).join(', '),
      y: rund(r.top + scrollY)};
    if (tag === 'svg') {
      e.art = 'svg inline'; e.markup_laenge = el.outerHTML.length; e.viewbox = el.getAttribute('viewBox');
      const fs = new Set();
      for (const k of el.querySelectorAll('*')) { const c = getComputedStyle(k); for (const w of [c.fill, c.stroke]) { const f = farbe(w); if (f && f.alpha > 0) fs.add(f.hex); } }
      e.farben = [...fs].slice(0, 8);
    } else {
      const src = el.currentSrc || el.src || '';
      e.art = ARTEN[endung(src)] || endung(src); e.src = src.startsWith('data:') ? src.slice(0, 80) + '…' : src;
      e.natuerlich = [el.naturalWidth, el.naturalHeight];
    }
    logos.push(e);
    if (logos.length >= 12) break;
  }

  const metaInhalt = (sel) => { const m = document.querySelector(sel); return m ? m.getAttribute('content') : null; };
  const meta = {
    titel: document.title, sprache: document.documentElement.lang || null,
    theme_color: [...document.querySelectorAll('meta[name="theme-color"]')].map(m => { const f = farbe(m.content); return {wert: m.content, media: m.media || null, hex: f ? f.hex : null}; }),
    color_scheme: metaInhalt('meta[name="color-scheme"]'), beschreibung: (metaInhalt('meta[name="description"]') || '').slice(0, 240) || null,
    og_bild: metaInhalt('meta[property="og:image"]'),
    icons: [...document.querySelectorAll('link[rel*="icon"]')].slice(0, 8).map(l => ({rel: l.rel, href: l.href, groessen: l.sizes ? l.sizes.value || null : null})),
  };
  const geladen = [...new Set([...document.fonts].filter(f => f.status === 'loaded').map(f => f.family.replace(/["']/g, '') + ' ' + f.weight + ' ' + f.style))];

  return {
    elemente: {gesamt, gemessen, grenze: MAX},
    farben: {text: farbListe(text), flaechen: farbListe(flaechen), raender: farbListe(raender, 12), svg: farbListe(svg, 12)},
    verlaeufe: zaehlListe(verlaeufe, 6).map(v => ({wert: v.wert})),
    schriften: schriftListe, ueberschriften,
    radien: zaehlListe(radien, 15), radien_pillen_oder_kreise: pillen, schatten: zaehlListe(schatten, 10),
    abstaende: {padding: zaehlListe(padding, 15, 'px'), margin: zaehlListe(margin, 15, 'px'), gap: zaehlListe(gap, 10, 'px')},
    bewegung: {dauer: zaehlListe(dauer, 8), kurven: zaehlListe(kurven, 6), eigenschaften: zaehlListe(eigenschaften, 8), animationen: zaehlListe(animationen, 8)},
    variablen_farben: variablenFarben, logos, meta, schriften_geladen: geladen,
    seitenhoehe: document.documentElement.scrollHeight,
  };
})
"""


# ---------------------------------------------------------------- Hilfen

def vp_hoehe(breite):
    if breite <= 480:
        return 812
    if breite < 1024:
        return 1024
    return 900


def slug(url):
    teile = urllib.parse.urlparse(url)
    pfad = teile.path.strip("/")
    if not pfad:
        return "start"
    return re.sub(r"[^a-z0-9]+", "-", pfad.lower()).strip("-")[:40] or "seite"


def jetzt():
    return datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def ueberlappung(a, b):
    """Gemeinsamer Anteil zweier Farblisten in % (Summe der Minima, bezogen auf die größere Liste)."""
    da, db = Counter(), Counter()
    for x in a:
        da[(x["hex"], x["deckkraft"])] += x["anteil"]
    for x in b:
        db[(x["hex"], x["deckkraft"])] += x["anteil"]
    gesamt = max(sum(da.values()), sum(db.values())) or 1
    return round(sum(min(v, db[k]) for k, v in da.items()) / gesamt * 100, 1)


def schriftdateien_buendeln(fontface):
    """@font-face je Familie/Gewicht/Stil zusammenfassen (Unicode-Range-Teildateien)."""
    aus = {}
    for f in fontface:
        k = (f["familie"], f["gewicht"], f["stil"])
        if k not in aus:
            aus[k] = dict(f, dateien=0)
        aus[k]["dateien"] += 1
    return list(aus.values())


# ---------------------------------------------------------------- Messung mit Chrome

def messen_chrome(urls, out, breiten, modi, max_hoehe, warten):
    ergebnis = {"url": urls[0], "seiten": urls, "zeit": jetzt(), "methode": "chrome",
                "ansichten": [], "css_variablen": [], "schriftdateien": {}, "logos": [],
                "meta": {}, "vergleich_hell_dunkel": [], "hinweise": []}
    hinweise = ergebnis["hinweise"]
    fontface, geladen, logos_seen = [], set(), {}
    with Chrome(datei_zugriff=any(u.startswith("file:") for u in urls)) as c:
        for url in urls:
            scan = None
            name = slug(url)
            for modus in modi:
                c.farbschema("dark" if modus == "dunkel" else "light")
                for breite in breiten:
                    hoehe = vp_hoehe(breite)
                    print("Messe {} · {} px · {} …".format(url, breite, modus), file=sys.stderr)
                    c.viewport(breite, hoehe)
                    c.navigiere(url, warten_s=warten)
                    if scan is None:
                        scan = c.auswerten(SCAN_JS)
                        for v in scan["variablen"]:
                            v["url"] = url
                        ergebnis["css_variablen"] += scan["variablen"]
                        fontface += scan["fontface"]
                        if scan["nicht_lesbar"]:
                            hinweise.append("{}: {} Stylesheet(s) fremder Herkunft nicht lesbar (Variablen/@font-face daraus fehlen): {}".format(
                                url, len(scan["nicht_lesbar"]), ", ".join(scan["nicht_lesbar"][:5])))
                    methode_modus, zustand = umschalten(c, scan, c.auswerten(ZUSTAND_JS), modus)
                    c.auswerten(DURCHSCROLLEN_JS + "({})".format(int(max_hoehe)), timeout=120)
                    basis = "{}-{}-{}".format(name, breite, modus)
                    c.screenshot(os.path.join(out, basis + ".png"))
                    voll = c.screenshot(os.path.join(out, basis + "-voll.png"), voll=True, max_hoehe=max_hoehe)
                    daten = c.auswerten(MESS_JS + "(" + json.dumps(
                        {"max_elemente": 4000, "var_namen": scan["variablen_namen"]}) + ")", timeout=90)
                    if daten["elemente"]["gesamt"] > daten["elemente"]["grenze"]:
                        hinweise.append("{} · {} px · {}: {} Elemente, gemessen wurden die ersten {} sichtbaren.".format(
                            url, breite, modus, daten["elemente"]["gesamt"], daten["elemente"]["grenze"]))
                    if voll.get("abgeschnitten"):
                        hinweise.append("{} · {} px: Ganzseiten-Screenshot bei {} px abgeschnitten (Seite {} px hoch).".format(
                            url, breite, max_hoehe, voll["seitenhoehe"]))
                    geladen.update(daten.pop("schriften_geladen"))
                    for lg in daten.pop("logos"):
                        schluessel = (lg.get("src") or "") + "|" + lg["art"] + "|" + str(lg.get("markup_laenge", ""))
                        if schluessel in logos_seen:
                            wo = "{} px {}".format(breite, modus)
                            if wo not in logos_seen[schluessel]["gefunden_in"]:
                                logos_seen[schluessel]["gefunden_in"].append(wo)
                        else:
                            lg.update(url=url, gefunden_in=["{} px {}".format(breite, modus)])
                            logos_seen[schluessel] = lg
                    meta = daten.pop("meta")
                    if url not in ergebnis["meta"]:
                        meta["prefers_color_scheme_regeln"] = scan["media_dunkel"]
                        meta["dunkel_ueber_klasse"] = scan["klassen_dunkel"]
                        ergebnis["meta"][url] = meta
                    ansicht = {"url": url, "breite": breite, "hoehe_viewport": hoehe, "modus": modus,
                               "modus_methode": methode_modus, "html_zustand": zustand,
                               "screenshot": basis + ".png", "vollbild": basis + "-voll.png"}
                    ansicht.update(daten)
                    ergebnis["ansichten"].append(ansicht)
        hinweise += c.hinweise
    ergebnis["schriftdateien"] = {"font_face": schriftdateien_buendeln(fontface), "geladen": sorted(geladen)}
    ergebnis["logos"] = sorted(logos_seen.values(), key=lambda l: (not l["startseiten_link"], l["ort"] != "kopf/navigation", l["y"]))
    vergleichen(ergebnis)
    return ergebnis


def umschalten(c, scan, zustand, modus):
    """Bringt die Seite in den gewünschten Modus. Gibt (Methode, Zustand danach) zurück.

    Erst wirkt die emulierte Medienregel prefers-color-scheme. Ist die Seite danach noch im
    falschen Modus (gemessen an der Helligkeit des Seitengrunds), schaltet das Skript über
    die Klassen/Attribute um, die das CSS der Seite verwendet (.dark, .light, data-theme …).
    """
    dunkel = modus == "dunkel"
    klassen = scan["klassen_dunkel"]
    wort = "dunkel" if dunkel else "hell"
    medien = "prefers-color-scheme: {} emuliert ({} Medienregeln)".format(
        "dark" if dunkel else "light", scan["media_dunkel"])
    if zustand["dunkel"] == dunkel:
        if scan["media_dunkel"]:
            return medien, zustand
        return "Seite ist ohne Umschalten {} (Grund {})".format(wort, zustand["grund"]), zustand
    if not klassen:
        return "{}; kein Umschalter im CSS gefunden, Seite bleibt {} (Grund {})".format(
            medien, "dunkel" if zustand["dunkel"] else "hell", zustand["grund"]), zustand
    c.auswerten(MODUS_SETZEN_JS + "({}, {})".format("true" if dunkel else "false", json.dumps(klassen)))
    time.sleep(0.8)  # Übergänge abwarten
    nachher = c.auswerten(ZUSTAND_JS)
    wirkung = "wirksam" if nachher["dunkel"] == dunkel else "OHNE Wirkung"
    return "Klasse/Attribut am html-Element vom Messskript gesetzt ({}; Seite nutzt {}), {} (Grund {} → {})".format(
        wort, ", ".join(sorted(klassen)), wirkung, zustand["grund"], nachher["grund"]), nachher


def vergleichen(ergebnis):
    """Hell/dunkel je URL und Breite vergleichen und Hinweise schreiben."""
    nach = {}
    for a in ergebnis["ansichten"]:
        nach.setdefault((a["url"], a["breite"]), {})[a["modus"]] = a
    for (url, breite), m in nach.items():
        if "hell" not in m or "dunkel" not in m:
            continue
        h, d = m["hell"], m["dunkel"]
        fl = ueberlappung(h["farben"]["flaechen"], d["farben"]["flaechen"])
        tx = ueberlappung(h["farben"]["text"], d["farben"]["text"])
        vh = {v["name"]: v["hex"] for v in h["variablen_farben"]}
        vd = {v["name"]: v["hex"] for v in d["variablen_farben"]}
        geaendert = sorted(k for k in vh if k in vd and vh[k] != vd[k])
        gleich = fl >= 95 and tx >= 95
        ergebnis["vergleich_hell_dunkel"].append({
            "url": url, "breite": breite, "flaechen_gleich_prozent": fl, "text_gleich_prozent": tx,
            "variablen_geaendert": len(geaendert), "beispiele": geaendert[:8],
            "unterschiedlich": not gleich, "methode_dunkel": d["modus_methode"]})
        ohne_medien = not ergebnis["meta"].get(url, {}).get("prefers_color_scheme_regeln")
        if gleich:
            ergebnis["hinweise"].append(
                "{} · {} px: Hell und dunkel liefern dieselben Farben (Flächen {} %, Text {} % gleich). "
                "Die Seite hat {}. Dunkel: {}.".format(
                    url, breite, fl, tx, "keine prefers-color-scheme-Regeln" if ohne_medien else "prefers-color-scheme-Regeln, "
                    "die aber nichts an den gemessenen Farben ändern", d["modus_methode"]))
        else:
            ergebnis["hinweise"].append(
                "{} · {} px: Hell und dunkel unterscheiden sich (Flächen {} %, Text {} % gleich, {} Farbvariablen "
                "geändert). Hell: {}. Dunkel: {}.{}".format(
                    url, breite, fl, tx, len(geaendert), h["modus_methode"], d["modus_methode"],
                    " Die Seite hat keine prefers-color-scheme-Regeln: Ohne Umschalten per Klasse wären beide Messungen "
                    "gleich." if ohne_medien and "Messskript" in h["modus_methode"] + d["modus_methode"] else ""))


# ---------------------------------------------------------------- Ersatzweg ohne Browser (CSS als Text)

FARB_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?|oklch|oklab)\([^()]*\)|\b(?:white|black)\b", re.I)
ROOT_SEL = re.compile(r"^(?:html|:root|:host)?(?:\.(?:dark|light|theme-dark|theme-light)|\[data-(?:theme|modus|mode)[^\]]*\]|:root)*$", re.I)


def holen(url, zeitlimit=20, max_bytes=6_000_000):
    anfrage = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,text/css,*/*;q=0.8",
                                                   "Accept-Language": "de,en;q=0.8"})
    with urllib.request.urlopen(anfrage, timeout=zeitlimit) as antwort:
        daten = antwort.read(max_bytes)
        zeichensatz = antwort.headers.get_content_charset() or "utf-8"
        return daten.decode(zeichensatz, "replace"), antwort.geturl()


def _zahl(t, skala=1.0):
    t = t.strip().lower()
    if t in ("none", ""):
        return 0.0
    if t.endswith("%"):
        return float(t[:-1]) / 100 * skala
    return float(t)


def _winkel(t):
    t = t.strip().lower()
    if t in ("none", ""):
        return 0.0
    for einheit, faktor in (("deg", 1), ("grad", 0.9), ("rad", 180 / math.pi), ("turn", 360)):
        if t.endswith(einheit):
            return float(t[:-len(einheit)]) * faktor
    return float(t)


def _hex(r, g, b):
    return "#{:02X}{:02X}{:02X}".format(*(max(0, min(255, int(round(v)))) for v in (r, g, b)))


def _oklab_zu_rgb(L, a, b):
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    lin = (4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
           -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
           -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_)
    gamma = [12.92 * x if x <= 0.0031308 else 1.055 * (max(x, 0) ** (1 / 2.4)) - 0.055 for x in lin]
    return [max(0.0, min(1.0, x)) * 255 for x in gamma]


def farbe_normalisieren(wert):
    """CSS-Farbwert → (#RRGGBB, Deckkraft) oder None."""
    w = wert.strip().lower()
    try:
        if w == "white":
            return "#FFFFFF", 1.0
        if w == "black":
            return "#000000", 1.0
        if w.startswith("#"):
            h = w[1:]
            if len(h) in (3, 4):
                h = "".join(ch * 2 for ch in h)
            if len(h) not in (6, 8):
                return None
            alpha = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
            return "#" + h[:6].upper(), round(alpha, 2)
        name, _, rest = w.partition("(")
        rest = rest.rstrip(")")
        alpha = 1.0
        if "/" in rest:
            rest, _, a = rest.partition("/")
            alpha = _zahl(a)
        teile = [t for t in re.split(r"[\s,]+", rest.strip()) if t]
        if len(teile) == 4 and name in ("rgba", "hsla", "rgb", "hsl"):
            alpha = _zahl(teile.pop())
        if len(teile) != 3:
            return None
        if name in ("rgb", "rgba"):
            r, g, b = (_zahl(t, 255) for t in teile)
        elif name in ("hsl", "hsla"):
            hue = _winkel(teile[0]) / 360 % 1
            s, l = (_zahl(t, 1) if "%" in t else float(t) / 100 for t in teile[1:])
            r, g, b = (x * 255 for x in colorsys.hls_to_rgb(hue, l, s))
        elif name == "oklch":
            L = _zahl(teile[0], 1)
            C = _zahl(teile[1], 0.4)
            hue = math.radians(_winkel(teile[2]))
            r, g, b = _oklab_zu_rgb(L, C * math.cos(hue), C * math.sin(hue))
        elif name == "oklab":
            r, g, b = _oklab_zu_rgb(_zahl(teile[0], 1), _zahl(teile[1], 0.4), _zahl(teile[2], 0.4))
        else:
            return None
        return _hex(r, g, b), round(max(0.0, min(1.0, alpha)), 2)
    except (ValueError, IndexError):
        return None


def css_bloecke(css):
    """Zerlegt CSS in (Stapel der Präludien, Deklarationstext) je Block."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    stapel, bloecke, dekl, pos = [], [], [""], 0
    for m in re.finditer(r"[{}]", css):
        seg = css[pos:m.start()]
        pos = m.end()
        if m.group() == "{":
            vor, _, praeludium = seg.rpartition(";")
            dekl[-1] += vor + ";"
            stapel.append(praeludium.strip())
            dekl.append("")
        else:
            dekl[-1] += seg
            if stapel:
                bloecke.append((list(stapel), dekl.pop()))
                stapel.pop()
    return bloecke


def deklarationen(text):
    """(Eigenschaft, Wert)-Paare; Semikolons in Klammern werden respektiert."""
    tiefe, start, teile = 0, 0, []
    for i, ch in enumerate(text):
        if ch == "(":
            tiefe += 1
        elif ch == ")":
            tiefe = max(0, tiefe - 1)
        elif ch == ";" and tiefe == 0:
            teile.append(text[start:i])
            start = i + 1
    teile.append(text[start:])
    for t in teile:
        if ":" in t:
            k, _, v = t.partition(":")
            k = k.strip().lower() if not k.strip().startswith("--") else k.strip()
            if re.match(r"^-{0,2}[\w-]+$", k):
                yield k, v.strip()


class HtmlSammler(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.html = html
        self.zeilen = [0]
        for m in re.finditer("\n", html):
            self.zeilen.append(m.end())
        self.stylesheets, self.styles, self.inline, self.logos = [], [], [], []
        self.meta = {"titel": None, "sprache": None, "theme_color": [], "icons": [], "color_scheme": None}
        self.kopf, self.a_stapel, self.svg_tiefe, self.svg_start = 0, [], 0, None
        self._in_style = self._in_title = False

    def _offset(self):
        zeile, spalte = self.getpos()
        return self.zeilen[zeile - 1] + spalte

    def _logo_pruefen(self, tag, a):
        merkmale = " ".join(filter(None, [a.get("alt"), a.get("class"), a.get("id"), a.get("src"),
                                          a.get("aria-label"), a.get("title")] + [x[1] for x in self.a_stapel]))
        start_link = any(x[0] in ("/", "./") for x in self.a_stapel)
        logo_wort = bool(re.search(r"logo|brand|\bmarke\b|wortmarke|bildmarke|signet", merkmale, re.I))
        return (self.kopf > 0 or logo_wort or start_link), logo_wort, start_link

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "html" and a.get("lang"):
            self.meta["sprache"] = a["lang"]
        elif tag in ("header", "nav"):
            self.kopf += 1
        elif tag == "a":
            self.a_stapel.append((a.get("href", ""), a.get("aria-label", "") + " " + a.get("class", "")))
        elif tag == "link":
            rel = a.get("rel", "").lower()
            if "stylesheet" in rel and a.get("href"):
                self.stylesheets.append(a["href"])
            elif "icon" in rel:
                self.meta["icons"].append({"rel": rel, "href": a.get("href"), "groessen": a.get("sizes") or None})
        elif tag == "meta":
            if a.get("name", "").lower() == "theme-color":
                self.meta["theme_color"].append({"wert": a.get("content"), "media": a.get("media") or None})
            elif a.get("name", "").lower() == "color-scheme":
                self.meta["color_scheme"] = a.get("content")
        elif tag == "style":
            self._in_style = True
        elif tag == "title":
            self._in_title = True
        elif tag == "img":
            passt, wort, start = self._logo_pruefen(tag, a)
            if passt:
                src = a.get("src") or a.get("data-src") or ""
                self.logos.append({"art": "img", "src": src, "alt": a.get("alt") or None,
                                   "breite": a.get("width") or None, "hoehe": a.get("height") or None,
                                   "ort": "kopf/navigation" if self.kopf else "seite", "startseiten_link": start})
        elif tag == "svg":
            if self.svg_tiefe == 0:
                passt, wort, start = self._logo_pruefen(tag, a)
                self.svg_start = (self._offset(), a, passt, start) if passt else None
            self.svg_tiefe += 1
        if a.get("style"):
            self.inline.append(a["style"])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag == "svg":
            self.handle_endtag("svg")
        elif tag == "a" and self.a_stapel:
            self.a_stapel.pop()

    def handle_endtag(self, tag):
        if tag in ("header", "nav"):
            self.kopf = max(0, self.kopf - 1)
        elif tag == "a" and self.a_stapel:
            self.a_stapel.pop()
        elif tag == "style":
            self._in_style = False
        elif tag == "title":
            self._in_title = False
        elif tag == "svg" and self.svg_tiefe:
            self.svg_tiefe -= 1
            if self.svg_tiefe == 0 and self.svg_start:
                start, a, _, start_link = self.svg_start
                ende = self.html.find(">", self._offset()) + 1
                self.logos.append({"art": "svg inline", "src": None, "alt": a.get("aria-label") or None,
                                   "breite": a.get("width") or None, "hoehe": a.get("height") or None,
                                   "viewbox": a.get("viewbox"), "markup_laenge": max(0, ende - start),
                                   "ort": "kopf/navigation" if self.kopf else "seite", "startseiten_link": start_link})
                self.svg_start = None

    def handle_data(self, data):
        if self._in_style:
            self.styles.append(data)
        elif self._in_title and not self.meta["titel"]:
            self.meta["titel"] = data.strip()


def farbvariablen_aufloesen(bloecke):
    """Farbvariablen aus dem CSS-Text, var()-Verweise über die :root-Werte aufgelöst."""
    basis = {}
    for b in bloecke:
        if not re.search(r"\.(dark|light|theme-)|\[data-", b["selektor"]) and "prefers-color-scheme" not in b["bedingung"]:
            for k, v in b["variablen"].items():
                basis.setdefault(k, v)

    def aufloesen(wert, tiefe=0):
        m = re.fullmatch(r"var\(\s*(--[\w-]+)\s*(?:,\s*(.+))?\)", wert.strip())
        if not m or tiefe > 6:
            return wert.strip()
        ziel = basis.get(m.group(1), m.group(2) or "")
        return aufloesen(ziel, tiefe + 1)

    aus = []
    for b in bloecke:
        for name, wert in b["variablen"].items():
            echt = aufloesen(wert)
            if FARB_RE.fullmatch(echt):
                n = farbe_normalisieren(echt)
                if n:
                    aus.append({"name": name, "wert": wert[:120], "hex": n[0], "deckkraft": n[1],
                                "selektor": b["selektor"][:80], "bedingung": b["bedingung"]})
    return aus


def messen_css_text(urls, grund):
    """Schätzung ohne Browser. Gibt (ergebnis, None) oder (None, Fehlermeldung) zurück."""
    ergebnis = {"url": urls[0], "seiten": urls, "zeit": jetzt(), "methode": "css-text", "schaetzung": True,
                "ansichten": [], "farben": {}, "schriften": {}, "radien": [], "css_variablen": [],
                "farb_variablen": [], "schriftdateien": {"font_face": []}, "logos": [], "meta": {},
                "hinweise": ["SCHÄTZUNG ohne Browser ({}): Werte stammen aus dem CSS-Quelltext. Häufigkeiten zählen "
                             "Vorkommen im Code, nicht sichtbare Flächen; ungenutzte Regeln zählen mit; keine "
                             "Screenshots, kein Hell/Dunkel-Vergleich.".format(grund)]}
    rollen = {r: Counter() for r in ("text", "flaechen", "raender", "svg", "variablen", "sonstige")}
    alle_farben, familien, groessen, radien = Counter(), Counter(), Counter(), Counter()
    media_dunkel, klassen = 0, Counter()
    gelesen, fehler = [], []
    for nr, url in enumerate(urls):
        try:
            html, endurl = holen(url)
        except Exception as e:
            fehler.append("{}: {}".format(url, e))
            continue
        p = HtmlSammler(html)
        try:
            p.feed(html)
        except Exception as e:  # kaputtes HTML: mit dem Gelesenen weiter
            ergebnis["hinweise"].append("{}: HTML nur teilweise lesbar ({}).".format(url, e))
        p.meta["theme_color"] = [dict(t, hex=(farbe_normalisieren(t["wert"] or "") or [None])[0]) for t in p.meta["theme_color"]]
        ergebnis["meta"][url] = p.meta
        for lg in p.logos[:12]:
            if lg.get("src"):
                lg["src"] = urllib.parse.urljoin(endurl, lg["src"])
                endung = re.search(r"\.(svg|png|jpe?g|webp|gif|avif)(?:$|[?#])", urllib.parse.unquote(lg["src"]).lower())
                lg["art"] = {"svg": "svg-datei", "jpeg": "jpg"}.get(endung.group(1), endung.group(1)) if endung else "img (unbekannt)"
            lg["url"] = url
            ergebnis["logos"].append(lg)
        quellen = [("inline <style>", s) for s in p.styles]
        quellen.append(("style-Attribute", "x{" + ";".join(p.inline) + "}"))
        warteschlange = [urllib.parse.urljoin(endurl, h) for h in p.stylesheets]
        geholt = set()
        while warteschlange and len(geholt) < 20:
            href = warteschlange.pop(0)
            if href in geholt:
                continue
            geholt.add(href)
            try:
                css, _ = holen(href)
            except Exception as e:
                ergebnis["hinweise"].append("Stylesheet nicht ladbar: {} ({})".format(href, e))
                continue
            quellen.append((href, css))
            for imp in re.findall(r"@import\s+(?:url\()?\s*[\"']?([^\"')\s;]+)", css):
                warteschlange.append(urllib.parse.urljoin(href, imp))
        gelesen.append({"url": url, "stylesheets": sorted(geholt)})

        for quelle, css in quellen:
            media_dunkel += len(re.findall(r"prefers-color-scheme", css))
            for stapel, dekl in css_bloecke(css):
                innen = stapel[-1]
                if innen.lower().startswith("@font-face"):
                    d = dict(deklarationen(dekl))
                    ergebnis["schriftdateien"]["font_face"].append({
                        "familie": d.get("font-family", "").strip("\"' "), "src": d.get("src", "")[:400],
                        "gewicht": d.get("font-weight", ""), "stil": d.get("font-style", ""), "quelle": quelle})
                    continue
                for k in (".dark", ".light"):
                    if re.search(re.escape(k) + r"(?![-\w])", innen):
                        klassen[k] += 1
                for k in ("[data-theme", "[data-modus", "[data-mode"):
                    if k in innen:
                        klassen[k] += 1
                teile = [t.strip() for t in re.split(r",(?![^(]*\))", innen)]
                ist_root = any(t and ROOT_SEL.match(t) for t in teile)
                variablen = {}
                for k, v in deklarationen(dekl):
                    if k.startswith("--"):
                        rolle = "variablen"
                        if ist_root:
                            variablen[k] = v[:200]
                        if re.search(r"font(?!-(weight|size|feature|variation|smoothing))", k.lower()) \
                                and re.search(r"[a-z]", v, re.I) and not v.startswith(("var(", "initial", "inherit")):
                            familien[v.split(",")[0].strip().strip("\"'")] += 1
                        if "radius" in k.lower():
                            radien[v] += 1
                    elif k == "color":
                        rolle = "text"
                    elif k.startswith("background"):
                        rolle = "flaechen"
                    elif k.startswith("border") or k.startswith("outline"):
                        rolle = "raender"
                    elif k in ("fill", "stroke", "stop-color"):
                        rolle = "svg"
                    else:
                        rolle = "sonstige"
                    if k == "font-family":
                        fam = v.split(",")[0].strip().strip("\"'")
                        if fam and not fam.startswith("var(") and fam not in ("inherit", "initial", "unset"):
                            familien[fam] += 1
                    elif k == "font-size" and re.match(r"^[\d.]+(px|rem|em|pt)$", v):
                        groessen[v] += 1
                    elif k == "border-radius" and "var(" not in v:
                        radien[v] += 1
                    for f in FARB_RE.findall(v):
                        n = farbe_normalisieren(f)
                        if n and n[1] > 0:  # transparent zählt nicht
                            schluessel = "{}@{}".format(*n)
                            rollen[rolle][schluessel] += 1
                            alle_farben[schluessel] += 1
                if variablen:
                    kontext = " ".join(stapel[:-1])
                    ergebnis["css_variablen"].append({"selektor": innen[:160], "bedingung": kontext,
                                                      "quelle": quelle, "url": url, "variablen": variablen})
    if not gelesen:
        return None, "Keine Seite ladbar: " + "; ".join(fehler)
    ergebnis["farb_variablen"] = farbvariablen_aufloesen(ergebnis["css_variablen"])
    ergebnis["hinweise"] += ["Nicht ladbar: " + f for f in fehler]

    def liste(counter, n=20):
        gesamt = sum(counter.values()) or 1
        aus = []
        for k, v in counter.most_common(n):
            hex_, alpha = k.split("@")
            aus.append({"hex": hex_, "deckkraft": float(alpha), "anzahl": v, "anteil": round(v / gesamt * 100, 1)})
        return aus

    ergebnis["farben"] = {"alle": liste(alle_farben, 30), "nach_rolle": {r: liste(c, 15) for r, c in rollen.items()}}
    ergebnis["schriften"] = {"familien": [{"familie": k, "anzahl": v} for k, v in familien.most_common(12)],
                             "groessen": [{"wert": k, "anzahl": v} for k, v in groessen.most_common(15)]}
    ergebnis["radien"] = [{"wert": k, "anzahl": v} for k, v in radien.most_common(15)]
    ergebnis["gelesen"] = gelesen
    ergebnis["schriftdateien"]["font_face"] = schriftdateien_buendeln(ergebnis["schriftdateien"]["font_face"])
    ergebnis["dunkel"] = {"prefers_color_scheme_vorkommen": media_dunkel, "dunkel_ueber_klasse": dict(klassen)}
    return ergebnis, None


# ---------------------------------------------------------------- Zusammenfassung (Markdown)

def _farben_md(liste, n=6, schluessel="anteil"):
    if not liste:
        return "–"
    teile = []
    for f in liste[:n]:
        dk = "" if f["deckkraft"] >= 1 else " ({:.0f} % deckend)".format(f["deckkraft"] * 100)
        wert = "{} %".format(f["anteil"]) if schluessel == "anteil" else "{}×".format(f["anzahl"])
        teile.append("`{}`{} {}".format(f["hex"], dk, wert))
    return " · ".join(teile)


def _zaehl_md(liste, n=8, schluessel="wert", einheit=""):
    if not liste:
        return "–"
    return " · ".join("{}{} ×{}".format(x[schluessel], einheit, x["anzahl"]) for x in liste[:n])


def zusammenfassung_md(e):
    z = ["# Messung: {}".format(e["url"]), "",
         "- Zeit: {} · Methode: **{}**{}".format(e["zeit"], e["methode"], " (SCHÄTZUNG)" if e.get("schaetzung") else ""),
         "- Seiten: " + ", ".join(e["seiten"]), ""]
    if e["hinweise"]:
        z += ["## Hinweise", ""] + ["- " + h for h in e["hinweise"]] + [""]
    if e["methode"] == "chrome":
        for a in e["ansichten"]:
            herkunft = "{} · {} px · {}".format(a["url"], a["breite"], a["modus"])
            z += ["## {}".format(herkunft), "",
                  "Screenshots: `{}`, `{}` · Modus: {} · Elemente gemessen: {}".format(
                      a["screenshot"], a["vollbild"], a["modus_methode"], a["elemente"]["gemessen"]), "",
                  "- Text (nach Zeichen): " + _farben_md(a["farben"]["text"]),
                  "- Flächen (nach Fläche): " + _farben_md(a["farben"]["flaechen"]),
                  "- Ränder (nach Länge): " + _farben_md(a["farben"]["raender"], 5),
                  "- SVG (nach Anzahl): " + _farben_md(a["farben"]["svg"], 5)]
            if a["verlaeufe"]:
                z.append("- Verläufe: " + " · ".join("`{}`".format(v["wert"][:90]) for v in a["verlaeufe"][:3]))
            for s in a["schriften"][:4]:
                z.append("- Schrift **{}** ({} % der Zeichen; Stapel `{}`): Größen {} · Gewichte {} · Zeilenhöhen {} · Laufweiten {}{}".format(
                    s["familie"], s["anteil_zeichen"], s["stapel"][:80], _zaehl_md(s["groessen_px"], 8, "px", "px"),
                    _zaehl_md(s["gewichte"], 5), _zaehl_md(s["zeilenhoehen"], 4), _zaehl_md(s["laufweiten"], 4),
                    "" if s["text_transform"][0]["wert"] == "none" and len(s["text_transform"]) == 1
                    else " · Transform " + _zaehl_md(s["text_transform"], 3)))
            for tag in ("h1", "h2", "h3"):
                for h in a["ueberschriften"].get(tag, [])[:2]:
                    z.append("- {}: {} px / {} / {} · Zeilenhöhe {} · Laufweite {} em · `{}` · „{}“".format(
                        tag, h["groesse_px"], h["gewicht"], h["familie"], h["zeilenhoehe"], h["laufweite_em"],
                        h["farbe"], h["text"][:50]))
            z += ["- Radien: " + _zaehl_md(a["radien"], 6) + " · Pillen/Kreise: {}".format(a["radien_pillen_oder_kreise"]),
                  "- Schatten: " + _zaehl_md(a["schatten"], 3),
                  "- Abstände padding: " + _zaehl_md(a["abstaende"]["padding"], 10, "px", "px"),
                  "- Abstände margin: " + _zaehl_md(a["abstaende"]["margin"], 8, "px", "px"),
                  "- Abstände gap: " + _zaehl_md(a["abstaende"]["gap"], 8, "px", "px"),
                  "- Bewegung: Dauer " + _zaehl_md(a["bewegung"]["dauer"], 5) + " · Kurven " +
                  _zaehl_md(a["bewegung"]["kurven"], 3) + " · Animationen " + _zaehl_md(a["bewegung"]["animationen"], 4), ""]
        if e["vergleich_hell_dunkel"]:
            z += ["## Hell/dunkel", ""]
            for v in e["vergleich_hell_dunkel"]:
                z.append("- {} · {} px: {} (Flächen {} % gleich, Text {} % gleich, {} Farbvariablen geändert{})".format(
                    v["url"], v["breite"], "unterschiedlich" if v["unterschiedlich"] else "GLEICH",
                    v["flaechen_gleich_prozent"], v["text_gleich_prozent"], v["variablen_geaendert"],
                    ": " + ", ".join(v["beispiele"][:5]) if v["beispiele"] else ""))
            z.append("")
        farbvars = {}
        for a in e["ansichten"]:
            for v in a["variablen_farben"]:
                farbvars.setdefault(v["name"], {})[a["modus"]] = v["hex"]
        if farbvars:
            z += ["## Farbvariablen (aufgelöst am html-Element, Auszug)", ""]
            reihe = sorted(farbvars.items(), key=lambda kv: len(set(kv[1].values())) == 1)  # geänderte zuerst
            for name, werte in reihe[:50]:
                z.append("- `{}`: ".format(name) + " · ".join("{} `{}`".format(m, h) for m, h in werte.items()))
            z.append("")
    else:
        f = e["farben"]
        z += ["## Farben (Vorkommen im CSS, Schätzung)", "",
              "- Alle: " + _farben_md(f["alle"], 10, "anzahl")]
        for rolle, liste in f["nach_rolle"].items():
            z.append("- {}: {}".format(rolle, _farben_md(liste, 6, "anzahl")))
        z += ["", "## Schriften (Schätzung)", "",
              "- Familien: " + _zaehl_md(e["schriften"]["familien"], 8, "familie"),
              "- Größen: " + _zaehl_md(e["schriften"]["groessen"], 10),
              "- Radien: " + _zaehl_md(e["radien"], 8),
              "- Dunkelmodus im CSS: prefers-color-scheme {}×, Klassen {}".format(
                  e["dunkel"]["prefers_color_scheme_vorkommen"], e["dunkel"]["dunkel_ueber_klasse"] or "keine"), ""]
        if e["farb_variablen"]:
            z += ["## Farbvariablen (aus dem CSS, Auszug)", ""]
            for v in e["farb_variablen"][:50]:
                z.append("- `{}` = `{}` → `{}` ({}{})".format(v["name"], v["wert"][:50], v["hex"], v["selektor"],
                                                             " " + v["bedingung"] if v["bedingung"] else ""))
            z.append("")
    andere = [(b["selektor"], b["bedingung"], k, w) for b in e["css_variablen"] for k, w in b["variablen"].items()]
    if andere:
        z += ["## CSS-Variablen (Auszug, {} insgesamt)".format(len(andere)), ""]
        for sel, bed, k, w in andere[:60]:
            z.append("- `{}: {}` ({}{})".format(k, w[:70], sel[:50], " · " + bed[:60] if bed else ""))
        z.append("")
    ff = e["schriftdateien"]["font_face"]
    if ff or e["schriftdateien"].get("geladen"):
        z += ["## Schriftdateien", ""]
        for f in ff[:15]:
            z.append("- @font-face **{}** {} {}{}: {}".format(f["familie"], f["gewicht"], f["stil"],
                                                             " ({} Dateien)".format(f["dateien"]) if f.get("dateien", 1) > 1 else "",
                                                             f["src"][:120]))
        if e["schriftdateien"].get("geladen"):
            z.append("- Geladen (document.fonts): " + ", ".join(e["schriftdateien"]["geladen"][:20]))
        z.append("")
    if e["logos"]:
        z += ["## Logo-Kandidaten", ""]
        for lg in e["logos"][:10]:
            z.append("- {} · {} · {} × {} · {}{}{}".format(
                lg["art"], lg.get("src") or "inline ({} Zeichen Markup)".format(lg.get("markup_laenge")),
                lg.get("breite"), lg.get("hoehe"), lg.get("ort"),
                " · Farben " + ", ".join(lg["farben"]) if lg.get("farben") else "",
                " · " + ", ".join(lg["gefunden_in"]) if lg.get("gefunden_in") else ""))
        z.append("")
    z += ["## Meta", ""]
    for url, m in e["meta"].items():
        z.append("- {}: Titel „{}“ · Sprache {} · theme-color {} · color-scheme {}".format(
            url, m.get("titel"), m.get("sprache"),
            ", ".join("{}{}".format(t["wert"], " (" + t["media"] + ")" if t.get("media") else "") for t in m["theme_color"]) or "–",
            m.get("color_scheme") or "–"))
    return "\n".join(z) + "\n"


# ---------------------------------------------------------------- Hauptprogramm

def main():
    ap = argparse.ArgumentParser(description="Website messen: Farben, Schriften, Radien, Variablen, Logos.")
    ap.add_argument("url")
    ap.add_argument("--out", required=True, help="Ausgabeordner")
    ap.add_argument("--breiten", default="375,1440", help="Viewport-Breiten, z. B. 375,1440")
    ap.add_argument("--modi", default="hell,dunkel", help="hell, dunkel oder beide")
    ap.add_argument("--seiten", default="", help="weitere URLs, kommagetrennt")
    ap.add_argument("--max-hoehe", type=int, default=8000, help="Höchsthöhe des Ganzseiten-Screenshots in px")
    ap.add_argument("--warten", type=float, default=1.5, help="Sekunden nach dem load-Ereignis")
    ap.add_argument("--nur-css", action="store_true", help="ohne Browser, CSS als Text lesen (Schätzung)")
    args = ap.parse_args()

    try:
        breiten = [int(b) for b in args.breiten.split(",") if b.strip()]
    except ValueError:
        ap.error("--breiten erwartet Zahlen, z. B. 375,1440")
    modi = [m.strip() for m in args.modi.split(",") if m.strip()]
    if any(m not in ("hell", "dunkel") for m in modi):
        ap.error("--modi erlaubt nur hell und dunkel")
    urls = [args.url] + [u.strip() for u in args.seiten.split(",") if u.strip()]
    for u in urls:
        if not re.match(r"^(https?|file)://", u):
            ap.error("URL muss mit http://, https:// oder file:// beginnen: " + u)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    ergebnis, grund = None, None
    if args.nur_css:
        grund = "--nur-css"
    elif not finde_chrome():
        grund = "kein Chrome gefunden"
        print("Kein Chrome gefunden, nutze den Ersatzweg ohne Browser (Schätzung).", file=sys.stderr)
    else:
        try:
            ergebnis = messen_chrome(urls, str(out), breiten, modi, args.max_hoehe, args.warten)
        except CDPFehler as e:
            grund = "Chrome-Messung fehlgeschlagen: {}".format(e)
            print(grund + " Nutze den Ersatzweg ohne Browser.", file=sys.stderr)
    if ergebnis is None:
        ergebnis, fehler = messen_css_text(urls, grund)
        if ergebnis is None:
            print("Messung nicht möglich: {}. Netzwerk prüfen oder Seite als HTML-Datei bereitstellen.".format(fehler),
                  file=sys.stderr)
            return 3

    with open(out / "messung.json", "w", encoding="utf-8") as f:
        json.dump(ergebnis, f, ensure_ascii=False, indent=1)
    with open(out / "messung.md", "w", encoding="utf-8") as f:
        f.write(zusammenfassung_md(ergebnis))
    print("Fertig ({}): {} und {}".format(ergebnis["methode"], out / "messung.json", out / "messung.md"))
    for h in ergebnis["hinweise"]:
        print("Hinweis: " + h)
    return 0


if __name__ == "__main__":
    sys.exit(main())
