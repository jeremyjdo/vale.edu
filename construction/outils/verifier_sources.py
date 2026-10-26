"""Vérifie que les notions correspondent toujours aux PDF officiels, et détecte les nouvelles versions.

Usage :
  python3 outils/verifier_sources.py              # empreintes des PDF locaux + fidélité des notions
  python3 outils/verifier_sources.py --en-ligne   # en plus, retélécharge chaque PDF et compare l'empreinte

1. Empreintes : chaque PDF de programmes-officiels/ est comparé à son SHA-256 enregistré dans
   programmes-officiels/sources.json. Une différence signale un fichier modifié.
2. Fidélité : chaque phrase de `officialObjectives` doit se retrouver dans le texte du PDF cité par
   `source.file`. Les notions dont le texte n'est plus retrouvé sont listées : ce sont celles à revoir
   si le programme a changé (ou celles mal recopiées).
3. En ligne : si le PDF publié a changé, la nouvelle version est enregistrée à part (jamais à la place
   de l'ancienne) et la vérification de fidélité est refaite sur elle, pour lister les notions touchées.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
import unicodedata
import urllib.request
from collections import Counter, defaultdict

from commun import PROGRAMMES, RACINE, charger

MANIFESTE = json.load(open(os.path.join(PROGRAMMES, "sources.json")))["sources"]
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower().replace("œ", "oe").replace("æ", "ae"))
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9]", "", s)


_cache = {}
def texte_pdf(path):
    """Texte normalisé du PDF, en modes « raw » et « layout » concaténés.
    Pour un PDF en images, texte de l'OCR (textes/<nom>.ocr.txt, voir ocr_pdf.py) s'il existe."""
    if path not in _cache:
        morceaux = [subprocess.run(["pdftotext", mode, path, "-"], capture_output=True, text=True).stdout
                    for mode in ("-raw", "-layout")]
        texte, ocr = "|".join(norm(m) for m in morceaux), False
        fichier_ocr = os.path.join(RACINE, "textes", os.path.splitext(os.path.basename(path))[0] + ".ocr.txt")
        if len(texte) < 1000 and os.path.exists(fichier_ocr):
            texte, ocr = norm(open(fichier_ocr).read()), True
        _cache[path] = (texte, ocr)
    return _cache[path]


def segments(objectif):
    """Découpe un objectif en morceaux vérifiables (les extractions joignent parfois plusieurs puces)."""
    parts = re.split(r"\s+[–—]\s+|\s*;\s*|\s:\s|\n", objectif)
    segs = [p for p in (norm(x) for x in parts) if len(p) >= 12]
    # Objectif très court (« Voix passive. ») : on le cherche en entier.
    return segs or [norm(objectif)]


def fidelite(notions, pdf_pour):
    """Renvoie {programme: Counter(statut)} et la liste des notions non retrouvées."""
    stats, absentes = defaultdict(Counter), []
    for n in notions:
        pdf = pdf_pour(n["source"]["file"])
        texte, ocr = texte_pdf(pdf)
        if len(texte) < 1000:
            stats[n["programme"]]["PDF image, non vérifiable"] += 1
            continue
        suffixe = " (OCR)" if ocr else ""
        segs = [s for o in n["officialObjectives"] for s in segments(o)]
        trouves = sum(1 for s in segs if s in texte)
        if segs and trouves == len(segs):
            stats[n["programme"]]["retrouvée" + suffixe] += 1
        elif trouves:
            stats[n["programme"]]["partielle" + suffixe] += 1
        else:
            stats[n["programme"]]["non retrouvée" + suffixe] += 1
            absentes.append((n["id"], n["source"]["page"], n["officialObjectives"][0][:90]))
    return stats, absentes


def afficher(stats, absentes, titre):
    print(f"\n== {titre}")
    for prog, c in stats.items():
        print(f"  {prog:16} " + ", ".join(f"{k} {v}" for k, v in c.most_common()))
    if absentes:
        print(f"  {len(absentes)} notion(s) dont l'objectif n'est pas retrouvé dans le PDF :")
        for nid, page, txt in absentes:
            print(f"   - {nid} (p. {page}) : {txt}")


# 1. Empreintes locales
print("== Empreintes des PDF locaux")
modifies = []
for rel, info in MANIFESTE.items():
    path = os.path.join(PROGRAMMES, rel)
    if not os.path.exists(path):
        print(f"  MANQUANT : {rel}")
    elif sha256(path) != info["sha256"]:
        modifies.append(rel)
        print(f"  MODIFIÉ localement : {rel}")
print(f"  {len(MANIFESTE) - len(modifies)} / {len(MANIFESTE)} PDF identiques au manifeste")

# 2. Fidélité des notions au PDF local
notions, _, _ = charger()
stats, absentes = fidelite(notions, lambda f: os.path.join(PROGRAMMES, f))
afficher(stats, absentes, "Fidélité des notions aux PDF locaux")

# 3. Vérification en ligne
if "--en-ligne" in sys.argv:
    print("\n== Versions publiées en ligne")
    dossier = tempfile.mkdtemp(prefix="nouvelles-versions-")
    nouvelles = {}
    for rel, info in MANIFESTE.items():
        try:
            req = urllib.request.Request(info["url"], headers={"User-Agent": UA})
            data = urllib.request.urlopen(req, timeout=60).read()
        except Exception as e:  # page retirée, déplacée ou bloquée
            print(f"  INACCESSIBLE : {rel} ({e})")
            continue
        if hashlib.sha256(data).hexdigest() != info["sha256"]:
            cible = os.path.join(dossier, rel.replace("/", "__"))
            open(cible, "wb").write(data)
            nouvelles[rel] = cible
            print(f"  NOUVELLE VERSION : {rel} -> enregistrée dans {cible}")
            print(f"    pour l'adopter : python3 outils/preparer_pdf.py {rel} --depuis {cible} --bo \"<BO de la nouvelle version>\"")
    print(f"  {len(MANIFESTE) - len(nouvelles)} PDF inchangés en ligne")
    if nouvelles:
        touchees = [n for n in notions if n["source"]["file"] in nouvelles]
        stats, absentes = fidelite(touchees, lambda f: nouvelles.get(f, os.path.join(PROGRAMMES, f)))
        afficher(stats, absentes, "Notions à revoir avec les nouvelles versions")
