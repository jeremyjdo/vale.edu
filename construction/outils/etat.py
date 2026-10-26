"""État de la base : ce qui est à jour, et ce qu'il reste à faire après l'ajout ou la mise à jour d'un programme.

Usage :
  python3 outils/etat.py                  # bilan de toute la base et liste des actions à faire
  python3 outils/etat.py --programme <clé> # impact d'une ré-extraction de ce programme

Contrôles : PDF absents du manifeste ou modifiés, textes manquants, programmes du registre sans
extraction, notions tirées d'une ancienne version de leur PDF, liaisons à refaire (un programme
touché a été ré-extrait depuis), liaison manquante avec le programme précédent (`follows`), liens
cassés, assemblage ou atlas à refaire. La procédure complète est dans outils/MISE-A-JOUR.md.
"""
import glob
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict

from commun import DONNEES, EXTRACTIONS, PROGRAMMES, RACINE, SITE, charger, registre

MANIFESTE = json.load(open(os.path.join(PROGRAMMES, "sources.json")))["sources"]
reg = registre()
notions, liens, par_fichier = charger()
by_id = {n["id"]: n for n in notions}
prog_de = {n["id"]: n["programme"] for n in notions}
fichiers_de = defaultdict(list)
extraction = {}
for f, d in par_fichier.items():
    if "notions" in d:
        fichiers_de[d["programme"]].append(os.path.basename(f))
        extraction[d["programme"]] = max(extraction.get(d["programme"], ""), d.get("extraitLe", ""))
# Fichier d'origine de chaque lien
origine = []
for f, d in par_fichier.items():
    origine += [(os.path.basename(f), l) for l in d.get("liens", [])]


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


if "--programme" in sys.argv:
    cle = sys.argv[sys.argv.index("--programme") + 1]
    if cle not in reg:
        sys.exit(f"{cle} : absent du registre outils/programmes.json")
    info = reg[cle]
    ids = {n["id"] for n in notions if n["programme"] == cle}
    print(f"# Impact d'une ré-extraction de {cle} ({info['subject']}, {', '.join(info['levels'])})\n")
    print(f"PDF : programmes-officiels/{info['file']} ({info['bo']})")
    print(f"Extraction : {', '.join(fichiers_de[cle]) or 'aucune'}, {len(ids)} notions, le {extraction.get(cle)}")
    entrants = Counter((f, prog_de.get(l["vers"])) for f, l in origine
                       if l["de"] in ids and l["vers"] not in ids)
    sortants = Counter((f, prog_de.get(l["de"])) for f, l in origine
                       if l["vers"] in ids and l["de"] not in ids)
    print("\nLiens d'autres programmes vers celui-ci (à refaire si les id changent) :")
    for (f, p), c in sorted(entrants.items()) or [(("—", "—"), 0)]:
        print(f"  - {f} : {c} lien(s) depuis {p}")
    print("Liens de celui-ci vers d'autres programmes (à refaire après la ré-extraction) :")
    for (f, p), c in sorted(sortants.items()) or [(("—", "—"), 0)]:
        print(f"  - {f} : {c} lien(s) vers {p}")
    noms = {by_id[i]["nom"] for i in ids}
    cites = Counter(n["programme"] for n in notions if n["programme"] != cle
                    for acquis in n.get("acquisAnterieurs", []) if any(nom in acquis for nom in noms))
    if cites:
        print("acquisAnterieurs qui citent ses notions : " + ", ".join(f"{p} ({c})" for p, c in cites.most_common()))
    suivants = [k for k, v in reg.items() if v.get("follows") == cle]
    print(f"Programmes qui lui font suite (follows) : {', '.join(suivants) or 'aucun'}")
    print(f"Programme précédent : {info.get('follows') or 'aucun'}")
    remplaces = [k for k, v in reg.items() if cle in v.get("remplace", [])]
    if info.get("remplace") or remplaces:
        print(f"Remplace : {', '.join(info.get('remplace', [])) or '—'} ; remplacé par : {', '.join(remplaces) or '—'}")
    print("\nÉtapes : voir outils/MISE-A-JOUR.md, « Nouvelle version d'un programme déjà extrait ».")
    sys.exit()

actions = []
print("# État de la base de notions\n")

# 1. PDF et manifeste
sur_disque = {os.path.relpath(p, PROGRAMMES) for p in glob.glob(os.path.join(PROGRAMMES, "**", "*.pdf"), recursive=True)
              if os.sep + "archives" + os.sep not in p}
nouveaux = sorted(sur_disque - set(MANIFESTE))
manquants = sorted(set(MANIFESTE) - sur_disque)
modifies = sorted(r for r in set(MANIFESTE) & sur_disque if sha(os.path.join(PROGRAMMES, r)) != MANIFESTE[r]["sha256"])
sans_texte = sorted(r for r in MANIFESTE if not os.path.exists(
    os.path.join(RACINE, "textes", os.path.splitext(os.path.basename(r))[0] + ".txt")))
