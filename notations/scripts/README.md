# Scripts du référentiel notationnel

Outils en lecture seule, Python 3 sans dépendance externe, à lancer depuis la racine du dépôt.

| Script | Rôle | Phase |
|---|---|---|
| `extract_symbols.py` | Inventaire lexical des symboles mathématiques (occurrences, expressions, familles, glyphes, exclusions) | G0.1 |
| `check_coverage.py` | Contrôles de couverture : audit `\rho`, contrôle croisé regex, audit V5.16, labels, délimiteurs ; code de sortie 0/1 | G0.1 |
| `tests/` | Tests unitaires sur des fragments réels des sources | G0.1 |

```bash
python3 -I notations/scripts/extract_symbols.py --out audits/G0/G0_01_inventory
python3 -I notations/scripts/check_coverage.py --inv audits/G0/G0_01_inventory
python3 -I -m unittest discover -s notations/scripts/tests
```

Méthode, règles de classification et limites : `audits/G0/G0_01_inventory/extraction_report.md`.
