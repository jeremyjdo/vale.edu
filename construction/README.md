# Construction de la base

Ce dossier contient tout ce qui sert à fabriquer la base : les programmes officiels en PDF, leur texte, les notions extraites classe par classe et les outils qui les vérifient, les relient et les assemblent. Le résultat va à la racine du dépôt : le jeu de données dans [../data/](../data/README.md), l'atlas dans [../site/](../site/README.md).

Le principe : les programmes officiels découpés en notions fines, chacune avec ses critères de réussite, reliées entre elles par des prérequis, et rattachées au texte officiel dont elles viennent.

> **Statut : première version complète (5 vagues, 23/10/2026), à relire.**

## Organisation

| Dossier | Contenu |
|---|---|
| [programmes-officiels/](programmes-officiels/README.md) | PDF des programmes, et manifeste `sources.json` : adresse, BO, date de téléchargement et empreinte SHA-256 de chaque PDF |
| [textes/](textes/) | Texte brut de chaque PDF, page par page, utilisé pour l'extraction (`.ocr.txt` pour les PDF en images) |
| [extractions/](extractions/) | Fichiers sources de la base : un par classe et par programme (`<programme>-<classe>.json`), plus les liens entre classes (`liens-<programme>.json`). Leur format est décrit dans [outils/consignes-extraction.md](outils/consignes-extraction.md) |
| [outils/](outils/) | Registre des programmes (`programmes.json`), consignes d'extraction et de liaison, procédure de mise à jour, scripts |

Toutes les commandes se lancent depuis ce dossier :

```bash
cd construction && python3 outils/valider.py && python3 outils/assembler.py && python3 outils/etat.py
```

## Avancement

| Vague | Programmes | État |
|---|---|---|
| 1-2 | Maths et français, du CP à la 3e (cycles 2, 3 et 4), avec les liens entre toutes les classes | **fait** : 1 640 notions, 3 268 prérequis |
| 3 | Questionner le monde (2020) ; histoire-géo et sciences du cycle 3 (2026) ; langues vivantes du cours moyen ; EMC du CP à la 3e | **fait** : 662 notions, 753 prérequis |
| 4 | Histoire-géo, sciences et langues du cycle 2 (2026) ; EPS cycles 2 et 3 ; vie affective (EVAR/EVARS), de la maternelle à la 3e | **fait** : 605 notions, 671 prérequis |
| 5 | Maternelle (six domaines) ; arts plastiques, éducation musicale et histoire des arts (cycles 2 à 4, 2020) ; histoire-géo, physique-chimie, SVT, EPS et EMI du cycle 4 (2020) ; technologie (2024) ; anglais, espagnol, allemand et italien au collège (2025) | **fait** : 2 697 notions, 3 310 prérequis |

Total : 43 programmes, 5 604 notions, 8 042 prérequis, de la petite section à la 3e. Les programmes de l'élémentaire ont été extraits en premier, puis la maternelle et le collège.

Les programmes de maths et de français du cycle 3 ont des exemples de réussite publiés à part par Éduscol, utilisés pour les critères. Ceux du cycle 4 n'en ont pas : leurs critères et leurs questions sont rédigés à partir des objectifs, et c'est indiqué dans la vue de chaque notion.

Les parties des programmes de 2020 déjà remplacées par un nouveau programme (français, maths, histoire-géo, EPS, langues, sciences là où un texte de 2024-2026 existe) ne sont pas extraites, pas plus que le programme de sciences de 2023 ni la technologie de 2020. Les langues et cultures de l'Antiquité ne le sont pas non plus : leur programme n'est pas dans le PDF du cycle 4. Seules quatre langues du collège sont extraites (anglais, espagnol, allemand, italien).

## Méthode

1. **Préparation** : `outils/preparer_pdf.py` enregistre le PDF dans le manifeste et prépare son texte (`textes/`), avec reconnaissance de texte si le PDF est en images.
2. **Extraction** : une sous-tâche par classe et par programme suit [outils/consignes-extraction.md](outils/consignes-extraction.md). Chaque puce « Objectifs d'apprentissage » devient une notion avec ses « Exemples de réussite ». Les prérequis sont posés à l'intérieur de la classe. `outils/estampiller.py` ajoute à chaque notion l'empreinte du PDF et la date d'extraction.
3. **Vérification** : `outils/valider.py` contrôle le format, les identifiants, la traçabilité et l'absence de boucle ; `outils/couverture.py` vérifie que toutes les puces du programme sont reprises.
4. **Liaison** : une sous-tâche par programme relie chaque notion à ce qu'elle suppose des classes précédentes, y compris du cycle d'avant ([outils/consignes-liens.md](outils/consignes-liens.md)). `outils/elaguer_liens.py` retire ensuite les liens redondants.
5. **Assemblage** : `outils/assembler.py` produit le jeu de données `../data/` (programmes, objectifs officiels, notions et liens, avec les vues et le journal) et l'atlas `../site/index.html` (`outils/construire_site.py`, modèle `../site/modele.html`). Les changements sont notés dans [../data/JOURNAL.md](../data/JOURNAL.md).

