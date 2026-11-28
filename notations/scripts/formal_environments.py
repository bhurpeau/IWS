#!/usr/bin/env python3
"""G0.2bis — inventaire des sections et des énoncés formels (lecture seule).

Relève, pour chaque manuscrit :
  - les commandes de sectionnement (part, chapter, section, subsection, subsubsection, paragraph),
    avec leur plage de lignes (jusqu'à la commande suivante de niveau égal ou supérieur) ;
  - les énoncés formels :
      * environnements de type théorème (definition, proposition, lemma, theoreme, corollary,
        candidate, remark, crashtest, question, … tels que déclarés par \\newtheorem) ;
      * volume I : \\resultheading{Type}{label}{…} et \\resultstep{label} (énoncés numérotés),
        boîtes `encadre` (titre), paragraphes titrés « Définition / Proposition / Lemme /
        Hypothèse / Notation / Convention / Corollaire / Théorème » ou étiquetés (A1), (E2), O1… ;
  - le chemin de section de chaque énoncé.

Les commentaires LaTeX sont ignorés. Aucun contenu mathématique n'est interprété.

Usage :
    python3 -I notations/scripts/formal_environments.py --out audits/G0/G0_02bis
"""
import argparse
import csv
import os
import re

CORPUS = {
    'volI': ['Volume_I/IWS_PART_I.tex', 'Volume_I/IWS_PART_II.tex', 'Volume_I/IWS_PART_III.tex'] +
            ['Volume_I/Annexes/IWS_ANNEXE_%s.tex' % c for c in 'ABCDEFGHIJKL'],
    'volII': ['Volume_II/IWS_volume_II_classe_objets_transformations_v5_17.tex'],
    'compagnons': ['Volume_II/preuves_compagnons/certification_huit_episodes_V2.tex',
                   'Volume_II/preuves_compagnons/transmission_profondeur_finie_V2.tex'],
}
LEVELS = {'part': 0, 'chapter': 1, 'section': 2, 'subsection': 3, 'subsubsection': 4, 'paragraph': 5}
THM_ENVS = ['definition', 'candidate', 'proposition', 'propositionthm', 'lemma', 'lemme', 'theoreme', 'theorem',
            'corollary', 'corollaire', 'remark', 'remarque', 'crashtest', 'question', 'hypothesis', 'assumption',
            'notation', 'convention', 'example', 'exemple']
KIND = {'definition': 'DEF', 'candidate': 'DEF', 'proposition': 'PROP', 'propositionthm': 'PROP', 'lemma': 'LEM',
        'lemme': 'LEM', 'theoreme': 'THM', 'theorem': 'THM', 'corollary': 'COR', 'corollaire': 'COR',
        'remark': 'REM', 'remarque': 'REM', 'crashtest': 'TEST', 'question': 'QUEST', 'hypothesis': 'HYP',
        'assumption': 'HYP', 'notation': 'NOT', 'convention': 'NOT', 'example': 'EX', 'exemple': 'EX'}
PARA_KIND = [('DEF', r'^D[ée]finition'), ('PROP', r'^Proposition'), ('LEM', r'^Lemme'), ('THM', r'^Th[ée]or[èe]me'),
             ('COR', r'^Corollaire'), ('HYP', r'^Hypoth[èe]se'), ('NOT', r'^(Notation|Convention|Vocabulaire)'),
             ('PROOF', r'^D[ée]monstration'), ('LABELLED', r'^\(?[A-Z]{1,2}[0-9]+[a-z]?\)?(\s|$|\s*---)')]
SEC_RE = re.compile(r'\\(part|chapter|section|subsection|subsubsection|paragraph)\*?\s*(?:\[[^\]]*\])?\{')
BEGIN_RE = re.compile(r'\\begin\{(%s|encadre)\}' % '|'.join(THM_ENVS))
RH_RE = re.compile(r'\\resultheading\{([^}]*)\}\{([^}]*)\}')
RS_RE = re.compile(r'\\resultstep\{([^}]*)\}')
LABEL_RE = re.compile(r'\\label\{([^}]*)\}')


def strip_comment(line):
    out, i = [], 0
    while i < len(line):
        c = line[i]
        if c == '\\' and i + 1 < len(line):
            out.append(line[i:i + 2])
            i += 2
            continue
        if c == '%':
            break
        out.append(c)
        i += 1
    return ''.join(out)


def braced(s, start):
    """Contenu d'un groupe {…} commençant juste après l'accolade ouvrante en position start."""
    depth, i = 1, start
    while i < len(s) and depth:
        if s[i] == '\\':
            i += 2
            continue
        if s[i] == '{':
            depth += 1
        elif s[i] == '}':
            depth -= 1
        i += 1
    return s[start:i - 1] if depth == 0 else s[start:]


