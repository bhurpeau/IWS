#!/usr/bin/env python3
"""G0.4 — validation et exploitation du catalogue des collisions (lecture seule des sources).

Entrées : notations/collisions.yaml (catalogue) ; notations/registry.yaml ; notations/crosswalk_relations.yaml ;
          inventaire G0.1 (audits/G0/G0_01_inventory/occurrences_*.csv) ;
          audits/G0/G0_02bis/unresolved_classification.csv (50 clés USAGE_AMBIGU) ; sources manuscrites (motifs texte).
Sorties (audits/G0/G0_04_collisions/) :
  collisions.csv             une ligne par collision, avec décomptes d'occurrences ;
  collision_occurrences.csv  décompte par collision, sélecteur, rôle et fichier (propagation) ;
  ambiguous_keys_coverage.csv  bilan des 50 clés ambiguës ;
  collisions_summary.json    répartition par niveau, nature, portée, famille, arbitrage ; erreurs.

Contrôles (code de sortie 1 si l'un échoue) :
  - champs obligatoires, valeurs autorisées (nature, niveau, portée, catégorie), identifiants uniques ;
  - objets existants dans le registre ; relations existantes dans la table ; anomalies connues (registre ou RESERVES.md) ;
  - chaque sélecteur compte au moins une occurrence (un sélecteur vide signale une erreur de catalogue) ;
  - couverture : chacune des 50 clés ambiguës est rattachée à au moins une collision ;
  - chaque relation DIST/ANA/UNK intervolumes est traitée (collision ou motif d'absence) ;
  - chaque relation ID (et R001, R002) est examinée pour la synonymie ;
  - une collision de catégorie SCIENTIFIQUE porte un arbitrage scientifique ;
  - règle F1 : un N3 est intervolumes et motive une proximité (la réservation est un facteur aggravant, non un critère) ;
  - intervention dans les valeurs autorisées ; tout reclassement est documenté.
Usage : .venv-g0/bin/python -I notations/scripts/build_collisions.py
"""
import collections
import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import registry_io  # noqa: E402

CAT = 'notations/collisions.yaml'
REG = 'notations/registry.yaml'
XW = 'notations/crosswalk_relations.yaml'
INV = 'audits/G0/G0_01_inventory/occurrences_%s.csv'
RES = 'audits/G0/RESERVES.md'
AMB = 'audits/G0/G0_02bis/unresolved_classification.csv'
OUT = 'audits/G0/G0_04_collisions/'
NATURES = {'HOMONYMIE', 'SYNONYMIE', 'QUASI_COLLISION', 'AMBIGUITE'}
NIVEAUX = {'N0', 'N1', 'N2', 'N3', 'N4'}
PORTEES = {'intra_I', 'intra_II', 'intra_C', 'inter', 'inter_C'}
INTERV = {'PRESERVER', 'DOCUMENTER', 'CORRECTION_CANDIDATE', 'A_ARBITRER'}
CATEG = {'NOTATIONNELLE', 'TERMINOLOGIQUE', 'DOCUMENTAIRE', 'SCIENTIFIQUE'}
REQUIRED = ['id', 'famille', 'symboles', 'objets', 'nature', 'niveau', 'portee', 'justification', 'impact_scientifique',
            'impact_editorial', 'impact_lean', 'intervention', 'propagation', 'action_proposee', 'arbitrage', 'categorie_correction',
            'selecteurs']
VOLS = ('volI', 'volII', 'compagnons')
SRC_I = ['Volume_I/main.tex', 'Volume_I/IWS_PART_I.tex', 'Volume_I/IWS_PART_II.tex', 'Volume_I/IWS_PART_III.tex',
         'Volume_I/TABLE_ENONCES.tex'] + ['Volume_I/Annexes/IWS_ANNEXE_%s.tex' % x for x in 'ABCDEFGHIJKL']
SRC_II = ['Volume_II/IWS_volume_II_classe_objets_transformations_v5_17.tex']
SRC_C = ['Volume_II/preuves_compagnons/certification_huit_episodes_V2.tex',
         'Volume_II/preuves_compagnons/transmission_profondeur_finie_V2.tex']
SOURCES = {'volI': SRC_I, 'volII': SRC_II, 'compagnons': SRC_C}


def key(r):
    k = r['glyphe']
    if r['indice']:
        k += '_{%s}' % r['indice']
    if r['exposant']:
        k += '^{%s}' % r['exposant']
    return k


def match(sel, r):
    """Même sémantique que link_registry.match ; niveau 0 (hors indices) par défaut."""
    if sel.get('glyphe') and r['glyphe'] != sel['glyphe']:
        return False
    for fld, col in (('indice', 'indice'), ('exposant', 'exposant'), ('fichier', 'fichier'), ('decoration', 'decoration')):
        if fld in sel and not re.search(sel[fld], r[col]):
            return False
    if 'lignes' in sel and not (sel['lignes'][0] <= int(r['ligne']) <= sel['lignes'][1]):
        return False
    if r['niveau'] != str(sel.get('niveau', '0')):
        return False
    return r['contexte'] != 'definition_macro'