Le format des données est décrit dans [../data/README.md](../data/README.md#format).

## Traçabilité et mise à jour

Pour ajouter un programme ou une nouvelle version d'un programme : [outils/MISE-A-JOUR.md](outils/MISE-A-JOUR.md). Dans Claude Code, le skill `maj-programme` (dans `.claude/skills/` à la racine du dépôt) applique cette procédure.

- **Chaque PDF** est enregistré dans [programmes-officiels/sources.json](programmes-officiels/sources.json) avec son adresse, son BO, sa date de téléchargement et son empreinte SHA-256. Une version remplacée est archivée dans `programmes-officiels/archives/` et reste listée dans `anciennesVersions`.
- **Chaque notion** pointe vers son PDF (`source.fichier`), sa référence BO (`source.bo`), sa page (`source.page`) et, quand il a servi, vers le document d'exemples Éduscol (`source.exemples`, `source.exemplesPage`). Elle porte l'empreinte du PDF au moment de son extraction (`source.sha256`) et recopie mot pour mot l'objectif officiel (`objectifsOfficiels`). Chaque fichier d'extraction porte sa date (`extraitLe`).
- **Chaque fichier de liens** porte sa date (`relieLe`) et la date d'extraction des programmes qu'il relie (`versionsCibles`). Si l'un d'eux est ré-extrait, la liaison est signalée comme à refaire.
- **Chaque assemblage** est comparé au précédent : les notions et liens ajoutés, retirés ou modifiés sont résumés dans [../data/JOURNAL.md](../data/JOURNAL.md), avec le détail dans `../data/historique/`.
- **`python3 outils/etat.py`** fait le bilan : PDF nouveaux ou modifiés, programmes à extraire ou à ré-extraire, liaisons à refaire, liens cassés, assemblage ou atlas en retard. Il donne la liste des actions à faire. `python3 outils/etat.py --programme <clé>` montre l'impact d'une ré-extraction.
- **`python3 outils/verifier_sources.py --en-ligne`** retélécharge chaque PDF pour détecter une nouvelle version publiée. Il vérifie aussi que l'objectif de chaque notion se retrouve dans son PDF.

Pour un PDF publié en images, le texte est reconnu par OCR (`outils/ocr_pdf.py`, avec la reconnaissance de texte de macOS) et enregistré dans `textes/<nom>.ocr.txt`, que le script de vérification lit à la place du texte du PDF. C'était le cas des deux programmes de sciences de 2026 jusqu'au 27/10/2026. Le ministère les a republiés avec un vrai texte : ils ont alors été remplacés, ré-extraits (mêmes notions, mêmes id) et reliés de nouveau.

État au 27/10/2026 : 34 PDF sur 34 conformes au manifeste. Les objectifs de toutes les notions sont retrouvés dans leur PDF, avec ces exceptions connues :
- 61 notions d'EMC, dont l'objectif commence par une étiquette « Notion(s) abordée(s) : » ajoutée pendant l'extraction ;
- quelques puces de maths, coupées par la mise en page en deux colonnes ;
- une notion d'histoire-géo et deux de langues vivantes, dont la puce est coupée entre deux pages ;
- en sciences au cycle 3, 4 puces coupées par la mise en page en deux colonnes ou par un changement de page. Toutes les notions de sciences du cycle 2 sont retrouvées.

## À relire

- Les prérequis « déduits » sont des propositions plausibles, qu'aucun enseignant n'a validées.
- Quelques notions viennent d'attentes écrites hors des tableaux (rapidité en calcul mental, démarche de résolution de problèmes) : leur `objectifsOfficiels` cite alors une phrase du texte.
- Quand le programme ne donne pas d'exemple pour une puce, les critères sont reformulés à partir de la puce elle-même.
- Vie affective (EVAR/EVARS) : les critères viennent des « propositions de démarches et d'activités », que le texte dit non prescriptives. Quelques définitions courtes destinées aux parents ont été ajoutées (intersexe, PrEP/TPE, emprise, stéréotype…) et sont à relire. En maternelle, le texte parle de paliers d'âge, rattachés ici à PS, MS et GS.
- Environ 380 questions des vagues 1 à 4 (`question`) reprennent l'enfant par « il » (« quand il lit… »). C'est correct dans les vues, où `{{prenom}}` devient « l'enfant », mais pas quand une application le remplace par un prénom de fille : à reformuler sans pronom.
- Programmes rédigés par cycle (arts, technologie, physique-chimie, SVT, EPS et EMI du collège) : la plupart des notions sont au niveau `Cycle 2`, `Cycle 3` ou `Cycle 4`, faute de repère qui les place dans une classe.
- Maternelle : le programme donne des repères d'âge (« avant 4 ans », « à partir de 4 ans », « à partir de 5 ans »), rattachés ici à PS, MS et GS. Le repère exact est dans `periode`.
- Collège (programmes de 2020) : quand le texte dit « dans la continuité du cycle 3 », il vise l'ancien cycle 3. Les liens vers le cycle 3 de 2026 sont donc presque tous « déduits ».
- Langues du collège : les liens de 6e vers le CM2 portent sur des compétences, car la langue étudiée au CM2 n'est pas forcément la même.
- Quelques descriptions et questions contiennent des précisions ou des valeurs absentes du texte officiel (en SVT et en physique-chimie, par exemple « les antibiotiques n'agissent pas sur les virus », 340 m/s) : à relire. En allemand et en italien, des coquilles du BO sont gardées dans `objectifsOfficiels` mais corrigées dans les critères.
- Quelques liens marqués « texte » s'appuient sur une phrase générale du programme (« prend appui sur les acquis du cycle 1 », « découverte au CE2 ») plutôt que sur une notion précise.
