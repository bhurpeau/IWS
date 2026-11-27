"""Tests de l'extracteur G0.1 sur des fragments réels des sources IWS.

Exécution (depuis la racine du dépôt) :
    python3 -I -m unittest discover -s notations/scripts/tests -v
"""
import collections
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import extract_symbols as ex  # noqa: E402

VOL2_MACROS = r"""
\newcommand{\X}{\mathcal X}
\newcommand{\M}{\mathfrak M}
\newcommand{\Madm}{\mathfrak M^{\mathrm{adm}}}
\newcommand{\Reach}{\operatorname{Reach}}
\newcommand{\norm}[1]{\lVert #1\rVert}
"""


def atoms_of(math, macros_src=''):
    macros = ex.parse_macros(macros_src)
    text = '$' + math + '$'
    segs, problems = ex.find_math_segments(text)
    assert not problems, problems
    out = []
    for s in segs:
        mp = ex.MathParser(text, 0, macros, None, collections.Counter(), [])
        atoms = mp.parse(s['inner_start'], s['inner_end'])
        by_ref = {a['ref']: a for a in atoms}
        children = collections.defaultdict(list)
        for a in atoms:
            p = a.get('parent_ref')
            while p is not None and p in by_ref:
                children[p].append(a)
                p = by_ref[p].get('parent_ref')
        for a in atoms:
            cls, var = ex.classify(a, children.get(a['ref'], []))
            a['classe'] = cls
            out.append(a)
    return out


def top(atoms):
    return [a for a in atoms if a['niveau'] == 0]


