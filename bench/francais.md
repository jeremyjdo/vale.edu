# Projets français

Relevé du 26/10/2026. Les dates d'activité et les licences viennent de l'API de la Forge des communs numériques éducatifs (`forge.apps.education.fr`) ou de GitHub, le jour du relevé.

## 1. Les plus proches : programmes découpés et consultables

### Explorateurs de Programmes 2026

- **Quoi** : un portail et une série d'applications, une par cycle ou par domaine (maternelle, polyvalence C2, polyvalence C3, maths C2-C3, français C2-C3, sciences C1-C3, EPS C1-C4, numérique C1-C3 avec le CRCN). On cherche les objectifs d'apprentissage des programmes 2026, on les met dans un « panier » et on les copie.
- **Contenu** : objectifs d'apprentissage et **exemples de réussite**, de la PS à la 6e.
- **Format** : données écrites dans chaque page HTML (avec des marqueurs `||EX: … ||` pour les exemples). Pas de jeu de données séparé, pas de prérequis.
- **Licence** : GPL-3.0+.
- **Activité** : créé en juin 2026, mis à jour en août-septembre 2026. Une variante existe chez `rouxsimon` (français et maths C2-C3).
- **Lien** : [portail](https://forge.apps.education.fr/chedotalnicole/explorateur-portail-programmes-de-la-ps-a-la-sixieme), [maths C2-C3](https://forge.apps.education.fr/chedotalnicole/explorateur-programmes-c-2-c-3-maths).
- **Comparaison** : même matière première que vale.edu (objectifs mot pour mot et exemples de réussite), mais pour l'enseignant qui prépare sa classe. Pas de découpage en notions, de graphe, de question d'évaluation ni de lien vers la page du PDF.

### Lecteur de programmes et m-progression

- **Quoi** : un site statique pour consulter et filtrer les programmes de maths, et un générateur de progressions.
- **Contenu** : un fichier JSON par classe, de la 6e à la terminale (plus SNT et NSI) ; m-progression a les versions 2020 et 2026 du collège.
- **Format** : JSON `meta` / `filtres` / `parties` / `sousParts` / `contenus` / `capacites`. C'est l'arborescence du programme, sans identifiant de notion ni prérequis.
- **Licence** : CC BY-SA 4.0 pour le lecteur ; aucune pour m-progression.
- **Activité** : juin à octobre 2026.
- **Lien** : [lecteur-de-programmes](https://forge.apps.education.fr/duplessyerwan/lecteur-de-programmes), [m-progression](https://forge.apps.education.fr/duplessyerwan/m-progression).

### Socle4

- **Quoi** : un « navigateur de compétences » du cycle 4, toutes matières, qui croise les compétences des disciplines avec les cinq domaines du socle commun.
- **Contenu** : pour chaque compétence, un attendu par classe (5e, 4e, 3e), des verbes d'action, des indicateurs et des ressources typiques.
- **Format** : YAML (site Astro), exports CSV et JSON. Hiérarchie par `parent_id`, sans prérequis.
- **Licence** : aucune déclarée.
- **Activité** : mai à octobre 2026.
- **Lien** : [glb/socle4](https://forge.apps.education.fr/glb/socle4).
- **Comparaison** : le projet le plus proche par l'intention (« structurer une bonne fois pour toutes »), mais limité au cycle 4 et sans graphe.

### Petits jeux de données d'enseignants

- [programmes_liste-des-objectifs-attendus](https://forge.apps.education.fr/g.annedouche/programmes_liste-des-objectifs-attendus) : objectifs de français du CM1 et du CM2 en CSV. Pas de licence. Avril 2026.
- [generateur-progressions](https://forge.apps.education.fr/pantalonivincent/generateur-progressions) : objectifs CM2-6e en CSV et un script Python de progression. CC BY-SA 4.0.
- [arbre-de-competences](https://forge.apps.education.fr/yannlefebvre/arbre-de-competences) : arbre de compétences pour une classe, dans Grist, avec une table `Liens_Competences` qui débloque une compétence quand une compétence liée est acquise. C'est le seul projet français trouvé avec une notion de dépendance, mais il est propre à une classe et sans données publiées. Pas de licence.

## 2. Accès aux textes, sans découpage

- **Jeu de données officiel** : [data.education.gouv.fr](https://data.education.gouv.fr/explore/dataset/fr-en-programmes-enseignement-premier-degre/) publie la liste des programmes du premier degré, avec un lien vers le PDF. Au 26/10/2026, il compte 10 lignes, dont la plus récente entre en vigueur à la rentrée 2020. **Les programmes 2024-2026 n'y sont pas**, et il n'y a aucun contenu structuré.
- [Passe-moi le programme](https://forge.apps.education.fr/guerinludovic/passe-moi-le-programme) : une interface sur ce jeu de données (premier et second degré). AGPL-3.0.
- [Boussole 1D](https://forge.apps.education.fr/roedererphilippe/boussole1d) : répertoire des textes officiels et des livrets Éduscol de la maternelle à la 6e (circonscription de Cluses). AGPL-3.0 et CC BY-SA.
- [chat-bot-programmes](https://forge.apps.education.fr/chat-bot-programmes/chat-bot-programmes.forge.apps.education.fr) : rassemble les documents d'accompagnement en PDF pour un assistant conversationnel. GPL-3.0+.
- [Fabunia](https://forge.apps.education.fr/fabunia/fabunia.forge.apps.education.fr) : « atelier pédagogique augmenté » qui transforme les programmes en progressions et séances, en commençant par les maths de 6e (2026-2027). AGPL-3.0. Pas encore de fichiers publiés au moment du relevé.

## 3. Outils d'évaluation et d'exercices

- **SACoche** (Sésamath) : évaluation par compétences et suivi du socle, avec des référentiels partagés entre enseignants. AGPL-3.0. Les référentiels sont des listes de compétences, sans prérequis. [Forge](https://forge.apps.education.fr/sesamath/sacoche), [site](https://sacoche.sesamath.net).
- **MathALÉA / Coopmaths** : générateur d'exercices de maths, avec des référentiels JSON par classe qui relient les exercices aux attendus. AGPL-3.0, 59 étoiles, très actif. Le contenu commence vraiment en CM1. [Forge](https://forge.apps.education.fr/coopmaths/mathalea).
- **Sésaparcours** (Sésamath) : le moteur des exercices interactifs de LaboMEP et Mathenpoche. [Forge](https://forge.apps.education.fr/sesamath/sesaparcours).

Ces trois projets seraient des **utilisateurs** naturels d'une base de notions : un exercice MathALÉA ou une compétence SACoche pourrait pointer vers un identifiant `fr-…`.

## 4. Données sémantiques et métadonnées

- **Ontologies du système et des programmes scolaires** ([data.gouv.fr](https://www.data.gouv.fr/datasets/ontologies-descriptives-du-systeme-et-des-programmes-scolaires-francais)) : OWL en RDF/XML, publiées à titre individuel, pas par le ministère. Surtout le secondaire, d'après d'anciens programmes. Licence CC BY pour un usage non commercial.
- **ScoLOMFR** ([Éduscol](https://eduscol.education.gouv.fr/4917/le-referentiel-scolomfr)) : profil de métadonnées et vocabulaires SKOS de la DNE et de Réseau Canopé (niveaux, domaines d'enseignement…). Utile pour aligner les codes de matière et de classe, pas pour les notions.

## 5. Recherche et produits non ouverts

- **Cartographie des Savoirs** (Educlever/Maxicours, 2013-2015) : référentiel de compétences de maths et de français du cycle 3, annoncé en open data dans un [article EIAH 2015](https://perso.liris.cnrs.fr/nathalie.guin/EAEI/Guin.pdf). Aucune trace d'une publication actuelle.
- **SmartEnseigno** (Educlever, Cabrilog, Ludotic, IFÉ, IREM de Grenoble, Inria Wimmics ; programme P2IA) : référentiel des maths du cycle 2 (nombre, calcul, géométrie) découpé en « cocons » et organisé en arbre, dont on tire des graphes pour les parcours ([actes COPIRELEM 2021](https://irem.univ-grenoble-alpes.fr/medias/fichier/actes-grenoble-e_1707925611476-pdf)). Plateforme gratuite pour les classes depuis 2021, mais aucune licence ouverte trouvée.
- **Adaptiv'Math** (EvidenceB, Inria Flowers ; P2IA) : parcours adaptatifs de maths au cycle 2, avec l'algorithme ZPDES issu de Kidlearn et un graphe pédagogique interne. Données non ouvertes.
- **COMPER** ([ANR-18-CE38-0012](https://anr.fr/Projet-ANR-18-CE38-0012), LIRIS) : modèle de référentiels de compétences et de profils d'élèves, testé du primaire à l'université. Projet de recherche.

## 6. Sur GitHub

Aucun dépôt de programmes français structurés n'est sorti des recherches (« programmes scolaires », « eduscol », « socle commun », « référentiel compétences »…). Les projets français de ce type sont sur la Forge.
