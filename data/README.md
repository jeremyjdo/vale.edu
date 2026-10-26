# Jeu de données

Le curriculum français en données : les objectifs des programmes officiels, de la petite section à la 3e, les notions qui en sont tirées et les liens de prérequis entre elles. Licence : [Licence Ouverte 2.0](../LICENCE-DONNEES.md), en citant « vale.edu ».

| Fichier | Contenu |
|---|---|
| [programmes.json](programmes.json) | Les 43 programmes officiels : matière, classes, PDF, adresse, BO, empreinte, date d'extraction |
| [objectifs.json](objectifs.json) | Les 6 798 objectifs officiels, **mot pour mot**, avec leur place dans le programme et leur source |
| [notions.json](notions.json) | Les 5 604 notions, chacune reliée aux objectifs dont elle vient |
| [liens.json](liens.json) | Les 8 042 liens de prérequis entre notions |
| [vues/](vues/index.md) | Les mêmes données en Markdown, une page par programme |
| [JOURNAL.md](JOURNAL.md) | Ce qui a changé à chaque assemblage |
| `historique/` | Le détail de chaque changement, valeurs avant et après |

Ces fichiers sont générés par `construction/outils/assembler.py` à partir des extractions (`construction/extractions/`). Pour corriger une notion, on corrige son fichier d'extraction puis on relance l'assemblage : voir [../construction/README.md](../construction/README.md).

## Format

Version du format : `0.4`. Chaque fichier commence par `jeuDeDonnees`, `version` et `genereLe` (date de l'assemblage).

On distingue ce que dit le texte officiel (les **objectifs**, cités mot pour mot) de ce qu'on en tire pour accompagner un enfant (les **notions**, reformulées). Une notion renvoie à un ou plusieurs objectifs ; un objectif peut être découpé en plusieurs notions.

**Un programme** (`programmes.json`, objet `programmes`, par clé, ex. `maths-c2`)

| Champ | Contenu |
|---|---|
| `matiere`, `classes` | Matière et classes couvertes |
| `fichier`, `url`, `bo` | PDF (relatif à `construction/programmes-officiels/`), adresse de téléchargement, référence du Bulletin officiel |
| `sha256`, `extraitLe` | Empreinte du PDF et date d'extraction des notions |
| `suit`, `remplace` | Programme de la même matière au cycle précédent ; programmes qu'il remplace, même en partie |

**Un objectif officiel** (`objectifs.json`, tableau `objectifs`)

| Champ | Contenu |
|---|---|
| `id` | `fr-<matière>-<classe>-objectif-<empreinte>`, ex. `fr-ma-ce1-objectif-aa097e8d`. L'empreinte est calculée sur le texte : l'identifiant reste le même tant que le texte ne change pas |
| `programme`, `classe` | Programme et classe (`CE2`, ou `Cycle 4` quand le programme ne précise pas la classe) |
| `domaine`, `sousDomaine` | Intertitres du programme |
| `texte` | Puce « Objectifs d'apprentissage » (ou « Connaissances et compétences associées »), **mot pour mot** |
| `source` | PDF, BO, page et empreinte SHA-256 du PDF au moment de l'extraction |

**Une notion** (`notions.json`, tableau `notions`)

| Champ | Contenu | Origine |
|---|---|---|
| `id` | `fr-<matière>-<classe>-<thème>-NN`, ex. `fr-ma-ce2-fra-01` | — |
| `programme`, `matiere`, `domaine`, `sousDomaine` | Programme, matière et intertitres | texte |
| `classe`, `cycle` | Classe et cycle | texte |
| `periode` | Période de l'année, quand le programme la précise | texte |
| `objectifs` | Identifiants des objectifs officiels couverts | texte |
| `criteres` | Critères de réussite, tirés des « Exemples de réussite » (condensés, rien d'inventé) | texte |
| `source` | Page du programme, et document d'exemples Éduscol s'il a servi (`exemples`, `exemplesPage`, `exemplesSha256`) | texte |
| `nom` | Nom court de la notion | rédigé |
| `description` | Explication simple pour un parent | rédigé |
| `nature` | `compréhension`, `savoir-faire`, `représentation` (passer d'une représentation à une autre), `vocabulaire` ou `stratégie` | rédigé |
| `question` | Question pour vérifier la notion, avec `{{prenom}}` à remplacer par un prénom ou « l'enfant » | rédigé |
| `acquisAnterieurs` | Ce que la notion suppose des classes précédentes, en phrases | rédigé |

« texte » : repris du programme officiel ; « rédigé » : reformulé lors de l'extraction, à vérifier avant tout usage pédagogique.

**Un lien** (`liens.json`, tableau `liens`) : la notion `de` est un prérequis de la notion `vers`.

| Champ | Contenu |
|---|---|
| `type` | `prerequis` (seul type pour l'instant) |
| `force` | `indispensable`, ou `utile` si la notion aide sans être nécessaire |
| `origine` | `texte` si le programme le dit explicitement (492 liens), `déduit` sinon (7 510 liens, à relire) |
| `continuite` | Liens entre classes : `true` quand c'est le même savoir-faire l'année d'avant |
| `raison` | Une phrase d'explication |

Le graphe est sans boucle, et les liens redondants (déjà impliqués par d'autres) sont retirés.
