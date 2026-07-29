# ═══════════════════════════════════════════════════════════════════
# Demo: SPH Fluid Dynamics — Water-like particle simulation
# Run: zap run main.zap
# ═══════════════════════════════════════════════════════════════════

say("")
say("=== DEMO: SPH Fluid Dynamics ===")

let fw = FluidWorld()
fw.rest_density = 50.0
fw.gas_constant = 500.0
fw.viscosity = 100.0
fw.h = 2.0
fw.by_min = -10
fw.by_max = 15
fw.bx_min = -10
fw.bx_max = 10

say("-- Creating fluid particles in a block --")
for row in range(4):
  for col in range(5):
    let x = -4.0 + col * 1.0
    let y = 2.0 + row * 1.0
    let p = FluidParticle("f" + str(row) + str(col), 1.0, Vec2(x, y), Vec2(0, 0))
    fw.add(p)

say("  Created " + str(len(fw.particles)) + " fluid particles")
say("")
say("-- Initial state --")
fw.summary()

say("")
say("-- Simulating fluid dynamics (15 steps) --")
for step in range(15):
  fw.step(0.02)

say("")
say("-- Final state --")
fw.summary()

say("")
say("  Fluid settled under gravity with pressure & viscosity!")
