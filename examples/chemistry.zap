# ═══════════════════════════════════════════════════════════════════
# Demo: Chemistry Lab — Molecules, reactions, thermodynamics
# Run via: zap run main.zap (imports all libs + examples)
# ═══════════════════════════════════════════════════════════════════

say("")
say("=== DEMO: Chemistry Lab ===")

let water = make_water()
let co2 = make_co2()
let methane = make_methane()
let nacl = make_nacl()
let h2 = make_hydrogen()
let o2 = make_oxygen()
let fe2o3 = make_iron_oxide()
let h2so4 = make_sulfuric_acid()
let ammonia = make_ammonia()

say("")
say("-- Molecules --")
say("  " + str(water))
say("  " + str(co2))
say("  " + str(methane))
say("  " + str(nacl))
say("  " + str(fe2o3))
say("  " + str(h2so4))
say("  " + str(ammonia))

say("")
say("-- Molecular Properties --")
say("  Water bond energy: " + str(water.bond_energy()) + " kJ/mol")
say("  Water polarity: " + str(round(water.polarity(), 2)))
say("  Water formula: " + water.formula())
say("  CO2 molecular mass: " + str(round(co2.molecular_mass(), 3)) + " g/mol")
say("  NaCl ionic bond energy: " + str(nacl.bond_energy()) + " kJ/mol")
say("  H2SO4 mass: " + str(round(h2so4.molecular_mass(), 3)) + " g/mol")
say("  Ammonia atoms: " + str(ammonia.atom_count()))

say("")
say("-- Chemical Reactions --")

let combustion = Reaction("Methane Combustion", [methane, o2], [co2, water], -890.4)
say("  " + str(combustion))
say("  exothermic? " + str(combustion.is_exothermic()))
say("  energy/gram: " + str(round(combustion.energy_per_gram(), 2)) + " kJ/g")

let rust = Reaction("Iron Rusting", [fe2o3], [fe2o3], -824.2)
say("  " + str(rust))

let neutralize = Reaction("Neutralization", [nacl], [nacl], -57.1)
say("  " + str(neutralize))

say("")
say("-- Thermodynamics --")
let T = celsius_to_kelvin(25)
say("  25C in Kelvin: " + str(round(T, 2)) + " K")

let P = ideal_gas_pressure(1, T, 0.0224)
say("  1 mol ideal gas at STP: " + str(round(P, 1)) + " Pa")

let dH = -890.4
let dS = -0.242
let G = gibbs_free_energy(dH, dS, T)
say("  Methane combustion:")
say("    dH = " + str(dH) + " kJ/mol")
say("    dS = " + str(dS) + " kJ/(mol*K)")
say("    T  = " + str(round(T, 2)) + " K")
say("    Gibbs free energy: " + str(round(G, 2)) + " kJ/mol")
say("    Spontaneous at 25C? " + str(G < 0))

let rms = root_mean_square_speed(0.018, T)
say("  H2O RMS speed at 25C: " + str(round(rms, 1)) + " m/s")
