# ATOMIC & MOLECULAR SIMULATION (CHE F497)

- Course code: CHE F497
- Category: I-Semester 2026-27
- Nalanda: https://nalanda.bits-pilani.ac.in/course/view.php?id=1707
- Instructor (on the decks): Dr. Sarbani Ghosh, Department of Chemical Engineering, BITS Pilani
- Tools named on the decks: VMD (visualisation), Avogadro (molecular modelling); C, Fortran or MATLAB
  for the exercises

## Contents

### `Slides/` — lecture decks (as uploaded)

| Deck | Pages | Lecture / module | Topic |
| --- | --- | --- | --- |
| `L1_L2_AMS_2026.pdf` | 15 | Lecture Class I, II & III — 4th, 6th & 7th Aug 2026 | **Module I** — Introduction to Atomic and Molecular Simulation Methods & Recap of Statistical Thermodynamics: why computer simulation; history (Colossus, MANIAC, Vineyard 1959); atomistic vs molecular simulation and the micro/meso/macro scales; the three levels of method (QM-based, classical MD, hybrid QM-MM); thermodynamics vs statistical mechanics; micro- and macrostates; Boltzmann relation, partition function, ensembles, time vs ensemble averages |
| `L4-L5.pdf` | 13 | Lecture Class IV & V — 11th & 13th Aug 2026 | **Module II** — Quantum Chemical Methods: why quantum mechanics; matter–radiation theory; wave–particle duality; the wave function and Born's statistical interpretation; Schrödinger equation; Born–Oppenheimer approximation and the adiabatic potential energy surface; dimensionality of the many-body problem (CO₂, 100-Pt nanocluster); Hartree product; electron density and the Pauli principle; Hohenberg–Kohn theorems; Kohn–Sham equations and the self-consistent algorithm; plane-wave DFT, supercells, lattice parameters, BCC/FCC |
| `L6-7.pdf` | 11 | Module II continuation | DFT (recap), exchange–correlation functional, uniform electron gas, **LDA** and **GGA** (PW91, PBE); localized vs spatially extended functions; wave-function-based methods; **Hartree–Fock**, spin orbitals, antisymmetry principle, **Slater determinant**; 1998 Nobel Prize (Kohn, Pople) |

All three decks carry a real text layer, so their content was read directly from the PDFs — no OCR
was needed for this subject.

### `Notes/` — written here

- `AMS-Short-Notes-and-Formula-Sheet.tex` — short notes + formula sheet covering all three decks,
  organised as one section per deck plus a consolidated formula sheet and a table of the order in
  which the decks introduce their approximations.
- `AMS-Short-Notes-and-Formula-Sheet.pdf` — 8-page A4 PDF compiled from that `.tex`.

The document follows the structure and depth of `SEPARATION PROCESSES II (CHE F313)/Notes/SP2-notes.tex`,
which is the standard for notes in this repository.

Rebuild the PDF after editing the `.tex` — see **Building the PDFs** below.

**Both documents are LaTeX in, PDF out. Keep the `.tex` whenever the PDF is edited or replaced** —
the `.tex` is the editable copy; the PDF is a build product.

### Questions document — status

CHE F497 does **not** yet have a segregated problems-and-solutions document, and this is deliberate
rather than an omission.

Reading all 39 pages of the three decks, **no numerical problem is posed anywhere in them**. The
decks are conceptual: they develop method ideas (what a wave function is, why the many-body problem
is hard, what the Hohenberg–Kohn theorems say, how the Kohn–Sham cycle runs, what LDA and GGA
assume) and quote only illustrative figures — `>100` million tons of NH₃ per year, `1 %` of world
energy, `T > 400 °C` and `P > 100 atm` for ammonia synthesis, `1800×` the electron mass for a
nucleon, CO₂ as `N = 22, M = 3` giving a 66-dimensional wave function, a 100-Pt nanocluster needing
`>23 000` dimensions, `12–26` steps in ammonia synthesis, `<100 ps` for QM-based dynamics, and the
1/1000 µs/1 s scale boundaries. None of these is attached to a question or a required answer.

Per the rule applied across this repository — *no question is invented to fill a list* — a questions
document will be added if the course uploads a tutorial sheet, test paper or problem set for this
subject. Until then this record is the audit trail: the decks were read in full and carry no
numericals.

## Source and delivered files (the rule)

Everything in this repository is one of two kinds:

- **Source** — the files as uploaded by the course: all of `Slides/`. These are the source of truth.
  Definitions, notation, formulas, worked arguments and illustrative figures all come from them.
- **Delivered** — the files created here: `Notes/AMS-Short-Notes-and-Formula-Sheet.tex`, its PDF, and
  this README. They are derived work.

Rules that follow:

1. **Nothing delivered is presented as source.** Every statement in the notes is traceable to a named
   deck, and the notes say which deck each section comes from.
2. **No outside method or fact.** Where a deck gives a particular form (e.g. its four-term
   decomposition of the energy functional, its four-step Kohn–Sham algorithm, its wording of the
   Hohenberg–Kohn theorems), that form is reproduced rather than a textbook equivalent.
3. **Where a deck is incomplete, say so.** The slides show the Kohn–Sham equations, the Hartree
   potential and the density expression as *figures*, and the extracted text does not carry their
   symbols; the notes therefore state those relations in the standard notation and say what each term
   means, without claiming to reproduce a figure the text layer does not contain.
4. **Nothing is invented to fill space.** The absence of numericals is recorded above instead of being
   papered over with problems taken from elsewhere.

## Building the PDFs

The notes compile with the repository's LaTeX harness:

```bash
bash /home/user/.texbuild/setup.sh          # installs npm `texlive`, ~2 s
cd /tmp/texplay/build
node ../compile.mjs ../node_modules/texlive/texlive \
     AMS-Short-Notes-and-Formula-Sheet.tex AMS-Short-Notes-and-Formula-Sheet.pdf 2
```

The document is written to compile with the base TeX tree only — `geometry`, `amsmath`, `amssymb`,
`amsfonts`, `bm`, `color`, `array`, `tabularx`, `longtable`, `multicol`, `calc`, `graphicx`,
`fancyhdr`, `hyperref` — so it also builds with a full TeX Live, TeX Gyre or Tectonic installation.
The SP2-standard preamble (section bars, formula boxes, footer) is generated by
`/home/user/.texbuild/mknotes.py`; the `.tex` in `Notes/` already has it expanded in, so no
generator is needed to edit or rebuild it.
