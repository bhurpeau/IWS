#!/usr/bin/env python3
"""Inventaire lexical G0.1 des symboles mathématiques des sources LaTeX IWS.

Lecture seule : aucun fichier source n'est modifié.

Usage (depuis la racine du dépôt IWS) :
    python3 -I notations/scripts/extract_symbols.py --out audits/G0/G0_01_inventory

Principes (détaillés dans audits/G0/G0_01_inventory/extraction_report.md) :
- segmentation du source en commentaires, verbatim, texte et mathématiques
  ($...$, $$...$$, \\(...\\), \\[...\\], environnements mathématiques) ;
- tokenisation des segments mathématiques ; un « atome » est une base symbolique
  (lettre latine, lettre grecque, lettre en police mathématique, nom d'opérateur,
  macro utilisateur) avec ses décorations, primes, indices et exposants ;
- les atomes contenus dans un indice ou un exposant sont aussi enregistrés
  (niveau > 0, lien vers l'atome porteur) ;
- forme source (littérale) et forme développée (macros utilisateur sans argument
  du document, développées une fois) sont distinctes ;
- aucune interprétation sémantique : la classe est purement lexicale.
"""
import argparse
import collections
import csv
import hashlib
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# Corpus
# ---------------------------------------------------------------------------

VOL1_FILES = (['main.tex', 'IWS_PART_I.tex', 'IWS_PART_II.tex', 'IWS_PART_III.tex']
              + ['Annexes/IWS_ANNEXE_%s.tex' % c for c in 'ABCDEFGHIJKL']
              + ['TABLE_ENONCES.tex'])
CORPUS = [
    # (corpus, volume, racine, fichiers, document maître pour les macros)
    ('manuscrit', 'I', 'Volume_I', VOL1_FILES, 'main.tex'),
    ('manuscrit', 'II', 'Volume_II', ['IWS_volume_II_classe_objets_transformations_v5_17.tex'],
     'IWS_volume_II_classe_objets_transformations_v5_17.tex'),
    ('compagnon', 'II', 'Volume_II/preuves_compagnons', ['certification_huit_episodes_V2.tex'],
     'certification_huit_episodes_V2.tex'),
    ('compagnon', 'II', 'Volume_II/preuves_compagnons', ['transmission_profondeur_finie_V2.tex'],
     'transmission_profondeur_finie_V2.tex'),
]
MD_COMPANIONS = ['Volume_II/NOTES_V5_17.md', 'Volume_II/preuves_compagnons/audit_cauchy_lemme_V2.md']

# ---------------------------------------------------------------------------
# Lexique
# ---------------------------------------------------------------------------

GREEK = set('''alpha beta gamma delta epsilon varepsilon zeta eta theta vartheta iota kappa varkappa
lambda mu nu xi omicron pi varpi rho varrho sigma varsigma tau upsilon phi varphi chi psi omega
Gamma Delta Theta Lambda Xi Pi Sigma Upsilon Phi Psi Omega varGamma varDelta varTheta varLambda
varXi varPi varSigma varUpsilon varPhi varPsi varOmega digamma'''.split())
LETTERLIKE = {'ell': 'ell', 'imath': 'imath', 'jmath': 'jmath', 'wp': 'wp', 'Re': 'Re', 'Im': 'Im',
              'aleph': 'aleph', 'hbar': 'hbar', 'beth': 'beth', 'eth': 'eth'}
CONSTANTS = {'infty', 'emptyset', 'varnothing', 'partial', 'nabla', 'top', 'bot', 'Box', 'square',
             'triangle', 'star', 'dagger', 'ddagger', 'flat', 'sharp', 'natural', 'checkmark'}
FONTS = {'mathcal', 'mathscr', 'mathfrak', 'mathbb', 'mathbf', 'boldsymbol', 'bm', 'mathsf',
         'mathit', 'mathtt', 'mathnormal', 'pmb'}
NAME_CMDS = {'mathrm', 'operatorname', 'text', 'textrm', 'textup', 'textit', 'textbf', 'textsf',
             'texttt', 'mbox', 'textnormal', 'emph', 'mathrm*', 'operatorname*'}
TEXT_GROUP_CMDS = {'tag', 'tag*', 'text', 'textrm', 'textup', 'textit', 'textbf', 'textsf', 'texttt', 'mbox',
                   'textnormal', 'emph', 'intertext', 'shortintertext', 'hbox', 'textsc'}
DECORATIONS = {'hat', 'widehat', 'tilde', 'widetilde', 'bar', 'overline', 'dot', 'ddot', 'dddot',
               'vec', 'check', 'breve', 'acute', 'grave', 'underline', 'mathring', 'overrightarrow',
               'overleftarrow', 'underbar'}
NAMED_OPS = set('''sin cos tan cot sec csc arcsin arccos arctan sinh cosh tanh coth log ln lg exp
max min sup inf lim liminf limsup det dim ker deg arg gcd hom Pr mod bmod pmod'''.split())
BIG_OPS = set('''sum prod coprod int iint iiint oint bigcup bigcap bigvee bigwedge bigoplus
bigotimes bigsqcup biguplus bigodot'''.split())
STRUCTURAL = set('''frac dfrac tfrac cfrac sqrt binom dbinom tbinom overset underset stackrel
substack boxed phantom hphantom vphantom displaystyle textstyle scriptstyle scriptscriptstyle
limits nolimits tag label nonumber notag ref eqref cite citep citet begin end hline cline
multicolumn multirow left right middle big Big bigg Bigg bigl bigr Bigl Bigr biggl biggr Biggl
Biggr overbrace underbrace not mathop mathbin mathrel mathord mathpunct mathopen mathclose
color textcolor hspace vspace quad qquad enspace thinspace negthinspace mkern mskip kern raisebox
smash mathstrut strut cdots ldots dots dotsc dotsb dotsm vdots ddots hdots colon ensuremath
arraystretch centering small footnotesize scriptsize large Large normalsize tiny noalign
allowbreak linebreak newline displaybreak lefteqn rule makebox fbox framebox tfrac genfrac
operatornamewithlimits xrightarrow xleftarrow xmapsto pm mp relax protect hfill hfil dotfill
leq geq le ge neq ne in notin ni subset subseteq subsetneq supset supseteq supsetneq to mapsto
rightarrow leftarrow Rightarrow Leftarrow leftrightarrow Leftrightarrow iff implies impliedby
longrightarrow longleftarrow Longrightarrow Longleftarrow longmapsto longleftrightarrow
Longleftrightarrow hookrightarrow hookleftarrow twoheadrightarrow rightharpoonup uparrow
downarrow updownarrow Uparrow Downarrow nearrow searrow swarrow nwarrow leadsto rightsquigarrow
circlearrowleft circlearrowright curvearrowright rightleftharpoons
sim simeq approx equiv cong propto perp parallel mid nmid ll gg lll ggg prec succ preceq succeq
models vdash dashv asymp doteq triangleq coloneqq eqqcolon vartriangleleft trianglelefteq
lesssim gtrsim leqslant geqslant nleq ngeq neg lnot land lor forall exists nexists therefore because
cdot times circ ast bullet oplus ominus otimes oslash odot cup cap sqcup sqcap uplus setminus
smallsetminus wedge vee diamond div bigtriangleup bigtriangledown triangleleft triangleright amalg
wr dotplus ltimes rtimes boxplus boxtimes langle rangle lvert rvert lVert rVert vert Vert lfloor
rfloor lceil rceil lbrace rbrace backslash prime emptyset textbackslash S P dag copyright
quad ldotp cdotp vcentcolon Bbbk complement mho angle measuredangle sphericalangle diagup diagdown
blacksquare blacktriangle lozenge blacklozenge bigstar circledS varkappa wideparen
underset overset sideset tbinom pmatrix bmatrix vmatrix matrix cases hookrightarrow restriction
upharpoonright downharpoonright rightrightarrows leftleftarrows nrightarrow nleftarrow
nRightarrow nLeftrightarrow nsubseteq nsupseteq subsetneqq supsetneqq lessgtr gtrless
unlhd unrhd lhd rhd sqsubseteq sqsupseteq sqsubset sqsupset ncong nsim npreceq nsucceq
displaylimits bigm Bigm biggm Biggm vphantom ast ell@ linewidth textwidth columnwidth qedhere frown smile'''.split())
# Anciennes commandes de police (bascule) : les lettres qui suivent forment un nom romain.
OLD_FONT_SWITCHES = {'rm': 'rm', 'it': 'it', 'bf': 'bf', 'sf': 'sf', 'tt': 'tt'}
# Commandes dont les arguments ne sont pas mathématiques (nombre de groupes à ignorer).
SKIP_ARGS = {'label': 1, 'ref': 1, 'eqref': 1, 'cite': 1, 'citep': 1, 'citet': 1,
             'end': 1, 'hspace': 1, 'vspace': 1, 'hspace*': 1, 'vspace*': 1, 'color': 1,
             'textcolor': 1, 'rule': 2, 'raisebox': 1, 'multicolumn': 2, 'multirow': 2, 'mkern': 0,
             'kern': 0, 'mskip': 0, 'makebox': 0, 'arraystretch': 0, 'genfrac': 4}
