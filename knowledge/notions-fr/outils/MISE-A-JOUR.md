# Ajouter ou mettre à jour un programme

Procédure à suivre quand un programme officiel change ou qu'un nouveau programme est publié. Chaque étape laisse une trace : on peut toujours savoir de quelle version d'un PDF vient une notion, quand elle a été extraite, et ce qui a changé d'une version de la base à l'autre.

Toutes les commandes se lancent depuis `knowledge/notions-fr/`.

## Ce qui est tracé

| Élément | Où | Ce qui est enregistré |
|---|---|---|
| PDF officiel | `../programmes-officiels/sources.json` | Adresse, BO, date de téléchargement, SHA-256, taille, pages. Les versions remplacées sont listées dans `anciennesVersions`, avec leur fichier archivé dans `../programmes-officiels/archives/` |
| Texte du PDF | `textes/<nom>.txt` (et `.ocr.txt` pour un PDF en images) | Texte page par page. Les anciennes versions vont dans `textes/archives/` |
| Programme | `outils/programmes.json` | PDF, BO, classes, programme précédent (`follows`), programmes qu'il remplace (`remplace`) |
| Notion | `extractions/<programme>.json` | PDF, BO, page, **empreinte du PDF au moment de l'extraction** (`source.sha256`), objectif officiel mot pour mot. Le fichier porte sa date d'extraction (`extractedAt`) |
| Lien entre notions | `extractions/liens-*.json` | Date de la liaison (`linkedAt`) et date d'extraction de chaque programme relié (`versionsCibles`) |
| Base assemblée | `data/`, `JOURNAL.md`, `data/historique/` | Pour chaque programme : empreinte et date d'extraction. À chaque assemblage : notions et prérequis ajoutés, retirés ou modifiés, avec les valeurs avant et après |

`python3 outils/etat.py` compare tout cela et donne la liste des actions à faire. Quand il répond « Tout est à jour », la base est cohérente.

## 1. Savoir si un programme a changé

```bash
python3 outils/verifier_sources.py --en-ligne
```

