#!/usr/bin/env python3
# =============================================================================
#  sp2-answers-check.py  --  CHE F313 Separation Processes II
#
#  Arithmetic record for the solutions documents. Prints every number that
#  appears in SP2-Problems-and-Solutions.pdf, in the same order.
#  Inputs are the data as printed on the uploaded files; outputs are computed.
#
#  Run:  python3 sp2-answers-check.py
# =============================================================================

import math

SEP = "=" * 78


def head(t):
    print("\n" + SEP + "\n" + t + "\n" + SEP)


def show(label, value, unit=""):
    s = f"{value:,.6g}" if isinstance(value, float) else str(value)
    print(f"  {label:<48s} = {s} {unit}".rstrip())


# =============================================================================
#  SLIDE PROBLEMS  (Q1 - Q5)
# =============================================================================

# ---- Q1 clay catalyst: Mod 1 Lec 3, slide 10 --------------------------------
Q1 = dict(rho_g_per_cm3=1.2, phi_s=0.5,
          increments=[(0.0252, 0.088), (0.0178, 0.178), (0.0126, 0.293),
                      (0.0089, 0.194), (0.0038, 0.247)])


def q1():
    head("Q1  CLAY CATALYST   (Mod 1 Lec 3, slide 10)")
    rho = Q1["rho_g_per_cm3"] / 1000.0
    inc = sorted(Q1["increments"])
    show("sum x_i", sum(x for _, x in inc))
    run = 0.0
    for dp, x in inc:
        run += x
        print(f"    Dpi={dp:7.4f}  x_i={x:6.3f}  cum smaller={run:.4f}"
              f"  cum larger={1 - run:.4f}")
    s1 = sum(x / dp for dp, x in inc)
    s3 = sum(x / dp ** 3 for dp, x in inc)
    show("sum(x_i/Dpi)", s1, "1/mm")
    Aw = 6.0 / (rho * Q1["phi_s"]) * s1
    show("A_w", Aw, "mm2/g"); show("A_w", Aw / 100, "cm2/g")
    Ds = 1.0 / s1
    show("D_s", Ds, "mm"); show("D_s", Ds * 1000, "um")
    show("check 6/(phi_s rho_p A_w)", 6.0 / (Q1["phi_s"] * rho * Aw), "mm")
    show("sum(x_i/Dpi^3)", s3, "1/mm3")
    for a in (math.pi / 6, 0.5, 0.8):
        show(f"N_w with a={a:.4f}", s3 / (a * rho), "particles/g")


# ---- Q2 crushed quartz: Mod 1 Lec 3, slides 11-12 ---------------------------
Q2_TABLE = [("4", 4.699, 0.0000, None), ("6", 3.327, 0.0251, 4.013),
            ("8", 2.362, 0.1250, 2.845), ("10", 1.651, 0.3207, 2.007),
            ("14", 1.168, 0.2570, 1.409), ("20", 0.833, 0.1590, 1.001),
            ("28", 0.589, 0.0538, 0.711), ("35", 0.417, 0.0210, 0.503),
            ("48", 0.295, 0.0102, 0.356), ("65", 0.208, 0.0077, 0.252),
            ("100", 0.147, 0.0058, 0.178), ("150", 0.104, 0.0041, 0.126),
            ("200", 0.074, 0.0031, 0.089), ("Pan", 0.000, 0.0075, 0.037)]
Q2 = dict(rho_g_per_mm3=0.00265, a=0.8, phi_s=0.571)


def q2_block(rows, label):
    rho, a, phi_s = Q2["rho_g_per_mm3"], Q2["a"], Q2["phi_s"]
    print(f"  --- {label}")
    s1 = sum(x / db for _, x, db in rows)
    s3 = sum(x / db ** 3 for _, x, db in rows)
    show("sum x_i", sum(x for _, x, _ in rows))
    show("sum(x_i/Dbar_i)", s1, "1/mm")
    show("sum(x_i/Dbar_i^3)", s3, "1/mm3")
    Aw = 6.0 / (rho * phi_s) * s1
    show("A_w", Aw, "mm2/g"); show("A_w", Aw / 100, "cm2/g")
    Nw = s3 / (a * rho)
    show("N_w", Nw, "particles/g")
    show("D_v", (1.0 / s3) ** (1.0 / 3.0), "mm")
    show("D_s", 1.0 / s1, "mm")
    show("D_w", sum(x * db for _, x, db in rows), "mm")
    Ni = 0.0031 / (a * rho * 0.089 ** 3)
    show("N_i (150/200 increment)", Ni, "particles/g")
    show("N_i / N_T", Ni / Nw)
    print(f"    -> {Ni / Nw * 100:.2f} % of particles; mass fraction 0.31 %")


