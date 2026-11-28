#!/usr/bin/env python3
"""G0.2bis — matrice de couverture documentaire par livre, annexe et section (lecture seule).

Pour chaque section de niveau chapitre ou section (ou fichier entier pour le volume II et les compagnons, découpés en
sections), donne :
  - plage de lignes ; statut de lecture (journal reading_log.csv : integrale > integrale_declaree > extraits > non_lue) ;
  - nombre d'énoncés formels et de définitions (formal_statements_*.csv) ;
  - nombre d'objets du registre dont le site de définition commence dans la section ;
  - occurrences de niveau 0 et part rattachée au registre ;
  - clés structurantes (≥ 5 occurrences dans le corpus) présentes dans la section et non rattachées, avec leur
    catégorie de classement (unresolved_classification.csv).

Usage :
    .venv-g0/bin/python -I notations/scripts/coverage_matrix.py --out audits/G0/G0_02bis
"""
import argparse
import collections
import csv
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import registry_io  # noqa: E402

INV = 'audits/G0/G0_01_inventory/occurrences_%s.csv'
LINKS = 'audits/G0/G0_02_semantic/registry_occurrences.csv'
B = 'audits/G0/G0_02bis/'
RANK = {'non_lue': 0, 'extraits': 1, 'integrale_declaree': 2, 'integrale': 3}


