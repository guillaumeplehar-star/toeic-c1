# -*- coding: utf-8 -*-
"""Test de Cap 945 : vocabulaire, Part 5, Part 2, Progrès, Réglages, sauvegarde, reprise, hors ligne.

    py tests\\test_appli.py

Banque de test figée (tests/donnees/banque) : 10 mots en deux thèmes, 12 questions de Part 5, 8 de Part 2.
Captures d'écran dans tests/sortie/captures.
"""
import json
import os

from playwright.sync_api import sync_playwright

from commun import CAPTURES, check, finish, fresh_copy, new_page, nb, serve, shot, wait_ready


def today(page):
    return page.evaluate("() => dayNum()")


def state(page):
    return page.evaluate("() => state")


def vocab(page, errors):
    print("\n— vocabulaire")
    check(page.evaluate("() => current") == "mots", "l'appli s'ouvre sur Mots")
    check(page.evaluate("() => WORDS.length") == 10, "10 mots chargés", page.evaluate("() => WORDS.length"))
    counts = "".join(nb(page.inner_text("#counts")).split())
    check("0àrevoir" in counts and "10nouveaux" in counts, "compteurs : 0 à revoir, 10 nouveaux", counts)
    check(page.is_visible("#v-turn") and page.is_hidden("#v-grades"), "carte face anglaise, bouton « Voir la réponse »")
    said = page.evaluate("() => window.__said.length")
    shot(page, "mots-recto")
    page.click("#v-turn")
    check(page.is_visible("#v-grades") and page.is_visible(".v-back"), "la réponse s'affiche avec × et √")
    check(page.is_visible(".v-back mark"), "le mot est surligné dans l'exemple")
    shot(page, "mots-verso")
    first = page.evaluate("() => vstudy.cur")
    page.click('.grade[data-g="1"]')
    c = state(page)["words"][first]
    check(c["b"] == 1 and c["d"] == today(page) + 1, "√ : seau 1, revient demain", c)
    # × then four other cards: the missed word comes back
    missed = page.evaluate("() => vstudy.cur")
    page.click("#v-turn")
    page.click('.grade[data-g="0"]')
    c = state(page)["words"][missed]
    check(c["b"] == 0 and "k" in c, "× : seau 0, à reprendre", c)
    seen = []
    for _ in range(4):
        seen.append(page.evaluate("() => vstudy.cur"))
        page.click("#v-turn")
        page.click('.grade[data-g="1"]')
    check(missed not in seen, "le mot raté ne revient pas tout de suite", seen)
    check(page.evaluate("() => vstudy.cur") == missed, "il revient après quatre autres cartes", page.evaluate("() => vstudy.cur"))
    check("À reprendre" in page.inner_text(".v-meta"), "étiquette « À reprendre »", page.inner_text(".v-meta"))
    # keyboard
    page.keyboard.press("Space")
    check(page.is_visible("#v-grades"), "Espace tourne la carte")
    page.keyboard.press("2")
    check(state(page)["words"][missed]["b"] == 1, "la touche 2 note √")
    cur = page.evaluate("() => WBYID.get(vstudy.cur).en")
    page.wait_for_function("en => window.__said.some(s => s.text === en)", arg=cur, timeout=3000)
    check(page.evaluate("() => window.__said.length") > said, "le mot est lu à voix haute")
    voices = {s["voice"] for s in page.evaluate("() => window.__said")}
    check(not voices & {"Zarvox", "Thomas"}, "ni voix fantaisie ni voix française", voices)
    # French first
    page.click('.tab[data-view="reglages"]')
    page.click('[data-set="firstSide"][data-v="fr"]')
    page.click('.tab[data-view="mots"]')
    w = page.evaluate("() => WBYID.get(vstudy.cur)")
    check(nb(w["fr"]).split(";")[0].strip() in nb(page.inner_text(".v-front")), "face française d'abord", page.inner_text(".v-front"))
    page.click("#v-turn")
    check(page.is_visible(".v-back .v-en"), "l'anglais au verso")
    page.click('.tab[data-view="reglages"]')
    page.click('[data-set="firstSide"][data-v="en"]')
    # word list
    page.click('.tab[data-view="mots"]')
    page.click("#v-browse")
    page.fill("#w-q", "factur")
    check(page.locator(".wrow").count() == 1 and "invoice" in page.inner_text(".wrow"), "recherche en français sans accent")
    page.click(".wrow")
    check(page.is_visible(".wmore .v-ex"), "un mot de la liste s'ouvre sur son exemple")
    shot(page, "mots-liste")
    page.keyboard.press("Escape")
    check(page.is_hidden("#sheet"), "Échap ferme la feuille")


