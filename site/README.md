# Le site : la carte du curriculum français

Une page pour consulter le curriculum : en ligne sur [vale-edu.vercel.app](https://vale-edu.vercel.app), ou en ouvrant [index.html](index.html) dans un navigateur, sans serveur ni installation.

La version en ligne est publiée par Vercel à chaque envoi sur la branche `main` : seul `index.html` est publié (voir `vercel.json` et `.vercelignore` à la racine du dépôt).

- **La carte** : toutes les notions, les classes de la petite section à la 3e de gauche à droite, une bande par matière. Un clic sur une notion trace en bleu tout ce qu'il faut savoir avant, classe par classe, et en rouge ce qu'elle ouvre.
- **La fiche**, ouverte au clic par-dessus la carte : description, question à poser, critères de réussite, prérequis avec leur raison, texte officiel mot pour mot et lien vers la page du PDF.
- **La recherche** (sans accents), la liste des notions d'une classe ou d'une matière en cliquant sur la carte, et un lien direct vers chaque notion (`index.html#fr-ma-ce1-fra-07`).
- **Les sources** : les programmes officiels, dans une fenêtre ouverte depuis le bas de la page (`index.html#sources`).

## Comment elle est faite

`index.html` est générée : ne la modifie pas à la main.

- [modele.html](modele.html) contient la page (HTML, CSS et JavaScript, sans dépendance hormis les polices Google Fonts).
- `construction/outils/construire_site.py` y intègre `data/notions.json` et `data/prerequis.json`, compressés, et écrit `index.html`. L'assemblage (`construction/outils/assembler.py`) le lance à chaque fois.

```bash
cd construction && python3 outils/construire_site.py
```

Les matières sont regroupées en bandes par la liste `FAMILLES` de `construire_site.py` : une matière nouvelle s'y ajoute, sinon elle forme sa propre bande.

Licence : MIT ([LICENSE](../LICENSE)).
