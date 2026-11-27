#!/usr/bin/env python3
"""Contrôles de couverture de l'inventaire G0.1 (lecture seule).

Usage (depuis la racine du dépôt IWS, après extract_symbols.py) :
    python3 -I notations/scripts/check_coverage.py --inv audits/G0/G0_01_inventory

Produit dans le répertoire d'inventaire :
- coverage_rho_volI.csv : confrontation avec l'audit historique des 455 \\rho ;
- coverage_crosscheck.csv : décompte indépendant par expression régulière vs inventaire ;
- coverage_v516.csv : familles de l'audit V5.16 recomptées sur V5.17 ;
- coverage_v516_patterns.csv : motifs obsolètes de l'audit V5.16 recherchés dans V5.17 ;
- coverage_v517_new_families.csv : familles de V5.17 absentes du tableau V5.16 ;
- coverage_labels.csv : cohérence des ancres avec les labels des .aux de référence ;
- coverage_summary.json.
Code de sortie : 0 si tous les contrôles bloquants passent, 1 sinon.
"""
import argparse
import collections
import csv
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(__file__))
import extract_symbols as ex  # noqa: E402

V2 = 'Volume_II/IWS_volume_II_classe_objets_transformations_v5_17.tex'


def load(inv, key):
    return list(csv.DictReader(open(os.path.join(inv, 'occurrences_%s.csv' % key), encoding='utf-8')))


def body(r):
    return not r['contexte'].startswith('commentaire') and r['contexte'] != 'definition_macro'


def in_ranges(line, ranges):
    return any(a <= line <= b for a, b in ranges)