def part5(page, errors):
    print("\n— Part 5")
    page.click('.tab[data-view="lecture"]')
    check(page.is_visible("#p5-home") and "Part 5" in page.inner_text("#p5-home"), "accueil de la Part 5")
    page.click('[data-set="p5Size"][data-v="10"]')
    page.click('#p5-home [data-act="start"]')
    check(page.is_visible("#p5-run"), "la série commence")
    check(page.is_visible("#p5-text .gap"), "la phrase montre le trou")
    shot(page, "p5-question")
    q = page.evaluate("() => curQ('p5')")
    page.click('#p5-opts .opt[data-c="%d"]' % q["ans"])
    check(page.is_visible("#p5-fb") and "Bonne réponse" in page.inner_text("#p5-fb"), "bonne réponse : correction affichée")
    check(page.is_visible("#p5-text .fill.ok"), "le trou est rempli par la bonne réponse")
    shot(page, "p5-correction")
    page.click('#p5-fb [data-act="next"]')
    q2 = page.evaluate("() => curQ('p5')")
    wrong = (q2["ans"] + 1) % 4
    page.keyboard.press(str(wrong + 1))
    check("Raté" in page.inner_text("#p5-fb"), "mauvaise réponse au clavier : « Raté »")
    s = state(page)["q"][q2["id"]]
    check(s["e"] == 1 and s["d"] == today(page) + 1 and s["f"] == 0, "la question ratée entre au carnet d'erreurs (demain)", s)
    page.keyboard.press("Enter")
    check(page.evaluate("() => state.runs.p5.i") == 2, "Entrée passe à la suivante")
    # reload in the middle: the series is offered again, the answered question is not asked twice
    q3 = page.evaluate("() => curQ('p5')")
    page.click('#p5-opts .opt[data-c="%d"]' % q3["ans"])
    page.reload()
    wait_ready(page)
    check(page.evaluate("() => current") == "lecture", "rechargée sur Lecture")
    check("Série en cours" in page.inner_text("#p5-home"), "la série en cours est proposée")
    page.click('#p5-home [data-act="resume"]')
    check(page.is_visible("#p5-fb") and page.locator("#p5-opts .opt:disabled").count() == 4, "la question déjà répondue reste corrigée")
    check(len(state(page)["runs"]["p5"]["ans"]) == 3, "trois réponses gardées")
    page.click('#p5-fb [data-act="next"]')
    while page.evaluate("() => !!state.runs.p5"):
        q = page.evaluate("() => curQ('p5')")
        page.click('#p5-opts .opt[data-c="%d"]' % q["ans"])
        page.click('#p5-fb [data-act="next"]')
    done = nb(page.inner_text("#p5-done"))
    check("Série terminée" in done and "9 / 10" in done, "résultat : 9 / 10", done[:120])
    check(page.locator("#p5-done .errlist details").count() == 1, "une erreur à revoir")
    shot(page, "p5-resultat", full=True)
    page.click('#p5-done [data-act="home"]')
    check("Carnet d’erreurs" in page.inner_text("#p5-home"), "le carnet d'erreurs est annoncé")
    # the mistake due comes first in the next series
    page.evaluate("id => { state.q[id].d = dayNum(); save(); }", q2["id"])
    ids = page.evaluate("() => pickSeries('p5', 10, '')")
    check(q2["id"] in ids, "l'erreur due revient dans la série suivante")
    page.evaluate("id => { state.q[id].d = dayNum() + 1; save(); }", q2["id"])
    # exam mode
    page.click('[data-set="p5Mode"][data-v="exam"]')
    page.click('#p5-home [data-act="start"]')
    check(page.evaluate("() => state.runs.p5.left") == 10 * 20000, "examen : 20 s par question")
    check(":" in page.inner_text("#p5-clock"), "le chronomètre décompte", page.inner_text("#p5-clock"))
    for k in range(3):
        page.click('#p5-opts .opt[data-c="0"]')
        page.wait_for_function("k => state.runs.p5.i === k", arg=k + 1)
    check(page.is_hidden("#p5-fb"), "pas de correction pendant l'examen")
    page.evaluate("() => { state.runs.p5.left = 800; live.p5.resumedAt = Date.now(); }")
    page.wait_for_selector("#p5-done:not([hidden])", timeout=4000)
    done = nb(page.inner_text("#p5-done"))
    check("Temps écoulé" in done and "/ 10" in done, "temps écoulé : les questions restantes comptent fausses", done[:120])
    page.click('#p5-done [data-act="home"]')
    page.click('[data-set="p5Mode"][data-v="train"]')
    # one skill only
    page.click('#p5-home [data-tag="prep"]')
    page.click('#p5-home [data-act="start"]')
    tags = page.evaluate("() => state.runs.p5.ids.map(id => QBYID.get(id).tag)")
    check(tags and set(tags) == {"prep"}, "filtre par compétence", tags)
    page.click("#p5-stop")
    check("Série arrêtée" in page.inner_text("#p5-done") or "Aucune réponse" in page.inner_text("#p5-done"), "Arrêter montre le bilan")
    page.click('#p5-done [data-act="home"]')
    page.click('#p5-home [data-tag=""]')