print(f"PDF : {len(MANIFESTE)} dans le manifeste, {len(nouveaux)} nouveau(x), {len(modifies)} modifié(s), "
      f"{len(manquants)} manquant(s), {len(sans_texte)} sans texte")
actions += [f"Enregistrer le nouveau PDF : python3 outils/preparer_pdf.py {r} --url <adresse> --bo \"<BO>\"" for r in nouveaux]
actions += [f"PDF modifié hors procédure, remets l'ancien puis : python3 outils/preparer_pdf.py {r} --depuis <nouveau.pdf>"
            for r in modifies]
actions += [f"PDF manquant : {r} (retrouve-le à l'adresse du manifeste)" for r in manquants]
actions += [f"Générer le texte : python3 outils/preparer_pdf.py {r}" for r in sans_texte if r not in nouveaux]

# 2. Registre et extractions
sans_manifeste = sorted(k for k, v in reg.items() if v["file"] not in MANIFESTE)
a_extraire = [k for k in reg if k not in extraction and k not in sans_manifeste]
perimes = Counter(n["programme"] for n in notions
                  if n["source"].get("fichier") in MANIFESTE and n["source"].get("sha256") != MANIFESTE[n["source"]["fichier"]]["sha256"])
print(f"Programmes : {len(reg)} au registre, {len(extraction)} extraits, {len(a_extraire)} à extraire, "
      f"{len(perimes)} tiré(s) d'une ancienne version de leur PDF")
actions += [f"Programme {k} : son PDF {reg[k]['file']} n'est pas dans le manifeste (preparer_pdf.py)" for k in sans_manifeste]
actions += [f"Extraire {k} ({reg[k]['subject']}, {', '.join(reg[k]['levels'])}) : voir outils/MISE-A-JOUR.md" for k in a_extraire]
actions += [f"Ré-extraire {k} : {c} notion(s) viennent d'une ancienne version du PDF "
            f"(impact : python3 outils/etat.py --programme {k})" for k, c in perimes.items()]

# 3. Liaisons
a_relier = []
for f, d in par_fichier.items():
    if "notions" in d:
        continue
    cibles = d.get("versionsCibles")
    if cibles is None:
        a_relier.append((os.path.basename(f), "pas de versionsCibles (lance estampiller.py)"))
        continue
    for p, quand in cibles.items():
        if extraction.get(p) and (quand or "") < extraction[p]:
            a_relier.append((os.path.basename(f), f"{p} ré-extrait le {extraction[p]}"))
casses = [(f, l) for f, l in origine if l["vers"] not in by_id or l["de"] not in by_id]
sans_suite = []
for k, v in reg.items():
    precedent = v.get("follows")
    if k in extraction and precedent in extraction and not any(
            prog_de.get(l["vers"]) == k and prog_de.get(l["de"]) == precedent for l in liens):
        sans_suite.append((k, precedent))
print(f"Liaisons : {len(a_relier)} fichier(s) de liens à refaire, {len(casses)} lien(s) cassé(s), "
      f"{len(sans_suite)} programme(s) sans lien avec le précédent")
actions += [f"Refaire la liaison {f} ({raison}) : voir outils/consignes-liens.md" for f, raison in a_relier]
for f, n in Counter(f for f, _ in casses).items():
    actions.append(f"{f} : {n} lien(s) vers des notions qui n'existent plus, à refaire")
actions += [f"Relier {k} à {p} (programme précédent) : voir outils/consignes-liens.md" for k, p in sans_suite]

# 4. Assemblage
data = os.path.join(DONNEES, "notions.json")
recents = [f for f in glob.glob(os.path.join(EXTRACTIONS, "*.json")) + [os.path.join(RACINE, "outils", "programmes.json"),
           os.path.join(PROGRAMMES, "sources.json")]
           if not os.path.exists(data) or os.path.getmtime(f) > os.path.getmtime(data)]
print(f"Assemblage : {'à refaire' if recents else 'à jour'}")
if recents:
    actions.append("Assembler : python3 outils/valider.py && python3 outils/assembler.py")
site = os.path.join(SITE, "index.html")
sources_site = [data, os.path.join(SITE, "modele.html"), os.path.join(RACINE, "outils", "construire_site.py")]
if not recents and (not os.path.exists(site) or any(
        os.path.exists(f) and os.path.getmtime(f) > os.path.getmtime(site) for f in sources_site)):
    print("Atlas : à reconstruire")
    actions.append("Reconstruire l'atlas : python3 outils/construire_site.py")

print()
if actions:
    print("## Actions à faire\n")
    for i, a in enumerate(actions, 1):
        print(f"{i}. {a}")
    print("\nPuis : python3 outils/verifier_sources.py")
else:
    print("Tout est à jour. Pour détecter une nouvelle version publiée : python3 outils/verifier_sources.py --en-ligne")
