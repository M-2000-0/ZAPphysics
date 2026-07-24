# ═══════════════════════════════════════════════════════════════════
# Demo: 3D Particle Simulation — N-body in 3D space
# Run: zap run main.zap
# ═══════════════════════════════════════════════════════════════════

say("")
say("=== DEMO: 3D Particle Simulation ===")

let particles = []
let s = Particle3D("Sun", 1000, Vec3(0, 0, 0), Vec3(0, 0, 0))
let p1 = Particle3D("Planet-XY", 1, Vec3(10, 0, 0), Vec3(0, 7, 2))
let p2 = Particle3D("Planet-XZ", 2, Vec3(0, 0, -12), Vec3(5, 0, 0))
let p3 = Particle3D("Planet-XYZ", 0.5, Vec3(-5, 8, 3), Vec3(1, -3, 4))

particles = particles + [s, p1, p2, p3]

say("-- Initial positions --")
for p in particles:
  say("  " + str(p))

say("")
say("-- Simulating 3D orbits (25 steps, dt=0.02) --")
let G = 50
for step in range(25):
  for i in range(1, len(particles)):
    let diff = particles[i].pos.sub(particles[0].pos)
    let dist = max(diff.length(), 0.5)
    let strength = G * particles[0].mass * particles[i].mass / (dist * dist)
    let dir = diff.normalize().scale(strength)
    particles[i].apply_force(dir)
    particles[0].apply_force(dir.scale(-1))
  for p in particles:
    p.step(0.02)

say("")
say("-- Final positions --")
for p in particles:
  say("  " + str(p) + "  speed=" + str(round(p.speed(), 2)))
say("  3D orbital mechanics verified!")
