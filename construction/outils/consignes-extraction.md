# Consignes d'extraction des notions

Ces consignes s'appliquent à toute extraction d'une classe d'un programme. Les paramètres (programme, classe, fichier de sortie) sont donnés dans la demande.

Dossier de travail : `construction/` dans le dépôt. Les commandes se lancent depuis ce dossier.

## Entrées (lecture seule)

- Registre des programmes : `construction/outils/programmes.json` (matière, code, fichier PDF, BO, classes).
- Texte du programme : `construction/textes/<nom du PDF>.txt`, issu de `pdftotext -layout`. Les marqueurs `=== PAGE n ===` donnent la page du PDF. Le texte contient toutes les classes du cycle : ne traite **que la classe demandée**, mais lis aussi les « Principes » et les introductions générales, utiles pour le contexte.
- PDF source : `construction/programmes-officiels/<file du registre>`.
- **Exemples de réussite publiés à part** : pour le français et les maths du cycle 3, le BO ne contient que les objectifs ; les exemples sont dans `construction/textes/exemples-reussite-<maths|francais>-<cm1|cm2|6e>-2025.txt` (PDF dans `programmes-officiels/cycle-3-cm1-cm2-6e/exemples-reussite/`). Tire alors les critères de ces exemples. `objectifsOfficiels` et `source.page` restent ceux du BO ; ajoute dans `source` les champs `exemples` (chemin du PDF d'exemples, relatif à `programmes-officiels/`) et `exemplesPage`.

Les tableaux ont deux colonnes côte à côte : « Objectifs d'apprentissage » (puces « - » à gauche) et « Exemples de réussite » (à droite), entrelacées ligne par ligne. Reconstitue soigneusement quelle puce va avec quels exemples. En cas de doute, commence par `pdftotext -f N -l N -raw <pdf> -`, qui est peu coûteux. Ne lis la page en image (outil Read avec `pages`) que si c'est vraiment nécessaire.

## Sortie

Écris UNIQUEMENT le fichier de sortie indiqué dans la demande, puis lance :

```
python3 outils/estampiller.py <ton fichier> && python3 outils/valider.py <ton fichier> && python3 outils/couverture.py textes/<texte>.txt <ton fichier>
```

Tes scripts de travail vont dans un sous-dossier à ton nom (par exemple `<scratchpad>/<programme>/`), jamais à la racine du scratchpad : d'autres extractions tournent en même temps.

`estampiller.py` ajoute à chaque notion l'empreinte du PDF dont elle vient, et la date d'extraction au fichier : ne les écris pas toi-même. Si tu régénères ton fichier, relance-le avant `valider.py`.

Corrige jusqu'à ce que `valider.py` réponde « OK ». `couverture.py` signale les puces non retrouvées, mais il travaille sur toutes les classes du texte : seules les puces de ta classe te concernent. Quand le texte contient plusieurs programmes (la maternelle, par exemple), ajoute `--pages <début>-<fin>` pour ne compter que tes pages. Il se trompe aussi parfois quand la mise en page colle les deux colonnes ; vérifie ces cas à la main. Ne crée ni ne modifie aucun autre fichier.

Format :

```json
{
  "programme": "<clé du registre>",
  "classe": "<classe>",
  "codesThemes": {"num": "Les nombres entiers", "...": "..."},
  "notions": [
    {
      "id": "fr-<code>-<classe>-<thème>-NN",
      "programme": "<clé du registre>",
      "nature": "savoir-faire",
      "matiere": "<matière du registre>",
      "domaine": "Grande partie du programme (intertitre de premier niveau)",
      "sousDomaine": "Intertitre de la partie",
      "classe": "<classe>",
      "cycle": 3,
      "nom": "Nom court de la notion (≤ 80 caractères)",
      "description": "1 à 2 phrases simples pour un parent.",
      "objectifsOfficiels": ["Texte exact de la ou des puces « Objectifs d'apprentissage » couvertes"],
      "criteres": ["Critère observable tiré des « Exemples de réussite »"],
      "periode": "période 2",
      "question": "Est-ce que {{prenom}} sait ... ? (avec un exemple concret du texte)",
      "acquisAnterieurs": ["Ce qui est requis d'une classe antérieure, avec la classe entre parenthèses"],
      "source": {"fichier": "<file du registre>", "bo": "<bo du registre>", "page": 12}
    }
  ],
  "liens": [
    {"de": "<notion prérequise>", "vers": "<notion qui en dépend>", "type": "prerequis",
     "force": "indispensable", "origine": "déduit", "raison": "Raison courte"}
  ]
}
```

`periode` et `acquisAnterieurs` sont facultatifs. `valider.py` refuse tout autre champ.

**Classes, cycles et slug d'id :**

| Classe | Slug | Cycle |
|---|---|---|
| PS, MS, GS | ps, ms, gs | 1 |
| CP, CE1, CE2 | cp, ce1, ce2 | 2 |
| CM1, CM2, 6e | cm1, cm2, 6e | 3 |
| 5e, 4e, 3e | 5e, 4e, 3e | 4 |

## Règles

1. **Granularité** : une notion = une idée enseignable et évaluable seule. En général une puce d'objectif = une notion. Regroupe plusieurs puces seulement si elles sont indissociables et partagent les mêmes exemples. Découpe une puce si elle couvre des savoir-faire nettement distincts ; la même puce figure alors dans chaque notion issue du découpage.
2. **Couverture et fidélité** : chaque puce d'objectif de ta classe doit apparaître mot pour mot dans `objectifsOfficiels` d'au moins une notion. N'invente aucune notion absente du texte. Une attente importante écrite hors tableau (fluence, champ numérique, nombre de mots lus par minute, périodes, limites) va dans la description ou les critères des notions concernées. Elle ne devient une notion à part que si elle n'a aucune puce correspondante ; cite alors la phrase exacte dans `objectifsOfficiels`.
3. **criteres** : 1 à 6 critères, tirés des « Exemples de réussite ». Garde les nombres, les exemples et les objectifs chiffrés. Tu peux condenser, pas inventer. Formule au présent, en commençant par un verbe (« Complète… », « Lit… »), sans « L'élève sait ».
4. **description** : langage simple pour un parent, sans jargon (ou jargon expliqué).
5. **nature** : `compréhension` (comprendre une idée), `savoir-faire` (technique, procédure), `représentation` (passer d'une représentation à une autre : schémas, tableaux, graphiques, cartes), `vocabulaire` (vocabulaire, notions de langue et expressions propres à la matière), `stratégie` (stratégies, vérification, réflexion sur sa démarche).
6. **id** : `fr-<code du registre>-<slug de la classe>-<thème>-NN`. Le thème est un code de 2 à 5 lettres minuscules par intertitre, déclaré dans `codesThemes`. Numérote à partir de 01 par thème, dans l'ordre de lecture.
7. **domaine / sousDomaine** : intertitres du programme, tels qu'écrits.
8. **liens** : seulement entre notions de TON fichier. Un lien va de la notion prérequise (`de`) vers la notion qui en dépend (`vers`), avec `"type": "prerequis"`. `origine` = « texte » si le programme le dit explicitement, « déduit » sinon. `force` = « indispensable » (impossible sans) ou « utile » (aide). Pas de liens redondants par transitivité. En général 0 à 3 par notion. Le graphe doit être sans boucle.
9. **acquisAnterieurs** : ce qui vient des classes précédentes (ou d'un cycle précédent) et dont la notion dépend, de façon précise : la notion et la classe. Ces textes servent ensuite à créer les liens entre classes.
10. **Ré-extraction** : si une extraction précédente du programme existe dans `extractions/archives/`, garde l'`id` de chaque notion dont l'objectif officiel est inchangé, pour que les liens des autres programmes restent valides. Une notion nouvelle prend un numéro libre. Ne redonne jamais l'`id` d'une notion supprimée à une autre notion. Indique dans le rapport les notions ajoutées, retirées et modifiées.
11. **Valable pour tout enfant** : la base est générique et pourra être publiée. N'emploie aucun pronom pour désigner l'enfant (ni « il », ni « elle », ni « lui-même ») : `{{prenom}}` peut être remplacé par n'importe quel prénom. Répète `{{prenom}}` ou tourne la phrase autrement (« en lisant », « au moment de lire »). Exemple : « quand {{prenom}} lit à voix haute », et non « quand il lit ». Les pronoms qui renvoient à autre chose restent permis (« il faut », « il y a »).

## Rapport final (15 lignes max)

Nombre de notions par domaine, nombre de prérequis, résultat de la couverture, et les points de doute (alignements difficiles, puces sans exemple, découpages ou regroupements discutables).
