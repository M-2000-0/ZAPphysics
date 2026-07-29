# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Thermodynamics: Gas laws, Gibbs energy, entropy
# ═══════════════════════════════════════════════════════════════════

fn celsius_to_kelvin(c) c + 273.15
fn kelvin_to_celsius(k) k - 273.15

fn ideal_gas_pressure(n, t, v)
  let R = 8.314
  n * R * t / v

fn ideal_gas_volume(n, t, p)
  let R = 8.314
  n * R * t / p

fn entropy_change(dh, t)
  if t > 0:
    dh / t
  el:
    0

fn gibbs_free_energy(dh, ds, t)
  dh - t * ds

fn boltzmann_probability(energy, temperature)
  let k = 1.380649e-23
  exp(-energy / (k * temperature))

fn arrhenius_rate(a, ea, t)
  let R = 8.314
  a * exp(-ea / (R * t))

fn heat_capacity_cv(degrees_freedom)
  degrees_freedom * 4.164

fn heat_capacity_cp(degrees_freedom)
  (degrees_freedom + 2) * 4.164

fn root_mean_square_speed(molar_mass, temperature)
  let R = 8.314
  sqrt(3 * R * temperature / molar_mass)
