#!/usr/bin/env python3
"""Reproduces every derived number in KRD-Problems-and-Solutions.tex.

Source files (Slides/): Ch1-krd (1).pdf, Ch2-krd (1).pdf, Ch3-krd.pdf,
Ch4-_Krd.pdf, Ch5_-_krd.pdf, Ch6_krd.pdf, Ch7-_krd.pdf, Catalysis_Krd.pdf,
Non_ideal_KRD.pdf.  Only the method and data printed on the slides are used;
where a slide leaves something undefined the assumption is stated in the
document and repeated here as a comment.
"""
import numpy as np

def simpson(f, x):
    """composite Simpson over possibly uneven segments: uses pairs of equal-h."""
    f = np.asarray(f, float); x = np.asarray(x, float)
    tot = 0.0; i = 0
    while i + 2 < len(x):
        h1, h2 = x[i+1]-x[i], x[i+2]-x[i+1]
        if abs(h1-h2) < 1e-12:
            h = h1
            tot += h/3*(f[i] + 4*f[i+1] + f[i+2]); i += 2
        else:  # fall back to trapezium on the first segment
            tot += 0.5*(f[i]+f[i+1])*h1; i += 1
    if i + 1 < len(x):
        tot += 0.5*(f[i]+f[i+1])*(x[i+1]-x[i])
    return tot

def trap(y, x):
    y = np.asarray(y, float); x = np.asarray(x, float)
    return float(np.sum(0.5*(y[1:]+y[:-1])*(x[1:]-x[:-1])))

