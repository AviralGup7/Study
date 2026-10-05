# SEPARATION PROCESSES II (CHE F313)

- Course code: CHE F313
- Category: I-Semester 2026-27
- Nalanda: https://nalanda.bits-pilani.ac.in/course/view.php?id=1763
- Reference texts: McCabe, Smith & Harriott, *Unit Operations of Chemical Engineering*, 7th ed. (Ch. 28, 29);
  Swain, Patra & Roy, *Mechanical Operations*, Tata McGraw Hill

## Contents

### `Slides/` — lecture decks (as uploaded: some `.pptx`, some compressed `.pdf`)

| Deck | Format | Module / topic |
| --- | --- | --- |
| `Mod1-Lecture 1.pptx` | pptx | Properties and handling of particulate solids — introduction, particle characterisation, sphericity |
| `Mod1-Lecture 2.pptx` | pptx | Screening and screen analysis, standard screen series, differential vs cumulative |
| `Mod1-Lecture 3.pptx` | pptx | Mixed particle sizes — derivations of average diameters (contains hand-worked ink slides) |
| `Mod1-Lecture 4.pptx` | pptx | Properties of particulate masses, storage/bins/silos, conveying, mixing statistics |
| `Mod1-Lecture 5.pptx` | pptx | Size reduction (comminution) — energy laws, work index, generalised law |
| `Mod1-Lecture 6-compressed.pdf` | pdf | Equipment for size reduction — crushers, grinders, ultrafine grinders, cutting machines, circuits, energy consumption |
| `Mod 2-Lecture 1-compressed.pdf` | pdf | Mechanical separations; screening and screen effectiveness — material balance and overall effectiveness |
| `Mod 2-Lecture 2.pptx` | pptx | Filtration — media, filter aids, cake filtration, Kozeny–Carman / Burke–Plummer / Ergun |
| `Mod 2-Lecture 3 - Copy.pptx` | pptx | Pressure drop through the filter cake — channel model, working equations |
| `Mod 2-Lecture 4-compressed.pdf` | pdf | Constant-rate filtration |
| `Mod 2-Lecture 5.pptx` | pptx | Continuous filtration — the rotary-drum filter |
| `Mod 2-Lecture 6.pptx` | pptx | Centrifugal filtration and washing rate |
| `Mod 2-Lecture 7.pptx` | pptx | Clarifying, crossflow and membrane filters; sedimentation |
| `Mod 2-Lecture 8-compressed.pdf` | pdf | Centrifugal sedimentation |
| `Problems.pptx` | pptx | Practice problems — ball-mill speed, plate-and-frame washing time, hydraulic classifier (answers as Q13–Q15 in the questions document) |

### `Tutorials/` — tutorial sheets (as uploaded)

