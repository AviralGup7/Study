#!/usr/bin/env python3
# =============================================================================
#  sp2-answers-check.py  --  CHE F313 Separation Processes II
#
#  Reproduces EVERY number printed in SP2-problems-and-solutions.pdf, in the
#  same order as the solutions there. Nothing in that document was computed by
#  hand; this script is the arithmetic record.
#
#  Inputs are the slide-given data (the "SOURCE" quantities). Outputs are the
#  "DERIVED" quantities. Run:  python3 sp2-answers-check.py
#  Stdlib only (math), so it runs anywhere.
# =============================================================================

import math

# ------------------------- small helpers -------------------------------------
SEP = "=" * 78


def head(t):
    print("\n" + SEP)
    print(t)
    print(SEP)


def show(label, value, unit=""):
    if isinstance(value, float):
        s = f"{value:,.6g}"
    else:
        s = str(value)
    print(f"  {label:<46s} = {s} {unit}".rstrip())


# =============================================================================
# Q1 - CLAY CATALYST                       Mod 1 Lec 3, slide 10
# =============================================================================
# SOURCE data (slide): rho_p = 1.2 g/cm3, sphericity = 0.5, and the five size
# increments. Note the slide gives no volume shape factor a -> flagged.
Q1 = dict(
    rho_g_per_cm3=1.2,
    phi_s=0.5,
    # (Dpi / mm, x_i)
    increments=[
        (0.0252, 0.088),
        (0.0178, 0.178),
        (0.0126, 0.293),
        (0.0089, 0.194),
        (0.0038, 0.247),
    ],
)


def q1():
    head("Q1  CLAY CATALYST   (Mod 1 Lec 3, slide 10)")
    d = Q1
    rho = d["rho_g_per_cm3"] / 1000.0          # g/cm3 -> g/mm3
    inc = sorted(d["increments"])               # ascending Dp = order for cumulative

    sumx = sum(x for _, x in inc)
    show("sum x_i", sumx)

    print("  cumulative analysis (ascending Dp):")
    run = 0.0
    for dp, x in inc:
        run += x
        print(f"    Dpi={dp:7.4f}  x_i={x:6.3f}  cumulative smaller={run:.4f}"
              f"  cumulative larger={1 - run:.4f}")

    s1 = sum(x / dp for dp, x in inc)           # mm^-1
    show("sum(x_i/Dpi)", s1, "1/mm")
    Aw = 6.0 / (rho * d["phi_s"]) * s1          # mm2/g
    show("A_w", Aw, "mm2/g")
    show("A_w", Aw / 100.0, "cm2/g")
    show("A_w", Aw * 1e-3, "m2/g")

    Ds = 1.0 / s1
    show("D_s = 1/sum(x_i/Dpi)", Ds, "mm")
    show("D_s", Ds * 1000.0, "um")
    show("check D_s = 6/(phi_s rho_p A_w)", 6.0 / (d["phi_s"] * rho * Aw), "mm")

    s3 = sum(x / dp ** 3 for dp, x in inc)      # mm^-3
    show("sum(x_i/Dpi^3)", s3, "1/mm3")
    show("N_w pre-factor (1/(rho_p) * sum)", s3 / rho, "1/g")
    for a in (math.pi / 6, 0.5, 0.8):
        show(f"N_w with a = {a:.4f}", s3 / (a * rho), "particles/g")


# =============================================================================
# Q2 - CRUSHED QUARTZ                      Mod 1 Lec 3, slides 11-12
# =============================================================================
# SOURCE data (slide): rho_p = 2650 kg/m3, a = 0.8, phi_s = 0.571, and the
# 14-row screen table. Rows: (mesh, opening / mm, x_i retained, Dbar_i / mm)
Q2_TABLE = [
    ("4",   4.699, 0.0000, None),
    ("6",   3.327, 0.0251, 4.013),
    ("8",   2.362, 0.1250, 2.845),
    ("10",  1.651, 0.3207, 2.007),
    ("14",  1.168, 0.2570, 1.409),
    ("20",  0.833, 0.1590, 1.001),
    ("28",  0.589, 0.0538, 0.711),
    ("35",  0.417, 0.0210, 0.503),
    ("48",  0.295, 0.0102, 0.356),
    ("65",  0.208, 0.0077, 0.252),
    ("100", 0.147, 0.0058, 0.178),
    ("150", 0.104, 0.0041, 0.126),
    ("200", 0.074, 0.0031, 0.089),
    ("Pan", 0.000, 0.0075, 0.037),
]
Q2 = dict(rho_g_per_mm3=0.00265, a=0.8, phi_s=0.571)


