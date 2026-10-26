# Consignes de liaison entre classes

Une fois toutes les classes d'un programme extraites, on relie chaque notion à ce qu'elle suppose des classes précédentes. Ces liens vont d'une classe à une autre, à l'intérieur du programme ou depuis le programme du cycle précédent (champ `follows` du registre).

Dossier de travail : `construction/` dans le dépôt. Les commandes se lancent depuis ce dossier.

## Entrées

- Les fichiers `extractions/<programme>-<classe>.json` du programme. Le champ `priorKnowledge` de chaque notion décrit ce qu'elle suppose.
- Pour la première classe du programme : les notions de la dernière classe du programme `follows`, s'il existe.
- Pour lister les notions de façon compacte :

```
python3 -c "import json,sys; [print(n['id'],'|',n['name'],'|',' ; '.join(n.get('priorKnowledge',[]))) for f in sys.argv[1:] for n in json.load(open(f))['notions']]" extractions/<fichier>.json ...
```

## Sortie

Écris UNIQUEMENT `extractions/liens-<programme>.json`, puis lance dans le dossier de travail :

```
python3 outils/elaguer_liens.py extractions/liens-<programme>.json && python3 outils/estampiller.py extractions/liens-<programme>.json && python3 outils/valider.py extractions/<programme>-*.json extractions/<follows>-*.json extractions/liens-<programme>.json
```

(sans la partie `<follows>` si le programme n'en a pas). `estampiller.py` note la date de la liaison et la version des programmes reliés, ce qui permet de savoir quand refaire la liaison. Si le fichier de liens existe déjà (liaison refaite), supprime d'abord ses champs `linkedAt` et `versionsCibles` pour qu'ils soient recalculés. `valider.py` doit répondre « OK ». D'autres extractions peuvent être en cours d'écriture en même temps : ne valide que les fichiers ci-dessus.

```json
{
  "programme": "<clé du registre>",
  "prerequisites": [
    {"topicId": "<notion d'une classe>", "prerequisiteId": "<notion d'une classe antérieure>",
     "strength": "hard", "origin": "déduit", "continuation": true,
     "reason": "Prolonge « nom de la notion » (CE1)"}
  ]
}
```

## Règles

1. Un lien va toujours d'une notion vers une notion d'une classe **antérieure**, jamais vers la même classe : les liens internes à une classe existent déjà.
2. **Prolongement** (`continuation: true`) : relie chaque notion au même savoir-faire l'année d'avant (par exemple les nombres jusqu'à 10 000 du CE2 aux nombres jusqu'à 1 000 du CE1). C'est le lien principal, en général `hard`, avec la raison « Prolonge « <nom> » (<classe>) ».
3. **Appui** (`continuation: false`) : ajoute un lien vers une autre notion antérieure seulement si elle est vraiment nécessaire et n'est pas déjà couverte par le prolongement, avec une raison courte et concrète.
4. `origin` = « texte » seulement si le programme le dit explicitement (par exemple « les élèves réinvestissent ce qui a été vu au CE1 »). Sinon « déduit ».
5. Toute notion qui a un `priorKnowledge` devrait recevoir au moins un lien, sauf si rien d'équivalent n'existe dans les classes disponibles.
6. Pas besoin de chercher la redondance : `elaguer_liens.py` retire les liens déjà impliqués par une autre chaîne.

## Rapport final (10 lignes max)

Nombre de liens proposés et gardés, notions avec `priorKnowledge` restées sans lien et pourquoi, et points de doute.