TEXT_ENVS_IN_MATH = {'minipage', 'tabular', 'itemize', 'enumerate', 'center'}
TABULAR_ENVS = {'array', 'tabular', 'alignat', 'alignat*', 'alignedat', 'tabularx', 'longtable', 'subarray'}
# Commandes de délimitation ou d'espacement à un caractère.
ONECHAR_CS = set(',;:!> |{}_$&%#\\/\'"-.=()[]^~@`*0123456789+')
MATH_ENVS = {'equation', 'equation*', 'align', 'align*', 'gather', 'gather*', 'multline',
             'multline*', 'eqnarray', 'eqnarray*', 'displaymath', 'math', 'flalign', 'flalign*',
             'alignat', 'alignat*', 'dmath', 'dmath*'}
VERBATIM_ENVS = {'verbatim', 'verbatim*', 'lstlisting', 'minted', 'Verbatim'}
SECTION_CMDS = ['tome', 'part', 'chapter', 'section', 'subsection', 'subsubsection', 'paragraph']
# Environnements conteneurs : ils ne « possèdent » pas les labels qu'ils renferment.
CONTAINER_ENVS = {'document', 'itemize', 'enumerate', 'description', 'center', 'minipage', 'quote',
                  'quotation', 'abstract', 'flushleft', 'flushright', 'scope', 'tikzpicture',
                  'appendices', 'encadre', 'proof', 'longtable', 'tabular', 'array', 'small'}

CS_RE = re.compile(r'\\([A-Za-z@]+\*?|.)', re.S)


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def balanced_group(s, i):
    """s[i] == '{' : renvoie l'indice suivant l'accolade fermante correspondante."""
    assert s[i] == '{'
    d = 0
    j = i
    n = len(s)
    while j < n:
        c = s[j]
        if c == '\\':
            j += 2
            continue
        if c == '{':
            d += 1
        elif c == '}':
            d -= 1
            if d == 0:
                return j + 1
        j += 1
    return -1


def skip_ws(s, i):
    while i < len(s) and s[i] in ' \t\n\r':
        i += 1
    return i


class LineIndex:
    def __init__(self, text):
        self.starts = [0]
        for m in re.finditer('\n', text):
            self.starts.append(m.end())

    def line_col(self, off):
        import bisect
        k = bisect.bisect_right(self.starts, off) - 1
        return k + 1, off - self.starts[k] + 1


def mask_comments_and_verbatim(text):
    """Renvoie (texte masqué, commentaires, verbatims). Les offsets sont préservés."""
    out = list(text)
    comments, verbs = [], []
    i, n = 0, len(text)
    vb = re.compile(r'\\begin\{(%s)\}' % '|'.join(re.escape(e) for e in VERBATIM_ENVS))
    while i < n:
        c = text[i]
        if c == '\\':
            m = vb.match(text, i)
            if m:
                endtag = '\\end{%s}' % m.group(1)
                j = text.find(endtag, m.end())
                j = n if j < 0 else j + len(endtag)
                verbs.append((i, j, m.group(1)))
                for k in range(i, j):
                    if out[k] != '\n':
                        out[k] = ' '
                i = j
                continue
            if text.startswith('\\verb', i) and i + 5 < n and not text[i + 5].isalpha():
                d = text[i + 5]
                j = text.find(d, i + 6)
                j = n if j < 0 else j + 1
                verbs.append((i, j, 'verb'))
                for k in range(i, j):
                    out[k] = ' '
                i = j
                continue
            i += 2
            continue
        if c == '%':
            j = text.find('\n', i)
            j = n if j < 0 else j
            comments.append((i, j))
            for k in range(i, j):
                out[k] = ' '
            i = j
            continue
        i += 1
    return ''.join(out), comments, verbs


def find_math_segments(t, base=0, comment_mode=False):
    """Segments mathématiques dans un texte déjà masqué.

    Renvoie une liste de dict(start, end, inner_start, inner_end, kind).
    Les groupes textuels (\\text{...}) internes sont traités plus tard par le tokeniseur.
    """
    segs, problems = [], []
    i, n = 0, len(t)
    envre = re.compile(r'\\begin\{([A-Za-z]+\*?)\}')
    while i < n:
        c = t[i]
        if c == '\\':
            if t.startswith('\\(', i) or t.startswith('\\[', i):
                closer = '\\)' if t[i + 1] == '(' else '\\]'
                j = find_closer(t, i + 2, closer)
                if j < 0:
                    problems.append((base + i, 'délimiteur %s non fermé' % t[i:i + 2]))
                    i += 2
                    continue
                segs.append(dict(start=base + i, end=base + j + 2, inner_start=base + i + 2,
                                 inner_end=base + j, kind='inline' if closer == '\\)' else 'display'))
                i = j + 2
                continue
            m = envre.match(t, i)
            if m and m.group(1) in MATH_ENVS:
                endtag = '\\end{%s}' % m.group(1)
                j = t.find(endtag, m.end())
                if j < 0:
                    problems.append((base + i, 'environnement %s non fermé' % m.group(1)))
                    i = m.end()
                    continue
                segs.append(dict(start=base + i, end=base + j + len(endtag), inner_start=base + m.end(),
                                 inner_end=base + j, kind='env:' + m.group(1)))
                i = j + len(endtag)
                continue
            i += 2
            continue
        if c == '$':
            if t.startswith('$$', i):
                j = t.find('$$', i + 2)
                if j < 0:
                    problems.append((base + i, '$$ non fermé'))
                    i += 2
                    continue
                segs.append(dict(start=base + i, end=base + j + 2, inner_start=base + i + 2,
                                 inner_end=base + j, kind='display$$'))
                i = j + 2
                continue
            j = find_dollar_closer(t, i + 1)
            if j < 0:
                problems.append((base + i, '$ non fermé'))
                i += 1
                continue
            segs.append(dict(start=base + i, end=base + j + 1, inner_start=base + i + 1,
                             inner_end=base + j, kind='inline'))
            i = j + 1
            continue
        i += 1
    return segs, problems


