"""Tests G0.2bis : comparaison profonde du registre, sélecteurs (décoration, ancrage des fichiers), granularité."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import link_registry  # noqa: E402
import registry_io  # noqa: E402


def occ(**k):
    base = dict(glyphe='x', indice='', exposant='', symbole_source='x', fichier='Volume_I/IWS_PART_I.tex', ligne='10',
                niveau='0', nature='lettre', decoration='', police='')
    base.update(k)
    return base


class DeepDiff(unittest.TestCase):
    def test_types_distingues(self):
        self.assertTrue(registry_io.deep_diff({'a': 1}, {'a': '1'}))
        self.assertTrue(registry_io.deep_diff({'a': None}, {'a': ''}))
        self.assertTrue(registry_io.deep_diff({'a': True}, {'a': 1}))

    def test_ordre_des_cles(self):
        self.assertTrue(registry_io.deep_diff({'a': 1, 'b': 2}, {'b': 2, 'a': 1}))

    def test_egalite(self):
        d = {'objets': [{'id': 'I.X', 'lignes': [1, 2], 'v': None}]}
        self.assertEqual(registry_io.deep_diff(d, {'objets': [{'id': 'I.X', 'lignes': [1, 2], 'v': None}]}), [])


class Selecteurs(unittest.TestCase):
    def test_ancrage_fichier(self):
        sel = {'vol': 'volI', 'glyphe': 'u', 'fichier': 'IWS_PART_I\\.tex'}
        self.assertTrue(link_registry.match(sel, occ(glyphe='u')))
        self.assertFalse(link_registry.match(sel, occ(glyphe='u', fichier='Volume_I/IWS_PART_III.tex')))
        self.assertFalse(link_registry.match(sel, occ(glyphe='u', fichier='Volume_I/IWS_PART_II.tex')))

    def test_motif_non_ancre_capte_les_autres_livres(self):
        # défaut corrigé en G0.2bis : le motif non ancré capte aussi IWS_PART_III
        sel = {'vol': 'volI', 'glyphe': 'u', 'fichier': 'IWS_PART_I'}
        self.assertTrue(link_registry.match(sel, occ(glyphe='u', fichier='Volume_I/IWS_PART_III.tex')))

    def test_decoration(self):
        sel = {'vol': 'volI', 'glyphe': '\\tau', 'decoration': '^(?!\\\\bar)'}
        self.assertTrue(link_registry.match(sel, occ(glyphe='\\tau')))
        self.assertTrue(link_registry.match(sel, occ(glyphe='\\tau', decoration='\\dot')))
        self.assertFalse(link_registry.match(sel, occ(glyphe='\\tau', decoration='\\bar')))

    def test_lignes_et_indice(self):
        sel = {'vol': 'volII', 'glyphe': 'q', 'indice': '^$', 'lignes': [1260, 1290]}
        self.assertTrue(link_registry.match(sel, occ(glyphe='q', ligne='1262')))
        self.assertFalse(link_registry.match(sel, occ(glyphe='q', ligne='1796')))
        self.assertFalse(link_registry.match(sel, occ(glyphe='q', indice='0', ligne='1262')))


class RegistreCourant(unittest.TestCase):
    """Invariants du registre versionné (lecture du fichier ; PyYAML requis pour le style bloc)."""

    @classmethod
    def setUpClass(cls):
        root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..')
        path = os.path.join(root, 'notations', 'registry.yaml')
        if registry_io.yaml is None:
            raise unittest.SkipTest('PyYAML absent (environnement .venv-g0)')
        cls.objs = registry_io.load(path)['objets']
        cls.by = {o['id']: o for o in cls.objs}

    def test_familles_reciproques(self):
        for o in self.objs:
            for c in o.get('composants', []):
                self.assertIn(o['id'], self.by[c].get('familles', []), (o['id'], c))
            for f in o.get('familles', []):
                self.assertIn(o['id'], self.by[f].get('composants', []), (o['id'], f))

    def test_familles_sans_composants_motivees(self):
        for o in self.objs:
            if o.get('granularite') == 'famille' and not o.get('composants'):
                self.assertTrue(o.get('motif_granularite'), o['id'])

    def test_notation_canonique_vide_et_prefixe(self):
        for o in self.objs:
            self.assertEqual(o['notation_canonique'], '', o['id'])
            self.assertTrue(o['id'].startswith(('I.', 'II.', 'C.')), o['id'])

    def test_fichiers_ancres(self):
        for o in self.objs:
            for s in o['selecteurs']:
                f = s.get('fichier', '')
                for book in ('IWS_PART_I', 'IWS_PART_II', 'IWS_PART_III'):
                    for alt in f.split('|'):
                        if alt == book:
                            self.fail('motif non ancré %s dans %s' % (alt, o['id']))


if __name__ == '__main__':
    unittest.main()
