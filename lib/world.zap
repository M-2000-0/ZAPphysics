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
    self.integrator = "velocity_verlet"
    self.adaptive_dt = false
    self.dt_min = 1e-6
    self.dt_max = 1.0
    self.force_threshold = 1000.0

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

  fn compute_all_forces(self)
    self.apply_global_forces()
    self.apply_gravity_forces()

  fn compute_accelerations(self)
    let accels = []
    for p in self.particles:
      let ax = p.force.x / p.mass
      let ay = p.force.y / p.mass
      accels = accels + [Vec2(ax, ay)]
    accels

  # Velocity Verlet integrator (symplectic, 2nd order)
  fn step_velocity_verlet(self, dt)
    let accels_old = self.compute_accelerations()

    # Update positions: x(t+dt) = x(t) + v(t)*dt + 0.5*a(t)*dt^2
    for i in range(len(self.particles)):
      let p = self.particles[i]
      let a = accels_old[i]
      p.pos = p.pos.add(p.vel.scale(dt)).add(a.scale(0.5 * dt * dt))

    # Clear forces, recompute at new positions
    for p in self.particles:
      p.force = Vec2(0, 0)
    self.compute_all_forces()

    let accels_new = self.compute_accelerations()

    # Update velocities: v(t+dt) = v(t) + 0.5*(a(t) + a(t+dt))*dt
    for i in range(len(self.particles)):
      let p = self.particles[i]
      let a_avg = accels_old[i].add(accels_new[i]).scale(0.5)
      p.vel = p.vel.add(a_avg.scale(dt))

    self.resolve_collisions()
    self.enforce_bounds()
    self.time = self.time + dt
    self.steps = self.steps + 1

  # Leapfrog integrator (symplectic, 2nd order)
  fn step_leapfrog(self, dt)
    # Kick: v(t+dt/2) = v(t) + a(t)*dt/2
    let accels = self.compute_accelerations()
    for i in range(len(self.particles)):
      let p = self.particles[i]
      let a = accels[i]
      p.vel = p.vel.add(a.scale(dt * 0.5))

    # Drift: x(t+dt) = x(t) + v(t+dt/2)*dt
    for p in self.particles:
      p.pos = p.pos.add(p.vel.scale(dt))

    # Clear forces, recompute at new positions
    for p in self.particles:
      p.force = Vec2(0, 0)
    self.compute_all_forces()

    # Kick: v(t+dt) = v(t+dt/2) + a(t+dt)*dt/2
    let accels_new = self.compute_accelerations()
    for i in range(len(self.particles)):
      let p = self.particles[i]
      let a = accels_new[i]
      p.vel = p.vel.add(a.scale(dt * 0.5))

    self.resolve_collisions()
    self.enforce_bounds()
    self.time = self.time + dt
    self.steps = self.steps + 1

  # Adaptive time-stepping based on force magnitude
  fn compute_adaptive_dt(self, dt)
    if not self.adaptive_dt:
      ret dt
    let max_force = 0.0
    for p in self.particles:
      let f = p.force.length()
      if f > max_force:
        max_force = f
    if max_force < self.force_threshold:
      ret dt
    let scale = self.force_threshold / max_force
    let new_dt = dt * scale
    if new_dt < self.dt_min:
      new_dt = self.dt_min
    if new_dt > self.dt_max:
      new_dt = self.dt_max
    ret new_dt

  fn step(self, dt)
    let adaptive_dt = self.compute_adaptive_dt(dt)
    if self.integrator == "velocity_verlet":
      self.step_velocity_verlet(adaptive_dt)
    el:
      if self.integrator == "leapfrog":
        self.step_leapfrog(adaptive_dt)
      el:
        # Original Euler integrator
        self.apply_global_forces()
        self.apply_gravity_forces()
        for p in self.particles:
          p.step(adaptive_dt)
        self.resolve_collisions()
        self.enforce_bounds()
        self.time = self.time + adaptive_dt
        self.steps = self.steps + 1

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
    say("  integrator: " + self.integrator)
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