def find_closer(t, i, closer):
    n = len(t)
    while i < n:
        if t[i] == '\\':
            if t.startswith(closer, i):
                return i
            i += 2
            continue
        i += 1
    return -1


def find_dollar_closer(t, i):
    """Cherche le $ fermant, en sautant les groupes \\text{...} (qui peuvent contenir des $)."""
    n = len(t)
    while i < n:
        c = t[i]
        if c == '\\':
            m = CS_RE.match(t, i)
            name = m.group(1)
            if name in TEXT_GROUP_CMDS:
                k = skip_ws(t, m.end())
                if k < n and t[k] == '{':
                    e = balanced_group(t, k)
                    if e > 0:
                        i = e
                        continue
            i = m.end()
            continue
        if c == '$':
            return i
        i += 1
    return -1


# ---------------------------------------------------------------------------
# Macros utilisateur
# ---------------------------------------------------------------------------

NEWCMD_RE = re.compile(r'\\(newcommand|renewcommand|providecommand)\*?\s*\{?\s*\\([A-Za-z@]+)\s*\}?\s*(\[(\d)\])?\s*(\[[^\]]*\])?\s*\{')
DMO_RE = re.compile(r'\\DeclareMathOperator(\*?)\s*\{\s*\\([A-Za-z@]+)\s*\}\s*\{')


def parse_macros(masked):
    macros = {}
    for m in NEWCMD_RE.finditer(masked):
        b = m.end() - 1
        e = balanced_group(masked, b)
        if e < 0:
            continue
        nargs = int(m.group(4)) if m.group(4) else 0
        macros[m.group(2)] = dict(name=m.group(2), nargs=nargs, body=masked[b + 1:e - 1],
                                  def_start=m.start(), def_end=e, body_start=b + 1, kind=m.group(1))
    for m in DMO_RE.finditer(masked):
        b = m.end() - 1
        e = balanced_group(masked, b)
        macros[m.group(2)] = dict(name=m.group(2), nargs=0, body='\\operatorname%s{%s}' % (m.group(1), masked[b + 1:e - 1]),
                                  def_start=m.start(), def_end=e, body_start=b + 1, kind='DeclareMathOperator')
    return macros


def is_math_macro(md):
    """Macro à développer dans les mathématiques : sans argument et dont le corps est mathématique."""
    if md['nargs'] != 0:
        return False
    body = md['body']
    if '$' in body or '\\node' in body or '\\draw' in body:
        return False
    return bool(re.search(r'\\(mathcal|mathfrak|mathscr|mathbb|mathbf|operatorname|mathrm|'
                          + '|'.join(sorted(GREEK)) + r')(?![A-Za-z])', body))


# ---------------------------------------------------------------------------
# Tokenisation mathématique
# ---------------------------------------------------------------------------

_UID = [0]


def uid(atom):
    """Identifiant séquentiel stable d'un atome (id() Python peut être réutilisé)."""
    if '_uid' not in atom:
        _UID[0] += 1
        atom['_uid'] = _UID[0]
    return atom['_uid']


class Tok:
    __slots__ = ('kind', 'val', 'start', 'end')

    def __init__(self, kind, val, start, end):
        self.kind, self.val, self.start, self.end = kind, val, start, end

    def __repr__(self):
        return '%s:%r' % (self.kind, self.val)


def tokenize(s, base):
    toks, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == '\\':
            m = CS_RE.match(s, i)
            if not m:
                i += 1
                continue
            toks.append(Tok('cs', m.group(1), base + i, base + m.end()))
            i = m.end()
            continue
        if c in ' \t\n\r~':
            i += 1
            continue
        if c.isalpha():
            toks.append(Tok('letter', c, base + i, base + i + 1))
        elif c.isdigit():
            toks.append(Tok('digit', c, base + i, base + i + 1))
        elif c == '{':
            toks.append(Tok('open', c, base + i, base + i + 1))
        elif c == '}':
            toks.append(Tok('close', c, base + i, base + i + 1))
        elif c in '^_':
            toks.append(Tok('script', c, base + i, base + i + 1))
        elif c == "'":
            toks.append(Tok('prime', c, base + i, base + i + 1))
        elif c == '$':
            toks.append(Tok('dollar', c, base + i, base + i + 1))
        else:
            toks.append(Tok('other', c, base + i, base + i + 1))
        i += 1
    return toks


def group_end(toks, k):
    """toks[k] est 'open' : indice suivant le 'close' correspondant."""
    d = 0
    for j in range(k, len(toks)):
        if toks[j].kind == 'open':
            d += 1
        elif toks[j].kind == 'close':
            d -= 1
            if d == 0:
                return j + 1
    return len(toks)


def arg_span(toks, k):
    """Argument d'une commande à la position k : renvoie (debut, fin) des tokens (fin exclue)."""
    if k >= len(toks):
        return k, k
    if toks[k].kind == 'open':
        return k, group_end(toks, k)
    return k, k + 1


def src(text, toks, a, b, base):
    if a >= b:
        return ''
    return text[toks[a].start - base:toks[b - 1].end - base]


def strip_braces(x):
    x = x.strip()
    while x.startswith('{') and x.endswith('}') and balanced_group(x, 0) == len(x):
        x = x[1:-1].strip()
    return x


def norm_ws(x):
    return re.sub(r'\s+', ' ', x).strip()


