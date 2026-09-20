#!/usr/bin/env python3
"""port.py -- regenerate the base-tree port of a canonical XeLaTeX document.

  python3 tools/latex/port.py <canonical.tex> <code> "<name>" "<doctype>" <out.tex> [--body <file>]

The repository keeps two kinds of .tex file:

  * the *canonical* document -- authored for XeLaTeX + TeX Live full
    (tcolorbox, siunitx, booktabs, enumitem, ...), e.g.
    ``SEPARATION PROCESSES II (CHE F313)/Notes/SP2-notes.tex``.  This is the
    editable copy and the one that carries the prose.
  * the *port* -- the same document rewritten for the base tree that the
    sandbox can actually build (see tools/latex/setup.sh), e.g.
    ``SP2-Short-Notes-and-Formula-Sheet.tex``.  Generated, never edited.

The port is assembled as

    preamble.tex ($code/$name/$doctype filled, ending in \\begin{document})
  + mknotes.port(<body of the canonical document>)
  + \\end{document}

i.e. a complete standalone document.  With --body, the body alone (no
preamble) is also written out, which is what tools/latex/gen.py compiles.

Edit the canonical file, run this, then compile the body with gen.py.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mknotes                                                    # noqa: E402


def body_of(path):
    """The document body: everything between \\begin{document} and \\end{document}."""
    s = open(path, encoding='utf-8').read()
    m = re.search(r'\\begin\{document\}', s)
    if not m:
        raise SystemExit('no \\begin{document} in ' + path)
    body = s[m.end():]
    cut = body.rindex(r'\end{document}')
    return body[:cut]


def port(tex, code, name, doctype, out, body_out=None):
    pre = mknotes.preamble().rstrip()
    assert pre.endswith(r'\begin{document}')
    # Keep the trailing \begin{document}: the assembled file must be a complete,
    # standalone document.  Stripping it here (as an earlier version did)
    # produces a .tex with \end{document} but no \begin{document}, which fails
    # at the first body line with "Missing \begin{document}" and cascades into
    # bogus \@pdfcolorstack / .aux errors -- that is exactly the state the
    # committed SP2-Short-Notes-and-Formula-Sheet.tex was caught in.
    esc = lambda t: re.sub(r'([&%#_$])', r'\\\1', t)
    pre = pre.replace('$code', esc(code)) \
             .replace('$name', esc(name)) \
             .replace('$doctype', esc(doctype))
    ported = mknotes.port(body_of(tex)).strip()
    open(out, 'w', encoding='utf-8').write(pre + '\n' + ported + '\n\n\\end{document}\n')
    print('port : %s (%d chars)' % (out, len(pre) + len(ported)))
    if body_out:
        open(body_out, 'w', encoding='utf-8').write(ported + '\n')
        print('body : %s' % body_out)


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) < 5:
        print(__doc__)
        sys.exit(2)
    b = a[a.index('--body') + 1] if '--body' in a else None
    port(a[0], a[1], a[2], a[3], a[4], b)
