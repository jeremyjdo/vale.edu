"""Valide des fichiers d'extraction de notions.

Usage : python3 outils/valider.py [fichier.json ...]
Sans argument, valide tous les fichiers de extractions/ ensemble.
Les fichiers donnés sont validés ensemble (ids uniques, prérequis résolus sur l'ensemble).
"""
import re
import sys

from commun import NIVEAUX, TYPES, charger, registre

REQUIRED = ["id", "type", "subject", "domain", "subdomain", "level", "cycle",
            "ageRangeStart", "ageRangeEnd", "name", "description",
            "officialObjectives", "evidence", "assessmentPrompt", "source"]

reg = registre()
notions, prereqs, par_fichier = charger(sys.argv[1:] or None)
errors = []

for f, d in par_fichier.items():
    if d.get("programme") not in reg:
        errors.append(f"{f}: « programme » absent ou inconnu du registre outils/programmes.json")
    # Dates de traçabilité, posées par outils/estampiller.py
    if not d.get("extractedAt" if "notions" in d else "linkedAt"):
        errors.append(f"{f}: date absente (lance python3 outils/estampiller.py {f})")

ids = set()
for n in notions:
    nid = n.get("id", "?")
    prog = reg.get(n.get("programme"), {})
    for champ in REQUIRED:
        if champ not in n or n[champ] in ("", [], None):
            errors.append(f"{nid}: champ manquant ou vide « {champ} »")
    if nid in ids:
        errors.append(f"{nid}: id en double")
    ids.add(nid)
    lvl = n.get("level")
    if lvl not in NIVEAUX:
        errors.append(f"{nid}: niveau inconnu {lvl}")
        continue
    slug, cycle, a0, a1 = NIVEAUX[lvl]
    if prog and lvl not in prog["levels"]:
        errors.append(f"{nid}: niveau {lvl} absent du programme {n.get('programme')}")
    if prog and not re.match(rf"^fr-{prog['code']}-{re.escape(slug)}-[a-z]{{2,5}}-\d{{2,3}}$", nid):
        errors.append(f"{nid}: id mal formé (attendu fr-{prog.get('code')}-{slug}-<thème>-NN)")
    if prog and n.get("subject") != prog["subject"]:
        errors.append(f"{nid}: subject doit valoir « {prog['subject']} »")
    if (n.get("cycle"), n.get("ageRangeStart"), n.get("ageRangeEnd")) != (cycle, a0, a1):
        errors.append(f"{nid}: attendu cycle {cycle}, âges {a0}-{a1}")
    if n.get("type") not in TYPES:
        errors.append(f"{nid}: type invalide {n.get('type')}")
    if len(n.get("name", "")) > 80:
        errors.append(f"{nid}: nom trop long (> 80 caractères)")
    if not (1 <= len(n.get("evidence", [])) <= 6):
        errors.append(f"{nid}: 1 à 6 critères de réussite attendus")
    if "{{prenom}}" not in n.get("assessmentPrompt", ""):
        errors.append(f"{nid}: assessmentPrompt doit contenir {{{{prenom}}}}")
    src = n.get("source", {})
    if not isinstance(src, dict) or not {"file", "bo", "page"} <= set(src):
        errors.append(f"{nid}: source doit avoir file, bo, page")
    elif prog and src["file"] != prog["file"]:
        errors.append(f"{nid}: source.file doit valoir « {prog['file']} »")
    elif not re.fullmatch(r"[0-9a-f]{64}", src.get("sha256", "")):
        errors.append(f"{nid}: source.sha256 absent (lance outils/estampiller.py sur le fichier)")
    if not all(isinstance(k, str) for k in n.get("priorKnowledge", [])):
        errors.append(f"{nid}: priorKnowledge doit être une liste de textes")

graph, vus = {}, set()
for p in prereqs:
    a, b = p.get("topicId"), p.get("prerequisiteId")
    tag = f"{a} <- {b}"
    if (a, b) in vus:
        errors.append(f"prérequis {tag}: en double")
    vus.add((a, b))
    if a not in ids:
        errors.append(f"prérequis {tag}: topicId inconnu")
    if b not in ids:
        errors.append(f"prérequis {tag}: prerequisiteId inconnu")
    if a == b:
        errors.append(f"prérequis {tag}: une notion ne peut pas être son propre prérequis")
    if p.get("strength") not in {"hard", "soft"}:
        errors.append(f"prérequis {tag}: strength doit être hard ou soft")
    if p.get("origin") not in {"texte", "déduit"}:
        errors.append(f"prérequis {tag}: origin doit être « texte » ou « déduit »")
    if not p.get("reason"):
        errors.append(f"prérequis {tag}: reason manquante")
    graph.setdefault(a, []).append(b)

etat = {}
def visiter(u, pile):
    etat[u] = 1
    for v in graph.get(u, []):
        if etat.get(v) == 1:
            errors.append("cycle de prérequis : " + " -> ".join(pile + [u, v]))
        elif etat.get(v) is None:
            visiter(v, pile + [u])
    etat[u] = 2
sys.setrecursionlimit(10000)
for u in list(graph):
    if etat.get(u) is None:
        visiter(u, [])

if errors:
    print(f"{len(errors)} erreur(s) :")
    for e in errors[:200]:
        print(" -", e)
    sys.exit(1)
par_niveau = {}
for n in notions:
    par_niveau[n["level"]] = par_niveau.get(n["level"], 0) + 1
print(f"OK : {len(notions)} notions {par_niveau}, {len(prereqs)} prérequis, graphe acyclique")
