# SEPARATION PROCESSES II (CHE F313)

- Course code: CHE F313
- Category: I-Semester 2026-27
- Nalanda: https://nalanda.bits-pilani.ac.in/course/view.php?id=1763
- Reference texts: McCabe, Smith & Harriott, *Unit Operations of Chemical Engineering*, 7th ed. (Ch. 28, 29);
  Swain, Patra & Roy, *Mechanical Operations*, Tata McGraw Hill

## Contents

### `Slides/`
Lecture decks exactly as uploaded (some as `.pptx`, some as compressed `.pdf`):

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

### `Notes/`
- `SP2-notes.tex` — short notes + formula sheet, covering Module 1 Lectures 1–6 and Module 2
  Lectures 1–2. Definitions, the derivation steps (including the hand-worked Lecture 3, Lecture 5
  and Mod 2 Lecture 1 derivations), every formula on the slides, and the practice problems.
- `SP2-Short-Notes-and-Formula-Sheet.pdf` — 13-page A4 PDF compiled from `SP2-notes.tex`.
- `SP2-problems-and-solutions.tex` — **every numerical question that appears in the slides, with its
  solution**, plus the provenance rules used to keep the two kinds of statement apart.
- `SP2-Problems-and-Solutions.pdf` — 11-page A4 PDF compiled from `SP2-problems-and-solutions.tex`.
- `sp2-answers-check.py` — the arithmetic record. Reproduces every derived number in the solutions
  document, in the same order; stdlib-only, run `python3 sp2-answers-check.py`.

Rebuild either PDF after editing its `.tex` with any XeLaTeX-capable TeX distribution, e.g.
`latexmk -xelatex SP2-notes.tex` or `tectonic SP2-problems-and-solutions.tex`. Packages used:
`geometry`, `amsmath`, `amssymb`, `mathtools`, `xcolor`, `booktabs`, `tabularx`, `array`, `multirow`,
`enumitem`, `fancyhdr`, `tcolorbox` (`breakable,skins`), `siunitx`, `hyperref`.

**Both documents are LaTeX in, PDF out. Keep the `.tex` whenever the PDF is edited or replaced** —
the `.tex` is the editable copy; the PDF is a build product.

### Practice problems collected in the notes
1. Screen analysis of a clay catalyst (Mod 1, Lec. 3)
2. Screen analysis of crushed quartz (Mod 1, Lec. 3)
3. Mixing index in a muller mixer (Mod 1, Lec. 4)
4. Crusher power by Rittinger's law (Mod 1, Lec. 5)
5. Screen effectiveness of a quartz mixture (Mod 2, Lec. 1) — answers: `D/F` = 0.42, `B/F` = 0.58, `E` ≈ 67 %

Worked solutions to all five are in `Notes/SP2-Problems-and-Solutions.pdf`; the notes state the
problem, that document solves it.

## Problems & solutions (`Notes/SP2-Problems-and-Solutions.pdf`)

Every numerical that appears on any of the eight decks, segregated by module, lecture and slide, and
numbered `Q1`, `Q2`, … with a matching `Ans` block:

| ID | Source | Topic | Answer summary |
| --- | --- | --- | --- |
| Q1 | Mod 1 Lec 3, slide 10 | Clay catalyst | `A_w` = 1.2354×10⁶ mm²/g, `D̄_s` = 8.09 µm, `N_w` = 4.133×10⁹/`a` per g |
| Q2 | Mod 1 Lec 3, slides 11–12 (also Lec 2 slide 17) | Crushed quartz | `A_w` = 3282 mm²/g, `N_w` = 4148/g, `D̄_v` = 0.484 mm, `D̄_s` = 1.208 mm, `D̄_w` = 1.677 mm, `N_i` = 2074/g, 50 % of particles |
| Q3 | Mod 1 Lec 4, slide 19 | Muller mixer mixing index | `s` = 1.04 wt %, `σ₀` = 0.30, `I_p` = 28.9 |
| Q4 | Mod 1 Lec 5, slide 20 | Rittinger crushing power | `K_R` = 2.1875×10⁻³ kW h m/t, `P₂` = 31.25 kW (26.25 kW net) |
| Q5 | Mod 2 Lec 1, slide 16 | 10-mesh screen effectiveness | `D/F` = 0.42, `B/F` = 0.58, `E_A` = 0.759, `E_B` = 0.881, `E` = 0.669 |

### What is trusted, and in what order

1. **The uploaded decks in `Slides/` — the source of truth.** Questions, given data, formulas and
   methods all come from them. The solutions use the method taught in the lecture that set the
   question; no outside method is substituted.
2. **The reference texts** (McCabe/Smith/Harriott; Swain/Patra/Roy) — used only to confirm a standard
   form or a published answer.
3. **Anything generated in this repository — lowest precedence, always.** Verified by
   `sp2-answers-check.py` rather than by hand.

### Provenance tags used in the solutions document

| Tag | Meaning |
| --- | --- |
| `SOURCE` | transcribed from the uploaded decks — trusted |
| `DERIVED` | generated here (algebra, arithmetic, unit conversion) — verify before relying on it |
| `VERIFY` | an independent re-computation used to check an answer |
| `TEXT` | from a cited textbook; secondary confirmation only |
| `FLAG` | an ambiguity, a missing datum, or an assumption — every place the slides are silent is flagged, never filled in silently |

Rules that follow from this:

- Nothing generated may be presented as slide content: generated material sits in a coloured
  `DERIVED`/`VERIFY` box, source material in a green `SOURCE` box.
- If a `SOURCE` box and a `DERIVED` box ever disagree, the source wins and the solution is recomputed.
- Where a datum is missing from the slides (e.g. the volume shape factor `a` in Q1), the solution says
  so and parameterises or flags it instead of inventing a value.
- No arithmetic is done by hand: every derived number is reproduced by `sp2-answers-check.py`, which is
  kept beside the `.tex` files.
- Answers are reported to the precision the input data supports, with the unrounded value shown where
  that is useful.

### Slides checked and carrying no question

Mod 1 Lec 5 slides 7–18, Mod 1 Lec 3 slides 3–8, Mod 2 Lec 1 slides 11–15 (hand-written derivations,
no question posed); Mod 1 Lec 1 slides 11/18 and Mod 2 Lec 2 slide 16 (conceptual text only); slides
that merely link demonstration videos or show data tables, diagrams and graphs. No question was
invented to fill the list, and no slide that poses a question was left out.
