# ═══════════════════════════════════════════════════════════════════
# Demo: Spring-Mass System — Damped harmonic oscillations
# Run via: zap run main.zap (imports all libs + examples)
# ═══════════════════════════════════════════════════════════════════

say("")
say("=== DEMO: Spring-Mass System ===")

let world = World()
world.has_gravity = false

let anchor = Particle("Anchor", 10000, Vec2(0, 0), Vec2(0, 0))
let mass1 = Particle("Mass-1", 1, Vec2(3, 0), Vec2(0, 2))
let mass2 = Particle("Mass-2", 1, Vec2(5, 0), Vec2(0, -1))

world.add(anchor)
world.add(mass1)
world.add(mass2)

say("")
say("-- Simulating spring oscillations --")
for step in range(30):
  let f1 = spring_force(world.particles[0], world.particles[1], 8, 2)
  let f2 = spring_force(world.particles[1], world.particles[2], 8, 2)
  world.particles[1].apply_force(f1)
  world.particles[1].apply_force(f2.scale(-1))
  world.particles[2].apply_force(f2)
  world.particles[1].apply_force(drag_force(world.particles[1].vel, 0.1))
  world.particles[2].apply_force(drag_force(world.particles[2].vel, 0.1))
  world.step(0.02)

world.summary()
say("Spring oscillations converge toward rest!")
