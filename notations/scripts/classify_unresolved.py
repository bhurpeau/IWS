#!/usr/bin/env python3
"""G0.2bis — classement des clés de notation structurantes non (entièrement) rattachées (lecture seule).

Entrée : audits/G0/G0_02_semantic/coverage_structuring_keys.csv (produit par link_registry.py) et une table
de classement manuel (CSV) ; sortie : audits/G0/G0_02bis/unresolved_classification.csv.

Catégories (consigne C3, point 7) :
  VARIABLE_LOCALE              variable générique ou locale à un passage (x, t, X_0…)
  INDICE_MUET                  indice ou variable muette (i, j, k de sommation…)
  NOTATION_USUELLE             notation mathématique usuelle (tanh, max, C^2, ∞…)
  STRUCTURANT_NON_INSTRUIT     objet structurant non encore enregistré
  USAGE_AMBIGU                 même clé pour plusieurs objets ; rattachement par sélecteur impossible sans lecture fine
  NON_RESOLU                   rôle non établi

Le classement manuel prime ; à défaut, des règles lexicales attribuent NOTATION_USUELLE ou INDICE_MUET ;
toute clé restante est NON_RESOLU et doit être examinée.

Usage :
    python3 -I notations/scripts/classify_unresolved.py --manual audits/G0/G0_02bis/unresolved_manual.csv \
        --out audits/G0/G0_02bis/unresolved_classification.csv
"""
import argparse
import csv
import re

COV = 'audits/G0/G0_02_semantic/coverage_structuring_keys.csv'
CATS = ['VARIABLE_LOCALE', 'INDICE_MUET', 'NOTATION_USUELLE', 'STRUCTURANT_NON_INSTRUIT', 'USAGE_AMBIGU', 'NON_RESOLU']
USUEL = re.compile(r'^(\\tanh|\\cos|\\sin|\\deg|\\max|\\min|\\inf|\\sup|\\sum|\\operatorname\{sech\}|\\mathrm\{d\}|\\infty|\\mathbb\{R\}|I_\{d\}|\\Re|'
                   r'\\operatorname\{spec\}|\\operatorname\{Deg\}|\\square|\\varnothing|\\overline\{\.\.\.\}|C\^\{[12]\}|\\partial_\{t\}|e\^\{|\\exp|\\log|\\det|'
                   r'\\operatorname\{int\}|\\operatorname\{Stab\}|O$|\\pi$|S\^\{1\}|\\mathbb)')
MUET = re.compile(r'^(i|j|n|\\sum_\{.*\}|\\max_\{.*\})$')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--manual', default='audits/G0/G0_02bis/unresolved_manual.csv')
    ap.add_argument('--out', default='audits/G0/G0_02bis/unresolved_classification.csv')
    a = ap.parse_args()
    manual = {}
    for row in csv.DictReader(open(a.manual, encoding='utf-8')):
        if row['categorie'] not in CATS:
            raise SystemExit('catégorie inconnue : %r' % row)
        manual[(row['corpus'], row['cle'])] = row
    out, stats = [], {}
    for r in csv.DictReader(open(COV, encoding='utf-8')):
        if r['statut'] == 'resolue':
            continue
        k = (r['corpus'], r['cle'])
        if k in manual:
            cat, just, src = manual[k]['categorie'], manual[k]['justification'], 'manuel'
        elif USUEL.match(r['cle']):
            cat, just, src = 'NOTATION_USUELLE', 'règle lexicale (fonction ou symbole usuel)', 'règle'
        elif MUET.match(r['cle']):
            cat, just, src = 'INDICE_MUET', 'règle lexicale (indice)', 'règle'
        else:
            cat, just, src = 'NON_RESOLU', 'aucun classement', 'défaut'
        nr = int(r['occurrences']) - int(r['rattachees'])
        out.append(dict(corpus=r['corpus'], cle=r['cle'], occurrences=r['occurrences'], rattachees=r['rattachees'], non_rattachees=nr,
                        statut_couverture=r['statut'], categorie=cat, justification=just, source_classement=src, fichiers=r['fichiers']))
        stats.setdefault(r['corpus'], {}).setdefault(cat, [0, 0])
        stats[r['corpus']][cat][0] += 1
        stats[r['corpus']][cat][1] += nr
    with open(a.out, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    for v, d in stats.items():
        print(v, ' ; '.join('%s %d clés / %d occ.' % (c, *d[c]) for c in CATS if c in d))
    unk = [o for o in out if o['categorie'] == 'NON_RESOLU']
    print('non résolus :', len(unk))
    for o in unk:
        print('  ', o['corpus'], o['cle'], o['non_rattachees'], o['fichiers'][:80])


if __name__ == '__main__':
    main()