def linreg(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    b = np.polyfit(x, y, 1); return b[0], b[1]

def bisect(g, a, b, tol=1e-10):
    fa = g(a)
    for _ in range(200):
        m = 0.5*(a+b); fm = g(m)
        if fa*fm <= 0: b = m
        else: a, fa = m, fm
        if b-a < tol: break
    return 0.5*(a+b)

print("=== Q1 rocket engine (Ch1 slide 36) ===")
V = np.pi/4*0.6**2*0.75
nH2O = 108/18.0        # kmol/s
print(f"V = {V:.4f} m3; -rH2 = {nH2O/V:.0f} kmol/m3.s; -rO2 = {0.5*nH2O/V:.0f} kmol/m3.s")

print("=== Q2 A->B CSTR/PFR/batch (Ch1 slide 54) ===")
FA0, v0, X = 5.0, 10.0, 0.99; CA0 = FA0/v0
k0, k1, k2 = 0.05, 0.0001*3600, 3.0
print(f"a: CSTR {FA0*X/k0:.1f} dm3, PFR {FA0*X/k0:.1f} dm3")
print(f"b: CSTR {v0*X/(k1*(1-X)):.0f} dm3, PFR {v0/k1*np.log(1/(1-X)):.1f} dm3")
print(f"c: CSTR {v0*X/(k2*CA0*(1-X)**2):.0f} dm3, PFR {v0/(k2*CA0)*X/(1-X):.0f} dm3")
print(f"d: batch a {CA0*X/k0:.2f} h, b {np.log(1/(1-X))/k1:.2f} h, c {X/(k2*CA0*(1-X)):.1f} h")

print("=== Q3-Q5 Levenspiel table sizing (Ch2 slides 19-38) ===")
Xg = np.array([0, .1, .2, .4, .6, .7, .8]); g = np.array([.89, 1.08, 1.33, 2.05, 3.54, 5.06, 8.0])
print(f"Q3 CSTR {8.0*0.8:.2f} m3 ; PFR(5-pt Simpson) {0.2/3*(0.89+4*1.33+2*2.05+4*3.54+8.0):.3f} m3")
print(f"Q4 CSTRs 0.4/0.8: {2.05*0.4:.2f} + {8.0*0.4:.2f} = {2.05*0.4+8.0*0.4:.2f} m3")
V1 = 0.2/3*(0.89+4*1.33+2.05); V2 = 0.2/3*(2.05+4*3.54+8.0)
print(f"Q5 PFRs: {V1:.3f} + {V2:.3f} = {V1+V2:.3f} m3")

print("=== Q6 unknown stoichiometry (Ch2 slide 42) ===")
tau = 1.0
rA, rB, rC = (0.02-0.10)/tau, (0.03-0.01)/tau, (0.04-0.0)/tau
print(f"rA={rA}, rB={+rB}, rC={+rC}  -> 4A -> B + 2C")

print("=== Q7 parallel PFR branches (Ch2 slide 46) ===")
# slide 46 prints branch D = 50 L + 30 L = 80 L, branch E = 40 L; equal space
# time per branch => F_D/F = 80/120 (an early draft misread D as 20+30 L)
print(f"fraction to D = 80/120 = {80/120:.3f}")

print("=== Q8 P2-7 (Ch2 slide 59) ===")
Xq = np.array([0, .2, .4, .45, .5, .6, .8, .9]); rA = np.array([1.0, 1.67, 5.0, 5.0, 5.0, 5.0, 1.25, 0.91])
F = 300.0; gq = F/rA
print(f"(a) CSTR {60*0.4:.1f} dm3 ; PFR {simpson(gq[:3], Xq[:3]):.1f} dm3")
GQ = np.concatenate([[0.0], np.array([trap(gq[:i+1], Xq[:i+1]) for i in range(1, len(Xq))])])
def pint(x):  # piecewise-linear (trapezium) integral of gq
    return float(np.interp(x, Xq, GQ))
f_eq = lambda x: x*np.interp(x, Xq, gq) - pint(x)
xb = bisect(f_eq, 0.61, 0.79)
print(f"(b) equal volumes at X ~ {xb:.2f}")
xc = bisect(lambda x: x*np.interp(x, Xq, gq) - 105, 0.6, 0.8)
print(f"(c) 105 dm3 CSTR -> X = {xc:.2f}")
# (d) 72 PFR then 24 CSTR
x1 = bisect(lambda x: pint(x) - 72, 0.3, 0.5)
x2 = bisect(lambda x: (x - x1)*np.interp(x, Xq, gq) - 24, x1, 0.9)
print(f"(d) X1 = {x1:.3f}, X2 = {x2:.3f}")
# (e) 24 CSTR then 72 PFR
y1 = 0.40  # exact root: 0.40*60 = 24 (high-conversion steady state)
# integral 0.4 -> 0.9 is 142.4-71.9 = 70.5 ~ 72: X2 reaches the end of the data
y2 = min(bisect(lambda x: pint(x) - pint(y1) - 72, y1, 0.9), 0.90)
print(f"(e) X1 = {y1:.3f}, X2 = {y2:.3f}")

print("=== Q9/Q10 relative rates (Ch3 slides 5-7) ===")
print("Q9: rNO2=+4 -> rNO = -4, rO2 = -2 mol/m3.s")
print("Q10: rA=-10 -> rB = -15, rC = +25 mol/dm3.s")

print("=== Q13 dimerization MFR (Ch3 slide 62 / Ch5 slide 77) ===")
v0s = np.array([10.0, 3.0, 1.2, 0.5]); CAs = np.array([85.7, 66.7, 50, 33.4]); CA0 = 100.0
Xs = (CA0-CAs)/(CA0-0.5*CAs); r = v0s*CA0*Xs/0.1
n, lk = linreg(np.log(CAs), np.log(r))
print(f"X = {np.round(Xs,4)}; -rA = {np.round(r,1)}; order n = {n:.2f}")
print(f"k per run = {np.round(r/CAs**2,4)} L/(mmol.h)")

print("=== Q14 phosphine PFR (Ch3 slide 63) ===")
T = 649+273.15; P = 460e3; R = 8.314
CA0 = P/(R*T); k = 10.0; FA0 = 40.0; eps = 1.5; X = 0.8
V = FA0/(k*CA0)*((1+eps)*np.log(1/(1-X)) - eps*X)
print(f"CA0 = {CA0:.2f} mol/m3; V = {V:.4f} m3")

print("=== Ch3 milk sterilisation activation energy (Ch3 slide 61, notes 3.5) ===")
# same sterilisation result => same k*t; first order. Deck prints 80C/30min vs
# 74C/15s; hotter must be shorter, so pair 353.15K with 15s, 347.15K with 1800s.
t1, t2 = 1800.0, 15.0; T1, T2 = 347.15, 353.15
E = 8.314*np.log(t1/t2)/(1/T1 - 1/T2)
print(f"E = {E/1000:.0f} kJ/mol")

print("=== Q15 EO batch (Ch4 slides 17-20) ===")
t = np.array([.5, 1, 1.5, 2, 3, 4, 6, 10]); lnCA = np.array([-.157, -.315, -.472, -.629, -.942, -1.255, -1.884, -3.147])
m, c = linreg(t, lnCA)
print(f"slope k = {-m:.3f} min-1 ; t90 = {np.log(10)/-m:.2f} min ; k=1e-4/s -> {np.log(10)/1e-4/3600:.2f} h")

print("=== Q16 EG CSTR (Ch4 slides 29-38) ===")
FA0 = 200e6/62/525600/0.8   # lbmol/min EO
vA0 = FA0/1.0; v0 = 2*vA0; CA0 = 0.5; k = 0.311
V = FA0*X/(k*CA0*(1-X))
print(f"FA0 = {FA0:.3f} lbmol/min; v0 = {v0:.2f} ft3/min; V(80%) = {V:.1f} ft3")
tau_p = 800/7.48/vA0; Da = k*tau_p
print(f"parallel: tau = {tau_p:.2f} min, Da = {Da:.2f}, X = {Da/(1+Da):.3f}")
tau_s = 800/7.48/v0; Das = k*tau_s
print(f"series: tau = {tau_s:.2f} min, Da = {Das:.3f}, X = {1-1/(1+Das)**2:.2f}")

print("=== Q17 ethylene PFR (Ch4 slide 44) ===")
k1000, E, Rcal = 0.072, 82000, 1.987
k = k1000*np.exp(E/Rcal*(1/1000 - 1/1100))
FA0 = 300e6/28/3.1536e7*1000/2.2046  # mol/s  (lb->kg not needed; 1 lbmol=453.6 mol)
FA0 = 300e6/28/3.1536e7*453.6        # mol? no: 300e6 lb/28 lb per lbmol = lbmol/yr -> /3.1536e7 s -> lbmol/s -> *453.6 mol/lbmol
CA0 = 6*101325/(8.314*1100)
v0 = FA0/CA0
V = v0/k*((1+1)*np.log(1/0.2) - 0.8)
print(f"k(1100K) = {k:.3f} 1/s; FA0 = {FA0:.1f} mol/s; CA0 = {CA0:.3f} mol/m3; v0 = {v0:.3f} m3/s; V = {V:.2f} m3 = {V*35.315:.1f} ft3")
print(f"tubes of 0.0205 ft3: {V*35.315/0.0205:.0f}")

print("=== Q18 PBR A+B->2C (Ch4 slides 55-58) ===")
G = 3/100  # back-calculated group kCA0^2/FA0 from X=0.75 (no drop)
W, a = 100, 0.0099
Xd = G*(W - a*W*W/2)
print(f"group = {G}; X(drop) = {Xd/(1+Xd):.4f} (deck 0.6); X(no drop) = {G*W/(1+G*W):.2f}")

print("=== Q19 PBR+CSTR order (Ch4 slide 76) ===")
# first order in pA, pure A, eps=1; current: PBR 50 kg gives X=0.5, P0=20 atm, alpha=0.018/kg


print("=== Q19 PBR+CSTR order (Ch4 slide 76) ===")
def rk4(f, y0, W, h=0.05):
    y = np.array(y0, float)
    n = int(round(W/h))
    for _ in range(n):
        k1 = np.array(f(y)); k2 = np.array(f(y+h/2*k1)); k3 = np.array(f(y+h/2*k2)); k4 = np.array(f(y+h*k3))
        y = y + h/6*(k1+2*k2+2*k3+k4)
    return y
def pbr(X0, p0, a, alpha, W):
    f = lambda y: [a*(1-y[0])/(1+y[0])*y[1], -alpha/(2*y[1]) if y[1] > 1e-9 else 0.0]
    return rk4(f, [X0, p0], W)
a = bisect(lambda a: pbr(0, 1, a, 0.018, 50)[0] - 0.5, 0.001, 0.1)
Xp, pp = pbr(0, 1, a, 0.018, 50)
print(f"group a = {a:.5f}; X = {Xp:.3f}; p exit = {pp:.4f}; P exit = {20*pp:.2f} atm")
X2 = bisect(lambda x: x - Xp - a*(1-x)/(1+x)*pp*50, Xp, 0.999)
Y1 = bisect(lambda x: x - a*(1-x)/(1+x)*50, 0, 0.999)
YX, Yp = pbr(Y1, 1, a, 0.018, 50)
print(f"PBR->CSTR X = {X2:.3f}; CSTR->PBR X = {YX:.3f}")
ad = 0.018*2*(1/1.5**4)
Xd, pd = pbr(0, 1, a, ad, 50)
X2d = bisect(lambda x: x - Xd - a*(1-x)/(1+x)*pd*50, Xd, 0.999)
print(f"(d) alpha' = {ad:.5f}: PBR->CSTR X = {X2d:.3f}")

print("=== Q20 series batch (Ch4 slide 78) ===")
k1, k2, CA0 = 1.0, 2.0, 5.0
tmax = np.log(k2/k1)/(k2-k1)
CBmax = CA0*k1/(k2-k1)*(np.exp(-k1*tmax)-np.exp(-k2*tmax))
print(f"tmax = {tmax:.3f} h; CBmax = {CBmax:.3f}")

print("=== Q22 trityl (Ch5) ===")
t = np.array([0, 50, 100, 150, 200, 250, 300]); CA = np.array([50, 38, 30.6, 25.6, 22.2, 19.5, 17.4])*1e-3
r = np.empty_like(CA)
r[0] = -(-3*CA[0]+4*CA[1]-CA[2])/(2*50)
r[-1] = -(CA[-3]-4*CA[-2]+3*CA[-1])/(2*50)
for i in range(1, 6): r[i] = -(CA[i+1]-CA[i-1])/100
n, _ = linreg(np.log(CA[1:]), np.log(r[1:]))
mk, bk = linreg(t[1:], 1/CA[1:])
print(f"order n = {n:.2f}; integral k' = {mk:.4f}; k = {2*mk:.3f} dm6/mol2.min")

print("=== Q23 DME (Ch5 slide 75) ===")
tp = np.array([390, 777, 1195, 3155]); pi = np.array([408, 488, 562, 799]); pinf = 931
p0 = pinf/3; pA = (pinf-pi)/2
ks = np.log(p0/pA)/tp
print(f"pi0 = {p0:.1f}; k = {np.round(ks,5)}; mean {ks.mean():.2e} 1/s")

print("=== Q24 A<->R (Ch5 slide 72) ===")
ksum = np.log(2)/8; print(f"k1 = {ksum*2/3:.5f}; k2 = {ksum/3:.5f}")

print("=== Q26 L5.19 (Ch5 slide 74) ===")
v0 = np.array([0.06, 0.48, 1.5, 8.1]); CA = np.array([30, 60, 80, 105]); CA0 = 120.0
X = (CA0-CA)/(CA0+2*CA); r = v0*CA0*X
n, _ = linreg(np.log(CA), np.log(r))
print(f"n = {n:.2f}; k = {np.round(r/CA**2,5)} L/(mmol.min)")

print("=== Q27 L3.25 (Ch5 slide 76) ===")
t = np.array([2, 4, 6, 8, 10, 12, 14]); pA = np.array([600, 475, 380, 320, 275, 240, 215]); pAe = 150.0
m, _ = linreg(t, np.log((pA-pAe)/(760-pAe)))
print(f"k = {-m:.4f} 1/min")

print("=== Q29 bomb 2A->B (Ch5 slide 78) ===")
t = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20]); pi = np.array([1.14, 1.04, .982, .94, .905, .87, .85, .832, .815, .8, .754, .728])
pA = 2*pi-1.0
m1, _ = linreg(t, np.log(pA)); m2, _ = linreg(t, 1/pA)
r1 = np.corrcoef(t, np.log(pA))[0,1]**2; r2 = np.corrcoef(t, 1/pA)[0,1]**2
print(f"1st k = {-m1:.4f} r2 = {r1:.5f}; 2nd k = {m2:.4f} r2 = {r2:.5f}")

