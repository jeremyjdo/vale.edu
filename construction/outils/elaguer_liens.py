"""Retire d'un fichier de liens entre classes ceux qui se déduisent déjà d'une autre chaîne de prérequis.

Usage : python3 outils/elaguer_liens.py extractions/liens-<programme>.json
Règles :
- un lien écrit dans le programme (origine « texte ») n'est jamais retiré ;
- les liens utiles sont examinés d'abord, puis les liens indispensables d'appui, puis les liens indispensables
  de prolongement (« continuite »: true, même savoir-faire l'année d'avant) ;
- un lien indispensable n'est redondant que s'il existe une autre chaîne composée uniquement de liens indispensables.
"""
import json
import sys

from commun import charger

cible = sys.argv[1]
_, tous, par_fichier = charger()
liens = json.load(open(cible))

graph = {}
for l in tous:
    graph.setdefault(l["vers"], {})[l["de"]] = l["force"]


def atteignable(src, dst, ignore, fort_seulement):
    vus, pile = set(), [src]
    while pile:
        u = pile.pop()
        for v, force in graph.get(u, {}).items():
            if (u, v) == ignore or v in vus or (fort_seulement and force != "indispensable"):
                continue
            if v == dst:
                return True
            vus.add(v)
            pile.append(v)
    return False


ordre = sorted(liens["liens"],
               key=lambda c: (c["force"] == "indispensable", bool(c.get("continuite"))))
retires = set()
for c in ordre:
    arete = (c["vers"], c["de"])
    if c["origine"] == "texte":
        continue
    if atteignable(arete[0], arete[1], arete, fort_seulement=c["force"] == "indispensable"):
        retires.add(arete)
        del graph[arete[0]][arete[1]]

avant = len(liens["liens"])
liens["liens"] = [c for c in liens["liens"] if (c["vers"], c["de"]) not in retires]
json.dump(liens, open(cible, "w"), ensure_ascii=False, indent=2)
print(f"{avant} liens, {len(retires)} redondants retirés, {len(liens['liens'])} gardés")
