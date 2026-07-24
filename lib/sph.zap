# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — SPH: Smoothed Particle Hydrodynamics
# Fluid dynamics simulation using particle-based methods
# ═══════════════════════════════════════════════════════════════════

# integer power helper
fn ipow(base, exp)
  let result = 1
  for i in range(exp):
    result = result * base
  result

# Poly6 kernel (2D): W(r,h) = 4/(pi*h^8) * (h^2 - r^2)^3
fn poly6_2d(r, h)
  if r >= h:
    ret 0
  let diff = h * h - r * r
  4.0 / (3.14159265 * ipow(h, 8)) * diff * diff * diff

# Spiky gradient kernel (2D): for pressure forces
fn spiky_gradient_2d(r_vec, r_len, h)
  if r_len >= h or r_len < 1e-10:
    ret Vec2(0, 0)
  let diff = h - r_len
  let factor = -30.0 / (3.14159265 * ipow(h, 5)) * diff * diff
  r_vec.normalize().scale(factor)

# Viscosity Laplacian kernel (2D): for viscous forces
fn viscosity_laplacian_2d(r_len, h)
  if r_len >= h:
    ret 0
  40.0 / (3.14159265 * ipow(h, 5)) * (h - r_len)

# SPH Fluid Particle
class FluidParticle:
  fn init(self, name, mass, pos, vel)
    self.name = name
    self.mass = mass
    self.pos = pos
    self.vel = vel
    self.force = Vec2(0, 0)
    self.density = 0
    self.pressure = 0
    self.radius = 0.3

  fn apply_force(self, f)
    self.force = self.force.add(f)

  fn step(self, dt)
    let ax = self.force.x / max(self.density, 0.001)
    let ay = self.force.y / max(self.density, 0.001)
    self.vel = self.vel.add(Vec2(ax, ay).scale(dt))
    self.pos = self.pos.add(self.vel.scale(dt))
    self.force = Vec2(0, 0)

  fn kinetic_energy(self)
    0.5 * self.mass * self.vel.dot(self.vel)

  fn repr(self)
    self.name + "@(" + str(round(self.pos.x, 2)) + "," + str(round(self.pos.y, 2)) + ") rho=" + str(round(self.density, 2))

# SPH Fluid World
class FluidWorld:
  fn init(self)
    self.particles = []
    self.h = 1.0
    self.rest_density = 1000.0
    self.gas_constant = 2000.0
    self.viscosity = 200.0
    self.gx = 0
    self.gy = -9.81
    self.time = 0
    self.steps = 0
    self.bx_min = -20
    self.bx_max = 20
    self.by_min = -20
    self.by_max = 20

  fn add(self, p)
    self.particles = self.particles + [p]

  fn compute_density_pressure(self)
    for i in range(len(self.particles)):
      let pi = self.particles[i]
      pi.density = 0
      for j in range(len(self.particles)):
        let pj = self.particles[j]
        let r = pi.pos.dist(pj.pos)
        pi.density = pi.density + pj.mass * poly6_2d(r, self.h)
      pi.pressure = self.gas_constant * (pi.density - self.rest_density)

  fn compute_forces(self)
    for i in range(len(self.particles)):
      let pi = self.particles[i]
      let pressure_force = Vec2(0, 0)
      let viscosity_force = Vec2(0, 0)

      for j in range(len(self.particles)):
        if i != j:
          let pj = self.particles[j]
          let diff = pi.pos.sub(pj.pos)
          let r = diff.length()
          if r < self.h and r > 1e-10:
            # pressure force
            let avg_pressure = (pi.pressure + pj.pressure) / 2.0
            let grad = spiky_gradient_2d(diff, r, self.h)
            pressure_force.x = pressure_force.x - pj.mass * avg_pressure / pj.density * grad.x
            pressure_force.y = pressure_force.y - pj.mass * avg_pressure / pj.density * grad.y

            # viscosity force
            let lap = viscosity_laplacian_2d(r, self.h)
            viscosity_force.x = viscosity_force.x + self.viscosity * pj.mass * (pj.vel.x - pi.vel.x) / pj.density * lap
            viscosity_force.y = viscosity_force.y + self.viscosity * pj.mass * (pj.vel.y - pi.vel.y) / pj.density * lap

      # gravity
      let gravity_force = Vec2(self.gx, self.gy).scale(pi.density)

      pi.force = pressure_force.add(viscosity_force).add(gravity_force)

  fn enforce_bounds(self)
    for p in self.particles:
      if p.pos.x < self.bx_min:
        p.pos.x = self.bx_min
        p.vel.x = abs(p.vel.x) * 0.5
      if p.pos.x > self.bx_max:
        p.pos.x = self.bx_max
        p.vel.x = -abs(p.vel.x) * 0.5
      if p.pos.y < self.by_min:
        p.pos.y = self.by_min
        p.vel.y = abs(p.vel.y) * 0.5
      if p.pos.y > self.by_max:
        p.pos.y = self.by_max
        p.vel.y = -abs(p.vel.y) * 0.5

  fn step(self, dt)
    self.compute_density_pressure()
    self.compute_forces()
    for p in self.particles:
      p.step(dt)
    self.enforce_bounds()
    self.time = self.time + dt
    self.steps = self.steps + 1

  fn total_energy(self)
    let ke = 0
    for p in self.particles:
      ke = ke + p.kinetic_energy()
    ke

  fn avg_density(self)
    let total = 0
    for p in self.particles:
      total = total + p.density
    if len(self.particles) > 0:
      total / len(self.particles)
    el:
      0

  fn summary(self)
    say("=== FLUID WORLD SUMMARY ===")
    say("  time: " + str(round(self.time, 3)) + "s")
    say("  steps: " + str(self.steps))
    say("  particles: " + str(len(self.particles)))
    say("  total KE: " + str(round(self.total_energy(), 4)))
    say("  avg density: " + str(round(self.avg_density(), 2)))
    for p in self.particles:
      say("  " + p.name + " pos=(" + str(round(p.pos.x, 2)) + "," + str(round(p.pos.y, 2)) + ")"
          + " vel=(" + str(round(p.vel.x, 2)) + "," + str(round(p.vel.y, 2)) + ")"
          + " rho=" + str(round(p.density, 1)))