print("=== Q30/Q31 (Ch5 slides 80-81) ===")
k = np.log(2)/4+np.log(2)/2; print(f"gamble t = {np.log(100)/k:.2f} h")
X6 = bisect(lambda x: x/(1-x)**2-12, 0.5, 0.999); print(f"6x MFR X = {X6:.3f}; PFR X = {2/3:.3f}")

print("=== Q31 A+3B->6R, gas, eps=0.5 (Ch5 slide 82) ===")
# variable volume: CA = CA0(1-X)/(1+eps X), eps = yA0*delta = 0.25*2 = 0.5
XA = (100-40)/(100+0.5*40); XB = 3*100*XA/200; CB = 200*(1-XB)/(1+0.5*XA)
print(f"XA = {XA:.3f}; XB = {XB:.3f}; CB = {CB:.2f}")

print("=== Q32 A+B->5R with T,pi change, eps=1 (Ch5 slide 83) ===")
# CA = CA0(1-X)/(1+eps X) * (T0/T)*(pi/pi0); (1000/400)*(4/5) = 2
X = bisect(lambda x: 100*(1-x)/(1+x)*2.0-20, 0, 1)
XB = X*100/200; CB = 200*(1-XB)/(1+X)*2.0
print(f"XA = {X:.4f}; XB = {XB:.4f}; CB = {CB:.2f}")

