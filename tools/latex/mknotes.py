#!/usr/bin/env python3
"""mknotes.py -- assemble the Arena short-notes / questions LaTeX documents.

The look of every document in this repository is fixed by ONE preamble, kept
beside this file as ``preamble.tex``.  It was extracted verbatim from a document
already checked into the repo, so it is ground truth rather than a description.

``SEPARATION PROCESSES II (CHE F313)/Notes/SP2-notes.tex`` is the canonical
*standard* for structure and depth (user instruction: "take sp2 notes as
standard and improve other notes based on it").  SP2-notes.tex was authored for
XeLaTeX + TeX Live-full; the engine we can run here is the emscripten **pdftex**
in the npm ``texlive`` package, whose TeX Live 2016 tree ships only base
packages -- no xcolor, tcolorbox, siunitx, booktabs, mathtools, enumitem,
multirow, framed, expl3, and no EC/TS1 font metrics.  ``preamble.tex`` therefore
reproduces the SP2 design with base-tree packages only:

  \\spsection   -> \\colorbox{accent} + minipage bar        (was tcolorbox)
  formulabox / daybox / qbox / mthbox / ansbox / warnbox
                -> lrbox + minipage + \\fcolorbox            (were tcolorbox)
  \\toprule/\\midrule/\\bottomrule -> \\hline shims            (was booktabs)
  \\SI/\\si/\\num -> rendered to plain math                   (was siunitx)
  \\textdegree/\\textperiodcentered -> math glyphs            (no TS1 fonts)

Usage from another script::

    import mknotes
    open('out.tex','w').write(mknotes.build(
        body, 'CHE F311', 'Kinetics & Reactor Design', 'Short Notes & Formula Sheet'))

``render_si`` / ``port`` turn a XeLaTeX+siunitx body into something this
preamble accepts, so an original XeLaTeX source can be recompiled verbatim.

PREAMBLE PITFALLS -- each of these cost a debugging cycle once already:

* ``formulabox`` & friends are ENVIRONMENTS, not macros.  ``\\warnbox{...}``
  expands only the begin-code, leaves a minipage open, and everything after it
  is swallowed until TeX dies on ``main memory size``.
* ``\\bgroup``/``\\egroup`` inside a helper macro silently discards the box body.
  The preamble uses lrbox + minipage + \\usebox instead -- do not "simplify" it.
* A long sentence in one ``\\text{...}`` cell of ``align*`` is unbreakable and
  produces a 300pt Overfull that pushes text off the page while still compiling.
  Keep ``\\text{}`` cells under about half a line.
* ``$...$`` is fatal inside a math group; use ``\\ensuremath{}``.
"""
import os
import re

_HERE = os.path.dirname(os.path.abspath(__file__))


def preamble():
    """The shared preamble, with $code/$name/$doctype still unsubstituted.

    Ends with \begin{document}; build() asserts that, because slicing it off
    yields a document that fails only at \end{document} with a misleading
    ".aux not found" error.
    """
    pre = open(os.path.join(_HERE, 'preamble.tex'), encoding='utf-8').read()
    assert pre.rstrip().endswith(r'\begin{document}'), \
        'preamble.tex must end with \\begin{document}'
    return pre


POSTAMBLE = "\n\\end{document}\n"


def build(body, code, name, doctype):
    """Assemble a complete document from a body of LaTeX.

    `body` goes between \\begin{document} and \\end{document}.  siunitx macros in
    the body are rendered, so a body may use \\SI{...}{...} freely.
    """
    head = preamble()
    # &, %, #, $, _ are special in LaTeX; the footer text is arbitrary prose.
    esc = lambda t: re.sub(r'([&%#_$])', r'\\\1', t)
    head = head.replace('$code', esc(code)) \
               .replace('$name', esc(name)) \
               .replace('$doctype', esc(doctype))
    return head + '\n' + render_si(body.strip()) + '\n' + POSTAMBLE