def q2():
    head("Q2  CRUSHED QUARTZ   (Mod 1 Lec 3, slides 11-12)")
    print("  table check: Dbar_i = (opening of screen above + own opening)/2")
    devs = []
    for i in range(1, len(Q2_TABLE)):
        mesh, op, _, db = Q2_TABLE[i]
        above = Q2_TABLE[i - 1][1]
        calc = (above + op) / 2.0
        devs.append(abs(calc - db))
        print(f"    mesh {mesh:>3s}: ({above:.3f}+{op:.3f})/2 = {calc:.4f}"
              f"   table {db:.3f}   dev {calc - db:+.4f}")
    print(f"    13/13 within 0.0005 mm (max dev {max(devs):.4f} mm)")
    rows_all = [(op, x, db) for _, op, x, db in Q2_TABLE if db is not None]
    q2_block(rows_all[:-1], "4-200 mesh only, pan EXCLUDED (answer)")
    q2_block(rows_all, "all rows incl. Pan (alternative scope)")


# ---- Q3 mixing index: Mod 1 Lec 4, slide 19 --------------------------------
Q3_SAMPLES = [10.24, 9.30, 7.94, 10.24, 11.08, 10.03,
              11.91, 9.72, 9.20, 10.76, 10.97, 10.55]


def q3():
    head("Q3  MIXING INDEX, MULLER MIXER   (Mod 1 Lec 4, slide 19)")
    x = Q3_SAMPLES
    n = len(x)
    mean = sum(x) / n
    ss = sum((v - mean) ** 2 for v in x)
    show("N", n); show("mean xbar", mean, "wt%")
    show("sum (x_i-xbar)^2", ss, "(wt%)^2")
    s1 = math.sqrt(ss / (n - 1))
    s0 = math.sqrt(ss / n)
    show("s (N-1)", s1, "wt%"); show("s (N-1) as fraction", s1 / 100)
    show("s (N)", s0, "wt%"); show("s (N) as fraction", s0 / 100)
    for mu, lab in ((0.10, "mu=0.10 charged"), (mean / 100, "mu=xbar")):
        sig = math.sqrt(mu * (1 - mu))
        show(f"sigma_0, {lab}", sig)
        show(f"I_p, {lab}, N-1", sig / (s1 / 100))
        show(f"I_p, {lab}, N  ", sig / (s0 / 100))


# ---- Q4 Rittinger crusher: Mod 1 Lec 5, slide 20 ---------------------------
def q4():
    head("Q4  CRUSHER POWER, RITTINGER   (Mod 1 Lec 5, slide 20)")
    Pnet1 = 40.0 - 5.0
    spec1 = Pnet1 / 20.0
    g1 = 1 / 10e-4 - 1 / 50e-4
    g2 = 1 / 5e-4 - 1 / 10e-4
    show("net power duty 1", Pnet1, "kW"); show("specific energy duty 1", spec1, "kWh/t")
    show("1/Dsb-1/Dsa duty 1", g1, "1/m"); show("1/Dsb-1/Dsa duty 2", g2, "1/m")
    KR = spec1 / g1
    show("K_R", KR, "kWh.m/t")
    Pnet2 = KR * 12.0 * g2
    show("net power duty 2", Pnet2, "kW")
    show("total power duty 2", Pnet2 + 5.0, "kW")
    show("ratio route", 5.0 + 0.75 * Pnet1, "kW")


# ---- Q5 screen effectiveness: Mod 2 Lec 1, slide 16 ------------------------
def q5():
    head("Q5  SCREEN EFFECTIVENESS   (Mod 2 Lec 1, slide 16)")
    xF, xD, xB = 0.47, 0.85, 0.195
    DF = (xF - xB) / (xD - xB); BF = (xF - xD) / (xB - xD)
    show("D/F", DF); show("B/F", BF); show("D/F+B/F", DF + BF)
    EA = DF * xD / xF; EB = BF * (1 - xB) / (1 - xF)
    show("E_A", EA); show("E_B", EB); show("E = E_A E_B", EA * EB)
    show("E  percent", EA * EB * 100, "%")
    Ebox = (xD / xF) * (xF - xB) / (xD - xB) * (
        1 - (1 - xD) / (1 - xF) * (xF - xB) / (xD - xB))
    show("E  boxed form", Ebox)
    show("oversize balance vs xF", DF * xD + BF * xB)
    show("undersize balance vs 1-xF", DF * (1 - xD) + BF * (1 - xB))


