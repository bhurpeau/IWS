#!/usr/bin/env python3
"""G0.3 — génération et contrôle de la table de correspondance intervolumes (lecture seule des sources).

Entrées : notations/crosswalk_relations.yaml (source des relations et des bilans NEW) ;
          notations/registry.yaml (référence 301 entrées).
Sorties : notations/crosswalk.csv (une ligne par relation, enrichie par le registre) ;
          audits/G0/G0_03_crosswalk/coverage_by_object.csv (bilan de recherche pour chaque objet) ;
          audits/G0/G0_03_crosswalk/crosswalk_summary.json.

Contrôles (code de sortie 1 si l'un échoue) :
  - identifiants existants ; relation, statut et confiance dans les valeurs autorisées ;
  - orientation : source I.* ou C.*, cible II.* (sauf portee: intravolume, cible I.*) ;
  - unicité des identifiants de relation et des couples (source, cible) ;
  - pas deux relations contradictoires sur un même couple (ID avec DIST, etc.) ;
  - un objet déclaré NEW ne porte aucune relation d'identification (ID, GEN, SPEC, PROJ, DER) ;
  - chaque objet du registre reçoit un bilan (relation, NEW, ou famille dont les composants ont un bilan) ;
  - une relation entre familles n'est pas propagée aux composants (aucune ligne n'est créée automatiquement).
Usage : .venv-g0/bin/python -I notations/scripts/build_crosswalk.py
"""
import collections
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import registry_io  # noqa: E402

SRC = 'notations/crosswalk_relations.yaml'
REG = 'notations/registry.yaml'
OUT = 'notations/crosswalk.csv'
AUD = 'audits/G0/G0_03_crosswalk/'
RELS = {'ID', 'GEN', 'SPEC', 'PROJ', 'DER', 'ANA', 'DIST', 'UNK', 'NEW'}
IDENT = {'ID', 'GEN', 'SPEC', 'PROJ', 'DER'}
STATUTS = {'etablie', 'candidate', 'indeterminee'}
CONF = {'haute', 'moyenne', 'faible'}
INCOMPAT = [({'ID'}, {'DIST', 'GEN', 'SPEC'}), ({'DIST'}, {'ID', 'GEN', 'SPEC', 'PROJ', 'DER'})]


def src_ref(o):
    d = o['definition']
    if not d.get('fichier'):
        return ''
    lig = d.get('lignes')
    return '%s%s' % (d['fichier'].split('/')[-1], (' l. %d–%d' % tuple(lig)) if lig else '')


def notation(o):
    return ' ; '.join(n['forme'] for n in o['notations'])[:200]


