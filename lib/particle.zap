# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Particle: Point-mass with force accumulation
# ═══════════════════════════════════════════════════════════════════

class Particle:
  fn init(self, name, mass, pos, vel)
    self.name = name
    self.mass = mass
    self.pos = pos
    self.vel = vel
    self.force = Vec2(0, 0)
    self.charge = 0
    self.radius = mass * 0.5

  fn apply_force(self, f)
    self.force = self.force.add(f)

  fn kinetic_energy(self)
    0.5 * self.mass * self.vel.dot(self.vel)

  fn momentum(self)
    self.vel.scale(self.mass)

  fn step(self, dt)
    let ax = self.force.x / self.mass
    let ay = self.force.y / self.mass
    self.vel = self.vel.add(Vec2(ax, ay).scale(dt))
    self.pos = self.pos.add(self.vel.scale(dt))
    self.force = Vec2(0, 0)

  fn speed(self)
    self.vel.length()

  fn repr(self)
    self.name + "@(" + str(round(self.pos.x, 2)) + "," + str(round(self.pos.y, 2)) + ")"
