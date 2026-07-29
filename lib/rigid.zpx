# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Rigid: Rigid body rotation & torque
# ═══════════════════════════════════════════════════════════════════

class RigidBody:
  fn init(self, name, mass, pos, vel)
    self.name = name
    self.mass = mass
    self.pos = pos
    self.vel = vel
    self.force = Vec2(0, 0)
    self.angle = 0
    self.angular_vel = 0
    self.torque = 0
    self.inertia = mass * 1.0
    self.radius = mass * 0.5
    self.restitution = 0.8
    self.friction = 0.1

  fn apply_force(self, f)
    self.force = self.force.add(f)

  fn apply_force_at(self, f, contact_point)
    let r = contact_point.sub(self.pos)
    self.force = self.force.add(f)
    self.torque = self.torque + r.x * f.y - r.y * f.x

  fn apply_torque(self, t)
    self.torque = self.torque + t

  fn angular_momentum(self)
    self.inertia * self.angular_vel

  fn rotational_kinetic_energy(self)
    0.5 * self.inertia * self.angular_vel * self.angular_vel

  fn translational_kinetic_energy(self)
    0.5 * self.mass * self.vel.dot(self.vel)

  fn total_kinetic_energy(self)
    self.translational_kinetic_energy() + self.rotational_kinetic_energy()

  fn step(self, dt)
    let ax = self.force.x / self.mass
    let ay = self.force.y / self.mass
    self.vel = self.vel.add(Vec2(ax, ay).scale(dt))
    self.pos = self.pos.add(self.vel.scale(dt))
    let alpha = self.torque / self.inertia
    self.angular_vel = self.angular_vel + alpha * dt
    self.angle = self.angle + self.angular_vel * dt
    self.force = Vec2(0, 0)
    self.torque = 0

  fn point_velocity(self, point)
    let r = point.sub(self.pos)
    let tangent = Vec2(-r.y, r.x).scale(self.angular_vel)
    self.vel.add(tangent)

  fn my_inertia_disk(self)
    0.5 * self.mass * self.radius * self.radius

  fn my_inertia_ring(self)
    self.mass * self.radius * self.radius

  fn my_inertia_rectangle(self, w, h)
    self.mass * (w * w + h * h) / 12.0

  fn repr(self)
    self.name + "@(" + str(round(self.pos.x, 2)) + "," + str(round(self.pos.y, 2)) + ") angle=" + str(round(self.angle, 2)) + " rad"

# Torque = r x F (2D cross product scalar)
fn torque_2d(r, force)
  r.x * force.y - r.y * force.x

# Moment of inertia for common shapes
fn inertia_disk(m, r) 0.5 * m * r * r
fn inertia_sphere(m, r) 0.4 * m * r * r
fn inertia_cylinder(m, r) 0.5 * m * r * r
fn inertia_rod(m, l) m * l * l / 12.0

# Angular acceleration: alpha = torque / inertia
fn angular_acceleration(torque, inertia)
  if abs(inertia) > 1e-10:
    torque / inertia
  el:
    0

# Rotational impulse: delta_omega = torque * dt / I
fn rotational_impulse(torque, inertia, dt)
  angular_acceleration(torque, inertia) * dt