# =============================================================================
#  TUTORIAL / TEST PROBLEMS  (Q6 - Q11)
# =============================================================================

# ---- Q6 Tutorial 3 Problem 1: sieve analysis -------------------------------
T3_SIEVES = [4.00, 3.00, 2.00, 1.50, 1.00, 0.75, 0.50]
T3_MASS = [20, 45, 80, 110, 140, 105, 70, 30]     # last = pan (<0.50 mm)
T3 = dict(rho_kg_m3=2500, phi_s=1.0, a=math.pi / 6)


def q6():
    head("Q6  SIEVE ANALYSIS, CRUSHED SOLID   (Tutorial 3, slide 2)")
    tot = sum(T3_MASS)
    show("total mass", tot, "g")
    ap = T3_SIEVES + [0.0]
    rows = []
    for i, m in enumerate(T3_MASS):
        above = T3_SIEVES[i - 1] if i > 0 else T3_SIEVES[0]   # top: own aperture
        dbar = (above + ap[i]) / 2.0
        rows.append((i + 1, ap[i], above, dbar, m, m / tot))
    print("  no.  aperture  from   Dbar/mm   mass/g    x_i")
    for n, a, b, d, m, x in rows:
        print(f"    {n}   {a:5.2f}   {b:5.2f}   {d:6.3f}   {m:5d}   {x:.4f}")
    show("sum x_i", sum(r[5] for r in rows))

    print("  cumulative percentages (coarsest first):")
    run = 0.0
    for n, a, b, d, m, x in rows:
        run += x
        print(f"    on {a:5.2f} mm : retained cum {run*100:7.3f} %"
              f"   passing {100 - run*100:7.3f} %")

    # D50 by linear interpolation on the passing curve (vs aperture)
    pts = [(rows[0][1], 100 - rows[0][5] * 100)]
    run = 0.0
    for n, a, b, d, m, x in rows:
        run += x
        pts.append((a, 100 - run * 100))
    pts[0] = (rows[0][1], 100.0)          # above the top sieve 100 % passes
    print("   passing vs aperture:", [(f"{a:g}", f"{p:.2f}") for a, p in pts])
    for i in range(len(pts) - 1):
        a1, p1 = pts[i]; a2, p2 = pts[i + 1]
        if p1 >= 50 >= p2:
            D50 = a1 + (50 - p1) * (a2 - a1) / (p2 - p1)
            show(f"D50 between {a1:g} and {a2:g} mm", D50, "mm")
    # log-linear alternative
    for i in range(len(pts) - 1):
        a1, p1 = pts[i]; a2, p2 = pts[i + 1]
        if p1 >= 50 >= p2 and a1 * a2 > 0:
            f = (math.log10(a1) + (50 - p1) / (p2 - p1) * (math.log10(a2) - math.log10(a1)))
            show("D50, log-interpolation (comparison)", 10 ** f, "mm")

    # particle numbers and surface area
    rho = T3["rho_kg_m3"] / 1000.0 / 1000.0     # kg/m3 -> g/mm3
    show("rho_p", rho, "g/mm3")
    print("  particle counts per fraction and totals:")
    NT = 0.0
    for n, a, b, d, m, x in rows:
        Ni = m / (T3["a"] * rho * d ** 3)
        NT += Ni
        print(f"    Dbar={d:6.3f} mm  x_i={x:.4f}  N_i={Ni:14.1f}  "
              f"n_i (per g)={x / (T3['a'] * rho * d ** 3):12.1f}")
    show("total particles in 600 g", NT)
    show("total particles per gram", NT / tot)

    s1 = sum(x / d for _, a, b, d, m, x in rows)
    show("sum(x_i/Dbar_i)", s1, "1/mm")
    Aw = 6.0 / (rho * T3["phi_s"]) * s1
    show("A_w", Aw, "mm2/g"); show("A_w", Aw / 100, "cm2/g")
    show("A_w", Aw * 1e-3, "m2/g")
    Dvs = 1.0 / s1
    show("D_vs (Sauter) = 1/sum(x/D)", Dvs, "mm")