print("=== Q34 sucrose MM (Ch5 slide 84) ===")
t = np.arange(1, 12); CA = np.array([.68, .6, .55, .38, .27, .16, .09, .04, .018, .006, .0025]); CA0 = 1.0
lnr = np.log(CA0/CA)
m, b = linreg((CA0-CA)/lnr, t/lnr)
print(f"k3CS0 = {1/m:.4f} 1/h; CM = {b/m:.4f} mmol/L; k3 = {1/m/0.01:.1f} 1/h")

print("=== Q36 product distribution (Ch6 slide 32) ===")
u = lambda c: np.sqrt(c)
a = 2*(u(10)-np.log(1+u(10))) - 2*(u(1)-np.log(2))
c_ = 9 - np.log(11/2)
print(f"(a) CR = {a:.3f}; (b) CR = {0.5*9:.2f}; (c) CR = {c_:.3f}")

print("=== Q37 two MFRs (Ch6 slide 33) ===")
k1 = 0.08/0.16; k2 = 0.16/0.4
CA2 = bisect(lambda c: 0.4 - c - (k1*c*c + k2*c)*10, 0.01, 0.4)
CR2 = 0.2 + k1*CA2*CA2*10; CS2 = 0.7 + k2*CA2*10
print(f"k1 = {k1}, k2 = {k2}; CA2 = {CA2:.4f}; CR2 = {CR2:.4f}; CS2 = {CS2:.4f}")

