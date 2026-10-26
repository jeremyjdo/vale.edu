# Atlas des notions

Une page pour consulter la base : ouvre [index.html](index.html) dans un navigateur, sans serveur ni installation.

- **La carte** : toutes les notions, les classes de la petite section à la 3e de gauche à droite, une bande par matière. Un clic sur une notion trace en bleu tout ce qu'il faut savoir avant, classe par classe, et en rouge ce qu'elle ouvre.
- **La fiche** : description, question à poser, critères de réussite, prérequis avec leur raison, texte officiel mot pour mot et lien vers la page du PDF.
- **La recherche** (sans accents), le menu « Parcourir » par matière et classe, et un lien direct vers chaque notion (`index.html#fr-ma-ce1-fra-07`).

## Comment elle est faite

`index.html` est générée : ne la modifie pas à la main.

- [modele.html](modele.html) contient la page (HTML, CSS et JavaScript, sans dépendance hormis les polices Google Fonts).
- `construction/outils/construire_site.py` y intègre `data/notions.json` et `data/prerequis.json`, compressés, et écrit `index.html`. L'assemblage (`construction/outils/assembler.py`) le lance à chaque fois.

```bash
cd construction && python3 outils/construire_site.py
```

Les matières sont regroupées en bandes par la liste `FAMILLES` de `construire_site.py` : une matière nouvelle s'y ajoute, sinon elle forme sa propre bande.

Licence : MIT ([LICENSE](../LICENSE)).