# ---- Q7 Tutorial 3 Problem 2: shape factor & sphericity --------------------
def q7():
    head("Q7  SHAPE FACTOR AND SPHERICITY   (Tutorial 3, slide 3)")
    v, s, Dp = 2.0e-9, 5.5e-6, 1.5e-3
    show("v_p", v, "m3"); show("s_p", s, "m2"); show("D_p", Dp, "m")
    show("a = v_p/D_p^3", v / Dp ** 3)
    Dvs = 6 * v / s
    show("D_vs = 6 v_p/s_p", Dvs, "m"); show("D_vs", Dvs * 1000, "mm")
    show("phi_s = 6v_p/(D_p s_p)", 6 * v / (Dp * s))
    show("phi_s = D_vs/D_p", Dvs / Dp)
    d_eq = (6 * v / math.pi) ** (1 / 3)
    show("equal-volume sphere diameter", d_eq, "m")
    show("sphere area of same volume", math.pi * d_eq ** 2, "m2")
    show("if s_p were 5.5e-5 m2, phi_s", 6 * v / (Dp * 5.5e-5))


# ---- Q8 Tutorial 4 Problem 1: crusher power --------------------------------
def q8():
    head("Q8  CRUSHER POWER, SAME MILL   (Tutorial 4, slide 2)")
    P1, m1, Da1, Db1 = 9.5, 1.2, 20.0, 5.0        # kW, t/h, mm
    m2, Da2, Db2 = 0.1, 20.0, 4.0
    spec1 = P1 / m1
    show("specific energy duty 1", spec1, "kWh/t")
    g1 = 1 / Db1 - 1 / Da1
    g2 = 1 / Db2 - 1 / Da2
    show("1/Db-1/Da duty 1", g1, "1/mm"); show("1/Db-1/Da duty 2", g2, "1/mm")
    KR = spec1 / g1
    show("K_R", KR, "kWh.mm/t")
    show("P2 (Rittinger)", KR * m2 * g2, "kW")
    KK = spec1 / math.log(Da1 / Db1)
    show("K_K (Kick)", KK, "kWh/t")
    show("P2 (Kick, comparison)", KK * math.log(Da2 / Db2) * m2, "kW")


# ---- Q9 Tutorial 4 Problem 2: Kick's law -----------------------------------
def q9():
    head("Q9  ENERGY PER kg, KICK'S LAW   (Tutorial 4, slide 3)")
    KK, Da, Db = 5.0, 10.0, 2.0
    show("ln(Da/Db)", math.log(Da / Db))
    show("E = K_K ln(Da/Db)", KK * math.log(Da / Db), "kJ/kg")


# ---- Q10 Quiz 1: mixing index ----------------------------------------------
def q10():
    head("Q10  MIXING INDEX, BINARY MIXTURE   (Quiz-1, 03/09/2026)")
    masses = [52, 48, 55, 45, 51, 49, 54, 46, 50, 50]
    n = len(masses)
    xi = [m / 100.0 for m in masses]
    show("N", n)
    show("sum x_i", sum(xi)); show("sum x_i^2", sum(v * v for v in xi))
    xbar = sum(xi) / n
    show("xbar", xbar)
    s = math.sqrt((sum(v * v for v in xi) - xbar * sum(xi)) / (n - 1))
    show("s  (slide formula)", s)
    s0 = math.sqrt((sum(v * v for v in xi) - xbar * sum(xi)) / n)
    show("s  (N denominator, comparison)", s0)
    mu = 0.5
    sig0 = math.sqrt(mu * (1 - mu))
    show("sigma_0", sig0)
    show("I_s = sigma_0/s", sig0 / s)
    show("I_s with s rounded to 0.031", sig0 / 0.031)
    npart = 1000
    sig_e = math.sqrt(mu * (1 - mu) / npart)
    show("sigma_e (granular, n=1000)", sig_e)
    show("I_s = sigma_e/s (alternative)", sig_e / s)


# ---- Q11 TT 1: Bond work index ---------------------------------------------
def q11():
    head("Q11  BOND WORK INDEX   (Tutorial Test 1, 07/09/2026)")
    P1, m1, F80, P80 = 320.0, 140.0, 50.0, 2.0      # kW, t/h, mm, mm
    spec1 = P1 / m1
    show("specific energy duty 1", spec1, "kWh/t")
    g1 = 1 / math.sqrt(P80) - 1 / math.sqrt(F80)
    show("1/rootP - 1/rootF (mm^-1/2)", g1)
    Wi = spec1 / (0.3162 * g1)
    show("W_i", Wi, "kWh/t")
    g2 = 1 / math.sqrt(1.6) - 1 / math.sqrt(50)
    show("duty 2 size term", g2)
    E2 = 0.3162 * Wi * g2
    show("E2", E2, "kWh/t")
    show("P2", E2 * 140.0, "kW")


if __name__ == "__main__":
    print("CHE F313  --  arithmetic record for the solutions document")
    for fn in (q1, q2, q3, q4, q5, q6, q7, q8, q9, q10, q11):
        fn()
    print("\n" + SEP + "\ndone.\n" + SEP)