def text_hits(sel):
    """Occurrences d'un motif texte (expression régulière) dans les sources, lignes de commentaire exclues."""
    hits = collections.Counter()
    pat = re.compile(sel['texte'])
    for f in SOURCES[sel['vol']]:
        for line in open(f, encoding='utf-8'):
            if line.lstrip().startswith('%'):
                continue
            n = len(pat.findall(line))
            if n:
                hits[f] += n
    return hits


def main():
    cat = registry_io.load(CAT)
    reg = {o['id']: o for o in registry_io.load(REG)['objets']}
    anomalies = {o.get('anomalie') for o in reg.values() if o.get('anomalie')}
    anomalies |= set(re.findall(r'^\| (A-G02-\d+) ', open(RES, encoding='utf-8').read(), re.M))
    xw = {r['id']: r for r in registry_io.load(XW)['relations']}
    occ = {v: list(csv.DictReader(open(INV % v, encoding='utf-8'))) for v in VOLS}
    err, rows, prop = [], [], []
    ids = collections.Counter(c['id'] for c in cat['collisions'])
    err += ['identifiant de collision dupliqué %s' % i for i, n in ids.items() if n > 1]
    key_map = collections.defaultdict(list)
    rel_cov = collections.defaultdict(list)
    for c in cat['collisions']:
        cid = c['id']
        for f in REQUIRED:
            if f not in c or c[f] in (None, '', []):
                err.append('%s : champ manquant %s' % (cid, f))
        for n in c.get('nature', []):
            if n not in NATURES:
                err.append('%s : nature invalide %s' % (cid, n))
        if c.get('niveau') not in NIVEAUX:
            err.append('%s : niveau invalide' % cid)
        if c.get('portee') not in PORTEES:
            err.append('%s : portée invalide' % cid)
        if c.get('categorie_correction') not in CATEG:
            err.append('%s : catégorie invalide' % cid)
        if c.get('categorie_correction') == 'SCIENTIFIQUE' and 'scientifique' not in c.get('arbitrage', ''):
            err.append('%s : catégorie SCIENTIFIQUE sans arbitrage scientifique' % cid)
        if c.get('niveau') == 'N3':
            if c.get('portee') not in ('inter', 'inter_C'):
                err.append('%s : N3 hors portée intervolumes (règle F1)' % cid)
            if not re.search(r'proximit', c.get('justification', '') + c.get('revue_F1', '')):
                err.append('%s : N3 sans proximité motivée (règle F1)' % cid)
        if c.get('intervention') not in INTERV:
            err.append('%s : intervention invalide' % cid)
        if c.get('niveau_G04_initial') and not c.get('reclassement_F1'):
            err.append('%s : reclassement non documenté' % cid)
        for o in c.get('objets', []):
            if o not in reg:
                err.append('%s : objet inconnu %s' % (cid, o))
        for x in c.get('relations', []) or []:
            if x not in xw:
                err.append('%s : relation inconnue %s' % (cid, x))
            rel_cov[x].append(cid)
        for a in c.get('anomalies', []) or []:
            if a not in anomalies:
                err.append('%s : anomalie inconnue %s' % (cid, a))
        for k in c.get('cles_ambigues', []) or []:
            key_map[k].append(cid)
        tot = collections.Counter()
        for i, s in enumerate(c.get('selecteurs', [])):
            if 'texte' in s:
                hits = text_hits(s)
                forme = 'texte:%s' % s['texte']
            else:
                hits = collections.Counter(r['fichier'] for r in occ[s['vol']] if match(s, r))
                forme = ' '.join('%s=%s' % (k, v) for k, v in s.items() if k not in ('role', 'vol'))
            n = sum(hits.values())
            if n == 0:
                err.append('%s : sélecteur %d vide (%s %s)' % (cid, i, s['vol'], forme))
            tot[(s['role'], s['vol'])] += n
            for f, m in sorted(hits.items()):
                prop.append(dict(collision=cid, selecteur=i, role=s['role'], vol=s['vol'], forme=forme,
                                 fichier=f, occurrences=m))
        a_ex = sum(v for (r, _), v in tot.items() if r == 'cote_a_examiner')
        ref = sum(v for (r, _), v in tot.items() if r == 'reference')
        rows.append(dict(id=cid, famille=c['famille'], niveau=c['niveau'],
                         niveau_G04_initial=c.get('niveau_G04_initial', c['niveau']),
                         intervention=c['intervention'], facteur_aggravant=c.get('facteur_aggravant', ''), nature=' '.join(c['nature']),
                         portee=c['portee'], categorie=c['categorie_correction'], arbitrage=c['arbitrage'],
                         symboles=' | '.join(c['symboles']), objets=' '.join(c['objets']),
                         relations=' '.join(c.get('relations', []) or []),
                         anomalies=' '.join(c.get('anomalies', []) or []),
                         cles_ambigues=' '.join(c.get('cles_ambigues', []) or []),
                         occ_cote_a_examiner=a_ex, occ_reference=ref,
                         action_proposee=c['action_proposee'], justification=c['justification']))
    # Couverture des 50 clés ambiguës
    amb = [r for r in csv.DictReader(open(AMB, encoding='utf-8')) if r['categorie'] == 'USAGE_AMBIGU']
    keycov = []
    for r in amb:
        k = '%s|%s' % (r['corpus'], r['cle'])
        cs = key_map.get(k, [])
        if not cs:
            err.append('clé ambiguë sans collision : %s' % k)
        lv = sorted({next(c['niveau'] for c in cat['collisions'] if c['id'] == x) for x in cs})
        keycov.append(dict(corpus=r['corpus'], cle=r['cle'], occurrences=r['occurrences'], collisions=' '.join(cs),
                           niveaux=' '.join(lv), justification_G02bis=r['justification']))
    for k in key_map:
        if k not in {'%s|%s' % (r['corpus'], r['cle']) for r in amb}:
            err.append('clé déclarée absente de la liste des 50 : %s' % k)
    # Relations DIST / ANA / UNK et synonymies ID
    sans = {x['relation'] for x in cat.get('relations_examinees_sans_collision', [])}
    syn = {x['relation'] for x in cat.get('synonymies_ID_examinees', [])}
    for x in sans | syn:
        if x not in xw:
            err.append('relation examinée inconnue %s' % x)
    for rid, r in xw.items():
        if r['relation'] in ('DIST', 'ANA', 'UNK') and r.get('portee') != 'intravolume':
            if rid not in rel_cov and rid not in sans:
                err.append('relation %s %s non examinée' % (r['relation'], rid))
        if r['relation'] == 'ID' or r.get('portee') == 'intravolume':
            if rid not in syn:
                err.append('relation %s %s : synonymie non examinée' % (r['relation'], rid))
    for x in cat.get('reservations_V5_16', []):
        if x['collision'] and x['collision'] not in ids:
            err.append('réservation %s : collision inconnue %s' % (x['symbole'], x['collision']))
    for x in cat.get('corrections_scientifiques', []):
        if x['anomalie'] and x['anomalie'] not in anomalies:
            err.append('correction %s : anomalie inconnue' % x['id'])
    os.makedirs(OUT, exist_ok=True)
    for name, data in (('collisions.csv', rows), ('collision_occurrences.csv', prop), ('ambiguous_keys_coverage.csv', keycov)):
        with open(OUT + name, 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=list(data[0]))
            w.writeheader()
            w.writerows(data)
    C = collections.Counter
    summ = dict(collisions=len(rows),
                par_niveau=dict(sorted(C(r['niveau'] for r in rows).items())),
                par_nature=dict(C(n for r in rows for n in r['nature'].split())),
                par_portee=dict(C(r['portee'] for r in rows)),
                par_famille=dict(C(r['famille'] for r in rows)),
                par_intervention=dict(C(r['intervention'] for r in rows)),
                intervention_par_niveau={n: dict(C(r['intervention'] for r in rows if r['niveau'] == n))
                                         for n in sorted(NIVEAUX)},
                reclassements=[dict(id=r['id'], de=r['niveau_G04_initial'], vers=r['niveau']) for r in rows
                               if r['niveau_G04_initial'] != r['niveau']],
                facteur_aggravant_reservation=sum(1 for r in rows if r['facteur_aggravant']),
                par_categorie=dict(C(r['categorie'] for r in rows)),
                par_arbitrage=dict(C(r['arbitrage'] for r in rows)),
                niveau_par_famille={f: dict(sorted(C(r['niveau'] for r in rows if r['famille'] == f).items()))
                                    for f in sorted({r['famille'] for r in rows})},
                cles_ambigues=dict(total=len(amb), couvertes=sum(1 for k in keycov if k['collisions'])),
                relations_DIST_ANA_UNK=sorted(rid for rid, r in xw.items()
                                              if r['relation'] in ('DIST', 'ANA', 'UNK') and r.get('portee') != 'intravolume'),
                propagation_cote_a_examiner=sum(r['occ_cote_a_examiner'] for r in rows),
                propagation_N3_N4_cote_a_examiner=sum(r['occ_cote_a_examiner'] for r in rows if r['niveau'] in ('N3', 'N4')),
                corrections_scientifiques=[x['id'] for x in cat.get('corrections_scientifiques', [])],
                erreurs=err)
    json.dump(summ, open(OUT + 'collisions_summary.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in summ.items() if k not in ('erreurs', 'relations_DIST_ANA_UNK')},
                     ensure_ascii=False, indent=1))
    for e in err:
        print('ERREUR', e)
    return 1 if err else 0


if __name__ == '__main__':
    sys.exit(main())
