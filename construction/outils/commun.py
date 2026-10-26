"""Constantes et chargement partagés par les outils de construction de la base."""
import glob
import hashlib
import json
import os
import sys

# construction/ : PDF officiels, textes, extractions et outils
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACTIONS = os.path.join(RACINE, "extractions")
PROGRAMMES = os.path.join(RACINE, "programmes-officiels")
# À la racine du dépôt : le jeu de données publié (data/) et l'atlas (site/)
DEPOT = os.path.dirname(RACINE)
DONNEES = os.path.join(DEPOT, "data")
SITE = os.path.join(DEPOT, "site")

# Classe -> (slug utilisé dans les id, cycle, âge début, âge fin)
NIVEAUX = {
    "PS": ("ps", 1, 3, 4), "MS": ("ms", 1, 4, 5), "GS": ("gs", 1, 5, 6),
    "CP": ("cp", 2, 6, 7), "CE1": ("ce1", 2, 7, 8), "CE2": ("ce2", 2, 8, 9),
    "CM1": ("cm1", 3, 9, 10), "CM2": ("cm2", 3, 10, 11),
    # Programmes qui traitent CM1 et CM2 en un seul bloc « cours moyen » (ex. EPS 2026)
    "CM1-CM2": ("cm", 3, 9, 11),
    "6e": ("6e", 3, 11, 12),
    "5e": ("5e", 4, 12, 13), "4e": ("4e", 4, 13, 14), "3e": ("3e", 4, 14, 15),
    "Cycle 1": ("c1", 1, 3, 6), "Cycle 2": ("c2", 2, 6, 9),
    "Cycle 3": ("c3", 3, 9, 12), "Cycle 4": ("c4", 4, 12, 15),
}
ORDRE_NIVEAUX = list(NIVEAUX)
# Nature d'une notion : comprendre une idée, savoir-faire, passer d'une représentation à une autre,
# vocabulaire de la matière, stratégie sur sa propre démarche
NATURES = ["compréhension", "savoir-faire", "représentation", "vocabulaire", "stratégie"]
FORCES = {"indispensable", "utile"}
# Version du format des données publiées dans data/
VERSION = "0.4"


def id_objectif(code, classe, programme, texte):
    """Identifiant stable d'un objectif officiel : il ne change que si son texte change."""
    empreinte = hashlib.sha1(f"{programme}|{classe}|{texte}".encode()).hexdigest()[:8]
    return f"fr-{code}-{NIVEAUX[classe][0]}-objectif-{empreinte}"


def registre():
    return json.load(open(os.path.join(RACINE, "outils", "programmes.json")))


def charger(fichiers=None):
    """Charge les fichiers d'extraction (par défaut : tous). Renvoie (notions, liens, par_fichier)."""
    fichiers = fichiers or sorted(glob.glob(os.path.join(EXTRACTIONS, "*.json")))
    notions, liens, par_fichier = [], [], {}
    for f in fichiers:
        try:
            d = json.load(open(f))
        except json.JSONDecodeError:
            # Fichier en cours d'écriture par une autre extraction : on l'ignore.
            print(f"(ignoré, JSON illisible : {os.path.basename(f)})", file=sys.stderr)
            continue
        par_fichier[f] = d
        for n in d.get("notions", []):
            n.setdefault("programme", d.get("programme"))
            notions.append(n)
        liens += d.get("liens", [])
    return notions, liens, par_fichier