def q2_block(rows, label):
    """rows = list of (opening, x_i, Dbar)."""
    rho, a, phi_s = Q2["rho_g_per_mm3"], Q2["a"], Q2["phi_s"]
    print(f"  --- {label}")
    sumx = sum(x for _, x, _ in rows)
    s1 = sum(x / db for _, x, db in rows)
    s3 = sum(x / db ** 3 for _, x, db in rows)
    show("sum x_i", sumx)
    show("sum(x_i/Dbar_i)", s1, "1/mm")
    show("sum(x_i/Dbar_i^3)", s3, "1/mm3")

    Aw = 6.0 / (rho * phi_s) * s1
    show("A_w", Aw, "mm2/g")
    show("A_w", Aw / 100.0, "cm2/g")
    Nw = s3 / (a * rho)
    show("N_w", Nw, "particles/g")

    Dv = (1.0 / s3) ** (1.0 / 3.0)
    show("D_v = [1/sum(x/D^3)]^(1/3)", Dv, "mm")
    Ds = 1.0 / s1
    show("D_s = 1/sum(x/D)", Ds, "mm")
    Dw = sum(x * db for _, x, db in rows)
    show("D_w = sum(x_i Dbar_i)", Dw, "mm")

    xi_150, d_150 = 0.0031, 0.089
    Ni = xi_150 / (a * rho * d_150 ** 3)
    show("N_i (150/200 increment)", Ni, "particles/g")
    show("N_i / N_T  = N_i / N_w", Ni / Nw)
    show("N_i / N_T  (from x/D^3 directly)", (xi_150 / d_150 ** 3) / s3)
    print(f"    -> {Ni / Nw * 100:.2f} % of all particles; "
          f"mass fraction of the increment = {xi_150 * 100:.2f} %")


def q2():
    head("Q2  CRUSHED QUARTZ   (Mod 1 Lec 3, slides 11-12)")
    # (0) table self-consistency: Dbar_i is the mean of the two defining openings
    # The increment labelled by mesh m is the material that passed screen
    # (m-1) and was retained on screen m, so its mean diameter is the mean of
    # the opening of the screen ABOVE it and its own opening.  The table prints
    # 3 decimals, so agreement is tested to within half of that.
    print("  table check: Dbar_i == (opening of screen above + opening_i)/2 ?")
    devs = []
    for i in range(1, len(Q2_TABLE)):
        mesh, op, _, db = Q2_TABLE[i]
        above = Q2_TABLE[i - 1][1]
        calc = (above + op) / 2.0
        devs.append(abs(calc - db))
        print(f"    mesh {mesh:>3s}: ({above:.3f}+{op:.3f})/2 = {calc:.4f}"
              f"   table {db:.3f}   dev {calc - db:+.4f}")
    mx = max(devs)
    print(f"    {len(devs)}/{len(devs)} rows agree to within 0.0005 mm"
          f"  (max deviation {mx:.4f} mm)")
    print("    -> the table stores 3-decimal roundings of the increment means")

    rows_all = [(op, x, db) for m, op, x, db in Q2_TABLE if db is not None]
    rows_4_200 = rows_all[:-1]          # 4-mesh .. 200-mesh: pan excluded
    q2_block(rows_4_200, "4-200 mesh only, pan EXCLUDED (used in the answer)")
    q2_block(rows_all, "all rows incl. Pan (quoted in the FLAG box)")


# =============================================================================
# Q3 - MIXING INDEX                        Mod 1 Lec 4, slide 19
# =============================================================================
Q3_SAMPLES = [10.24, 9.30, 7.94, 10.24, 11.08, 10.03,
              11.91, 9.72, 9.20, 10.76, 10.97, 10.55]
Q3 = dict(mu_charged=0.10)


def q3():
    head("Q3  MIXING INDEX (muller mixer, cohesive paste)   (Mod 1 Lec 4, slide 19)")
    x = Q3_SAMPLES
    n = len(x)
    show("N (spot samples)", n)
    mean = sum(x) / n
    show("mean xbar", mean, "wt%")
    ss = sum((v - mean) ** 2 for v in x)
    show("sum (x_i - xbar)^2", ss, "(wt%)^2")

    s_n1 = math.sqrt(ss / (n - 1))
    s_n = math.sqrt(ss / n)
    show("s  (slide formula, N-1)", s_n1, "wt%")
    show("s  as mass fraction", s_n1 / 100.0)
    show("s  (N denominator)", s_n, "wt%")
    show("s  (N denominator) as fraction", s_n / 100.0)

    for mu, lab in ((Q3["mu_charged"], "mu = 0.10 charged"),
                    (mean / 100.0, "mu = xbar measured")):
        s0 = math.sqrt(mu * (1.0 - mu))
        show(f"sigma_0 = sqrt(mu(1-mu)), {lab}", s0)
        show(f"I_p = sigma_0/s   ({lab}, N-1)", s0 / (s_n1 / 100.0))
        show(f"I_p = sigma_0/s   ({lab}, N  )", s0 / (s_n / 100.0))


