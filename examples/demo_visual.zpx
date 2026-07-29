# ═══════════════════════════════════════════════════════════════════
# Demo: ASCII Visualization — Charts, heatmaps, vector fields
# Run: zap run main.zap
# ═══════════════════════════════════════════════════════════════════

say("")
say("=== DEMO: ASCII Visualization ===")

say("")
say("-- Bar Chart: Energy types --")
let labels = ["KE-orbit", "KE-spring", "KE-collision", "bond-H2O", "bond-NaCl", "Gibbs"]
let values = [68.65, 38.37, 31.0, 700, 411, -818]
ascii_bar_chart(values, labels, 30)

say("")
say("-- Sparkline: Temperature data --")
let temps = [20, 22, 25, 28, 31, 29, 26, 23, 21, 20, 22, 25, 28, 32, 35, 33, 30, 27, 24, 22]
say("  " + ascii_sparkline(temps))
say("  Min: " + str(temps[10]) + " Max: " + str(temps[14]))

say("")
say("-- Heatmap: Simulated density field (10x10) --")
let heat = []
for r in range(10):
  for c in range(10):
    let dx = c - 5
    let r_val = r - 5
    let val = exp(-(dx * dx + r_val * r_val) / 8.0) * 100
    heat = heat + [val]
ascii_heatmap(heat, 10, 10)

say("")
say("-- Box Diagram --")
ascii_box(0, 0, 20, 5)

say("")
say("-- Particle positions rendered --")
let world = World()
world.has_gravity = false
world.bx_min = 0
world.bx_max = 30
world.by_min = 0
world.by_max = 15
let a = Particle("A", 1, Vec2(3, 8), Vec2(2, -1))
let b = Particle("B", 2, Vec2(15, 5), Vec2(-1, 2))
let c = Particle("C", 1, Vec2(25, 10), Vec2(-2, 0))
world.add(a)
world.add(b)
world.add(c)

for step in range(5):
  world.step(0.5)

ascii_render_particles(world.particles, 30, 15, 0, 30, 0, 15)
say("  ASCII visualization verified!")
