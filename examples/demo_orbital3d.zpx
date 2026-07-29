# ═══════════════════════════════════════════════════════════════════
# Demo: 3D Orbital Mechanics with Velocity Verlet
# Run via: zap run main.zap or: zap run examples/demo_orbital3d.zap
# ═══════════════════════════════════════════════════════════════════

import "../lib/particle3d.zap"
import "../lib/world3d.zap"
import "../lib/visual.zap"

say("")
say("=== DEMO: 3D Orbital Mechanics (Velocity Verlet) ===")

let world = World3D()
world.g_const = 50
world.has_gravity = false
world.integrator = "velocity_verlet"
world.adaptive_dt = true
world.force_threshold = 1000.0
world.dt_min = 1e-4
world.dt_max = 0.05

let star = Particle3D("Star", 10000, Vec3(0, 0, 0), Vec3(0, 0, 0))
star.radius = 5
let planet1 = Particle3D("Planet-A", 10, Vec3(100, 0, 0), Vec3(0, 31.6, 10))
planet1.radius = 1
let planet2 = Particle3D("Planet-B", 20, Vec3(0, 0, -200), Vec3(22.4, 0, -5))
planet2.radius = 1.5
let comet = Particle3D("Comet", 1, Vec3(-300, 100, 50), Vec3(10, 15, -3))
comet.radius = 0.5

world.add(star)
world.add(planet1)
world.add(planet2)
world.add(comet)

say("")
say("-- Initial state --")
world.summary()

let energy_history = []
let step_count = 200

say("")
say("-- Simulating " + str(step_count) + " steps (dt=0.01s) with Velocity Verlet --")
for step in range(step_count):
  world.step(0.01)
  let e = world.total_energy()
  energy_history = energy_history + [e]

say("")
say("-- Final state --")
world.summary()

say("")
say("-- Energy conservation check --")
let e0 = energy_history[0]
let ef = energy_history[len(energy_history) - 1]
let drift = abs(ef - e0) / abs(e0) * 100
say("  Initial energy: " + str(round(e0, 4)))
say("  Final energy:   " + str(round(ef, 4)))
say("  Energy drift:   " + str(round(drift, 4)) + "%")
if drift < 1.0:
  say("  Result: ENERGY CONSERVED")
el:
  say("  Result: ENERGY DRIFT DETECTED (drift > 1%)")

say("")
say("-- Energy history (sparkline) --")
let spark = ascii_sparkline(energy_history)
say("  " + spark)