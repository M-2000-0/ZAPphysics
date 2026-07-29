# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — EM: Electromagnetic force simulation
# Coulomb's law + electric field + dipole interactions
# ═══════════════════════════════════════════════════════════════════

class Charge:
  fn init(self, particle, q)
    self.particle = particle
    self.q = q
    particle.charge = q

  fn is_positive(self)
    self.q > 0

  fn is_negative(self)
    self.q < 0

  fn is_neutral(self)
    abs(self.q) < 1e-10

  fn repr(self)
    self.particle.name + "(q=" + str(round(self.q, 4)) + ")"

# Coulomb's law: F = k * q1 * q2 / r^2
fn coulomb_force(c1, c2, k_const)
  let diff = c2.particle.pos.sub(c1.particle.pos)
  let dist = diff.length()
  if dist < 0.01:
    dist = 0.01
  let strength = k_const * c1.q * c2.q / (dist * dist)
  let dir = diff.normalize()
  dir.scale(strength)

# Electric field at point p due to charge c: E = k * q / r^2 * r_hat
fn electric_field(c, point, k_const)
  let diff = point.sub(c.particle.pos)
  let dist = diff.length()
  if dist < 0.01:
    dist = 0.01
  let strength = k_const * c.q / (dist * dist)
  let dir = diff.normalize()
  dir.scale(strength)

# Electric potential energy between two charges: U = k * q1 * q2 / r
fn electric_potential_energy(c1, c2, k_const)
  let dist = c1.particle.pos.dist(c2.particle.pos)
  if dist < 0.01:
    dist = 0.01
  k_const * c1.q * c2.q / dist

# Electric potential at point: V = k * q / r
fn electric_potential(c, point, k_const)
  let dist = c.particle.pos.dist(point)
  if dist < 0.01:
    dist = 0.01
  k_const * c.q / dist

# Magnetic force on moving charge: F = q * v x B
fn magnetic_force(charge, velocity, B_field)
  let v_cross_b = velocity.cross(B_field)
  v_cross_b.scale(charge.q)

# Lorentz force: F = q * (E + v x B)
fn lorentz_force(charge, velocity, E_field, B_field)
  let magnetic = velocity.cross(B_field).scale(charge.q)
  let electric = E_field.scale(charge.q)
  electric.add(magnetic)

# Coulomb constant in SI: 8.9875e9
fn coulomb_constant() 8.9875e9

# Permittivity of free space: 8.854e-12
fn permittivity() 8.854e-12
