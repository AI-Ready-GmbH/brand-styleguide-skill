"""Gemeinsame Helfer für die Token-Skripte: Laden, Verweise auflösen, Farben, Kontrast, Größen.

Nur Standardbibliothek. Format der Tokens: references/tokens.md.
"""
import json
import math
import pathlib
import re

PFLICHT = {
    "farbe.rolle": ["grund", "flaeche", "text", "text-leise", "linie", "linie-stark", "akzent", "akzent-text",
                    "handlung", "handlung-hover", "handlung-text", "fokus", "fehler"],
    "schrift.familie": ["titel", "text"],
    "schrift.web": ["fliesstext", "label"],
    "radius": ["steuerung", "karte", "pille"],
    "bewegung.dauer": ["kurz", "mittel", "lang"],
    "bewegung.kurve": ["standard"],
    "layout": ["container", "rand", "lesebreite"],
}
VERWEIS = re.compile(r"\{([a-z0-9_.\-]+)\}")


class TokenFehler(Exception):
    pass


def laden(pfad):
    pfad = pathlib.Path(pfad)
    try:
        daten = json.loads(pfad.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise TokenFehler(f"{pfad}: kein gültiges JSON (Zeile {e.lineno}: {e.msg})")
    return Tokens(daten, pfad)


class Tokens:
    def __init__(self, daten, pfad=None):
        self.daten = daten
        self.pfad = pfad
        self.marke = daten.get("$marke", {})
        self.modi = self.marke.get("modi") or ["hell"]
        self.flach = {}
        self._sammeln(daten, [])

    def _sammeln(self, knoten, weg):
        for k, v in knoten.items():
            if k.startswith("$"):
                continue
            if isinstance(v, dict) and "$value" in v:
                self.flach[".".join(weg + [k])] = v
            elif isinstance(v, dict):
                self._sammeln(v, weg + [k])

    def gruppe(self, praefix):
        """Namen der Tokens direkt unter einer Gruppe, in Reihenfolge der Datei."""
        p = praefix + "."
        return [k[len(p):] for k in self.flach if k.startswith(p) and "." not in k[len(p):]]

    def roh(self, pfad, modus=None):
        tok = self.flach.get(pfad)
        if tok is None:
            raise TokenFehler(f"Verweis ins Leere: {{{pfad}}}")
        if modus and modus != self.modi[0]:
            ext = (tok.get("$extensions") or {}).get("modi") or {}
            if modus in ext:
                return ext[modus]
            if modus == "druck" and "hell" in ext and self.modi[0] != "hell":
                return ext["hell"]
        return tok["$value"]

    def wert(self, pfad, modus=None, tiefe=0):
        """Wert mit aufgelösten Verweisen (rekursiv, im selben Modus)."""
        if tiefe > 12:
            raise TokenFehler(f"Verweiskette zu lang oder zirkulär bei {pfad}")
        return self._aufloesen(self.roh(pfad, modus), modus, tiefe)

    def _aufloesen(self, v, modus, tiefe):
        if isinstance(v, str):
            m = VERWEIS.fullmatch(v.strip())
            if m:
                return self.wert(m.group(1), modus, tiefe + 1)
            return VERWEIS.sub(lambda m: str(self._als_text(self.wert(m.group(1), modus, tiefe + 1))), v)
        if isinstance(v, dict):
            return {k: self._aufloesen(x, modus, tiefe) for k, x in v.items()}
        if isinstance(v, list):
            return [self._aufloesen(x, modus, tiefe) for x in v]
        return v

    @staticmethod
    def _als_text(v):
        if isinstance(v, list):
            return ", ".join(v)
        return v

    def typ(self, pfad):
        return self.flach[pfad].get("$type")

    def fehlende_pflicht(self):
        fehlend = []
        for gruppe, namen in PFLICHT.items():
            vorhanden = set(self.gruppe(gruppe))
            fehlend += [f"{gruppe}.{n}" for n in namen if n not in vorhanden]
        return fehlend


# ---------- Farben ----------

HEX = re.compile(r"#([0-9a-fA-F]{6})([0-9a-fA-F]{2})?$")
MIX = re.compile(r"color-mix\(\s*in\s+srgb\s*,\s*(.+?)\s+([\d.]+)%\s*,\s*(.+?)\s*\)$")


def farbe(text):
    """'#RRGGBB', '#RRGGBBAA' oder 'color-mix(in srgb, A x%, B|transparent)' → (r, g, b, a) mit 0–255 und a 0–1."""
    t = str(text).strip()
    m = HEX.match(t)
    if m:
        h = m.group(1)
        a = int(m.group(2), 16) / 255 if m.group(2) else 1.0
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)
    m = MIX.match(t)
    if m:
        a1, p, b = farbe(m.group(1)), float(m.group(2)) / 100, m.group(3).strip()
        if b == "transparent":
            return (a1[0], a1[1], a1[2], a1[3] * p)
        b1 = farbe(b)
        return tuple(a1[i] * p + b1[i] * (1 - p) for i in range(3)) + (a1[3] * p + b1[3] * (1 - p),)
    if t.lower() in ("white", "#fff"):
        return (255, 255, 255, 1.0)
    if t.lower() in ("black", "#000"):
        return (0, 0, 0, 1.0)
    raise TokenFehler(f"Farbe nicht lesbar: {text!r} (erlaubt: #RRGGBB oder color-mix(in srgb, … x%, …))")


def auf_grund(vorne, hinten):
    """Mischt eine halbtransparente Farbe auf einen deckenden Grund."""
    a = vorne[3]
    return tuple(vorne[i] * a + hinten[i] * (1 - a) for i in range(3)) + (1.0,)


def hex_von(rgb):
    return "#" + "".join(f"{max(0, min(255, round(c))):02X}" for c in rgb[:3])


def _lin(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def leuchtdichte(rgb):
    r, g, b = (_lin(c) for c in rgb[:3])
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def kontrast(a, b):
    la, lb = leuchtdichte(a), leuchtdichte(b)
    hell, dunkel = max(la, lb), min(la, lb)
    return (hell + 0.05) / (dunkel + 0.05)


def lab(rgb):
    r, g, b = (_lin(c) for c in rgb[:3])
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 1.0
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def delta_e(a, b):
    """Farbabstand CIE76 im Lab-Raum (unter etwa 3 kaum unterscheidbar)."""
    la, lb = lab(a), lab(b)
    return math.sqrt(sum((la[i] - lb[i]) ** 2 for i in range(3)))


def buntheit(rgb):
    _, a, b = lab(rgb)
    return math.hypot(a, b)


# ---------- Größen ----------

def px(text, minimum=True):
    """'16px', '1.25rem', '12pt', 'clamp(2rem, 4vw, 3.25rem)' → px (bei clamp der kleinste bzw. größte Wert)."""
    t = str(text).strip()
    m = re.fullmatch(r"clamp\((.+),(.+),(.+)\)", t)
    if m:
        return px(m.group(1) if minimum else m.group(3))
    m = re.fullmatch(r"(-?[\d.]+)\s*(px|rem|em|pt)?", t)
    if not m:
        return None
    zahl, einheit = float(m.group(1)), m.group(2) or "px"
    return zahl * {"px": 1, "rem": 16, "em": 16, "pt": 4 / 3}[einheit]


def ms(text):
    t = str(text).strip()
    m = re.fullmatch(r"([\d.]+)\s*(ms|s)", t)
    if not m:
        return None
    return float(m.group(1)) * (1000 if m.group(2) == "s" else 1)


def zahl_de(x, stellen=1):
    return f"{x:.{stellen}f}".replace(".", ",")
