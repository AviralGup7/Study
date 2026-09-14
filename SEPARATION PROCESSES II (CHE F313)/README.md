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
- `SP2-notes.tex` — **the source of truth**: LaTeX short notes + formula sheet covering Module 1
  Lectures 1–6 and Module 2 Lectures 1–2. Definitions, the derivation steps (including the
  hand-worked Lecture 3, Lecture 5 and Mod 2 Lecture 1 derivations), every formula on the slides,
  and the practice problems.
- `SP2-Short-Notes-and-Formula-Sheet.pdf` — 13-page A4 PDF compiled from that `.tex`.

Rebuild the PDF after editing the `.tex` with any XeLaTeX-capable TeX distribution, e.g.
`latexmk -xelatex SP2-notes.tex` or `tectonic SP2-notes.tex`. Packages used: `geometry`, `amsmath`,
`amssymb`, `mathtools`, `xcolor`, `booktabs`, `tabularx`, `enumitem`, `fancyhdr`, `tcolorbox`
(`breakable,skins`), `siunitx`, `hyperref`.

### Practice problems collected in the notes
1. Screen analysis of a clay catalyst (Mod 1, Lec. 3)
2. Screen analysis of crushed quartz (Mod 1, Lec. 3)
3. Mixing index in a muller mixer (Mod 1, Lec. 4)
4. Crusher power by Rittinger’s law (Mod 1, Lec. 5)
5. Screen effectiveness of a quartz mixture (Mod 2, Lec. 1) — answers: `D/F` = 0.42, `B/F` = 0.58, `E` ≈ 67 %
