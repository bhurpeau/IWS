# IWS — Inner World Systems

## Présentation

IWS (*Inner World Systems*) est un programme de recherche consacré à l'étude de systèmes dynamiques hybrides dont l'histoire peut modifier les restructurations futures.

Il explore notamment les relations entre dynamique continue, mémoire interne, événements discrets (Kairos), organisation structurelle, historicité, observation et accessibilité.

La démarche est non téléologique : les mécanismes d'évolution ne sont pas définis par la poursuite d'un objectif prédéterminé.

Ce dépôt constitue le point d'entrée scientifique du projet. Il rassemble les manuscrits de référence, les documents compagnons et les conventions mathématiques communes aux différents travaux.

## 1. Organisation du programme de recherche

### Volume I — Construction et analyse du noyau

Le premier volume construit un spécimen particulier d'IWS, étudie sa dynamique et introduit les premières constructions relatives à son observation.

Il est organisé en trois livres, complétés par les annexes mathématiques A à L.

- [Sources LaTeX du volume I](Volume_I/)
- [Document maître](Volume_I/main.tex)
- [Annexes mathématiques](Volume_I/Annexes/)
- [Table des énoncés](Volume_I/TABLE_ENONCES.tex)

### Volume II — Classe, présentations et transformations

Le deuxième volume cherche à passer du spécimen particulier à une classe de systèmes présentés.

Il développe notamment les notions de lecture déclarée, d'histoires admissibles, de structure lisible, d'opacité, de transformations et de partitions à profondeur finie.

Il distingue les propriétés établies des hypothèses constitutives et des directions de recherche encore ouvertes, notamment celles relatives à la géométrie et à la tameness.

**Version de référence actuelle : V5.17.**

- [Sources LaTeX du volume II](Volume_II/)
- [Source canonique V5.17](Volume_II/IWS_volume_II_classe_objets_transformations_v5_17.tex)
- [Notes de consolidation V5.17](Volume_II/NOTES_V5_17.md)
- [Preuves compagnons](Volume_II/preuves_compagnons/)


## 2. Écosystème des dépôts IWS

Les différents dépôts du projet répondent à des responsabilités distinctes.

