"""Tests G0.3 : la table de correspondance est cohérente et couvre le registre (PyYAML requis)."""
import csv
import os
import subprocess
import sys
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'notations', 'scripts'))
import registry_io  # noqa: E402


@unittest.skipIf(registry_io.yaml is None, 'PyYAML absent (environnement .venv-g0)')
class Crosswalk(unittest.TestCase):
    def test_build_sans_erreur(self):
        p = subprocess.run([sys.executable, '-I', 'notations/scripts/build_crosswalk.py'], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stdout[-2000:])

    def test_orientation_et_codes(self):
        rows = list(csv.DictReader(open(os.path.join(ROOT, 'notations', 'crosswalk.csv'), encoding='utf-8')))
        self.assertTrue(rows)
        for r in rows:
            self.assertIn(r['relation'], {'ID', 'GEN', 'SPEC', 'PROJ', 'DER', 'ANA', 'DIST', 'UNK', 'NEW'})
            if r['portee'] == 'intervolumes':
                self.assertTrue(r['source'].startswith(('I.', 'C.')))
                self.assertTrue(r['cible'].startswith('II.'))
            if r['relation'] == 'UNK':
                self.assertEqual(r['statut'], 'indeterminee')

    def test_chaque_objet_a_un_bilan(self):
        cov = list(csv.DictReader(open(os.path.join(ROOT, 'audits', 'G0', 'G0_03_crosswalk', 'coverage_by_object.csv'), encoding='utf-8')))
        reg = registry_io.load(os.path.join(ROOT, 'notations', 'registry.yaml'))['objets']
        self.assertEqual(len(cov), len(reg))
        self.assertFalse([c['objet'] for c in cov if c['bilan'] == 'SANS_BILAN'])


if __name__ == '__main__':
    unittest.main()
