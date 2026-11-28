#!/usr/bin/env python3
"""G0.2 — validation du registre candidat et rattachement aux occurrences G0.1 (lecture seule).

Usage (depuis la racine du dépôt) :
    .venv-g0/bin/python -I notations/scripts/link_registry.py --out audits/G0/G0_02_semantic
(PyYAML requis pour le registre YAML style bloc ; voir registry_io.py)

Contrôles : schéma minimal, unicité des identifiants, statuts autorisés, dépendances existantes,
notation canonique vide (G0.2). Rattachement : chaque sélecteur filtre les occurrences de
l'inventaire (glyphe exact, indice / exposant / symbole source en expressions régulières,
fichier en expression régulière, plage de lignes, niveau, nature).

Couverture : une clé de notation (glyphe + indice + exposant, niveau 0) est dite « structurante »
si elle compte au moins SEUIL occurrences dans un manuscrit. On mesure la part de ses occurrences
rattachées à au moins un objet. Code de sortie : 0 si le schéma est valide, 1 sinon.
"""
import argparse
import collections
import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import registry_io  # noqa: E402

REG = 'notations/registry.yaml'
INV = 'audits/G0/G0_01_inventory/'
STATUTS = {'EXPLICIT', 'IMPLICIT', 'AMBIGUOUS', 'UNDEFINED'}
CONFIANCES = {'haute', 'moyenne', 'faible'}
REQUIRED = ['id', 'phase', 'designation', 'notations', 'nature', 'type', 'domaine', 'codomaine', 'definition',
            'hypotheses', 'portee', 'dependances', 'selecteurs', 'statut_definition', 'motif_statut',
            'confiance', 'notation_canonique']
SEUIL = 5
GRANULARITES = {'famille', 'element'}
PROVENANCES = {'LOCAL', 'BY_REFERENCE', 'DERIVED'}


def key(r):
    k = r['glyphe']
    if r['indice']:
        k += '_{%s}' % r['indice']
    if r['exposant']:
        k += '^{%s}' % r['exposant']
    return k


