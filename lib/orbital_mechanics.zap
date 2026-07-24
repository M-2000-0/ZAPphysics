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
    say("  Transfer time: " + str(round(self.transfer_time(1.496e11, 2.279e11) / 86400, 1)) + " days")
    say("")

# ── Lambert Solver ──
# Solves Lambert's problem: find orbit connecting r1 -> r2 in time dt
# Returns: [dv1, dv2, a, e, theta1, theta2] or nil if no solution
fn lambert_solver(r1, r2, dt, mu, prograde)
  let r1_mag = r1.length()
  let r2_mag = r2.length()
  let cos_dtheta = r1.dot(r2) / (r1_mag * r2_mag)
  if cos_dtheta > 1:
    cos_dtheta = 1
  if cos_dtheta < -1:
    cos_dtheta = -1
  let dtheta = acos(cos_dtheta)
  if not prograde:
    dtheta = 2 * 3.14159265 - dtheta

  let c = sqrt(r1_mag * r1_mag + r2_mag * r2_mag - 2 * r1_mag * r2_mag * cos_dtheta)
  let s = (r1_mag + r2_mag + c) / 2

  # Initial guess for semi-major axis using minimum energy orbit
  let a_min = s / 2
  let n = sqrt(mu / (a_min * a_min * a_min))
  let t_min = 3.14159265 * sqrt(a_min * a_min * a_min / mu)

  if dt < t_min:
    ret nil

  # Universal variable approach - iterate on x
  let x = 0.0
  let tolerance = 1e-10
  let max_iter = 50

  for iter in range(max_iter):
    let z = x * x / a_min
    let s_z, c_z = stumpff(z)

    let y = r1_mag + r2_mag + (s_z - 1) / c_z * x * x
    let sqrt_y = sqrt(y)

    let t = (x**3 * s_z + sqrt_y * c_z * x) / sqrt(mu)
    
    if abs(t - dt) < tolerance:
      break

    # Newton-Raphson update
    let dt_dx = (x**2 * c_z + y) / sqrt(mu)
    x = x + (dt - t) / dt_dx

  let a = 1 / (2 / r1_mag - x**2 / y)
  let f = 1 - y / r1_mag
  let g = dt - x**3 * s_z / sqrt(mu)
  let fdot = sqrt(mu / (r1_mag * y)) * (z * s_z - 1) * x
  let gdot = 1 - y / r2_mag

  let v1 = r1.scale(1/g).sub(r2.scale(1/g)).scale(-1)  # Not exact but direction
  # Proper v1 calculation:
  let v1x = (r2.x - f * r1.x) / g
  let v1y = (r2.y - f * r1.y) / g
  let v1z = (r2.z - f * r1.z) / g
  let v1_vec = Vec3(v1x, v1y, v1z)
  
  let dv1 = v1_vec.length() - sqrt(mu / r1_mag)
  
  # Arrival velocity
  let v2x = (gdot * r2.x - r1.x) / g
  let v2y = (gdot * r2.y - r1.y) / g
  let v2z = (gdot * r2.z - r1.z) / g
  let v2_vec = Vec3(v2x, v2y, v2z)
  
  let dv2 = v2_vec.length() - sqrt(mu / r2_mag)

  [dv1, dv2, a, sqrt(1 - (c/a)**2), dtheta]

# Stumpff functions for universal variable formulation
fn stumpff(z)
  if z > 1e-10:
    let sqrt_z = sqrt(z)
    [(1 - cos(sqrt_z)) / z, (sqrt_z - sin(sqrt_z)) / (sqrt_z * z)]
  el:
    if z < -1e-10:
      let sqrt_nz = sqrt(-z)
      [(cosh(sqrt_nz) - 1) / (-z), (sinh(sqrt_nz) - sqrt_nz) / (sqrt_nz * (-z) * sqrt_nz)]
    el:
      [0.5, 1/6.0]

fn sinh(x) (exp(x) - exp(-x)) / 2
fn cosh(x) (exp(x) + exp(-x)) / 2

# Simple Lambert solver using universal variables (returns dv1, dv2, semi-major axis)
fn lambert(r1_vec, r2_vec, dt, mu, prograde)
  let r1 = r1_vec.length()
  let r2 = r2_vec.length()
  let cos_dnu = r1_vec.dot(r2_vec) / (r1 * r2)
  if cos_dnu > 1:
    cos_dnu = 1
  if cos_dnu < -1:
    cos_dnu = -1
  let dnu = acos(cos_dnu)
  if not prograde:
    dnu = 2 * 3.14159265 - dnu

  let chord = sqrt(r1*r1 + r2*r2 - 2*r1*r2*cos_dnu)
  let s = (r1 + r2 + chord) / 2

  # Minimum energy orbit
  let a_min = s / 2
  let t_min = 3.14159265 * sqrt(a_min * a_min * a_min / mu)
  
  if dt < t_min:
    ret nil

  # Use universal variable x
  let x = sqrt(mu) * dt / a_min  # initial guess
  
  for i in range(50):
    let z = x * x / a_min
    let sz, cz = stumpff(z)
    let y = r1 + r2 + (sz - 1)/cz * x * x
    if y < 0:
      y = 0
    let t = (x*x*x*sz + sqrt(y)*cz*x) / sqrt(mu)
    
    if abs(t - dt) < 1e-8:
      break
      
    let dtdx = (x*x*cz + y) / sqrt(mu)
    x = x + (dt - t) / dtdx

  let a = 1 / (2/r1 - x*x / (r1 + r2 + (sz - 1)/cz * x * x))
  let alpha = 1 / a
  let f = 1 - (x*x/cz) / r1
  let g = dt - x*x*x*sz / sqrt(mu)
  let v1_mag = sqrt(alpha * mu * (2/r1 - alpha))
  let v2_mag = sqrt(alpha * mu * (2/r2 - alpha))
  
  [v1_mag - sqrt(mu/r1), v2_mag - sqrt(mu/r2), a]