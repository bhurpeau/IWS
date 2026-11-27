#!/usr/bin/env python3
"""G0.2 — repérage des sites de définition candidats (lecture seule).

Pour chaque ligne source portant un indice de définition (environnement de définition,
« on note », « désigne », « on appelle », « soit », « on pose », :=, \\coloneqq…), relève les
clés de notation de niveau 0 de l'inventaire G0.1 présentes sur la ligne, ainsi qu'une
statistique par clé (occurrences, fichiers, sections, première occurrence).

Ce n'est qu'un outil d'aide à la lecture : aucune identification sémantique n'est faite ici.

Usage :
    python3 -I notations/scripts/definition_sites.py --out audits/G0/G0_02_semantic
"""
import argparse
import collections
import csv
import os
import re

INV = 'audits/G0/G0_01_inventory/'
CUES = [
    ('env_definition', r'\\begin\{(definition|candidate|definitionthm)\}'),
    ('on_note', r'\b[Oo]n (le |la |les )?note\b|\b[Nn]otons\b|\bnoté[es]?\b'),
    ('designe', r'\bdésigne(nt)?\b'),
    ('on_appelle', r'\b[Oo]n (l\'|les? |la )?appelle\b|\best appelée?s?\b|\bappelons\b'),
    ('on_definit', r'\b[Oo]n (le |la |les )?définit\b|\best défini[es]?\b|\bdéfinissons\b|\bdéfinie? par\b'),
    ('on_pose', r'\b[Oo]n pose\b|\b[Pp]osons\b'),
    ('soit', r'\b[Ss]oi(en)?t\b'),
    ('affectation', r':=|\\coloneqq|\\eqqcolon|=:'),
    ('resultheading', r'\\resultheading\{(Définition|Notation)'),
]


def key(r):
    k = r['glyphe']
    if r['indice']:
        k += '_{%s}' % r['indice']
    if r['exposant']:
        k += '^{%s}' % r['exposant']
    return k


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='audits/G0/G0_02_semantic')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for vol in ('volI', 'volII', 'compagnons'):
        occ = [r for r in csv.DictReader(open(INV + 'occurrences_%s.csv' % vol, encoding='utf-8'))
               if r['niveau'] == '0' and r['contexte'] != 'definition_macro']
        by_line = collections.defaultdict(list)
        stats = {}
        for r in occ:
            k = key(r)
            by_line[(r['fichier'], int(r['ligne']))].append(k)
            s = stats.setdefault(k, dict(cle=k, famille=r['famille_lexicale'], glyphe=r['glyphe'], n=0,
                                         fichiers=collections.Counter(), sections=set(),
                                         premiere='%s:%s' % (r['fichier'], r['ligne'])))
            s['n'] += 1
            s['fichiers'][r['fichier'].split('/')[-1]] += 1
            s['sections'].add(r['section'])
        rows = []
        for f in sorted({r['fichier'] for r in occ}):
            lines = open(f, encoding='utf-8').read().split('\n')
            for i, l in enumerate(lines, 1):
                body = l.split('%')[0] if not l.lstrip().startswith('%') else ''
                cues = [n for n, p in CUES if re.search(p, body)]
                if not cues:
                    continue
                keys = by_line.get((f, i), [])
                # une définition introduit souvent le symbole sur la ligne suivante
                nxt = by_line.get((f, i + 1), [])
                rows.append(dict(fichier=f, ligne=i, indices=';'.join(cues), cles_ligne=' '.join(dict.fromkeys(keys)),
                                 cles_ligne_suivante=' '.join(dict.fromkeys(nxt)), extrait=body.strip()[:220]))
        with open(os.path.join(a.out, 'definition_sites_%s.csv' % vol), 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        with open(os.path.join(a.out, 'notation_keys_%s.csv' % vol), 'w', newline='', encoding='utf-8') as fh:
            w = csv.writer(fh)
            w.writerow(['cle', 'famille', 'glyphe', 'occurrences_niveau0', 'nb_fichiers', 'nb_sections', 'premiere', 'fichiers'])
            for s in sorted(stats.values(), key=lambda s: -s['n']):
                w.writerow([s['cle'], s['famille'], s['glyphe'], s['n'], len(s['fichiers']), len(s['sections']), s['premiere'],
                            ' '.join('%s:%d' % x for x in s['fichiers'].most_common())])
        print(vol, 'sites', len(rows), 'clés', len(stats))


if __name__ == '__main__':
    main()