def key(r):
    k = r['glyphe']
    if r['indice']:
        k += '_{%s}' % r['indice']
    if r['exposant']:
        k += '^{%s}' % r['exposant']
    return k


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=B)
    a = ap.parse_args()
    linked = {r['occurrence_id'] for r in csv.DictReader(open(LINKS, encoding='utf-8'))}
    log = list(csv.DictReader(open(B + 'reading_log.csv', encoding='utf-8')))
    unres = {(r['corpus'], r['cle']): r['categorie'] for r in csv.DictReader(open(B + 'unresolved_classification.csv', encoding='utf-8'))}
    reg = registry_io.load('notations/registry.yaml')['objets']
    defs = collections.defaultdict(list)
    for o in reg:
        d = o['definition']
        if d.get('fichier') and d.get('lignes'):
            defs[d['fichier']].append((d['lignes'][0], o['id']))
    out = []
    for vol in ('volI', 'volII', 'compagnons'):
        occ = [r for r in csv.DictReader(open(INV % vol, encoding='utf-8')) if r['niveau'] == '0' and r['contexte'] != 'definition_macro']
        keycount = collections.Counter(key(r) for r in occ)
        byfile = collections.defaultdict(list)
        for r in occ:
            byfile[r['fichier']].append(r)
        secs = list(csv.DictReader(open(B + 'sections_%s.csv' % vol, encoding='utf-8')))
        stm = list(csv.DictReader(open(B + 'formal_statements_%s.csv' % vol, encoding='utf-8')))
        for f in sorted({s['fichier'] for s in secs}):
            lvl = 'chapter' if any(s['fichier'] == f and s['niveau'] == 'chapter' for s in secs) else 'section'
            units = [s for s in secs if s['fichier'] == f and s['niveau'] in (lvl, 'section' if lvl == 'chapter' else 'x')]
            # sections de rang 2 (section) ; s'il existe des chapitres dans le fichier, on garde chapitres et sections
            units = [s for s in secs if s['fichier'] == f and s['niveau'] in ('chapter', 'section')]
            first = min([int(s['ligne']) for s in units] or [1])
            nlines = sum(1 for _ in open(f, encoding='utf-8'))
            spans = []
            if first > 1:
                spans.append(('(préambule du fichier)', 'preambule', 1, first - 1))
            for s in units:
                if s['niveau'] == 'chapter':
                    # le chapitre ne couvre que ses lignes avant la première section
                    subs = [int(t['ligne']) for t in units if t['niveau'] == 'section' and int(s['ligne']) < int(t['ligne']) <= int(s['fin'])]
                    end = (min(subs) - 1) if subs else int(s['fin'])
                else:
                    end = int(s['fin'])
                spans.append((s['titre'], s['niveau'], int(s['ligne']), end))
            for titre, niv, l0, l1 in spans:
                if l1 < l0:
                    continue
                # statut de lecture d'une unité = mode le plus faible parmi ses lignes, chaque ligne prenant le meilleur
                # mode des entrées du journal qui la couvrent (tolérance d'une ligne en fin de fichier)
                ents = [e for e in log if e['fichier'] == f]
                worst = None
                for ln in range(l0, l1 + 1):
                    cov_ln = [e for e in ents if int(e['ligne_debut']) <= ln <= int(e['ligne_fin']) + 1]
                    b = max(cov_ln, key=lambda e: (RANK[e['mode']], e['phase'])) if cov_ln else None
                    if worst is None or (RANK[b['mode']] if b else 0) < (RANK[worst['mode']] if worst else 0) or b is None:
                        worst = b
                        if b is None:
                            break
                best = worst
                st = [s for s in stm if s['fichier'] == f and l0 <= int(s['ligne']) <= l1]
                rows = [r for r in byfile[f] if l0 <= int(r['ligne']) <= l1]
                lk = sum(1 for r in rows if r['id'] in linked)
                nonlk = collections.Counter(key(r) for r in rows if r['id'] not in linked and keycount[key(r)] >= 5)
                cats = collections.Counter(unres.get((vol, k), 'NON_CLASSE') for k in nonlk for _ in range(nonlk[k]))
                objs = [i for (l, i) in defs.get(f, []) if l0 <= l <= l1]
                out.append(dict(corpus=vol, fichier=f.split('/')[-1], niveau=niv, titre=titre[:90], ligne_debut=l0, ligne_fin=l1,
                                lecture=(best['mode'] if best else 'non_lue'), phase_lecture=(best['phase'] if best else ''),
                                enonces=len(st), definitions=sum(1 for s in st if s['type'] == 'DEF'),
                                objets_definis=len(objs), occurrences=len(rows), rattachees=lk,
                                taux=round(lk / len(rows), 3) if rows else '',
                                non_rattachees_structurantes=sum(nonlk.values()),
                                dont_structurant_non_instruit=cats.get('STRUCTURANT_NON_INSTRUIT', 0),
                                dont_ambigu=cats.get('USAGE_AMBIGU', 0), dont_local_muet_usuel=cats.get('VARIABLE_LOCALE', 0) + cats.get('INDICE_MUET', 0) + cats.get('NOTATION_USUELLE', 0),
                                dont_non_classe=cats.get('NON_CLASSE', 0) + cats.get('NON_RESOLU', 0),
                                cles_principales_non_rattachees=' '.join('%s:%d' % kv for kv in nonlk.most_common(4))))
    with open(os.path.join(a.out, 'coverage_matrix.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]))
        w.writeheader()
        w.writerows(out)
    # synthèse par fichier
    agg = collections.OrderedDict()
    for r in out:
        k = (r['corpus'], r['fichier'])
        g = agg.setdefault(k, dict(unites=0, non_lues=0, extraits=0, enonces=0, objets=0, occ=0, lk=0, sni=0, nc=0))
        g['unites'] += 1
        g['non_lues'] += r['lecture'] == 'non_lue'
        g['extraits'] += r['lecture'] == 'extraits'
        g['enonces'] += r['enonces']
        g['objets'] += r['objets_definis']
        g['occ'] += r['occurrences']
        g['lk'] += r['rattachees']
        g['sni'] += r['dont_structurant_non_instruit']
        g['nc'] += r['dont_non_classe']
    with open(os.path.join(a.out, 'coverage_matrix_by_file.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['corpus', 'fichier', 'unites', 'unites_non_lues', 'unites_extraits', 'enonces', 'objets_definis', 'occurrences', 'rattachees', 'taux',
                    'occ_structurant_non_instruit', 'occ_non_classees'])
        for (v, f), g in agg.items():
            w.writerow([v, f, g['unites'], g['non_lues'], g['extraits'], g['enonces'], g['objets'], g['occ'], g['lk'],
                        round(g['lk'] / g['occ'], 3) if g['occ'] else '', g['sni'], g['nc']])
            print('%-11s %-58s unités %3d  non lues %d  extraits %d  énoncés %3d  objets %3d  occ %5d  rattachées %5.1f %%  non classées %d' % (
                v, f, g['unites'], g['non_lues'], g['extraits'], g['enonces'], g['objets'], g['occ'], 100 * g['lk'] / g['occ'] if g['occ'] else 0, g['nc']))


if __name__ == '__main__':
    main()
