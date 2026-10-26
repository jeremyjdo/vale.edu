"""Construit l'atlas, la page de consultation de la base : site/index.html, à la racine du dépôt.

Usage :
  python3 outils/construire_site.py                     # site/index.html, page autonome qui s'ouvre sans serveur
  python3 outils/construire_site.py --artefact <fichier> [--lien <adresse>]
                                                       # même page sans en-tête HTML, pour une publication en ligne ;
                                                       # --lien donne l'adresse publique, pour le bouton « Copier le lien »

La page reprend le jeu de données data/ (programmes, objectifs, notions et liens), compressé et intégré à la page : elle se met à jour
à chaque assemblage (assembler.py l'appelle). Le modèle de la page est site/modele.html.
Une matière absente de FAMILLES forme sa propre bande sur la carte : ajoute-la à la bonne famille.
"""
import base64
import gzip
import json
import os
import sys
from collections import defaultdict

from commun import DONNEES, NATURES, NIVEAUX, ORDRE_NIVEAUX, PROGRAMMES, SITE, registre

MODELE = os.path.join(SITE, "modele.html")
SORTIE = os.path.join(SITE, "index.html")

# Bandes de la carte, de haut en bas. `choix` : matières parallèles dont la carte n'affiche qu'une à la fois.
FAMILLES = [
    {"court": "Français", "nom": "Français", "matieres": ["Langage oral et écrit", "Français"]},
    {"court": "Mathématiques", "nom": "Mathématiques", "matieres": ["Premiers outils mathématiques", "Mathématiques"]},
    {"court": "Sciences", "nom": "Sciences et technologie", "matieres": [
        "Découvrir le monde du vivant, de la matière et des objets", "Questionner le monde", "Sciences et technologie",
        "Sciences de la vie et de la Terre", "Physique-chimie", "Technologie"]},
    {"court": "Histoire-géo", "nom": "Histoire-géographie", "matieres": [
        "Se repérer dans le temps et l'espace", "Histoire-géographie"]},
    {"court": "Langues vivantes", "nom": "Langues vivantes", "matieres": [
        "Langues vivantes", "Anglais", "Espagnol", "Allemand", "Italien"],
     "choix": ["Anglais", "Espagnol", "Allemand", "Italien"]},
    {"court": "Moral et civique", "nom": "Enseignement moral et civique", "matieres": ["Enseignement moral et civique"]},
    {"court": "Vie affective", "nom": "Vie affective et relationnelle", "matieres": [
        "Éducation à la vie affective et relationnelle",
        "Éducation à la vie affective et relationnelle, et à la sexualité"]},
    {"court": "Arts", "nom": "Arts", "matieres": [
        "Activités artistiques", "Arts plastiques", "Éducation musicale", "Histoire des arts"]},
    {"court": "EPS", "nom": "Éducation physique et sportive", "matieres": [
        "Activités physiques", "Éducation physique et sportive"]},
    {"court": "Médias", "nom": "Éducation aux médias et à l'information", "matieres": [
        "Éducation aux médias et à l'information"]},
]
NOMS_CYCLES = {1: "maternelle", 2: "apprentissages fondamentaux", 3: "consolidation", 4: "approfondissements"}
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre",
        "novembre", "décembre"]


def apostrophes(s):
    return s.replace("’", "'")


def nombre(n):
    return f"{n:,}".replace(",", " ")


def notion_par_defaut(notions, liens):
    """Notion ouverte au premier affichage : une notion de maths dont la chaîne de prérequis
    remonte sur le plus de classes, sans être trop longue."""
    avant = defaultdict(list)
    for l in liens:
        avant[l["vers"]].append(l["de"])
    niveau = {n["id"]: n["classe"] for n in notions}

    def ancetres(i):
        vus, pile = set(), [i]
        while pile:
            for p in avant[pile.pop()]:
                if p not in vus:
                    vus.add(p)
                    pile.append(p)
        return vus

    candidats = []
    for i, n in enumerate(notions):
        if n["matiere"] == "Mathématiques" and n["classe"] in ("CE2", "CM1", "CM2", "6e"):
            a = ancetres(n["id"])
            if 12 <= len(a) <= 70:
                candidats.append((len({niveau[x] for x in a}), -len(a), -i))
    return -max(candidats)[2] if candidats else 0


