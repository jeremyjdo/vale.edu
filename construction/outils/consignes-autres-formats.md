# Consignes complémentaires : programmes qui ne suivent pas le format « Objectifs / Exemples de réussite »

À lire **en plus** de `consignes-extraction.md`, dont toutes les règles restent valables (format de sortie, validation, granularité, fidélité, natures, id, liens, rapport). Seule change la façon de trouver les notions et les critères.

## Anciens programmes de 2020 (cycles 2 à 4) et programmes rédigés par cycle

Structure habituelle par thème : « Attendus de fin de cycle », puis un tableau « Connaissances et compétences associées » / « Exemples de situations, d'activités et de ressources pour l'élève », puis des « Repères de progressivité ».

- **Notion** : en général une puce de « Connaissances et compétences associées ». Les intertitres en gras qui regroupent plusieurs puces donnent le `sousDomaine`.
- **objectifsOfficiels** : la ou les puces de « Connaissances et compétences associées », mot pour mot. Quand un attendu de fin de cycle n'a aucune puce correspondante, il peut devenir une notion et être cité mot pour mot.
- **criteres** : tirés des « Attendus de fin de cycle » correspondants et des « Exemples de situations, d'activités et de ressources ». Formule des critères observables, sans inventer.
- **classe** : la classe quand les « Repères de progressivité » placent clairement la notion dans une année (ex. « au CE2… »). Sinon le cycle entier : `Cycle 2`, `Cycle 3` ou `Cycle 4` (slug c2, c3, c4 dans l'id). Mets la progression décrite par les repères dans `description` ou dans `periode`.
- La couverture se vérifie sur les puces de « Connaissances et compétences associées » : `couverture.py` ne les détecte pas, fais ton propre contrôle.

## Programmes en tableaux par année sans « Exemples de réussite » (ex. EMC 2024)

Colonnes « Notions abordées » / « Contenus d'enseignement » / « Démarches et situations d'apprentissage possibles ».

- **Notion** : une « notion abordée » avec ses « contenus d'enseignement » ; découpe si les contenus couvrent des savoirs nettement distincts.
- **objectifsOfficiels** : le texte exact de la notion abordée et du contenu d'enseignement correspondant.
- **criteres** : tirés des contenus et des « démarches et situations possibles », reformulée en critères observables (« Explique… », « Donne un exemple de… »).

## Programmes disponibles seulement en image (PDF scannés)

`textes/<pdf>.txt` est vide. Lis les pages du PDF avec l'outil Read (`pages`, 5 pages au plus par appel) et transcris fidèlement. Comme la copie mot pour mot est plus difficile, relis chaque `objectifsOfficiels` sur l'image avant de valider.
