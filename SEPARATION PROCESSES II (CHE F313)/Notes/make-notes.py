#!/usr/bin/env python3
"""SP2 short notes / formula sheet generator.

Source of the content: the Module 1 (Lectures 1-5) and Module 2 (Lecture 2) decks in ../PPTs/.
Everything is plain text + <sub>/<sup> markup, so editing a formula means editing a string here.

Usage:  python3 make-notes.py SP2-Short-Notes-and-Formula-Sheet.pdf
Requires: reportlab  (pip install reportlab)
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
                                Table, TableStyle, HRFlowable, PageBreak, KeepTogether)

F = '/usr/share/fonts/truetype/dejavu/'
pdfmetrics.registerFont(TTFont('DJ', F + 'DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DJB', F + 'DejaVuSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('DJI', F + 'DejaVuSans-Oblique.ttf')) if os.path.exists(F + 'DejaVuSans-Oblique.ttf') else pdfmetrics.registerFont(TTFont('DJI', F + 'DejaVuSans.ttf'))
pdfmetrics.registerFontFamily('DJ', normal='DJ', bold='DJB', italic='DJI', boldItalic='DJB')

ACCENT = colors.HexColor('#0B3C5D')
ACCENT2 = colors.HexColor('#1D6FA5')
GREY = colors.HexColor('#F1F4F7')
BORDER = colors.HexColor('#C6D1DA')
RULE = colors.HexColor('#9FB3C2')
INK = colors.HexColor('#152029')

st_title = ParagraphStyle('t', fontName='DJB', fontSize=19, leading=23, textColor=ACCENT, alignment=TA_CENTER)
st_sub = ParagraphStyle('s', fontName='DJ', fontSize=10.5, leading=14, textColor=ACCENT2, alignment=TA_CENTER)
st_small = ParagraphStyle('sm', fontName='DJ', fontSize=8.5, leading=11.5, textColor=colors.HexColor('#333333'), alignment=TA_CENTER)
st_h1 = ParagraphStyle('h1', fontName='DJB', fontSize=12.6, leading=15.6, textColor=colors.white,
                       backColor=ACCENT, borderPadding=(5, 6, 5, 6), spaceBefore=9, spaceAfter=7)
st_h2 = ParagraphStyle('h2', fontName='DJB', fontSize=10.3, leading=13.2, textColor=ACCENT, spaceBefore=7, spaceAfter=3)
st_body = ParagraphStyle('b', fontName='DJ', fontSize=9.1, leading=12.4, textColor=INK, spaceAfter=2.2)
st_bul = ParagraphStyle('bu', parent=st_body, leftIndent=9.5, bulletIndent=1.5, spaceAfter=1.9)
st_bul2 = ParagraphStyle('bu2', parent=st_body, leftIndent=22, bulletIndent=12.5, spaceAfter=1.5, fontSize=8.8, leading=12)
st_form = ParagraphStyle('f', fontName='DJ', fontSize=9.6, leading=15.4, textColor=colors.HexColor('#0E2430'),
                         backColor=GREY, borderColor=BORDER, borderWidth=0.6, borderPadding=(6.5, 7, 6.5, 7),
                         spaceBefore=4, spaceAfter=6, leftIndent=1, rightIndent=1)
st_form2 = ParagraphStyle('f2', parent=st_form, textColor=colors.HexColor('#44515A'), fontSize=8.9, leading=13.6)
st_note = ParagraphStyle('n', fontName='DJ', fontSize=8.3, leading=11.2, textColor=colors.HexColor('#46535C'),
                         spaceAfter=3, leftIndent=2)


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def H1(t):  return Paragraph(t, st_h1)
def H2(t):  return Paragraph(t, st_h2)
def P(t):   return Paragraph(t, st_body)
def B(t, lvl=1): return Paragraph(t, st_bul if lvl == 1 else st_bul2, bulletText='\u2022' if lvl == 1 else '\u2013')
def N(t):   return Paragraph(t, st_note)
def F(*lines): return KeepTogether(Paragraph('<br/>'.join(l if l else '&nbsp;' for l in lines), st_form))
def F2(*lines): return KeepTogether(Paragraph('<br/>'.join(l if l else '&nbsp;' for l in lines), st_form2))


Dbar = 'D\u0304'      # D with combining macron
xbar = 'x\u0304'
S = []

# ------------------------------------------------------------------ cover
S += [Spacer(1, 6*mm),
      Paragraph('SEPARATION PROCESSES II', st_title),
      Paragraph('CHE F313 &nbsp;&middot;&nbsp; BITS Pilani &nbsp;&middot;&nbsp; I-Semester 2026-27', st_sub),
      Spacer(1, 2.5*mm),
      HRFlowable(width='60%', thickness=1.1, color=ACCENT, hAlign='CENTER'),
      Spacer(1, 3*mm),
      Paragraph('Short Notes &amp; Formula Sheet', ParagraphStyle('c2', parent=st_title, fontSize=14, leading=17)),
      Spacer(1, 3*mm),
      Paragraph('Module 1 &mdash; Properties and Handling of Particulate Solids (Ch. 28)<br/>'
                'Module 2 &mdash; Mechanical Separations (Ch. 29)', st_sub),
      Spacer(1, 5*mm)]

cover = Table([[Paragraph(
    '<b>Compiled from</b><br/>Mod1-Lecture 1 &hellip; Lecture 5 (Module 1) &nbsp;&middot;&nbsp; Mod 2-Lecture 2 (Module 2) &mdash; course slide decks<br/>'
    '<b>Reference texts</b><br/>McCabe, Smith &amp; Harriott, <i>Unit Operations of Chemical Engineering</i>, 7e (Ch. 28, 29)<br/>'
    'Swain, Patra &amp; Roy, <i>Mechanical Operations</i>, Tata McGraw Hill', st_small)]],
    colWidths=[168*mm])
cover.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), GREY),
                           ('BOX', (0, 0), (-1, -1), 0.7, BORDER),
                           ('LEFTPADDING', (0, 0), (-1, -1), 9), ('RIGHTPADDING', (0, 0), (-1, -1), 9),
                           ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6)]))
S += [cover, Spacer(1, 5*mm)]

S.append(H2('What is inside'))
toc = [['<b>Module 1 \u2014 Properties &amp; Handling of Particulate Solids</b>', '<b>Lecture</b>'],
       ['Introduction and characterisation of solid particles', '1'],
       ['Screening and screen analysis', '2'],
       ['Mixed particle sizes, average diameters and specific surface \u2014 derivations', '3'],
       ['Particulate masses: properties, storage, conveying and mixing', '4'],
       ['Size reduction (comminution): energy laws and work index', '5'],
       ['<b>Module 2 \u2014 Mechanical Separations</b>', ''],
       ['Filtration: media, filter aids, cake filtration and pressure drop', '2'],
       ['Practice problems set from the slides', '\u2014']]
_tocst = ParagraphStyle('toc', fontName='DJ', fontSize=8.8, leading=11.4, textColor=INK)
t = Table([[Paragraph(a, _tocst), Paragraph(b, ParagraphStyle('toc2', parent=_tocst, alignment=TA_CENTER))]
           for a, b in toc], colWidths=[148*mm, 20*mm], hAlign='LEFT')
t.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), 'DJ'), ('FONTSIZE', (0, 0), (-1, -1), 8.8),
                       ('TEXTCOLOR', (0, 0), (-1, -1), INK), ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                       ('LINEBELOW', (0, 0), (-1, 0), 0.6, RULE),
                       ('LINEABOVE', (0, 6), (-1, 6), 0.6, RULE),
                       ('BACKGROUND', (0, 0), (-1, 0), GREY),
                       ('BACKGROUND', (0, 6), (-1, 6), GREY),
                       ('TOPPADDING', (0, 0), (-1, -1), 2.6), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.6),
                       ('FONTNAME', (0, 6), (-1, 6), 'DJB'), ('FONTNAME', (0, 0), (-1, 0), 'DJB')]))
S += [t, Spacer(1, 5*mm)]

S.append(H2('Notation used throughout'))
nota = [
    ['D<sub>p</sub>', 'particle diameter (equivalent or nominal)', 'A<sub>w</sub>', 'specific surface area of the mixture, m²/kg'],
    ['D̄<sub>s</sub>', 'volume-surface (Sauter) mean diameter', 'N<sub>w</sub>', 'number of particles per unit mass'],
    ['D̄<sub>v</sub>', 'volume mean diameter', 'N<sub>i</sub>, N<sub>T</sub>', 'particles in fraction i, total number'],
    ['D̄<sub>N</sub>', 'arithmetic (number) mean diameter', 'x<sub>i</sub>', 'mass fraction of fraction i'],
    ['D̄<sub>w</sub>', 'mass mean diameter', 'a', 'volume shape factor, v<sub>p</sub> = a D<sub>p</sub>³'],
    ['Φ<sub>s</sub>', 'sphericity of the particle', 'W<sub>i</sub>', 'Bond work index, kWh/short ton'],
    ['ρ<sub>p</sub>', 'density of the particle', 'η<sub>c</sub>, η<sub>m</sub>', 'crushing, mechanical efficiency'],
    ['s<sub>p</sub>, v<sub>p</sub>', 'surface area, volume of one particle', 'ε', 'porosity of the bed / cake'],
]
nt = Table([[Paragraph(c, ParagraphStyle('nt', fontName='DJ', fontSize=8.4, leading=11, textColor=INK)) for c in row] for row in nota],
           colWidths=[16*mm, 60*mm, 20*mm, 72*mm], hAlign='LEFT')
nt.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('LINEBELOW', (0, 0), (-1, -2), 0.35, colors.HexColor('#DCE3E9')),
                        ('TOPPADDING', (0, 0), (-1, -1), 2.2), ('BOTTOMPADDING', (0, 0), (-1, -1), 2.2)]))
S.append(nt)
S.append(PageBreak())

# ------------------------------------------------------------- Lecture 1
S.append(H1('MODULE 1  \u00b7  LECTURE 1  \u2014  Introduction and Characterisation of Solid Particles'))
S.append(H2('Why particulate solids matter'))
S.append(B('Solids are more difficult to handle than liquids or gases; of all the shapes and sizes found in solids, the small particle is the most important from a chemical-engineering standpoint.'))
S.append(B('Designing processes and equipment for streams containing solids needs an understanding of the characteristics of masses of particulate solids.'))
S.append(B('Most important properties of pieces of solids: density (mass per unit volume), hardness (resistance to scratching), fragility (how easily a particle crumbles), tenacity (resistance to collisions).'))

S.append(H2('Characterisation: size, shape and density'))
S.append(B('Every particle is characterised by size (D<sub>p</sub>), shape and density (ρ<sub>p</sub>).'))
S.append(B('Density: particles of homogeneous solids have the same density as the bulk material; particles from a composite solid (e.g. metal-bearing ore) have various densities, usually different from the bulk.'))
S.append(B('Size: for regular (equidimensional) particles size and shape are easily specified (spheres, cubes); non-equidimensional particles are characterised by the second longest major dimension; for needle-like particles D<sub>p</sub> refers to the thickness, not the length; for irregular particles (sand grains, mica flakes) size and shape must be defined arbitrarily.'))
S.append(B('Equivalent (nominal) diameter: the size of a spherical particle having the same controlling characteristic as the particle considered. The controlling characteristic depends on the system and the process:'))
S.append(B('surface area controls (irregular catalyst particle) → surface diameter D<sub>ps</sub>', 2))
S.append(B('mass/volume controls (gravitational free settling in a liquid) → volume diameter D<sub>pv</sub>', 2))
S.append(B('both area and volume control → volume-surface (Sauter) diameter D<sub>vs</sub>', 2))
S.append(F('Surface diameter:  s<sub>p</sub> = π D<sub>ps</sub>²    and    D<sub>ps</sub> = √(s<sub>p</sub>/π)',
           'Volume diameter:   v<sub>p</sub> = π D<sub>pv</sub>³/6   and   D<sub>pv</sub> = (6 v<sub>p</sub>/π)<sup>1/3</sup>',
           'Sauter diameter:   D<sub>vs</sub> = 6 v<sub>p</sub>/s<sub>p</sub>   and   s<sub>p</sub>/v<sub>p</sub> = (π D<sub>vs</sub>²)/(π D<sub>vs</sub>³/6) = 6/D<sub>vs</sub>',
           'Sphericity:        Φ<sub>s</sub> = 6 v<sub>p</sub> / (D<sub>p</sub> s<sub>p</sub>)',
           'Screen-average D<sub>p</sub>:  arithmetic average of the aperture sizes of the two successive standard screens, one of which passes and the other retains the particle'))
S.append(N('Sphericity = (surface-area-to-volume ratio of a sphere of the same diameter) ÷ (surface-area-to-volume ratio of the particle); Φ<sub>s</sub> = 1 for a sphere and is independent of particle size. '
           'Sphericity values for common shapes are tabulated in Table 28.1 of the text. For granular materials, exact v<sub>p</sub> and s<sub>p</sub> cannot be measured, so D<sub>p</sub> is the nominal size from screen analysis or microscopy.'))

S.append(H2('Size ranges, measurement methods'))
S.append(B('Coarse particles: inches or millimetres; fine: screen size; very fine: micrometres or nanometres; ultrafine: sometimes described by surface area per unit mass (m²/g).'))
S.append(B('Screening > 50 µm; sedimentation and elutriation > 1 µm; permeability method ≈ 1 µm.'))
S.append(B('Instrumental analysers: electronic particle counter (Coulter counter), laser-diffraction analysers, X-ray or photo-sedimentometers, dynamic light-scattering techniques.'))
S.append(PageBreak())

# ------------------------------------------------------------- Lecture 2
S.append(H1('MODULE 1  \u00b7  LECTURE 2  \u2014  Screening and Screen Analysis'))
S.append(H2('Screen geometry'))
S.append(F('Mesh number          = number of openings per linear inch',
           'Clear opening (inch) = 1/(mesh number) − wire thickness',
           'Pitch  p = w + d      (p = pitch, w = aperture width, d = wire diameter)'))
S.append(B('Aperture width w: distance between two adjacent warp or weft wires, measured in the projected plane at the mid positions.'))
S.append(B('Warp: wires running lengthwise of the woven cloth. Weft: wires running across.'))
S.append(B('Standard series: BSS (British Standard Screen), IMM (Institute of Mining &amp; Metallurgy), U.S. Tyler mesh (Appendix 5 of the text), U.S. ASTM.'))

S.append(H2('Notation and experimental procedure'))
S.append(B('14/20 means "through 14 mesh and on 20 mesh"; −14 +20 means "passes 14 and is retained on 20".'))
S.append(B('Minus (−) material / undersize passes the screen; plus (+) material / oversize is retained on it.'))
S.append(B('A set of standard screens is stacked smallest mesh at the bottom, largest at the top. The sample goes on the top screen and the stack is shaken mechanically for a definite time (~20 min). Each increment is removed and weighed, and the masses are converted to mass fractions or percentages of the total sample. Particles passing the finest screen are caught in the bottom pan.'))

S.append(H2('The standard screen series'))
S.append(F('Base      : opening of the 200-mesh screen = 0.074 mm',
           'Ratio     : area of the openings of a screen = 2 × area of the next smaller screen',
           '            ⇒ mesh-dimension ratio = √2 = 1.41',
           'Intermediate screens: mesh dimension = 2<sup>1/4</sup> = 1.189 times the next smaller standard screen'))

S.append(H2('Differential vs cumulative analysis'))
S.append(B('Differential analysis tabulates the mass (or number) fraction in each size increment against the average particle size (or size range) of the increment.'))
S.append(B('Cumulative analysis adds the individual increments consecutively, starting with the increment containing the smallest particles, and plots the cumulative sums against the maximum particle diameter of the increment.'))
S.append(B('Methods based on the cumulative analysis are more precise in principle, since the assumption that all particles in a fraction are of equal size is not needed; measurement accuracy rarely justifies it, so calculations are nearly always based on the differential analysis.'))
S.append(B('For mixtures of particles of various sizes and densities: sort the mixture into fractions of constant density and approximately constant size, weigh each fraction (or count the particles), apply the area and number equations to each fraction and add the results.'))
S.append(PageBreak())

# ------------------------------------------------------------- Lecture 3
S.append(H1('MODULE 1  \u00b7  LECTURE 3  \u2014  Mixed Particle Sizes: Derivations and Average Diameters'))
S.append(H2('Basis'))
S.append(B('A sample of uniform particles of diameter D<sub>p</sub> is separated into a number of fractions, each fraction i consisting of particles of average size D<sub>pi</sub> and constant density ρ<sub>p</sub>.'))
S.append(B('m = total mass of the sample; m<sub>i</sub> = mass of the i-th fraction; x<sub>i</sub> = m<sub>i</sub>/m = mass fraction of the i-th increment.'))
S.append(B('Other symbols: v<sub>p</sub> = volume of one particle, s<sub>p</sub> = surface area of one particle, N = number of particles.'))

S.append(H2('Step 1 \u2014 surface area and specific surface area'))
S.append(F('(1)  Sphericity                  Φ<sub>s</sub> = 6 v<sub>p</sub>/(D<sub>p</sub> s<sub>p</sub>)   ⇒   s<sub>p</sub> = 6 v<sub>p</sub>/(D<sub>p</sub> Φ<sub>s</sub>)',
           '(2)  Number of particles         N = m/(ρ<sub>p</sub> v<sub>p</sub>)',
           '(3)  Total surface area          A = N s<sub>p</sub> = [m/(ρ<sub>p</sub> v<sub>p</sub>)] × [6 v<sub>p</sub>/(Φ<sub>s</sub> D<sub>p</sub>)] = 6m/(ρ<sub>p</sub> Φ<sub>s</sub> D<sub>p</sub>)',
           '(4)  Area of the i-th fraction   A<sub>i</sub> = 6 m<sub>i</sub>/(ρ<sub>p</sub> Φ<sub>s</sub> D<sub>pi</sub>)',
           '(5)  Specific surface area       A<sub>i</sub>/m<sub>i</sub> = 6/(ρ<sub>p</sub> Φ<sub>s</sub> D<sub>pi</sub>)',
           '(6)  Net specific surface area of the mixture  (m<sub>i</sub>/m = x<sub>i</sub>):',
           '     A<sub>w</sub> = 6x<sub>1</sub>/(ρ<sub>p</sub>Φ<sub>s</sub>D<sub>p1</sub>) + 6x<sub>2</sub>/(ρ<sub>p</sub>Φ<sub>s</sub>D<sub>p2</sub>) + … = 6/(ρ<sub>p</sub> Φ<sub>s</sub>) Σ<sub>i=1…n</sub> (x<sub>i</sub>/D<sub>pi</sub>)',
           '(7)  A<sub>w</sub> = 6/(Φ<sub>s</sub> ρ<sub>p</sub> ' + Dbar + '<sub>s</sub>)',
           '(8)  Volume-surface (Sauter) mean diameter',
           '     ' + Dbar + '<sub>s</sub> = 1/[Σ(x<sub>i</sub>/D<sub>pi</sub>)]  =  6/(Φ<sub>s</sub> ρ<sub>p</sub> A<sub>w</sub>)   ←  the result used most often'))

S.append(H2('Step 2 \u2014 number of particles (volume shape factor)'))
S.append(B('Write the volume of a particle as v<sub>p</sub> = a D<sub>p</sub>³, where a is the volume shape factor (a = π/6 for a sphere); a is constant and independent of size.'))
S.append(F('(9)   N = m/(a ρ<sub>p</sub> D<sub>p</sub>³)',
           '(10)  N<sub>i</sub> = m<sub>i</sub>/(a ρ<sub>p</sub> D<sub>pi</sub>³)                    (i-th fraction)',
           '(11)  N<sub>i</sub>/m<sub>i</sub> = 1/(a ρ<sub>p</sub> D<sub>pi</sub>³)                  (specific number)',
           '(12)  N<sub>w</sub> = (1/(a ρ<sub>p</sub>)) Σ(x<sub>i</sub>/D<sub>pi</sub>³)          (particles per unit mass)',
           '(13)  N<sub>w</sub> = 1/(a ρ<sub>p</sub> ' + Dbar + '<sub>v</sub>³)   ⇒   ' + Dbar + '<sub>v</sub> = [1/Σ(x<sub>i</sub>/D<sub>pi</sub>³)]<sup>1/3</sup> = (1/(N<sub>w</sub> a ρ<sub>p</sub>))<sup>1/3</sup>'))

S.append(H2('Summary of average particle sizes (from the slides)'))
S.append(F('Sauter (volume-surface):  ' + Dbar + '<sub>s</sub> = 6/(Φ<sub>s</sub> ρ<sub>p</sub> A<sub>w</sub>)  =  1/Σ<sub>i=1…n</sub>(x<sub>i</sub>/D<sub>pi</sub>)',
           'Volume mean:              ' + Dbar + '<sub>v</sub> = [1/Σ(x<sub>i</sub>/D<sub>pi</sub>³)]<sup>1/3</sup>',
           'Arithmetic mean:          ' + Dbar + '<sub>N</sub> = Σ(N<sub>i</sub> D<sub>pi</sub>)/ΣN<sub>i</sub> = Σ(N<sub>i</sub> D<sub>pi</sub>)/N<sub>T</sub>',
           'Mass mean:                ' + Dbar + '<sub>w</sub> = Σ x<sub>i</sub> D<sub>pi</sub>',
           'Particles per unit mass:  N<sub>w</sub> = (1/(a ρ<sub>p</sub>)) Σ(x<sub>i</sub>/D<sub>pi</sub>³)'))
S.append(PageBreak())

# ------------------------------------------------------------- Lecture 4
S.append(H1('MODULE 1  \u00b7  LECTURE 4  \u2014  Particulate Masses: Properties, Storage, Conveying, Mixing'))
S.append(H2('Properties of particulate masses'))
S.append(B('Masses of dry, non-sticky solid particles have many of the properties of a fluid, but differ as follows:'))
S.append(B('the pressure is not the same in all directions;', 2))
S.append(B('a shear stress applied at the surface of a mass is transmitted throughout a static mass of particles unless failure occurs;', 2))
S.append(B('the density of the mass varies with the degree of packing of the grains;', 2))
S.append(B('before a tightly packed mass can flow it must increase in volume, so that interlocking grains can move past one another;', 2))
S.append(B('when granular solids are piled on a flat surface the sides of the pile are at a definite reproducible angle with the horizontal (angle of repose; the related angle of internal friction is also used).', 2))
S.append(B('By flow properties, particulate solids are divided into non-cohesive materials (grain, dry sand, plastic chips) that flow readily out of a bin or silo, and cohesive solids (wet clay) characterised by reluctance to flow through openings.'))

S.append(H2('Bulk storage, bins and silos'))
S.append(B('Coarse solids (gravel, coal) are stored outside in large piles unprotected from the weather; outdoor storage can cause dusting or leaching of soluble material. Solids too valuable or too soluble to expose are stored in bins, hoppers or silos.'))
S.append(B('In a bin or silo the lateral pressure exerted on the walls at any point is less than that predicted from the head of material above that point.'))
S.append(B('Wall–solid friction, whose effect is felt throughout the mass because of interlocking, offsets the weight of the solid and reduces the pressure on the floor; the vertical pressure on the floor or packing support is much smaller than that of a column of liquid of the same density and height.'))
S.append(B('Solids are best discharged through an opening in the floor: flow through a side opening is uncertain, increases the lateral pressure on the other side while flowing, and a bottom outlet is less likely to clog and does not induce abnormally high wall pressures.'))

S.append(H2('Conveying'))
S.append(B('Belt conveyors and bucket elevators, closed-belt conveyors with zipper-like fasteners, drag and flight conveyors — all include a return leg carrying the empty belt or chain from the discharge back to the loading point.'))
S.append(B('Vibrating, pneumatic and screw conveyors have no return leg but operate only over relatively short distances.'))

S.append(H2('Mixing of solids \u2014 statistical measures of mixer performance'))
S.append(B('Mixing of solids, free-flowing or cohesive, resembles to some extent the mixing of low-viscosity liquids: two or more separate components are intermingled to form a more or less uniform product. Some equipment used for blending liquids can occasionally be used for solids.'))
S.append(B('Mixing is harder to define for solids and pastes than for liquids; quantitative measures are based on statistical procedures applied to spot samples taken from the mix at various times. A mixture in which one component is randomly distributed through another is said to be completely mixed.'))
S.append(F('Granular non-cohesive solids — N spot samples, each of n particles:',
           '  s  = √[ Σ(x<sub>i</sub> − ' + xbar + ')² / (N − 1) ]        standard deviation of the sample analyses',
           '  σ<sub>e</sub> = √[ μ<sub>p</sub>(1 − μ<sub>p</sub>)/n ]              theoretical s.d. for a completely random mixture',
           '  I<sub>s</sub> = σ<sub>e</sub>/s                        mixing index (increases as mixing proceeds)',
           'Cohesive solids and pastes — mass fractions instead of numbers:',
           '  σ<sub>0</sub> = √[ μ(1 − μ) ]                   theoretical s.d. at zero mixing (at the beginning)',
           '  I<sub>s</sub> = σ<sub>0</sub>/s                        mixing index for pastes'))
S.append(N('x<sub>i</sub> = fraction of component A in each sample (number fraction for non-cohesive, mass fraction for cohesive); ' + xbar + ' = average of the measured fractions; '
           'μ<sub>p</sub> = overall number fraction of A in the mixture; μ = overall mass fraction of A. '
           's diminishes towards zero and I<sub>s</sub> increases as mixing proceeds, so a low s (high I<sub>s</sub>) means good mixing.'))
S.append(PageBreak())

# ------------------------------------------------------------- Lecture 5
S.append(H1('MODULE 1  \u00b7  LECTURE 5  \u2014  Size Reduction (Comminution)'))
S.append(H2('Purpose, mechanisms, influencing factors'))
S.append(B('Cutting or breaking solids into smaller pieces is called comminution. Reasons: to get a workable size, to increase reactivity, to separate unwanted ingredients by mechanical methods, to handle and dispose easily.'))
S.append(B('Objectives: increase the surface area, because in most chemical reactions and some unit operations (drying, adsorption, leaching) the reaction or transfer is directly proportional to the area of contact between the solid and the second phase; produce particles of the desired shape, size or size range and specific surface; separate unwanted particles effectively; dispose of solid wastes easily; mix solid particles more intimately; improve handling, storage and transportation characteristics.'))
S.append(B('Mechanisms of size reduction: compression (nutcracker — coarse reduction of hard solids, very few fines); impact (hammer — coarse, medium and fine products); attrition or rubbing (file — very fine products); cutting or shear (a pair of shears — definite particle size with few or no fines).'))
S.append(B('Properties of solids affecting size reduction: hardness (affects power consumption and wear of the machine); toughness (resistance to impact, the reverse of friability or brittleness); structure (granular, e.g. coal or rock, or fibrous); friability (tendency to fracture during normal handling); moisture content; explosive nature (must be ground wet or in an inert environment); soapiness (a low coefficient of friction of the surface makes crushing more difficult); heat sensitivity (heat generated during size reduction can cause loss of heat-sensitive components).'))
S.append(B('Process factors: moisture and sticky material in the equipment feed; fines in the feed; segregation of feed particles in the crushing chamber; lack of feed control; wrong motor size; insufficient crusher discharge area; insufficient capacity of the crusher discharge conveyor; extremely hard material; surface energy of solids; power consumption; selection of an appropriate crushing chamber.'))

S.append(H2('Energy and power requirement'))
S.append(B('The cost of power is a major expense in crushing and grinding. During size reduction the feed particles are first distorted and strained; the work to strain them is stored temporarily in the solid as mechanical energy of stress, like energy in a coiled spring. As more force is applied the particles distort beyond their ultimate strength and suddenly rupture into fragments, generating new surface.'))
S.append(B('Since a unit area of solid has a definite surface energy, creating new surface requires work, supplied by the release of stress energy when the particle breaks. By conservation of energy, all stress energy in excess of the new surface energy created must appear as heat.'))
S.append(F('Crushing efficiency     η<sub>c</sub> = surface energy created / energy absorbed by solids',
           '                            = e<sub>s</sub>(A<sub>wb</sub> − A<sub>wa</sub>)/W<sub>n</sub>',
           'Mechanical efficiency  η<sub>m</sub> = energy absorbed by solids / total energy input = W<sub>n</sub>/W',
           '',
           'W = W<sub>n</sub>/η<sub>m</sub> = e<sub>s</sub>(A<sub>wb</sub> − A<sub>wa</sub>)/(η<sub>c</sub> η<sub>m</sub>)',
           '',
           'e<sub>s</sub> = surface energy per unit area (J/m²)      A<sub>w</sub> = specific surface area (m²/kg):  A<sub>wb</sub> product, A<sub>wa</sub> feed',
           'W<sub>n</sub> = energy absorbed by unit mass of material (J/kg)',
           '',
           'Power required by the machine (ṁ = feed rate into the equipment, kg/s):',
           '  P = ṁW = [ 6 ṁ e<sub>s</sub> / (η<sub>c</sub> η<sub>m</sub> ρ<sub>p</sub>) ] [ 1/(Φ<sub>sb</sub> ' + Dbar + '<sub>sb</sub>) − 1/(Φ<sub>sa</sub> ' + Dbar + '<sub>sa</sub>) ]',
           'using  A<sub>w</sub> = 6/(Φ<sub>s</sub> ' + Dbar + '<sub>s</sub> ρ<sub>p</sub>)  for product (b) and feed (a), with ρ<sub>a</sub> = ρ<sub>b</sub> = ρ<sub>p</sub>'))

S.append(H2('The three empirical laws'))
S.append(B('Rittinger (1867): the work required in crushing is proportional to the new surface created.'))
S.append(B('Kick (1885): the work required for crushing a given mass of material is constant for the same reduction ratio = (initial particle size)/(final particle size).'))
S.append(B('Bond (1952): the work required to form particles of size D<sub>p</sub> from a very large feed is proportional to the square root of the surface-to-volume ratio of the product.'))
S.append(F('Rittinger:   P/ṁ = K<sub>R</sub> [ 1/' + Dbar + '<sub>sb</sub> − 1/' + Dbar + '<sub>sa</sub> ]        K<sub>R</sub> = 6 e<sub>s</sub>/(Φ<sub>s</sub> ρ<sub>p</sub>)  (Rittinger constant; 1/K<sub>R</sub> = Rittinger number)',
           '             valid for fine grinding, feed < 0.05 mm with Φ<sub>sb</sub> = Φ<sub>sa</sub>',
           '',
           'Kick:        P/ṁ = K<sub>k</sub> ln( ' + Dbar + '<sub>sa</sub>/' + Dbar + '<sub>sb</sub> )          K<sub>k</sub> = Kick constant',
           '',
           'Bond:        P/ṁ ∝ √(s<sub>p</sub>/v<sub>p</sub>) = √(6/(Φ<sub>s</sub> D<sub>p</sub>)) = K √(6/Φ<sub>s</sub>) √(1/D<sub>p</sub>) = K<sub>b</sub>/√D<sub>p</sub>',
           '             P/ṁ = K<sub>b</sub> [ 1/√D<sub>pb</sub> − 1/√D<sub>pa</sub> ]      and, for a very large feed, 1/√D<sub>pa</sub> is negligible',
           '             ⇒  P/ṁ = K<sub>b</sub>/√D<sub>pb</sub>   with   K<sub>b</sub> = 0.3162 W<sub>i</sub>',
           '             P/ṁ = 0.3162 W<sub>i</sub> [ 1/√D<sub>pb</sub> − 1/√D<sub>pa</sub> ]      (D<sub>p</sub> in mm, P in kW, ṁ in ton/h)'))
S.append(N('K<sub>b</sub> = Bond constant, depends on the type of machine and the material being crushed; K<sub>b</sub> = W<sub>i</sub> √(100 × 10⁻⁶) = 0.3162 W<sub>i</sub>, which follows from the definition of W<sub>i</sub> at 100 µm. '
           'Both Kick\u2019s and Rittinger\u2019s laws apply to limited ranges of particle size.'))

S.append(H2('Work index and the generalised law'))
S.append(B('Work index W<sub>i</sub>: the gross energy requirement in kilowatt-hours per short ton (2000 lb) of feed needed to reduce a very large feed to such a size that 80 % of the product passes a 100 µm screen; units kWh/ton. 1 short ton = 2000 lb = 908 kg.'))
S.append(B('Work indices include friction in the crusher (Table 28.2 of the text). For dry grinding W<sub>i</sub> should be multiplied by 4/3.'))
S.append(F('Generalised differential law:   dW = d(P/ṁ) = − K d' + Dbar + '<sub>s</sub> / ' + Dbar + '<sub>s</sub><sup>n</sup>',
           '',
           '   n = 1  →  Kick\u2019s law:      W = −K ln ' + Dbar + '<sub>s</sub> = K { ln(1/' + Dbar + '<sub>sb</sub>) − ln(1/' + Dbar + '<sub>sa</sub>) } = K ln( ' + Dbar + '<sub>sa</sub>/' + Dbar + '<sub>sb</sub> )',
           '   n = 2  →  Rittinger\u2019s law: W = K [ 1/' + Dbar + '<sub>sb</sub> − 1/' + Dbar + '<sub>sa</sub> ]',
           '   n = 3  →  Bond\u2019s law:      W = K [ 1/√D<sub>pb</sub> − 1/√D<sub>pa</sub> ]',
           '',
           '∫ x<sup>n</sup> dx = x<sup>n+1</sup>/(n+1) + C'))
S.append(PageBreak())

# ------------------------------------------------------------- Module 2
S.append(H1('MODULE 2  \u00b7  LECTURE 2  \u2014  Filtration'))
S.append(H2('Definition, driving force, classification'))
S.append(B('Filtration is the removal of solid particles from a fluid by passing the fluid (slurry) through a filtering medium (a porous septum) on which the solids are deposited. Industrial filtration ranges from simple straining to highly complex separations. The fluid may be a liquid or a gas; the valuable stream may be the fluid, or the solids, or both — and sometimes neither, as when waste solids must be separated from waste liquid before disposal.'))
S.append(B('The fluid flows through the medium by virtue of a pressure differential across it: pressure above atmospheric on the upstream side of the medium, a vacuum on the downstream side, or gravity. In a gravity filter the medium can be no finer than a coarse screen or a bed of coarse particles such as sand.'))
S.append(B('Filters are divided into three main groups: cake filters, clarifying filters and crossflow filters.'))
S.append(B('Cake filter: at the start some particles enter the pores of the medium and are immobilised, but soon others collect on the septum surface. After this brief initial period the cake of solids does the filtration, not the septum; a visible cake of appreciable thickness builds up on the surface and must be periodically removed.', 2))
S.append(B('Clarifying (depth) filter: removes small amounts of solids to produce a clean gas or sparkling clear liquids such as beverages. The particles are trapped inside the medium, whose pores are much larger in diameter than the particles to be removed.', 2))
S.append(B('Crossflow filter: the feed suspension flows under pressure at fairly high velocity across the medium; a thin layer of solids may form but the high velocity keeps it from building up. The medium is a ceramic, metal or polymer membrane with pores small enough to exclude most suspended particles; clear liquid passes through, leaving a concentrated suspension behind.', 2))

S.append(H2('Filter media and filter aids'))
S.append(B('A filter medium must: retain the solids to be filtered, giving a reasonably clear filtrate; not plug or blind; be chemically resistant and physically strong enough to withstand the process conditions; permit the cake to discharge cleanly and completely; not be prohibitively expensive.'))
S.append(B('Common medium: canvas cloth, duck or twill weave. Corrosive liquids require woollen cloth, metal cloth of monel or stainless steel, glass cloth or paper. Synthetic fabrics (nylon, polypropylene, various polyesters) are also highly resistant chemically.'))
S.append(B('Slimy or very fine solids are difficult to filter because they form a dense, impermeable cake that quickly plugs the medium; the porosity of the cake must be increased so that the filtrate flows at a reasonable rate.'))
S.append(B('Filter aids are generally granular or fibrous solids which form a highly permeable cake — diatomaceous silica, perlite, purified wood cellulose or other inert porous solids. Properties: low bulk density, porous, chemically inert to the filtrate. They may be used as a precoat or mixed directly with the slurry before filtration.'))

S.append(H2('Principles of cake filtration'))
S.append(B('Flow resistances increase with time as the medium clogs or a cake builds up. The quantities of interest are the flow rate through the filter and the pressure drop across the unit.'))
S.append(B('Constant-pressure filtration: the pressure drop is held constant and the flow rate is allowed to fall with time. Constant-rate filtration: the pressure drop is progressively increased.'))
S.append(B('The liquid passes through two resistances in series — that of the cake and that of the filter medium. The medium resistance, the only resistance in clarifying filters, is normally important only during the early stages of cake filtration; the cake resistance is zero at the start and increases with time. If the cake is washed after filtering, both resistances are constant during washing and the medium resistance is usually negligible.'))
S.append(B('Rate of filtration depends on: the pressure drop across cake and medium; the resistance of the cake; the resistance of the medium; the area of the filtering surface; the viscosity of the filtrate.'))

S.append(H2('Pressure drop through a filter cake'))
S.append(F('   v<sub>0</sub> ∝ ΔP      and      v<sub>0</sub> ∝ 1/L',
           '',
           'Kozeny–Carman  (laminar flow, valid for Re < 1):',
           '   ΔP/L = 150 v\u0304 μ (1 − ε)² / (g<sub>c</sub> Φ<sub>s</sub>² D<sub>p</sub>² ε³)',
           '',
           'Burke–Plummer  (purely empirical, valid for Re > 1000):',
           '   ΔP/L = 1.75 ρ v\u0304² (1 − ε) / (g<sub>c</sub> Φ<sub>s</sub> D<sub>p</sub> ε³)',
           '',
           'Ergun  (entire range of flow rates — viscous loss + kinetic-energy loss):',
           '   ΔP/L = [150 v\u0304 μ/(g<sub>c</sub> Φ<sub>s</sub>² D<sub>p</sub>²)] (1 − ε)²/ε³  +  [1.75 ρ v\u0304²/(g<sub>c</sub> Φ<sub>s</sub> D<sub>p</sub>)] (1 − ε)/ε³'))
S.append(N('v\u0304 = superficial velocity, ε = bed/cake porosity, Φ<sub>s</sub> = sphericity, D<sub>p</sub> = particle diameter, μ = fluid viscosity, ρ = fluid density, g<sub>c</sub> = conversion factor. '
           'The section through the medium and cake shows the fluid pressure P falling from P<sub>a</sub> at the upstream face of the cake to P<sub>e</sub> at the cake–medium interface and on to P<sub>b</sub> through the medium, plotted against the distance L from the medium.'))
S.append(PageBreak())

# ------------------------------------------------------------- problems
S.append(H1('PRACTICE PROBLEMS FROM THE SLIDES'))
S.append(H2('1 \u00b7 Screen analysis of a clay catalyst (Lec. 3)'))
S.append(P('Finely divided clay used as a catalyst in the petroleum industry: density 1.2 g/cc, sphericity 0.5. Size analysis:'))
_cell = ParagraphStyle('cell', fontName='DJ', fontSize=8.6, leading=11.4, textColor=INK, alignment=TA_CENTER)
_cellh = ParagraphStyle('cellh', parent=_cell, fontName='DJB')
tb = Table([[Paragraph(c, _cellh if j == 0 else _cell) for j, c in enumerate(row)]
            for row in [['D<sub>pi</sub> , mm', '0.0252', '0.0178', '0.0126', '0.0089', '0.0038'],
                        ['x<sub>i</sub> (g/g)', '0.088', '0.178', '0.293', '0.194', '0.247']]],
           colWidths=[26*mm] + [18*mm]*5, hAlign='LEFT')
tb.setStyle(TableStyle([('FONTNAME', (0, 0), (-1, -1), 'DJ'), ('FONTSIZE', (0, 0), (-1, -1), 8.6),
                        ('FONTNAME', (0, 0), (0, -1), 'DJB'),
                        ('BACKGROUND', (0, 0), (0, -1), GREY), ('GRID', (0, 0), (-1, -1), 0.5, BORDER),
                        ('ALIGN', (1, 0), (-1, -1), 'CENTER'), ('TEXTCOLOR', (0, 0), (-1, -1), INK),
                        ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
S += [tb, Spacer(1, 2*mm)]
S.append(B('Show the differential and cumulative screen analysis of the mixture.'))
S.append(B('Find the specific surface area A<sub>w</sub> and the Sauter mean diameter of the clay.'))
S.append(B('Find the number of particles in a 1 g sample.'))
S.append(N('Use A<sub>w</sub> = 6/(ρ<sub>p</sub> Φ<sub>s</sub>) Σ(x<sub>i</sub>/D<sub>pi</sub>) with D<sub>pi</sub> in mm and ρ<sub>p</sub> in g/mm³ (1.2 g/cc = 1.2 × 10⁻³ g/mm³), then ' + Dbar + '<sub>s</sub> = 1/Σ(x<sub>i</sub>/D<sub>pi</sub>) and N<sub>w</sub> = (1/(a ρ<sub>p</sub>)) Σ(x<sub>i</sub>/D<sub>pi</sub>³).'))

S.append(H2('2 \u00b7 Screen analysis of crushed quartz (Lec. 3)'))
S.append(P('The screen analysis applies to a sample of crushed quartz. Density of the particles 2650 kg/m³ (0.00265 g/mm³); shape factors a = 0.8 and Φ<sub>s</sub> = 0.571. For the material between 4-mesh and 200-mesh, calculate:'))
S.append(B('A<sub>w</sub> in mm²/g and N<sub>w</sub> in particles/g'))
S.append(B('(b) D̄<sub>v</sub>   (c) D̄<sub>s</sub>   (d) D̄<sub>w</sub>'))
S.append(B('N<sub>i</sub> for the 150/200-mesh increment, and the fraction of the total number of particles in that increment'))

S.append(H2('3 \u00b7 Mixing index in a muller mixer (Lec. 4)'))
S.append(P('A silty soil containing 14 % moisture was mixed in a large muller mixer with 10 wt% of a tracer consisting of dextrose and picric acid. After 3 min of mixing, 12 random samples were taken and analysed colorimetrically for tracer material. Measured concentrations (wt% tracer):'))
S.append(F2('10.24   9.30   7.94   10.24   11.08   10.03   11.91   9.72   9.20   10.76   10.97   10.55'))
S.append(P('Calculate the mixing index I<sub>p</sub> and the standard deviation.'))

S.append(H2('4 \u00b7 Crusher power by Rittinger\u2019s law (Lec. 5)'))
S.append(P('Particles of average feed size 50 × 10⁻⁴ m are crushed to an average product size of 10 × 10⁻⁴ m at the rate of 20 tonnes per hour. At this rate the crusher consumes 40 kW, of which 5 kW is required for running the mill empty. Calculate the power consumption if 12 tonnes/h of this product is crushed to 5 × 10⁻⁴ m size in the same mill. Assume Rittinger\u2019s law is applicable.'))
S.append(N('Net power = 40 − 5 = 35 kW for the first duty; the Rittinger constant K<sub>R</sub> is found from that duty, then the new size range and feed rate are substituted. The empty-mill power is again added back at the end.'))

S.append(Spacer(1, 3*mm))
S.append(HRFlowable(width='100%', thickness=0.7, color=RULE, spaceBefore=2, spaceAfter=5))
S.append(N('Prepared from the Module 1 (Lectures 1–5) and Module 2 (Lecture 2) slide decks of the course. Results follow the notation used on the slides; where a slide carried a hand-worked derivation, the intermediate steps are reproduced above in linear form. '
           'Notation: D<sub>p</sub> particle diameter, Φ<sub>s</sub> sphericity, ρ<sub>p</sub> particle density, s<sub>p</sub> surface area of a particle, v<sub>p</sub> volume of a particle, x<sub>i</sub> mass fraction, '
           'N<sub>i</sub> particles in a fraction, N<sub>T</sub> total number, A<sub>w</sub> specific surface area, N<sub>w</sub> particles per unit mass, a volume shape factor, W<sub>i</sub> work index, '
           'η<sub>c</sub> crushing efficiency, η<sub>m</sub> mechanical efficiency, ε bed porosity, K<sub>R</sub>, K<sub>k</sub>, K<sub>b</sub> the Rittinger, Kick and Bond constants.'))


def footer(canv, doc):
    canv.saveState()
    canv.setFont('DJ', 7.5)
    canv.setFillColor(colors.HexColor('#5A6B77'))
    canv.drawString(18*mm, 12*mm, 'CHE F313 \u00b7 Separation Processes II \u2014 Short Notes & Formula Sheet')
    canv.drawRightString(A4[0] - 18*mm, 12*mm, 'Page %d' % doc.page)
    canv.setStrokeColor(RULE)
    canv.setLineWidth(0.5)
    canv.line(18*mm, 14.5*mm, A4[0] - 18*mm, 14.5*mm)
    canv.restoreState()


def build(path):
    doc = BaseDocTemplate(path, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm,
                          topMargin=15*mm, bottomMargin=18*mm,
                          title='CHE F313 Separation Processes II - Short Notes & Formula Sheet',
                          author='Compiled from course slide decks', subject='Modules 1 & 2 - formula notes')
    doc.addPageTemplates([PageTemplate(id='all',
                                       frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')],
                                       onPage=footer)])
    doc.build(S)
    return path


if __name__ == '__main__':
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else 'notes.pdf'
    build(out)
    print('wrote', out, os.path.getsize(out) // 1024, 'KB')