def part2(page, errors):
    print("\n— Part 2")
    page.click('.tab[data-view="ecoute"]')
    check("Voix" in page.inner_text("#p2-home"), "les voix trouvées sont annoncées", page.inner_text("#p2-home"))
    page.click('[data-set="p2Size"][data-v="10"]')
    page.evaluate("() => { window.__said.length = 0; }")
    page.click('#p2-home [data-act="start"]')
    page.wait_for_function("() => window.__said.length >= 4 && !document.querySelector('#p2-replay').hidden", timeout=6000)
    said = page.evaluate("() => window.__said")
    q = page.evaluate("() => curQ('p2')")
    check(said[0]["text"] == q["text"] and said[1]["text"].startswith("A. ") and said[3]["text"].startswith("C. "),
          "la question puis les réponses A, B, C sont lues", [s["text"] for s in said[:4]])
    check(said[0]["voice"] != said[1]["voice"], "deux voix différentes", (said[0]["voice"], said[1]["voice"]))
    check(page.is_hidden("#p2-fb") and q["text"] not in page.inner_text("#p2-run"), "rien n'est écrit avant la réponse")
    shot(page, "p2-ecoute")
    page.click("#p2-replay")
    page.wait_for_function("() => window.__said.length >= 8", timeout=6000)
    check(True, "Réécouter relit la question et les réponses")
    page.click('#p2-opts .opt[data-c="%d"]' % ((q["ans"] + 1) % 3))
    check(page.is_visible("#p2-fb .tr-opts") and q["text"] in page.inner_text("#p2-fb"), "après la réponse : texte, correction et explication")
    check(page.locator("#p2-fb .tr-opts li.ok").count() == 1 and page.locator("#p2-fb .tr-opts li.ko").count() == 1, "bonne et mauvaise réponses marquées")
    shot(page, "p2-correction", full=True)
    check(state(page)["q"][q["id"]]["e"] == 1, "erreur notée au carnet")
    page.click("#p2-stop")
    page.click('#p2-done [data-act="home"]')
    # exam: no answer within 5 s counts wrong, then the next item
    page.click('[data-set="p2Mode"][data-v="exam"]')
    page.click('#p2-home [data-act="start"]')
    q = page.evaluate("() => curQ('p2')")
    page.wait_for_selector("#p2-window:not([hidden])", timeout=6000)
    check(page.is_hidden("#p2-replay"), "examen : pas de réécoute")
    page.wait_for_function("() => state.runs.p2 && state.runs.p2.i === 1", timeout=9000)
    s = state(page)["q"][q["id"]]
    check(s["l"] >= 1 and s["a"] == -1, "sans réponse en 5 s : compté faux, question suivante", s)
    page.click("#p2-stop")
    check("Pas de réponse" in page.inner_text("#p2-done") or "/ 1" in nb(page.inner_text("#p2-done")), "bilan de l'examen")
    page.click('#p2-done [data-act="home"]')
    page.click('[data-set="p2Mode"][data-v="train"]')


def reading_sets(page, errors):
    print("\n— Parts 6 et 7")
    page.click('.tab[data-view="lecture"]')
    page.click('#p5-home [data-part="p6"]')
    check(page.is_visible("#p6-home") and "Part 6" in page.inner_text("#p6-home"), "Lecture : on passe à la Part 6")
    page.click('#p6-home [data-act="start"]')
    check(page.locator("#p6-run .blank[data-b]").count() == 4, "texte à quatre trous")
    s = page.evaluate("() => curSet('p6')")
    for i, q in enumerate(s["qs"]):
        page.click('#p6-run .opt[data-qi="%d"][data-c="%d"]' % (i, q["ans"] if i else (q["ans"] + 1) % 4))
    first = s["qs"][0]
    check(first["opts"][(first["ans"] + 1) % 4] in page.inner_text('#p6-run .doc'), "le mot choisi s'écrit dans le trou")
    shot(page, "p6-texte", full=True)
    page.click('#p6-run [data-act="check"]')
    check(page.locator("#p6-run .sqfb:not([hidden])").count() == 4, "correction de chaque trou")
    check(page.locator("#p6-run .blank.ko").count() == 1 and page.locator("#p6-run .blank.ok").count() == 3, "trous corrigés dans le texte")
    st = state(page)["q"]
    check(st["6t-001-1"]["e"] == 1 and st["6t-001-2"]["f"] == 1, "chaque question du texte a sa fiche (carnet d'erreurs)")
    shot(page, "p6-correction", full=True)
    page.click('#p6-run [data-act="next"]')
    check("Série terminée" in page.inner_text("#p6-done") and "3 / 4" in nb(page.inner_text("#p6-done")), "bilan du texte : 3 / 4")
    page.click('#p6-done [data-act="home"]')

    page.click('#p6-home [data-part="p7"]')
    page.click('#p7-home [data-tag="multiple"]')
    page.click('#p7-home [data-act="start"]')
    check(page.locator("#p7-run .doc").count() == 2 and page.locator("#p7-run .tbl").count() == 1, "lot double avec un tableau")
    s = page.evaluate("() => curSet('p7')")
    for q in s["qs"]:
        page.keyboard.press(str(q["ans"] + 1))
    check(page.locator("#p7-run .opt.sel").count() == 5, "au clavier : une réponse par question, dans l'ordre")
    page.reload()
    wait_ready(page)
    check("Série en cours" in page.inner_text("#p7-home"), "Part 7 : série reprise après un rechargement")
    page.click('#p7-home [data-act="resume"]')
    check(page.locator("#p7-run .opt.sel").count() == 5, "les choix faits sont gardés")
    page.keyboard.press("Enter")
    check("Documents croisés" in page.inner_text("#p7-run") and page.locator("#p7-run .opt.ok").count() == 5, "Entrée valide : tout juste, types affichés")
    shot(page, "p7-correction", full=True)
    page.keyboard.press("Enter")
    check("5 / 5" in nb(page.inner_text("#p7-done")), "bilan 5 / 5")
    page.click('#p7-done [data-act="home"]')
    page.click('#p7-home [data-tag=""]')
    page.click('[data-set="p7Mode"][data-v="exam"]')
    page.click('#p7-home [data-act="start"]')
    nq = page.evaluate("() => state.runs.p7.ids.reduce((n, id) => n + SBYID.get(id).qs.length, 0)")
    check(page.evaluate("() => state.runs.p7.left") == nq * 60000, "Part 7 examen : une minute par question")
    page.click('#p7-run .opt[data-qi="0"][data-c="0"]')
    page.evaluate("() => { state.runs.p7.left = 600; live.p7.resumedAt = Date.now(); }")
    page.wait_for_selector("#p7-done:not([hidden])", timeout=4000)
    check("Temps écoulé" in page.inner_text("#p7-done"), "temps écoulé : le lot en cours compte avec ce qui est coché")
    page.click('#p7-done [data-act="home"]')
    page.click('[data-set="p7Mode"][data-v="train"]')
    page.click('#p7-home [data-part="p5"]')


