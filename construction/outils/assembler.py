"""Assemble toutes les extractions dans le jeu de données data/ (à la racine du dépôt), génère les vues lisibles
dans data/vues/ et l'atlas site/index.html, et tient le journal data/JOURNAL.md.

Usage : python3 outils/assembler.py

Le jeu de données compte quatre fichiers : programmes.json, objectifs.json (le texte officiel, mot pour mot),
notions.json (chaque notion renvoie à ses objectifs) et liens.json (les prérequis entre notions).
Chaque assemblage est comparé au précédent : les notions et liens ajoutés, retirés ou modifiés
sont écrits dans data/historique/<date>.json et résumés dans data/JOURNAL.md.
"""
import json
import os
from collections import Counter, defaultdict
from datetime import datetime

from commun import DONNEES, ORDRE_NIVEAUX, PROGRAMMES, VERSION, charger, id_objectif, registre

reg = registre()
# Programmes dont le BO ne contient pas d'exemples de réussite et sans document d'exemples séparé
SANS_EXEMPLES = {k for k, v in reg.items() if v.get("examples") == "aucun"}
REMPLACE_PAR = defaultdict(list)
for k, v in reg.items():
    for ancien in v.get("remplace", []):
        REMPLACE_PAR[ancien].append(k)
extraites, liens, par_fichier = charger()

# L'empreinte du PDF est posée à l'extraction (outils/estampiller.py). Une empreinte différente de celle
# du manifeste signale une notion tirée d'une version antérieure du programme, à ré-extraire.
MANIFESTE = json.load(open(os.path.join(PROGRAMMES, "sources.json")))["sources"]
perimees = {n["id"] for n in extraites
            if n["source"].get("fichier") in MANIFESTE and n["source"].get("sha256") != MANIFESTE[n["source"]["fichier"]]["sha256"]}
extraction = {}
for d in par_fichier.values():
    if "notions" in d:
        extraction[d["programme"]] = max(extraction.get(d["programme"], ""), d.get("extraitLe", ""))
os.makedirs(os.path.join(DONNEES, "historique"), exist_ok=True)
os.makedirs(os.path.join(DONNEES, "vues"), exist_ok=True)

progs = [k for k in reg if any(n["programme"] == k for n in extraites)]
maintenant = datetime.now().replace(microsecond=0)
entete = {"jeuDeDonnees": "Notions des programmes officiels français", "version": VERSION,
          "genereLe": maintenant.isoformat()}
programmes = {k: {"matiere": reg[k]["subject"], "classes": reg[k]["levels"], "fichier": reg[k]["file"],
                  "url": MANIFESTE.get(reg[k]["file"], {}).get("url"), "bo": reg[k]["bo"],
                  "sha256": MANIFESTE.get(reg[k]["file"], {}).get("sha256"), "extraitLe": extraction.get(k),
                  **({"suit": reg[k]["follows"]} if reg[k].get("follows") else {}),
                  **({"remplace": reg[k]["remplace"]} if reg[k].get("remplace") else {})} for k in progs}

# Objectifs officiels : un par texte distinct, dans une classe d'un programme. Plusieurs notions peuvent
# renvoyer au même objectif (puce découpée) et une notion à plusieurs objectifs (puces regroupées).
objectifs, notions = {}, []
for n in extraites:
    src = n["source"]
    refs = []
    for texte in n["objectifsOfficiels"]:
        oid = id_objectif(reg[n["programme"]]["code"], n["classe"], n["programme"], texte)
        o = objectifs.get(oid)
        if o is None:
            objectifs[oid] = {"id": oid, "programme": n["programme"], "classe": n["classe"], "domaine": n["domaine"],
                              "sousDomaine": n["sousDomaine"], "texte": texte,
                              "source": {k: src[k] for k in ("fichier", "bo", "page", "sha256") if k in src}}
        else:
            assert o["texte"] == texte and o["programme"] == n["programme"], f"empreinte en double : {oid}"
            o["source"]["page"] = min(o["source"]["page"], src["page"])
        refs.append(oid)
    notions.append({
        "id": n["id"], "programme": n["programme"], "matiere": n["matiere"], "domaine": n["domaine"],
        "sousDomaine": n["sousDomaine"], "classe": n["classe"], "cycle": n["cycle"],
        **({"periode": n["periode"]} if n.get("periode") else {}),
        "nom": n["nom"], "description": n["description"], "nature": n["nature"], "objectifs": refs,
        "criteres": n["criteres"], "question": n["question"],
        **({"acquisAnterieurs": n["acquisAnterieurs"]} if n.get("acquisAnterieurs") else {}),
        "source": {k: src[k] for k in ("page", "exemples", "exemplesPage", "exemplesSha256") if k in src},
    })
by_id = {n["id"]: n for n in notions}


def avec_textes(notion, textes):
    """Notion où les identifiants d'objectifs sont remplacés par leur texte, pour comparer deux assemblages."""
    return {**notion, "objectifs": [textes.get(o, o) for o in notion.get("objectifs", [])]}