class MathParser:
    """Extrait les atomes d'un segment mathématique."""

    def __init__(self, text, base, macros, ctx, unknown, textsegs):
        self.text = text          # texte complet du fichier (masqué)
        self.base = 0
        self.macros = macros
        self.ctx = ctx
        self.unknown = unknown    # Counter des commandes non reconnues
        self.textsegs = textsegs  # groupes textuels internes renfermant des maths
        self.atoms = []

    def parse(self, start, end, level=0, parent=None, position='corps'):
        seg = self.text[start:end]
        toks = tokenize(seg, start)
        self._parse_toks(toks, level, parent, position)
        return self.atoms

    def _parse_toks(self, toks, level, parent, position):
        k, n = 0, len(toks)
        while k < n:
            t = toks[k]
            atom = None
            if t.kind == 'letter':
                atom = dict(source=t.val, base=t.val, nature='latine', police='', var=False, famille=t.val,
                            glyphe=t.val, start=t.start, end=t.end)
                k += 1
            elif t.kind == 'cs':
                name = t.val
                if name in GREEK:
                    fam = name[3:] if name.startswith('var') and name[3:] in GREEK else name
                    if name == 'varkappa':
                        fam = 'kappa'
                    atom = dict(source='\\' + name, base='\\' + name, nature='grecque', police='',
                                var=name.startswith('var'), famille=fam, glyphe='\\' + name,
                                start=t.start, end=t.end)
                    k += 1
                elif name in LETTERLIKE:
                    atom = dict(source='\\' + name, base='\\' + name, nature='lettre_speciale', police='',
                                var=False, famille=name, glyphe='\\' + name, start=t.start, end=t.end)
                    k += 1
                elif name in CONSTANTS:
                    atom = dict(source='\\' + name, base='\\' + name, nature='symbole_constant', police='',
                                var=False, famille=name, glyphe='\\' + name, start=t.start, end=t.end)
                    k += 1
                elif name in FONTS:
                    a, b = arg_span(toks, k + 1)
                    inner = toks[a + 1:b - 1] if (a < len(toks) and toks[a].kind == 'open') else toks[a:b]
                    content = strip_braces(src(self.text, toks, a, b, 0))
                    fam_letters = [x for x in inner if x.kind in ('letter', 'cs', 'digit')]
                    if len(fam_letters) == 1 and fam_letters[0].kind == 'letter':
                        famille = fam_letters[0].val
                        nature = 'police'
                    elif len(fam_letters) == 1 and fam_letters[0].kind == 'cs' and fam_letters[0].val in GREEK:
                        v = fam_letters[0].val
                        famille = v[3:] if v.startswith('var') and v[3:] in GREEK else v
                        nature = 'police_grecque'
                    elif len(fam_letters) == 1 and fam_letters[0].kind == 'digit':
                        famille = fam_letters[0].val
                        nature = 'police'
                    else:
                        famille = content
                        nature = 'police_mot'
                    glyph = '\\%s{%s}' % (name, content)
                    atom = dict(source=src(self.text, toks, k, b, 0), base=glyph, nature=nature, police=name,
                                var=content.startswith('\\var'), famille=famille, glyphe=glyph,
                                start=t.start, end=toks[b - 1].end if b > k + 1 else t.end)
                    k = b
                elif name in ('mathrm', 'operatorname', 'operatorname*'):
                    a, b = arg_span(toks, k + 1)
                    content = strip_braces(src(self.text, toks, a, b, 0))
                    single = re.fullmatch(r'[A-Za-z]', content)
                    glyph = '\\%s{%s}' % (name, content)
                    atom = dict(source=src(self.text, toks, k, b, 0), base=glyph,
                                nature='romaine' if single else 'nom_operateur', police=name.rstrip('*'),
                                var=False, famille=content if single else 'op:' + content, glyphe=glyph,
                                start=t.start, end=toks[b - 1].end if b > k + 1 else t.end)
                    k = b
                elif name == 'parbox':
                    a, b = arg_span(toks, k + 1)
                    a2, b2 = arg_span(toks, b)
                    if a2 < len(toks) and toks[a2].kind == 'open' and b2 - 1 > a2:
                        self.textsegs.append((toks[a2].end, toks[b2 - 1].start, level, parent))
                    self.unknown['texte_en_mode_math:parbox'] += 1
                    k = b2
                    continue
                elif name in TEXT_GROUP_CMDS:
                    a, b = arg_span(toks, k + 1)
                    # groupe textuel : pas d'atome ; maths imbriquées éventuelles
                    if a < len(toks) and toks[a].kind == 'open' and b - 1 > a:
                        s0, e0 = toks[a].end, toks[b - 1].start
                        self.textsegs.append((s0, e0, level, parent))
                    k = b
                    continue
                elif name in NAMED_OPS:
                    atom = dict(source='\\' + name, base='\\' + name, nature='operateur_nomme', police='',
                                var=False, famille='op:' + name, glyphe='\\' + name, start=t.start, end=t.end)
                    k += 1
                elif name in BIG_OPS:
                    atom = dict(source='\\' + name, base='\\' + name, nature='grand_operateur', police='',
                                var=False, famille='op:' + name, glyphe='\\' + name, start=t.start, end=t.end)
                    k += 1
                elif name in DECORATIONS:
                    a, b = arg_span(toks, k + 1)
                    s0 = e0 = None
                    if a < b:
                        s0 = toks[a].start + (1 if toks[a].kind == 'open' else 0)
                        e0 = toks[b - 1].end - (1 if toks[a].kind == 'open' else 0)
                        dry = MathParser(self.text, 0, self.macros, self.ctx, collections.Counter(), [])
                        dry_atoms = dry.parse(s0, e0, level, parent, position)
                    else:
                        dry_atoms = []
                    top = [x for x in dry_atoms if x['niveau'] == level]
                    single = len(top) == 1 and not top[0]['indice'] and not top[0]['exposant']
                    sub = MathParser(self.text, 0, self.macros, self.ctx, self.unknown, self.textsegs)
                    inner_atoms = sub.parse(s0, e0, level, parent, position) if (single and s0 is not None) else []
                    top = [x for x in inner_atoms if x['niveau'] == level]
                    if single and top:
                        x = top[0]
                        x['decoration'] = ('\\' + name + ('+' + x['decoration'] if x['decoration'] else ''))
                        x['source'] = src(self.text, toks, k, b, 0)
                        x['start'] = t.start
                        atom = x
                        sub_atoms = [y for y in inner_atoms if y is not x]
                        k = b
                        k = self._scripts(toks, k, atom, level)
                        self._emit(atom, level, parent, position)
                        for y in sub_atoms:
                            self.atoms.append(y)
                        continue
                    # décoration d'une expression : atome composite + atomes internes
                    content = src(self.text, toks, a, b, 0)
                    atom = dict(source=src(self.text, toks, k, b, 0), base='\\%s{%s}' % (name, strip_braces(content)),
                                nature='expression_decoree', police='', var=False,
                                famille='deco:' + name, glyphe='\\%s{...}' % name, start=t.start,
                                end=toks[b - 1].end if b > k else t.end, decoration='\\' + name,
                                composite_force=True)
                    k = b
                    k = self._scripts(toks, k, atom, level)
                    self._emit(atom, level, parent, position)
                    if s0 is not None:
                        sub = MathParser(self.text, 0, self.macros, self.ctx, self.unknown, self.textsegs)
                        for y in sub.parse(s0, e0, level + 1, uid(atom), 'argument_decoration'):
                            self.atoms.append(y)
                    continue
                elif name in self.macros and self.macros[name]['nargs'] == 0 and is_math_macro(self.macros[name]):
                    body = self.macros[name]['body']
                    # développement contrôlé : analyse du corps comme un segment isolé
                    sub = MathParser(body, 0, {}, self.ctx, collections.Counter(), [])
                    inner = sub.parse(0, len(body), 0, None, 'corps')
                    top = [x for x in inner if x['niveau'] == 0]
                    x = top[0] if top else None
                    atom = dict(source='\\' + name, base=norm_ws(body), nature='macro_utilisateur',
                                police=x['police'] if x else '', var=x['var'] if x else False,
                                famille=x['famille'] if x else 'macro:' + name, glyphe=x['glyphe'] if x else norm_ws(body),
                                start=t.start, end=t.end, developpe=norm_ws(body),
                                macro_scripts=(x['indice'], x['exposant']) if x else ('', ''))
                    k += 1
                elif name in self.macros:
                    # macro utilisateur avec arguments ou non mathématique : signalée, non développée
                    self.unknown['macro_non_developpee:\\' + name] += 1
                    k += 1
                    continue
                elif name in OLD_FONT_SWITCHES:
                    j = k + 1
                    while j < len(toks) and toks[j].kind == 'letter':
                        j += 1
                    if j == k + 1:
                        k += 1
                        continue
                    content = ''.join(x.val for x in toks[k + 1:j])
                    single = len(content) == 1
                    glyph = '{\\%s %s}' % (name, content)
                    atom = dict(source=src(self.text, toks, k, j, 0), base=glyph,
                                nature='romaine' if single else 'nom_operateur', police=name, var=False,
                                famille=content if single else 'op:' + content, glyphe=glyph,
                                start=t.start, end=toks[j - 1].end, statut='bascule_police')
                    k = j
                elif name == 'begin':
                    a, b = arg_span(toks, k + 1)
                    envn = strip_braces(src(self.text, toks, a, b, 0))
                    k = b
                    if envn in TEXT_ENVS_IN_MATH:
                        # retour au mode texte : on saute jusqu'au \end correspondant, maths internes analysées à part
                        depth, j = 1, k
                        while j < len(toks):
                            if toks[j].kind == 'cs' and toks[j].val in ('begin', 'end'):
                                aa, bb = arg_span(toks, j + 1)
                                if strip_braces(src(self.text, toks, aa, bb, 0)) == envn:
                                    depth += 1 if toks[j].val == 'begin' else -1
                                    if depth == 0:
                                        break
                                j = bb
                                continue
                            j += 1
                        if k < len(toks) and toks[k].kind == 'open':  # largeur {0.86\linewidth}
                            k = group_end(toks, k)
                        if k < j:
                            self.textsegs.append((toks[k].start, toks[j - 1].end, level, parent))
                        self.unknown['texte_en_mode_math:' + envn] += 1
                        k = arg_span(toks, j + 1)[1] if j < len(toks) else j
                        continue
                    if envn in TABULAR_ENVS:
                        if k < len(toks) and toks[k].kind == 'other' and toks[k].val == '[':
                            while k < len(toks) and not (toks[k].kind == 'other' and toks[k].val == ']'):
                                k += 1
                            k += 1
                        a, b = arg_span(toks, k)
                        k = b
                    continue
                elif name in SKIP_ARGS:
                    k += 1
                    for _ in range(SKIP_ARGS[name]):
                        a, b = arg_span(toks, k)
                        k = b
                    continue
                elif name in STRUCTURAL or name in ONECHAR_CS or len(name) == 1:
                    k += 1
                    continue
                else:
                    self.unknown['\\' + name] += 1
                    self.atoms.append(dict(source='\\' + name, base='\\' + name, nature='non_reconnu', police='',
                                           var=False, famille='?\\' + name, glyphe='\\' + name, start=t.start,
                                           end=t.end, niveau=level, parent_ref=parent, position=position,
                                           indice='', exposant='', primes=0, decoration='', statut='non_reconnu',
                                           ref=None))
                    self.atoms[-1]['ref'] = uid(self.atoms[-1])
                    k += 1
                    continue
            elif t.kind == 'script':
                # script sans base symbolique (après une parenthèse, un chiffre…) : on analyse son contenu
                a, b = arg_span(toks, k + 1)
                if a < b:
                    s0 = toks[a].start + (1 if toks[a].kind == 'open' else 0)
                    e0 = toks[b - 1].end - (1 if toks[a].kind == 'open' else 0)
                    sub = MathParser(self.text, 0, self.macros, self.ctx, self.unknown, self.textsegs)
                    for y in sub.parse(s0, e0, level + 1, None, 'script_orphelin'):
                        self.atoms.append(y)
                k = b
                continue
            else:
                k += 1
                continue
            if atom is None:
                continue
            atom.setdefault('decoration', '')
            k = self._scripts(toks, k, atom, level)
            self._emit(atom, level, parent, position)
        return self.atoms

    def _scripts(self, toks, k, atom, level):
        """Collecte primes, indices et exposants qui suivent la base."""
        atom.setdefault('indice', '')
        atom.setdefault('exposant', '')
        atom.setdefault('primes', 0)
        atom.setdefault('children', [])
        n = len(toks)
        while k < n:
            t = toks[k]
            if t.kind == 'prime':
                atom['primes'] += 1
                atom['end'] = t.end
                k += 1
                continue
            if t.kind == 'cs' and t.val == 'prime':
                atom['primes'] += 1
                atom['end'] = t.end
                k += 1
                continue
            if t.kind == 'cs' and t.val in ('limits', 'nolimits'):
                k += 1
                continue
            if t.kind == 'script':
                a, b = arg_span(toks, k + 1)
                if a >= b:
                    k += 1
                    continue
                content = src(self.text, toks, a, b, 0)
                key = 'indice' if t.val == '_' else 'exposant'
                atom[key] = (atom[key] + ',' if atom[key] else '') + strip_braces(content)
                s0 = toks[a].start + (1 if toks[a].kind == 'open' else 0)
                e0 = toks[b - 1].end - (1 if toks[a].kind == 'open' else 0)
                atom['children'].append((s0, e0, key))
                atom['end'] = toks[b - 1].end
                k = b
                continue
            break
        return k

    def _emit(self, atom, level, parent, position):
        atom['niveau'] = level
        atom['parent_ref'] = parent
        atom['position'] = position
        atom.setdefault('statut', 'ok')
        atom['ref'] = uid(atom)
        atom['source'] = self.text[atom['start']:atom['end']]
        self.atoms.append(atom)
        for (s0, e0, key) in atom.pop('children', []):
            sub = MathParser(self.text, 0, self.macros, self.ctx, self.unknown, self.textsegs)
            for y in sub.parse(s0, e0, level + 1, uid(atom), key):
                self.atoms.append(y)


