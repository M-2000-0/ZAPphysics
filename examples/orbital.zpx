# ═══════════════════════════════════════════════════════════════════
# Demo: Orbital Mechanics — Star + 3 orbiting bodies
# Run via: zap run main.zap (imports all libs + examples)
# ═══════════════════════════════════════════════════════════════════

say("")
say("=== DEMO: Orbital Mechanics ===")

let world = World()
world.g_const = 100
world.has_gravity = false
world.bx_min = -500
world.bx_max = 500
world.by_min = -500
world.by_max = 500

let star = Particle("Star", 10000, Vec2(0, 0), Vec2(0, 0))
star.radius = 5
let planet1 = Particle("Planet-A", 10, Vec2(100, 0), Vec2(0, 31.6))
planet1.radius = 1
let planet2 = Particle("Planet-B", 20, Vec2(0, -200), Vec2(22.4, 0))
planet2.radius = 1.5
let comet = Particle("Comet", 1, Vec2(-300, 100), Vec2(10, 15))
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
say("-- Simulating " + str(step_count) + " steps (dt=0.01s) --")
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