Le script retélécharge chaque PDF du manifeste. Une « NOUVELLE VERSION » est enregistrée à part (jamais à la place de l'ancienne), avec la commande pour l'adopter et la liste des notions dont le texte n'y figure plus. Pour un nouveau programme (nouveau BO), il faut surveiller les pages Éduscol des cycles, listées en tête de `../programmes-officiels/README.md`.

## 2. Nouvelle version d'un programme déjà extrait

1. **Enregistrer le PDF** (l'ancien est archivé, rien n'est écrasé) :
   ```bash
   python3 outils/preparer_pdf.py <chemin dans programmes-officiels> --depuis <nouveau.pdf> --bo "BO n° …"
   ```
2. **Mesurer l'impact** : `python3 outils/etat.py` signale « Ré-extraire <programme> ». `python3 outils/etat.py --programme <clé>` liste les fichiers d'extraction, les liens d'autres programmes qui pointent vers ses notions et les programmes qui lui font suite.
3. **Archiver l'ancienne extraction** (chaque fichier listé par `etat.py --programme`) :
   ```bash
   mkdir -p extractions/archives && mv extractions/<fichier>.json extractions/archives/<fichier>-<extractedAt>.json
   ```
4. **Ré-extraire** avec les consignes (`outils/consignes-extraction.md`, modèle de demande ci-dessous). La règle 10 garde les mêmes `id` pour les notions inchangées, ce qui préserve les liens des autres programmes.
5. **Refaire les liaisons** listées par `etat.py` : celles du programme vers ses prédécesseurs, et celles des autres programmes vers lui (`outils/consignes-liens.md`). `valider.py` signale tout lien vers une notion disparue.
6. **Assembler et vérifier** :
   ```bash
   python3 outils/valider.py && python3 outils/assembler.py && python3 outils/verifier_sources.py && python3 outils/etat.py
   ```
   `assembler.py` ajoute une entrée à `JOURNAL.md` avec le détail des changements, et reconstruit la page de consultation `site/index.html`.
7. **Mettre à jour les README** : le tableau des textes en vigueur dans `../programmes-officiels/README.md`, et l'avancement dans `README.md`.

## 3. Nouveau programme

1. **Télécharger le PDF** dans le dossier de son cycle, nommé `<matière>-<cycle>-BO<n°>-<année>.pdf`, puis l'enregistrer :
   ```bash
   python3 outils/preparer_pdf.py <chemin dans programmes-officiels> --url <adresse> --bo "BO n° … du …"
   ```
   Le texte est préparé automatiquement, avec reconnaissance de texte si le PDF est en images.
2. **L'inscrire au registre** `outils/programmes.json` :

   | Champ | Contenu |
   |---|---|
   | clé | `<matière>-c<cycle>`, ex. `hg-c4` |
   | `subject` | Nom de la matière |
   | `code` | 2 à 5 lettres, utilisé dans les `id` (`fr-<code>-<classe>-…`). Il doit rester unique pour chaque classe |
   | `file`, `bo` | Chemin du PDF et BO, comme dans le manifeste |
   | `levels` | Classes couvertes, plus `Cycle N` si des notions valent pour tout le cycle |
   | `follows` | Programme de la même matière au cycle précédent |
   | `remplace` | Programmes qu'il remplace, même en partie ou progressivement |
   | `examples`, `format` | `aucun` s'il n'y a pas d'exemples de réussite ; `ancien`, `image`… si le format diffère (voir `consignes-autres-formats.md`) |

   Si le nouveau programme précède un programme existant, mets à jour le `follows` de celui-ci. Si sa matière est nouvelle, ajoute-la à la bonne famille dans `FAMILLES` (`outils/construire_site.py`) : sinon elle forme sa propre bande sur la carte de la page de consultation.
3. **Extraire**, puis **relier** au programme précédent et aux programmes qui lui font suite (étapes 4 à 7 ci-dessus). `etat.py` liste ce qui manque.
4. **Programme remplacé** : tant qu'il s'applique encore à une classe, il reste dans la base, avec la mention « remplacé progressivement par… » dans sa vue. Quand il ne s'applique plus nulle part, archive son extraction (étape 3 de la partie 2), retire-le du registre, puis refais les liaisons qui pointaient vers lui (`etat.py` les signale comme liens cassés).

## Modèles de demande

Une extraction ou une liaison se fait avec un agent (sous-tâche) par classe ou par programme. Six au plus à la fois. Chaque agent écrit ses scripts dans son propre sous-dossier du dossier de travail temporaire.

**Extraction**

> Tu extrais les notions d'un programme officiel français pour une base de connaissances générique (format inspiré de la taxonomie Marble). Dossier de travail : `knowledge/notions-fr/`. Lis d'abord `outils/consignes-extraction.md` (et `outils/consignes-autres-formats.md` si le programme n'a pas de tableaux « Objectifs d'apprentissage / Exemples de réussite »).
> Programme : `<clé>` du registre, `<matière>` (<classes>), <BO>. Texte : `textes/<nom>.txt`, pages <a> à <b>. Sortie : `extractions/<fichier>.json` (`"level": "multiple"` si le fichier couvre plusieurs classes).
> [Ré-extraction : l'ancienne extraction est dans `extractions/archives/<fichier>` ; applique la règle 10.]
> `priorKnowledge` : renvoie aux notions de `<programme précédent>` (`extractions/<fichier>.json`).
> Ne crée ni ne modifie aucun autre fichier du projet. Rapport final en français, comme indiqué dans les consignes.

**Liaison**

> Tu relies les notions de `<programme>` à celles de `<programme précédent>`. Dossier de travail : `knowledge/notions-fr/`. Lis et applique `outils/consignes-liens.md`. Notions de départ : `extractions/<fichier>.json` (<classe>). Notions visées : `extractions/<fichier>.json` (<classe>). Écris uniquement `extractions/liens-<programme>.json`, puis lance `elaguer_liens.py`, `estampiller.py` et `valider.py` sur ce fichier et sur les fichiers des programmes reliés. Rapport final en français, 10 lignes au plus.

Après des liaisons faites en parallèle, relance `elaguer_liens.py` sur tous les fichiers de liens, puis `valider.py` sans argument.