print("=== Q38 butane adiabatic PFR (Ch7 slides 14-16) ===")
XS = np.linspace(0, 0.7, 141)
T = 330+43.3*XS
k = 31.1*np.exp(7902*(1/360-1/T))
Kc = 3.03*np.exp(830.3*(1/333-1/T))
rA = k*9.3*(1-(1+1/Kc)*XS)
F = 0.9*163
V = trap(F/rA, XS)
print(f"V(70%) = {V:.3f} m3 ; deck-table values: T@0.2 = {330+43.3*0.2:.1f}, -rA@0 = {31.1*np.exp(7902*(1/360-1/330))*9.3:.1f}")

print("=== Q39 interstage cooling (Ch7 slides 48-51) ===")
Xe = lambda T: (lambda K: K/(1+K))(1e5*np.exp(-33.78*(T-298)/T))
T1 = bisect(lambda T: 2.5e-3*(T-300) - 0.95*Xe(T), 300, 600)
X1 = 2.5e-3*(T1-300)
T2 = bisect(lambda T: X1 + 2.5e-3*(T-350) - 0.95*Xe(T), 350, 600)
X2 = X1 + 2.5e-3*(T2-350)
Q1 = 40*50*(T1-350); Q2 = 40*50*(T2-350)
print(f"R1: X = {X1:.3f} @ {T1:.1f} K; R2: X = {X2:.3f} @ {T2:.1f} K; Q1 = {Q1/1000:.1f} kcal/s; Q2 = {Q2/1000:.1f} kcal/s")

