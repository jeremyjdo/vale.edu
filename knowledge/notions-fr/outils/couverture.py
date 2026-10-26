"""Vérifie que chaque puce « Objectifs d'apprentissage » d'un programme est reprise dans une notion.

Usage : python3 outils/couverture.py textes/<programme>.txt extractions/<fichier>.json [...] [--pages 36-52]
(--pages : ne compte que les puces qui commencent sur ces pages du PDF.)
Approximatif : quand la mise en page colle les deux colonnes, une puce peut être signalée à tort.
"""
import json
import re
import sys
import unicodedata


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s)


args = sys.argv[1:]
pages = None
if "--pages" in args:
    i = args.index("--pages")
    a, _, b = args[i + 1].partition("-")
    pages = range(int(a), int(b or a) + 1)
    del args[i:i + 2]

lines = open(args[0]).read().split("\n")
bullets, current, in_table, page, retrait, blanc = [], None, False, 0, 0, False
for line in lines:
    blanc_avant, blanc = blanc, not line.strip()
    if line.startswith("=== PAGE "):
        # Un saut de page ne termine pas le tableau en cours.
        page = int(line.split()[2])
        continue
    if "Objectifs" in line and "Exemples de r" in line:
        in_table, current = True, None
        continue
    if not in_table:
        continue
    left = re.split(r"\s{3,}", line.strip())[0] if line.strip() else ""
    indent = len(line) - len(line.lstrip())
    if line.lstrip().startswith("- ") and indent <= 4:
        if current:
            bullets.append(current)
        current, retrait = (left[2:].strip(), page), indent
    elif current is not None and left and retrait < indent <= retrait + 3 and not blanc_avant:
        current = (current[0] + " " + left, current[1])
    elif not line.strip() or indent > retrait + 3:
        continue
    else:
        if current:
            bullets.append(current)
        current, in_table = None, False
if current:
    bullets.append(current)
bullets = [b for b, p in bullets if pages is None or p in pages]

blob = "|".join(norm(o) for f in args[1:] for n in json.load(open(f)).get("notions", [])
                for o in n.get("officialObjectives", []))
missing = [b for b in bullets if norm(b)[:40] not in blob]
print(f"{len(bullets)} puces détectées, {len(bullets) - len(missing)} retrouvées dans les notions")
for b in missing:
    print("  ? non retrouvée :", b[:150])
