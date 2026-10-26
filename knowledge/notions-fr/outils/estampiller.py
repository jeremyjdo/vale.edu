"""Estampille des fichiers d'extraction ou de liens avec la version des sources dont ils viennent.

Usage : python3 outils/estampiller.py extractions/<fichier>.json [...] [--date AAAA-MM-JJ]

- Fichier de notions : chaque notion reçoit l'empreinte SHA-256 du PDF cité (`source.sha256`, et
  `source.examplesSha256` pour un document d'exemples), lue dans programmes-officiels/sources.json.
  La racine reçoit `extractedAt` (date du jour, ou --date) si elle n'en a pas.
- Fichier de liens : la racine reçoit `linkedAt` s'il n'en a pas, et `versionsCibles`, la date
  d'extraction de chaque programme touché par ses liens. outils/etat.py s'en sert pour signaler
  une liaison à refaire quand l'un de ces programmes est ré-extrait.

À lancer juste après avoir écrit un fichier, avant valider.py. Une empreinte déjà présente n'est
jamais remplacée : une notion garde la version du PDF dont elle a été extraite.
"""
import json
import os
import sys
from datetime import date

from commun import RACINE, charger

MANIFESTE = json.load(open(os.path.join(os.path.dirname(RACINE), "programmes-officiels", "sources.json")))["sources"]

args = sys.argv[1:]
jour = date.today().isoformat()
if "--date" in args:
    i = args.index("--date")
    jour = args[i + 1]
    del args[i:i + 2]

notions, _, par_fichier = charger()
programme_de = {n["id"]: n["programme"] for n in notions}
# Date d'extraction de chaque programme : la plus récente de ses fichiers.
extraction = {}
for d in par_fichier.values():
    if "notions" in d and d.get("extractedAt"):
        p = d["programme"]
        extraction[p] = max(extraction.get(p, ""), d["extractedAt"])

for f in args:
    d = json.load(open(f))
    if "notions" in d:
        manquants = 0
        for n in d["notions"]:
            src = n["source"]
            for cle, champ in (("file", "sha256"), ("examples", "examplesSha256")):
                if src.get(cle) and champ not in src:
                    if src[cle] in MANIFESTE:
                        src[champ] = MANIFESTE[src[cle]]["sha256"]
                    else:
                        manquants += 1
        d.setdefault("extractedAt", jour)
        extraction[d["programme"]] = max(extraction.get(d["programme"], ""), d["extractedAt"])
        print(f"{f} : {len(d['notions'])} notions estampillées, extraites le {d['extractedAt']}"
              + (f", {manquants} PDF absent(s) du manifeste" if manquants else ""))
    else:
        d.setdefault("linkedAt", jour)
        touches = {programme_de.get(p[k]) for p in d.get("prerequisites", []) for k in ("topicId", "prerequisiteId")}
        d["versionsCibles"] = {p: extraction.get(p) for p in sorted(t for t in touches if t)}
        print(f"{f} : liens du {d['linkedAt']}, {len(d['versionsCibles'])} programme(s) touché(s)")
    json.dump(d, open(f, "w"), ensure_ascii=False, indent=2)