def listening_sets(page, errors):
    print("\n— Parts 3 et 4")
    page.click('.tab[data-view="ecoute"]')
    page.click('#p2-home [data-part="p3"]')
    page.click('[data-set="p3Size"][data-v="3"]')
    page.evaluate("() => { window.__said.length = 0; }")
    page.click('#p3-home [data-act="start"]')
    s = page.evaluate("() => curSet('p3')")
    page.wait_for_function("n => window.__said.length >= n && !document.querySelector('#p3-replay').hidden", arg=len(s["lines"]), timeout=8000)
    said = page.evaluate("() => window.__said")
    check([x["text"] for x in said[:len(s["lines"])]] == [l[1] for l in s["lines"]], "toute la conversation est lue, réplique après réplique")
    sex = {"Samantha": "f", "Karen": "f", "Daniel": "m"}
    good = all(sex.get(said[i]["voice"]) == s["speakers"][l[0]] for i, l in enumerate(s["lines"]))
    check(good, "voix de femme pour la femme, voix d'homme pour l'homme", [(l[0], said[i]["voice"]) for i, l in enumerate(s["lines"])])
    if "M2" in s["speakers"]:
        m1 = next(said[i] for i, l in enumerate(s["lines"]) if l[0] == "M")
        m2 = next(said[i] for i, l in enumerate(s["lines"]) if l[0] == "M2")
        check(m1["pitch"] != m2["pitch"] or m1["voice"] != m2["voice"], "deux hommes : deux voix ou deux hauteurs")
    check(page.locator("#p3-run .sq").count() == 3 and s["lines"][0][1] not in page.inner_text("#p3-run"), "les questions sont écrites, la conversation non")
    for i, q in enumerate(s["qs"]):
        page.click('#p3-run .opt[data-qi="%d"][data-c="%d"]' % (i, q["ans"]))
    page.click('#p3-run [data-act="check"]')
    check(s["lines"][0][1] in page.inner_text("#p3-fb") and "Homme" in page.inner_text("#p3-fb"), "après la réponse : la transcription, avec qui parle")
    shot(page, "p3-correction", full=True)
    while page.evaluate("() => !!state.runs.p3"):
        if page.is_visible('#p3-run [data-act="next"]'):
            page.click('#p3-run [data-act="next"]')
            continue
        s = page.evaluate("() => curSet('p3')")
        if s["graphic"]:
            check(page.locator("#p3-run .tbl").count() == 1, "le graphique s'affiche avec les questions")
        page.wait_for_function("() => !document.querySelector('#p3-replay').hidden", timeout=8000)
        for i, q in enumerate(s["qs"]):
            page.click('#p3-run .opt[data-qi="%d"][data-c="%d"]' % (i, q["ans"]))
        page.click('#p3-run [data-act="check"]')
    check("6 / 6" in nb(page.inner_text("#p3-done")), "bilan de la Part 3")
    page.click('#p3-done [data-act="home"]')
    page.click('#p3-home [data-part="p4"]')
    page.click('#p4-home [data-act="start"]')
    page.wait_for_function("() => !document.querySelector('#p4-replay').hidden", timeout=8000)
    page.click('#p4-run [data-act="check"]')
    check("Pas de réponse" in page.inner_text("#p4-run") and "Femme" not in page.inner_text("#p4-fb"), "Part 4 : un seul locuteur, réponses manquantes comptées")
    page.click('#p4-run [data-act="next"]')
    page.click('#p4-done [data-act="home"]')
    page.click('#p4-home [data-part="p2"]')