def rho_audit(I, out):
    """Audit historique diag_rho_volI.md : 48 (R1) + 8 (valeur propre) + 4 (rayon spectral) + 395 (lecture)."""
    rho = [r for r in I if r['famille_lexicale'] == 'rho' and body(r)]
    r1 = {'IWS_PART_II.tex': [(889, 983)], 'Annexes/IWS_ANNEXE_E.tex': [(55, 475), (1554, 1554)],
          'Annexes/IWS_ANNEXE_F.tex': [(158, 158)]}
    modal = {'Annexes/IWS_ANNEXE_C.tex': [(1844, 1888)]}
    cats = collections.Counter()
    rows = []
    for r in rho:
        f = r['fichier'].replace('Volume_I/', '')
        ln = int(r['ligne'])
        if r['indice'] == r'\mathrm{sp}':
            c = 'rayon_spectral'
        elif f in r1 and in_ranges(ln, r1[f]):
            c = 'R1_reouverture'
        elif f in modal and in_ranges(ln, modal[f]):
            c = 'valeur_propre_modale'
        else:
            c = 'lecture_resolution'
        cats[c] += 1
        rows.append(dict(id=r['id'], fichier=f, ligne=ln, symbole_source=r['symbole_source'], classe=r['classe_lexicale'],
                         niveau=r['niveau'], porteur=r['porteur'], attribution_par_plage=c))
    with open(os.path.join(out, 'coverage_rho_volI.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    per_file = collections.Counter(r['fichier'].replace('Volume_I/', '') for r in rho)
    expected = dict(R1_reouverture=48, valeur_propre_modale=8, rayon_spectral=4, lecture_resolution=395)
    return dict(total=len(rho), attendu_total=455, par_categorie=dict(cats), attendu=expected,
                par_fichier=dict(per_file), concordance=dict(cats) == expected and len(rho) == 455,
                classes=dict(collections.Counter(r['classe_lexicale'] for r in rho)),
                niveaux=dict(collections.Counter(r['niveau'] for r in rho)))


def crosscheck(root, inv_all, out):
    """Décompte brut indépendant (regex sur le source sans commentaires) vs atomes inventoriés."""
    rows, mismatches = [], 0
    files = {}
    for corpus, volume, sub, fl, master in ex.CORPUS:
        for f in fl:
            rel = os.path.join(sub, f)
            files[rel] = ex.mask_comments_and_verbatim(open(os.path.join(root, rel), encoding='utf-8').read())[0]
    names = sorted(ex.GREEK | set(ex.LETTERLIKE) | ex.FONTS | {'mathrm', 'operatorname'} | ex.NAMED_OPS | ex.BIG_OPS)
    inv_by = collections.defaultdict(collections.Counter)
    for r in inv_all:
        if not body(r):
            continue
        if r['nature'] in ('macro_utilisateur', 'expression_decoree'):
            continue  # le corps d'une macro n'apparaît pas dans le texte ; l'argument décoré a ses propres lignes
        # commandes présentes dans le glyphe (base, police) et dans la décoration éventuelle
        for m in re.finditer(r'\\([A-Za-z]+)', r['glyphe'] + ' ' + r['decoration'].replace('+', ' ')):
            inv_by[r['fichier']][m.group(1)] += 1
    # macros utilisateur : leurs corps comptent dans le décompte brut des définitions
    for rel, masked in files.items():
        segs, _ = ex.find_math_segments(masked)
        math_text = ' '.join(masked[s['inner_start']:s['inner_end']] for s in segs)
        for n in names:
            pat = r'\\%s(?![A-Za-z])' % re.escape(n)
            raw_all = len(re.findall(pat, masked))
            raw_math = len(re.findall(pat, math_text))
            got = inv_by[rel][n]
            if raw_all == 0 and got == 0:
                continue
            status = 'ok' if raw_math == got else 'ecart'
            note = ''
            if raw_all != raw_math:
                note = '%d hors segments mathématiques (préambule, définitions, texte)' % (raw_all - raw_math)
            if status == 'ecart':
                mismatches += 1
            rows.append(dict(fichier=rel, commande='\\' + n, brut_fichier=raw_all, brut_maths=raw_math,
                             inventaire=got, statut=status, note=note))
    with open(os.path.join(out, 'coverage_crosscheck.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return dict(commandes_controlees=len(rows), ecarts=mismatches,
                ecarts_detail=[r for r in rows if r['statut'] == 'ecart'][:40])


V516 = [  # (libellé de l'audit, occurrences indicatives V5.16, filtre sur l'inventaire)
    ('C', 181, lambda r: r['glyphe'] == 'C'),
    (r'\Xi', 7, lambda r: r['glyphe'] == r'\Xi'),
    (r'\Sigma', 28, lambda r: r['glyphe'] == r'\Sigma'),
    (r'\Omega', 25, lambda r: r['glyphe'] == r'\Omega'),
    (r'\Phi', 11, lambda r: r['glyphe'] == r'\Phi'),
    (r'\vartheta', 26, lambda r: r['glyphe'] == r'\vartheta'),
    ('Dep(Σ)', 19, lambda r: r['famille_lexicale'] in ('op:Dep',)),
    ('k', 18, lambda r: r['glyphe'] == 'k'),
    ('r', 9, lambda r: r['glyphe'] == 'r'),
    ('u', 22, lambda r: r['glyphe'] == 'u'),
    ('v', 1, lambda r: r['glyphe'] == 'v'),
    ('s_i', 1, lambda r: r['glyphe'] == 's' and r['indice'] == 'i'),
    (r'\mathscr F_w', 3, lambda r: r['glyphe'] == r'\mathscr{F}' and r['indice'] == 'w'),
    ('Ω_w', 5, lambda r: r['glyphe'] == r'\Omega' and r['indice'] == 'w'),
    ('b_{i,w}, λ_{r,w}', 8, lambda r: (r['glyphe'] == 'b' and r['indice'] == 'i,w') or (r['glyphe'] == r'\lambda' and r['indice'] == 'r,w')),
    ('τ_*', 9, lambda r: r['glyphe'] == r'\tau' and r['indice'] in (r'*', r'\ast', r'\star', '*')),
]

V516_PATTERNS = [  # motifs obsolètes explicitement formulés dans l'audit V5.16
    ('Références internes V5.10', r'V5\.10'),
    (r'Partition indexée par r (\mathcal P_r)', r'\\mathcal\s*P_r(?![A-Za-z])'),
    (r'Partition indexée par r (\mathcal P_{r...})', r'\\mathcal\s*P_\{r'),
    (r'Ancien Dep(\vartheta)', r'Dep\}?\s*\(\s*\\vartheta'),
    (r'Ancien indexage b_{i,\Xi}', r'b_\{i,\s*\\Xi'),
    (r'Ancien indexage \lambda_{r,\Xi}', r'\\lambda_\{r,\s*\\Xi'),
    ('Ancien compteur s_w', r'(?<![A-Za-z\\])s_w(?![A-Za-z])'),
    (r'Ancien compteur \ell_w', r'\\ell_w(?![A-Za-z])'),
    (r'Réemploi u:=\tau', r'u\s*:=\s*\\tau'),
    (r'Réemploi v_i:=\tau', r'v_i\s*:=\s*\\tau'),
    (r'Ancien compteur récursif 3^\ell', r'3\^\{?\\ell'),
    (r'Ancien \pi_0(E)', r'\\pi_0\s*\(\s*E\s*\)'),
    (r'Ancien compteur \mu_w', r'\\mu_w(?![A-Za-z])'),
]


def v516(root, II, out):
    rows = []
    b = [r for r in II if body(r)]
    for lab, n516, flt in V516:
        sel = [r for r in b if flt(r)]
        rows.append(dict(symbole_audit=lab, occurrences_V516=n516, occurrences_V517_inventaire=len(sel),
                         dont_niveau0=sum(1 for r in sel if r['niveau'] == '0'),
                         premiere_ligne=min((int(r['ligne']) for r in sel), default='')))
    with open(os.path.join(out, 'coverage_v516.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    masked = ex.mask_comments_and_verbatim(open(os.path.join(root, V2), encoding='utf-8').read())[0]
    li = ex.LineIndex(masked)
    prow = []
    for lab, pat in V516_PATTERNS:
        hits = [li.line_col(m.start())[0] for m in re.finditer(pat, masked)]
        prow.append(dict(motif=lab, regex=pat, occurrences=len(hits), lignes=' '.join(map(str, hits[:20]))))
    with open(os.path.join(out, 'coverage_v516_patterns.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(prow[0]))
        w.writeheader()
        w.writerows(prow)
    audited_glyphs = {'C', r'\Xi', r'\Sigma', r'\Omega', r'\Phi', r'\vartheta', 'k', 'r', 'u', 'v', 's',
                      r'\mathscr{F}', 'b', r'\lambda', r'\tau', r'\operatorname{Dep}', r'\mathrm{Dep}'}
    first = {}
    cnt = collections.Counter()
    for r in b:
        if r['niveau'] != '0' or r['glyphe'] in audited_glyphs:
            continue
        cnt[r['glyphe']] += 1
        first.setdefault(r['glyphe'], (int(r['ligne']), r['section']))
    nrows = [dict(glyphe=g, occurrences_niveau0=n, premiere_ligne=first[g][0], section_premiere=first[g][1])
             for g, n in cnt.most_common()]
    with open(os.path.join(out, 'coverage_v517_new_families.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=list(nrows[0]))
        w.writeheader()
        w.writerows(nrows)
    late = [r for r in nrows if r['premiere_ligne'] >= 1600]
    return dict(table=rows, motifs=prow, glyphes_hors_audit=len(nrows),
                glyphes_apparus_apres_l1600=[(r['glyphe'], r['premiere_ligne']) for r in late])


def labels_check(inv, I, II, out):
    res = {}
    rows = []
    for key, occ, csvname in (('volI', I, 'labels_volI.csv'), ('volII', II, 'labels_volII.csv')):
        p = os.path.join('audits/G0/G0_00_controls', csvname)
        aux = {r['label'] for r in csv.DictReader(open(p, encoding='utf-8'))}
        used = collections.Counter(r['label_stable'] for r in occ if r['label_stable'])
        missing = sorted(l for l in used if l not in aux)
        for l in missing:
            rows.append(dict(volume=key, label=l, occurrences=used[l], present_dans_aux=0))
        res[key] = dict(labels_aux=len(aux), labels_utilises_comme_ancre=len(used), absents_aux=missing,
                        occurrences_sans_ancre=sum(1 for r in occ if not r['label_stable']),
                        occurrences=len(occ))
    with open(os.path.join(out, 'coverage_labels.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=['volume', 'label', 'occurrences', 'present_dans_aux'])
        w.writeheader()
        w.writerows(rows)
    return res


def latin_check(root, inv_all):
    """Contrôle indicatif des lettres latines : décompte brut après retrait des commandes et des
    arguments non mathématiques, comparé aux atomes latins inventoriés (lettre nue ou en police)."""
    strip = re.compile(r'\\(text|textrm|textup|textit|textbf|textsf|texttt|mbox|emph|label|ref|eqref|tag|'
                       r'cite|begin|end|hspace|vspace|operatorname\*?|mathrm|mathcal|mathscr|mathfrak|mathbb|'
                       r'mathbf|boldsymbol|color|textcolor)\s*\{[^{}]*(\{[^{}]*\}[^{}]*)*\}')
    res = {}
    inv = collections.Counter()
    for r in inv_all:
        if body(r) and r['nature'] == 'latine':
            inv[r['fichier']] += 1
    for corpus, volume, sub, fl, master in ex.CORPUS:
        for f in fl:
            rel = os.path.join(sub, f)
            masked = ex.mask_comments_and_verbatim(open(os.path.join(root, rel), encoding='utf-8').read())[0]
            segs, _ = ex.find_math_segments(masked)
            n = 0
            for s in segs:
                m = masked[s['inner_start']:s['inner_end']]
                # texte en mode math (minipage) : seules les maths internes comptent
                def _mp(mm):
                    inner, _ = ex.find_math_segments(mm.group(0))
                    return ' ' + ' '.join(mm.group(0)[x['inner_start']:x['inner_end']] for x in inner) + ' '
                m = re.sub(r'\\begin\{minipage\}.*?\\end\{minipage\}', _mp, m, flags=re.S)
                m = re.sub(r'\\begin\{(array|alignat\*?|tabular)\}(\[[^\]]*\])?\{[^}]*\}', ' ', m)
                prev = None
                while prev != m:
                    prev, m = m, strip.sub(' ', m)
                m = re.sub(r'\\(rm|it|bf|sf|tt)\s*[A-Za-z]+', ' ', m)
                m = re.sub(r'\\(mathcal|mathscr|mathfrak|mathbb|mathbf|boldsymbol|mathrm|operatorname)\s*[A-Za-z]', ' ', m)
                m = re.sub(r'\\[A-Za-z@]+', ' ', m)
                n += len(re.findall(r'[A-Za-z]', m))
            res[rel] = dict(brut=n, inventaire=inv[rel], ecart=n - inv[rel])
    return res


def delimiters(root):
    """Décompte brut des délimiteurs mathématiques vs segments détectés."""
    res = {}
    for corpus, volume, sub, fl, master in ex.CORPUS:
        for f in fl:
            rel = os.path.join(sub, f)
            masked = ex.mask_comments_and_verbatim(open(os.path.join(root, rel), encoding='utf-8').read())[0]
            segs, problems = ex.find_math_segments(masked)
            kinds = collections.Counter(s['kind'] for s in segs)
            raw_paren = len(re.findall(r'(?<!\\)\\\(', masked))
            raw_brack = len(re.findall(r'(?<!\\)\\\[', masked))
            envs = sum(len(re.findall(r'\\begin\{%s\}' % re.escape(e), masked)) for e in ex.MATH_ENVS)
            res[rel] = dict(segments=len(segs), problemes=len(problems), brut_paren=raw_paren, brut_crochet=raw_brack,
                            brut_envs_math=envs, envs_detectes=sum(v for k, v in kinds.items() if k.startswith('env')),
                            caracteres_maths=sum(s['inner_end'] - s['inner_start'] for s in segs))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.')
    ap.add_argument('--inv', default='audits/G0/G0_01_inventory')
    a = ap.parse_args()
    I, II, C = load(a.inv, 'volI'), load(a.inv, 'volII'), load(a.inv, 'compagnons')
    summary = dict(rho=rho_audit(I, a.inv), crosscheck=crosscheck(a.root, I + II + C, a.inv),
                   v516=v516(a.root, II, a.inv), labels=labels_check(a.inv, I, II, a.inv),
                   delimiteurs=delimiters(a.root), latin=latin_check(a.root, I + II + C))
    with open(os.path.join(a.inv, 'coverage_summary.json'), 'w', encoding='utf-8') as fh:
        json.dump(summary, fh, indent=1, ensure_ascii=False)
    ok = summary['rho']['concordance'] and summary['crosscheck']['ecarts'] == 0
    print('rho : %s ; écarts regex/inventaire : %d' % (summary['rho']['par_categorie'], summary['crosscheck']['ecarts']))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
