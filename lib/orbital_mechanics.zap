# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Orbital: Orbital mechanics & astrodynamics
# Hohmann transfers, orbital elements, interplanetary trajectories
# ═══════════════════════════════════════════════════════════════════

# ── Orbital Elements ──
class OrbitalElements:
  fn init(self, a, e, inc, raan, argp, nu)
    self.a = a
    self.e = e
    self.inc = inc
    self.raan = raan
    self.argp = argp
    self.nu = nu

  fn period(self, mu)
    2 * 3.14159265 * sqrt(self.a * self.a * self.a / mu)

  fn apoapsis(self)
    self.a * (1 + self.e)

  fn periapsis(self)
    self.a * (1 - self.e)

  fn is_circular(self)
    self.e < 0.01

  fn is_elliptic(self)
    self.e < 1

  fn is_hyperbolic(self)
    self.e > 1

  fn repr(self)
    "a=" + str(round(self.a, 0)) + " e=" + str(round(self.e, 4)) + " T=" + str(round(self.period(3.986e14), 0)) + "s"

# ── Orbital Mechanics Functions ──

# Standard gravitational parameters (m^3/s^2)
fn mu_earth() 3.986004418e14
fn mu_sun() 1.32712440018e20
fn mu_moon() 4.9048698e12
fn mu_mars() 4.282837e13

# Hohmann transfer between two circular orbits
# Returns: [dv1, dv2, total_dv, transfer_time, a_transfer]
fn hohmann_transfer(r1, r2, mu)
  let a_transfer = (r1 + r2) / 2
  let dv1 = sqrt(mu / r1) * (sqrt(2 * r2 / (r1 + r2)) - 1)
  let dv2 = sqrt(mu / r2) * (1 - sqrt(2 * r1 / (r1 + r2)))
  let total_dv = abs(dv1) + abs(dv2)
  let transfer_time = 3.14159265 * sqrt(a_transfer * a_transfer * a_transfer / mu)
  [dv1, dv2, total_dv, transfer_time, a_transfer]

# Bi-elliptic transfer
# Returns: [dv1, dv2, dv3, total_dv]
fn bi_elliptic_transfer(r1, r2, r3, mu)
  let a1 = (r1 + r3) / 2
  let a2 = (r2 + r3) / 2
  let dv1 = sqrt(mu / r1) * (sqrt(2 * r3 / (r1 + r3)) - 1)
  let dv2 = sqrt(mu / r3) * (sqrt(2 * r2 / (r2 + r3)) - 1)
  let dv3 = sqrt(mu / r2) * (1 - sqrt(2 * r3 / (r2 + r3)))
  let total_dv = abs(dv1) + abs(dv2) + abs(dv3)
  [dv1, dv2, dv3, total_dv]

# Orbital velocity (circular)
fn orbital_velocity(r, mu)
  sqrt(mu / r)

# Escape velocity
fn escape_velocity(r, mu)
  sqrt(2 * mu / r)

# Vis-viva equation: v^2 = mu * (2/r - 1/a)
fn vis_viva(r, a, mu)
  sqrt(mu * (2 / r - 1 / a))

# Orbital period
fn orbital_period(a, mu)
  2 * 3.14159265 * sqrt(a * a * a / mu)

# Synodic period between two orbits
fn synodic_period(t1, t2)
  1 / abs(1 / t1 - 1 / t2)

# Rocket equation for delta-v calculation
fn delta_v(m0, mf, isp)
  isp * 9.80665 * log(m0 / mf)

# Required mass ratio for given delta-v
fn mass_ratio(dv, isp)
  exp(dv / (isp * 9.80665))

# Propellant fraction
fn propellant_fraction(dv, isp)
  let mr = mass_ratio(dv, isp)
  1 - 1 / mr

# Payload fraction
fn payload_fraction(dv, isp)
  1 / mass_ratio(dv, isp)

# Oberth effect: energy gain from burning at periapsis
fn oberth_effect(dv_burn, v_periapsis)
  v_periapsis * dv_burn

# Gravity assist delta-v
fn gravity_assist(v_inf, v_planet)
  2 * v_planet * v_inf / (v_planet + v_inf)

# ── Orbit Propagator ──
class OrbitPropagator:
  fn init(self, pos, vel, mu)
    self.pos = pos
    self.vel = vel
    self.mu = mu
    self.elements = self.compute_elements()

  fn compute_elements(self)
    let r = self.pos.length()
    let v = self.vel.length()
    let h = self.pos.cross(self.vel)
    let h_mag = h.length()
    let e_vec = self.vel.cross(h).scale(1 / self.mu).sub(self.pos.normalize())
    let e = e_vec.length()
    let energy = v * v / 2 - self.mu / r
    let a = -self.mu / (2 * energy)
    let inc = 0
    if h_mag > 1e-10:
      let cos_inc = h.z / h_mag
      if cos_inc > 1:
        cos_inc = 1
      if cos_inc < -1:
        cos_inc = -1
      inc = cos_inc
    OrbitalElements(a, e, inc, 0, 0, 0)

  fn energy(self)
    let r = self.pos.length()
    let v = self.vel.length()
    v * v / 2 - self.mu / r

  fn summary(self)
    say("=== ORBITAL ELEMENTS ===")
    say("  Semi-major axis: " + str(round(self.elements.a, 0)) + " m")
    say("  Eccentricity: " + str(round(self.elements.e, 6)))
    say("  Period: " + str(round(self.elements.period(self.mu), 0)) + " s (" + str(round(self.elements.period(self.mu) / 60, 1)) + " min)")
    say("  Apoapsis: " + str(round(self.elements.apoapsis(), 0)) + " m")
    say("  Periapsis: " + str(round(self.elements.periapsis(), 0)) + " m")
    say("")

# ── Interplanetary Transfer ──
class InterplanetaryTransfer:
  fn init(self, origin, destination, mu_origin, mu_dest)
    self.origin = origin
    self.destination = destination
    self.mu_origin = mu_origin
    self.mu_dest = mu_dest

  fn departure_dv(self, r_origin, r_dest)
    let v_transfer = sqrt(self.mu_origin * (2 / r_origin - 2 / (r_origin + r_dest)))
    abs(v_transfer - sqrt(self.mu_origin / r_origin))

  fn arrival_dv(self, r_dest)
    let v_capture = sqrt(self.mu_dest * (2 / r_dest - 2 / (r_dest + self.mu_origin)))
    abs(v_capture - sqrt(self.mu_dest / r_dest))

  fn total_dv(self, r_origin, r_dest)
    self.departure_dv(r_origin, r_dest) + self.arrival_dv(r_dest)

  fn transfer_time(self, r_origin, r_dest)
    let a = (r_origin + r_dest) / 2
    3.14159265 * sqrt(a * a * a / mu_sun())

  fn summary(self)
    say("=== INTERPLANETARY TRANSFER ===")
    say("  From: " + self.origin)
    say("  To: " + self.destination)
    say("")