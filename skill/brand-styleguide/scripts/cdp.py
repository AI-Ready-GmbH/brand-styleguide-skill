"""Minimaler Chrome-Client über das DevTools-Protokoll (CDP), nur Standardbibliothek.

Wird von messen.py und render.py importiert. Startet genau eine Headless-Instanz
mit eigenem Profil im Temp-Ordner und räumt im __exit__ alles wieder ab.

Beispiel:
    from cdp import Chrome, finde_chrome, datei_url
    with Chrome() as c:
        c.viewport(1440, 900)
        c.navigiere("https://example.org", warten_s=1)
        print(c.auswerten("document.title"))
        c.screenshot("start.png", voll=True)
        c.pdf("start.pdf")

Umgebungsvariable CHROME_PATH setzt den Browser fest.
"""

import atexit
import base64
import collections
import glob
import hashlib
import json
import os
import shutil
import signal
import socket
import struct
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse
import urllib.request
from pathlib import Path

try:
    import fcntl  # nur POSIX: Sperre gegen parallele Instanzen
except ImportError:  # Windows
    fcntl = None


class CDPFehler(RuntimeError):
    """Fehler beim Start oder bei der Steuerung von Chrome."""


class ChromeFehlt(CDPFehler):
    """Kein Chrome, Chromium oder Edge gefunden."""


# ---------------------------------------------------------------- Chrome finden

def finde_chrome():
    """Pfad zu Chrome/Chromium/Edge oder None."""
    env = os.environ.get("CHROME_PATH")
    if env:
        if os.path.isfile(env) or shutil.which(env):
            return shutil.which(env) or env
        print("CHROME_PATH zeigt auf keine Datei ({}), suche an den üblichen Orten.".format(env),
              file=sys.stderr)
    home = str(Path.home())
    kandidaten = []
    if sys.platform == "darwin":
        for basis in ("/Applications", home + "/Applications"):
            kandidaten += [
                basis + "/Google Chrome.app/Contents/MacOS/Google Chrome",
                basis + "/Chromium.app/Contents/MacOS/Chromium",
                basis + "/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
                basis + "/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
            ]
    elif os.name == "nt":
        for var in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA"):
            basis = os.environ.get(var)
            if basis:
                kandidaten += [
                    basis + r"\Google\Chrome\Application\chrome.exe",
                    basis + r"\Microsoft\Edge\Application\msedge.exe",
                    basis + r"\Chromium\Application\chrome.exe",
                ]
    else:
        for name in ("google-chrome", "google-chrome-stable", "chromium",
                     "chromium-browser", "microsoft-edge", "chrome"):
            pfad = shutil.which(name)
            if pfad:
                kandidaten.append(pfad)
        kandidaten += ["/usr/bin/chromium", "/usr/bin/chromium-browser",
                       "/opt/google/chrome/chrome"]
    # Letzter Versuch: von Playwright/Puppeteer mitgebrachte Browser (Sandboxen)
    for muster in (home + "/.cache/ms-playwright/chromium-*/chrome-linux*/chrome",
                   home + "/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux*/headless_shell",
                   home + "/Library/Caches/ms-playwright/chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium",
                   home + "/.cache/puppeteer/chrome/*/chrome-linux64/chrome"):
        kandidaten += sorted(glob.glob(muster), reverse=True)
    for pfad in kandidaten:
        if pfad and os.path.isfile(pfad) and os.access(pfad, os.X_OK):
            return pfad
    return None


def datei_url(pfad):
    """file://-URL für einen lokalen Pfad (Leerzeichen und Umlaute werden kodiert)."""
    return Path(pfad).expanduser().resolve().as_uri()


# ---------------------------------------------------------------- WebSocket (RFC 6455)