def match(sel, r):
    if sel.get('glyphe') and r['glyphe'] != sel['glyphe']:
        return False
    for fld, col in (('indice', 'indice'), ('exposant', 'exposant'), ('symbole', 'symbole_source'), ('fichier', 'fichier'),
                     ('decoration', 'decoration'), ('police', 'police')):
        if fld in sel and not re.search(sel[fld], r[col]):
            return False
    if 'lignes' in sel and not (sel['lignes'][0] <= int(r['ligne']) <= sel['lignes'][1]):
        return False
    if 'niveau' in sel and r['niveau'] != sel['niveau']:
        return False
    if 'nature' in sel and r['nature'] != sel['nature']:
        return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='audits/G0/G0_02_semantic')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    reg = registry_io.load(REG)
    objs = reg['objets']
    errors = []
    ids = [o.get('id') for o in objs]
    for i, c in collections.Counter(ids).items():
        if c > 1:
            errors.append('identifiant dupliqué : %s' % i)
    idset = set(ids)
    byid = {o['id']: o for o in objs}
    for o in objs:
        for f in REQUIRED:
            if f not in o:
                errors.append('%s : champ manquant %s' % (o.get('id'), f))
        if o.get('statut_definition') not in STATUTS:
            errors.append('%s : statut invalide %s' % (o['id'], o.get('statut_definition')))
        if o.get('confiance') not in CONFIANCES:
            errors.append('%s : confiance invalide' % o['id'])
        if o.get('notation_canonique'):
            errors.append('%s : notation canonique renseignée (interdit en G0.2)' % o['id'])
        for dep in o.get('dependances', []):
            if dep not in idset:
                errors.append('%s : dépendance inconnue %s' % (o['id'], dep))
        for rel in o.get('relations_intra', []):
            if rel['cible'] not in idset:
                errors.append('%s : relation vers objet inconnu %s' % (o['id'], rel['cible']))
        if o.get('provenance_definition') not in PROVENANCES:
            errors.append('%s : provenance_definition invalide ou absente %s' % (o['id'], o.get('provenance_definition')))
        gran = o.get('granularite')
        if gran is not None and gran not in GRANULARITES:
            errors.append('%s : granularité invalide %s' % (o['id'], gran))
        for comp in o.get('composants', []):
            if comp not in idset:
                errors.append('%s : composant inconnu %s' % (o['id'], comp))
            elif o['id'] not in byid[comp].get('familles', []):
                errors.append('%s : composant %s sans renvoi à sa famille' % (o['id'], comp))
        for fam in o.get('familles', []):
            if fam not in idset:
                errors.append('%s : famille inconnue %s' % (o['id'], fam))
            elif o['id'] not in byid[fam].get('composants', []):
                errors.append('%s : famille %s ne le liste pas' % (o['id'], fam))
        if gran == 'famille' and not o.get('composants') and not o.get('motif_granularite'):
            errors.append('%s : famille sans composants ni motif de non-décomposition' % o['id'])
        if not o['id'].startswith(('I.', 'II.', 'C.')):
            errors.append('%s : préfixe de volume absent' % o['id'])
        fichier = o.get('definition', {}).get('fichier', '')
        if fichier and not os.path.isfile(fichier):
            errors.append('%s : fichier de définition introuvable %s' % (o['id'], fichier))
    occ = {v: list(csv.DictReader(open(INV + 'occurrences_%s.csv' % v, encoding='utf-8'))) for v in ('volI', 'volII', 'compagnons')}
    links = collections.defaultdict(set)   # occurrence id -> objets
    per_obj = collections.Counter()
    sel_empty = []
    for o in objs:
        for k, sel in enumerate(o['selecteurs']):
            n = 0
            for r in occ[sel['vol']]:
                if r['contexte'] == 'definition_macro':
                    continue
                if match(sel, r):
                    links[r['id']].add(o['id'])
                    n += 1
            if n == 0:
                sel_empty.append('%s#%d' % (o['id'], k))
    for oid_set in links.values():
        for oid in oid_set:
            per_obj[oid] += 1
    with open(os.path.join(a.out, 'registry_occurrences.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['occurrence_id', 'objets', 'nb_objets', 'fichier', 'ligne', 'symbole_source', 'niveau'])
        for v, rows in occ.items():
            for r in rows:
                if r['id'] in links:
                    s = sorted(links[r['id']])
                    w.writerow([r['id'], ' '.join(s), len(s), r['fichier'], r['ligne'], r['symbole_source'], r['niveau']])
    # couverture des clés structurantes (niveau 0, manuscrits)
    cov_rows, summary_cov = [], {}
    for v in ('volI', 'volII', 'compagnons'):
        rows = [r for r in occ[v] if r['niveau'] == '0' and r['contexte'] != 'definition_macro']
        bykey = collections.defaultdict(list)
        for r in rows:
            bykey[key(r)].append(r)
        struct = {k: rs for k, rs in bykey.items() if len(rs) >= SEUIL}
        tot = sum(len(rs) for rs in struct.values())
        lk = sum(1 for rs in struct.values() for r in rs if r['id'] in links)
        all_tot = len(rows)
        all_lk = sum(1 for r in rows if r['id'] in links)
        summary_cov[v] = dict(cles_structurantes=len(struct), occurrences_structurantes=tot, rattachees=lk,
                              taux=round(lk / tot, 4) if tot else None, occurrences_niveau0=all_tot,
                              rattachees_niveau0=all_lk, taux_niveau0=round(all_lk / all_tot, 4) if all_tot else None)
        for k, rs in sorted(struct.items(), key=lambda kv: -len(kv[1])):
            n_l = sum(1 for r in rs if r['id'] in links)
            objs_k = collections.Counter(o for r in rs for o in links.get(r['id'], ()))
            files = collections.Counter(r['fichier'].split('/')[-1] for r in rs)
            cov_rows.append(dict(corpus=v, cle=k, occurrences=len(rs), rattachees=n_l, taux=round(n_l / len(rs), 3),
                                 statut='resolue' if n_l == len(rs) else ('partielle' if n_l else 'non_resolue'),
                                 objets=' '.join('%s(%d)' % x for x in objs_k.most_common(4)),
                                 fichiers=' '.join('%s:%d' % x for x in files.most_common(5)),
                                 premiere='%s:%s' % (rs[0]['fichier'].split('/')[-1], rs[0]['ligne'])))
    with open(os.path.join(a.out, 'coverage_structuring_keys.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(cov_rows[0]))
        w.writeheader()
        w.writerows(cov_rows)
    multi = collections.Counter(tuple(sorted(s)) for s in links.values() if len(s) > 1)
    dist = dict(
        par_statut=dict(collections.Counter(o['statut_definition'] for o in objs)),
        par_phase=dict(collections.Counter(o['phase'] for o in objs)),
        par_confiance=dict(collections.Counter(o['confiance'] for o in objs)),
        par_volume=dict(collections.Counter(o['id'].split('.')[0] for o in objs)),
        par_provenance=dict(collections.Counter(o.get('provenance_definition') for o in objs)),
        par_granularite=dict(collections.Counter(o.get('granularite', 'non renseignée') for o in objs)),
        par_nature=dict(collections.Counter(o['nature'].split(' (')[0].split(';')[0] for o in objs)),
        avec_anomalie=sorted({o.get('anomalie') for o in objs if o.get('anomalie')}),
    )
    summary = dict(nb_objets=len(objs), erreurs_schema=errors, selecteurs_vides=sel_empty,
                   occurrences_par_objet=dict(per_obj.most_common()), objets_sans_occurrence=sorted(i for i in idset if per_obj[i] == 0),
                   rattachements_multiples=[dict(objets=list(k), occurrences=n) for k, n in multi.most_common()],
                   couverture=summary_cov, distribution=dist, seuil_structurant=SEUIL)
    with open(os.path.join(a.out, 'registry_summary.json'), 'w', encoding='utf-8') as fh:
        json.dump(summary, fh, indent=1, ensure_ascii=False)
    print('objets %d ; erreurs %d ; sélecteurs vides %d' % (len(objs), len(errors), len(sel_empty)))
    for e in errors:
        print('  ERREUR', e)
    for v, c in summary_cov.items():
        print('%s : clés structurantes %d, occurrences %d, rattachées %.1f %% (niveau 0 global %.1f %%)' % (
            v, c['cles_structurantes'], c['occurrences_structurantes'], 100 * (c['taux'] or 0), 100 * (c['taux_niveau0'] or 0)))
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
