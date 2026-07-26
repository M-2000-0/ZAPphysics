# ═══════════════════════════════════════════════════════════════════
# Demo: Rocket Engineering — Multi-stage rocket design & simulation
# Run via: zap run main.zap (imports all libs + examples)
# ═══════════════════════════════════════════════════════════════════

say("")
say("=== DEMO: Rocket Engineering ===")

# ── Design a Falcon 9-like rocket ──
let rocket = Rocket("Falcon-9")

# First stage
let engine1 = merlin_1d()
let stage1 = RocketStage("Stage 1", engine1, 40000, 25000)
stage1.color = "#e94560"
rocket.add_stage(stage1)

# Second stage
let engine2 = merlin_1d()
let stage2 = RocketStage("Stage 2", engine2, 10000, 4000)
stage2.color = "#00d4ff"
rocket.add_stage(stage2)

# Payload
rocket.set_payload(5000)

say("")
say("-- Rocket Design --")
rocket.summary()

# ── Simulate flight ──
say("")
say("-- Simulating flight trajectory --")
let dt = 1.0
let trajectory = rocket.simulate(dt, 400)

# Print key milestones
say("  Data points: " + str(len(trajectory)))
let max_alt = 0
let max_vel = 0
for t in trajectory:
  if t["altitude"] > max_alt:
    max_alt = t["altitude"]
  if t["velocity"] > max_vel:
    max_vel = t["velocity"]
say("  Max altitude: " + str(round(max_alt, 1)) + " m")
say("  Max velocity: " + str(round(max_vel, 1)) + " m/s")

# ── Thrust curve ──
say("")
say("-- Thrust curve data --")
let thrust_data = rocket.thrust_curve(dt)
say("  Total data points: " + str(len(thrust_data)))
say("  Peak thrust: " + str(rocket.stages[0].engine.thrust) + " N")
say("  Total impulse: " + str(round(rocket.total_impulse(), 0)) + " Ns")

# ── Rocket equation verification ──
say("")
say("-- Tsiolkovsky Rocket Equation --")
let total_dv = rocket.total_delta_v()
say("  Total delta-v: " + str(round(total_dv, 1)) + " m/s")
say("  Required for LEO: ~9400 m/s")
say("  Required for Moon: ~12000 m/s")
say("  Required for Mars: ~15000 m/s")
if total_dv > 9400:
  say("  Result: Can reach LEO")
el:
  say("  Result: Cannot reach LEO (need more delta-v)")

# ── Engine comparison ──
say("")
say("-- Engine Comparison --")
let engines = [merlin_1d(), raptor(), f1(), rs_25(), rutherford()]
for e in engines:
  say("  " + e.name + ": Isp=" + str(e.isp) + "s, Thrust=" + str(e.thrust) + "N, mdot=" + str(round(e.mass_flow_rate(), 1)) + "kg/s, impulse=" + str(round(e.total_impulse(), 0)) + "Ns")

# ── Mass ratio calculations ──
say("")
say("-- Mass Ratio Calculations --")
say("  LEO (9400 m/s, Isp=350): mass_ratio=" + str(round(mass_ratio(9400, 350), 2)) + ", prop_frac=" + str(round(propellant_fraction(9400, 350) * 100, 1)) + "%")
say("  Moon (12000 m/s, Isp=350): mass_ratio=" + str(round(mass_ratio(12000, 350), 2)) + ", prop_frac=" + str(round(propellant_fraction(12000, 350) * 100, 1)) + "%")
say("  Mars (15000 m/s, Isp=450): mass_ratio=" + str(round(mass_ratio(15000, 450), 2)) + ", prop_frac=" + str(round(propellant_fraction(15000, 450) * 100, 1)) + "%")

# ── Summary ──
say("")
say("Rocket engineering verified!")