"""Enregistre un PDF de programme dans le manifeste et prépare son texte pour l'extraction.

Usage :
  python3 outils/preparer_pdf.py <chemin dans programmes-officiels/> --url URL --bo "BO n° …"
  python3 outils/preparer_pdf.py <chemin dans programmes-officiels/> --depuis <nouveau.pdf> [--url URL] [--bo …]

1. Nouveau PDF (déjà copié dans programmes-officiels/) : ajoute son entrée à sources.json
   (adresse, BO, date, SHA-256, taille, pages).
2. Nouvelle version d'un PDF connu (--depuis) : l'ancienne version est déplacée dans
   programmes-officiels/archives/, son texte dans textes/archives/, et l'entrée du manifeste garde
   la trace de l'ancienne empreinte dans `anciennesVersions`. Les notions extraites de l'ancienne
   version restent vérifiables, et outils/etat.py les signale comme à ré-extraire.
3. Écrit textes/<nom>.txt (pdftotext -layout, marqueurs « === PAGE n === »). Si le PDF ne contient
   pas de texte (images), lance la reconnaissance de texte (outils/ocr_pdf.py, macOS).
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import date

from commun import RACINE

PROGRAMMES = os.path.join(os.path.dirname(RACINE), "programmes-officiels")
CHEMIN_MANIFESTE = os.path.join(PROGRAMMES, "sources.json")
ICI = os.path.dirname(os.path.abspath(__file__))


def option(nom):
    if nom in sys.argv:
        i = sys.argv.index(nom)
        return sys.argv[i + 1]
    return None


rel = sys.argv[1]
cible = os.path.join(PROGRAMMES, rel)
nom = os.path.splitext(os.path.basename(rel))[0]
texte = os.path.join(RACINE, "textes", f"{nom}.txt")
manifeste = json.load(open(CHEMIN_MANIFESTE))
entree = manifeste["sources"].get(rel)
depuis = option("--depuis")

if depuis:
    nouveau = hashlib.sha256(open(depuis, "rb").read()).hexdigest()
    if entree and nouveau == entree["sha256"]:
        sys.exit(f"{rel} : ce PDF est identique à la version enregistrée, rien à faire.")
    if entree and os.path.exists(cible):
        # Archive l'ancienne version et son texte, sans rien écraser.
        court = entree["sha256"][:8]
        archive = os.path.join("archives", f"{nom}-{entree['downloadedAt']}-{court}.pdf")
        os.makedirs(os.path.join(PROGRAMMES, "archives"), exist_ok=True)
        shutil.move(cible, os.path.join(PROGRAMMES, archive))
        if os.path.exists(texte):
            os.makedirs(os.path.join(RACINE, "textes", "archives"), exist_ok=True)
            shutil.move(texte, os.path.join(RACINE, "textes", "archives", f"{nom}-{entree['downloadedAt']}-{court}.txt"))
        ancienne = {k: entree[k] for k in ("sha256", "downloadedAt", "bytes", "pages", "url", "bo") if k in entree}
        entree.setdefault("anciennesVersions", []).append({**ancienne, "archive": archive})
        print(f"Ancienne version archivée : programmes-officiels/{archive}")
    os.makedirs(os.path.dirname(cible), exist_ok=True)
    shutil.copyfile(depuis, cible)

if not os.path.exists(cible):
    sys.exit(f"{cible} introuvable : copie le PDF dans programmes-officiels/ ou utilise --depuis.")
entree = entree or {}
entree["url"] = option("--url") or entree.get("url")
entree["bo"] = option("--bo") or entree.get("bo")
if not entree["url"] or not entree["bo"]:
    sys.exit("Indique --url et --bo pour un nouveau PDF.")
donnees = open(cible, "rb").read()
info = subprocess.run(["pdfinfo", cible], capture_output=True, text=True).stdout
pages = int(next(l.split()[-1] for l in info.splitlines() if l.startswith("Pages:")))
entree.update({"downloadedAt": date.today().isoformat(), "sha256": hashlib.sha256(donnees).hexdigest(),
               "bytes": len(donnees), "pages": pages})
manifeste["sources"][rel] = dict(sorted(entree.items(), key=lambda kv: kv[0] == "anciennesVersions"))
manifeste["sources"] = dict(sorted(manifeste["sources"].items()))
json.dump(manifeste, open(CHEMIN_MANIFESTE, "w"), ensure_ascii=False, indent=2)
print(f"Manifeste : {rel}, {pages} pages, sha256 {entree['sha256'][:12]}…")

# Texte page par page (pdftotext sépare les pages par un saut de page \f)
brut = subprocess.run(["pdftotext", "-layout", cible, "-"], capture_output=True, text=True).stdout
morceaux = brut.split("\f")[:pages]
open(texte, "w").write("".join(f"=== PAGE {i} ===\n" + "".join(l + "\n" for l in p.splitlines() if l.strip()) + "\n"
                               for i, p in enumerate(morceaux, 1)))
print(f"Texte : textes/{nom}.txt")
if len(brut.strip()) < 1000:
    print("Le PDF ne contient presque pas de texte (images) : reconnaissance de texte…")
    subprocess.run([sys.executable, os.path.join(ICI, "ocr_pdf.py"), rel], check=True)
print("Étape suivante : python3 outils/etat.py")