# Journal : comparaison avec l'assemblage précédent
CHAMPS = ("nom", "classe", "nature", "domaine", "sousDomaine", "description", "objectifs", "criteres",
          "periode", "question", "source")
CHAMPS_LIEN = ("force", "origine", "continuite", "raison")
chemins = {k: os.path.join(DONNEES, f"{k}.json") for k in ("programmes", "objectifs", "notions", "liens")}
ancien = json.load(open(chemins["notions"])) if os.path.exists(chemins["notions"]) else None
nb = {}
if ancien and ancien.get("version") != VERSION:
    # Le format a changé : pas de comparaison champ par champ avec l'assemblage précédent.
    with open(os.path.join(DONNEES, "JOURNAL.md"), "a") as j:
        j.write(f"## {maintenant:%d/%m/%Y %H:%M}\n\nNouveau format des données (version {VERSION}, "
                f"auparavant {ancien.get('version') or ancien.get('dataset', '?')}) : pas de comparaison avec "
                f"l'assemblage précédent. {len(notions)} notions, {len(objectifs)} objectifs, {len(liens)} liens.\n\n\n")
    print(f"Journal : nouveau format {VERSION}")
elif ancien:
    textes_avant = {o["id"]: o["texte"] for o in json.load(open(chemins["objectifs"]))["objectifs"]}
    textes_apres = {i: o["texte"] for i, o in objectifs.items()}
    avant = {n["id"]: avec_textes(n, textes_avant) for n in ancien["notions"]}
    apres = {i: avec_textes(n, textes_apres) for i, n in by_id.items()}
    liens_avant = {(l["vers"], l["de"]): l for l in json.load(open(chemins["liens"]))["liens"]}
    liens_apres = {(l["vers"], l["de"]): l for l in liens}
    modifiees = []
    for nid in sorted(set(avant) & set(apres)):
        champs = {c: {"avant": avant[nid].get(c), "apres": apres[nid].get(c)}
                  for c in CHAMPS if avant[nid].get(c) != apres[nid].get(c)}
        if champs:
            modifiees.append({"id": nid, "programme": apres[nid]["programme"], "champs": champs})
    diff = {
        "date": maintenant.isoformat(), "precedent": ancien.get("genereLe"),
        "notions": {
            "ajoutees": [{"id": i, "programme": apres[i]["programme"], "nom": apres[i]["nom"]}
                         for i in sorted(set(apres) - set(avant))],
            "retirees": [{"id": i, "programme": avant[i].get("programme"), "nom": avant[i]["nom"]}
                         for i in sorted(set(avant) - set(apres))],
            "modifiees": modifiees},
        "liens": {
            "ajoutes": [liens_apres[k] for k in sorted(set(liens_apres) - set(liens_avant))],
            "retires": [liens_avant[k] for k in sorted(set(liens_avant) - set(liens_apres))],
            "modifies": [liens_apres[k] for k in sorted(set(liens_avant) & set(liens_apres))
                         if any(liens_avant[k].get(c) != liens_apres[k].get(c) for c in CHAMPS_LIEN)]},
    }
    nb = {k: len(v) for part in ("notions", "liens") for k, v in diff[part].items()}
    if any(nb.values()):
        nom = maintenant.strftime("%Y-%m-%dT%H%M%S") + ".json"
        json.dump(diff, open(os.path.join(DONNEES, "historique", nom), "w"), ensure_ascii=False, indent=2)
        touches = Counter(x["programme"] for k in ("ajoutees", "retirees", "modifiees") for x in diff["notions"][k])
        entree = [f"## {maintenant:%d/%m/%Y %H:%M}", "",
                  f"Notions : {nb['ajoutees']} ajoutée(s), {nb['retirees']} retirée(s), {nb['modifiees']} modifiée(s). "
                  f"Liens : {nb['ajoutes']} ajouté(s), {nb['retires']} retiré(s), {nb['modifies']} modifié(s).", ""]
        if touches:
            entree += ["Programmes touchés : " + ", ".join(f"{p} ({c})" for p, c in touches.most_common()) + ".", ""]
        entree += [f"Détail : [historique/{nom}](historique/{nom})", "", ""]
        with open(os.path.join(DONNEES, "JOURNAL.md"), "a") as j:
            j.write("\n".join(entree))
        print(f"Journal : {nb}")
for cle, contenu in (("programmes", {"programmes": programmes}),
                     ("objectifs", {"nombreObjectifs": len(objectifs), "objectifs": list(objectifs.values())}),
                     ("notions", {"nombreNotions": len(notions), "notions": notions}),
                     ("liens", {"nombreLiens": len(liens), "liens": liens})):
    json.dump({**entete, **contenu}, open(chemins[cle], "w"), ensure_ascii=False, indent=2)
textes_objectifs = {i: o["texte"] for i, o in objectifs.items()}

pre_of = defaultdict(list)
for l in liens:
    pre_of[l["vers"]].append(l)


def label(nid, prog):
    n = by_id[nid]
    matiere = "" if n["programme"] == prog else f"{n['matiere']}, "
    return f"{n['nom']} ({matiere}{n['classe']})"


