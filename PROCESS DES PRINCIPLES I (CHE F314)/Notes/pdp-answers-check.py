#!/usr/bin/env python3
# =============================================================================
#  pdp-answers-check.py  --  CHE F314 Process Design Principles I
#
#  Arithmetic record for PDP-Problems-and-Solutions.pdf
#  (problems taken from the uploaded lecture decks L-1, L-2, L-4, EDM).
#  Run:  python3 pdp-answers-check.py
# =============================================================================

import math

SEP = "=" * 78


def head(t):
    print("\n" + SEP + "\n" + t + "\n" + SEP)


def show(label, value, unit=""):
    s = f"{value:,.6g}" if isinstance(value, float) else str(value)
    print(f"  {label:<50s} = {s} {unit}".rstrip())


# =============================================================================
# P1  Approach-temperature heuristic   (EDM.pdf, slides 94-95)
# =============================================================================
P1 = dict(F=51000.0, Cp=1.0, Uc=30.0, Us=20.0, CA=11.38,
          Cw=0.07388, Cs=21.22, dHs=933.7, Ts=267.0, Tin=366.0,
          Tcw_in=90.0, Tcw_out=120.0, Tout=100.0)


def areas_and_tac(T1):
    d = P1
    F, Cp = d["F"], d["Cp"]
    # steam generator: waste 366 -> T1, steam at Ts (isothermal on the cold side)
    Qs = F * Cp * (d["Tin"] - T1)
    dtm_s = (d["Tin"] - T1) / math.log((d["Tin"] - d["Ts"]) / (T1 - d["Ts"]))
    As = Qs / (d["Us"] * dtm_s)
    Ws = Qs / d["dHs"]                       # lb/h of steam
    # cooler: waste T1 -> 100, water 90 -> 120
    Qc = F * Cp * (T1 - d["Tout"])
    dtm_c = ((T1 - d["Tcw_out"]) - (d["Tout"] - d["Tcw_in"])) / math.log(
        (T1 - d["Tcw_out"]) / (d["Tout"] - d["Tcw_in"]))
    Ac = Qc / (d["Uc"] * dtm_c)
    Wc = Qc / (Cp * (d["Tcw_out"] - d["Tcw_in"]))
    tac = d["CA"] * (As + Ac) + d["Cw"] * Wc - d["Cs"] * Ws
    return dict(As=As, Ac=Ac, Qs=Qs, Qc=Qc, Ws=Ws, Wc=Wc,
                area_cost=d["CA"] * (As + Ac), cw_cost=d["Cw"] * Wc,
                steam_credit=d["Cs"] * Ws, tac=tac,
                dt_s=T1 - d["Ts"], dt_c=T1 - d["Tcw_out"])


def p1():
    head("P1  HEAT-EXCHANGER APPROACH TEMPERATURE   (EDM.pdf, slides 94-95)")
    d = P1
    FF = d["F"] * d["Cp"]
    show("F Cp", FF, "Btu/h.F")
    show("heat available above 100 F", d["F"] * d["Cp"] * (d["Tin"] - d["Tout"]), "Btu/h")
    show("steam that could be raised", d["F"] * d["Cp"] * (d["Tin"] - d["Tout"]) / d["dHs"], "lb/h")

    print("  T1 / F   dt_s / F   dt_c / F    A_s/ft2    A_c/ft2"
          "     TAC/$/yr")
    for T1 in (277, 280, 285, 290, 295, 300, 310, 320, 340, 360):
        r = areas_and_tac(T1)
        print(f"   {T1:4.0f}   {r['dt_s']:7.1f}   {r['dt_c']:7.1f}"
              f"   {r['As']:9.0f}  {r['Ac']:9.0f}   {r['tac']:12,.0f}")

    best = None
    T = 277.0
    while T <= 365.0:          # stop short of T1 = Tin (zero log mean difference)
        r = areas_and_tac(T)
        if best is None or r["tac"] < best[1]["tac"]:
            best = (T, r)
        T += 0.25
    T1o, ro = best
    head("P1  optimum")
    show("T1 optimum", T1o, "F")
    show("approach at steam-generator cold end", T1o - d["Ts"], "F")
    show("approach at cooler hot end", T1o - d["Tcw_out"], "F")
    for k in ("As", "Ac", "area_cost", "cw_cost", "steam_credit", "tac"):
        show(k, ro[k])
    r10 = areas_and_tac(277.0)
    show("TAC at the 10 F rule of thumb", r10["tac"], "$/yr")
    show("penalty vs optimum", (r10["tac"] / ro["tac"] - 1) * 100, "%")
    print("  range of T1 within 5 % of the optimum TAC:")
    lo = hi = None
    T = 277.0
    while T <= 365.0:
        r = areas_and_tac(T)
        if r["tac"] <= 1.05 * ro["tac"]:
            lo = T if lo is None else lo
            hi = T
        T += 0.25
    show("  T1 lower bound", lo, "F")
    show("  T1 upper bound", hi, "F")
    show("  approach lower bound", lo - d["Ts"], "F")
    show("  approach upper bound", hi - d["Ts"], "F")


