# État des lieux : projets voisins

> Relevé du 26/10/2026. Question : existe-t-il, en français ou en open source, une base des programmes scolaires découpée en notions et reliée par des prérequis ?

Ce dossier situe vale.edu parmi les projets qui structurent des programmes scolaires. Il décrit chaque projet tel qu'il était le jour du relevé : il peut avoir changé depuis.

- [francais.md](francais.md) : projets français (Forge des communs numériques éducatifs, données ouvertes, recherche, produits non ouverts)
- [international.md](international.md) : projets étrangers (Marble, Learning Commons, Oak, CASE…)

## En bref

- **Côté français, les programmes 2026 existent sous forme consultable** (objectifs d'apprentissage, exemples de réussite), dans des outils d'enseignants. Aucun projet ouvert trouvé ne les découpe en notions avec des identifiants ni ne les relie par des prérequis.
- **Les projets français libres sont surtout sur la Forge des communs numériques éducatifs** (`forge.apps.education.fr`), le GitLab de l'Éducation nationale, plus que sur GitHub. Beaucoup sont apparus en 2026 avec les nouveaux programmes, et chaque outil embarque sa propre copie des textes.
- **Les données officielles donnent les textes, pas leur contenu** : le jeu « programmes du premier degré » de data.education.gouv.fr liste des liens vers des PDF, et sa ligne la plus récente entre en vigueur à la rentrée 2020.
- **Les graphes de prérequis français connus ne sont pas ouverts** : SmartEnseigno (maths du cycle 2), Adaptiv'Math, la « Cartographie des Savoirs » d'Educlever (2013-2015).
- **À l'étranger, des graphes ouverts existent** : Marble (primaire, en anglais) et le Knowledge Graph de Learning Commons (standards américains).

## Comparaison

| Projet | Pays | Classes | Matières | Unité | Prérequis | Critères, questions | Lien au PDF | Licence |
|---|---|---|---|---|---|---|---|---|
| **vale.edu** | FR | PS → 3e | 43 programmes | notion avec identifiant | entre notions, entre classes | critères et question | BO, page, SHA-256 | Licence Ouverte 2.0 + MIT |
| [Explorateurs de Programmes 2026](https://forge.apps.education.fr/chedotalnicole/explorateur-portail-programmes-de-la-ps-a-la-sixieme) | FR | PS → 6e | toutes | objectif du programme | — | exemples de réussite | — | GPL-3.0+ |
| [Socle4](https://forge.apps.education.fr/glb/socle4) | FR | 5e → 3e | toutes | compétence, attendu par classe | hiérarchie seulement | indicateurs | — | non déclarée |
| [Lecteur de programmes](https://forge.apps.education.fr/duplessyerwan/lecteur-de-programmes) | FR | 6e → Tle | maths, SNT, NSI | partie du programme | — | — | — | CC BY-SA 4.0 |
| SmartEnseigno | FR | cycle 2 | maths | « cocon » | arbre, graphes | exercices | — | non ouverte |
| [Ontologies (data.gouv.fr)](https://www.data.gouv.fr/datasets/ontologies-descriptives-du-systeme-et-des-programmes-scolaires-francais) | FR | surtout lycée | — | classe OWL | — | — | — | CC BY-NC |
| [Marble](https://github.com/withmarbleapp/os-taxonomy) | US, UK, AU (anglais) | primaire | 9 | notion | entre notions | critères, pistes | standard source | ODbL + CC BY-SA |
| [Learning Commons](https://github.com/learning-commons-org/knowledge-graph) | US | K-12 | 4 | standard, composante (maths) | progressions | — | standard source | CC BY 4.0 |
| [Oak National Academy](https://open-api.thenational.academy/) | UK | KS1 → KS4 | toutes | unité, leçon | — | ressources de leçon | — | OGL v3 |

« — » : absent ou non trouvé.

## Où se situe vale.edu

- **Prérequis** : c'est l'apport principal par rapport aux projets français ouverts relevés.
- **Traçabilité** : chaque notion cite l'objectif mot pour mot, avec le BO, la page et l'empreinte du PDF.
- **Périmètre** : toutes les matières de la PS à la 3e ; les autres projets français couvrent un cycle ou une matière.
- **Format** : texte officiel et notions séparés, liens typés entre notions, noms de champs en français.
- **Public** : parents autant qu'enseignants, avec des descriptions simples et des questions de vérification.
- **Limite** : les prérequis déduits n'ont pas encore été relus par des enseignants, contrairement au référentiel SmartEnseigno, construit par l'IREM de Grenoble.

## Interopérabilité

Formats d'échange relevés, qui pourraient servir d'exports :
- **JSON au format Marble** : pour croiser vale.edu avec la taxonomie de Marble ;
- **CSV par programme** : le format des petits jeux de données d'enseignants sur la Forge ;
- **CASE** (1EdTech), outillé par OpenSALT : le format standard d'échange des référentiels de compétences ;
- **serveur MCP** : Marble et Learning Commons en ont un, pour l'usage par des assistants IA.

Projets qui pourraient relier leurs données aux identifiants `fr-…` :
- les Explorateurs de Programmes 2026, pour afficher les prérequis d'un objectif ;
- MathALÉA (Coopmaths) et SACoche (Sésamath), pour rattacher exercices et compétences à des notions ;
- Socle4, pour le cycle 4.

## Méthode

- Recherche par mots-clés dans l'API de la Forge (programmes, compétences, référentiel, progression, socle, Éduscol, LSU, notions, explorateur, parcours…), puis lecture des README, des licences et d'échantillons de données.
- Recherche de dépôts sur GitHub, en français et en anglais.
- Recherche web sur les données ouvertes du ministère, les projets de recherche (COMPER, Kidlearn, SmartEnseigno, Educlever) et les graphes étrangers.
- Non vérifié : le contenu exact des produits non ouverts, l'état actuel du référentiel annoncé en open data par Educlever en 2015, la liste des jeux de Learning Commons soumis à autorisation.

Un projet manque ou a changé ? Les signalements sont bienvenus (voir « Contribuer » dans le [README](../README.md#contribuer)).
