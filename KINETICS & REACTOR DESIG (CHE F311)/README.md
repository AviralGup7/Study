# KINETICS & REACTOR DESIG (CHE F311)

- Course code: CHE F311
- Category: I-Semester 2026-27
- Nalanda: https://nalanda.bits-pilani.ac.in/course/view.php?id=1591

## Contents

### `Slides/` — lecture decks (as uploaded: scanned `.pdf` slide photographs)

| Deck | Pages | Topic |
| --- | --- | --- |
| `Ch1-krd (1).pdf` | 12 | CRE objectives; rates of reaction; general mole balance; ideal reactors; rocket-engine example; $A\to B$ sizing problem |
| `Ch2-krd (1).pdf` | 15 | Conversion and reactor sizing; Levenspiel plots; reactors in series; space time; sizing numericals; best-arrangement rules; P2-7 |
| `Ch3-krd.pdf` | 16 | Relative rates; power-law kinetics; Arrhenius; reversible rate laws; batch/flow stoichiometric tables; saponification and $A+2B$ examples; dimerisation and phosphine numericals |
| `Ch4-_Krd.pdf` | 23 | Isothermal design algorithm; batch/CSTR/PFR/PBR design; Damköhler; EG production; ethane cracking; pressure drop in PBRs and PFRs; PBR+CSTR problem; MATLAB solution scripts |
| `Ch5_-_krd.pdf` | 19 | Collection and analysis of rate data: differential/integral/half-life/initial-rate methods; nonlinear regression; Michaelis–Menten; Levenspiel numericals (trityl, DME, bombs, MFR/PFR rate equations) |
| `Ch6_krd.pdf` | 18 | Multiple reactions: selectivity and yield; parallel/series patterns; product distribution; two worked numericals |
| `Ch7-_krd.pdf` | 24 | Non-isothermal design: energy balance; adiabatic PFR (butane); equilibrium conversion; interstage cooling; CSTR heat exchange; propylene-oxide CSTR; multiple steady states; runaway |
| `Catalysis_Krd.pdf` | 14 | Heterogeneous catalysis: adsorption, L-H / Eley–Rideal mechanisms; diffusion and reaction in pellets; Thiele modulus, effectiveness factor; Weisz–Prater and Mears criteria; two numericals |
| `Non_ideal_KRD.pdf` | 22 | Residence-time distributions: $E,F,I$ curves; mean and variance; segregation and maximum-mixedness models; tanks-in-series and dispersion models; two-parameter models; two numericals |

The decks are image-only (photographed slides), so every question and datum used below was read
from the slide pictures (OCR-checked by eye at high resolution).

### `Notes/` — written here

- `KRD-Short-Notes-and-Formula-Sheet.tex` — short notes + formula sheet at the depth of the course
  standard (`SEPARATION PROCESSES II (CHE F313)/Notes/SP2-notes.tex`): a `Compiled from` box naming all
  nine decks, a `What is inside` index, a notation table, then one section per deck with subheads,
  the reasoning behind each formula, and the deck's own worked numbers carried through to a boxed
  answer. Closes with a consolidated formula sheet and a table of the four reactor-choice comparisons
  the course keeps asking.
- `KRD-Short-Notes-and-Formula-Sheet.pdf` — 14-page A4 PDF compiled from that `.tex`
  (0 errors, 0 overfull boxes).
- `KRD-Problems-and-Solutions.tex` — **every numerical question or example posed in the nine decks,
  with its solution** (Q1–Q46, each question quoted with its `Source:` line and followed by its
  answer, segregated by deck into Parts A–I).
- `KRD-Problems-and-Solutions.pdf` — 12-page A4 PDF compiled from `KRD-Problems-and-Solutions.tex`.
- `krd-answers-check.py` — the arithmetic record. Reproduces every derived number in the solutions
  document; numpy-only, run `python3 krd-answers-check.py`.

Rebuild either PDF after editing its `.tex` with any LaTeX distribution, e.g.
`tectonic KRD-Problems-and-Solutions.tex`. Packages used: `geometry`, `amsmath`, `amssymb`,
`mathtools`, `xcolor`, `booktabs`, `tabularx`, `array`, `enumitem`, `fancyhdr`,
`tcolorbox` (`breakable,skins`), `siunitx`, `hyperref`.

