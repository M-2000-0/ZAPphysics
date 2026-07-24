# ═══════════════════════════════════════════════════════════════════
# Demo: Rigid Body Rotation & Torque — Spinning objects
# Run: zap run main.zap
# ═══════════════════════════════════════════════════════════════════

say("")
say("=== DEMO: Rigid Body Rotation & Torque ===")

let world = World()
world.has_gravity = false

# spinning top
let top1 = RigidBody("Top", 5, Vec2(0, 0), Vec2(0, 0))
top1.inertia = 10.0
top1.angular_vel = 15.0
world.add(top1)

# disk with applied torque
let disk = RigidBody("Disk", 3, Vec2(8, 0), Vec2(0, 0))
disk.inertia = inertia_disk(3.0, 2.0)
world.add(disk)

# rod spinning
let rod = RigidBody("Rod", 2, Vec2(-8, 0), Vec2(0, 0))
rod.inertia = inertia_rod(2.0, 6.0)
rod.angular_vel = 8.0
world.add(rod)

say("")
say("-- Initial state --")
for b in world.particles:
  say("  " + str(b) + "  omega=" + str(round(b.angular_vel, 2)) + " KE=" + str(round(b.total_kinetic_energy(), 2)))

say("")
say("-- Applying torque to disk (5 Nm for 20 steps) --")
for step in range(20):
  disk.apply_torque(5.0)
  world.step(0.05)

say("")
say("-- Final state --")
for b in world.particles:
  say("  " + str(b) + "  omega=" + str(round(b.angular_vel, 2)) + " KE=" + str(round(b.total_kinetic_energy(), 2)))
  say("    translational KE=" + str(round(b.translational_kinetic_energy(), 2))
      + " rotational KE=" + str(round(b.rotational_kinetic_energy(), 2)))

say("")
say("  Inertia shapes:")
say("    Disk (m=3, r=2): I=" + str(round(inertia_disk(3, 2), 2)))
say("    Rod (m=2, l=6):  I=" + str(round(inertia_rod(2, 6), 2)))
say("    Sphere (m=5, r=2): I=" + str(round(inertia_sphere(5, 2), 2)))
say("  Rotation verified!")
