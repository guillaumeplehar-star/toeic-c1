# -*- coding: utf-8 -*-
"""Outils communs aux tests de Cap 945 (Playwright, Chromium sans fenêtre).

Les tests tournent sur une copie du dépôt dont le dossier banque/ est remplacé par tests/donnees/banque :
ils ne dépendent donc pas du contenu de la vraie banque. La voix est simulée (Chromium sans fenêtre n'en a pas) :
chaque phrase « dite » est notée dans window.__said.

Prérequis (une fois) :  py -m pip install playwright   puis   py -m playwright install chromium
"""
import functools
import http.server
import json
import os
import shutil
import socketserver
import sys
import threading

for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

TESTS = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(TESTS)
SORTIE = os.path.join(TESTS, "sortie")
CAPTURES = os.path.join(SORTIE, "captures")
os.makedirs(CAPTURES, exist_ok=True)

failures = []


def check(cond, label, detail=""):
    print(("  ok   " if cond else "  ÉCHEC ") + label + ("" if cond else "  -> %s" % (detail,)))
    if not cond:
        failures.append(label)


class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a, **k):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "max-age=600")  # ce qu'envoie GitHub Pages
        super().end_headers()


class Server(socketserver.ThreadingTCPServer):
    def handle_error(self, request, client_address):
        if not isinstance(sys.exc_info()[1], (ConnectionAbortedError, ConnectionResetError, BrokenPipeError)):
            super().handle_error(request, client_address)


def serve(folder):
    handler = functools.partial(Handler, directory=folder)
    httpd = Server(("127.0.0.1", 0), handler)
    httpd.daemon_threads = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, "http://127.0.0.1:%d/" % httpd.server_address[1]


IGNORE = shutil.ignore_patterns(".git", "tests", "__pycache__", "node_modules", ".claude", "*.pyc", "outils")


def fresh_copy(name, real_bank=False):
    """Copie du site (racine du dépôt), avec la banque de test figée sauf real_bank."""
    dst = os.path.join(SORTIE, name)
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(REPO, dst, ignore=IGNORE)
    if not real_bank:
        shutil.rmtree(os.path.join(dst, "banque"))
        shutil.copytree(os.path.join(TESTS, "donnees", "banque"), os.path.join(dst, "banque"))
    return dst


VOICES = [("Samantha", "en-US"), ("Daniel", "en-GB"), ("Karen", "en-AU"), ("Zarvox", "en-US"), ("Thomas", "fr-FR")]


def speech_script(voices=VOICES):
    """voices : (nom, langue) ou (nom, langue, identifiant) ou (nom, langue, identifiant, voix locale)."""
    def one(v):
        n, l = v[0], v[1]
        uri = v[2] if len(v) > 2 else None
        local = v[3] if len(v) > 3 else True
        return '{name:%s,lang:"%s",localService:%s,default:false,voiceURI:%s}' % (json.dumps(n), l, "true" if local else "false", json.dumps(uri or n))
    vs = ",".join(one(v) for v in voices)
    return """(() => {
  const voices = [%s];
  const said = window.__said = [];
  class U { constructor(t) { this.text = t; this.lang = ""; this.voice = null; this.rate = 1; this.pitch = 1; this.onend = null; this.onerror = null; } }
  const synth = {
    speaking: false, pending: false, paused: false,
    getVoices() { return voices; },
    speak(u) {
      said.push({ text: u.text, voice: u.voice && u.voice.name, uri: u.voice && u.voice.voiceURI, pitch: u.pitch, rate: u.rate });
      if (window.__netFails && u.voice && u.voice.localService === false) {   // a network voice that cannot reach its server
        setTimeout(() => { if (u.onerror) u.onerror({ error: "network" }); }, 5);
        return;
      }
      setTimeout(() => { if (u.onend) u.onend({}); }, window.__speechMs == null ? 20 : window.__speechMs);
    },
    cancel() {}, pause() {}, resume() {},
    addEventListener() {}, removeEventListener() {},
  };
  Object.defineProperty(window, "speechSynthesis", { value: synth, configurable: true });
  window.SpeechSynthesisUtterance = U;
})();""" % vs


def new_page(browser, errors, scheme="light", size=(390, 844), offline_ok=False, mobile=True, voices=VOICES):
    ctx = browser.new_context(viewport={"width": size[0], "height": size[1]}, device_scale_factor=2 if mobile else 1,
                              is_mobile=mobile, has_touch=mobile, color_scheme=scheme, locale="fr-FR", accept_downloads=True)
    ctx.add_init_script(speech_script(voices))
    page = ctx.new_page()

    def on_console(m):
        if m.type in ("error", "warning"):
            if offline_ok and ("Failed to fetch" in m.text or "ERR_INTERNET_DISCONNECTED" in m.text or "net::" in m.text):
                return
            errors.append("%s: %s" % (m.type, m.text))
    page.on("console", on_console)
    page.on("pageerror", lambda e: errors.append("pageerror: %s" % e))
    return ctx, page


def wait_ready(page):
    page.wait_for_function("() => typeof BANK !== 'undefined' && BANK && current", timeout=15000)
    page.wait_for_timeout(300)


def state(page):
    """L'état de l'appli (progression et réglages)."""
    return page.evaluate("() => state")


def nb(s):
    """Espaces insécables (fines ou non) -> espaces ordinaires, pour comparer les textes de l'appli."""
    return (s or "").replace(" ", " ").replace(" ", " ")


def shot(page, name, full=False):
    page.screenshot(path=os.path.join(CAPTURES, name + ".png"), full_page=full)


def finish(errors):
    print("\nerreurs dans la console :", len(errors))
    for e in errors[:30]:
        print("  ", e)
    print("échecs :", failures if failures else "aucun")
    print("captures d'écran :", CAPTURES)
    sys.exit(1 if failures or errors else 0)