def listening_exam(browser, url, errors):
    print("\n— Part 3, examen (horloge simulée)")
    ctx, page = new_page(browser, errors)
    page.clock.install()
    page.goto(url)
    page.wait_for_function("() => typeof BANK !== 'undefined' && BANK && current", timeout=15000)
    page.click('.tab[data-view="ecoute"]')
    page.click('#p2-home [data-part="p3"]')
    page.click('[data-set="p3Mode"][data-v="exam"]')
    page.click('#p3-home [data-act="start"]')
    check("Lis les questions" in page.inner_text("#p3-msg"), "examen : d'abord le temps de lire les questions")
    check(page.evaluate("() => window.__said.filter(s => s.text.trim()).length") == 0, "rien n'est lu pendant ce temps")
    page.clock.run_for(10000)
    page.clock.run_for(5000)
    check(page.is_visible("#p3-window") and page.is_hidden("#p3-replay"), "après une seule écoute : le temps de répondre, sans réécoute")
    page.click('#p3-run .opt[data-qi="0"][data-c="0"]')
    page.clock.run_for(30000)
    check(page.evaluate("() => state.runs.p3 ? state.runs.p3.i : -1") == 1, "le temps écoulé valide le lot et passe au suivant")
    check(page.locator("#p3-run .sqfb:not([hidden])").count() == 0, "pas de correction pendant l'examen")
    ctx.close()


def answer_current(page, kind):
    """Répond juste à la question ou au lot à l'écran (mode examen : passe ensuite tout seul)."""
    if kind in ("p5", "p2"):
        q = page.evaluate("k => curQ(k)", kind)
        page.click('#%s-opts .opt[data-c="%d"]' % (kind, q["ans"]))
    else:
        s = page.evaluate("k => curSet(k)", kind)
        for i, q in enumerate(s["qs"]):
            page.click('#%s-run .opt[data-qi="%d"][data-c="%d"]' % (kind, i, q["ans"]))
        page.click('#%s-run [data-act="check"]' % kind)


def mock_reading(page, errors):
    print("\n— examen blanc : lecture")
    page.click('.tab[data-view="examen"]')
    check("Examen blanc" in page.inner_text("#view-examen"), "onglet Examen")
    page.click('#view-examen [data-set="mockFormat"][data-v="read"]')
    check("75 minutes de lecture" in nb(page.inner_text("#view-examen")), "format Lecture : 75 minutes")
    page.click('#view-examen [data-act="mock-start"]')
    check(page.evaluate("() => current") == "lecture" and page.is_visible("#p5-run"), "l'examen commence par la Part 5")
    check("Examen blanc" in page.inner_text("#p5-pos") and page.inner_text("#p5-stop") == "Pause", "Part 5 en examen blanc, bouton Pause")
    check(page.evaluate("() => state.runs.p5.left") == 75 * 60000, "une seule horloge de 75 minutes pour la lecture")
    while page.evaluate("() => state.mock && state.mock.stages[state.mock.stage].kind === 'p5'"):
        i = page.evaluate("() => state.runs.p5 ? state.runs.p5.i : -1")
        answer_current(page, "p5")
        page.wait_for_function("i => !state.runs.p5 || state.runs.p5.i > i", arg=i)
    check(page.is_visible("#p6-run"), "puis la Part 6, sans bilan entre les deux")
    left = page.evaluate("() => state.runs.p6.left")
    check(0 < left < 75 * 60000, "le temps restant passe de la Part 5 à la Part 6", left)
    page.click('#p6-run [data-act="stop"]')
    check(page.evaluate("() => current") == "examen" and "Examen en cours" in page.inner_text("#view-examen"), "Pause : retour à l'onglet Examen")
    page.click('.tab[data-view="lecture"]')
    check("Examen blanc en cours" in page.inner_text("#p6-home"), "la partie en pause renvoie à l'examen")
    page.click('#p6-home [data-act="to-exam"]')
    page.click('#view-examen [data-act="mock-resume"]')
    check(page.is_visible("#p6-run"), "Reprendre : on revient au texte en cours")
    while page.evaluate("() => !!state.mock"):
        kind = page.evaluate("() => state.mock.stages[state.mock.stage].kind")
        n = page.evaluate("k => state.runs[k] ? state.runs[k].ans.length : -1", kind)
        answer_current(page, kind)
        page.wait_for_function("([k, n]) => !state.mock || !state.runs[k] || state.runs[k].ans.length > n", arg=[kind, n])
        page.wait_for_timeout(350)
    text = nb(page.inner_text("#view-examen"))
    check(page.evaluate("() => current") == "examen" and "495" in text and "C1" in text, "résultat : 495 en lecture, niveau C1", text[:160])
    m = page.evaluate("() => state.mocks[0]")
    check(m["R"]["ok"] == m["R"]["n"] and m["total"] is None and m["format"] == "read", "examen enregistré (lecture seule, pas de total)", m)
    shot(page, "examen-resultat")
    page.click('#view-examen [data-act="mock-close"]')
    check("Tes examens blancs" in page.inner_text("#view-examen"), "l'examen apparaît dans l'historique")
    # the clock runs out in Part 5: Parts 6 and 7 count as unanswered
    page.click('#view-examen [data-act="mock-start"]')
    answer_current(page, "p5")
    page.wait_for_function("() => state.runs.p5 && state.runs.p5.i === 1")
    page.evaluate("() => { state.runs.p5.left = 500; live.p5.resumedAt = Date.now(); }")
    page.wait_for_function("() => !state.mock", timeout=5000)
    m = page.evaluate("() => state.mocks[0]")
    total_q = page.evaluate("() => P5.length + QS.p6.length + QS.p7.length")
    check(m["R"]["n"] == total_q and m["R"]["ok"] == 1, "temps écoulé : tout ce qui reste compte faux", (m["R"], total_q))
    page.click('#view-examen [data-act="mock-close"]')