# =============================================================================
# P2  Back-of-envelope trays vs Fenske   (EDM.pdf, slide 96)
# =============================================================================
def p2():
    head("P2  MINIMUM TRAYS: BACK-OF-ENVELOPE vs FENSKE   (EDM.pdf, slide 96)")
    # Fenske:  N = ln S / ln alpha,  S = separation factor
    # Clausius-Clapeyron (equal latent heats):  ln alpha = (lambda/R)(T1-T2)/(T1 T2)
    # Back of envelope: N = (T1+T2) / (3 (T1-T2))
    for split in (0.99, 0.999):
        S = (split / (1 - split)) ** 2
        show(f"separation factor S for {split*100:g} % split", S)
        show("ln S", math.log(S))
    lnS = math.log((0.99 / 0.01) ** 2)
    show("ln S used below (99 % split)", lnS)

    # consistency: (lambda/R) required for the two to agree exactly
    for (T1, T2, name) in ((383.78, 353.25, "toluene / benzene (K)"),):
        tavg = (T1 + T2) / 2
        lam_R = 1.5 * lnS * tavg
        show(f"({name}) T_avg", tavg, "K")
        show("(lambda/R) that makes the two equal", lam_R, "K")
        show("  i.e. lambda", lam_R * 8.314 / 1000, "kJ/mol")
        show("  i.e. lambda", lam_R * 1.987 / 1000, "kcal/mol")
        Nheu = (T1 + T2) / (3 * (T1 - T2))
        show("back-of-envelope N", Nheu, "trays")
        for lam in (lam_R, 3800.0):
            lna = lam * (T1 - T2) / (T1 * T2)
            show(f"  ln alpha with lambda/R={lam:.0f}", lna)
            show("  alpha", math.exp(lna))
            show("  Fenske N", lnS / lna, "trays")
        print("  check: same rule in degrees Rankine (absolute) gives the same N")

        T1R, T2R = T1 * 1.8, T2 * 1.8
        show("  back-of-envelope N, Rankine", (T1R + T2R) / (3 * (T1R - T2R)), "trays")

    # where the heuristic crosses a design split
    print("  implied separation if lambda/R = 5000 K (lambda = 10 kcal/mol):")
    T1, T2 = 383.78, 353.25
    lna = 5000.0 * (T1 - T2) / (T1 * T2)
    Nheu = (T1 + T2) / (3 * (T1 - T2))
    show("  ln S implied", lna * Nheu)
    show("  S implied", math.exp(lna * Nheu))
    show("  split implied (each component)", math.sqrt(math.exp(lna * Nheu)) / (
        1 + math.sqrt(math.exp(lna * Nheu))))


if __name__ == "__main__":
    print("CHE F314  --  arithmetic record for the PDP solutions document")
    p1()
    p2()
    print("\n" + SEP + "\ndone.\n" + SEP)