def main():
    data = registry_io.load(SRC)
    reg = {o['id']: o for o in registry_io.load(REG)['objets']}
    err = []
    rows, pairs, seen = [], collections.defaultdict(set), set()
    rel_by_obj = collections.defaultdict(list)
    for r in data['relations']:
        rid = r['id']
        if rid in seen:
            err.append('identifiant de relation dupliqué %s' % rid)
        seen.add(rid)
        intra = r.get('portee') == 'intravolume'
        a = r['I']
        b = r.get('I_cible') if intra else r.get('II')
        for x in (a, b):
            if x not in reg:
                err.append('%s : identifiant inconnu %s' % (rid, x))
        if r['relation'] not in RELS:
            err.append('%s : relation invalide' % rid)
        if r['statut'] not in STATUTS:
            err.append('%s : statut invalide' % rid)
        if r['confiance'] not in CONF:
            err.append('%s : confiance invalide' % rid)
        if not a.startswith(('I.', 'C.')):
            err.append('%s : la source doit être I.* ou C.*' % rid)
        if intra and not b.startswith('I.'):
            err.append('%s : relation intravolume vers un objet non I.*' % rid)
        if not intra and not b.startswith('II.'):
            err.append('%s : la cible doit être II.*' % rid)
        if r['relation'] == 'UNK' and r['statut'] != 'indeterminee':
            err.append('%s : UNK doit être indeterminee' % rid)
        if not r.get('conditions') or not r.get('justification'):
            err.append('%s : conditions ou justification manquantes' % rid)
        pairs[(a, b)].add(r['relation'])
        if a in reg and b in reg:
            oa, ob = reg[a], reg[b]
            card_a = sum(1 for q in data['relations'] if q['I'] == a and q.get('portee') != 'intravolume')
            card_b = sum(1 for q in data['relations'] if (q.get('II') == b))
            rows.append(dict(
                id_relation=rid, portee='intravolume' if intra else 'intervolumes', source=a, cible=b,
                relation=r['relation'], orientation='%s → %s' % (a.split('.')[0], b.split('.')[0]),
                statut=r['statut'], confiance=r['confiance'],
                granularite_source=oa.get('granularite', ''), granularite_cible=ob.get('granularite', ''),
                cardinalite='%s-%s' % ('1' if card_b <= 1 else 'n', '1' if card_a <= 1 else 'n'),
                designation_source=oa['designation'], designation_cible=ob['designation'],
                notation_source=notation(oa), notation_cible=notation(ob),
                type_source=oa.get('type') or '', type_cible=ob.get('type') or '',
                domaine_source=oa.get('domaine') or '', domaine_cible=ob.get('domaine') or '',
                hypotheses_source=' | '.join(oa.get('hypotheses') or [])[:300],
                hypotheses_cible=' | '.join(ob.get('hypotheses') or [])[:300],
                definition_source=src_ref(oa), definition_cible=src_ref(ob),
                statut_def_source=oa['statut_definition'], statut_def_cible=ob['statut_definition'],
                anomalies=' '.join(sorted({x for x in (oa.get('anomalie'), ob.get('anomalie')) if x})),
                conditions=r['conditions'], justification=r['justification']))
            rel_by_obj[a].append((rid, r['relation'], r['statut'], b))
            rel_by_obj[b].append((rid, r['relation'], r['statut'], a))
    for (a, b), s in pairs.items():
        for p, q in INCOMPAT:
            if s & p and s & q:
                err.append('relations contradictoires sur %s / %s : %s' % (a, b, sorted(s)))
    # bilans NEW
    new = {}
    for vol, groups in data.get('bilans_new', {}).items():
        for g in groups:
            for o in g['objets']:
                if o not in reg:
                    err.append('bilan NEW : identifiant inconnu %s' % o)
                if o in new:
                    err.append('bilan NEW en double : %s' % o)
                new[o] = g['motif']
                ident = [x for x in rel_by_obj.get(o, []) if x[1] in IDENT and not x[0].startswith('R')]
                if ident:
                    err.append('%s déclaré NEW mais porte une relation d\'identification %s' % (o, ident))
    # couverture
    cov = []
    for oid, o in reg.items():
        rels = rel_by_obj.get(oid, [])
        inter = [x for x in rels if not x[0].startswith('R')]
        ident_e = [x for x in inter if x[1] in IDENT and x[2] == 'etablie']
        ident_c = [x for x in inter if x[1] in IDENT and x[2] != 'etablie']
        if ident_e:
            st = 'correspondant_etabli'
        elif ident_c:
            st = 'correspondant_candidat'
        elif any(x[1] == 'UNK' for x in inter):
            st = 'indetermine'
        elif oid in new:
            st = 'sans_correspondant_identifie' + ('_avec_analogie_ou_distinction' if inter else '')
        elif o.get('granularite') == 'famille' and o.get('composants'):
            st = 'famille_bilan_par_composants'
        elif inter:
            st = 'analogie_ou_distinction_seulement'
        else:
            st = 'SANS_BILAN'
            err.append('objet sans bilan : %s' % oid)
        cov.append(dict(objet=oid, volume=oid.split('.')[0], designation=o['designation'], granularite=o.get('granularite', ''),
                        bilan=st, relations=' '.join('%s:%s(%s)→%s' % x for x in rels), motif_new=new.get(oid, '')))
    os.makedirs(AUD, exist_ok=True)
    with open(OUT, 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    with open(AUD + 'coverage_by_object.csv', 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(cov[0]))
        w.writeheader()
        w.writerows(sorted(cov, key=lambda c: (c['volume'], c['objet'])))
    summ = dict(relations=len(rows),
                par_relation=dict(collections.Counter(r['relation'] for r in rows if r['portee'] == 'intervolumes')),
                par_statut=dict(collections.Counter(r['statut'] for r in rows if r['portee'] == 'intervolumes')),
                intravolume=[r['id_relation'] for r in rows if r['portee'] == 'intravolume'],
                couverture={v: dict(collections.Counter(c['bilan'] for c in cov if c['volume'] == v)) for v in ('I', 'II', 'C')},
                erreurs=err)
    json.dump(summ, open(AUD + 'crosswalk_summary.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in summ.items() if k != 'erreurs'}, ensure_ascii=False, indent=1))
    for e in err:
        print('ERREUR', e)
    return 1 if err else 0


if __name__ == '__main__':
    sys.exit(main())
