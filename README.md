# vale.edu

**Le curriculum scolaire français, de la petite section à la 3e, découpé en notions et relié par les prérequis.**

vale.edu est une base de données ouverte du curriculum français : tout ce que les programmes officiels prévoient d'enseigner, classe par classe et matière par matière. Chaque objectif des programmes devient une notion : ce qu'elle veut dire, comment savoir si elle est acquise, et ce qu'il faut savoir avant. Chaque notion renvoie au texte officiel, à la page près.

| | |
|---|---|
| Programmes officiels | 43, de la petite section à la 3e (34 PDF publiés au Bulletin officiel) |
| Notions | 5 604 |
| Liens de prérequis | 8 002, chacun avec sa raison |
| Matières | français, mathématiques, sciences, histoire-géographie, langues vivantes, EMC, vie affective et relationnelle, arts, EPS, éducation aux médias |

Le projet s'inspire de la [taxonomie ouverte de Marble](https://github.com/withmarbleapp/os-taxonomy), construite à partir des curriculums américain et britannique du primaire. vale.edu en reprend le principe et le format pour le curriculum français, et l'étend au collège.

## Pourquoi

En France, le curriculum est fixé par les programmes officiels. Ils disent ce qu'un élève apprend chaque année, mais ils sont publiés en PDF, matière par matière et cycle par cycle, sans lien explicite d'une année à l'autre. Pour accompagner un enfant, il manque une base structurée : quelles notions, dans quel ordre, et comment savoir si elles sont acquises.

vale.edu veut fournir cette base, ouverte et réutilisable :

- **aux parents**, pour savoir ce qui s'apprend dans l'année et, quand quelque chose bloque, remonter aux notions qui manquent ;
- **aux enseignants**, pour repérer les prérequis d'une notion et préparer une remédiation ou un approfondissement ;
- **aux développeurs**, pour construire des outils sur un référentiel commun : exercices, fiches, plannings de révision, parcours adaptatifs.

## Consulter