def donnees():
    lire = lambda nom: json.load(open(os.path.join(DONNEES, f"{nom}.json")))
    base = lire("notions")
    liens = lire("liens")["liens"]
    textes_objectifs = {o["id"]: o["texte"] for o in lire("objectifs")["objectifs"]}
    manifeste = json.load(open(os.path.join(PROGRAMMES, "sources.json")))["sources"]
    reg = registre()
    notions = base["notions"]

    familles = [dict(f) for f in FAMILLES]
    famille_de = {apostrophes(m): i for i, f in enumerate(familles) for m in f["matieres"]}
    for n in notions:
        if apostrophes(n["matiere"]) not in famille_de:
            famille_de[apostrophes(n["matiere"])] = len(familles)
            familles.append({"court": n["matiere"], "nom": n["matiere"], "matieres": [n["matiere"]]})

    remplace_par = defaultdict(list)
    for k, v in reg.items():
        for ancien in v.get("remplace", []):
            remplace_par[ancien].append(k)
    programmes = {}
    for k, v in lire("programmes")["programmes"].items():
        programmes[k] = {
            "m": v["matiere"], "fam": famille_de[apostrophes(v["matiere"])], "niv": v["classes"], "bo": v["bo"],
            "pdf": v["fichier"], "url": v.get("url") or "", "ex": v.get("extraitLe") or "",
            "remplace": reg.get(k, {}).get("remplace", []), "remplacePar": remplace_par.get(k, []),
        }

    colonnes = [n for n in ORDRE_NIVEAUX if not n.startswith("Cycle") and "-" not in n]
    col = {n: i for i, n in enumerate(colonnes)}
    cols_du_cycle = defaultdict(list)
    for n in colonnes:
        cols_du_cycle[NIVEAUX[n][1]].append(col[n])
    etendues = {}
    for n in ORDRE_NIVEAUX:
        if n in col:
            etendues[n] = [col[n], col[n]]
        elif n.startswith("Cycle"):
            c = cols_du_cycle[NIVEAUX[n][1]]
            etendues[n] = [min(c), max(c)]
        else:
            debut, fin = n.split("-")
            etendues[n] = [col[debut], col[fin]]

    textes, index_texte = [], {}

    def t(s):
        if s not in index_texte:
            index_texte[s] = len(textes)
            textes.append(s)
        return index_texte[s]

    position = {n["id"]: i for i, n in enumerate(notions)}
    lignes = []
    for n in notions:
        src = n["source"]
        lignes.append([
            n["id"], n["programme"], NATURES.index(n["nature"]), t(n["domaine"]), t(n.get("sousDomaine") or ""),
            n["classe"], n["nom"], n["description"], [textes_objectifs[o] for o in n["objectifs"]], n["criteres"],
            n["question"], t(n["periode"]) if n.get("periode") else -1, src.get("page", 0),
            src.get("exemples", ""), src.get("exemplesPage", 0),
        ])
    exemples = {n["source"]["exemples"] for n in notions if n["source"].get("exemples")}
    return {
        "genere": base["genereLe"],
        "colonnes": colonnes,
        "cycles": [{"nom": f"Cycle {k}", "sous": NOMS_CYCLES.get(k, ""), "de": min(v), "a": max(v)}
                   for k, v in sorted(cols_du_cycle.items())],
        "ages": {n: f"{v[2]}-{v[3]} ans" for n, v in NIVEAUX.items()},
        "etendues": etendues,
        "types": [[k, k] for k in NATURES],
        "familles": familles,
        "programmes": programmes,
        "urls": {f: manifeste[f]["url"] for f in exemples if f in manifeste},
        "textes": textes,
        "n": lignes,
        "l": [[position[l["vers"]], position[l["de"]], int(l["force"] == "indispensable"),
               int(l["origine"] == "texte"), int(bool(l.get("continuite"))), l.get("raison", "")]
              for l in liens if l["vers"] in position and l["de"] in position],
        "defaut": notion_par_defaut(notions, liens),
    }


def construire(artefact=None, lien=""):
    """Écrit la page et renvoie son chemin."""
    d = donnees()
    brut = json.dumps(d, ensure_ascii=False, separators=(",", ":")).encode()
    # mtime=0 : la page ne change que si les données ou le modèle changent.
    paquet = base64.b64encode(gzip.compress(brut, compresslevel=9, mtime=0)).decode()
    annee, mois, jour = (int(x) for x in d["genere"][:10].split("-"))
    page = open(MODELE).read()
    for cle, valeur in {
        "@@NB_NOTIONS@@": nombre(len(d["n"])), "@@NB_LIENS@@": nombre(len(d["l"])),
        "@@NB_PROGRAMMES@@": str(len(d["programmes"])), "@@DATE@@": f"{jour} {MOIS[mois - 1]} {annee}",
        "@@LIEN_BASE@@": json.dumps(lien), "@@DONNEES@@": paquet,
    }.items():
        page = page.replace(cle, valeur)
    tete, corps = page.split("<!-- corps -->", 1)
    if artefact:
        sortie, contenu = artefact, tete + corps
    else:
        sortie = SORTIE
        contenu = ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
                   '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
                   f"{tete}</head>\n<body>\n{corps}</body>\n</html>\n")
    os.makedirs(os.path.dirname(os.path.abspath(sortie)), exist_ok=True)
    open(sortie, "w").write(contenu)
    return sortie


if __name__ == "__main__":
    artefact = sys.argv[sys.argv.index("--artefact") + 1] if "--artefact" in sys.argv else None
    lien = sys.argv[sys.argv.index("--lien") + 1] if "--lien" in sys.argv else ""
    chemin = construire(artefact, lien)
    print(f"Page écrite : {chemin} ({os.path.getsize(chemin) // 1024} Ko)")
