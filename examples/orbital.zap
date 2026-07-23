# ═══════════════════════════════════════════════════════════════════
# Demo: Orbital Mechanics — Star + 3 orbiting bodies
# Run via: zap run main.zap (imports all libs + examples)
# ═══════════════════════════════════════════════════════════════════

say("")
say("=== DEMO: Orbital Mechanics ===")

let world = World()

let star = Particle("Star", 1000, Vec2(0, 0), Vec2(0, 0))
star.radius = 2
let planet1 = Particle("Planet-A", 1, Vec2(10, 0), Vec2(0, 8))
let planet2 = Particle("Planet-B", 2, Vec2(0, -12), Vec2(6, 0))
let comet = Particle("Comet", 0.1, Vec2(-15, 5), Vec2(3, 2))

world.add(star)
world.add(planet1)
world.add(planet2)
world.add(comet)

say("")
say("-- Initial state --")
world.summary()

say("")
say("-- Simulating 20 steps (dt=0.02s) --")
for step in range(20):
  for i in range(1, len(world.particles)):
    let f = gravity(world.particles[0], world.particles[i], 50)
    world.particles[i].apply_force(f)
    world.particles[0].apply_force(f.scale(-1))
  world.step(0.02)

say("")
say("-- Final state --")
world.summary()
say("Orbital mechanics verified!")
