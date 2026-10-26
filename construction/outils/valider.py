"""Valide des fichiers d'extraction de notions.

Usage : python3 outils/valider.py [fichier.json ...]
Sans argument, valide tous les fichiers de extractions/ ensemble.
Les fichiers donnés sont validés ensemble (ids uniques, liens résolus sur l'ensemble).
"""
import re
import sys

from commun import FORCES, NATURES, NIVEAUX, charger, registre

REQUIRED = ["id", "nature", "matiere", "domaine", "sousDomaine", "classe", "cycle", "nom", "description",
            "objectifsOfficiels", "criteres", "question", "source"]
CHAMPS = set(REQUIRED) | {"programme", "periode", "acquisAnterieurs"}
CHAMPS_LIEN = {"de", "vers", "type", "force", "origine", "continuite", "raison"}

reg = registre()
notions, liens, par_fichier = charger(sys.argv[1:] or None)
errors = []

for f, d in par_fichier.items():
    if d.get("programme") not in reg:
        errors.append(f"{f}: « programme » absent ou inconnu du registre outils/programmes.json")
    # Dates de traçabilité, posées par outils/estampiller.py
    if not d.get("extraitLe" if "notions" in d else "relieLe"):
        errors.append(f"{f}: date absente (lance python3 outils/estampiller.py {f})")

ids = set()
for n in notions:
    nid = n.get("id", "?")
    prog = reg.get(n.get("programme"), {})
    for champ in REQUIRED:
        if champ not in n or n[champ] in ("", [], None):
            errors.append(f"{nid}: champ manquant ou vide « {champ} »")
    for champ in sorted(set(n) - CHAMPS):
        errors.append(f"{nid}: champ inconnu « {champ} »")
    if nid in ids:
        errors.append(f"{nid}: id en double")
    ids.add(nid)
    classe = n.get("classe")
    if classe not in NIVEAUX:
        errors.append(f"{nid}: classe inconnue {classe}")
        continue
    slug, cycle = NIVEAUX[classe][:2]
    if prog and classe not in prog["levels"]:
        errors.append(f"{nid}: classe {classe} absente du programme {n.get('programme')}")
    if prog and not re.match(rf"^fr-{prog['code']}-{re.escape(slug)}-[a-z]{{2,5}}-\d{{2,3}}$", nid):
        errors.append(f"{nid}: id mal formé (attendu fr-{prog.get('code')}-{slug}-<thème>-NN)")
    if prog and n.get("matiere") != prog["subject"]:
        errors.append(f"{nid}: matiere doit valoir « {prog['subject']} »")
    if n.get("cycle") != cycle:
        errors.append(f"{nid}: attendu cycle {cycle}")
    if n.get("nature") not in NATURES:
        errors.append(f"{nid}: nature invalide {n.get('nature')}")
    if len(n.get("nom", "")) > 80:
        errors.append(f"{nid}: nom trop long (> 80 caractères)")
    if not (1 <= len(n.get("criteres", [])) <= 6):
        errors.append(f"{nid}: 1 à 6 critères de réussite attendus")
    if "{{prenom}}" not in n.get("question", ""):
        errors.append(f"{nid}: question doit contenir {{{{prenom}}}}")
    src = n.get("source", {})
    if not isinstance(src, dict) or not {"fichier", "bo", "page"} <= set(src):
        errors.append(f"{nid}: source doit avoir fichier, bo, page")
    elif prog and src["fichier"] != prog["file"]:
        errors.append(f"{nid}: source.fichier doit valoir « {prog['file']} »")
    elif not re.fullmatch(r"[0-9a-f]{64}", src.get("sha256", "")):
        errors.append(f"{nid}: source.sha256 absent (lance outils/estampiller.py sur le fichier)")
    if not all(isinstance(k, str) for k in n.get("acquisAnterieurs", [])):
        errors.append(f"{nid}: acquisAnterieurs doit être une liste de textes")

graph, vus = {}, set()
for l in liens:
    a, b = l.get("vers"), l.get("de")
    tag = f"{b} -> {a}"
    for champ in sorted(set(l) - CHAMPS_LIEN):
        errors.append(f"lien {tag}: champ inconnu « {champ} »")
    if (a, b) in vus:
        errors.append(f"lien {tag}: en double")
    vus.add((a, b))
    if a not in ids:
        errors.append(f"lien {tag}: « vers » inconnu")
    if b not in ids:
        errors.append(f"lien {tag}: « de » inconnu")
    if a == b:
        errors.append(f"lien {tag}: une notion ne peut pas être son propre prérequis")
    if l.get("type") != "prerequis":
        errors.append(f"lien {tag}: type doit valoir « prerequis »")
    if l.get("force") not in FORCES:
        errors.append(f"lien {tag}: force doit valoir « indispensable » ou « utile »")
    if l.get("origine") not in {"texte", "déduit"}:
        errors.append(f"lien {tag}: origine doit valoir « texte » ou « déduit »")
    if "continuite" in l and not isinstance(l["continuite"], bool):
        errors.append(f"lien {tag}: continuite doit valoir true ou false")
    if not l.get("raison"):
        errors.append(f"lien {tag}: raison manquante")
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
par_classe = {}
for n in notions:
    par_classe[n["classe"]] = par_classe.get(n["classe"], 0) + 1
print(f"OK : {len(notions)} notions {par_classe}, {len(liens)} liens, graphe acyclique")
