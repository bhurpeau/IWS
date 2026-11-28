# Scripts du référentiel notationnel

Outils en lecture seule, à lancer depuis la racine du dépôt. Python 3 standard, sauf le registre YAML style bloc (G0.2bis), qui requiert PyYAML 6.0.2 dans l'environnement dédié `.venv-g0` (`notations/requirements-g0.txt` ; aucune installation globale).

| Script | Rôle | Phase |
|---|---|---|
| `extract_symbols.py` | Inventaire lexical des symboles mathématiques (occurrences, expressions, familles, glyphes, exclusions) | G0.1 |
| `check_coverage.py` | Contrôles de couverture : audit `\rho`, contrôle croisé regex, audit V5.16, labels, délimiteurs ; code de sortie 0/1 | G0.1 |
| `check_regression.py` | Non-régression de l'inventaire contre la référence `05afddd` | G0.1 (B2a) |
| `definition_sites.py` | Sites de définition candidats (« on note », « := »…) | G0.2 |
| `link_registry.py` | Validation du registre (schéma, granularité) et rattachement aux occurrences ; sélecteurs par glyphe, indice, exposant, fichier, lignes, niveau, décoration, police | G0.2, G0.2bis |
| `registry_io.py` | Lecture et écriture YAML du registre ; vérification d'égalité profonde (`verify`, `convert`) | G0.2bis (C4) |
| `formal_environments.py` | Sections et énoncés formels (environnements, `\resultheading`, `\resultstep`, encadrés, paragraphes étiquetés) | G0.2bis |
| `coverage_matrix.py` | Matrice de couverture documentaire par livre, annexe et section | G0.2bis |
| `classify_unresolved.py` | Classement des clés structurantes non rattachées (table manuelle + règles) | G0.2bis |
| `registry_diff.py` | Différentiel avec le registre de référence (95 objets) | G0.2bis |
| `build_crosswalk.py` | Génère `notations/crosswalk.csv` depuis `notations/crosswalk_relations.yaml` et le registre ; contrôles de cohérence et bilan par objet | G0.3 |
| `tests/` | Tests unitaires (extraction ; registre ; table de correspondance) | G0.1, G0.2bis, G0.3 |

```bash
python3 -I notations/scripts/extract_symbols.py --out audits/G0/G0_01_inventory
python3 -I notations/scripts/check_coverage.py --inv audits/G0/G0_01_inventory
python3 -I -m unittest discover -s notations/scripts/tests
```

G0.2 et G0.2bis :

```bash
python3 -m venv .venv-g0 && .venv-g0/bin/pip install -r notations/requirements-g0.txt
.venv-g0/bin/python -I notations/scripts/link_registry.py --out audits/G0/G0_02_semantic
.venv-g0/bin/python -I notations/scripts/formal_environments.py --out audits/G0/G0_02bis
python3 -I notations/scripts/classify_unresolved.py
.venv-g0/bin/python -I notations/scripts/coverage_matrix.py --out audits/G0/G0_02bis
.venv-g0/bin/python -I notations/scripts/registry_diff.py --out audits/G0/G0_02bis
.venv-g0/bin/python -I notations/scripts/build_crosswalk.py
.venv-g0/bin/python -I -m unittest discover -s notations/scripts/tests
```

Ordre : `link_registry.py` produit les rattachements utilisés par `classify_unresolved.py`, puis `coverage_matrix.py` les combine avec le journal de lecture (`audits/G0/G0_02bis/reading_log.csv`).

Méthode, règles de classification et limites : `audits/G0/G0_01_inventory/extraction_report.md`.