class WebSocket:
    """Kleiner WebSocket-Client: Text-Frames, Fragmente, Ping/Pong, Close."""

    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

    def __init__(self, url, zeitlimit=10):
        teile = urllib.parse.urlparse(url)
        host, port = teile.hostname, teile.port or 80
        pfad = teile.path + ("?" + teile.query if teile.query else "")
        self.sock = socket.create_connection((host, port), timeout=zeitlimit)
        self._puffer = bytearray()
        self._fragmente = []
        self._offen = True
        schluessel = base64.b64encode(os.urandom(16)).decode()
        anfrage = (
            "GET {} HTTP/1.1\r\nHost: {}:{}\r\nUpgrade: websocket\r\n"
            "Connection: Upgrade\r\nSec-WebSocket-Key: {}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n").format(pfad, host, port, schluessel)
        self.sock.sendall(anfrage.encode())
        while b"\r\n\r\n" not in self._puffer:
            daten = self.sock.recv(4096)
            if not daten:
                raise CDPFehler("WebSocket-Handshake mit Chrome abgebrochen.")
            self._puffer += daten
        kopf, _, rest = bytes(self._puffer).partition(b"\r\n\r\n")
        self._puffer = bytearray(rest)
        zeilen = kopf.decode("latin-1").split("\r\n")
        if " 101 " not in zeilen[0] + " ":
            raise CDPFehler("Chrome lehnt die WebSocket-Verbindung ab: " + zeilen[0])
        erwartet = base64.b64encode(
            hashlib.sha1((schluessel + self.GUID).encode()).digest()).decode()
        felder = {z.split(":", 1)[0].strip().lower(): z.split(":", 1)[1].strip()
                  for z in zeilen[1:] if ":" in z}
        if felder.get("sec-websocket-accept") != erwartet:
            raise CDPFehler("WebSocket-Handshake: falscher Accept-Schlüssel.")

    @staticmethod
    def _maskiere(daten, maske):
        if not daten:
            return b""
        n = len(daten)
        lang = (maske * (n // 4 + 1))[:n]
        return (int.from_bytes(daten, "big") ^ int.from_bytes(lang, "big")).to_bytes(n, "big")

    def _sende_frame(self, opcode, nutzlast):
        kopf = bytearray([0x80 | opcode])
        n = len(nutzlast)
        if n < 126:
            kopf.append(0x80 | n)
        elif n < 65536:
            kopf.append(0x80 | 126)
            kopf += struct.pack(">H", n)
        else:
            kopf.append(0x80 | 127)
            kopf += struct.pack(">Q", n)
        maske = os.urandom(4)
        self.sock.sendall(bytes(kopf) + maske + self._maskiere(nutzlast, maske))

    def senden(self, text):
        self._sende_frame(0x1, text.encode("utf-8"))

    def _frame_aus_puffer(self):
        """Ein vollständiges Frame aus dem Puffer nehmen, sonst None (Puffer bleibt heil)."""
        b = self._puffer
        if len(b) < 2:
            return None
        fin, opcode = b[0] & 0x80, b[0] & 0x0F
        maskiert, laenge, pos = b[1] & 0x80, b[1] & 0x7F, 2
        if laenge == 126:
            if len(b) < 4:
                return None
            laenge, pos = struct.unpack(">H", bytes(b[2:4]))[0], 4
        elif laenge == 127:
            if len(b) < 10:
                return None
            laenge, pos = struct.unpack(">Q", bytes(b[2:10]))[0], 10
        maske = b""
        if maskiert:
            if len(b) < pos + 4:
                return None
            maske, pos = bytes(b[pos:pos + 4]), pos + 4
        if len(b) < pos + laenge:
            return None
        nutzlast = bytes(b[pos:pos + laenge])
        del b[:pos + laenge]
        if maskiert:
            nutzlast = self._maskiere(nutzlast, maske)
        return bool(fin), opcode, nutzlast

    def empfangen(self, zeitlimit):
        """Nächste Textnachricht; TimeoutError nach zeitlimit Sekunden."""
        ende = time.monotonic() + zeitlimit
        while True:
            frame = self._frame_aus_puffer()
            if frame is None:
                rest = ende - time.monotonic()
                if rest <= 0:
                    raise TimeoutError()
                self.sock.settimeout(rest)
                try:
                    daten = self.sock.recv(1 << 20)
                except socket.timeout:
                    raise TimeoutError()
                if not daten:
                    self._offen = False
                    raise CDPFehler("Chrome hat die Verbindung geschlossen (abgestürzt?).")
                self._puffer += daten
                continue
            fin, opcode, nutzlast = frame
            if opcode == 0x9:  # Ping
                self._sende_frame(0xA, nutzlast)
                continue
            if opcode == 0xA:  # Pong
                continue
            if opcode == 0x8:  # Close
                try:
                    self._sende_frame(0x8, nutzlast[:2])
                except OSError:
                    pass
                self._offen = False
                raise CDPFehler("Chrome hat die Verbindung geschlossen.")
            if opcode in (0x1, 0x2):
                self._fragmente = [nutzlast]
            elif opcode == 0x0:
                self._fragmente.append(nutzlast)
            if fin:
                nachricht = b"".join(self._fragmente)
                self._fragmente = []
                return nachricht.decode("utf-8", "replace")

    def schliessen(self):
        if self._offen:
            try:
                self._sende_frame(0x8, struct.pack(">H", 1000))
            except OSError:
                pass
            self._offen = False
        try:
            self.sock.close()
        except OSError:
            pass


# ---------------------------------------------------------------- Chrome

def _lokal_holen(url, methode="GET", zeitlimit=5):
    """HTTP an den lokalen DevTools-Port, ohne Proxy aus der Umgebung."""
    oeffner = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    anfrage = urllib.request.Request(url, method=methode)
    with oeffner.open(anfrage, timeout=zeitlimit) as antwort:
        return json.loads(antwort.read().decode("utf-8"))


class Chrome:
    """Eine Headless-Chrome-Instanz als Kontextmanager.

    datei_zugriff=True erlaubt file://-Seiten, andere lokale Dateien zu laden.
    """

    SPERRDATEI = os.path.join(tempfile.gettempdir(), "brand-styleguide-chrome.lock")

    def __init__(self, pfad=None, zeitlimit=30, datei_zugriff=False, warte_auf_sperre_s=180):
        self.pfad = pfad
        self.zeitlimit = zeitlimit
        self.datei_zugriff = datei_zugriff
        self.warte_auf_sperre_s = warte_auf_sperre_s
        self.proc = None
        self.ws = None
        self.hinweise = []
        self._tmp = None
        self._sperre = None
        self._id = 0
        self._ereignisse = collections.deque(maxlen=5000)
        self._medien_typ = ""
        self._merkmale = {}
        self._alte_signale = {}

    # -- Start und Ende

    def __enter__(self):
        try:
            self.starten()
        except BaseException:
            self.beenden()
            raise
        return self

    def __exit__(self, *fehler):
        self.beenden()
        return False

    def _sperren(self):
        """Nur eine Chrome-Instanz dieser Skripte gleichzeitig (POSIX)."""
        if fcntl is None:
            return
        self._sperre = open(self.SPERRDATEI, "a+")
        ende = time.monotonic() + self.warte_auf_sperre_s
        gemeldet = False
        while True:
            try:
                fcntl.flock(self._sperre.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return
            except OSError:
                if time.monotonic() > ende:
                    self._sperre.close()
                    self._sperre = None
                    raise CDPFehler("Eine andere Chrome-Instanz dieser Skripte läuft noch "
                                    "(Sperre " + self.SPERRDATEI + "). Bitte erst beenden.")
                if not gemeldet:
                    print("Warte auf eine andere laufende Chrome-Instanz …", file=sys.stderr)
                    gemeldet = True
                time.sleep(0.5)

    def _signale_abfangen(self):
        """SIGTERM/SIGHUP lösen ein sauberes Beenden aus (nur im Hauptthread)."""
        if threading.current_thread() is not threading.main_thread():
            return

        def abbruch(signum, _frame):
            raise SystemExit(128 + signum)

        for name in ("SIGTERM", "SIGHUP"):
            sig = getattr(signal, name, None)
            if sig is not None:
                try:
                    self._alte_signale[sig] = signal.signal(sig, abbruch)
                except (ValueError, OSError):
                    pass

    def starten(self):
        pfad = self.pfad or finde_chrome()
        if not pfad:
            raise ChromeFehlt("Kein Chrome, Chromium oder Edge gefunden. "
                              "Pfad mit der Umgebungsvariable CHROME_PATH angeben.")
        self._sperren()
        self._signale_abfangen()
        atexit.register(self.beenden)
        self._tmp = tempfile.mkdtemp(prefix="bsg-chrome-")
        profil = os.path.join(self._tmp, "profil")
        os.makedirs(profil)
        args = [pfad, "--headless=new", "--remote-debugging-port=0",
                "--user-data-dir=" + profil, "--no-first-run", "--no-default-browser-check",
                "--disable-gpu", "--hide-scrollbars", "--disable-extensions",
                "--mute-audio", "--disable-sync", "--disable-background-networking",
                "--disable-component-update", "--disable-default-apps",
                "--password-store=basic", "--use-mock-keychain"]
        if self.datei_zugriff:
            args.append("--allow-file-access-from-files")
        if sys.platform.startswith("linux"):
            args.append("--disable-dev-shm-usage")
            if hasattr(os, "geteuid") and os.geteuid() == 0:
                args.append("--no-sandbox")  # als root (VM/Container) nötig
        args.append("about:blank")
        self._log = open(os.path.join(self._tmp, "chrome.log"), "wb")
        optionen = {"stdout": subprocess.DEVNULL, "stderr": self._log, "stdin": subprocess.DEVNULL}
        if os.name == "nt":
            optionen["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        else:
            optionen["start_new_session"] = True
        try:
            self.proc = subprocess.Popen(args, **optionen)
        except OSError as e:
            raise CDPFehler("Chrome ließ sich nicht starten ({}): {}".format(pfad, e))

        # Port aus DevToolsActivePort lesen
        portdatei = os.path.join(profil, "DevToolsActivePort")
        ende = time.monotonic() + self.zeitlimit
        port = None
        while time.monotonic() < ende:
            if self.proc.poll() is not None:
                raise CDPFehler("Chrome hat sich sofort beendet (Code {}). {}".format(
                    self.proc.returncode, self._log_ende()))
            try:
                with open(portdatei) as f:
                    zeilen = f.read().split()
                if zeilen and zeilen[0].isdigit():
                    port = int(zeilen[0])
                    break
            except OSError:
                pass
            time.sleep(0.1)
        if not port:
            raise CDPFehler("Chrome hat keinen DevTools-Port gemeldet (Zeitlimit {} s). {}".format(
                self.zeitlimit, self._log_ende()))
        self.port = port

        # Ziel (Tab) finden oder anlegen
        basis = "http://127.0.0.1:{}".format(port)
        ziel = None
        try:
            ziele = _lokal_holen(basis + "/json/list")
            ziel = next((z for z in ziele if z.get("type") == "page"
                         and z.get("webSocketDebuggerUrl")), None)
        except Exception:
            ziel = None
        if ziel is None:
            try:
                ziel = _lokal_holen(basis + "/json/new?about:blank", methode="PUT")
            except Exception as e:
                raise CDPFehler("Kein Tab in Chrome verfügbar: {}".format(e))
        self.ws = WebSocket(ziel["webSocketDebuggerUrl"], zeitlimit=self.zeitlimit)
        self.send("Page.enable")
        self.send("Runtime.enable")
        return self

    def _log_ende(self, zeichen=600):
        try:
            with open(os.path.join(self._tmp, "chrome.log"), "rb") as f:
                text = f.read().decode("utf-8", "replace").strip()
            return ("Chrome meldet: " + text[-zeichen:]) if text else ""
        except OSError:
            return ""

    def beenden(self):
        """Verbindung schließen, Prozessgruppe beenden, Profil löschen. Mehrfach aufrufbar."""
        if self.ws is not None:
            try:
                self.ws.schliessen()
            except Exception:
                pass
            self.ws = None
        if self.proc is not None:
            if self.proc.poll() is None:
                self._prozess_beenden()
            self.proc = None
        if getattr(self, "_log", None):
            try:
                self._log.close()
            except OSError:
                pass
            self._log = None
        if self._tmp:
            for _ in range(10):  # Chrome schreibt beim Beenden kurz nach
                shutil.rmtree(self._tmp, ignore_errors=True)
                if not os.path.exists(self._tmp):
                    break
                time.sleep(0.2)
            self._tmp = None
        if self._sperre is not None:
            try:
                fcntl.flock(self._sperre.fileno(), fcntl.LOCK_UN)
                self._sperre.close()
            except OSError:
                pass
            self._sperre = None
        for sig, alt in self._alte_signale.items():
            try:
                signal.signal(sig, alt)
            except (ValueError, OSError):
                pass
        self._alte_signale = {}
        try:
            atexit.unregister(self.beenden)
        except Exception:
            pass

    def _prozess_beenden(self):
        p = self.proc
        if os.name == "nt":
            subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                p.wait(5)
            except subprocess.TimeoutExpired:
                p.kill()
            return
        for sig, warte in ((signal.SIGTERM, 5), (signal.SIGKILL, 5)):
            try:
                os.killpg(p.pid, sig)  # ganze Gruppe: Renderer, GPU, Netzwerk
            except (ProcessLookupError, PermissionError):
                pass
            try:
                p.wait(warte)
                break
            except subprocess.TimeoutExpired:
                continue
        # Helfer, die evtl. noch hängen
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass

    # -- Protokoll

    def send(self, methode, params=None, timeout=30):
        """CDP-Befehl senden und auf die passende Antwort warten."""
        if self.ws is None:
            raise CDPFehler("Keine Verbindung zu Chrome.")
        self._id += 1
        mid = self._id
        self.ws.senden(json.dumps({"id": mid, "method": methode, "params": params or {}}))
        ende = time.monotonic() + timeout
        while True:
            rest = ende - time.monotonic()
            try:
                if rest <= 0:
                    raise TimeoutError()
                nachricht = json.loads(self.ws.empfangen(rest))
            except TimeoutError:
                raise CDPFehler("Zeitüberschreitung: Chrome hat auf {} nicht innerhalb von {} s "
                                "geantwortet.".format(methode, timeout))
            if nachricht.get("id") == mid:
                if "error" in nachricht:
                    raise CDPFehler("{} fehlgeschlagen: {}".format(
                        methode, nachricht["error"].get("message", nachricht["error"])))
                return nachricht.get("result", {})
            if "method" in nachricht:
                self._ereignisse.append(nachricht)

    def warte_auf_ereignis(self, name, timeout=30):
        """Wartet auf ein CDP-Ereignis (auch bereits gepufferte) und gibt dessen params zurück."""
        for e in list(self._ereignisse):
            if e.get("method") == name:
                self._ereignisse.remove(e)
                return e.get("params", {})
        ende = time.monotonic() + timeout
        while True:
            rest = ende - time.monotonic()
            try:
                if rest <= 0:
                    raise TimeoutError()
                nachricht = json.loads(self.ws.empfangen(rest))
            except TimeoutError:
                raise CDPFehler("Zeitüberschreitung beim Warten auf {} ({} s).".format(name, timeout))
            if nachricht.get("method") == name:
                return nachricht.get("params", {})
            if "method" in nachricht:
                self._ereignisse.append(nachricht)

    # -- Helfer

    def navigiere(self, url, warten_s=1.0, zeitlimit=45):
        """Seite laden, auf load warten, zusätzlich warten, dann auf Schriften."""
        self._ereignisse.clear()
        ergebnis = self.send("Page.navigate", {"url": url}, timeout=zeitlimit)
        if ergebnis.get("errorText"):
            raise CDPFehler("Seite nicht ladbar: {} ({})".format(url, ergebnis["errorText"]))
        try:
            self.warte_auf_ereignis("Page.loadEventFired", zeitlimit)
        except CDPFehler:
            self.hinweise.append("{}: load-Ereignis kam nicht innerhalb von {} s, "
                                 "gemessen wurde der bis dahin geladene Stand.".format(url, zeitlimit))
        if warten_s:
            time.sleep(warten_s)
        try:
            self.auswerten("document.fonts.ready.then(() => true)", timeout=15)
        except CDPFehler:
            self.hinweise.append(url + ": Schriften waren nach 15 s nicht fertig geladen.")

    def viewport(self, breite, hoehe, mobil=False, dpr=1):
        self.send("Emulation.setDeviceMetricsOverride", {
            "width": int(breite), "height": int(hoehe),
            "deviceScaleFactor": dpr, "mobile": bool(mobil)})

    def _medien_setzen(self):
        self.send("Emulation.setEmulatedMedia", {
            "media": self._medien_typ,
            "features": [{"name": k, "value": v} for k, v in self._merkmale.items()]})

    def farbschema(self, schema):
        """'dark' oder 'light' (auch 'dunkel'/'hell'); None hebt die Emulation auf."""
        wert = {"dunkel": "dark", "hell": "light"}.get(schema, schema) or ""
        self._merkmale["prefers-color-scheme"] = wert
        self._medien_setzen()

    def reduzierte_bewegung(self, an=True):
        self._merkmale["prefers-reduced-motion"] = "reduce" if an else ""
        self._medien_setzen()

    def medientyp(self, typ):
        """'print', 'screen' oder '' (Standard)."""
        self._medien_typ = typ or ""
        self._medien_setzen()

    def auswerten(self, js, timeout=30):
        """JavaScript im Seitenkontext ausführen; Promises werden abgewartet."""
        ergebnis = self.send("Runtime.evaluate", {
            "expression": js, "returnByValue": True, "awaitPromise": True,
            "userGesture": True}, timeout=timeout)
        if "exceptionDetails" in ergebnis:
            d = ergebnis["exceptionDetails"]
            text = (d.get("exception") or {}).get("description") or d.get("text", "unbekannt")
            raise CDPFehler("JavaScript-Fehler: " + text.splitlines()[0][:300])
        return ergebnis.get("result", {}).get("value")

    def seitenmasse(self):
        """CSS-Pixel: (Inhaltsbreite, Inhaltshöhe, Viewportbreite, Viewporthöhe)."""
        m = self.send("Page.getLayoutMetrics")
        inhalt = m.get("cssContentSize") or m.get("contentSize") or {}
        vp = m.get("cssLayoutViewport") or m.get("layoutViewport") or {}
        return (inhalt.get("width", 0), inhalt.get("height", 0),
                vp.get("clientWidth", 0), vp.get("clientHeight", 0))

    def screenshot(self, pfad, voll=False, max_hoehe=8000, clip=None, timeout=90):
        """PNG speichern. voll=True: ganze Seite bis max_hoehe. clip={x,y,width,height} in CSS-px."""
        params = {"format": "png"}
        info = {"pfad": str(pfad)}
        if clip is not None:
            params["clip"] = dict(clip, scale=1)
            params["captureBeyondViewport"] = True
            info.update(breite=round(clip["width"]), hoehe=round(clip["height"]))
        elif voll:
            breite, hoehe, vp_breite, _ = self.seitenmasse()
            breite = vp_breite or breite
            hoehe_cap = min(hoehe, max_hoehe)
            params["clip"] = {"x": 0, "y": 0, "width": breite, "height": hoehe_cap, "scale": 1}
            params["captureBeyondViewport"] = True
            info.update(breite=round(breite), hoehe=round(hoehe_cap),
                        seitenhoehe=round(hoehe), abgeschnitten=hoehe > max_hoehe)
        ergebnis = self.send("Page.captureScreenshot", params, timeout=timeout)
        Path(pfad).parent.mkdir(parents=True, exist_ok=True)
        with open(pfad, "wb") as f:
            f.write(base64.b64decode(ergebnis["data"]))
        return info

    def pdf(self, pfad, querformat=None, css_seitengroesse=True, timeout=180):
        """PDF mit Hintergründen. Ränder 0, sofern @page nichts anderes sagt."""
        params = {"printBackground": True, "preferCSSPageSize": bool(css_seitengroesse),
                  "marginTop": 0, "marginBottom": 0, "marginLeft": 0, "marginRight": 0}
        if querformat is not None:
            params["landscape"] = bool(querformat)
        ergebnis = self.send("Page.printToPDF", params, timeout=timeout)
        Path(pfad).parent.mkdir(parents=True, exist_ok=True)
        daten = base64.b64decode(ergebnis["data"])
        with open(pfad, "wb") as f:
            f.write(daten)
        return {"pfad": str(pfad), "bytes": len(daten)}