**Both documents are LaTeX in, PDF out. Keep the `.tex` whenever the PDF is edited or replaced** —
the `.tex` is the editable copy; the PDF is a build product.

## Source and delivered files (the rule)

Everything in this repository is one of two kinds:

- **Source** — the files as uploaded by the course: all of `Slides/`. These are the source of
  truth. Question text, given data, notation, formulas and the **method of solution** all come
  from them.
- **Delivered** — the files created here: `Notes/*.tex`, their PDFs, `krd-answers-check.py`, and
  this README. They are derived work.

Rules that follow:

1. **Nothing delivered is presented as source.** Every question names the deck and slide it comes
   from; the solution uses the method the deck teaches (design equations in conversion form,
   Levenspiel areas, the deck's own Simpson/quadrature rules, stoichiometric tables, Thiele-modulus
   and RTD formulas as printed).
2. **No outside method.** Where a deck prints its own answer (e.g. the EG CSTR volume 197.3 ft³,
   the dispersion conversion 0.68), the delivered solution reproduces it and says so.
3. **Every derived number is reproducible**: run `python3 krd-answers-check.py` and compare.
4. **Where a slide is silent, say so instead of inventing.** Examples in the solutions document:
   Q18 (the deck gives only $X=0.75$ without drop, so the group $kC_{A0}^2/F_{A0}=0.03$ is stated as
   implied by the deck's own answer); Q34 (the slide omits the rate constants — the textbook
   original the slide reproduces is quoted and attributed); Q42 (units of the printed rate
   constants are taken as written and flagged).

## Questions answered in `Notes/KRD-Problems-and-Solutions.pdf`

