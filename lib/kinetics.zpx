# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Kinetics: Reaction rate equations & equilibrium
# ═══════════════════════════════════════════════════════════════════

# integer power helper
fn ipow(base, exp)
  let result = 1
  for i in range(exp):
    result = result * base
  result

# Rate law: rate = k * [A]^m * [B]^n
fn rate_law(k, concentrations, orders)
  let rate = k
  for i in range(len(concentrations)):
    rate = rate * ipow(concentrations[i], orders[i])
  rate

# Integrated rate law: zero order [A] = [A]0 - k*t
fn integrated_zero_order(a0, k, t)
  a0 - k * t

# Integrated rate law: first order [A] = [A]0 * e^(-kt)
fn integrated_first_order(a0, k, t)
  a0 * exp(-k * t)

# Integrated rate law: second order 1/[A] = 1/[A]0 + k*t
fn integrated_second_order(a0, k, t)
  let denom = 1.0 / a0 + k * t
  1.0 / denom

# Half-life: zero order t1/2 = [A]0 / (2k)
fn half_life_zero(a0, k)
  a0 / (2.0 * k)

# Half-life: first order t1/2 = log(2) / k
fn half_life_first(k)
  0.693147180559945 / k

# Half-life: second order t1/2 = 1 / (k * [A]0)
fn half_life_second(a0, k)
  1.0 / (k * a0)

# Equilibrium constant Kc = [products]^p / [reactants]^r
fn equilibrium_constant(products_conc, reactants_conc)
  let num = 1
  for c in products_conc:
    num = num * c
  let den = 1
  for c in reactants_conc:
    den = den * c
  if den > 0:
    num / den
  el:
    999999

# Gibbs free energy from K: dG = -RT * log(K)
fn gibbs_from_equilibrium(K, T)
  let R = 8.314
  -R * T * log(K)

# Van't Hoff equation: log(K2/K1) = -dH/R * (1/T2 - 1/T1)
fn vant_hoff(K1, T1, T2, dH)
  let R = 8.314
  let ln_ratio = -dH / R * (1.0 / T2 - 1.0 / T1)
  K1 * exp(ln_ratio)

# Michaelis-Menten kinetics: v = Vmax * [S] / (Km + [S])
fn michaelis_menten(vmax, S, Km)
  vmax * S / (Km + S)

# Enzyme inhibition: competitive v = Vmax * [S] / (Km*(1 + [I]/Ki) + [S])
fn competitive_inhibition(vmax, S, Km, I, Ki)
  vmax * S / (Km * (1.0 + I / Ki) + S)

# Enzyme inhibition: non-competitive v = Vmax * [S] / ((Km + [S]) * (1 + [I]/Ki))
fn noncompetitive_inhibition(vmax, S, Km, I, Ki)
  vmax * S / ((Km + S) * (1.0 + I / Ki))

# Lineweaver-Burk: 1/v = (Km/Vmax) * 1/[S] + 1/Vmax
fn lineweaver_burk(S, Km, vmax)
  if S > 0:
    Km / vmax * (1.0 / S) + 1.0 / vmax
  el:
    999999

# Hill equation: v = Vmax * [S]^n / (K0.5^n + [S]^n)
fn hill_equation(vmax, S, K_half, n)
  vmax * ipow(S, n) / (ipow(K_half, n) + ipow(S, n))

# Cooperativity coefficient (Hill coefficient)
fn hill_coefficient(log_conc, log_rate, points)
  # simplified: slope of log(rate) vs log(conc) using first and last points
  if points > 1:
    let dx = log_conc[points - 1] - log_conc[0]
    if abs(dx) > 1e-10:
      (log_rate[points - 1] - log_rate[0]) / dx
    el:
      1
  el:
    1

# Arrhenius with pre-exponential factor
fn arrhenius(A, Ea, T)
  let R = 8.314
  A * exp(-Ea / (R * T))

# Activation energy from two temperatures
fn activation_energy(k1, T1, k2, T2)
  let R = 8.314
  R * log(k2 / k1) / (1.0 / T1 - 1.0 / T2)

# Collision frequency factor (hard sphere)
fn collision_frequency(sigma, mu, T)
  let k = 1.380649e-23
  sigma * sqrt(8 * k * T / (3.14159265 * mu))

# Transition state theory rate
fn transition_state_rate(kT_h, dG_star)
  kT_h * exp(-dG_star)

# Steady state approximation for [I] in A -> I -> P
fn steady_state_conc(k1, k2, A0, t)
  if abs(k1 - k2) > 1e-10:
    k1 * A0 / (k2 - k1) * (exp(-k1 * t) - exp(-k2 * t))
  el:
    k1 * A0 * t * exp(-k1 * t)

# Product concentration A -> P (first order)
fn product_concentration_first(a0, k, t)
  a0 * (1.0 - exp(-k * t))

# Reaction progress: extent of reaction xi
fn extent_of_reaction(a0, at, stoich)
  (a0 - at) / stoich

# Equilibrium from forward and reverse rates
fn equilibrium_from_rates(kf, kr)
  if kr > 0:
    kf / kr
  el:
    999999

# Le Chatelier shift: new K from pressure change (gas reactions)
fn le_chatelier_pressure(K, delta_n, P1, P2)
  K * ipow(P2 / P1, delta_n)

# Rate comparison: determine reaction order from data
fn determine_order(conc_data, rate_data, n_points)
  # simplified: compare rate ratios
  if n_points < 2:
    ret 0
  let ratio_rate = rate_data[1] / rate_data[0]
  let ratio_conc = conc_data[1] / conc_data[0]
  if ratio_conc > 1e-10:
    log(ratio_rate) / log(ratio_conc)
  el:
    0