class TestSymbols(unittest.TestCase):
    # IWS_PART_II.tex:889 — équation de perméabilité R1
    def test_r1_equation(self):
        a = atoms_of(r'\dot q=\rho(1-q)-\eta qgw')
        self.assertEqual([x['famille'] for x in top(a)], ['q', 'rho', 'q', 'eta', 'q', 'g', 'w'])
        self.assertEqual(a[0]['decoration'], r'\dot')
        self.assertEqual(a[0]['classe'], 'variante_typographique')
        self.assertEqual(a[1]['classe'], 'nu')

    # IWS_ANNEXE_E.tex:1238 — rayon spectral
    def test_rho_sp_is_indexed_not_bare(self):
        a = atoms_of(r'\rho_{\mathrm{sp}}(\mathcal M_g)<1')
        t = top(a)
        self.assertEqual(t[0]['glyphe'], r'\rho')
        self.assertEqual(t[0]['indice'], r'\mathrm{sp}')
        self.assertEqual(t[0]['classe'], 'indexe')
        self.assertEqual(t[1]['glyphe'], r'\mathcal{M}')
        self.assertEqual(t[1]['indice'], 'g')

    # \rho, \rho_X et \rho_{\mathrm{int}} restent distincts par leurs indices
    def test_rho_variants_distinct(self):
        a = top(atoms_of(r'\rho,\ \rho_X,\ \rho_{\mathrm{int}}'))
        self.assertEqual([(x['glyphe'], x['indice'], x['classe']) for x in a],
                         [(r'\rho', '', 'nu'), (r'\rho', 'X', 'indexe'), (r'\rho', r'\mathrm{int}', 'indexe')])

    # un préfixe de commande n'est pas un symbole
    def test_command_prefix(self):
        a = atoms_of(r'\varrho+\rho+\rhd')
        self.assertEqual([x['glyphe'] for x in top(a)], [r'\varrho', r'\rho'])
        self.assertEqual(a[0]['famille'], 'rho')
        self.assertTrue(a[0]['var'])

    # IWS_ANNEXE_K.tex:101 — notation composite signalée par l'audit historique
    def test_composite_with_nested_rho(self):
        a = atoms_of(r'\mathcal R^{\mathfrak B,\rho}')
        t = top(a)
        self.assertEqual(len(t), 1)
        self.assertEqual(t[0]['classe'], 'composite')
        inner = [x['glyphe'] for x in a if x['niveau'] == 1]
        self.assertEqual(inner, [r'\mathfrak{B}', r'\rho'])

    # macros du volume II : forme littérale et forme développée
    def test_macro_expansion(self):
        a = top(atoms_of(r'\X\times\Madm\to\Reach(x)', VOL2_MACROS))
        self.assertEqual(a[0]['source'], r'\X')
        self.assertEqual(a[0]['developpe'], r'\mathcal X')
        self.assertEqual(a[0]['famille'], 'X')
        self.assertEqual(a[1]['developpe'], r'\mathfrak M^{\mathrm{adm}}')
        self.assertEqual(a[2]['famille'], 'op:Reach')

    def test_macro_with_argument_not_expanded(self):
        a = top(atoms_of(r'\norm{x_0}', VOL2_MACROS))
        self.assertEqual([x['glyphe'] for x in a], ['x'])
        self.assertEqual(a[0]['indice'], '0')

    # commentaires et verbatim exclus du texte analysé
    def test_comments_masked(self):
        masked, comments, verbs = ex.mask_comments_and_verbatim('a $x$ % $y$\n\\begin{verbatim}$z$\\end{verbatim}')
        segs, _ = ex.find_math_segments(masked)
        self.assertEqual(len(segs), 1)
        self.assertEqual(len(comments), 1)
        self.assertEqual(len(verbs), 1)

    def test_text_group_and_nested_math(self):
        text = r'$x\text{ si $y>0$}$'
        segs, _ = ex.find_math_segments(text)
        self.assertEqual(len(segs), 1)
        self.assertEqual(segs[0]['end'], len(text))

    def test_delimiters(self):
        text = r'\(a\) \[b\] $$c$$ \begin{align*}d&=e\end{align*} \\[0.4em]'
        segs, problems = ex.find_math_segments(text)
        self.assertEqual([s['kind'] for s in segs], ['inline', 'display', 'display$$', 'env:align*'])
        self.assertFalse(problems)

    def test_label_and_array_spec_skipped(self):
        a = top(atoms_of(r'\begin{array}{cc} u & v\end{array}\label{eq:foo}'))
        self.assertEqual([x['glyphe'] for x in a], ['u', 'v'])

    # IWS_ANNEXE_C.tex:1844 — J(\rho), \zeta\rho S_\ast
    def test_modal_block(self):
        a = top(atoms_of(r'J(\rho)=\zeta\rho S_\ast'))
        self.assertEqual([x['glyphe'] for x in a], ['J', r'\rho', r'\zeta', r'\rho', 'S'])
        self.assertEqual(a[-1]['indice'], r'\ast')

    def test_primes_and_hat(self):
        a = top(atoms_of(r"x'+\hat{x}_1+\widehat{AB}"))
        self.assertEqual(a[0]['primes'], 1)
        self.assertEqual(a[1]['decoration'], r'\hat')
        self.assertEqual(a[1]['classe'], 'indexe')
        self.assertEqual(a[2]['nature'], 'expression_decoree')
        self.assertEqual(a[2]['classe'], 'composite')

    # transmission_profondeur_finie_V2.tex:26 — ancienne bascule de police dans un indice
    def test_old_rm_switch(self):
        a = atoms_of(r'\tau_{\rm ref}+\vth', r'\newcommand{\vth}{\vartheta}')
        self.assertEqual(a[0]['indice'], r'\rm ref')
        self.assertEqual([x['glyphe'] for x in a if x['niveau'] == 1], [r'{\rm ref}'])
        self.assertEqual(a[-1]['famille'], 'theta')
        self.assertEqual(a[-1]['source'], r'\vth')

    # B2a : la classe principale ne masque pas les attributs ; portée indice / exposant / combinaison
    def test_secondary_attributes(self):
        def sec(math):
            a = atoms_of(math)
            x = top(a)[0]
            ch = [y for y in a if y['niveau'] > 0]
            return x['classe'], ex.secondary_attributes(dict(x, niveau=0), [dict(y) for y in ch])
        cls, s = sec(r'\mathcal R^{\mathfrak B,\rho}')
        self.assertEqual(cls, 'composite')
        self.assertEqual(s['composite_portee'], 'exposant')
        self.assertIn('exposant:composants_multiples_non_latins', s['motifs_composite'])
        self.assertEqual(s['composants_exposant'], r'\mathfrak{B} \rho')
        self.assertIn('police=mathcal', s['attributs_secondaires'])
        cls, s = sec(r'\mathcal R_X^\rho')
        self.assertEqual(cls, 'composite')
        self.assertEqual(s['composite_portee'], 'indice+exposant')
        self.assertIn('combinaison:', s['motifs_composite'])
        cls, s = sec(r'\rho_{\mathrm{sp}}')
        self.assertEqual((cls, s['motifs_composite']), ('indexe', ''))

    def test_unknown_command_reported(self):
        a = atoms_of(r'\foobar x')
        self.assertEqual(a[0]['nature'], 'non_reconnu')


if __name__ == '__main__':
    unittest.main()