| ID | Source | Answer summary |
| --- | --- | --- |
| Q1 | Ch1 s.7 | $-r_{H_2}=2.83\times10^4$, $-r_{O_2}=1.41\times10^4$ mol/(m³·s) |
| Q2 | Ch1 s.12 | (a) 99 dm³ both; (b) 2750 / 128 dm³; (c) 66 000 / 660 dm³; (d) 9.9 / 12.8 / 66 h |
| Q3 | Ch2 s.19–24 | CSTR 6.4 m³; PFR 2.165 m³ |
| Q4 | Ch2 s.31–36 | 0.82 + 3.20 = 4.02 m³ |
| Q5 | Ch2 s.37–38 | 0.551 + 1.614 = 2.165 m³ |
| Q6 | Ch2 s.41–42 | $-r_A=0.08$, $r_B=0.02$, $r_C=0.04$; stoichiometry $4A\to B+2C$ |
| Q7 | Ch2 s.45–46 | 2/3 ≈ 0.67 of the feed to branch D (80 L vs 40 L, equal space time) |
| Q8 | Ch2 s.59 | (a) 24 / 71.9 dm³; (b) ≈0.69; (c) 0.70; (d) 0.64; (e) 0.90 |
| Q9 | Ch3 s.5–7 | $r_{NO}=-4$, $r_{O_2}=-2$ |
| Q10 | Ch3 s.6–7 | $r_B=-15$, $r_C=+25$ |
| Q11 | Ch3 s.42–44 | $C_A=C_{A0}(1-X)$, $C_B=C_{A0}(\Theta_B-X/3)$, $C_C=C_{A0}X$, $C_D=C_{A0}X/3$ |
| Q12 | Ch3 s.48–51 | $\Theta_B=3.67$; $C_B=C_{A0}(3.67-2X)$, $C_C=C_D=C_{A0}X$ |
| Q13 | Ch3 s.61 (+Ch5 s.77) | second order, $-r_A\approx0.34\,C_A^2$ (mmol, L, h) |
| Q14 | Ch3 s.63 | $V\approx0.19$ m³ |
| Q15 | Ch4 s.17–20 | $k\approx0.311$ min⁻¹; $t_{90}\approx7.4$ min; 6.4 h at $k=10^{-4}$ s⁻¹ |
| Q16 | Ch4 s.29–38 | 197.3 ft³; parallel $X=0.81$; series $X=0.90$ |
| Q17 | Ch4 s.44–45 | $V\approx1.8$ m³ (65 ft³); ≈3150 tubes |
| Q18 | Ch4 s.55–58 | $X=0.60$ with drop, 0.75 without |
| Q19 | Ch4 s.76–77 | CSTR first: $X\approx0.69$ (0.60 reversed); exit 6.3 atm; (d) ≈0.73 |
| Q20 | Ch4 s.78–79 | $t_{max}=\ln2$ h, $C_B^{max}=1.25$ mol/m³ |
| Q21 | Ch4 s.90–98 | ≈20 m (2 cm, 10%); 10% possible / 20% not in 1.5 cm pipe |
| Q22 | Ch5 s.12–17 | order 2 (slope 1.99); $k'=0.125$, $k=0.25$ dm⁶/(mol²·min) |
| Q23 | Ch5 s.75 | $\pi_0\approx310$ mmHg; 1st order, $k\approx4.4\times10^{-4}$ s⁻¹ |
| Q24 | Ch5 s.72 | $k_1=0.058$, $k_2=0.029$ min⁻¹ |
| Q25 | Ch5 s.73 | complete at 40 min ($X=1$); $k=0.231$ min⁻¹ |
| Q26 | Ch5 s.74 | 2nd order, $k=0.004$ L/(mmol·min) |
| Q27 | Ch5 s.76 | 1st-order approach to $p_{Ae}=150$ mm, $k\approx0.16$ min⁻¹ |
| Q28 | Ch5 s.78–79 | 2nd order, $k\approx0.074$ atm⁻¹min⁻¹ ≈ 2.3 L/(mol·min) |
| Q29 | Ch5 s.80 | ≈8.9 h |
| Q30 | Ch5 s.81 | 6× MFR $X=0.75$; PFR $X=0.67$ |
| Q31 | Ch5 s.82 | $X_A=0.6$, $X_B=0.9$, $C_B=20$ |
| Q32 | Ch5 s.83 | $X_A=0.23$, $X_B=0.12$, $C_B\approx46$ |
| Q33 | Ch5 s.84 | MM fits: $k_3\approx32$ h⁻¹, $C_M\approx0.5$ mmol/L |
| Q34 | Ch5 s.61 | $X_e=0.80$; PFR $X\approx0.51$; CSTR 0.40 (rate law quoted from the textbook original) |
| Q35 | Ch5 s.62 | 1st order, $k\approx0.08$ min⁻¹ |
| Q36 | Ch6 s.32 | (a) 2.86; (b) 4.50; (c) 7.30 mol/L |
| Q37 | Ch6 s.33 | $C_A\approx0.075$, $C_R\approx0.23$, $C_S\approx1.00$ |
| Q38 | Ch7 s.14–17 | $V\approx2$–2.4 m³ at 70% |
| Q39 | Ch7 s.48–51 | $X_1\approx0.40$ @ 459 K, $X_2\approx0.62$ @ 440 K; duties ≈218 / 179 kcal/s |
| Q40 | Ch7 s.57–59 | $X\approx0.84$ at ≈151 °F > 125 °F — cannot be used adiabatically |
| Q41 | Ch7 s.60–74 | with coil $X\approx0.36$ at ≈104 °F — constraint satisfied |
| Q42 | Ch7 s.95 | coupled ODEs; $T\to\approx645$ K, product essentially B (units flagged) |
| Q43 | Catalysis s.48 | $\phi=5.99$; $C_A\approx2.4\times10^{-4}$; $d_p\approx6.8\times10^{-4}$ cm for $\eta=0.8$ |
| Q44 | Catalysis s.57 | rates $2.6\times10^{-5}$ / $2.5\times10^{-4}$ mol/(L·s); $E_{app}\approx14$ kcal/mol |
| Q45 | Non-ideal s.17–19 | $\int C\,dt=50$; ≈0.5 of material spent 3–6 min; $t_m\approx5.2$ min |
| Q46 | Non-ideal s.52–59 | (i) 0.68; (ii) 0.72; (iii) 0.56; (iv) 0.68 |
