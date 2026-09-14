# PROCESS DES PRINCIPLES I (CHE F314)

- Course code: CHE F314
- Category: I-Semester 2026-27
- Nalanda: https://nalanda.bits-pilani.ac.in/course/view.php?id=1682
- Reference texts cited by the decks themselves: Seider, Seader, Lewin & Widagdo, *Product and Process
  Design Principles*, 3rd ed. (2010); Douglas, *Conceptual Design of Chemical Processes* (1988)

## Contents

### `Slides/` — lecture decks (as uploaded)

| Deck | Pages | Topic |
| --- | --- | --- |
| `L-1.pdf` | 22 | Introduction — what chemical process design is; synthesis versus analysis; why design problems are underdefined |
| `L-2.pdf` | 35 | Steps in process design and retrofit; the hierarchy of decisions; the HDA case study; the ethanol example; the Formox and cumene problems |
| `L-4.pdf` | 42 | Synthesis step 2 — the hierarchical approach applied to vinyl chloride manufacture; gross profits; flow diagrams (BFD, PFD, P&ID) |
| `EDM.pdf` | 97 | Economic decision making — the solvent-recovery case study, heuristics H1–H4, the Kremser simplification and the cost model; the two numerical problems on approach temperature and trays |
| `EIA_Selected_Slides.pdf` | 6 | Energy integration analysis — composite curves, pinch, the 10 °F approach temperature, heat-exchanger network grids |

### `Notes/` — written here

- `PDP-Short-Notes-and-Formula-Sheet.tex` — short notes + formula sheet, one compact section per
  deck: the hierarchy of decisions, the synthesis steps and HDA/VCM case-study numbers, heuristics
  H1–H4, the Kremser equation and its simplifications, the TAC optimum, the approach-temperature
  and back-of-envelope distillation rules, and the EIA composite-curve/pinch/area formulas.
- `PDP-Short-Notes-and-Formula-Sheet.pdf` — 2-page A4 PDF compiled from that `.tex`.
- `PDP-Problems-and-Solutions.tex` — **every question or problem posed in the decks above, with its
  solution**, worked only with the method and the data given in the decks (P1–P7, in four parts:
  numerical/heuristic problems, the solvent-recovery case study, the flow-sheet synthesis problems, the
  vinyl chloride case).
- `PDP-Problems-and-Solutions.pdf` — 10-page A4 PDF compiled from that `.tex`.
- `pdp-answers-check.py` — the arithmetic record. Reproduces every computed number of P1 and P2;
  stdlib-only, run `python3 pdp-answers-check.py`.

Rebuild the PDF after editing the `.tex` with any LaTeX distribution, e.g.
`tectonic PDP-Problems-and-Solutions.tex` or `latexmk -xelatex PDP-Problems-and-Solutions.tex`.
Packages used: `geometry`, `fontenc`, `amsmath`, `amssymb`, `mathtools`, `xcolor`, `booktabs`,
`tabularx`, `array`, `enumitem`, `fancyhdr`, `tcolorbox` (`breakable,skins`), `siunitx`, `hyperref`.

**LaTeX in, PDF out. Keep the `.tex` whenever either PDF is edited or replaced** — the `.tex` is
the editable copy; the PDF is a build product.

## Source and delivered files (the rule)

- **Source** — the files as uploaded by the course: everything in `Slides/`. These are the source of
  truth. Question text, given data, notation, formulas and the **method of solution** all come from
  them.
- **Delivered** — the files created here: `Notes/PDP-Short-Notes-and-Formula-Sheet.tex`,
  `Notes/PDP-Problems-and-Solutions.tex`, their PDFs, the checker `Notes/pdp-answers-check.py`,
  and this README. They are derived work.

Rules that follow:

1. **Nothing delivered is presented as source.** A question is quoted from the deck; the solution is
   worked only with the method taught in that deck, and each question names the slide it comes from.
