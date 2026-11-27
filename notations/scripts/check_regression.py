#!/usr/bin/env python3
"""Non-régression de l'inventaire lexical par rapport à une version de référence (lecture seule).

Compare, pour chaque fichier d'occurrences, les colonnes présentes dans la version de référence
(par défaut le commit de clôture G0.1, 05afddd) avec l'inventaire courant. Les colonnes ajoutées
ultérieurement (attributs secondaires B2a) sont ignorées.

Usage (depuis la racine du dépôt) :
    python3 -I notations/scripts/check_regression.py [--ref 05afddd]
Code de sortie : 0 si aucune différence, 1 sinon.
"""
import argparse
import csv
import io
import subprocess
import sys

FILES = ['occurrences_volI.csv', 'occurrences_volII.csv', 'occurrences_compagnons.csv',
         'expressions_volI.csv', 'expressions_volII.csv', 'expressions_compagnons.csv',
         'symbol_families.csv', 'symbol_glyphs.csv']
INV = 'audits/G0/G0_01_inventory/'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ref', default='05afddd')
    a = ap.parse_args()
    bad = 0
    for f in FILES:
        ref_txt = subprocess.run(['git', 'show', '%s:%s%s' % (a.ref, INV, f)], capture_output=True, text=True)
        if ref_txt.returncode != 0:
            print('%s : absent de la référence %s' % (f, a.ref))
            continue
        old = list(csv.DictReader(io.StringIO(ref_txt.stdout)))
        new = list(csv.DictReader(open(INV + f, encoding='utf-8')))
        cols = list(old[0].keys()) if old else []
        diff = sum(1 for x, y in zip(old, new) if any(x[c] != y.get(c) for c in cols)) + abs(len(old) - len(new))
        bad += diff
        print('%-32s réf %6d  courant %6d  différences %d' % (f, len(old), len(new), diff))
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