def clean_title(t):
    t = re.sub(r'\\theproposition\{\}|\\theproposition', '#', t)
    t = re.sub(r'\\(textbf|emph|textit|mathrm|text)\{([^}]*)\}', r'\2', t)
    return re.sub(r'\s+', ' ', t).strip()


def scan(path):
    lines = [strip_comment(l) for l in open(path, encoding='utf-8').read().split('\n')]
    secs, stmts, env_stack = [], [], []
    in_doc_body = True
    for n, line in enumerate(lines, 1):
        for m in SEC_RE.finditer(line):
            lvl = m.group(1)
            title = clean_title(braced(line, m.end()))
            secs.append(dict(niveau=lvl, rang=LEVELS[lvl], ligne=n, titre=title))
            if lvl == 'paragraph':
                kind = next((k for k, rx in PARA_KIND if re.search(rx, title)), None)
                if kind and kind != 'PROOF':
                    lab = LABEL_RE.search(line)
                    stmts.append(dict(ligne=n, fin='', forme='paragraph', type=kind, label=lab.group(1) if lab else '',
                                      titre=title))
        for m in BEGIN_RE.finditer(line):
            env = m.group(1)
            rest = line[m.end():]
            title = ''
            if rest.startswith('['):
                j = rest.find(']')
                title = rest[1:j] if j > 0 else rest[1:]
                title = re.sub(r'^title=\{?|\}$', '', title)
            lab = LABEL_RE.search(line) or (LABEL_RE.search(lines[n]) if n < len(lines) else None)
            rec = dict(ligne=n, fin='', forme='env:' + env, type=KIND.get(env, 'BOX'), label=lab.group(1) if lab else '',
                       titre=clean_title(title))
            stmts.append(rec)
            env_stack.append((env, rec))
        for m in re.finditer(r'\\end\{(%s|encadre)\}' % '|'.join(THM_ENVS), line):
            for k in range(len(env_stack) - 1, -1, -1):
                if env_stack[k][0] == m.group(1):
                    env_stack[k][1]['fin'] = n
                    del env_stack[k]
                    break
        for m in RH_RE.finditer(line):
            kind = next((k for k, rx in PARA_KIND if re.search(rx, m.group(1))), 'PROP')
            stmts.append(dict(ligne=n, fin='', forme='resultheading', type=kind, label=m.group(2), titre=clean_title(m.group(1))))
        for m in RS_RE.finditer(line):
            lab = m.group(1)
            kind = {'def': 'DEF', 'prop': 'PROP', 'lem': 'LEM', 'cor': 'COR', 'thm': 'THM'}.get(lab.split(':')[0], 'PROP')
            stmts.append(dict(ligne=n, fin='', forme='resultstep', type=kind, label=lab, titre=''))
    # plages des sections
    for i, s in enumerate(secs):
        end = len(lines)
        for t in secs[i + 1:]:
            if t['rang'] <= s['rang']:
                end = t['ligne'] - 1
                break
        s['fin'] = end
    # chemin de section
    def path_at(n):
        cur = {}
        for s in secs:
            if s['ligne'] > n:
                break
            if s['rang'] >= 5:
                continue
            cur[s['rang']] = s['titre']
            for r in list(cur):
                if r > s['rang']:
                    del cur[r]
        return ' > '.join(cur[r] for r in sorted(cur))
    for st in stmts:
        st['section'] = path_at(st['ligne'])
    return secs, stmts, len(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='audits/G0/G0_02bis')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for vol, files in CORPUS.items():
        with open(os.path.join(a.out, 'sections_%s.csv' % vol), 'w', newline='', encoding='utf-8') as fs, \
                open(os.path.join(a.out, 'formal_statements_%s.csv' % vol), 'w', newline='', encoding='utf-8') as ft:
            ws = csv.writer(fs)
            ws.writerow(['fichier', 'niveau', 'ligne', 'fin', 'titre'])
            wt = csv.writer(ft)
            wt.writerow(['fichier', 'ligne', 'fin', 'forme', 'type', 'label', 'titre', 'section'])
            for f in files:
                secs, stmts, _ = scan(f)
                for s in secs:
                    ws.writerow([f, s['niveau'], s['ligne'], s['fin'], s['titre']])
                for st in sorted(stmts, key=lambda x: x['ligne']):
                    wt.writerow([f, st['ligne'], st['fin'], st['forme'], st['type'], st['label'], st['titre'], st['section']])
                print('%-70s sections %4d  énoncés %4d' % (f, len(secs), len(stmts)))


if __name__ == '__main__':
    main()
