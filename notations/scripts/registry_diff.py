#!/usr/bin/env python3
"""G0.2bis — différentiel entre le registre de référence (95 objets, itération 1) et le registre courant (lecture seule).

Pour chaque identifiant : ajouté, supprimé, inchangé ou modifié (liste des champs modifiés) ; motifs tirés du champ
« revisions » ; variation du nombre d'occurrences rattachées (registry_occurrences.csv de référence et courant).
Contrôle de conservation : aucun identifiant de référence ne doit disparaître.

Usage :
    .venv-g0/bin/python -I notations/scripts/registry_diff.py --out audits/G0/G0_02bis
Code de sortie : 0 si aucun identifiant de référence n'a disparu, 1 sinon.
"""
import argparse
import collections
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import registry_io  # noqa: E402

REF = 'audits/G0/G0_02_semantic/reference_95/registry_G0_02_iter1.json'
REF_OCC = 'audits/G0/G0_02_semantic/reference_95/registry_occurrences_iter1.csv'
CUR = 'notations/registry.yaml'
CUR_OCC = 'audits/G0/G0_02_semantic/registry_occurrences.csv'
IGNORE = {'revisions'}


def occ_counts(path):
    c = collections.Counter()
    for r in csv.DictReader(open(path, encoding='utf-8')):
        for o in r['objets'].split():
            c[o] += 1
    return c


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='audits/G0/G0_02bis')
    ap.add_argument('--ref', default=REF)
    ap.add_argument('--ref-occ', default=REF_OCC)
    ap.add_argument('--name', default='registry_diff.csv')
    a = ap.parse_args()
    ref = {o['id']: o for o in registry_io.load(a.ref)['objets']}
    cur = {o['id']: o for o in registry_io.load(CUR)['objets']}
    oref, ocur = occ_counts(a.ref_occ), occ_counts(CUR_OCC)
    rows = []
    for i in sorted(set(ref) | set(cur)):
        o_r, o_c = ref.get(i), cur.get(i)
        if o_c is None:
            etat, champs = 'supprime', ''
        elif o_r is None:
            etat, champs = 'ajoute', ''
        else:
            ch = sorted(k for k in set(o_r) | set(o_c) if k not in IGNORE and o_r.get(k) != o_c.get(k))
            etat, champs = ('modifie' if ch else 'inchange'), ' '.join(ch)
        revs = (o_c or {}).get('revisions', [])
        rows.append(dict(id=i, etat=etat, champs_modifies=champs,
                         natures_revision=' '.join(sorted({r['nature'] for r in revs})),
                         motifs=' | '.join(r['motif'] for r in revs),
                         granularite=(o_c or {}).get('granularite', ''), familles=' '.join((o_c or {}).get('familles', [])),
                         composants=' '.join((o_c or {}).get('composants', [])),
                         statut_ref=(o_r or {}).get('statut_definition', ''), statut_courant=(o_c or {}).get('statut_definition', ''),
                         occ_ref=oref.get(i, 0), occ_courant=ocur.get(i, 0)))
    os.makedirs(a.out, exist_ok=True)
    with open(os.path.join(a.out, a.name), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    c = collections.Counter(r['etat'] for r in rows)
    print('référence %d ; courant %d ; %s' % (len(ref), len(cur), dict(c)))
    nat = collections.Counter(n for r in rows for n in r['natures_revision'].split())
    print('natures de révision :', dict(nat))
    st = collections.Counter((r['statut_ref'], r['statut_courant']) for r in rows if r['statut_ref'] and r['statut_ref'] != r['statut_courant'])
    print('changements de statut :', dict(st))
    gone = [r['id'] for r in rows if r['etat'] == 'supprime']
    if gone:
        print('IDENTIFIANTS DISPARUS :', gone)
    return 1 if gone else 0


if __name__ == '__main__':
    sys.exit(main())