SIMPLE_INDEX_ATOM = {'latine', 'romaine'}


def classify(atom, children):
    """Classe lexicale (aucune interprétation sémantique)."""
    variant = bool(atom['police'] and atom['police'] not in ('mathrm', 'operatorname')) or atom['var'] \
        or bool(atom['decoration']) or atom['primes'] > 0
    scripts = atom['indice'] or atom['exposant']
    if atom['nature'] == 'macro_utilisateur':
        si, se = atom.get('macro_scripts', ('', ''))
        scripts = scripts or si or se
    composite = atom.get('composite_force', False)
    if scripts and not composite:
        direct = [c for c in children if c['niveau'] == atom['niveau'] + 1]
        nested = any(c for c in children if c['niveau'] > atom['niveau'] + 1)
        rich = [c for c in direct if c['nature'] not in SIMPLE_INDEX_ATOM]
        expr = atom['indice'] + ' ' + atom['exposant']
        has_struct = bool(re.search(r'\\(frac|dfrac|tfrac|sum|prod|int|sqrt|left|bigl?|in|le|leq|ge|geq|to|mapsto|cup|cap)(?![A-Za-z])', expr))
        if nested or (len(direct) >= 2 and rich) or has_struct or any(c['decoration'] for c in direct):
            composite = True
    if composite:
        return 'composite', variant
    if scripts:
        return 'indexe', variant
    if variant:
        return 'variante_typographique', True
    return 'nu', False


