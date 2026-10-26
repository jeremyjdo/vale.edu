"""Retire d'un fichier de liens entre classes ceux qui se déduisent déjà d'une autre chaîne de prérequis.

Usage : python3 outils/elaguer_liens.py extractions/liens-<programme>.json
Règles :
- un lien écrit dans le programme (origin « texte ») n'est jamais retiré ;
- les liens faibles sont examinés d'abord, puis les liens forts d'appui, puis les liens forts de prolongement
  (« continuation »: true, même savoir-faire l'année d'avant) ;
- un lien fort n'est redondant que s'il existe une autre chaîne composée uniquement de liens forts.
"""
import json
import sys

from commun import charger

cible = sys.argv[1]
_, prereqs, par_fichier = charger()
liens = json.load(open(cible))

graph = {}
for p in prereqs:
    graph.setdefault(p["topicId"], {})[p["prerequisiteId"]] = p["strength"]


def atteignable(src, dst, ignore, fort_seulement):
    vus, pile = set(), [src]
    while pile:
        u = pile.pop()
        for v, force in graph.get(u, {}).items():
            if (u, v) == ignore or v in vus or (fort_seulement and force != "hard"):
                continue
            if v == dst:
                return True
            vus.add(v)
            pile.append(v)
    return False


ordre = sorted(liens["prerequisites"],
               key=lambda c: (c["strength"] == "hard", bool(c.get("continuation"))))
retires = set()
for c in ordre:
    arete = (c["topicId"], c["prerequisiteId"])
    if c["origin"] == "texte":
        continue
    if atteignable(arete[0], arete[1], arete, fort_seulement=c["strength"] == "hard"):
        retires.add(arete)
        del graph[arete[0]][arete[1]]

avant = len(liens["prerequisites"])
liens["prerequisites"] = [c for c in liens["prerequisites"]
                          if (c["topicId"], c["prerequisiteId"]) not in retires]
json.dump(liens, open(cible, "w"), ensure_ascii=False, indent=2)
print(f"{avant} liens, {len(retires)} redondants retirés, {len(liens['prerequisites'])} gardés")