| Dépôt | Responsabilité |
|---|---|
| [IWS](https://github.com/bhurpeau/IWS) | Manuscrits scientifiques et référentiel notationnel |
| [iws-lean](https://github.com/bhurpeau/iws-lean) | Formalisation mathématique en Lean 4 |
| [IWS_minimality_package](https://github.com/bhurpeau/IWS_minimality_package) | Travaux expérimentaux, notes et certifications numériques du volume II |
| [IWS_1](https://github.com/bhurpeau/IWS_1) | Implémentation et expérimentations associées à l'article minimal sur le noyau IWS |

Le présent dépôt constitue la référence documentaire et scientifique commune.

### Formalisation mathématique

Le dépôt `iws-lean` formalise les résultats analytiques d'IWS à l'aide de Lean 4, Mathlib et LeanForControl.

État au 26 novembre 2026 :

| Annexe | Objet | Statut |
|---|---|---|
| A | Bonne position et exécutions hybrides | Formalisation achevée |
| C | Réduction homogène et paysage autonome | Formalisation achevée |
| D | Résistance et influence extérieure | Formalisation achevée |
| Autres annexes | Développements complémentaires | À formaliser |

Le corpus comprend 905 théorèmes IWS audités. Les dépendances axiomatiques rapportées sont limitées à `propext`, `Classical.choice` et `Quot.sound`, sans `sorryAx`.

La formalisation analytique ne constitue pas une certification systématique des résultats numériques, des conjectures ou des questions ouvertes du manuscrit.

Les hypothèses supplémentaires, corrections et limites de la formalisation sont documentées dans le README du dépôt Lean.

### Travaux expérimentaux

Le dépôt `IWS_minimality_package` contient notamment :

- les implémentations expérimentales du noyau ;
- les expériences de minimalité et de séparation ;
- les explorations des fibres d'opacité ;
- les partitions et leur raffinement récursif ;
- les études d'accessibilité ;
- les travaux sur les murs actifs ;
- les études de régularité et de transmission à profondeur finie ;
- les scripts de génération de figures ;
- les certificats numériques et les sorties de vérification ;
- les notes mathématiques intermédiaires.

Certains scripts historiques nécessitent encore des adaptations de chemins ou la régénération de données intermédiaires avant leur réexécution.

## 3. Conventions notationnelles

### Principe de primauté du volume II

Les conventions notationnelles stabilisées du volume II constituent le référentiel canonique du projet IWS.

Le volume I doit être harmonisé avec ce référentiel, dans le respect de l'identité, du type, des hypothèses et des propriétés des objets mathématiques qu'il introduit.

Cette primauté est notationnelle et non mathématique : une généralisation introduite dans le volume II ne doit pas conduire à modifier rétroactivement la définition d'un objet particulier du volume I.

Toute dérogation doit être explicitement motivée et documentée.

### Audits disponibles

- [Audit des occurrences de ρ dans le volume I](audits/diag_rho_volI.md)
- [Audit notation–rôle du volume II V5.16](audits/IWS_VolII_audit_notations_v5_16.md)

### Chantier G0 — Harmonisation intervolumes

Le chantier G0 vise à construire un référentiel notationnel et sémantique commun aux deux volumes et à leur formalisation Lean.

Il comprend :

1. L'inventaire lexical des sources.
2. L'identification des objets mathématiques et de leurs rôles.
3. La construction de la table de correspondance intervolumes.
4. Le diagnostic et l'arbitrage des collisions notationnelles.
5. La constitution d'un registre canonique versionné.
6. L'application des conventions aux sources LaTeX.
7. Le raccord documentaire avec la formalisation Lean.
8. L'audit final de cohérence.

La formalisation de l'annexe G et des annexes qui en découlent doit s'appuyer sur les conventions stabilisées par G0.

**Statut actuel : chantier préparatoire.**

## 4. Statut scientifique des résultats

Le projet distingue explicitement :

- les définitions et choix de modélisation ;
- les résultats analytiques démontrés ;
- les résultats conditionnels ;
- les résultats numériques (`[PROP-NUM]`) ;
- les candidats à une caractérisation ;
- les conjectures et questions ouvertes.

La présence d'un résultat dans un manuscrit, une note expérimentale ou un script ne lui confère pas automatiquement un statut de théorème démontré.

De même, une certification numérique assistée par ordinateur ne doit pas être assimilée à une preuve formelle vérifiée par Lean.

Les statuts propres à chaque résultat sont précisés dans les documents concernés.

## 5. Compilation des manuscrits

Les manuscrits sont rédigés en LaTeX.

Depuis la racine du dépôt, les commandes de compilation proposées sont les suivantes.

Volume I :

```bash
cd Volume_I
latexmk -pdf main.tex
```

Volume II :

```bash
cd Volume_II
latexmk -pdf IWS_volume_II_classe_objets_transformations_v5_17.tex
```

Les compilations doivent être effectuées depuis les répertoires respectifs des volumes afin de préserver la résolution des chemins relatifs vers les figures et les fichiers inclus.

La reproductibilité des compilations de référence reste à vérifier dans le cadre du chantier G0.

## 6. Organisation du dépôt

```text
IWS/
├── README.md
├── Volume_I/
│   ├── main.tex
│   ├── IWS_PART_I.tex
│   ├── IWS_PART_II.tex
│   ├── IWS_PART_III.tex
│   ├── IWS_TOME_I_II_REFERENCES.bib
│   ├── TABLE_ENONCES.tex
│   ├── Annexes/
│   └── fig/
├── Volume_II/
│   ├── IWS_volume_II_classe_objets_transformations_v5_17.tex
│   ├── IWS_volume_II_classe_objets_transformations_v5_17.pdf
│   ├── NOTES_V5_17.md
│   ├── preuves_compagnons/
│   └── fig/
├── diag_rho_volI.md
└── IWS_VolII_audit_notations_v5_16.md
```

Un répertoire `notations/` sera ajouté lors de la constitution du référentiel canonique intervolumes.

## 7. Principes de développement

Le projet suit une démarche de construction progressive :

- ne pas introduire de structure mathématique sans nécessité identifiée ;
- distinguer les propriétés du spécimen des propriétés constitutives de la classe ;
- privilégier la réutilisation des résultats mathématiques existants ;
- préserver les résultats validés lors des évolutions éditoriales ;
- documenter les hypothèses, les limites et les divergences ;
- maintenir une distinction explicite entre démonstration, expérimentation et conjecture.

La formalisation mathématique constitue à la fois un instrument de certification et un instrument d'investigation.

## 8. Auteur

Benoit Hurpeau

Programme de recherche IWS — Inner World Systems.