def mock_listening(browser, url, errors):
    print("\n— examen blanc : écoute (horloge simulée)")
    ctx, page = new_page(browser, errors)
    page.clock.install()
    page.goto(url)
    page.wait_for_function("() => typeof BANK !== 'undefined' && BANK && current", timeout=15000)
    page.click('.tab[data-view="examen"]')
    page.click('#view-examen [data-set="mockFormat"][data-v="listen"]')
    page.click('#view-examen [data-act="mock-start"]')
    check(page.evaluate("() => current") == "ecoute" and page.is_visible("#p2-run"), "l'examen d'écoute commence par la Part 2")
    for _ in range(12):
        if not page.evaluate("() => !!state.mock"):
            break
        page.clock.run_for(30000)
    check(not page.evaluate("() => !!state.mock"), "sans réponse, les Parts 2, 3 et 4 s'enchaînent jusqu'au bout")
    m = page.evaluate("() => state.mocks[0]")
    expected = page.evaluate("() => P2.length + QS.p3.length + QS.p4.length")
    check(m["L"]["n"] == expected and m["L"]["ok"] == 0 and m["L"]["score"] == 5, "score d'écoute : 5 pour aucune bonne réponse", m["L"])
    check(page.evaluate("() => current") == "examen" and "Écoute" in page.inner_text("#view-examen"), "résultats dans l'onglet Examen")
    ctx.close()


def scores_and_draw(page, errors):
    print("\n— score estimé et tirage")
    r = page.evaluate("""() => {
      const steps = Array.from({length: 101}, (_, i) => i / 100);
      const mono = t => steps.every((x, i) => !i || scaled(t, x) >= scaled(t, steps[i - 1]));
      return {l0: scaled(SCALE_L, 0), l1: scaled(SCALE_L, 1), r1: scaled(SCALE_R, 1), r9: scaled(SCALE_R, 0.9), l9: scaled(SCALE_L, 0.9),
        mono: mono(SCALE_L) && mono(SCALE_R), c1: cefr(CEFR_L, 490), b2: cefr(CEFR_L, 489), rc1: cefr(CEFR_R, 455)}; }""")
    check(r["l0"] == 5 and r["l1"] == 495 and r["r1"] == 495 and r["mono"], "échelle de 5 à 495, toujours croissante", r)
    check(r["r9"] < r["l9"], "la lecture est notée plus sévèrement que l'écoute", r)
    check(r["c1"] == "C1" and r["b2"] == "B2" and r["rc1"] == "C1", "niveaux CECRL d'ETS (C1 : 490 en écoute, 455 en lecture)", r)
    share = page.evaluate("""() => { let a = 0; for (let k = 0; k < 4000; k++) if (weightedShuffle(['a', 'b'], x => x === 'a' ? 3 : 1)[0] === 'a') a++; return a / 4000; }""")
    check(0.7 < share < 0.8, "tirage pondéré : un poids 3 passe devant un poids 1 trois fois sur quatre", share)
    w = page.evaluate("""() => { const save = JSON.stringify(state.q);
      for (const q of P5) state.q[q.id] = { r: 1, ok: q.tag === 'prep' ? 0 : 1, l: q.tag === 'prep' ? 1 : 0, f: q.tag === 'prep' ? 0 : 1, e: 0, t: dayNum() };
      const w = tagWeights('p5'); state.q = JSON.parse(save); return w; }""")
    check(w["prep"] > 1.3 and w["forme"] < 0.8, "une compétence ratée pèse plus qu'une compétence réussie", w)


def progress_settings(page, errors):
    print("\n— Progrès et Réglages")
    page.click('.tab[data-view="progres"]')
    text = nb(page.inner_text("#view-progres"))
    check("Vocabulaire" in text and "Part 5" in text and "Part 2" in text, "Progrès : les trois parties")
    check("Règle la date" in text, "invite à régler la date de l'examen")
    check(page.locator("#view-progres .brow").count() >= 3, "barres par compétence")
    shot(page, "progres", full=True)
    page.click('.tab[data-view="reglages"]')
    page.fill("#exam-date", "2028-01-15")
    page.dispatch_event("#exam-date", "change")
    page.click('.tab[data-view="progres"]')
    check("avant l’examen, le 15 janvier 2028" in nb(page.inner_text("#view-progres")), "compte à rebours de l'examen")
    page.click('.tab[data-view="reglages"]')
    page.click('[data-set="theme"][data-v="dark"]')
    check(page.evaluate("() => document.documentElement.dataset.theme") == "dark", "thème sombre")
    page.click('[data-set="textSize"][data-v="l"]')
    check(page.evaluate("() => document.documentElement.dataset.text") == "l", "texte agrandi")
    shot(page, "reglages-sombre", full=True)
    page.click('[data-set="theme"][data-v="auto"]')
    page.click('[data-set="textSize"][data-v="m"]')
    before = page.evaluate("() => ORDER.length")
    page.click('.switch[data-list="t2"]')
    check(page.evaluate("() => ORDER.length") == before - 4, "un thème désactivé quitte la file")
    page.click('.switch[data-list="t2"]')
    page.click('.switch[data-acc="gb"]')
    check("gb" not in state(page)["settings"]["accents"], "un accent se retire")
    page.click('.switch[data-acc="gb"]')
    check(page.locator('.switch[data-acc="ca"][disabled]').count() == 1, "accent sans voix sur l'appareil : grisé")