print("=== Q40/Q41 PO CSTR (Ch7 slides 57-74) ===")
k = lambda T: 16.96e12*np.exp(-32400/(1.987*T))
tau = (300/7.48)/326.34
Xa = bisect(lambda X: X - k(535+90.1*X)*tau/(1+k(535+90.1*X)*tau), 0.01, 0.99)
Ta = 535+90.1*Xa
print(f"adiabatic: X = {Xa:.3f}, T = {Ta:.1f} R = {Ta-460:.0f} F")
def cool(X):
    T = bisect(lambda T: X*(43.04*36400) - (17379*(T-535) + 4000*(T-545)), 535, 700)
    return T
Xc = bisect(lambda X: X - k(cool(X))*tau/(1+k(cool(X))*tau), 0.01, 0.99)
Tc = cool(Xc)
print(f"with coil: X = {Xc:.4f}, T = {Tc:.2f} R = {Tc-460:.1f} F")

print("=== Q43 pellet (Catalysis slide 48) ===")
phi = 2*np.arccosh(10)
r = 1e-3; d = 3e-4; rr = r-d
ratio = (r/rr)*np.sinh(phi*rr/r)/np.sinh(phi)
eta = lambda p: 3/p**2*(p/np.tanh(p)-1)
p8 = bisect(lambda p: eta(p)-0.8, 0.1, 5)
print(f"phi = {phi:.3f}; CA/CAs = {ratio:.4f}; CA = {0.001*ratio:.2e}; phi(0.8) = {p8:.3f}; d_new = {2e-3*p8/phi:.2e} cm")

print("=== Q44 Mears (Catalysis slide 57) ===")
R = 0.2; De = 0.015
k100 = 0.93; phi1 = R*np.sqrt(k100/De); eta1 = eta(phi1)
r100 = eta1*k100*3.25e-5
k150 = 0.93*np.exp(20000/1.987*(1/373.15-1/423.15))
phi2 = R*np.sqrt(k150/De); eta2 = eta(phi2)
r150 = eta2*k150*3.25e-5
Eapp = 1.987*np.log(r150/r100)/(1/373.15-1/423.15)
print(f"phi100 = {phi1:.3f} eta = {eta1:.4f} r = {r100:.3e}; k150 = {k150:.2f} phi = {phi2:.2f} eta = {eta2:.3f} r = {r150:.3e}; Eapp = {Eapp:.0f} cal/mol")

print("=== Q45 tracer pulse (Non_ideal slide 17) ===")
t = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14]); C = np.array([0, 1, 5, 8, 10, 8, 6, 4, 3, 2.2, 1.5, 0.6, 0])
A1 = simpson(C[:11], t[:11]); A2 = simpson(C[10:], t[10:]); At = A1+A2
tm = trap(t*C, t)/At
sig = trap((t-tm)**2*C, t)/At
frac = simpson(C[3:7], t[3:7])/At
print(f"area = {At:.2f}; tm = {tm:.2f}; sigma2 = {sig:.2f}; frac(3-6) = {frac:.3f}")

print("=== Q46 dispersion (Non_ideal slides 52-59) ===")
tm = 5.13; s2 = 5.92; k = 0.25
s2t = s2/tm**2
Pe = bisect(lambda p: 2/p - 2/p**2*(1-np.exp(-p)) - s2t, 1, 50)
Da = k*tm
q = np.sqrt(1+4*Da/Pe)
X = 1 - 4*q*np.exp(Pe/2)/((1+q)**2*np.exp(Pe*q/2)-(1-q)**2*np.exp(-Pe*q/2))
n = tm**2/s2
XT = 1-1/(1+Da/n)**n
print(f"Pe = {Pe:.2f}; Da = {Da:.2f}; X disp = {X:.3f}; X PFR = {1-np.exp(-Da):.2f}; X CSTR = {Da/(1+Da):.2f}; n = {n:.2f}; X TIS = {XT:.3f}")

