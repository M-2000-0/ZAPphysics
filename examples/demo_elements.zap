# ═══════════════════════════════════════════════════════════════════
# Demo: Periodic Table — All 118 elements
# Run: zap run main.zap
# ═══════════════════════════════════════════════════════════════════

say("")
say("=== DEMO: Periodic Table (118 Elements) ===")

say("")
say("-- Period 1 --")
say("  " + str(H) + "  " + str(He))

say("")
say("-- Period 2 --")
say("  " + str(Li) + "  " + str(Be) + "  " + str(B) + "  " + str(C) + "  " + str(N) + "  " + str(O) + "  " + str(F) + "  " + str(Ne))

say("")
say("-- Period 3 --")
say("  " + str(Na) + "  " + str(Mg) + "  " + str(Al) + "  " + str(Si) + "  " + str(P) + "  " + str(S) + "  " + str(Cl) + "  " + str(Ar))

say("")
say("-- Period 4 --")
say("  " + str(K) + "  " + str(Ca) + "  " + str(Sc) + "  " + str(Ti) + "  " + str(V) + "  " + str(Cr) + "  " + str(Mn) + "  " + str(Fe))
say("  " + str(Co) + "  " + str(Ni) + "  " + str(Cu) + "  " + str(Zn) + "  " + str(Ga) + "  " + str(Ge) + "  " + str(As) + "  " + str(Se))
say("  " + str(Br) + "  " + str(Kr))

say("")
say("-- Period 5 --")
say("  " + str(Rb) + "  " + str(Sr) + "  " + str(Y) + "  " + str(Zr) + "  " + str(Nb) + "  " + str(Mo) + "  " + str(Tc) + "  " + str(Ru))
say("  " + str(Rh) + "  " + str(Pd) + "  " + str(Ag) + "  " + str(Cd) + "  " + str(In) + "  " + str(Sn) + "  " + str(Sb) + "  " + str(Te))
say("  " + str(I) + "  " + str(Xe))

say("")
say("-- Period 6 --")
say("  " + str(Cs) + "  " + str(Ba) + "  " + str(La) + "  " + str(Ce) + "  " + str(Pr) + "  " + str(Nd) + "  " + str(Pm) + "  " + str(Sm))
say("  " + str(Eu) + "  " + str(Gd) + "  " + str(Tb) + "  " + str(Dy) + "  " + str(Ho) + "  " + str(Er) + "  " + str(Tm) + "  " + str(Yb))
say("  " + str(Lu) + "  " + str(Hf) + "  " + str(Ta) + "  " + str(W) + "  " + str(Re) + "  " + str(Os) + "  " + str(Ir) + "  " + str(Pt))
say("  " + str(Au) + "  " + str(Hg) + "  " + str(Tl) + "  " + str(Pb) + "  " + str(Bi) + "  " + str(Po) + "  " + str(At) + "  " + str(Rn))

say("")
say("-- Period 7 --")
say("  " + str(Fr) + "  " + str(Ra) + "  " + str(Ac) + "  " + str(Th) + "  " + str(Pa) + "  " + str(U) + "  " + str(Np) + "  " + str(Pu))
say("  " + str(Am) + "  " + str(Cm) + "  " + str(Bk) + "  " + str(Cf) + "  " + str(Es) + "  " + str(Fm) + "  " + str(Md) + "  " + str(No))
say("  " + str(Lr) + "  " + str(Rf) + "  " + str(Db) + "  " + str(Sg) + "  " + str(Bh) + "  " + str(Hs) + "  " + str(Mt) + "  " + str(Ds))
say("  " + str(Rg) + "  " + str(Cn) + "  " + str(Nh) + "  " + str(Fl) + "  " + str(Mc) + "  " + str(Lv) + "  " + str(Ts) + "  " + str(Og))

say("")
say("-- Element Properties Check --")
say("  Gold (Au): mass=" + str(Au.mass) + "  EN=" + str(Au.electronegativity) + "  valence=" + str(Au.valence))
say("  Iron (Fe): mass=" + str(Fe.mass) + "  EN=" + str(Fe.electronegativity) + "  valence=" + str(Fe.valence))
say("  Uranium (U): mass=" + str(U.mass) + "  EN=" + str(U.electronegativity) + "  valence=" + str(U.valence))
say("  Oganesson (Og): mass=" + str(Og.mass) + "  EN=" + str(Og.electronegativity) + "  valence=" + str(Og.valence))
say("  Total: 118 elements loaded!")
