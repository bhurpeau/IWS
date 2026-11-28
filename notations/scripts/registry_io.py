#!/usr/bin/env python3
"""Lecture / écriture du registre candidat (G0.2bis, décision C4).

Le registre `notations/registry.yaml` est écrit en YAML style bloc (PyYAML 6.0.2, environnement
virtuel `.venv-g0`, voir `notations/requirements-g0.txt`). À défaut de PyYAML, la lecture retombe
sur le module json (valable pour l'ancien format JSON, sous-ensemble de YAML 1.2).

Usage :
    .venv-g0/bin/python -I notations/scripts/registry_io.py verify REF.json REGISTRE.yaml
        vérifie l'égalité profonde (valeurs, types, ordre des listes et des clés) entre deux registres.
    .venv-g0/bin/python -I notations/scripts/registry_io.py convert SOURCE OUT.yaml
        réécrit SOURCE (JSON ou YAML) en YAML style bloc puis vérifie l'aller-retour.
"""
import json
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None


def load(path):
    txt = open(path, encoding='utf-8').read()
    if yaml is not None:
        return yaml.safe_load(txt)
    return json.loads(txt)


def dump(data, path):
    if yaml is None:
        raise SystemExit('PyYAML requis (environnement .venv-g0)')
    txt = yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=110, default_flow_style=False)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write('# Registre sémantique candidat — voir _meta. YAML 1.2 style bloc, généré par registry_io.py.\n')
        fh.write(txt)


def deep_diff(a, b, path='$'):
    """Liste des différences ; compare aussi les types (bool ≠ int, str ≠ int, None) et l'ordre des clés."""
    out = []
    if type(a) is not type(b):
        return ['%s : type %s ≠ %s' % (path, type(a).__name__, type(b).__name__)]
    if isinstance(a, dict):
        if list(a) != list(b):
            out.append('%s : clés ou ordre des clés différents' % path)
        for k in a:
            if k in b:
                out += deep_diff(a[k], b[k], '%s.%s' % (path, k))
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append('%s : longueurs %d ≠ %d' % (path, len(a), len(b)))
        for i, (x, y) in enumerate(zip(a, b)):
            out += deep_diff(x, y, '%s[%d]' % (path, i))
    elif a != b:
        out.append('%s : %r ≠ %r' % (path, a, b))
    return out


def main(argv):
    if len(argv) != 4 or argv[1] not in ('verify', 'convert'):
        print(__doc__)
        return 2
    src = load(argv[2])
    if argv[1] == 'convert':
        dump(src, argv[3])
    d = deep_diff(src, load(argv[3]))
    for x in d[:50]:
        print('  ÉCART', x)
    print('%s : %d écart(s)' % (argv[1], len(d)))
    return 1 if d else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
