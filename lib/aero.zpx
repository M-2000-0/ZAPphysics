# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Aero: Aerodynamics & flight mechanics
# Lift, drag, airfoil analysis, flight performance
# ═══════════════════════════════════════════════════════════════════

# ── Airfoil ──
class Airfoil:
  fn init(self, name, cl_max, cd0, ar, efficiency)
    self.name = name
    self.cl_max = cl_max
    self.cd0 = cd0
    self.ar = ar
    self.efficiency = efficiency

  fn cl_at_alpha(self, alpha_deg)
    let alpha_rad = alpha_deg * 3.14159265 / 180
    let cl_alpha = 2 * 3.14159265
    let cl = cl_alpha * alpha_rad
    if cl > self.cl_max:
      cl = self.cl_max
    if cl < -self.cl_max:
      cl = -self.cl_max
    cl

  fn cd_at_cl(self, cl)
    self.cd0 + (cl * cl) / (3.14159265 * self.ar * self.efficiency)

  fn stall_angle(self)
    self.cl_max / (2 * 3.14159265) * 180 / 3.14159265

  fn repr(self)
    self.name + " (Cl_max=" + str(self.cl_max) + ", AR=" + str(self.ar) + ")"

# ── Airplane ──
class Airplane:
  fn init(self, name, mass, wing_area, wing_span, airfoil)
    self.name = name
    self.mass = mass
    self.s = wing_area
    self.b = wing_span
    self.airfoil = airfoil
    self.rho = 1.225
    self.g = 9.80665

  fn weight(self)
    self.mass * self.g

  fn wing_loading(self)
    self.weight() / self.s

  fn aspect_ratio(self)
    self.b * self.b / self.s

  fn lift(self, v, altitude)
    let rho = self.air_density(altitude)
    0.5 * rho * v * v * self.s * self.airfoil.cl_at_alpha(5)

  fn level_flight_speed(self, altitude)
    let rho = self.air_density(altitude)
    sqrt(2 * self.weight() / (rho * self.s * 0.5))

  fn stall_speed(self, altitude)
    let rho = self.air_density(altitude)
    sqrt(2 * self.weight() / (rho * self.s * self.airfoil.cl_max))

  fn drag(self, v, altitude)
    let rho = self.air_density(altitude)
    let cl = 2 * self.weight() / (rho * v * v * self.s)
    let cd = self.airfoil.cd_at_cl(cl)
    0.5 * rho * v * v * self.s * cd

  fn best_glide_speed(self, altitude)
    let rho = self.air_density(altitude)
    let cl = sqrt(self.airfoil.cd0 / (self.airfoil.cd0 * 3.14159265 * self.airfoil.ar * self.airfoil.efficiency))
    sqrt(2 * self.weight() / (rho * self.s * cl))

  fn best_glide_ratio(self)
    0.5 * sqrt(3.14159265 * self.airfoil.ar * self.airfoil.efficiency / self.airfoil.cd0)

  fn rate_of_climb(self, v, altitude, thrust)
    let drag = self.drag(v, altitude)
    let excess_thrust = thrust - drag
    excess_thrust * v / self.weight()

  fn air_density(self, altitude)
    let temp = 288.15 - 0.0065 * altitude
    let pressure = 101325 * (temp / 288.15) * (temp / 288.15) * (temp / 288.15) * (temp / 288.15) * (temp / 288.15)
    pressure / (287.05 * temp)

  fn simulate(self, thrust, dt, max_time, initial_altitude, initial_speed)
    let results = []
    let t = 0
    let alt = initial_altitude
    let v = initial_speed
    let angle = 5 * 3.14159265 / 180

    while t < max_time and alt > 0:
      let rho = self.air_density(alt)
      let alpha_deg = angle * 180 / 3.14159265
      let cl = self.airfoil.cl_at_alpha(alpha_deg)
      let lift = 0.5 * rho * v * v * self.s * cl
      let cd = self.airfoil.cd_at_cl(cl)
      let drag = 0.5 * rho * v * v * self.s * cd

      let weight = self.weight()
      let excess_thrust = thrust - drag
      let accel = (excess_thrust - weight * sin(angle)) / (weight / self.g)

      v = v + accel * dt
      alt = alt + v * sin(angle) * dt

      if lift < weight:
        angle = angle - 0.001
      el:
        angle = angle + 0.0005

      if angle < 0.01:
        angle = 0.01

      results = results + [{"time": t, "altitude": alt, "velocity": v, "alpha": angle, "lift": lift, "drag": drag}]
      t = t + dt

    results

  fn summary(self)
    say("=== AIRPLANE: " + self.name + " ===")
    say("  Mass: " + str(round(self.mass, 1)) + " kg")
    say("  Wing area: " + str(self.s) + " m^2")
    say("  Wing span: " + str(self.b) + " m")
    say("  Wing loading: " + str(round(self.wing_loading(), 1)) + " N/m^2")
    say("  Aspect ratio: " + str(round(self.aspect_ratio(), 1)))
    say("  Best glide ratio: " + str(round(self.best_glide_ratio(), 1)) + ":1")
    say("  Stall speed (SL): " + str(round(self.stall_speed(0), 1)) + " m/s")
    say("  Best glide speed (SL): " + str(round(self.best_glide_speed(0), 1)) + " m/s")
    say("")

# ── Common Airfoils ──
fn naca_2412()
  Airfoil("NACA 2412", 1.4, 0.0052, 7.5, 0.8)

fn naca_0012()
  Airfoil("NACA 0012", 1.3, 0.005, 6.0, 0.85)

fn clark_y()
  Airfoil("Clark Y", 1.4, 0.0055, 8.0, 0.82)

fn wf_116()
  Airfoil("Wortmann FX 60-153", 1.5, 0.006, 8.5, 0.8)

# ── Common Aircraft ──
fn cessna_172()
  let plane = Airplane("Cessna 172", 1230, 16.2, 11.0, naca_2412())
  plane

fn boeing_737()
  let plane = Airplane("Boeing 737", 62000, 125, 35.8, clark_y())
  plane

fn f16()
  let plane = Airplane("F-16 Fighting Falcon", 8300, 27.9, 10.7, naca_0012())
  plane

# ── Aerodynamic Functions ──
fn reynolds_number(rho, v, chord, mu)
  rho * v * chord / mu

fn mach_number(v, alt)
  let a = 340.3 * sqrt(1 - 0.0065 * alt / 288.15)
  v / a

fn dynamic_pressure(rho, v)
  0.5 * rho * v * v

fn lift_to_drag(cl, cd)
  if cd > 0:
    cl / cd
  el:
    0

fn induced_drag(cl, ar, e)
  cl * cl / (3.14159265 * ar * e)

fn parasite_drag(cd0, rho, v, s)
  cd0 * 0.5 * rho * v * v * s