CHOSEN_VOICES = [
    ("Samantha", "en-US", "com.apple.voice.compact.en-US.Samantha"),
    ("Samantha", "en-US", "com.apple.voice.enhanced.en-US.Samantha"),
    ("Ava (Premium)", "en-US", "com.apple.voice.premium.en-US.Ava"),
    ("Evan (Enhanced)", "en-US", "com.apple.voice.enhanced.en-US.Evan"),
    ("Daniel", "en-GB", "com.apple.voice.compact.en-GB.Daniel"),
    ("Nora", "en-US", "com.apple.eloquence.en-US.Nora"),
    ("Google UK English Male", "en-GB", "Google UK English Male", False),
]


def voice_choice(browser, url, errors):
    print("\n— choix des voix")
    ctx, page = new_page(browser, errors, voices=CHOSEN_VOICES)
    page.goto(url)
    wait_ready(page)
    page.wait_for_function("() => speech.voices.length > 0")
    keys = page.evaluate("() => speech.voices.map(x => x.key)")
    check("com.apple.voice.enhanced.en-US.Samantha" in keys and "com.apple.voice.compact.en-US.Samantha" not in keys,
          "deux versions d'une voix : la version améliorée seulement", keys)
    check("com.apple.eloquence.en-US.Nora" not in keys, "voix Eloquence écartées")
    pool = lambda: page.evaluate("() => speech.pool().map(x => x.key)")
    check("com.apple.voice.compact.en-GB.Daniel" not in pool() and len(pool()) == 4, "assez de voix naturelles : la voix standard coupée d'office", pool())
    page.click('.tab[data-view="reglages"]')
    page.click("details.vlist summary")
    check(page.locator("details.vlist .switch[data-voice]").count() == 5, "Réglages : une ligne par voix")
    text = nb(page.inner_text("#view-reglages"))
    check("1 coupée" in text and "très naturelle" in text and "en ligne seulement" in text, "Réglages : voix coupées, qualité, voix en ligne")
    i = keys.index("com.apple.voice.compact.en-GB.Daniel")
    page.click('.switch[data-voice="%d"]' % i)
    check("com.apple.voice.compact.en-GB.Daniel" in pool() and state(page)["settings"]["voiceChoice"] == {"com.apple.voice.compact.en-GB.Daniel": True},
          "une voix standard remise")
    check(page.locator("details.vlist[open]").count() == 1, "la liste reste ouverte")
    a = keys.index("com.apple.voice.premium.en-US.Ava")
    page.click('.switch[data-voice="%d"]' % a)
    check("com.apple.voice.premium.en-US.Ava" not in pool(), "une voix coupée n'est plus tirée")
    n = page.evaluate("() => window.__said.length")
    page.click('[data-hear="%d"]' % a)
    page.wait_for_function("n => window.__said.length > n", arg=n)
    check(page.evaluate("() => window.__said.at(-1).uri") == "com.apple.voice.premium.en-US.Ava", "Écouter : la voix choisie, même coupée")
    page.click('.tab[data-view="mots"]')
    page.click('.tab[data-view="reglages"]')
    page.click('.switch[data-voice="%d"]' % a)
    check(state(page)["settings"]["voiceChoice"] == {"com.apple.voice.compact.en-GB.Daniel": True}, "un choix revenu à la valeur d'office est oublié")
    check("Google UK English Male" in pool(), "en ligne : la voix en ligne est tirée")
    ctx.set_offline(True)
    check("Google UK English Male" not in pool(), "hors ligne : la voix en ligne est écartée", (page.evaluate("navigator.onLine"), pool()))
    ctx.set_offline(False)
    page.reload()
    wait_ready(page)
    check(state(page)["settings"]["voiceChoice"] == {"com.apple.voice.compact.en-GB.Daniel": True}, "choix gardés au rechargement")
    page.click("details.vlist summary")
    shot(page, "reglages-voix", full=True)
    ctx.close()


def backup(page, errors):
    print("\n— sauvegarde")
    page.click('.tab[data-view="reglages"]')
    with page.expect_download() as dl:
        page.click("#backup-save")
    path = os.path.join(CAPTURES, "..", "sauvegarde.json")
    dl.value.save_as(path)
    data = json.load(open(path, encoding="utf-8"))
    check(data["app"] == "cap945" and data["state"]["words"], "sauvegarde exportée")
    words = len(data["state"]["words"])
    page.evaluate("() => { state.words = {}; save(); }")
    page.set_input_files("#backup-file", path)
    page.wait_for_selector("#imp-yes")
    page.click("#imp-yes")
    check(len(state(page)["words"]) == words, "sauvegarde réimportée")