index = ["# Notions par programme", "",
         "Vues lisibles générées automatiquement à partir de [notions.json](../notions.json), [objectifs.json](../objectifs.json) et [liens.json](../liens.json).", "",
         "| Programme | Classes | Notions | Prérequis |", "|---|---|---:|---:|"]
for prog in progs:
    info = reg[prog]
    items = [n for n in notions if n["programme"] == prog]
    ids = {n["id"] for n in items}
    liens_prog = [l for l in liens if l["vers"] in ids]
    levels = [c for c in info["levels"] if any(n["classe"] == c for n in items)]
    index.append(f"| [{info['subject']} ({', '.join(info['levels'])})]({prog}.md) | "
                 f"{', '.join(levels)} | {len(items)} | {len(liens_prog)} |")

    domaines = list(dict.fromkeys(n["domaine"] for n in items))
    out = [f"# {info['subject']} : {', '.join(info['levels'])}", "",
           f"Source : {info['bo']} ([PDF](../../construction/programmes-officiels/{info['file']})), extraite le {extraction.get(prog)}. "
           "Vue générée automatiquement, à ne pas modifier à la main.", ""]
    if REMPLACE_PAR.get(prog):
        out += [f"Programme remplacé progressivement par : {', '.join(f'[{p}]({p}.md)' for p in REMPLACE_PAR[prog])}.", ""]
    if info.get("remplace"):
        out += [f"Remplace : {', '.join(f'[{p}]({p}.md)' for p in info['remplace'])}.", ""]
    perimees_prog = sum(1 for n in items if n["id"] in perimees)
    if perimees_prog:
        out += [f"⚠ {perimees_prog} notion(s) extraite(s) d'une version antérieure du PDF : à ré-extraire "
                "(voir `python3 outils/etat.py`).", ""]
    out += ["| Domaine | " + " | ".join(levels) + " |", "|---|" + "---:|" * len(levels)]
    cnt = Counter((n["domaine"], n["classe"]) for n in items)
    for dom in domaines:
        out.append(f"| {dom} | " + " | ".join(str(cnt[(dom, l)]) for l in levels) + " |")
    tot = Counter(n["classe"] for n in items)
    out.append("| **Total** | " + " | ".join(f"**{tot[l]}**" for l in levels) + " |")
    texte = sum(1 for l in liens_prog if l["origine"] == "texte")
    out += ["", f"{len(liens_prog)} liens de prérequis, dont {texte} écrits dans le programme "
            "(les autres sont déduits et à relire).", ""]
    for lvl in sorted(levels, key=ORDRE_NIVEAUX.index):
        out += [f"## {lvl}", ""]
        for dom in domaines:
            sel = [n for n in items if n["classe"] == lvl and n["domaine"] == dom]
            if not sel:
                continue
            out += [f"### {dom}", ""]
            sub = None
            for n in sel:
                if n["sousDomaine"] != sub:
                    sub = n["sousDomaine"]
                    out += [f"#### {sub}", ""]
                out += [f"**{n['nom']}** · _{n['nature']}_ · `{n['id']}`" +
                        (f" · {n['periode']}" if n.get("periode") else ""), "",
                        n["description"], "", "Critères de réussite :"]
                out += [f"- {e}" for e in n["criteres"]]
                if pre_of.get(n["id"]):
                    out += ["", "Prérequis : " + " ; ".join(
                        label(l["de"], prog) + ("" if l["force"] == "indispensable" else " _(utile)_")
                        for l in pre_of[n["id"]])]
                src = n["source"]
                if src.get("exemples"):
                    origine = f"programme p. {src['page']} ; critères tirés des exemples de réussite Éduscol p. {src.get('exemplesPage', '?')}"
                elif prog in SANS_EXEMPLES:
                    origine = f"programme p. {src['page']} ; pas d'exemples officiels, critères rédigés à partir des objectifs"
                else:
                    origine = f"programme p. {src['page']}"
                if n["id"] in perimees:
                    origine += " ; ⚠ extraite d'une version antérieure du PDF"
                out += ["", f"> Question : {n['question'].replace('{{prenom}}', "l'enfant")}", "",
                        f"<sub>Source : {origine}</sub>", ""]
    open(os.path.join(DONNEES, "vues", f"{prog}.md"), "w").write("\n".join(out))

index += ["", f"Total : {len(notions)} notions, {len(liens)} liens de prérequis."]
open(os.path.join(DONNEES, "vues", "index.md"), "w").write("\n".join(index) + "\n")
print(f"{len(notions)} notions, {len(objectifs)} objectifs, {len(liens)} liens, {len(progs)} programme(s) : {', '.join(progs)}")
if perimees:
    print(f"⚠ {len(perimees)} notion(s) extraite(s) d'une version antérieure de leur PDF : voir python3 outils/etat.py")

# Atlas (site/index.html), reconstruit à partir de data/
from construire_site import construire  # noqa: E402
print(f"Atlas : {os.path.relpath(construire(), os.path.dirname(DONNEES))}")
