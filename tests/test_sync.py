# -*- coding: utf-8 -*-
"""Progression partagée entre deux appareils (un iPhone et un ordinateur) par le serveur de synchronisation
(outils/sync/worker.mjs, lancé ici par outils/sync/serveur_local.mjs, base SQLite en mémoire), et bouton Installer.

Code trop court, code inconnu (Créer ou Annuler), créer un code, le rejoindre autrement écrit (seuls ses lettres et
chiffres comptent), mots et questions transmis, réglages partagés ou propres à l'appareil, changements des deux côtés
(dernière réponse gardée, compteurs et historique additionnés), pas d'aller-retour sans fin, réponse du serveur perdue
(rien compté deux fois), hors ligne puis de retour, examens blancs des deux appareils gardés, version plus récente
refusée, arrêt, bouton Installer et critères d'installation de Chrome.
Lancer depuis la racine du dépôt :  py tests\\test_sync.py      (demande Node 22.13 ou plus)
"""
import hashlib
import json
import os
import re
import socket
import subprocess
import time
import unicodedata
import urllib.error
import urllib.request

from playwright.sync_api import sync_playwright

from commun import REPO, check, finish, fresh_copy, nb, new_page, serve, shot, state, wait_ready

CODE = "Tigre violet 2028"


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def start_server():
    port = free_port()
    proc = subprocess.Popen(["node", os.path.join(REPO, "outils", "sync", "serveur_local.mjs"), "--port", str(port)],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    url = "http://127.0.0.1:%d" % port
    for _ in range(100):
        try:
            if json.loads(urllib.request.urlopen(url + "/sante", timeout=1).read()) == "ok":
                return proc, url
        except Exception:
            time.sleep(0.1)
    raise SystemExit("le serveur de synchronisation ne démarre pas (Node 22.13 ou plus ?)")


def key_of(code):
    """Comme l'appli : seuls les lettres et chiffres du code comptent (codeKey)."""
    k = "".join(c for c in unicodedata.normalize("NFKD", code) if not unicodedata.combining(c)).lower()
    return hashlib.sha256(("cap945:" + re.sub(r"[^a-z0-9]", "", k)).encode("utf-8")).hexdigest()


def server_doc(url):
    return json.loads(urllib.request.urlopen("%s/p/%s" % (url, key_of(CODE))).read())


def server_put(url, v, data):
    req = urllib.request.Request("%s/p/%s" % (url, key_of(CODE)), method="PUT", data=json.dumps({"v": v, "data": data}).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(req).read())
    except urllib.error.HTTPError as e:
        return {"status": e.code, **json.loads(e.read())}


def sync_now(page):
    """« Synchroniser » dans Réglages, puis attendre la fin de l'échange."""
    page.click('.tab[data-view="reglages"]')
    page.click('[data-sync="now"]')
    page.wait_for_function("() => !syncing", timeout=10000)
    return page.evaluate("() => sync && sync.err")


def doc(page):
    return page.evaluate("() => canon(docOf(state))")


def same_server():
    """outils/sync est une copie du serveur de 形音义 : la comparer au dépôt xingyinyi s'il est sur cet ordinateur
    (variable XINGYINYI, sinon Documents\\Chinois_App\\xingyinyi-appli à côté de ce dépôt)."""
    print("\n— copie du serveur")
    xing = os.environ.get("XINGYINYI") or os.path.join(REPO, "..", "..", "Chinois_App", "xingyinyi-appli")
    read = lambda p: open(p, encoding="utf-8").read().replace("\r\n", "\n")
    for f in ("worker.mjs", "serveur_local.mjs"):
        theirs = os.path.join(xing, "outils", "sync", f)
        if not os.path.exists(theirs):
            print("  (dépôt xingyinyi introuvable : %s non comparé)" % f)
            continue
        check(read(theirs) == read(os.path.join(REPO, "outils", "sync", f)), "outils/sync/%s identique à celui du dépôt xingyinyi" % f)


def main():
    errors = []
    same_server()
    proc, sync_url = start_server()
    site = fresh_copy("sync")
    path = os.path.join(site, "index.html")
    html = open(path, encoding="utf-8").read()
    html = re.sub(r'const SYNC_URL = "[^"]*";', 'const SYNC_URL = "%s";' % sync_url, html)
    open(path, "w", encoding="utf-8").write(html)
    httpd, url = serve(site)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            ctx_a, a = new_page(browser, errors, offline_ok=True)                                         # the iPhone
            ctx_b, b = new_page(browser, errors, size=(1366, 768), mobile=False, offline_ok=True)         # the computer
            for page in (a, b):
                page.goto(url)
                wait_ready(page)

            print("\n— créer un code")
            a.click('.tab[data-view="reglages"]')
            a.fill("#sync-code", "abc-12")
            a.click('[data-sync="join"]')
            check("au moins 8" in a.inner_text("#sync-box"), "code trop court refusé")
            a.fill("#sync-code", "personne-ne-l-utilise")
            a.click('[data-sync="join"]')
            a.wait_for_selector('[data-sync="create"]')
            a.click('[data-sync="cancel"]')
            check(a.locator("#sync-code").count() == 1 and a.evaluate("() => sync") is None, "code inconnu : rien n'est créé sans « Créer »")
            ids = a.evaluate("() => ORDER.slice(0, 3)")
            a.evaluate("""ids => { applyGrade(ids[0], true); applyGrade(ids[1], false); recordAnswer(P5[0], true, 9000, P5[0].ans);
              state.settings.exam = '2028-01-15'; state.settings.theme = 'dark'; save(); }""", ids)
            a.fill("#sync-code", CODE)
            a.press("#sync-code", "Enter")
            a.wait_for_selector('[data-sync="create"]')
            a.click('[data-sync="create"]')
            a.wait_for_function("() => sync && !syncing && sync.at > 0", timeout=10000)
            s = server_doc(sync_url)
            check(s["v"] > 0 and s["data"]["app"] == "cap945" and ids[0] in s["data"]["words"], "code créé : la progression est sur le serveur")
            check("theme" not in s["data"]["settings"] and s["data"]["settings"]["exam"] == "2028-01-15", "réglages : le thème reste sur l'appareil, la date d'examen part")
            check("Synchronisé aujourd’hui" in nb(a.inner_text("#sync-box")), "état affiché", a.inner_text("#sync-box"))
            shot(a, "sync-iphone", full=True)

            print("\n— rejoindre le code")
            b.click('.tab[data-view="reglages"]')
            b.fill("#sync-code", "tigre-VIOLET 2028")
            b.click('[data-sync="join"]')
            b.wait_for_function("() => sync && !syncing && sync.at > 0", timeout=10000)
            sb = state(b)
            check(sb["words"].get(ids[0], {}).get("b") == 1 and sb["words"].get(ids[1], {}).get("b") == 0, "le code autrement écrit : les mots arrivent")
            check(sb["q"].get(a.evaluate("() => P5[0].id"), {}).get("r") == 1, "les questions arrivent")
            check(sb["settings"]["exam"] == "2028-01-15" and sb["settings"]["theme"] == "auto", "date d'examen reçue, thème inchangé")
            check(doc(a) == doc(b), "les deux appareils ont la même progression")
            v0 = server_doc(sync_url)["v"]
            check(not sync_now(a) and not sync_now(b) and server_doc(sync_url)["v"] == v0, "rien de nouveau : aucun envoi, pas d'aller-retour")

            print("\n— changements des deux côtés")
            r0 = sb["words"][ids[0]]["r"]
            log0 = a.evaluate("() => state.log[dayNum()]")
            a.evaluate("ids => { applyGrade(ids[0], false); applyGrade(ids[2], true); save(); }", ids)
            b.evaluate("ids => { applyGrade(ids[0], true); recordAnswer(P5[1], false, 7000, (P5[1].ans + 1) % 4); save(); }", ids)
            log_a, log_b = a.evaluate("() => state.log[dayNum()]"), b.evaluate("() => state.log[dayNum()]")
            check(not sync_now(a) and not sync_now(b) and not sync_now(a), "trois échanges sans erreur")
            check(doc(a) == doc(b), "après échange : la même progression des deux côtés")
            w = state(a)["words"][ids[0]]
            check(w["r"] == r0 + 2, "un mot révisé des deux côtés : révisions additionnées", w)
            check(state(a)["words"].get(ids[2], {}).get("b") == 1 and state(b)["q"].get(b.evaluate("() => P5[1].id"), {}).get("l") == 1
                  and state(a)["q"].get(b.evaluate("() => P5[1].id"), {}).get("l") == 1, "changements d'un seul côté : gardés")
            log = state(a)["log"][str(a.evaluate("() => dayNum()"))]
            check(all(log.get(k, 0) == log_a.get(k, 0) + log_b.get(k, 0) - log0.get(k, 0) for k in ("n", "r", "p5", "p5ok")),
                  "historique du jour additionné", (log, log_a, log_b, log0))
            v1 = server_doc(sync_url)["v"]
            check(not sync_now(b) and not sync_now(a) and server_doc(sync_url)["v"] == v1, "plus rien à échanger")

            print("\n— réponse du serveur perdue")
            r1 = state(b)["words"][ids[2]]["r"]
            b.evaluate("ids => { applyGrade(ids[2], true); save(); }", ids)

            def lose(route):
                if route.request.method == "PUT":
                    route.fetch()            # the server gets it…
                    route.abort()            # …but the answer never comes back
                else:
                    route.continue_()
            b.route(sync_url + "/p/**", lose)
            err = sync_now(b)
            check(bool(err), "réponse perdue : échec affiché", err)
            b.unroute(sync_url + "/p/**")
            check(not sync_now(b), "nouvel essai réussi")
            check(state(b)["words"][ids[2]]["r"] == r1 + 1 and server_doc(sync_url)["data"]["words"][ids[2]]["r"] == r1 + 1, "rien n'est compté deux fois")

            print("\n— réponse perdue, puis fusion par l'autre appareil")
            r2 = state(b)["words"][ids[2]]["r"]
            today = str(b.evaluate("() => dayNum()"))
            lr = state(b)["log"][today].get("r", 0)
            b.evaluate("ids => { applyGrade(ids[2], true); save(); }", ids)
            b.route(sync_url + "/p/**", lose)
            check(bool(sync_now(b)), "réponse perdue de nouveau")
            b.unroute(sync_url + "/p/**")
            a.evaluate("ids => { applyGrade(ids[1], true); save(); }", ids)
            check(not sync_now(a) and state(a)["words"][ids[2]]["r"] == r2 + 1, "l'autre appareil reçoit l'envoi arrivé et le fusionne avec le sien")
            check(not sync_now(b) and not sync_now(a), "nouvel essai, puis échange")
            check(state(b)["words"][ids[2]]["r"] == r2 + 1 and state(a)["words"][ids[2]]["r"] == r2 + 1 and doc(a) == doc(b),
                  "envoi perdu puis fusionné ailleurs : rien n'est compté deux fois", (state(b)["words"][ids[2]], r2))
            check(state(b)["log"][today]["r"] == state(a)["log"][today]["r"] == lr + 2, "… ni dans l'historique du jour (une révision de chaque côté)",
                  (state(b)["log"][today], lr))

            print("\n— même mot, le même jour, sur les deux appareils")
            b.evaluate("ids => { applyGrade(ids[0], true); save(); }", ids)           # the earlier review
            b.wait_for_timeout(30)
            a.evaluate("ids => { applyGrade(ids[0], false); save(); }", ids)          # the later one
            wa = state(a)["words"][ids[0]]
            check(not sync_now(a) and not sync_now(b) and not sync_now(a), "échanges réussis")
            w1, w2 = state(a)["words"][ids[0]], state(b)["words"][ids[0]]
            check(w1["b"] == w2["b"] == wa["b"] == 0 and w1["at"] == w2["at"] == wa["at"], "la révision la plus récente l'emporte, même le même jour", (wa, w1, w2))

            print("\n— hors ligne")
            ctx_a.set_offline(True)
            a.evaluate("() => { recordAnswer(P5[2], true, 8000, P5[2].ans); save(); }")
            err = sync_now(a)
            check(err and "réseau" in err, "hors ligne : échec expliqué", err)
            check("Échec" in a.inner_text("#sync-box"), "hors ligne : échec affiché")
            ctx_a.set_offline(False)
            check(not sync_now(a) and not sync_now(b), "réseau revenu : échange réussi")
            check(state(b)["q"].get(a.evaluate("() => P5[2].id"), {}).get("r") == 1, "la réponse donnée hors ligne arrive")

            print("\n— examens blancs")
            for page, t in ((a, 1000), (b, 2000)):
                page.evaluate("""t => { state.mocks.unshift({ at: Date.now() - t, format: 'half', parts: {}, L: { score: 400 }, R: { score: 380 },
                  total: 780, readMs: 0 }); save(); }""", t)
            check(not sync_now(a) and not sync_now(b) and not sync_now(a), "échanges réussis")
            check(len(state(a)["mocks"]) == 2 and len(state(b)["mocks"]) == 2, "les examens blancs des deux appareils sont gardés")

            print("\n— double appui sur « Synchroniser »")
            a.click('[data-sync="stop"]')
            a.fill("#sync-code", CODE)
            a.evaluate("() => { const b = document.querySelector('[data-sync=\"join\"]'); b.click(); b.click(); }")   # two taps at once
            try:
                a.wait_for_function("() => sync && sync.at > 0 && !syncing", timeout=10000)
                joined = True
            except Exception:
                joined = False
            check(joined and not a.evaluate("() => sync.err") and doc(a) == doc(b), "double appui : le code est rejoint quand même")

            print("\n— version plus récente")
            s = server_doc(sync_url)
            newer = dict(s["data"], fmt=99)
            check(server_put(sync_url, s["v"], newer).get("v"), "document d'une version future écrit sur le serveur")
            a.evaluate("() => { state.settings.p5Size = 10; save(); }")
            err = sync_now(a)
            check(err and "plus récente" in err, "document d'une version plus récente : refusé, sans rien changer", err)
            check(state(a)["settings"]["p5Size"] == 10, "progression d'ici intacte")

            print("\n— arrêt")
            a.click('[data-sync="stop"]')
            check(a.evaluate("() => sync") is None and a.evaluate("() => localStorage.getItem('cap945.sync-base')") is None
                  and a.locator("#sync-code").count() == 1, "arrêt : le code est oublié sur cet appareil")
            check(len(state(a)["words"]) >= 3, "arrêt : la progression reste")

            print("\n— installer sur l'ordinateur")
            b.evaluate("""() => { const e = new Event('beforeinstallprompt', { cancelable: true });
              e.prompt = () => { window.__prompted = true; }; e.userChoice = Promise.resolve({ outcome: 'accepted' }); window.dispatchEvent(e); }""")
            b.click('.tab[data-view="reglages"]')
            check(b.locator("#app-install").count() == 1, "Réglages : bouton Installer")
            shot(b, "sync-ordinateur", full=True)
            b.click("#app-install")
            b.wait_for_function("() => !document.querySelector('#app-install')")
            check(b.evaluate("() => window.__prompted") is True, "Installer : la demande du navigateur s'ouvre")
            b.evaluate("() => navigator.serviceWorker.ready")
            cdp = ctx_b.new_cdp_session(b)
            errs = cdp.send("Page.getInstallabilityErrors").get("installabilityErrors", [])
            check(errs == [], "Chrome : l'appli remplit les critères d'installation", errs)
            ctx_a.close()
            ctx_b.close()
            browser.close()
    finally:
        proc.terminate()
        httpd.shutdown()
    errors[:] = [e for e in errors if "409 (Conflict)" not in e]   # a 409 is the server's normal answer to an old version
    finish(errors)


if __name__ == "__main__":
    main()
