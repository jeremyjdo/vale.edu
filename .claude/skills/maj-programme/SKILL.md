---
name: maj-programme
description: Ajoute un nouveau programme officiel (BO) ou une nouvelle version d'un programme à la base de notions vale.curriculum, en gardant toute la traçabilité (PDF archivé, empreintes, dates d'extraction et de liaison, journal des changements). À utiliser quand on dépose un nouveau PDF de programme, qu'un nouveau BO paraît, qu'on demande de vérifier si les programmes ont changé, ou de mettre la base à jour.
---

# Mettre à jour la base de notions

La procédure complète est dans `construction/outils/MISE-A-JOUR.md` : lis-la d'abord et suis-la. Toutes les commandes se lancent depuis `construction/`. Le jeu de données (`data/`) et l'atlas (`site/`) sont générés : ne les modifie jamais à la main.

## Déroulé

1. **État de départ** : `python3 outils/etat.py`. Note les actions déjà en attente.
2. **Identifier le cas** :
   - vérifier les mises à jour : `python3 outils/verifier_sources.py --en-ligne` ;
   - nouvelle version d'un PDF connu : partie 2 de la procédure ;
   - nouveau programme : partie 3. Demande l'adresse du PDF et le BO s'ils manquent. Ne télécharge que depuis education.gouv.fr ou eduscol.education.gouv.fr.
3. **Enregistrer le PDF** avec `outils/preparer_pdf.py`. Ne remplace jamais un PDF à la main : l'outil archive l'ancienne version.
4. **Mesurer l'impact** : `python3 outils/etat.py --programme <clé>`. Montre à l'utilisateur ce qui va être ré-extrait et les liaisons à refaire avant de lancer les agents.
5. **Extraire puis relier** avec des sous-agents (modèles de demande dans la procédure) :
   - six agents au plus en même temps ;
   - un sous-dossier de travail par agent ;
   - après les liaisons, relance `elaguer_liens.py` sur tous les fichiers de liens.
6. **Assembler et vérifier** : `valider.py`, `assembler.py` (le jeu de données `data/`, son journal et l'atlas `site/index.html` sont refaits automatiquement), `verifier_sources.py`, puis `etat.py`, qui doit répondre « Tout est à jour ». Une matière nouvelle doit être rangée dans `FAMILLES` (`outils/construire_site.py`).
7. **Documenter** : mets à jour `construction/programmes-officiels/README.md` (textes en vigueur), `construction/README.md` (avancement) et les chiffres du README à la racine, puis résume l'entrée ajoutée à `data/JOURNAL.md`.

## Règles

- La base est générique, et pourra être publiée : aucune référence à un enfant en particulier.
- Une notion garde l'empreinte du PDF dont elle vient. Ne recalcule jamais `source.sha256` sur une notion existante : ré-extrais-la.
- En cas de ré-extraction, garde les `id` des notions inchangées (règle 10 des consignes d'extraction).
- Rapport final en français, avec les chiffres : notions ajoutées, retirées et modifiées ; liens refaits ; écarts de vérification.
