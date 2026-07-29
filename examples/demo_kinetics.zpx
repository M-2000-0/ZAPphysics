# ═══════════════════════════════════════════════════════════════════
# Demo: Reaction Kinetics — Rate equations & equilibrium
# Run: zap run main.zap
# ═══════════════════════════════════════════════════════════════════

say("")
say("=== DEMO: Reaction Kinetics ===")

say("")
say("-- Rate Laws --")
let k = 0.05
let conc = [1.0, 2.0]
let orders = [1, 0]
let rate = rate_law(k, conc, orders)
say("  rate = k * [A]^1 * [B]^0")
say("  k=0.05, [A]=1.0, [B]=2.0")
say("  rate = " + str(round(rate, 4)) + " M/s")

say("")
say("-- Integrated Rate Laws --")
let a0 = 1.0
say("  [A]0 = " + str(a0) + " M")
say("")
say("  Zero order (k=0.1):")
for t in [0, 2, 4, 6, 8, 10]:
  say("    t=" + str(t) + "s  [A]=" + str(round(integrated_zero_order(a0, 0.1, t), 4)) + " M")
say("    half-life: " + str(round(half_life_zero(a0, 0.1), 1)) + " s")

say("")
say("  First order (k=0.2):")
for t in [0, 2, 4, 6, 8, 10]:
  say("    t=" + str(t) + "s  [A]=" + str(round(integrated_first_order(a0, 0.2, t), 4)) + " M")
say("    half-life: " + str(round(half_life_first(0.2), 2)) + " s")

say("")
say("  Second order (k=0.3):")
for t in [0, 2, 4, 6, 8, 10]:
  say("    t=" + str(t) + "s  [A]=" + str(round(integrated_second_order(a0, 0.3, t), 4)) + " M")
say("    half-life: " + str(round(half_life_second(a0, 0.3), 2)) + " s")

say("")
say("-- Equilibrium --")
let K = equilibrium_constant([0.5, 0.3], [1.0, 0.2])
say("  Kc = [C][D] / [A][B] = (0.5*0.3) / (1.0*0.2) = " + str(round(K, 4)))

let T = 298.15
let dG = gibbs_from_equilibrium(K, T)
say("  dG = -RT*ln(K) = " + str(round(dG, 2)) + " J/mol")

say("")
say("-- Van't Hoff Equation --")
let K2 = vant_hoff(K, 298.15, 350.15, -89040)
say("  K at 298K: " + str(round(K, 4)))
say("  K at 350K: " + str(round(K2, 4)))

say("")
say("-- Michaelis-Menten Kinetics --")
let Vmax = 10.0
let Km = 2.0
say("  Vmax=" + str(Vmax) + " Km=" + str(Km))
for S in [0.5, 1.0, 2.0, 5.0, 10.0, 20.0]:
  say("    [S]=" + str(S) + "  v=" + str(round(michaelis_menten(Vmax, S, Km), 2)))

say("")
say("-- Enzyme Inhibition --")
say("  Competitive inhibition (Ki=1.0, [I]=2.0):")
for S in [0.5, 2.0, 10.0]:
  let v_normal = michaelis_menten(Vmax, S, Km)
  let v_inhib = competitive_inhibition(Vmax, S, Km, 2.0, 1.0)
  say("    [S]=" + str(S) + "  v_normal=" + str(round(v_normal, 2)) + "  v_inhibited=" + str(round(v_inhib, 2)))

say("")
say("-- Arrhenius & Activation Energy --")
let k1 = 0.01
let k2 = 0.05
let Ea = activation_energy(k1, 300, k2, 350)
say("  k(300K)=" + str(k1) + "  k(350K)=" + str(k2))
say("  Activation energy: " + str(round(Ea / 1000, 2)) + " kJ/mol")

say("")
say("-- Hill Equation (Cooperativity) --")
let K_half = 5.0
for n_hill in [1, 2, 4]:
  say("  Hill n=" + str(n_hill) + ":")
  for S in [1, 3, 5, 10, 20]:
    say("    [S]=" + str(S) + "  v=" + str(round(hill_equation(10, S, K_half, n_hill), 2)))

say("")
say("-- Reaction Progress --")
let k_p = 0.1
say("  A -> P (first order, k=0.1)")
for t in [0, 5, 10, 15, 20, 25]:
  let a_t = integrated_first_order(1.0, k_p, t)
  let p_t = product_concentration_first(1.0, k_p, t)
  say("    t=" + str(t) + "s  [A]=" + str(round(a_t, 4)) + "  [P]=" + str(round(p_t, 4)))

say("")
say("  Reaction kinetics verified!")