- **Le site** : en ligne sur **[vale-edu.vercel.app](https://vale-edu.vercel.app)**, ou en ouvrant [`site/index.html`](site/index.html) dans un navigateur (la page est autonome, sans serveur). Une carte montre toutes les notions, classe par classe et matière par matière. Un clic sur une notion trace tout ce qu'il faut savoir avant, et ouvre sa fiche : description, question à poser, critères de réussite, prérequis, texte officiel et lien vers la page du PDF.
- **Les vues texte** : [`data/vues/`](data/vues/index.md), une page Markdown par programme.
- **Les données** : [`data/notions.json`](data/) et `prerequis.json`, décrits dans [`data/README.md`](data/README.md).

## Couverture

Nombre de notions par matière et par cycle :

| Matière | Cycle 1 (PS-GS) | Cycle 2 (CP-CE2) | Cycle 3 (CM1-6e) | Cycle 4 (5e-3e) | Total |
|---|--:|--:|--:|--:|--:|
| Français | 107 | 203 | 289 | 264 | 863 |
| Mathématiques | 82 | 251 | 384 | 249 | 966 |
| Sciences et technologie | 48 | 158 | 125 | 239 | 570 |
| Histoire-géographie | 73 | 65 | 115 | 69 | 322 |
| Langues vivantes¹ | | 151 | 619 | 1 285 | 2 055 |
| Enseignement moral et civique | | 43 | 45 | 36 | 124 |
| Vie affective et relationnelle | 29 | 39 | 42 | 58 | 168 |
| Arts (arts plastiques, musique, histoire des arts) | 75 | 41 | 75 | 98 | 289 |
| Éducation physique et sportive | 42 | 81 | 59 | 37 | 219 |
| Éducation aux médias et à l'information | | | | 28 | 28 |

¹ Au collège, l'anglais, l'espagnol, l'allemand et l'italien ont chacun leur programme : 1 683 notions à eux quatre.

En maternelle, le programme est écrit par domaine (« Mobiliser le langage », « Explorer le monde »…) ; ses notions sont rangées dans la matière la plus proche. Les programmes en vigueur, et ceux qui en remplacent d'autres progressivement, sont listés dans [`construction/programmes-officiels/README.md`](construction/programmes-officiels/README.md).

## Une notion

```json
{
  "id": "fr-ma-ce1-fra-07",
  "programme": "maths-c2",
  "type": "PROCEDURAL",
  "subject": "Mathématiques",
  "domain": "Nombres, calcul et résolution de problèmes",
  "subdomain": "Les fractions",
  "level": "CE1",
  "cycle": 2,
  "ageRangeStart": 7,
  "ageRangeEnd": 8,
  "name": "Additionner et soustraire des fractions de même dénominateur",
  "description": "Calculer par exemple 2/3 - 1/3 ou 1/5 + 2/5 en s'aidant de manipulations et de dessins…",
  "officialObjectives": ["Additionner et soustraire des fractions de même dénominateur."],
  "evidence": [
    "Calcule 2/3 - 1/3 ou 1/5 + 2/5 en s'appuyant sur des manipulations et des représentations.",
    "Verbalise le calcul : « deux tiers du tout moins un tiers du tout, cela fait un tiers du tout »."
  ],
  "assessmentPrompt": "Est-ce que {{prenom}} sait calculer 1/5 + 2/5 en expliquant avec des mots ce qu'il ou elle fait ?",
  "source": {
    "file": "cycle-2-cp-ce1-ce2/maths-c2-BO41-2024.pdf",
    "bo": "BO n° 41 du 31 octobre 2024",
    "page": 13,
    "sha256": "0fe8dfba39f78215e4d44f0dc871df80d7c9530267d6de40b49d205d3506caed"
  }
}
```

- `officialObjectives` est recopié mot pour mot du programme. `description`, `evidence` (critères de réussite, tirés des « exemples de réussite » officiels quand ils existent) et `assessmentPrompt` sont des reformulations.
- `type` : `CONCEPTUAL` (comprendre), `PROCEDURAL` (savoir-faire), `REPRESENTATIONAL` (passer d'une représentation à une autre), `LANGUAGE` (vocabulaire), `META` (stratégie).
- `source.sha256` est l'empreinte du PDF au moment de l'extraction : si le programme change, les notions concernées sont repérées.

Un prérequis :

```json
{
  "topicId": "fr-ma-ce1-fra-07",
  "prerequisiteId": "fr-ma-ce1-fra-02",
  "strength": "hard",
  "origin": "déduit",
  "reason": "Additionner 1/5 et 2/5 suppose de comprendre 3/5 comme trois fois 1/5."
}
```

`strength` vaut `hard` (indispensable) ou `soft` (utile). `origin` vaut `texte` quand le programme écrit lui-même le lien (492 liens), `déduit` sinon (7 510 liens). Le format complet est décrit dans [`data/README.md`](data/README.md#format).

Exemple en Python : tout ce qu'il faut savoir avant une notion.

```python
import json
from collections import defaultdict

notions = {n["id"]: n for n in json.load(open("data/notions.json"))["notions"]}
avant = defaultdict(list)
for p in json.load(open("data/prerequis.json"))["prerequisites"]:
    avant[p["topicId"]].append(p["prerequisiteId"])

def chaine(i, vus=None):
    vus = set() if vus is None else vus
    for p in avant[i]:
        if p not in vus:
            vus.add(p)
            chaine(p, vus)
    return vus

for i in sorted(chaine("fr-ma-ce1-fra-07"), key=lambda i: notions[i]["ageRangeStart"]):
    print(notions[i]["level"], notions[i]["name"])
```

## Comment la base est construite

1. **Sources** : les PDF des programmes sont téléchargés depuis education.gouv.fr et eduscol.education.gouv.fr. Leur adresse, leur BO, leur date de téléchargement et leur empreinte SHA-256 sont dans [`sources.json`](construction/programmes-officiels/sources.json).
2. **Extraction** : chaque classe de chaque programme est découpée en notions par un modèle de langage (Claude), selon des consignes publiques ([`consignes-extraction.md`](construction/outils/consignes-extraction.md)). Une puce « objectif d'apprentissage » donne en général une notion.
3. **Contrôles automatiques** : format et identifiants, graphe sans boucle (`valider.py`), toutes les puces du programme reprises (`couverture.py`), chaque objectif retrouvé mot pour mot dans le PDF (`verifier_sources.py`).
4. **Liaison** : chaque notion est reliée à ce qu'elle suppose des classes précédentes ([`consignes-liens.md`](construction/outils/consignes-liens.md)), puis les liens redondants sont retirés.
5. **Assemblage** : `assembler.py` produit le jeu de données (`data/`), ses vues et le site (`site/`), et note ce qui a changé dans [`data/JOURNAL.md`](data/JOURNAL.md).

**Traçabilité** : chaque notion garde la page et l'empreinte du PDF dont elle vient, chaque fichier sa date d'extraction ou de liaison. Un PDF n'est jamais écrasé : l'ancienne version est archivée. `python3 outils/etat.py` dit ce qu'il reste à faire après l'ajout ou la mise à jour d'un programme, et `python3 outils/verifier_sources.py --en-ligne` détecte une nouvelle version publiée. La procédure est dans [`MISE-A-JOUR.md`](construction/outils/MISE-A-JOUR.md).

## Limites

- **Seul le texte officiel fait foi.** Les descriptions, questions et critères sont des reformulations, à vérifier avant tout usage pédagogique.
- **La base n'a pas encore été relue en entier par des enseignants.** Les points à relire sont listés dans [`construction/README.md`](construction/README.md#à-relire), en particulier les 7 510 liens déduits.
- Programmes non couverts : langues et cultures de l'Antiquité, langues régionales et langues autres que les quatre principales au collège, lycée.

## Pistes

La base est une première brique. Pistes ouvertes, les contributions sont bienvenues :

- relecture par des enseignants, en commençant par les liens déduits ;
- questions reformulées sans pronom pour désigner l'enfant (environ 380 l'emploient encore) ;
- programmes manquants : langues et cultures de l'Antiquité, langues régionales, lycée ;
- correspondance avec les notions de Marble, pour relier les deux bases ;
- outils construits sur la base : mini-application d'exercices, fiches imprimables, planning de révision en séances courtes, au quotidien ou pendant les vacances, pour combler une difficulté, consolider ou aller plus loin.

## Contribuer

Les signalements d'erreur et les relectures sont les bienvenus : ouvre une *issue* en citant l'identifiant de la notion (`fr-ma-ce1-fra-07`), ce qui ne va pas, et si possible la page du programme.

Pour modifier la base, tout se lance depuis `construction/` :

```bash
python3 outils/valider.py      # contrôle les extractions
python3 outils/assembler.py    # refait ../data/ (données, vues, journal) et le site ../site/
python3 outils/etat.py         # dit ce qui reste à faire ; doit répondre « Tout est à jour »
```

Les scripts n'utilisent que la bibliothèque standard de Python 3. Préparer un nouveau PDF demande aussi `pdftotext` (Poppler) et, pour un PDF en images, la reconnaissance de texte de macOS. Le dossier [`.claude/skills/maj-programme`](.claude/skills/maj-programme/SKILL.md) contient la procédure sous forme de *skill* pour Claude Code.

## Arborescence

Le dépôt a trois parties : les données, le site qui les affiche, et la construction qui les produit.

```
data/                        le jeu de données (Licence Ouverte 2.0)
├── notions.json             les notions
├── prerequis.json           les liens de prérequis
├── vues/                    une page Markdown par programme
├── historique/              détail des changements, à chaque assemblage
└── JOURNAL.md               historique de la base
site/                        le site, la carte du curriculum (MIT)
├── index.html               page autonome, générée à partir de data/
└── modele.html              son modèle
construction/                fabrication de la base, des PDF officiels aux notions
├── programmes-officiels/    PDF officiels et manifeste sources.json (empreintes, BO, adresses)
├── textes/                  texte des PDF, page par page
├── extractions/             notions extraites (une classe d'un programme par fichier) et liens entre classes
└── outils/                  scripts, registre des programmes, consignes, procédure de mise à jour
bench/                       état des lieux des projets voisins
```

`data/` et `site/` sont générés : on ne les modifie pas à la main, on corrige les extractions puis on relance `assembler.py`.

## Projets voisins

- **[Marble, taxonomie ouverte](https://github.com/withmarbleapp/os-taxonomy)** : 1 930 notions du primaire et 4 102 prérequis, en anglais, alignés sur les programmes américains, britanniques, australiens et internationaux. Données sous ODbL, contenus sous CC BY-SA 4.0. vale.edu en reprend le format, pas les données.
- **[MathALÉA / Coopmaths](https://forge.apps.education.fr/coopmaths/mathalea)** (AGPL) : exercices de mathématiques générés aléatoirement, avec des référentiels JSON par niveau, surtout à partir du CM1.
- **Adaptiv'Math et Mathia** (programme P2IA du ministère) : parcours adaptatifs de mathématiques pour le cycle 2, gratuits, ouverts par l'enseignant, données fermées.
- **Ontologies des programmes scolaires** (data.gouv.fr) : OWL/RDF, surtout pour le secondaire et d'anciens programmes.

État des lieux plus complet, avec les projets d'enseignants de la Forge des communs numériques éducatifs et les graphes étrangers (relevé du 26/10/2026) : [`bench/`](bench/README.md).

## Licences

- **Données** (notions, liens, descriptions, questions, critères : `data/` et `construction/extractions/`) : [Licence Ouverte 2.0](LICENCE-DONNEES.md) (Etalab). Réutilisation libre, y compris commerciale, en citant « vale.edu » et l'adresse du dépôt.
- **Code** (scripts de `construction/outils/` et site `site/`) : [licence MIT](LICENSE).
- **Programmes officiels** (`construction/programmes-officiels/`, `construction/textes/` et citations dans `officialObjectives`) : informations publiques du ministère de l'Éducation nationale, réutilisables en citant leur source et leur date (articles L321-1 et L322-1 du code des relations entre le public et l'administration). Source et date de chaque document : [`sources.json`](construction/programmes-officiels/sources.json).

vale.edu est un projet indépendant, sans lien avec le ministère de l'Éducation nationale ni avec Marble.

## In English

vale.edu is an open dataset of the French national curriculum, from age 3 (petite section) to age 15 (3e): 5,604 learning concepts taken from 43 official programmes, linked by 8,002 prerequisite relations, each with its reason. Every concept quotes the official objective verbatim with the page of the source PDF. It follows the format of [Marble's open taxonomy](https://github.com/withmarbleapp/os-taxonomy) and extends it to lower secondary school. Content is in French. Data: Licence Ouverte 2.0 (compatible with CC BY 4.0). Code: MIT.
