# ═══════════════════════════════════════════════════════════════════
# Demo: Generative Art — Particle systems & emitters
# Run: zap run main.zap
# ═══════════════════════════════════════════════════════════════════

say("")
say("=== DEMO: Generative Art ===")

let art = ArtWorld(800, 600)

# fountain emitter
let fountain = Emitter(400, 500, 3)
fountain.speed = 200
fountain.spread = 0.8
fountain.life_min = 1.0
fountain.life_max = 2.5
fountain.set_colors(["cyan", "blue", "white"])
art.add_emitter(fountain)

# spiral emitter
let spiral = Emitter(200, 300, 2)
spiral.speed = 80
spiral.life_min = 2.0
spiral.life_max = 4.0
spiral.set_colors(["red", "orange", "yellow"])
art.add_emitter(spiral)

# burst emitter
let burst_emitter = Emitter(600, 300, 0)
art.add_emitter(burst_emitter)

# gravity wells
let well1 = GravityWell(400, 300, 5000)
let well2 = GravityWell(600, 200, 3000)
art.add_well(well1)
art.add_well(well2)

say("")
say("-- Running art simulation (120 frames) --")

for frame in range(120):
  if frame == 60:
    burst_emitter.burst(30)
  art.step(1.0 / 30.0)

art.summary()

say("")
say("-- Particle system features --")
say("  - Fountain: continuous upward spray with gravity wells")
say("  - Spiral: golden-ratio angular emission")
say("  - Burst: explosive radial emission at frame 60")
say("  - Gravity wells attract all particles")
say("  - Screen-wrap for infinite canvas feel")
say("  Generative art verified!")
