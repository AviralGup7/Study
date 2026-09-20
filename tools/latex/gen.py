#!/usr/bin/env python3
"""gen.py -- wrap a body in the shared preamble, compile it, report diagnostics.

  python3 tools/latex/gen.py <body.tex> <code> "<course name>" "<doctype>" <outname> [passes]

`<body.tex>` is a path to a file holding only the document body (no preamble, no
\\begin{document}).  The assembled document is written to /tmp/texplay/build/
<outname>.tex and compiled there, so any sibling figures must be copied into
that directory first.

Prints one summary line plus any errors and Overfull boxes.  A clean run is
`errors=0 overfull=0`; Underfull boxes in tables are cosmetic and expected.
"""
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mknotes

if len(sys.argv) < 6:
    print(__doc__)
    sys.exit(2)

body_f, code, name, doctype, out = sys.argv[1:6]
passes = sys.argv[6] if len(sys.argv) > 6 else '2'

body = open(body_f, encoding='utf-8').read()
tex = mknotes.build(body, code, name, doctype)

build = '/tmp/texplay/build'
os.makedirs(build, exist_ok=True)
open(os.path.join(build, out + '.tex'), 'w', encoding='utf-8').write(tex)

r = subprocess.run(
    ['node', '../compile.mjs', '../node_modules/texlive/texlive',
     out + '.tex', out + '.pdf', passes],
    cwd=build, capture_output=True, text=True, timeout=1800)
log = r.stdout + r.stderr

err = [l for l in log.splitlines() if re.match(r'^stdout: !', l)]
over = [l for l in log.splitlines() if 'Overfull' in l]
under = [l for l in log.splitlines() if 'Underfull' in l]
m = re.search(r'Output written on \S+ \((\d+) page', log)

print('%-40s pages=%-4s errors=%-3d overfull=%-3d underfull=%d'
      % (out, m.group(1) if m else '?', len(err), len(over), len(under)))
for l in err[:8]:
    print('   ', l)
for l in over[:8]:
    print('   ', l)
if 'success:' not in log:
    print(log[-3000:])
    sys.exit(1)
