"""Reconnaissance de texte (OCR macOS Vision) pour les PDF de programmes publiés en images.

Usage : python3 outils/ocr_pdf.py <chemin relatif dans programmes-officiels/> [...]
Écrit textes/<nom>.ocr.txt, page par page (marqueurs « === PAGE n === »), utilisé par
verifier_sources.py quand le PDF ne contient pas de texte. Nécessite pdftoppm et swiftc (macOS).
"""
import os
import subprocess
import sys
import tempfile

from commun import RACINE

PROGRAMMES = os.path.join(os.path.dirname(RACINE), "programmes-officiels")
ICI = os.path.dirname(os.path.abspath(__file__))


def ordre_lecture(lignes):
    """Remet les lignes dans l'ordre de lecture : dans les tableaux à deux colonnes, toute la colonne
    de gauche puis celle de droite, entre deux lignes qui traversent la page."""
    out, gauche, droite = [], [], []
    for l in lignes.splitlines():
        if "\t" not in l:
            continue
        coords, texte = l.split("\t", 1)
        x0, _, x1, _ = map(float, coords.split())
        if x0 < 0.45 and x1 > 0.55:
            out += gauche + droite + [texte]
            gauche, droite = [], []
        else:
            (gauche if x0 < 0.45 else droite).append(texte)
    return out + gauche + droite


tmp = tempfile.mkdtemp(prefix="ocr-")
binaire = os.path.join(tmp, "visionocr")
subprocess.run(["swiftc", "-O", os.path.join(ICI, "ocr.swift"), "-o", binaire], check=True)

for rel in sys.argv[1:]:
    nom = os.path.splitext(os.path.basename(rel))[0]
    dossier = os.path.join(tmp, nom)
    os.makedirs(dossier)
    subprocess.run(["pdftoppm", "-r", "200", "-png", os.path.join(PROGRAMMES, rel), os.path.join(dossier, "p")], check=True)
    pages = sorted(f for f in os.listdir(dossier) if f.endswith(".png"))
    out = []
    for i, f in enumerate(pages, 1):
        lignes = subprocess.run([binaire, os.path.join(dossier, f)], capture_output=True, text=True, check=True).stdout
        out += [f"=== PAGE {i} ==="] + ordre_lecture(lignes) + [""]
    cible = os.path.join(RACINE, "textes", f"{nom}.ocr.txt")
    open(cible, "w").write("\n".join(out))
    print(f"{rel} : {len(pages)} pages -> {cible}")