STRUCT_RE = re.compile(r'\\(frac|dfrac|tfrac|sum|prod|int|sqrt|left|bigl?|in|le|leq|ge|geq|to|mapsto|cup|cap)(?![A-Za-z])')


def secondary_attributes(atom, children):
    """Attributs secondaires (B2a) : n'influencent pas la classe principale.

    Renvoie dict(composite_portee, motifs_composite, composants_indice, composants_exposant,
    attributs_secondaires). Les motifs sont évalués séparément sur l'indice et sur l'exposant.
    """
    lvl = atom['niveau']
    direct = [c for c in children if c['niveau'] == lvl + 1]
    motifs = {'indice': [], 'exposant': []}
    comp = {}
    for pos in ('indice', 'exposant'):
        d = [c for c in direct if c['position'] == pos]
        comp[pos] = ' '.join(c['glyphe'] for c in d)
        ids = {c['ref'] for c in d}
        deeper = [c for c in children if c['niveau'] > lvl + 1]
        # un descendant plus profond appartient à cette position si son ancêtre direct y est
        if any(c.get('parent_ref') in ids for c in deeper):
            motifs[pos].append('script_imbrique')
        if len(d) >= 2 and any(c['nature'] not in SIMPLE_INDEX_ATOM for c in d):
            motifs[pos].append('composants_multiples_non_latins')
        if atom[pos] and STRUCT_RE.search(atom[pos]):
            motifs[pos].append('structure')
        if any(c['decoration'] for c in d):
            motifs[pos].append('decoration')
    portee = [p for p in ('indice', 'exposant') if motifs[p]]
    allm = ['%s:%s' % (p, m) for p in ('indice', 'exposant') for m in motifs[p]]
    # critère porté par la combinaison indice + exposant (ex. \mathcal R_X^\rho)
    if not portee and len(direct) >= 2 and any(c['nature'] not in SIMPLE_INDEX_ATOM for c in direct):
        portee = ['indice+exposant']
        allm.append('combinaison:composants_multiples_non_latins')
    if atom.get('composite_force'):
        portee = ['argument_decoration'] + portee
        allm = ['argument_decoration:expression_decoree'] + allm
    sec = []
    if atom['police'] and atom['police'] not in ('mathrm', 'operatorname'):
        sec.append('police=' + atom['police'])
    if atom['var']:
        sec.append('variante_var')
    if atom['decoration']:
        sec.append('decoration=' + atom['decoration'])
    if atom['primes']:
        sec.append('primes=%d' % atom['primes'])
    if atom['indice']:
        sec.append('indice')
    if atom['exposant']:
        sec.append('exposant')
    if atom['nature'] == 'macro_utilisateur':
        sec.append('macro')
    return dict(composite_portee='+'.join(portee), motifs_composite=';'.join(allm),
                composants_indice=comp['indice'], composants_exposant=comp['exposant'],
                attributs_secondaires=';'.join(sec))


# ---------------------------------------------------------------------------
# Structure du document : sections, environnements, labels
# ---------------------------------------------------------------------------

def document_structure(masked):
    secs = []
    secre = re.compile(r'\\(%s)\*?\s*(\[[^\]]*\])?\s*\{' % '|'.join(SECTION_CMDS))
    for m in secre.finditer(masked):
        b = m.end() - 1
        e = balanced_group(masked, b)
        if e < 0:
            continue
        secs.append((m.start(), SECTION_CMDS.index(m.group(1)), norm_ws(masked[b + 1:e - 1])[:90], b + 1, e - 1))
    envs, stack = [], []
    for m in re.finditer(r'\\(begin|end)\s*\{([A-Za-z]+\*?)\}', masked):
        if m.group(1) == 'begin':
            stack.append((m.group(2), m.start()))
        else:
            for j in range(len(stack) - 1, -1, -1):
                if stack[j][0] == m.group(2):
                    name, s = stack.pop(j)
                    envs.append(dict(name=name, start=s, end=m.end(), labels=[]))
                    break
    labels = []
    for m in re.finditer(r'\\label\s*\{([^}]*)\}', masked):
        if '#' not in m.group(1):
            labels.append((m.start(), m.group(1)))
    for m in re.finditer(r'\\resultstep\s*\{([^}]*)\}', masked):
        labels.append((m.start(), m.group(1)))
    for m in re.finditer(r'\\resultheading\s*\{', masked):
        e1 = balanced_group(masked, m.end() - 1)
        k = skip_ws(masked, e1)
        if k < len(masked) and masked[k] == '{':
            e2 = balanced_group(masked, k)
            labels.append((m.start(), masked[k + 1:e2 - 1].strip()))
    labels.sort()
    envs.sort(key=lambda e: (e['start'], -e['end']))
    for off, lab in labels:
        inner = None
        for e in envs:
            if e['name'] in CONTAINER_ENVS:
                continue
            if e['start'] <= off < e['end'] and (inner is None or e['start'] >= inner['start']):
                inner = e
        if inner is not None:
            inner['labels'].append(lab)
    return secs, envs, labels


def locate(off, secs, envs, labels):
    path = [None] * len(SECTION_CMDS)
    for s, lvl, title, _, _ in secs:
        if s > off:
            break
        path[lvl] = title
        for j in range(lvl + 1, len(path)):
            path[j] = None
    section = ' > '.join(p for p in path if p)
    enclosing = [e for e in envs if e['start'] <= off < e['end']]
    enclosing.sort(key=lambda e: e['start'])
    env_names = [e['name'] for e in enclosing if e['name'] != 'document']
    label, anchor = '', ''
    for e in reversed(enclosing):
        if e['labels']:
            label, anchor = e['labels'][0], 'env:' + e['name']
            break
    if not label:
        prev = [lab for o, lab in labels if o <= off]
        if prev:
            label, anchor = prev[-1], 'precedent'
    title_ctx = any(a <= off < b for _, _, _, a, b in secs)
    return section, '/'.join(env_names), label, anchor, title_ctx


# ---------------------------------------------------------------------------
# Extraction d'un fichier
# ---------------------------------------------------------------------------