# ----------------------------------------------------------------- siunitx port
PREFIX = {
    'kilo': 'k', 'hecto': 'h', 'deka': 'da', 'deca': 'da', 'deci': 'd',
    'centi': 'c', 'milli': 'm', 'micro': r'\mu', 'nano': 'n', 'pico': 'p',
    'mega': 'M', 'giga': 'G', 'tera': 'T',
}
BASE = {
    'gram': 'g', 'meter': 'm', 'metre': 'm', 'second': 's', 'minute': 'min',
    'hour': 'h', 'day': 'd', 'year': 'yr', 'mol': 'mol', 'mole': 'mol',
    'liter': 'L', 'litre': 'L', 'kelvin': 'K', 'pascal': 'Pa', 'joule': 'J',
    'watt': 'W', 'volt': 'V', 'hertz': 'Hz', 'bar': 'bar', 'newton': 'N',
    'molar': 'M', 'ampere': 'A', 'coulomb': 'C', 'poise': 'P', 'stokes': 'St',
    'rev': 'rev', 'radian': 'rad',
}
SPECIAL = {
    'degreeCelsius': r'^{\circ}\mathrm{C}',
    'degreeFahrenheit': r'^{\circ}\mathrm{F}',
    'celsius': r'^{\circ}\mathrm{C}',
    'percent': r'\%',
    'degree': r'^{\circ}',
    'angstrom': r'\text{\AA}',
    'ohm': r'\Omega',
}


def _parse_unit(u):
    """Parse siunitx unit syntax into (numerator, denominator) entry lists.

    Each entry is a finished math fragment such as ``\\mathrm{kg}`` or
    ``\\mathrm{cm}^{3}``.  ``\\per`` moves everything after it into the
    denominator, matching siunitx's per-mode=symbol output (kg/cm^3, mol/L).
    """
    u = u.strip()
    if not u:
        return [], []
    toks = re.findall(r'\\[a-zA-Z]+|\^\{[^}]*\}|\^[^\s{}]+|.', u)
    num, den = [], []
    prefix, power, denom, explicit = '', 1, False, False
    for t in toks:
        if t.isspace():
            continue
        if t.startswith('\\'):
            name = t[1:]
            if name == 'per':
                denom, power, explicit = True, 1, False
                continue
            if name == 'cubic':
                power, explicit = 3, True
                continue
            if name == 'square':
                power, explicit = 2, True
                continue
            if name == 'tothe':
                continue                      # exponent follows in braces
            if name in PREFIX:
                prefix = PREFIX[name]
                continue
            if name in SPECIAL:
                (den if denom else num).append(SPECIAL[name])
                prefix, power, explicit = '', 1, False
                continue
            if name in BASE:
                sym, p = BASE[name], power
                if denom and not explicit:
                    p = -1                    # \per with no power macro => inverse
                # NOTE the space in '%s %s': without it '\mu' + 's' tokenises as
                # the single undefined control word \mus.
                entry = r'\mathrm{%s %s}' % (prefix, sym)
                if abs(p) != 1:
                    entry += '^{%d}' % abs(p)
                (den if denom else num).append(entry)
                prefix, power, explicit = '', 1, False
                continue
            # compound single-word units: \kilogram, \centimeter, \milligram ...
            cm = re.match(r'(kilo|milli|centi|micro|deci|mega|nano|giga|hecto|pico)'
                          r'(gram|meter|metre|second|pascal|joule|liter|litre|mole)$', name)
            if cm:
                entry = r'\mathrm{%s %s}' % (PREFIX[cm.group(1)], BASE[cm.group(2)])
                if abs(power) != 1:
                    entry += '^{%d}' % abs(power)
                (den if denom else num).append(entry)
                prefix, power, explicit = '', 1, False
                continue
            continue                          # unknown macro: drop silently
        if t.startswith('^'):
            exp = t[1:]
            exp = exp[1:-1] if exp.startswith('{') else exp
            target = den if denom else num
            if target:
                target[-1] += '^{%s}' % exp
            continue
        if t == '{':
            continue
        num.append('\\' + t if t in '&%$#_' else t)
    return num, den