| Sheet | Date | Problems |
| --- | --- | --- |
| `Tutorial 3.pptx` | 01-09-2026 | sieve analysis of a crushed solid (six parts); shape factor and sphericity of an irregular particle |
| `Tutorial 4_7_9_2026.pptx` | 07-09-2026 | crusher power when capacity and product size change; energy per kg of material (Kick's law) |

### `Tests/` — test papers with the instructor's solutions (as uploaded)

| Paper | Date | Problem |
| --- | --- | --- |
| `Quiz1_Soln.pdf` | Quiz-1, 03-09-2026 | mixing index of a binary solid mixture (ten samples) |
| `TT1_Solution.pdf` | Tutorial Test 1, 07-09-2026 | Bond work index from a plant power draw; power for a finer product |

### `Notes/` — written here

- `SP2-notes.tex` — short notes + formula sheet, covering **all 14 lecture decks**: Module 1
  Lectures 1–6 and Module 2 Lectures 1–8. Definitions, the derivation steps (including the
  hand-worked Mod 2 Lecture 3 (considerably expanded), Lecture 5, Mod 2 Lecture 1 and Mod 2 Lecture 7 derivations), every
  formula on the slides, and the practice problems.
  **This is the canonical standard** for notes structure, style and depth across the whole
  repository; the other subjects' notes are built to match it. It is written for XeLaTeX with a
  full TeX Live (`xcolor`, `tcolorbox`, `siunitx`, `booktabs`, `enumitem`, `mathtools`, `multirow`).
- **Module 2 Lecture 3** (`Mod 2-Lecture 3 - Copy.pptx`) is almost entirely hand-written: slides 4--23
  carry no text at all, only ink pages, and were read as images (the ink is white-on-transparent, so
  the page images had to be flattened before reading). That section of `SP2-notes.tex` was then
  rewritten as a **step-by-step derivation** rather than a list of results: a six-step plan box, the
  bundle-of-channels model and its justification, the two sphericity equations, the elimination of
  $S_0$ between the surface balance (eq. 2) and the void-volume balance (eq. 3) shown line by line,
  the equivalent diameter checked at $\varepsilon=0.4$ ($D_{eq}=0.44\,\Phi_sD_p$), the channel-to-superficial
  velocity step, the Kozeny--Carman substitution with the arithmetic ($32\times\tfrac94=72$) and the
  $\lambda_1$/150 correction explained, Burke--Plummer and the Ergun sum, the cake-plus-medium split,
  the mass balance that removes $\mathrm{d}L$, the integration to $\Delta P_c$, the definitions of $\alpha$
  and $R_m$, the working form and how the $t/V$-against-$V$ line gives both $\alpha$ and $R_m$, the
  compressibility relation $\alpha=\alpha_0(\Delta P)^{s}$, a symbol list for the lecture, and one
  worked numerical illustration (marked as not from the deck).
- **Module 2 Lecture 6** (`Mod 2-Lecture 6.pptx`) is likewise picture-heavy: the radial-section and
  working-machine figures, the ``Summary'' slide's working equation, and the cycle-time / daily-output
  ink slide carry the content. That section now states the basket geometry and the machine, the six
  assumptions as listed on the deck, the derivation from the centrifugal pressure drop to $q$, both
  cases (thin cake, and cake area carried through the integration) with $\overline{A}_a$ and
  $\overline{A}_L$, the two limits, the filter-press / leaf-filter wash rates, the washing-time form,
  and the cycle-time and daily-output relations. It remains deliberately short, following the deck.
- **Module 2 Lecture 8** (`Mod 2-Lecture 8-compressed.pdf`) is a compressed PDF whose pages 15--21 and
  23--24 have **no text layer at all** --- the derivation lives there as scans/ink. Those pages were
  read as images and the section rebuilt: the trajectory geometry, the settling-time integral in full,
  the cut point and $q_c$ with the deck's own reading of both, the **thin-layer derivation with the
  $s/2$ settling distance** (the factor 2 in $q_c=2Vu_t/s$ was previously left unexplained and the old
  algebra for it was inconsistent), the $\Sigma$ scale-up with the deck's Table 30.5, and the
  $q_c=2\Sigma u_g$ collapse.
- **Module 2 Lecture 7** (`Mod 2-Lecture 7.pptx`, 17-09-2026) is mostly *handwritten*: slides 9–12,
  19–24, 26–28, 31 and 33 carry the content as ink pictures, not as text. That section of
  `SP2-notes.tex` was transcribed from those pictures and is written out in full — the
  clarification mechanisms and their plugging rates, the crossflow/dead-end comparison, the
  membrane cut-off chart row by row, the volume-flux equation with concentration polarization
  *derived* (convective flux balanced by back-diffusion, $J_v=K_c\ln[(C_s-C_2)/(C_1-C_2)]$, the gel
  limit and complete rejection), the Sherwood correlation, the five sedimentation assumptions, the
  force balance and its two terminal-velocity forms, $C_D$ and the four settling regions, the
  equal-settling (free-settling) diameter ratios in both the Stokes and Newton regimes, the batch
  sedimentation zones and curve, and the sedimentation-versus-filtration table. The only thing not
  reproduced is the deck's embedded demo video (slide 32), which is a link, not content.
- `SP2-Short-Notes-and-Formula-Sheet.tex` — the same document **ported to the base TeX tree**, so
  it rebuilds with `tools/latex` like every other subject's notes. Produced by
  `tools/latex/port.py` from `SP2-notes.tex`; edit `SP2-notes.tex` and re-port rather
  than editing this file. Verified equivalent: rebuilding through `tools/latex/gen.py`
  reproduces the committed PDF word for word (35 pp, 0 errors, 0 overfull).
  (The standalone file briefly carried a generator regression — `port.py` dropped the
  `\begin{document}` line; fixed 20-09-2026, and the file now also compiles on its own:
  35 pp, 0 errors, 0 overfull.)
- `SP2-notes.pdf` / `SP2-Short-Notes-and-Formula-Sheet.pdf` — 35-page A4 PDF (the two are the same
  document: the canonical source and its base-TeX-tree port, both compiled here from the port).
- `SP2-Problems-and-Solutions.tex` — **every numerical question in the uploaded slides, tutorials,
  tests and `Problems.pptx`, with its solution** (Q1–Q15, each followed by its `Ans` block,
  segregated by source; Part D holds the Module 2 / `Problems.pptx` problems Q12–Q15).
- `SP2-Problems-and-Solutions.pdf` — 16-page A4 PDF compiled from `SP2-Problems-and-Solutions.tex`.
- `sp2-sizing-curves.png` — the differential and cumulative size-distribution figure used by Q6,
  plotted here from the sieve table printed on `Tutorials/Tutorial 3.pptx` slide 2.
- `sp2-answers-check.py` — the arithmetic record. Reproduces every derived number in the solutions
  document, in the same order; stdlib-only, run `python3 sp2-answers-check.py`.

Rebuild either PDF after editing its `.tex` with any LaTeX distribution, e.g.
`tectonic SP2-Problems-and-Solutions.tex` or `latexmk -xelatex SP2-notes.tex`. Packages used:
`geometry`, `amsmath`, `amssymb`, `mathtools`, `xcolor`, `booktabs`, `tabularx`, `array`, `multirow`,
`enumitem`, `fancyhdr`, `tcolorbox` (`breakable,skins`), `siunitx`, `hyperref`.

**Both documents are LaTeX in, PDF out. Keep the `.tex` whenever the PDF is edited or replaced** —
the `.tex` is the editable copy; the PDF is a build product.

## Source and delivered files (the rule)

Everything in this repository is one of two kinds:

- **Source** — the files as uploaded by the course: all of `Slides/`, `Tutorials/` and `Tests/`.
  These are the source of truth. Question text, given data, notation, formulas and the **method of
  solution** all come from them.
- **Delivered** — the files created here: `Notes/SP2-notes.tex`, `Notes/SP2-Problems-and-Solutions.tex`,
  their PDFs, the figure `sp2-sizing-curves.png`, the checker `sp2-answers-check.py`, and this README.
  They are derived work.

Rules that follow:

1. **Nothing delivered is presented as source.** A question is quoted from the source; the solution is
   worked only with the method taught in that source, and each question names the slide, tutorial or
   test it comes from.
2. **No outside method.** Where a source gives a particular route (e.g. Rittinger rather than Bond, the
   slide's own form of the mixing-index variance), that route is used, even when another textbook
   method would also work.
3. **Every derived number is reproducible**: run `python3 sp2-answers-check.py` and compare.
4. **Where the source is silent or self-inconsistent, say so** — do not fill the gap with a guessed
   number. Two examples in the solutions document: the volume shape factor `a` is not given in Q1
   (the answer is written as a function of `a`, with the values for the common choices shown), and the
   shape factor / sphericity data of Q7 do not agree among themselves whichever shape factor is
   assumed (`Φ_s > 1`, impossible) — the document reports the formula result and says why.
5. Answers are reported to the precision the input data supports, with the unrounded value shown where
   that is useful.

## Questions answered in `Notes/SP2-Problems-and-Solutions.pdf`

| ID | Source | Topic | Answer summary |
| --- | --- | --- | --- |
| Q1 | Mod 1 Lec 3, slide 10 | Clay catalyst | `A_w` = 1.2354×10⁶ mm²/g, `D̄_s` = 8.09 µm, `N_w` = 4.133×10⁹/`a` per g |
| Q2 | Mod 1 Lec 3, slides 11–12 (also Lec 2 slide 17) | Crushed quartz | `A_w` = 3282 mm²/g, `N_w` = 4148/g, `D̄_v` = 0.484 mm, `D̄_s` = 1.208 mm, `D̄_w` = 1.677 mm, `N_i` = 2074, 50.0 % of the particles |
| Q3 | Mod 1 Lec 4, slide 19 | Müller-mixer mixing index | `s` = 1.0397 wt %, `σ₀` = 0.30, `I_p` = 28.9 |
| Q4 | Mod 1 Lec 5, slide 20 | Rittinger crushing power | `K_R` = 2.1875×10⁻³ kW h m/t, net 26.25 kW, **total 31.25 kW** |
| Q5 | Mod 2 Lec 1, slide 16 | 10-mesh screen effectiveness | `D/F` = 0.42, `B/F` = 0.58, `E_A` = 0.759, `E_B` = 0.881, **`E` = 0.669** |
| Q6 | Tutorial 3, problem 1 | Sieve analysis of a crushed solid | `D₅₀` = 1.339 mm (log-interpolated 1.317 mm), 1.881×10⁶ particles in 600 g (3135/g), `A_w` = 2.31 m²/g, `D̄_vs` = 1.040 mm |
| Q7 | Tutorial 3, problem 2 | Shape factor and sphericity | `a` = 0.593, `D̄_vs` = 2.18 mm; from the slide's own surface-area datum `Φ_s` = 1.45 — **not physically possible**; the slide's numbers are reported as they stand and the contradiction is explained |
| Q8 | Tutorial 4, problem 1 | Crusher power at a new duty | `K_R` = 52.78 (same units as Q4), **`P₂` = 1.06 kW**; Kick's-law alternative 0.92 kW |
| Q9 | Tutorial 4, problem 2 | Energy per kg (Kick's law) | **`E` = 8.05 kJ/kg** |
| Q10 | `Tests/Quiz1_Soln.pdf` | Mixing index of a binary mixture | `I_s` = 15.6 from the unrounded `s` = 0.03197, 16.1 with the instructor's rounded `s` = 0.031 (instructor's boxed value 16.12) |
| Q11 | `Tests/TT1_Solution.pdf` | Bond work index | **`W_i` = 12.78 kWh/t**, `E₂` = 2.623 kWh/t, `P₂` = 367.2 kW (instructor's boxed value 367.22 kW) |
| Q12 | Mod 2 Lec 8, slide 26 | Clarifying-centrifuge capacity | `q_c` = 210.7 m³/h (0.0585 m³/s) |
| Q13 | `Problems.pptx` slide 2 (critical-speed relation, Mod 1 Lec 6) | Mill speed when the grinding balls are replaced | `n₂` = 14.8 rpm — slightly slower than the present 15 rpm |
| Q14 | `Problems.pptx` slides 3–4 | Plate-and-frame press: washing time; time with doubled area | `K` = 90 m⁶/h, washing rate 0.375 m³/h, `t_w` = 8 h; doubled area: `K` = 360 m⁶/h, 2.5 h |
| Q15 | `Problems.pptx` slide 5 (Example 6.3) | Purity of dressed ore from a hydraulic classifier | purity ≈ 72 % at the 1 mm cut (equal-settling rock size 0.5 mm, 90 % of the rock retained) |

### Practice problems collected in the notes

The five practice problems printed in `Notes/SP2-notes.tex` are Q1–Q5 above; the questions documents
solves them, the notes state them.

### Slides checked and carrying no question

Mod 1 Lec 5 slides 7–18, Mod 1 Lec 3 slides 3–8, Mod 2 Lec 1 slides 11–15 (hand-written derivations,
no question posed); Mod 1 Lec 1 slides 11/18 and Mod 2 Lec 2 slide 16 (conceptual text only); slides
that merely link demonstration videos or show data tables, diagrams and graphs. No question was
invented to fill the list, and no slide, tutorial or test that poses a question was left out.
