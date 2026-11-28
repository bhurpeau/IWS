"""Tests G0.4 : le catalogue des collisions est valide, couvre les 50 clés ambiguës et ne choisit aucune notation."""
import csv
import os
import subprocess
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'notations', 'scripts'))
import registry_io  # noqa: E402
import build_collisions  # noqa: E402

AUD = os.path.join(ROOT, 'audits', 'G0', 'G0_04_collisions')


@unittest.skipIf(registry_io.yaml is None, 'PyYAML absent (environnement .venv-g0)')
class Collisions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.proc = subprocess.run([sys.executable, '-I', 'notations/scripts/build_collisions.py'], cwd=ROOT,
                                 capture_output=True, text=True)
        cls.cat = registry_io.load(os.path.join(ROOT, 'notations', 'collisions.yaml'))

    def test_build_sans_erreur(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stdout[-2000:])

    def test_cinquante_cles_couvertes(self):
        rows = list(csv.DictReader(open(os.path.join(AUD, 'ambiguous_keys_coverage.csv'), encoding='utf-8')))
        self.assertEqual(len(rows), 50)
        self.assertFalse([r['cle'] for r in rows if not r['collisions']])

    def test_aucune_notation_canonique(self):
        for c in self.cat['collisions']:
            self.assertNotIn('notation_canonique', c)

    def test_scientifique_distinct(self):
        anomalies = {x['anomalie'] for x in self.cat['corrections_scientifiques']}
        self.assertTrue({'A-G02-14', 'A-G02-15'} <= anomalies)

    def test_regle_F1(self):
        for c in self.cat['collisions']:
            if c['niveau'] == 'N3':
                self.assertIn(c['portee'], ('inter', 'inter_C'))
            if c['niveau'] in ('N0', 'N1'):
                self.assertNotEqual(c['intervention'], 'A_ARBITRER', c['id']) if c['arbitrage'] == 'aucun' else None
            if 'niveau_G04_initial' in c:
                self.assertTrue(c.get('reclassement_F1'))

    def test_rho_395(self):
        rows = list(csv.DictReader(open(os.path.join(AUD, 'collisions.csv'), encoding='utf-8')))
        rho = next(r for r in rows if r['id'] == 'COL-RHO-01')
        self.assertEqual(int(rho['occ_cote_a_examiner']), 395)

    def test_selecteur_niveau_par_defaut(self):
        r = dict(glyphe='\\rho', indice='', exposant='', fichier='Volume_I/IWS_PART_III.tex', decoration='',
                 ligne='10', niveau='1', contexte='inline')
        self.assertFalse(build_collisions.match({'glyphe': '\\rho'}, r))
        self.assertTrue(build_collisions.match({'glyphe': '\\rho', 'niveau': '1'}, r))


if __name__ == '__main__':
    unittest.main()
