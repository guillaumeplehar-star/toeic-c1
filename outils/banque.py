#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôle de la banque de Cap 945 (banque/banque.json et ses fichiers TSV).

    py outils\\banque.py verifier      contrôle tout ; code 1 s'il y a une erreur (TSV : mots, Parts 2 et 5 ; JSON : Parts 3, 4, 6, 7)
    py outils\\banque.py stats         répartition des réponses, compétences, niveaux et types par fichier
    py outils\\banque.py corriger      remplace les apostrophes droites par ’ et retire les espaces en trop
    py outils\\banque.py doublons      questions trop proches (même bonne réponse et phrase semblable, ou phrase presque identique)

Format des fichiers : outils/consignes.md.
"""
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANQUE = os.environ.get("CAP945_BANQUE") or os.path.join(ROOT, "banque")   # autre dossier : les tests

HEADERS = {
    "mots": ["anglais", "nature", "francais", "exemple", "traduction", "note"],
    "part5": ["id", "phrase", "a", "b", "c", "d", "reponse", "competence", "niveau", "explication", "traduction"],
    "part2": ["id", "question", "a", "b", "c", "reponse", "type", "explication", "tq", "ta", "tb", "tc"],
}
REQUIRED = {
    "mots": ["anglais", "nature", "francais", "exemple", "traduction"],
    "part5": HEADERS["part5"],
    "part2": HEADERS["part2"],
}
NATURES = {"nom", "verbe", "adjectif", "adverbe", "verbe à particule", "expression", "préposition", "conjonction"}
COMPETENCES = {"forme", "verbe", "vocab", "lien", "prep", "pronom", "compar"}
NIVEAUX = {"B2", "C1"}
TYPES = {"wh", "oui-non", "choix", "neg-tag", "demande", "affirm"}
FRENCH = {"mots": ["francais", "traduction", "note"], "part5": ["explication", "traduction"],
          "part2": ["explication", "tq", "ta", "tb", "tc"]}


def utf8():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def load_config():
    with open(os.path.join(BANQUE, "banque.json"), encoding="utf-8") as fh:
        return json.load(fh)


def read_rows(path):
    """Lignes du fichier : (numéro de ligne, cellules), en-tête à part."""
    with open(path, encoding="utf-8-sig", newline="") as fh:
        lines = fh.read().split("\n")
    lines = [l[:-1] if l.endswith("\r") else l for l in lines]
    head = lines[0].split("\t") if lines else []
    rows = [(n, l.split("\t")) for n, l in enumerate(lines[1:], start=2) if l.strip() and not l.startswith("#")]
    return head, rows


def words(s):
    return len(re.findall(r"[A-Za-z’']+(?:-[A-Za-z]+)*|\d[\d,.:]*", s))


def longest(opts, ans):
    """La bonne réponse est-elle strictement la plus longue ? (indice que le candidat apprendrait à suivre)"""
    return all(len(opts[ans]) > len(o) for i, o in enumerate(opts) if i != ans)


def long_line(st):
    n = st.get("nlong", 0)
    if not n:
        return ""
    share = 100 * st["long"] / n
    chance = 100 / st.get("nopts", 4)
    return "  | plus longue %d %%%s" % (share, " (TROP : hasard %d %%)" % chance if share > chance + 12 else "")


def check_file(entry, errors, warnings, seen_ids, seen_words):
    kind, name = entry["type"], entry["fichier"]
    path = os.path.join(BANQUE, name)
    if not os.path.exists(path):
        errors.append("%s : fichier absent" % name)
        return None
    head, rows = read_rows(path)
    want = HEADERS[kind]
    if [h.strip().lower() for h in head] != want:
        errors.append("%s : en-tête %s au lieu de %s" % (name, "\t".join(head), "\t".join(want)))
        return None
    stats = {"n": 0, "rep": Counter(), "tag": Counter(), "lvl": Counter()}
    local_words = {}
    prefix = None
    if kind != "mots":
        m = re.match(r"part[52]-([a-z]+)\.tsv$", name)
        prefix = (kind[-1] + m.group(1) + "-") if m else None

    def err(n, msg):
        errors.append("%s:%d : %s" % (name, n, msg))

    def warn(n, msg):
        warnings.append("%s:%d : %s" % (name, n, msg))

    for n, cells in rows:
        if len(cells) != len(want):
            err(n, "%d colonnes au lieu de %d" % (len(cells), len(want)))
            continue
        r = {h: c for h, c in zip(want, cells)}
        stats["n"] += 1
        for h in REQUIRED[kind]:
            if not r[h].strip():
                err(n, "colonne « %s » vide" % h)
        for h, c in r.items():
            if c != c.strip() or "  " in c:
                err(n, "espaces en trop dans « %s »" % h)
            if "'" in c:
                err(n, "apostrophe droite dans « %s » (py outils\\banque.py corriger)" % h)
            if '"' in c:
                err(n, "guillemet droit dans « %s »" % h)
        for h in FRENCH[kind]:
            if r[h].count("*") % 2:
                err(n, "astérisques sans paire dans « %s »" % h)
        if kind == "mots":
            if r["nature"] not in NATURES:
                err(n, "nature inconnue : %s" % r["nature"])
            ex = r["exemple"]
            if not re.search(r"\{[^{}]+\}", ex) or ex.count("{") != ex.count("}"):
                err(n, "exemple sans le mot entre accolades, ou accolades mal fermées")
            if "{" in r["traduction"] or "}" in r["traduction"]:
                err(n, "accolades dans la traduction")
            key = r["anglais"].lower()
            if key in local_words:
                err(n, "« %s » déjà à la ligne %d" % (r["anglais"], local_words[key]))
            else:
                local_words[key] = n
                if key in seen_words and seen_words[key][0] != name:
                    warn(n, "« %s » aussi dans %s:%d" % (r["anglais"], *seen_words[key]))
                seen_words.setdefault(key, (name, n))
            if not 6 <= words(ex) <= 26:
                warn(n, "exemple de %d mots" % words(ex))
        else:
            qid = r["id"]
            if qid in seen_ids:
                err(n, "id %s déjà utilisé (%s)" % (qid, seen_ids[qid]))
            seen_ids[qid] = "%s:%d" % (name, n)
            if prefix and not re.fullmatch(re.escape(prefix) + r"\d{3}", qid):
                err(n, "id %s : attendu %s000" % (qid, prefix))
            letters = "ABCD" if kind == "part5" else "ABC"
            if r["reponse"] not in letters or len(r["reponse"]) != 1:
                err(n, "réponse %s : attendu %s" % (r["reponse"], "/".join(letters)))
            stats["rep"][r["reponse"]] += 1
            opts = [r[x] for x in letters.lower()]
            if len({o.lower() for o in opts}) != len(opts):
                err(n, "deux propositions identiques")
            if r["reponse"] in letters:
                stats["nlong"] = stats.get("nlong", 0) + 1
                stats["long"] = stats.get("long", 0) + longest(opts, letters.index(r["reponse"]))
                stats["nopts"] = len(letters)
            if kind == "part5":
                if r["phrase"].count("-------") != 1 or "--------" in r["phrase"]:
                    err(n, "la phrase doit contenir un seul trou -------")
                if r["competence"] not in COMPETENCES:
                    err(n, "compétence inconnue : %s" % r["competence"])
                if r["niveau"] not in NIVEAUX:
                    err(n, "niveau inconnu : %s" % r["niveau"])
                stats["tag"][r["competence"]] += 1
                stats["lvl"][r["niveau"]] += 1
                if not 10 <= words(r["phrase"]) <= 40:
                    warn(n, "phrase de %d mots" % words(r["phrase"]))
            else:
                if r["type"] not in TYPES:
                    err(n, "type inconnu : %s" % r["type"])
                stats["tag"][r["type"]] += 1
                if not 3 <= words(r["question"]) <= 18:
                    warn(n, "question de %d mots" % words(r["question"]))
                for x in "abc":
                    if not 1 <= words(r[x]) <= 18:
                        warn(n, "réponse %s de %d mots" % (x.upper(), words(r[x])))
    return stats


SET_TYPES = {
    "part3": {"sujet", "detail", "inference", "action", "intention", "graphique"},
    "part4": {"sujet", "detail", "inference", "action", "intention", "graphique"},
    "part6": COMPETENCES | {"phrase"},
    "part7": {"idee", "detail", "inference", "vocab", "vrai-faux", "insertion", "intention", "croise"},
}
SPEAKERS = {"W": "f", "M": "m", "W2": "f", "M2": "m"}
MARKS = ["[1]", "[2]", "[3]", "[4]"]


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, list):
        for x in o:
            yield from strings(x)
    elif isinstance(o, dict):
        for x in o.values():
            yield from strings(x)


def check_table(t, err, what):
    if t is None:
        return
    rows = t.get("rows") if isinstance(t, dict) else None
    if not isinstance(rows, list) or len(rows) < 2 or not all(isinstance(r, list) and r for r in rows):
        err("%s : il faut {\"title\", \"rows\"} avec au moins deux lignes" % what)
    elif len({len(r) for r in rows}) != 1:
        err("%s : lignes de longueurs différentes" % what)


def check_sets(entry, errors, warnings, seen_ids):
    """Parts 3, 4, 6, 7 : un fichier JSON de lots ; voir outils/consignes.md."""
    kind, name = entry["type"], entry["fichier"]
    path = os.path.join(BANQUE, name)
    if not os.path.exists(path):
        errors.append("%s : fichier absent" % name)
        return None
    try:
        with open(path, encoding="utf-8-sig") as fh:
            data = json.load(fh)
    except Exception as e:
        errors.append("%s : JSON illisible (%s)" % (name, e))
        return None
    sets = data.get("sets") if isinstance(data, dict) else None
    if not isinstance(sets, list):
        errors.append("%s : il faut un objet {\"sets\": [ … ]}" % name)
        return None
    m = re.match(r"part([3467])-([a-z]+)\.json$", name)
    prefix = (m.group(1) + m.group(2) + "-") if m else None
    stats = {"n": 0, "q": 0, "rep": Counter(), "tag": Counter(), "lvl": Counter()}
    for k, s in enumerate(sets, 1):
        sid = s.get("id", "") if isinstance(s, dict) else ""
        where = "%s %s" % (name, sid or "lot %d" % k)

        def err(msg):
            errors.append("%s : %s" % (where, msg))

        def warn(msg):
            warnings.append("%s : %s" % (where, msg))

        if not isinstance(s, dict):
            err("pas un objet")
            continue
        if sid in seen_ids:
            err("id déjà utilisé (%s)" % seen_ids[sid])
        seen_ids[sid] = name
        if prefix and not re.fullmatch(re.escape(prefix) + r"\d{3}", sid):
            err("id attendu %s000" % prefix)
        texts = list(strings(s))
        if any("'" in t for t in texts):
            err("apostrophe droite (py outils\\banque.py corriger)")
        if any('"' in t for t in texts):
            err("guillemet droit dans un texte")
        qs = s.get("questions")
        if not isinstance(qs, list) or not qs:
            err("pas de questions")
            continue
        graphic_q = sum(1 for q in qs if isinstance(q, dict) and q.get("type") == "graphique")
        if kind in ("part3", "part4"):
            sp = s.get("speakers")
            if not isinstance(sp, dict) or any(SPEAKERS.get(key) != v for key, v in sp.items()):
                err("speakers : clés W, M, W2, M2 avec f ou m")
                sp = {}
            want = (2, 3) if kind == "part3" else (1, 1)
            if not want[0] <= len(sp) <= want[1]:
                err("%d locuteur(s) au lieu de %s" % (len(sp), "2 ou 3" if kind == "part3" else "1"))
            lines = s.get("lines")
            if not isinstance(lines, list) or not lines or not all(isinstance(l, list) and len(l) == 2 and l[0] in sp and l[1].strip() for l in lines):
                err("lines : liste de [locuteur, réplique] avec des locuteurs de speakers")
                lines = []
            if set(l[0] for l in lines) != set(sp):
                warn("un locuteur ne parle pas")
            fr = s.get("lines_fr")
            if not isinstance(fr, list) or len(fr) != len(lines) or not all(isinstance(x, str) and x.strip() for x in fr):
                err("lines_fr : une traduction par réplique")
            n = sum(words(l[1]) for l in lines)
            lo, hi = (80, 170) if kind == "part3" else (100, 190)
            if not lo <= n <= hi:
                warn("%d mots" % n)
            if len(qs) != 3:
                err("%d questions au lieu de 3" % len(qs))
            check_table(s.get("graphic"), err, "graphic")
            if bool(s.get("graphic")) != bool(graphic_q):
                err("un graphic va avec une question de type graphique, et inversement")
        elif kind == "part6":
            text = s.get("text", "")
            pos = [text.find(mk) for mk in MARKS]
            if any(text.count(mk) != 1 for mk in MARKS) or pos != sorted(pos):
                err("le texte doit contenir [1], [2], [3], [4] une fois chacun, dans l'ordre")
            if not str(s.get("text_fr", "")).strip():
                err("text_fr vide")
            if len(qs) != 4:
                err("%d questions au lieu de 4" % len(qs))
            if sum(1 for q in qs if isinstance(q, dict) and q.get("type") == "phrase") != 1:
                err("il faut une question de type phrase, une seule")
            if not 70 <= words(text) <= 190:
                warn("texte de %d mots" % words(text))
        else:
            docs = s.get("docs")
            if not isinstance(docs, list) or not 1 <= len(docs) <= 3 or not all(isinstance(d, dict) and str(d.get("text", "")).strip() for d in docs):
                err("docs : 1 à 3 documents avec un text")
                docs = []
            for d in docs:
                check_table(d.get("table"), err, "table")
            fr = s.get("docs_fr")
            if not isinstance(fr, list) or len(fr) != len(docs) or not all(isinstance(x, str) and x.strip() for x in fr):
                err("docs_fr : une traduction par document")
            if len(docs) == 1 and not 2 <= len(qs) <= 4:
                warn("lot simple avec %d questions" % len(qs))
            if len(docs) > 1 and len(qs) != 5:
                warn("lot de %d documents avec %d questions" % (len(docs), len(qs)))
            types = [q.get("type") for q in qs if isinstance(q, dict)]
            if "croise" in types and len(docs) < 2:
                err("question croise dans un lot d'un seul document")
            if len(docs) > 1 and "croise" not in types:
                warn("pas de question croise")
            if "insertion" in types:
                if not any(all(str(d.get("text", "")).count(mk) == 1 for mk in MARKS) for d in docs):
                    err("question insertion sans les marques [1] à [4] dans un document")
            stats["lvl"]["%d doc." % len(docs)] += 1
        for i, q in enumerate(qs, 1):
            if not isinstance(q, dict):
                err("question %d : pas un objet" % i)
                continue
            opts = q.get("opts")
            if not isinstance(opts, list) or len(opts) != 4 or not all(isinstance(o, str) and o.strip() for o in opts):
                err("question %d : il faut quatre propositions" % i)
            elif len({o.lower() for o in opts}) != 4:
                err("question %d : deux propositions identiques" % i)
            if q.get("ans") not in ("A", "B", "C", "D"):
                err("question %d : ans %s" % (i, q.get("ans")))
            if q.get("type") not in SET_TYPES[kind]:
                err("question %d : type inconnu %s" % (i, q.get("type")))
            if q.get("type") == "insertion" and opts != MARKS:
                err("question %d : insertion, opts = [1] à [4]" % i)
            need = ["expl"] if kind == "part6" else ["q", "expl", "q_fr"]
            for f in need:
                if not str(q.get(f, "")).strip():
                    err("question %d : %s vide" % (i, f))
            for f in ("expl", "q_fr"):
                if str(q.get(f, "")).count("*") % 2:
                    err("question %d : astérisques sans paire dans %s" % (i, f))
            stats["rep"][q.get("ans")] += 1
            stats["tag"][q.get("type")] += 1
            if isinstance(opts, list) and len(opts) == 4 and q.get("ans") in ("A", "B", "C", "D") and q.get("type") != "insertion":
                stats["nlong"] = stats.get("nlong", 0) + 1
                stats["long"] = stats.get("long", 0) + longest(opts, "ABCD".index(q["ans"]))
        stats["n"] += 1
        stats["q"] += len(qs)
    return stats


def verify(show_stats=False):
    config = load_config()
    errors, warnings, seen_ids, seen_words = [], [], {}, {}
    total = Counter()
    ids = set()
    for entry in config.get("listes", []):
        for k in ("id", "type", "nom", "fichier"):
            if not entry.get(k):
                errors.append("banque.json : entrée sans « %s » : %s" % (k, entry))
        if entry.get("type") not in HEADERS and entry.get("type") not in SET_TYPES:
            errors.append("banque.json : type inconnu %s" % entry.get("type"))
            continue
        if entry["id"] in ids:
            errors.append("banque.json : id %s en double" % entry["id"])
        ids.add(entry["id"])
        if entry["type"] in SET_TYPES:
            st = check_sets(entry, errors, warnings, seen_ids)
            if st is None:
                continue
            total[entry["type"]] += st["q"]
            line = "%-22s %4d lots, %d questions" % (entry["fichier"], st["n"], st["q"])
            if show_stats:
                line += "  réponses " + " ".join("%s %d" % kv for kv in sorted(st["rep"].items()))
                line += "  | " + ", ".join("%s %d" % kv for kv in st["tag"].most_common())
                if st["lvl"]:
                    line += "  | " + ", ".join("%s %d" % kv for kv in sorted(st["lvl"].items()))
                line += long_line(st)
            print(line)
            continue
        st = check_file(entry, errors, warnings, seen_ids, seen_words)
        if st is None:
            continue
        total[entry["type"]] += st["n"]
        line = "%-22s %4d" % (entry["fichier"], st["n"])
        if show_stats and entry["type"] != "mots":
            line += "  réponses " + " ".join("%s %d" % kv for kv in sorted(st["rep"].items()))
            line += "  | " + ", ".join("%s %d" % kv for kv in st["tag"].most_common())
            if st["lvl"]:
                line += "  | " + ", ".join("%s %d" % kv for kv in sorted(st["lvl"].items()))
            line += long_line(st)
        print(line)
    print("Total : %d mots ; questions : Part 2 %d, Part 3 %d, Part 4 %d, Part 5 %d, Part 6 %d, Part 7 %d." % (
        total["mots"], total["part2"], total["part3"], total["part4"], total["part5"], total["part6"], total["part7"]))
    for w in warnings[:60]:
        print("  attention  " + w)
    if len(warnings) > 60:
        print("  … et %d autres avertissements" % (len(warnings) - 60))
    for e in errors[:200]:
        print("  ERREUR     " + e)
    if len(errors) > 200:
        print("  … et %d autres erreurs" % (len(errors) - 200))
    print("%d erreur(s), %d avertissement(s)." % (len(errors), len(warnings)))
    return 1 if errors else 0


def fix():
    config = load_config()
    changed = 0
    for entry in config.get("listes", []):
        path = os.path.join(BANQUE, entry.get("fichier", ""))
        if not os.path.exists(path):
            continue
        if entry.get("type") in SET_TYPES:            # JSON : the apostrophes inside the texts
            with open(path, encoding="utf-8-sig") as fh:
                raw = fh.read()
            data = json.loads(raw)

            def tidy(o):
                if isinstance(o, str):
                    return re.sub(r" {2,}", " ", o.strip()).replace("'", "’")
                if isinstance(o, list):
                    return [tidy(x) for x in o]
                if isinstance(o, dict):
                    return {k: tidy(v) for k, v in o.items()}
                return o
            new = json.dumps(tidy(data), ensure_ascii=False, indent=2) + "\n"
            if new != raw:
                changed += 1
                with open(path, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(new)
                print("corrigé : " + entry["fichier"])
            continue
        with open(path, encoding="utf-8-sig", newline="") as fh:
            text = fh.read()
        crlf = "\r\n" in text
        lines = text.replace("\r\n", "\n").split("\n")
        out = []
        for i, line in enumerate(lines):
            if i == 0 or not line.strip():
                out.append(line)
                continue
            cells = [re.sub(r" {2,}", " ", c.strip()).replace("'", "’") for c in line.split("\t")]
            out.append("\t".join(cells))
        new = "\n".join(out)
        if crlf:
            new = new.replace("\n", "\r\n")
        if new != text:
            changed += 1
            with open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(new)
            print("corrigé : " + entry["fichier"])
    print("%d fichier(s) modifié(s)." % changed)


STOP = set("the a an of to in on for and or is are was were be been by with at from that this it as our your their all any will would "
           "has have had not no please its his her they we you he she which who".split())


def content_words(s):
    return {w for w in re.findall(r"[a-z’']+", s.lower().replace("-------", " ")) if w not in STOP and len(w) > 2}


def doubles():
    """Paires de questions trop proches, dans une même série ou entre deux séries."""
    config = load_config()
    items = []
    for entry in config.get("listes", []):
        if entry.get("type") not in ("part5", "part2"):
            continue
        path = os.path.join(BANQUE, entry["fichier"])
        if not os.path.exists(path):
            continue
        head, rows = read_rows(path)
        want = HEADERS[entry["type"]]
        for _, cells in rows:
            if len(cells) != len(want):
                continue
            r = dict(zip(want, cells))
            letters = "abcd" if entry["type"] == "part5" else "abc"
            right = r[letters["ABCD".index(r["reponse"])]] if r["reponse"] in "ABCD"[:len(letters)] else ""
            text = r["phrase"] if entry["type"] == "part5" else r["question"]
            items.append((entry["type"], r["id"], right.lower().strip(), content_words(text), text))
    found = 0
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i], items[j]
            if a[0] != b[0] or not a[3] or not b[3]:
                continue
            sim = len(a[3] & b[3]) / len(a[3] | b[3])
            if sim >= 0.5 or (a[2] == b[2] and sim >= 0.25):
                found += 1
                print("%s ~ %s  (%.0f %%%s)\n    %s\n    %s" % (a[1], b[1], 100 * sim, ", même réponse : " + a[2] if a[2] == b[2] else "", a[4], b[4]))
    print("%d paire(s) trop proche(s)." % found)


def main():
    utf8()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verifier"
    if cmd == "doublons":
        doubles()
        return
    if cmd == "verifier":
        sys.exit(verify())
    if cmd == "stats":
        sys.exit(verify(show_stats=True))
    if cmd == "corriger":
        fix()
        return
    sys.exit(__doc__)


if __name__ == "__main__":
    main()
