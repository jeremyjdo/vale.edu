# Jeu de données

Le curriculum français en données : les notions des programmes officiels, de la petite section à la 3e, et les liens de prérequis entre elles. Licence : [Licence Ouverte 2.0](../LICENCE-DONNEES.md), en citant « vale.edu ».

| Fichier | Contenu |
|---|---|
| [notions.json](notions.json) | Les 5 604 notions, avec la liste des programmes (BO, PDF, empreinte, date d'extraction) |
| [prerequis.json](prerequis.json) | Les 8 002 liens de prérequis |
| [vues/](vues/index.md) | Les mêmes données en Markdown, une page par programme |
| [JOURNAL.md](JOURNAL.md) | Ce qui a changé à chaque assemblage |
| `historique/` | Le détail de chaque changement, valeurs avant et après |

Ces fichiers sont générés par `construction/outils/assembler.py` à partir des extractions (`construction/extractions/`). Pour corriger une notion, on corrige son fichier d'extraction puis on relance l'assemblage : voir [../construction/README.md](../construction/README.md).

## Format

Les noms de champs reprennent ceux de la [taxonomie de Marble](https://github.com/withmarbleapp/os-taxonomy) pour rester compatibles. Le contenu est en français.

**Une notion** (`notions.json`, tableau `notions`)

| Champ | Contenu | Origine |
|---|---|---|
| `id` | `fr-<matière>-<classe>-<thème>-NN`, ex. `fr-ma-ce2-fra-01` | — |
| `programme` | Clé du programme, ex. `maths-c2` ; détail dans l'objet `programmes` du même fichier | — |
| `subject`, `domain`, `subdomain` | Matière, domaine et intertitre du programme | texte |
| `level`, `cycle`, `ageRangeStart`, `ageRangeEnd` | Classe (`CE2`, ou `Cycle 4` quand le programme ne précise pas la classe), cycle, âges | texte |
| `officialObjectives` | Puce(s) « Objectifs d'apprentissage » couvertes, **mot pour mot** | texte |
| `evidence` | Critères de réussite, tirés des « Exemples de réussite » (condensés, rien d'inventé) | texte |
| `period` | Période de l'année quand le programme la précise | texte |
| `source` | Fichier PDF (relatif à `construction/programmes-officiels/`), BO, page, empreinte SHA-256 du PDF au moment de l'extraction, et document d'exemples Éduscol s'il a servi | texte |
| `name` | Nom court de la notion | rédigé |
| `description` | Explication simple pour un parent | rédigé |
| `type` | `CONCEPTUAL` (comprendre), `PROCEDURAL` (savoir-faire), `REPRESENTATIONAL` (représentations), `LANGUAGE` (vocabulaire), `META` (stratégie) | rédigé |
| `assessmentPrompt` | Question pour vérifier la notion, avec `{{prenom}}` à remplacer par un prénom ou « l'enfant » | rédigé |
| `priorKnowledge` | Ce que la notion suppose des classes précédentes, en texte libre | rédigé |

« texte » : repris du programme officiel ; « rédigé » : reformulé lors de l'extraction, à vérifier avant tout usage pédagogique.

**Un prérequis** (`prerequis.json`, tableau `prerequisites`) : `topicId` dépend de `prerequisiteId`.

| Champ | Contenu |
|---|---|
| `strength` | `hard` si c'est indispensable, `soft` si ça aide |
| `origin` | `texte` si le programme le dit explicitement (492 liens), `déduit` sinon (7 510 liens, à relire) |
| `reason` | Une phrase d'explication |
| `continuation` | Liens entre classes : `true` quand c'est le même savoir-faire l'année d'avant |

Le graphe est sans boucle, et les liens redondants (déjà impliqués par d'autres) sont retirés.
