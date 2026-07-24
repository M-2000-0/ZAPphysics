# ═══════════════════════════════════════════════════════════════════
# Demo: Electromagnetic Forces — Coulomb, fields, Lorentz
# Run: zap run main.zap
# ═══════════════════════════════════════════════════════════════════

say("")
say("=== DEMO: Electromagnetic Forces ===")

let world = World()
world.has_gravity = false

let plus = Particle("Proton+", 1, Vec2(-5, 0), Vec2(0, 0))
let minus = Particle("Electron-", 0.1, Vec2(5, 0), Vec2(0, 3))
plus.charge = 1.6e-19
minus.charge = -1.6e-19

let c1 = Charge(plus, 1.0)
let c2 = Charge(minus, -1.0)

world.add(plus)
world.add(minus)

say("")
say("-- Coulomb Force --")
say("  " + str(c1))
say("  " + str(c2))

let k = 8.9875e9
let force = coulomb_force(c1, c2, k)
say("  Coulomb force magnitude: " + str(round(force.length(), 2)) + " N")

let energy = electric_potential_energy(c1, c2, k)
say("  Potential energy: " + str(round(energy, 4)) + " J")

say("")
say("-- Electric Field --")
let test_point = Vec2(0, 5)
let field1 = electric_field(c1, test_point, k)
let field2 = electric_field(c2, test_point, k)
let total_field = field1.add(field2)
say("  E-field at (0,5) from proton:  " + str(field1))
say("  E-field at (0,5) from electron: " + str(field2))
say("  Total E-field at (0,5): " + str(total_field))

say("")
say("-- Lorentz Force --")
let B = Vec3(0, 0, 1)
let v3 = Vec3(3, 0, 0)
let E3 = Vec3(0, 1, 0)
let charge_obj = Charge(plus, 1.0)
let lorentz = lorentz_force(charge_obj, v3, E3, B)
say("  v=" + str(v3) + " B=" + str(B) + " E=" + str(E3))
say("  Lorentz force: " + str(lorentz))

say("")
say("-- Simulating attraction (20 steps) --")
for step in range(20):
  let f = coulomb_force(c1, c2, 500)
  plus.apply_force(f)
  minus.apply_force(f.scale(-1))
  world.step(0.02)

say("  " + str(plus.pos) + " -> " + str(minus.pos))
say("  Particles attracted as expected!")