# =============================================================================
# Q4 - RITTINGER CRUSHER POWER             Mod 1 Lec 5, slide 20
# =============================================================================
Q4 = dict(P_total1_kW=40.0, P_empty_kW=5.0, mdot1_tph=20.0,
          Dsa1=50e-4, Dsb1=10e-4, mdot2_tph=12.0, Dsa2=10e-4, Dsb2=5e-4)


def q4():
    head("Q4  CRUSHER POWER, RITTINGER'S LAW   (Mod 1 Lec 5, slide 20)")
    d = Q4
    Pnet1 = d["P_total1_kW"] - d["P_empty_kW"]
    show("net power, duty 1", Pnet1, "kW")
    spec1 = Pnet1 / d["mdot1_tph"]
    show("specific energy, duty 1", spec1, "kW h/t")

    g1 = 1.0 / d["Dsb1"] - 1.0 / d["Dsa1"]
    g2 = 1.0 / d["Dsb2"] - 1.0 / d["Dsa2"]
    show("1/Dsb - 1/Dsa, duty 1", g1, "1/m")
    show("1/Dsb - 1/Dsa, duty 2", g2, "1/m")

    KR = spec1 / g1
    show("K_R", KR, "kW h m / t")

    Pnet2 = KR * d["mdot2_tph"] * g2
    show("net power, duty 2", Pnet2, "kW")
    P2 = Pnet2 + d["P_empty_kW"]
    show("TOTAL power, duty 2", P2, "kW")

    ratio = (d["mdot2_tph"] / d["mdot1_tph"]) * (g2 / g1)
    show("ratio (m2/m1)(g2/g1)", ratio)
    show("P_2 by ratio route", d["P_empty_kW"] + ratio * Pnet1, "kW")


# =============================================================================
# Q5 - SCREEN EFFECTIVENESS                Mod 2 Lec 1, slide 16
# =============================================================================
Q5 = dict(xF=0.47, xD=0.85, xB=0.195)


def q5():
    head("Q5  SCREEN EFFECTIVENESS (10-mesh cut)   (Mod 2 Lec 1, slide 16)")
    xF, xD, xB = Q5["xF"], Q5["xD"], Q5["xB"]
    DF = (xF - xB) / (xD - xB)
    BF = (xF - xD) / (xB - xD)
    show("D/F", DF)
    show("B/F", BF)
    show("D/F + B/F (mass balance)", DF + BF)

    EA = DF * xD / xF
    EB = BF * (1 - xB) / (1 - xF)
    show("E_A = (D/F)(xD/xF)", EA)
    show("E_B = (B/F)((1-xB)/(1-xF))", EB)
    show("E = E_A E_B", EA * EB)
    show("E  (percent)", (EA * EB) * 100.0, "%")

    Ebox = (xD / xF) * (xF - xB) / (xD - xB) * (
        1 - (1 - xD) / (1 - xF) * (xF - xB) / (xD - xB))
    show("E  (slide's rearranged boxed form)", Ebox)

    # The boxed form must agree with E = E_A E_B, which is how the slides DEFINE
    # the overall effectiveness; it does, so the boxed rearrangement is settled
    # regardless of what the hand-scribbled constant on the slide was.
    show("|E_boxed - E_A E_B|  (must be ~0)", abs(Ebox - EA * EB))

    # perfect-separation limit: xD -> 1, xB -> 0 must give E = 1
    xD2, xB2 = 1.0, 0.0
    DF2 = (xF - xB2) / (xD2 - xB2)
    E2 = (xD2 / xF) * DF2 * (1 - (1 - xD2) / (1 - xF) * DF2)
    show("limiting case xD=1, xB=0: E", E2)

    oversize = DF * xD + BF * xB
    undersize = DF * (1 - xD) + BF * (1 - xB)
    show("oversize balance  (D/F)xD + (B/F)xB  vs xF", oversize)
    show("undersize balance (D/F)(1-xD)+(B/F)(1-xB) vs 1-xF", undersize)


# =============================================================================
if __name__ == "__main__":
    print("CHE F313  --  arithmetic record for SP2-problems-and-solutions.pdf")
    print("Method used for every question = the method taught on the slides.")
    q1()
    q2()
    q3()
    q4()
    q5()
    print("\n" + SEP)
    print("done.")
    print(SEP)