2. **No outside method.** Where a deck gives a particular route (Douglas's hierarchy, the deck's own
   cost model, its own heuristics H1–H4), that route is used.
3. **Every computed number is reproducible**: run `python3 pdp-answers-check.py`.
4. **Where a deck is silent, say so.** Several questions are posed in the decks without a worked
   solution; the document marks those solutions as built from the deck's own method and data, and
   flags anything the deck leaves open (e.g. the MIBK loss printed on `EDM.pdf` slide 41 does not
   reproduce from its own printed factors — the document says so and shows that the decision is
   unaffected).
5. Answers are reported to the precision the input data supports.

## Questions answered in `Notes/PDP-Problems-and-Solutions.pdf`

| ID | Source | Topic | Answer |
| --- | --- | --- | --- |
| P1 | `EDM.pdf` slides 94–95 | Bounds on the heat-exchanger approach temperature (the 10 °F rule of thumb) | Bounds: `T₁ ≥ 277 °F`, i.e. an approach of at least 10 °F at the steam generator. Optimum approach 21.5 °F (`T₁*` = 288.5 °F), TAC = $43 143/yr; the 10 °F rule costs $49 745/yr, about 15 % more; the range 14–31 °F is within 5 % of the optimum |
| P2 | `EDM.pdf` slide 96 | Back-of-envelope tray count versus Fenske's equation | The two agree when `λ/R = (3/2) ln S · T_avg`, i.e. for `λ ≈ 10 kcal/mol` at 99 % split; benzene/toluene: 8.05 trays by the rule, 8.03 by Fenske |
| P3 | `EDM.pdf` slides 3–93 | Solvent-recovery case study — Q1 how to recover acetone, Q2 the cheapest alternative, Q3 discarding the process water — and the design the deck builds | Ans 1: alternatives listed; absorption with water developed. Ans 2: adsorption is cheapest below 5 % solute (here 1.47 %), but condensation/absorption are preferred in practice. Ans 3: yes — the temperature check (90 °F supply, below 120 °F return) and the negligible water cost ($25 600/yr against an EP of $1.315×10⁶/yr) justify it; this is heuristic H1. Design numbers: `m` = 2.02, `L` = 1943 mol/hr, 99.5 % recovery material balance, stream costs, the MIBK alternative rejected, 10 trays for 99 % (exact 10.1) and 16 for 99.9 %, optimum loss 0.4 % (99.6 % recovery) |
| P4 | `L-2.pdf` slide 29 (answers slides 30–32) | Ethanol by the hydration of ethylene — general, recycle and input–output structures | The deck's own three structures, described in words (the answer slides are diagrams) |
| P5 | `L-2.pdf` slide 33 | Formox process — hierarchy of flow sheets | The three structures built from the deck's description by the deck's hierarchy (the deck poses the problem without a worked answer; this is said in the document) |
| P6 | `L-2.pdf` slide 34 | Cumene process — hierarchy of flow sheets | Same treatment: the three structures from the deck's description |
| P7 | `L-4.pdf` slides 3–30 | Vinyl chloride case — pathway gross profits and the flowsheet decisions | Gross profits (cents/lb VC): path 2 −9.33, path 3 11.94, path 4 3.42, path 5 7.68; flows for 100 000 lb/hr VC: Cl₂ 113 400, C₂H₄ 44 900, C₂H₄Cl₂ 158 300 (plus 105 500 recycled, 263 800 to the mixer), HCl 58 300 lb/hr; distillation at 12 atm and 4.8 atm with the feed at 35 °C or above; the pump–vaporise–superheat sequence to 26 atm, 242 °C, 500 °C |

## Note on `EIA_Selected_Slides.pdf`

Despite the file name, these six selected slides are **energy integration analysis** — composite
curves, the pinch, the 10 °F approach temperature and heat-exchanger network grids — which is the
subject of `L-2.pdf` slide 11 and the background of the approach-temperature rule in P1, so the file
is kept in `Slides/` of this course.
