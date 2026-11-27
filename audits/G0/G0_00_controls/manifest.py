"""Recursive LaTeX inclusion manifest (read-only). Usage: python3 manifest.py <root_dir> <master.tex>"""
import hashlib, json, os, re, sys

root, master = sys.argv[1], sys.argv[2]
INC = re.compile(r'\\(input|include|subfile)\s*\{([^}]+)\}')
GFX = re.compile(r'\\includegraphics\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}')
PLANCHE = re.compile(r'\\planche\s*\{[^}]*\}\s*\{([^}]+)\}')
BIB = re.compile(r'\\(bibliography|addbibresource)\s*\{([^}]+)\}')
GPATH = re.compile(r'\\graphicspath\s*\{((?:\{[^}]*\})+)\}')
PKG = re.compile(r'\\(?:usepackage|RequirePackage)\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}')
MAC = re.compile(r'\\(newcommand|renewcommand|providecommand|DeclareMathOperator|newtheorem|newenvironment|renewenvironment|def)\*?\s*\{?\\?([A-Za-z@]+)')
LABEL = re.compile(r'\\label\s*\{([^}]+)\}')

def strip_comments(t):
    return '\n'.join(re.sub(r'(?<!\\)%.*', '', l) for l in t.split('\n'))

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

out = {'files': [], 'graphics': [], 'bib': [], 'packages': set(), 'macros': [], 'missing': [], 'commented_includes': [], 'labels': {}}
gpaths = ['']

def resolve(base, name, exts):
    for e in [''] + exts:
        p = os.path.normpath(os.path.join(root, name + e))
        if os.path.isfile(p):
            return p
    return None

def walk(path, depth=0, parent=None):
    rel = os.path.relpath(path, root)
    raw = open(path, encoding='utf-8', errors='replace').read()
    t = strip_comments(raw)
    out['files'].append({'file': rel, 'parent': parent, 'depth': depth, 'lines': raw.count('\n') + 1, 'sha256': sha(path)})
    for m in GPATH.finditer(t):
        gpaths.extend(re.findall(r'\{([^}]*)\}', m.group(1)))
    for m in INC.finditer(raw):
        line = raw[:m.start()].split('\n')[-1]
        if re.search(r'(?<!\\)%', line):
            out['commented_includes'].append({'in': rel, 'cmd': m.group(0)})
    for m in PKG.finditer(t):
        for p in m.group(1).split(','):
            out['packages'].add(p.strip())
    for m in MAC.finditer(t):
        out['macros'].append({'in': rel, 'kind': m.group(1), 'name': m.group(2), 'line': t[:m.start()].count('\n') + 1})
    labs = LABEL.findall(t)
    out['labels'][rel] = labs
    for m in BIB.finditer(t):
        for b in m.group(2).split(','):
            p = resolve(root, b.strip(), ['.bib'])
            out['bib'].append({'in': rel, 'name': b.strip(), 'resolved': os.path.relpath(p, root) if p else None, 'sha256': sha(p) if p else None})
            if not p: out['missing'].append({'in': rel, 'kind': 'bib', 'name': b})
    for rx, kind in ((GFX, 'includegraphics'), (PLANCHE, 'planche')):
        for m in rx.finditer(t):
            name = m.group(1).strip()
            if '#' in name: continue
            p = None
            for g in gpaths:
                p = resolve(root, os.path.join(g, name), ['.pdf', '.png', '.jpg', '.jpeg', '.eps'])
                if p: break
            out['graphics'].append({'in': rel, 'via': kind, 'name': name, 'line': t[:m.start()].count('\n') + 1,
                                    'resolved': os.path.relpath(p, root) if p else None, 'sha256': sha(p) if p else None})
            if not p: out['missing'].append({'in': rel, 'kind': 'graphic', 'name': name})
    for m in INC.finditer(t):
        name = m.group(2).strip()
        p = resolve(root, name, ['.tex'])
        if p: walk(p, depth + 1, rel)
        else: out['missing'].append({'in': rel, 'kind': m.group(1), 'name': name})

walk(os.path.join(root, master))
out['packages'] = sorted(out['packages'])
allfiles = set()
for dp, dn, fn in os.walk(root):
    for f in fn:
        if f == '.DS_Store': continue
        allfiles.add(os.path.relpath(os.path.join(dp, f), root))
used = {f['file'] for f in out['files']} | {g['resolved'] for g in out['graphics'] if g['resolved']} | {b['resolved'] for b in out['bib'] if b['resolved']}
out['unreferenced'] = sorted(allfiles - used)
out['unreferenced_sha'] = {f: sha(os.path.join(root, f)) for f in out['unreferenced']}
json.dump(out, sys.stdout, indent=1, ensure_ascii=False)
