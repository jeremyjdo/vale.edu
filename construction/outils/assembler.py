"""Assemble toutes les extractions dans le jeu de données data/ (à la racine du dépôt), génère les vues lisibles
dans data/vues/ et l'atlas site/index.html, et tient le journal data/JOURNAL.md.

Usage : python3 outils/assembler.py

Chaque assemblage est comparé au précédent : les notions et prérequis ajoutés, retirés ou modifiés
sont écrits dans data/historique/<date>.json et résumés dans data/JOURNAL.md.
"""
import json
import os
from collections import Counter, defaultdict
from datetime import date, datetime

from commun import DONNEES, ORDRE_NIVEAUX, PROGRAMMES, TYPES_FR, charger, registre

reg = registre()
# Programmes dont le BO ne contient pas d'exemples de réussite et sans document d'exemples séparé
SANS_EXEMPLES = {k for k, v in reg.items() if v.get("examples") == "aucun"}
REMPLACE_PAR = defaultdict(list)
for k, v in reg.items():
    for ancien in v.get("remplace", []):
        REMPLACE_PAR[ancien].append(k)
notions, prereqs, par_fichier = charger()

# L'empreinte du PDF est posée à l'extraction (outils/estampiller.py). Une empreinte différente de celle
# du manifeste signale une notion tirée d'une version antérieure du programme, à ré-extraire.
MANIFESTE = json.load(open(os.path.join(PROGRAMMES, "sources.json")))["sources"]
perimees = {n["id"] for n in notions
            if n["source"].get("file") in MANIFESTE and n["source"].get("sha256") != MANIFESTE[n["source"]["file"]]["sha256"]}
extraction = {}
for d in par_fichier.values():
    if "notions" in d:
        extraction[d["programme"]] = max(extraction.get(d["programme"], ""), d.get("extractedAt", ""))
by_id = {n["id"]: n for n in notions}
os.makedirs(os.path.join(DONNEES, "historique"), exist_ok=True)
os.makedirs(os.path.join(DONNEES, "vues"), exist_ok=True)

progs = [k for k in reg if any(n["programme"] == k for n in notions)]
maintenant = datetime.now().replace(microsecond=0)
meta = {
    "dataset": "Notions des programmes officiels français",
    "version": "0.3",
    "generatedAt": maintenant.isoformat(),
    "programmes": {k: {**{kk: reg[k][kk] for kk in ("subject", "levels", "file", "bo")},
                       "sha256": MANIFESTE.get(reg[k]["file"], {}).get("sha256"),
                       "extractedAt": extraction.get(k)} for k in progs},
}

# Journal : comparaison avec l'assemblage précédent
CHAMPS = ("name", "level", "type", "domain", "subdomain", "description", "officialObjectives", "evidence",
          "period", "assessmentPrompt", "source")
chemin_notions = os.path.join(DONNEES, "notions.json")
chemin_prereqs = os.path.join(DONNEES, "prerequis.json")
if os.path.exists(chemin_notions):
    ancien = json.load(open(chemin_notions))
    avant = {n["id"]: n for n in ancien["notions"]}
    liens_avant = {(p["topicId"], p["prerequisiteId"]): p for p in json.load(open(chemin_prereqs))["prerequisites"]}
    liens_apres = {(p["topicId"], p["prerequisiteId"]): p for p in prereqs}
    modifiees = []
    for nid in sorted(set(avant) & set(by_id)):
        champs = {c: {"avant": avant[nid].get(c), "apres": by_id[nid].get(c)}
                  for c in CHAMPS if avant[nid].get(c) != by_id[nid].get(c)}
        if champs:
            modifiees.append({"id": nid, "programme": by_id[nid]["programme"], "champs": champs})
    diff = {
        "date": maintenant.isoformat(), "precedent": ancien.get("generatedAt"),
        "notions": {
            "ajoutees": [{"id": i, "programme": by_id[i]["programme"], "name": by_id[i]["name"]}
                         for i in sorted(set(by_id) - set(avant))],
            "retirees": [{"id": i, "programme": avant[i].get("programme"), "name": avant[i]["name"]}
                         for i in sorted(set(avant) - set(by_id))],
            "modifiees": modifiees},
        "prerequis": {
            "ajoutes": [liens_apres[k] for k in sorted(set(liens_apres) - set(liens_avant))],
            "retires": [liens_avant[k] for k in sorted(set(liens_avant) - set(liens_apres))],
            "modifies": [liens_apres[k] for k in sorted(set(liens_avant) & set(liens_apres))
                         if any(liens_avant[k].get(c) != liens_apres[k].get(c) for c in ("strength", "origin", "reason"))]},
    }
    nb = {k: len(v) for part in ("notions", "prerequis") for k, v in diff[part].items()}
    if any(nb.values()):
        nom = maintenant.strftime("%Y-%m-%dT%H%M%S") + ".json"
        json.dump(diff, open(os.path.join(DONNEES, "historique", nom), "w"), ensure_ascii=False, indent=2)
        touches = Counter(x["programme"] for k in ("ajoutees", "retirees", "modifiees") for x in diff["notions"][k])
        entree = [f"## {maintenant:%d/%m/%Y %H:%M}", "",
                  f"Notions : {nb['ajoutees']} ajoutée(s), {nb['retirees']} retirée(s), {nb['modifiees']} modifiée(s). "
                  f"Prérequis : {nb['ajoutes']} ajouté(s), {nb['retires']} retiré(s), {nb['modifies']} modifié(s).", ""]
        if touches:
            entree += ["Programmes touchés : " + ", ".join(f"{p} ({c})" for p, c in touches.most_common()) + ".", ""]
        entree += [f"Détail : [historique/{nom}](historique/{nom})", "", ""]
        with open(os.path.join(DONNEES, "JOURNAL.md"), "a") as j:
            j.write("\n".join(entree))
        print(f"Journal : {nb}")
