# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — World: Simulation container and integrator
# ═══════════════════════════════════════════════════════════════════

import "forces.zap"

class World:
  fn init(self)
    self.particles = []
    self.gx = 0
    self.gy = -9.81
    self.has_gravity = true
    self.bx_min = -20
    self.bx_max = 20
    self.by_min = -20
    self.by_max = 20
    self.time = 0
    self.steps = 0
    self.g_const = 50

  fn add(self, p)
    self.particles = self.particles + [p]

  fn apply_global_forces(self)
    for p in self.particles:
      if self.has_gravity:
        let weight = Vec2(self.gx, self.gy).scale(p.mass)
        p.apply_force(weight)

  fn apply_gravity_forces(self)
    for i in range(len(self.particles)):
      for j in range(i + 1, len(self.particles)):
        let f = gravity(self.particles[i], self.particles[j], self.g_const)
        self.particles[i].apply_force(f)
        self.particles[j].apply_force(f.scale(-1))

  fn resolve_collisions(self)
    for i in range(len(self.particles)):
      for j in range(i + 1, len(self.particles)):
        collide(self.particles[i], self.particles[j])

  fn enforce_bounds(self)
    for p in self.particles:
      if p.pos.x < self.bx_min:
        p.pos.x = self.bx_min
        p.vel.x = abs(p.vel.x) * 0.8
      if p.pos.x > self.bx_max:
        p.pos.x = self.bx_max
        p.vel.x = -abs(p.vel.x) * 0.8
      if p.pos.y < self.by_min:
        p.pos.y = self.by_min
        p.vel.y = abs(p.vel.y) * 0.8
      if p.pos.y > self.by_max:
        p.pos.y = self.by_max
        p.vel.y = -abs(p.vel.y) * 0.8

  fn step(self, dt)
    self.apply_global_forces()
    self.apply_gravity_forces()
    for p in self.particles:
      p.step(dt)
    self.resolve_collisions()
    self.enforce_bounds()
    self.time = self.time + dt
    self.steps = self.steps + 1

  fn total_energy(self)
    let ke = 0
    for p in self.particles:
      ke = ke + p.kinetic_energy()
    let pe = 0
    for i in range(len(self.particles)):
      for j in range(i + 1, len(self.particles)):
        pe = pe + gravity_potential(self.particles[i], self.particles[j], self.g_const)
    ke + pe

  fn total_kinetic_energy(self)
    let ke = 0
    for p in self.particles:
      ke = ke + p.kinetic_energy()
    ke

  fn total_potential_energy(self)
    let pe = 0
    for i in range(len(self.particles)):
      for j in range(i + 1, len(self.particles)):
        pe = pe + gravity_potential(self.particles[i], self.particles[j], self.g_const)
    pe

  fn center_of_mass(self)
    let mx = 0
    let my = 0
    let total_m = 0
    for p in self.particles:
      mx = mx + p.pos.x * p.mass
      my = my + p.pos.y * p.mass
      total_m = total_m + p.mass
    if total_m > 0:
      Vec2(mx / total_m, my / total_m)
    el:
      Vec2(0, 0)

  fn momentum_sum(self)
    let px = 0
    let py = 0
    for p in self.particles:
      px = px + p.momentum().x
      py = py + p.momentum().y
    Vec2(px, py)

  fn summary(self)
    say("=== PHYSICS WORLD SUMMARY ===")
    say("  time: " + str(round(self.time, 3)) + "s")
    say("  steps: " + str(self.steps))
    say("  particles: " + str(len(self.particles)))
    say("  total energy (KE+PE): " + str(round(self.total_energy(), 4)))
    say("  kinetic energy: " + str(round(self.total_kinetic_energy(), 4)))
    say("  potential energy: " + str(round(self.total_potential_energy(), 4)))
    let com = self.center_of_mass()
    say("  center of mass: (" + str(round(com.x, 2)) + ", " + str(round(com.y, 2)) + ")")
    let mom = self.momentum_sum()
    say("  total momentum: (" + str(round(mom.x, 4)) + ", " + str(round(mom.y, 4)) + ")")
    for p in self.particles:
      say("  " + p.name + " pos=(" + str(round(p.pos.x, 2)) + "," + str(round(p.pos.y, 2)) + ")"
          + " vel=(" + str(round(p.vel.x, 2)) + "," + str(round(p.vel.y, 2)) + ")"
          + " KE=" + str(round(p.kinetic_energy(), 3)))
