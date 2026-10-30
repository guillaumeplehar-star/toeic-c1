#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contrôle de la banque de Cap 945 (banque/banque.json et ses fichiers TSV).

    py outils\\banque.py verifier      contrôle tout ; code 1 s'il y a une erreur
    py outils\\banque.py stats         répartition des réponses, compétences, niveaux et types par fichier
    py outils\\banque.py corriger      remplace les apostrophes droites par ’ et retire les espaces en trop

Format des fichiers : outils/consignes.md.
"""
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANQUE = os.path.join(ROOT, "banque")

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


def verify(show_stats=False):
    config = load_config()
    errors, warnings, seen_ids, seen_words = [], [], {}, {}
    total = Counter()
    ids = set()
    for entry in config.get("listes", []):
        for k in ("id", "type", "nom", "fichier"):
            if not entry.get(k):
                errors.append("banque.json : entrée sans « %s » : %s" % (k, entry))
        if entry.get("type") not in HEADERS:
            errors.append("banque.json : type inconnu %s" % entry.get("type"))
            continue
        if entry["id"] in ids:
            errors.append("banque.json : id %s en double" % entry["id"])
        ids.add(entry["id"])
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
        print(line)
    print("Total : %d mots, %d questions de Part 5, %d de Part 2." % (total["mots"], total["part5"], total["part2"]))
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


def main():
    utf8()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verifier"
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