def _render_unit(u):
    """siunitx unit -> math fragment usable with \\ensuremath."""
    num, den = _parse_unit(u)
    if not num and not den:
        return ''
    head = r'\,'.join(num)
    if not den:
        return head
    tail = r'\,'.join(den)
    return head + '/' + tail if head else '1/%s' % tail


def _num(n):
    """siunitx number -> math.  Handles e-notation; grouping is kept as typed."""
    n = n.strip()
    return re.sub(r'(\d+\.?\d*)\s*[eE]\s*([+-]?\d+)',
                  lambda m: m.group(1) + r'\times 10^{%s}' % m.group(2).lstrip('+'), n)


def render_si(s):
    r"""Expand the siunitx MACROS \SI/\si/\num/\SIrange into plain math.

    Safe to apply to any body: it only touches control sequences that do not
    exist in the base TeX tree anyway.  Table-column rewrites are NOT done here
    -- see convert_units.
    """
    def si(m):
        num, unit = _num(m.group('num')), _render_unit(m.group('unit'))
        inner = num if not unit else num + r'\,' + unit
        return r'\ensuremath{' + inner + '}'
    s = re.sub(r'\\SI\s*(?:\[[^\]]*\])?\s*\{(?P<num>(?:[^{}]|\{[^{}]*\})*)\}'
               r'\s*\{(?P<unit>(?:[^{}]|\{[^{}]*\})*)\}', si, s)

    def sirange(m):
        a, b, unit = _num(m.group(1)), _num(m.group(2)), _render_unit(m.group(3))
        inner = a + r'\,\text{--}\,' + b + (r'\,' + unit if unit else '')
        return r'\ensuremath{' + inner + '}'
    s = re.sub(r'\\SIrange\s*(?:\[[^\]]*\])?\s*\{([^{}]*)\}\s*\{([^{}]*)\}\s*\{([^{}]*)\}',
               sirange, s)

    def si_only(m):
        u = _render_unit(m.group(1))
        return r'\ensuremath{' + u + '}' if u else ''
    s = re.sub(r'\\si\s*(?:\[[^\]]*\])?\s*\{(?P<unit>(?:[^{}]|\{[^{}]*\})*)\}', si_only, s)

    s = re.sub(r'\\num\s*(?:\[[^\]]*\])?\s*\{([^{}]*)\}',
               lambda m: r'\ensuremath{' + _num(m.group(1)) + '}', s)
    s = re.sub(r'\\sisetup\s*\{[^{}]*\}', '', s)

    def ang(m):
        # siunitx \ang{} formats an angle; every current use is in degrees,
        # so render the value followed by the degree sign.
        v = _num(m.group('val'))
        return r'\ensuremath{' + v + r'^{\circ}}'
    s = re.sub(r'\\ang\s*(?:\[[^\]]*\])?\s*\{(?P<val>(?:[^{}]|\{[^{}]*\})*)\}', ang, s)
    return s


def convert_units(s):
    r"""render_si plus the column rewrites needed to port a real siunitx body."""
    s = render_si(s)
    return re.sub(r'S\s*\[[^\]]*\]', 'r', s)          # siunitx S column -> r


def port(s):
    """Full XeLaTeX+TeX-Live-full body -> base-tree pdftex body."""
    s = convert_units(s)
    s = re.sub(r'\\cmidrule\s*(?:\([^)]*\))?\s*\{(\d+)-(\d+)\}',
               lambda m: r'\cline{' + m.group(1) + '-' + m.group(2) + '}', s)
    s = re.sub(r'\\usepackage\s*(?:\[[^\]]*\])?\s*\{[^{}]*\}', '', s)
    s = re.sub(r'\\documentclass\s*(?:\[[^\]]*\])?\s*\{[^{}]*\}', '', s)
    s = s.replace(r'\begin{document}', '').replace(r'\end{document}', '')
    # enumitem's optional list argument has no meaning without enumitem; LaTeX
    # reads the [...] as body text and dies with "perhaps a missing \item".
    s = re.sub(r'(\\begin\{(?:itemize|enumerate|description)\})\s*\[[^\]]*\]', r'\1', s)
    return s.replace(r'\textsuperscript{th}', r'\ensuremath{^{\mathrm{th}}}')