def extract_file(path, relpath, corpus, volume, macros, stats):
    raw = open(path, encoding='utf-8').read()
    masked, comments, verbs = mask_comments_and_verbatim(raw)
    li = LineIndex(raw)
    secs, envs, labels = document_structure(masked)
    unknown = collections.Counter()
    segments, problems = find_math_segments(masked)
    # mathématiques dans les commentaires (corpus distinct, contexte « commentaire »)
    csegs = []
    for (a, b) in comments:
        sub, _ = find_math_segments(raw[a:b], base=a)
        for s in sub:
            s['kind'] = 'commentaire:' + s['kind']
        csegs.extend(sub)
    # corps des macros mathématiques : contexte « definition_macro »
    msegs = []
    for md in macros.values():
        if md.get('file') == relpath and is_math_macro(md):
            msegs.append(dict(start=md['body_start'], end=md['body_start'] + len(md['body']),
                              inner_start=md['body_start'], inner_end=md['body_start'] + len(md['body']),
                              kind='definition_macro'))
    stats['segments'][relpath] = collections.Counter(s['kind'] for s in segments)
    stats['problems'].extend((relpath,) + li.line_col(o) + (msg,) for o, msg in problems)
    stats['comments'][relpath] = len(comments)
    stats['verbatim'].extend((relpath, li.line_col(a)[0], li.line_col(b)[0], k) for a, b, k in verbs)
    occ, exprs = [], []
    # suppression des segments imbriqués (ex. $...$ à l'intérieur d'un environnement mathématique)
    allsegs = sorted(segments + csegs + msegs, key=lambda s: (s['start'], -s['end']))
    kept, last_end = [], -1
    for s in allsegs:
        if s['start'] < last_end and not s['kind'].startswith('commentaire'):
            continue
        kept.append(s)
        last_end = max(last_end, s['end'])
    expr_seen = collections.Counter()
    for s in kept:
        text_for = raw if s['kind'].startswith('commentaire') else masked
        textsegs = []
        mp = MathParser(text_for, 0, macros, None, unknown, textsegs)
        atoms = mp.parse(s['inner_start'], s['inner_end'])
        # maths imbriquées dans des groupes textuels
        guard = 0
        while textsegs and guard < 50:
            guard += 1
            pending, textsegs[:] = list(textsegs), []
            for (a, b, lvl, par) in pending:
                inner, _ = find_math_segments(text_for[a:b], base=a)
                for s2 in inner:
                    mp2 = MathParser(text_for, 0, macros, None, unknown, textsegs)
                    for y in mp2.parse(s2['inner_start'], s2['inner_end'], lvl, par, 'texte_imbrique'):
                        atoms.append(y)
        l1, c1 = li.line_col(s['start'])
        l2, _ = li.line_col(max(s['start'], s['end'] - 1))
        expr_src = raw[s['inner_start']:s['inner_end']]
        expr_id = '%s:%d:%d' % (relpath, l1, c1)
        exprs.append(dict(expr_id=expr_id, fichier=relpath, ligne_debut=l1, ligne_fin=l2, contexte=s['kind'],
                          nb_atomes=len(atoms), source=norm_ws(expr_src)))
        by_ref = {a['ref']: a for a in atoms}
        children = collections.defaultdict(list)
        for a in atoms:
            p = a.get('parent_ref')
            while p is not None and p in by_ref:
                children[p].append(a)
                p = by_ref[p].get('parent_ref')
        section, envname, label, anchor, in_title = locate(s['start'], secs, envs, labels)
        ordinal = collections.Counter()
        expr_key = (section, label, norm_ws(expr_src))
        expr_seen[expr_key] += 1
        for a in sorted(atoms, key=lambda a: (a['start'], a['niveau'])):
            cls, variant = classify(a, children.get(a['ref'], []))
            sec_attr = secondary_attributes(a, children.get(a['ref'], []))
            if a['nature'] == 'non_reconnu':
                cls = 'non_classe'
            la, ca = li.line_col(a['start'])
            ctx = s['kind']
            if in_title and not ctx.startswith('commentaire'):
                ctx += '+titre'
            ordinal[a['source']] += 1
            norm_expr = norm_ws(expr_src)
            fp = hashlib.sha1(('%s|%s|%s|%s|%d|%s|%d' % (relpath, section, label, norm_expr, expr_seen[expr_key], a['source'], ordinal[a['source']])).encode()).hexdigest()[:16]
            ex0 = max(0, a['start'] - 30)
            excerpt = norm_ws(raw[ex0:a['end'] + 30])
            occ.append(dict(
                corpus=corpus, volume=volume, fichier=relpath, ligne=la, colonne=ca,
                expr_ligne_debut=l1, expr_ligne_fin=l2, label_stable=label, type_ancre=anchor,
                section=section, environnement=envname, contexte=ctx, expr_id=expr_id,
                symbole_source=norm_ws(a['source']), forme_developpee=a.get('developpe', '') and norm_ws(a['developpe'] + (('_{' + a['indice'] + '}') if a['indice'] else '') + (('^{' + a['exposant'] + '}') if a['exposant'] else '')),
                glyphe=a['glyphe'], famille_lexicale=a['famille'], nature=a['nature'], police=a['police'],
                variante_var=int(bool(a['var'])), decoration=a['decoration'], primes=a['primes'],
                indice=norm_ws(a['indice']), exposant=norm_ws(a['exposant']), classe_lexicale=cls,
                variante=int(variant), niveau=a['niveau'], position=a['position'],
                porteur='' if a.get('parent_ref') is None or a['parent_ref'] not in by_ref else norm_ws(by_ref[a['parent_ref']]['glyphe']),
                statut_extraction=a.get('statut', 'ok'), empreinte=fp, extrait=excerpt, _ref=a['ref'], **sec_attr,
                _parent=a.get('parent_ref')))
    stats['unknown'][relpath] = unknown
    stats['math_chars'][relpath] = sum(s['inner_end'] - s['inner_start'] for s in kept if not s['kind'].startswith('commentaire'))
    return occ, exprs


def extract_markdown(path, relpath):
    """Extraction limitée des compagnons Markdown (mathématiques en Unicode dans des `...`)."""
    raw = open(path, encoding='utf-8').read()
    li = LineIndex(raw)
    occ = []
    for m in re.finditer(r'`([^`\n]+)`', raw):
        span = m.group(1)
        for g in re.finditer(r'[\u0370-\u03FF\U0001D400-\U0001D7FF\u2113\u2202\u2207\u221E]', span):
            l, c = li.line_col(m.start(1) + g.start())
            occ.append(dict(corpus='compagnon', volume='II', fichier=relpath, ligne=l, colonne=c,
                            symbole_source=g.group(0), contexte='markdown_code', extrait=span[:120],
                            statut_extraction='unicode_markdown'))
    return occ, len(re.findall(r'`[^`\n]+`', raw))


# ---------------------------------------------------------------------------
# Programme principal
# ---------------------------------------------------------------------------

OCC_FIELDS = ['id', 'corpus', 'volume', 'fichier', 'ligne', 'colonne', 'expr_ligne_debut', 'expr_ligne_fin',
              'label_stable', 'type_ancre', 'section', 'environnement', 'contexte', 'expr_id',
              'symbole_source', 'forme_developpee', 'glyphe', 'famille_lexicale', 'nature', 'police',
              'variante_var', 'decoration', 'primes', 'indice', 'exposant', 'classe_lexicale', 'variante',
              'niveau', 'position', 'porteur', 'parent_id', 'statut_extraction', 'empreinte', 'extrait',
              # attributs secondaires (décision B2a), ajoutés après les colonnes de référence G0.1
              'composite_portee', 'motifs_composite', 'composants_indice', 'composants_exposant',
              'attributs_secondaires']