print("=== Q35 reversible PFR (Ch5 slide 61; rate law from the textbook original) ===")
k1, k2, CA0 = 0.04, 0.01, 0.1
Xe = k1/(k1+k2)*1.0/(1)  # 0.04CA=0.01CR -> CR=4CA -> Xe
Xe = 4/5
tau = 2000/100
CAf = 0.02 + (CA0-0.02)*np.exp(-(k1+k2)*tau)
print(f"Xe = {Xe:.2f}; tau = {tau} min; CAf = {CAf:.4f}; X = {1-CAf/CA0:.3f}")

print("=== Q21 PFR pressure drop lengths (Ch4 slides 90-98) ===")
kv = 0.1/15.9155
print(f"no-drop L(10%) = {np.log(1/0.9)/kv:.1f} m; L(20%) = {np.log(1/0.8)/kv:.1f} m (deck: ~20 m with drop; 20% impossible in 1.5 cm)")

print("=== Q42 parallel rxns PFR heat effects (Ch7 slide 95): ODE setup ===")
def rhs(y):
    Fa, Fc, T = y
    Ft = Fa + Fc + (100 - Fa)  # B formed
    CA = Fa/60000.0
    k1 = 10*np.exp(4000*(1/423.15-1/T)); k2 = 0.09*np.exp(9000*(1/423.15-1/T))
    r1 = k1*CA; r2 = k2*CA*CA
    dFa = -r1 - 2*r2
    dFc = r2
    Cpsum = Fa*90 + (100-Fa)*90 + Fc*180
    dT = (r1*20000 + r2*60000)/Cpsum
    return [dFa, dFc, dT]
y = rk4(rhs, [100.0, 0.0, 423.15], 10000, h=10)
print(f"at V = 1e4 dm3: FA = {y[0]:.1f}, FC = {y[1]:.1f}, T = {y[2]:.0f} K")

print("=== Ch6 three-reaction selectivity reduction (Ch6 slides 18-19) ===")
# r_D = 0.0002 e^{36000(1/300-1/T)} C_A ; r_U = 0.0018 e^{25000(1/300-1/T)} C_A^1.5 ;
# r_Q = 0.00452 e^{5000(1/300-1/T)} C_A^0.5  ->  S_DU = r_D/r_U, S_DQ = r_D/r_Q
coef = 0.0002/0.0018; dE = 36000-25000; a = 1-1.5
print(f"S_DU = {coef:.2f} e^({dE}(1/300-1/T)) C_A^({a})   (deck prints 0.11 e^(11,000(1/300-1/T))/C_A^0.5)")
print(f"S_DQ: prefactor {0.0002/0.00452:.4f}, E-gap {36000-5000} -> very large at high T; order gap {1-0.5}")

print("=== Ch7 A<->B adiabatic equilibrium intersection (Ch7 slides 47-48) ===")
# X_EB = 50(T-300)/20000 = 2.5e-3(T-300); Kc = 1e5 exp(-33.78 (T-298)/T); Xe = Kc/(1+Kc)
slope = 50/20000; coef = 20000/1.987/298
print(f"X_EB slope = {slope:.1e} (deck 2.5e-3); van't Hoff coef = {coef:.2f} (deck 33.78)")
for Tt in [350, 400, 425, 450, 475, 500]:
    K = 1e5*np.exp(-coef*(Tt-298)/Tt)
    print(f"  Kc({Tt}) = {K:.2f}, Xe = {K/(1+K):.2f}")
f = lambda T: 1e5*np.exp(-coef*(T-298)/T)/(1+1e5*np.exp(-coef*(T-298)/T)) - slope*(T-300)
lo, hi = 300.0, 600.0
for _ in range(100):
    m = 0.5*(lo+hi)
    if f(lo)*f(m) <= 0: hi = m
    else: lo = m
T = 0.5*(lo+hi)
print(f"exact intersection X = {slope*(T-300):.3f} at T = {T:.1f} K (deck graphic: 0.42 at 465 K)")