json.dump({**meta, "notionCount": len(notions), "notions": notions},
          open(chemin_notions, "w"), ensure_ascii=False, indent=2)
json.dump({**meta, "prerequisiteCount": len(prereqs), "prerequisites": prereqs},
          open(chemin_prereqs, "w"), ensure_ascii=False, indent=2)

pre_of = defaultdict(list)
for p in prereqs:
    pre_of[p["topicId"]].append(p)


def label(nid, prog):
    n = by_id[nid]
    matiere = "" if n["programme"] == prog else f"{n['subject']}, "
    return f"{n['name']} ({matiere}{n['level']})"


index = ["# Notions par programme", "",
         "Vues lisibles générées automatiquement à partir de [notions.json](../notions.json) et [prerequis.json](../prerequis.json).", "",
         "| Programme | Classes | Notions | Prérequis |", "|---|---|---:|---:|"]
for prog in progs:
    info = reg[prog]
    items = [n for n in notions if n["programme"] == prog]
    ids = {n["id"] for n in items}
    liens = [p for p in prereqs if p["topicId"] in ids]
    levels = [l for l in info["levels"] if any(n["level"] == l for n in items)]
    index.append(f"| [{info['subject']} ({', '.join(info['levels'])})]({prog}.md) | "
                 f"{', '.join(levels)} | {len(items)} | {len(liens)} |")

    domaines = list(dict.fromkeys(n["domain"] for n in items))
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
    cnt = Counter((n["domain"], n["level"]) for n in items)
    for dom in domaines:
        out.append(f"| {dom} | " + " | ".join(str(cnt[(dom, l)]) for l in levels) + " |")
    tot = Counter(n["level"] for n in items)
    out.append("| **Total** | " + " | ".join(f"**{tot[l]}**" for l in levels) + " |")
    texte = sum(1 for p in liens if p["origin"] == "texte")
    out += ["", f"{len(liens)} liens de prérequis, dont {texte} écrits dans le programme "
            "(les autres sont déduits et à relire).", ""]
    for lvl in sorted(levels, key=ORDRE_NIVEAUX.index):
        out += [f"## {lvl}", ""]
        for dom in domaines:
            sel = [n for n in items if n["level"] == lvl and n["domain"] == dom]
            if not sel:
                continue
            out += [f"### {dom}", ""]
            sub = None
            for n in sel:
                if n["subdomain"] != sub:
                    sub = n["subdomain"]
                    out += [f"#### {sub}", ""]
                out += [f"**{n['name']}** · _{TYPES_FR[n['type']]}_ · `{n['id']}`" +
                        (f" · {n['period']}" if n.get("period") else ""), "",
                        n["description"], "", "Critères de réussite :"]
                out += [f"- {e}" for e in n["evidence"]]
                if pre_of.get(n["id"]):
                    out += ["", "Prérequis : " + " ; ".join(
                        label(p["prerequisiteId"], prog) + ("" if p["strength"] == "hard" else " _(utile)_")
                        for p in pre_of[n["id"]])]
                src = n["source"]
                if src.get("examples"):
                    origine = f"programme p. {src['page']} ; critères tirés des exemples de réussite Éduscol p. {src.get('examplesPage', '?')}"
                elif prog in SANS_EXEMPLES:
                    origine = f"programme p. {src['page']} ; pas d'exemples officiels, critères rédigés à partir des objectifs"
                else:
                    origine = f"programme p. {src['page']}"
                if n["id"] in perimees:
                    origine += " ; ⚠ extraite d'une version antérieure du PDF"
                out += ["", f"> Question : {n['assessmentPrompt'].replace('{{prenom}}', "l'enfant")}", "",
                        f"<sub>Source : {origine}</sub>", ""]
    open(os.path.join(DONNEES, "vues", f"{prog}.md"), "w").write("\n".join(out))

index += ["", f"Total : {len(notions)} notions, {len(prereqs)} liens de prérequis."]
open(os.path.join(DONNEES, "vues", "index.md"), "w").write("\n".join(index) + "\n")
print(f"{len(notions)} notions, {len(prereqs)} prérequis, {len(progs)} programme(s) : {', '.join(progs)}")
if perimees:
    print(f"⚠ {len(perimees)} notion(s) extraite(s) d'une version antérieure de leur PDF : voir python3 outils/etat.py")

# Atlas (site/index.html), reconstruit à partir de data/
from construire_site import construire  # noqa: E402
print(f"Atlas : {os.path.relpath(construire(), os.path.dirname(DONNEES))}")