def run(root, out):
    os.makedirs(out, exist_ok=True)
    stats = dict(segments={}, problems=[], comments={}, verbatim=[], unknown={}, math_chars={}, macros={})
    results = collections.defaultdict(list)
    expressions = collections.defaultdict(list)
    for corpus, volume, sub, files, master in CORPUS:
        mpath = os.path.join(root, sub, master)
        mmasked, _, _ = mask_comments_and_verbatim(open(mpath, encoding='utf-8').read())
        macros = parse_macros(mmasked)
        for md in macros.values():
            md['file'] = os.path.join(sub, master)
        stats['macros'][os.path.join(sub, master)] = {k: dict(nargs=v['nargs'], math=is_math_macro(v), body=norm_ws(v['body'])[:80]) for k, v in macros.items()}
        key = 'compagnons' if corpus == 'compagnon' else ('volI' if volume == 'I' else 'volII')
        for f in files:
            rel = os.path.join(sub, f)
            occ, ex = extract_file(os.path.join(root, rel), rel, corpus, volume, macros, stats)
            results[key].extend(occ)
            expressions[key].extend(ex)
    md_occ, md_spans = [], 0
    for rel in MD_COMPANIONS:
        o, n = extract_markdown(os.path.join(root, rel), rel)
        md_occ.extend(o)
        md_spans += n
    prefix = {'volI': 'I', 'volII': 'II', 'compagnons': 'C'}
    for key, occ in results.items():
        refmap = {}
        for i, o in enumerate(occ, 1):
            o['id'] = '%s-%06d' % (prefix[key], i)
            refmap[(o['fichier'], o['_ref'])] = o['id']
        for o in occ:
            o['parent_id'] = refmap.get((o['fichier'], o['_parent']), '') if o['_parent'] is not None else ''
        with open(os.path.join(out, 'occurrences_%s.csv' % key), 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=OCC_FIELDS, extrasaction='ignore')
            w.writeheader()
            w.writerows(occ)
        with open(os.path.join(out, 'expressions_%s.csv' % key), 'w', newline='', encoding='utf-8') as fh:
            w = csv.DictWriter(fh, fieldnames=['expr_id', 'fichier', 'ligne_debut', 'ligne_fin', 'contexte', 'nb_atomes', 'source'])
            w.writeheader()
            w.writerows(expressions[key])
    with open(os.path.join(out, 'occurrences_compagnons_markdown.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.DictWriter(fh, fieldnames=['corpus', 'volume', 'fichier', 'ligne', 'colonne', 'symbole_source', 'contexte', 'statut_extraction', 'extrait'])
        w.writeheader()
        w.writerows(md_occ)
    # familles
    fam = {}
    for key in ('volI', 'volII', 'compagnons'):
        for o in results[key]:
            if o['contexte'].startswith('commentaire') or o['contexte'] == 'definition_macro':
                continue
            f = fam.setdefault(o['famille_lexicale'], dict(glyphes=collections.Counter(), counts=collections.Counter()))
            f['glyphes'][o['glyphe']] += 1
            f['counts'][(key, o['classe_lexicale'])] += 1
            f['counts'][(key, 'total')] += 1
    classes = ['nu', 'indexe', 'variante_typographique', 'composite', 'non_classe']
    with open(os.path.join(out, 'symbol_families.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        hdr = ['famille_lexicale', 'glyphes']
        for key in ('volI', 'volII', 'compagnons'):
            hdr += ['%s_total' % key] + ['%s_%s' % (key, c) for c in classes]
        w.writerow(hdr)
        for name in sorted(fam, key=lambda n: -sum(fam[n]['counts'][(k, 'total')] for k in ('volI', 'volII'))):
            f = fam[name]
            row = [name, ' | '.join('%s (%d)' % g for g in f['glyphes'].most_common())]
            for key in ('volI', 'volII', 'compagnons'):
                row += [f['counts'][(key, 'total')]] + [f['counts'][(key, c)] for c in classes]
            w.writerow(row)
    # niveau du glyphe (la police distingue \\mathcal H de H, regroupés dans la même famille)
    gl = {}
    for key in ('volI', 'volII', 'compagnons'):
        for o in results[key]:
            if o['contexte'].startswith('commentaire') or o['contexte'] == 'definition_macro':
                continue
            g = gl.setdefault(o['glyphe'], dict(famille=o['famille_lexicale'], counts=collections.Counter(),
                                                indices=collections.Counter(), sources=collections.Counter()))
            g['counts'][(key, o['classe_lexicale'])] += 1
            g['counts'][(key, 'total')] += 1
            if o['indice']:
                g['indices'][o['indice']] += 1
            g['sources'][o['symbole_source'].split('_')[0].split('^')[0]] += 1
    with open(os.path.join(out, 'symbol_glyphs.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        hdr = ['glyphe', 'famille_lexicale']
        for key in ('volI', 'volII', 'compagnons'):
            hdr += ['%s_total' % key] + ['%s_%s' % (key, c) for c in classes]
        w.writerow(hdr + ['indices_principaux', 'formes_source'])
        for name in sorted(gl, key=lambda n: -sum(gl[n]['counts'][(k, 'total')] for k in ('volI', 'volII'))):
            g = gl[name]
            row = [name, g['famille']]
            for key in ('volI', 'volII', 'compagnons'):
                row += [g['counts'][(key, 'total')]] + [g['counts'][(key, c)] for c in classes]
            row += [' | '.join('%s (%d)' % x for x in g['indices'].most_common(8)),
                    ' | '.join('%s (%d)' % x for x in g['sources'].most_common(4))]
            w.writerow(row)
    # exclusions et constructions non traitées
    with open(os.path.join(out, 'exclusions.csv'), 'w', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        w.writerow(['type', 'fichier', 'ligne', 'detail'])
        for f, a, b, k in stats['verbatim']:
            w.writerow(['verbatim', f, '%d-%d' % (a, b), k])
        for p in stats['problems']:
            w.writerow(['segmentation', p[0], p[1], p[3]])
        for f, u in stats['unknown'].items():
            for name, n in sorted(u.items()):
                typ = ('macro_non_developpee' if name.startswith('macro_non') else
                       'texte_en_mode_math' if name.startswith('texte_en_mode_math') else 'commande_non_reconnue')
                w.writerow([typ, f, '', '%s (%d)' % (name, n)])
        for rel in MD_COMPANIONS:
            w.writerow(['markdown_extraction_limitee', rel, '', 'Unicode dans les spans de code seulement'])
    summary = dict(
        segments={k: dict(v) for k, v in stats['segments'].items()}, problems=stats['problems'],
        comments=stats['comments'], math_chars=stats['math_chars'],
        unknown={k: dict(v) for k, v in stats['unknown'].items()}, macros=stats['macros'],
        counts={k: len(v) for k, v in results.items()}, markdown=dict(occurrences=len(md_occ), code_spans=md_spans))
    with open(os.path.join(out, 'extraction_summary.json'), 'w', encoding='utf-8') as fh:
        json.dump(summary, fh, indent=1, ensure_ascii=False, sort_keys=True)
    return results, summary


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--root', default='.', help='racine du dépôt IWS')
    ap.add_argument('--out', default='audits/G0/G0_01_inventory')
    args = ap.parse_args()
    results, summary = run(args.root, args.out)
    for k, n in summary['counts'].items():
        print('%s : %d occurrences' % (k, n))
    return 0


if __name__ == '__main__':
    sys.exit(main())