def main():
    errors = []
    site = fresh_copy("site")
    httpd, url = serve(site)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx, page = new_page(browser, errors)
        page.goto(url)
        wait_ready(page)
        vocab(page, errors)
        part5(page, errors)
        part2(page, errors)
        reading_sets(page, errors)
        listening_sets(page, errors)
        mock_reading(page, errors)
        scores_and_draw(page, errors)
        progress_settings(page, errors)
        backup(page, errors)
        print("\n— hors ligne")
        page.evaluate("() => navigator.serviceWorker.ready")
        page.reload()
        wait_ready(page)
        page.wait_for_function("() => !!navigator.serviceWorker.controller", timeout=10000)
        ctx.set_offline(True)
        page.reload()
        wait_ready(page)
        check(page.evaluate("() => P5.length") == 12 and page.evaluate("() => WORDS.length") == 10, "hors ligne : l'appli et la banque se chargent")
        ctx.close()

        listening_exam(browser, url, errors)
        mock_listening(browser, url, errors)
        voice_choice(browser, url, errors)

        print("\n— sans voix")
        ctx, page = new_page(browser, errors, voices=[])
        page.goto(url)
        wait_ready(page)
        page.click('.tab[data-view="ecoute"]')
        page.wait_for_timeout(3300)
        check("Aucune voix anglaise" in page.inner_text("#p2-home"), "sans voix : message")
        page.click('[data-set="p2Mode"][data-v="exam"]')
        check(page.is_disabled('#p2-home [data-act="start"]'), "sans voix : pas de mode examen")
        page.click('[data-set="p2Mode"][data-v="train"]')
        page.click('#p2-home [data-act="start"]')
        check(page.is_visible("#p2-read") and page.evaluate("() => curQ('p2').text") in page.inner_text("#p2-read"), "sans voix : le texte à lire")
        ctx.close()

        print("\n— écrans")
        for scheme in ("light", "dark"):
            ctx, page = new_page(browser, errors, scheme=scheme, size=(1366, 768), mobile=False)
            page.goto(url)
            wait_ready(page)
            shot(page, "ordinateur-mots-" + scheme)
            page.click('.tab[data-view="lecture"]')
            page.click('#p5-home [data-act="start"]')
            shot(page, "ordinateur-p5-" + scheme)
            ctx.close()
        ctx, page = new_page(browser, errors, scheme="dark")
        page.goto(url)
        wait_ready(page)
        page.click("#v-turn")
        shot(page, "mots-verso-sombre")
        page.click('.tab[data-view="ecoute"]')
        page.click('#p2-home [data-act="start"]')
        page.wait_for_function("() => !document.querySelector('#p2-replay').hidden", timeout=6000)
        page.click('#p2-opts .opt[data-c="0"]')
        shot(page, "p2-correction-sombre", full=True)
        ctx.close()

        print("\n— vraie banque")
        real = fresh_copy("site-reel", real_bank=True)
        httpd2, url2 = serve(real)
        expected = {"mots": 0, "part2": 0, "part3": 0, "part4": 0, "part5": 0, "part6": 0, "part7": 0}
        config = json.load(open(os.path.join(real, "banque", "banque.json"), encoding="utf-8"))
        for entry in config["listes"]:
            path = os.path.join(real, "banque", entry["fichier"])
            if not os.path.exists(path):
                continue
            if entry["fichier"].endswith(".json"):   # sets: their questions
                expected[entry["type"]] += sum(len(s["questions"]) for s in json.load(open(path, encoding="utf-8-sig"))["sets"])
            else:
                lines = open(path, encoding="utf-8-sig").read().splitlines()[1:]
                expected[entry["type"]] += sum(1 for l in lines if l.strip() and not l.startswith("#"))
        ctx, page = new_page(browser, errors)
        page.goto(url2)
        wait_ready(page)
        got = page.evaluate("() => ({mots: WORDS.length, part2: P2.length, part3: QS.p3.length, part4: QS.p4.length, part5: P5.length, "
                            "part6: QS.p6.length, part7: QS.p7.length, missing: missingFiles})")
        check(got["missing"] == [], "tous les fichiers de la banque sont lus", got["missing"])
        check({k: got[k] for k in expected} == expected, "chaque ligne de la banque devient une carte ou une question", (got, expected))
        n = page.evaluate("""() => { const q = {}; for (const s of mockStages('full'))
          q[s.kind] = KINDS[s.kind].sets ? s.ids.reduce((n, id) => n + SBYID.get(id).qs.length, 0) : s.ids.length; return q; }""")
        listen, read = n.get("p2", 0) + n.get("p3", 0) + n.get("p4", 0), n.get("p5", 0) + n.get("p6", 0) + n.get("p7", 0)
        check(listen == 94 and 98 <= read <= 106, "examen complet sur la vraie banque : 94 questions d'écoute, environ 100 de lecture", n)
        page.click('.tab[data-view="lecture"]')
        page.click('#p5-home [data-part="p5"]') if page.is_visible('#p5-home [data-part="p5"]') else None
        page.click('#p5-home [data-act="start"]')
        check(page.is_visible("#p5-text .gap"), "une série de Part 5 démarre sur la vraie banque")
        shot(page, "vraie-banque-p5")
        ctx.close()
        httpd2.shutdown()
        browser.close()
    httpd.shutdown()
    finish(errors)


if __name__ == "__main__":
    main()
