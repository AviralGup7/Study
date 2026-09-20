#!/bin/bash
# setup.sh -- (re)create the LaTeX build sandbox under /tmp/texplay.
#
#   bash tools/latex/setup.sh
#
# /tmp is wiped between sessions, so run this before building anything. It
# installs the npm `texlive` package (emscripten pdftex + a trimmed TeX Live
# 2016 tree, ~3200 files) and puts a copy of compile.mjs where node can resolve
# `web-worker` from.
#
# Then build with:
#
#   cd /tmp/texplay/build
#   node ../compile.mjs ../node_modules/texlive/texlive <f>.tex <f>.pdf 2
#
# and re-run with `1` instead of `2`, grepping the log for
# 'Overfull|Underfull|^!' for layout diagnostics. A clean exit code is NOT a
# pass: always check the log and the PDF text layer.
#
# The texlive tree has no xcolor, tcolorbox, siunitx, booktabs, mathtools,
# enumitem, multirow, framed or expl3, and no EC/TS1 fonts. preamble.tex is
# written for that; do not add packages without checking they exist under
# node_modules/texlive/texlive/texmf-dist/tex/latex/.
set -e

TOOLS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLAY=/tmp/texplay

mkdir -p "$PLAY/build"
cd "$PLAY"

if [ ! -f "$PLAY/node_modules/texlive/pdftex-worker.js" ]; then
  echo "installing npm texlive ..."
  npm install texlive --no-audit --no-fund >/dev/null 2>&1
fi

# compile.mjs must sit where node can resolve node_modules/web-worker from.
cp "$TOOLS/compile.mjs" "$PLAY/compile.mjs"

echo "texlive tree : $(find "$PLAY/node_modules/texlive/texlive" -type f | wc -l) files"
echo "build dir    : $PLAY/build"
echo "compile with : cd $PLAY/build && node ../compile.mjs ../node_modules/texlive/texlive <f>.tex <f>.pdf 2"
