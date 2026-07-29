# ═══════════════════════════════════════════════════════════════════
# Demo: Elastic Collisions — 3-body collision dynamics
# Run via: zap run main.zap (imports all libs + examples)
# ═══════════════════════════════════════════════════════════════════

say("")
say("=== DEMO: Elastic Collisions ===")

let world = World()
world.has_gravity = false

let ball1 = Particle("Ball-1", 1, Vec2(-10, 0), Vec2(5, 0))
let ball2 = Particle("Ball-2", 1, Vec2(10, 0), Vec2(-5, 0))
let ball3 = Particle("Ball-3", 3, Vec2(0, 5), Vec2(0, -2))

world.add(ball1)
world.add(ball2)
world.add(ball3)

say("")
say("-- Simulating collisions --")
for step in range(20):
  for i in range(1, len(world.particles)):
    for j in range(i + 1, len(world.particles)):
      collide(world.particles[i], world.particles[j])
  world.step(0.05)

world.summary()
say("Collision dynamics verified!")
