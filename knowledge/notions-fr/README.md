# Notions des programmes officiels français

Équivalent français de la [taxonomie ouverte de Marble](https://github.com/withmarbleapp/os-taxonomy) : les programmes officiels ([../programmes-officiels/](../programmes-officiels/README.md)) découpés en notions fines, chacune avec ses critères de réussite, et reliées entre elles par des prérequis.

> **Statut : première version complète (5 vagues, 23/10/2026), à relire.** Pour consulter les notions, ouvre [site/index.html](site/index.html) dans un navigateur : carte de toutes les notions, recherche, fiche de chaque notion avec ses prérequis et le lien vers la page du PDF officiel. Versions texte : [vues/index.md](vues/index.md).

## Organisation

| Dossier | Contenu |
|---|---|
| [site/](site/index.html) | **Page de consultation** (`index.html`, autonome, s'ouvre sans serveur), générée automatiquement |
| [vues/](vues/index.md) | **Versions lisibles**, une par programme, générées automatiquement |
| [data/](data/) | Jeu de données assemblé : `notions.json` et `prerequis.json` (tous programmes) |
| [extractions/](extractions/) | Fichiers source, un par classe et par programme (`<programme>-<classe>.json`), plus les liens entre classes (`liens-<programme>.json`) |
| [textes/](textes/) | Texte brut de chaque PDF, page par page, utilisé pour l'extraction |
| [outils/](outils/) | Registre des programmes, consignes d'extraction et de liaison, procédure de mise à jour, scripts |
| [JOURNAL.md](JOURNAL.md) | Historique des modifications de la base (détail dans `data/historique/`) |

## Avancement

| Vague | Programmes | État |
|---|---|---|
| 1-2 | Maths et français, du CP à la 3e (cycles 2, 3 et 4), avec les liens entre toutes les classes | **fait** : 1 640 notions, 3 268 prérequis |
| 3 | Questionner le monde (2020) ; histoire-géo et sciences du cycle 3 (2026) ; langues vivantes du cours moyen ; EMC du CP à la 3e | **fait** : 662 notions, 753 prérequis |
| 4 | Histoire-géo, sciences et langues du cycle 2 (2026) ; EPS cycles 2 et 3 ; vie affective (EVAR/EVARS), de la maternelle à la 3e | **fait** : 605 notions, 671 prérequis |
| 5 | Maternelle (six domaines) ; arts plastiques, éducation musicale et histoire des arts (cycles 2 à 4, 2020) ; histoire-géo, physique-chimie, SVT, EPS et EMI du cycle 4 (2020) ; technologie (2024) ; anglais, espagnol, allemand et italien au collège (2025) | **fait** : 2 697 notions, 3 310 prérequis |

Total : 43 programmes, 5 604 notions, 8 002 prérequis, de la petite section à la 3e. Les programmes de l'élémentaire ont été extraits en premier, puis la maternelle et le collège.

Les programmes de maths et de français du cycle 3 ont des exemples de réussite publiés à part par Éduscol, utilisés pour les critères. Ceux du cycle 4 n'en ont pas : leurs critères et leurs questions sont rédigés à partir des objectifs, et c'est indiqué dans la vue de chaque notion.

Les parties des programmes de 2020 déjà remplacées par un nouveau programme (français, maths, histoire-géo, EPS, langues, sciences là où un texte de 2024-2026 existe) ne sont pas extraites, pas plus que le programme de sciences de 2023 ni la technologie de 2020. Les langues et cultures de l'Antiquité ne le sont pas non plus : leur programme n'est pas dans le PDF du cycle 4. Seules quatre langues du collège sont extraites (anglais, espagnol, allemand, italien).

## Format

Les noms de champs reprennent ceux de Marble pour rester compatibles. Le contenu est en français.

**Une notion**

| Champ | Contenu | Origine |
|---|---|---|
| `id` | `fr-<matière>-<classe>-<thème>-NN`, ex. `fr-ma-ce2-fra-01` | — |
| `programme` | Clé du registre `outils/programmes.json`, ex. `maths-c2` | — |
| `subject`, `domain`, `subdomain` | Matière, domaine et intertitre du programme | texte |
| `level`, `cycle`, `ageRangeStart`, `ageRangeEnd` | Classe, cycle, âges | texte |
| `officialObjectives` | Puce(s) « Objectifs d'apprentissage » couvertes, **mot pour mot** | texte |
| `evidence` | Critères de réussite, tirés des « Exemples de réussite » (condensés, rien d'inventé) | texte |
| `period` | Période de l'année quand le programme la précise | texte |
| `source` | Fichier, BO et page du PDF | texte |
| `name` | Nom court de la notion | rédigé |
| `description` | Explication simple pour un parent | rédigé |
| `type` | CONCEPTUAL (comprendre), PROCEDURAL (savoir-faire), REPRESENTATIONAL (représentations), LANGUAGE (vocabulaire), META (stratégie) | rédigé |
| `assessmentPrompt` | Question pour vérifier la notion, avec `{{prenom}}` | rédigé |
| `priorKnowledge` | Ce que la notion suppose des classes précédentes, en texte libre | rédigé |

**Un prérequis** : `topicId` dépend de `prerequisiteId`.
- `strength` : `hard` si c'est indispensable, `soft` si ça aide.
- `origin` : `texte` si le programme le dit explicitement, `déduit` sinon.
- `reason` : une phrase d'explication.
- `continuation` (liens entre classes) : `true` quand c'est le même savoir-faire l'année d'avant.

## Méthode

1. **Préparation** : `outils/preparer_pdf.py` enregistre le PDF dans le manifeste et prépare son texte (`textes/`), avec reconnaissance de texte si le PDF est en images.
2. **Extraction** : une sous-tâche par classe et par programme suit [outils/consignes-extraction.md](outils/consignes-extraction.md). Chaque puce « Objectifs d'apprentissage » devient une notion avec ses « Exemples de réussite ». Les prérequis sont posés à l'intérieur de la classe. `outils/estampiller.py` ajoute à chaque notion l'empreinte du PDF et la date d'extraction.
3. **Vérification** : `outils/valider.py` contrôle le format, les identifiants, la traçabilité et l'absence de boucle ; `outils/couverture.py` vérifie que toutes les puces du programme sont reprises.
4. **Liaison** : une sous-tâche par programme relie chaque notion à ce qu'elle suppose des classes précédentes, y compris du cycle d'avant ([outils/consignes-liens.md](outils/consignes-liens.md)). `outils/elaguer_liens.py` retire ensuite les liens redondants.
5. **Assemblage** : `outils/assembler.py` produit `data/`, `vues/` et la page `site/index.html` (`outils/construire_site.py`, modèle `outils/modele_site.html`), et note les changements dans [JOURNAL.md](JOURNAL.md).

```bash
cd knowledge/notions-fr && python3 outils/valider.py && python3 outils/assembler.py && python3 outils/etat.py
```

## Traçabilité et mise à jour

Pour ajouter un programme ou une nouvelle version d'un programme : [outils/MISE-A-JOUR.md](outils/MISE-A-JOUR.md). Dans Claude Code, le skill `maj-programme` (dans `knowledge/.claude/skills/`) applique cette procédure.

- **Chaque PDF** est enregistré dans [../programmes-officiels/sources.json](../programmes-officiels/sources.json) avec son adresse, son BO, sa date de téléchargement et son empreinte SHA-256. Une version remplacée est archivée dans `../programmes-officiels/archives/` et reste listée dans `anciennesVersions`.
- **Chaque notion** pointe vers son PDF (`source.file`), sa référence BO (`source.bo`), sa page (`source.page`) et, quand il a servi, vers le document d'exemples Éduscol (`source.examples`, `source.examplesPage`). Elle porte l'empreinte du PDF au moment de son extraction (`source.sha256`) et recopie mot pour mot l'objectif officiel (`officialObjectives`). Chaque fichier d'extraction porte sa date (`extractedAt`).
- **Chaque fichier de liens** porte sa date (`linkedAt`) et la date d'extraction des programmes qu'il relie (`versionsCibles`). Si l'un d'eux est ré-extrait, la liaison est signalée comme à refaire.
- **Chaque assemblage** est comparé au précédent : les notions et prérequis ajoutés, retirés ou modifiés sont résumés dans [JOURNAL.md](JOURNAL.md), avec le détail dans `data/historique/`.
- **`python3 outils/etat.py`** fait le bilan : PDF nouveaux ou modifiés, programmes à extraire ou à ré-extraire, liaisons à refaire, liens cassés, assemblage en retard. Il donne la liste des actions à faire. `python3 outils/etat.py --programme <clé>` montre l'impact d'une ré-extraction.
- **`python3 outils/verifier_sources.py --en-ligne`** retélécharge chaque PDF pour détecter une nouvelle version publiée. Il vérifie aussi que l'objectif de chaque notion se retrouve dans son PDF.

Les deux programmes de sciences de 2026 (cycles 2 et 3) sont publiés en images. Leur texte est reconnu par OCR (`outils/ocr_pdf.py`, avec la reconnaissance de texte de macOS) et enregistré dans `textes/<nom>.ocr.txt`. Le script de vérification s'en sert à la place du texte du PDF.

État au 26/10/2026 : 34 PDF sur 34 conformes au manifeste. Les objectifs de toutes les notions sont retrouvés dans leur PDF, avec ces exceptions connues :
- 61 notions d'EMC, dont l'objectif commence par une étiquette « Notion(s) abordée(s) : » ajoutée pendant l'extraction ;
- quelques puces de maths, coupées par la mise en page en deux colonnes ;
- une notion d'histoire-géo et deux de langues vivantes, dont la puce est coupée entre deux pages ;
- en sciences, 2 puces coupées entre deux pages et 2 passages mal lus par l'OCR (au CE1, « Mesurer les masses des objets avec une balance… »). Ces deux passages ont été recopiés depuis l'image.

## À relire

- Les prérequis « déduits » sont des propositions plausibles, qu'aucun enseignant n'a validées.
- Quelques notions viennent d'attentes écrites hors des tableaux (rapidité en calcul mental, démarche de résolution de problèmes) : leur `officialObjectives` cite alors une phrase du texte.
- Quand le programme ne donne pas d'exemple pour une puce, les critères sont reformulés à partir de la puce elle-même.
- Vie affective (EVAR/EVARS) : les critères viennent des « propositions de démarches et d'activités », que le texte dit non prescriptives. Quelques définitions courtes destinées aux parents ont été ajoutées (intersexe, PrEP/TPE, emprise, stéréotype…) et sont à relire. En maternelle, le texte parle de paliers d'âge, rattachés ici à PS, MS et GS.
- Environ 380 questions des vagues 1 à 4 (`assessmentPrompt`) reprennent l'enfant par « il » (« quand il lit… »). C'est correct dans les vues, où `{{prenom}}` devient « l'enfant », mais pas quand une application le remplace par un prénom de fille : à reformuler sans pronom.
- Programmes rédigés par cycle (arts, technologie, physique-chimie, SVT, EPS et EMI du collège) : la plupart des notions sont au niveau `Cycle 2`, `Cycle 3` ou `Cycle 4`, faute de repère qui les place dans une classe.
- Maternelle : le programme donne des repères d'âge (« avant 4 ans », « à partir de 4 ans », « à partir de 5 ans »), rattachés ici à PS, MS et GS. Le repère exact est dans `period`.
- Collège (programmes de 2020) : quand le texte dit « dans la continuité du cycle 3 », il vise l'ancien cycle 3. Les liens vers le cycle 3 de 2026 sont donc presque tous « déduits ».
- Langues du collège : les liens de 6e vers le CM2 portent sur des compétences, car la langue étudiée au CM2 n'est pas forcément la même.
- Quelques descriptions et questions contiennent des précisions ou des valeurs absentes du texte officiel (en SVT et en physique-chimie, par exemple « les antibiotiques n'agissent pas sur les virus », 340 m/s) : à relire. En allemand et en italien, des coquilles du BO sont gardées dans `officialObjectives` mais corrigées dans les critères.
- Quelques liens marqués « texte » s'appuient sur une phrase générale du programme (« prend appui sur les acquis du cycle 1 », « découverte au CE2 ») plutôt que sur une notion précise.
