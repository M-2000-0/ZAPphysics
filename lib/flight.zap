# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Flight: Flight dynamics & control
# Angle of attack, stability, control surfaces, flight envelopes
# ═══════════════════════════════════════════════════════════════════

# ── Control Surface ──
class ControlSurface:
  fn init(self, name, area, max_deflection, efficiency)
    self.name = name
    self.area = area
    self.max_deflection = max_deflection
    self.efficiency = efficiency
    self.deflection = 0

  fn set_deflection(self, angle_deg)
    if angle_deg > self.max_deflection:
      angle_deg = self.max_deflection
    if angle_deg < -self.max_deflection:
      angle_deg = -self.max_deflection
    self.deflection = angle_deg

  fn force(self, rho, v, chord)
    let dyn_q = 0.5 * rho * v * v
    let cl_per_deg = 0.1
    let cl = cl_per_deg * self.deflection * self.efficiency
    dyn_q * self.area * cl

  fn repr(self)
    self.name + " (area=" + str(self.area) + "m^2, max=" + str(self.max_deflection) + "deg)"

# ── Flight Vehicle ──
class FlightVehicle:
  fn init(self, name, mass, wing_area, wing_span, airfoil)
    self.name = name
    self.mass = mass
    self.s = wing_area
    self.b = wing_span
    self.cg = 0.25
    self.controls = []
    self.rho = 1.225
    self.g = 9.80665
    self.alpha = 0
    self.beta = 0
    self.p = 0
    self.q = 0
    self.r = 0
    self.phi = 0
    self.theta = 0
    self.psi = 0
    self.airfoil = airfoil

  fn add_control(self, control)
    self.controls = self.controls + [control]

  fn weight(self)
    self.mass * self.g

  fn wing_loading(self)
    self.weight() / self.s

  fn aspect_ratio(self)
    self.b * self.b / self.s

  fn aerodynamics(self, v, altitude, alpha_deg)
    let alpha = alpha_deg * 3.14159265 / 180
    let rho = self.air_density(altitude)
    let cl = 2 * 3.14159265 * alpha
    if cl > 1.5:
      cl = 1.5
    if cl < -1.5:
      cl = -1.5
    let cd0 = 0.005
    let cd = cd0 + cl * cl / (3.14159265 * self.aspect_ratio() * 0.8)
    let q = 0.5 * rho * v * v
    let lift = q * self.s * cl
    let drag = q * self.s * cd
    let control_force = 0
    for c in self.controls:
      control_force = control_force + c.force(rho, v, 1)
    [lift, drag, cl, cd, control_force]

  fn pitching_moment(self, alpha_deg, q)
    let alpha = alpha_deg * 3.14159265 / 180
    let cm_alpha = -1.0
    let cm_q = -5.0
    cm_alpha * alpha + cm_q * q

  fn static_margin(self, ac_position, cg_position)
    ac_position - cg_position

  fn stall_speed(self, altitude)
    let rho = self.air_density(altitude)
    sqrt(2 * self.weight() / (rho * self.s * self.airfoil.cl_max))

  fn air_density(self, altitude)
    let temp = 288.15 - 0.0065 * altitude
    let ratio = temp / 288.15
    let pressure = 101325 * ratio * ratio * ratio * ratio * ratio
    pressure / (287.05 * temp)

  fn simulate(self, thrust, dt, max_time, initial_altitude, initial_speed)
    let results = []
    let t = 0
    let alt = initial_altitude
    let v = initial_speed
    let angle = 5 * 3.14159265 / 180
    let q = 0

    while t < max_time and alt > 0:
      let rho = self.air_density(alt)
      let alpha_deg = angle * 180 / 3.14159265
      let aero = self.aerodynamics(v, alt, alpha_deg)
      let lift = aero[0]
      let drag = aero[1]
      let weight = self.weight()

      let gamma = angle
      let dq = self.pitching_moment(alpha_deg, q) * 0.1

      let dalpha = q - (weight * cos(gamma) - lift) / (weight * v) * v
      let dv = (lift * sin(gamma) - drag * cos(gamma) - weight * sin(gamma)) / (weight / self.g)
      let dalt = v * sin(gamma)

      angle = angle + dalpha * dt
      v = v + dv * dt
      q = q + dq * dt
      alt = alt + dalt * dt

      if angle > 15 * 3.14159265 / 180:
        angle = 15 * 3.14159265 / 180

      results = results + [{"time": t, "altitude": alt, "velocity": v, "alpha": angle, "theta": angle, "q": q, "lift": lift, "drag": drag}]
      t = t + dt

    results

  fn summary(self)
    say("=== FLIGHT VEHICLE: " + self.name + " ===")
    say("  Mass: " + str(round(self.mass, 1)) + " kg")
    say("  Wing area: " + str(self.s) + " m^2")
    say("  Wing span: " + str(self.b) + " m")
    say("  Wing loading: " + str(round(self.wing_loading(), 1)) + " N/m^2")
    say("  Aspect ratio: " + str(round(self.aspect_ratio(), 1)))
    say("  CG position: " + str(round(self.cg * 100, 1)) + "% chord")
    say("  Control surfaces: " + str(len(self.controls)))
    for c in self.controls:
      say("    " + c.name + " (area=" + str(c.area) + "m^2, max=" + str(c.max_deflection) + "deg)")
    say("")

# ── Common Aircraft ──
fn cessna_172()
  let plane = FlightVehicle("Cessna 172", 1230, 16.2, 11.0, naca_2412())
  plane.add_control(ControlSurface("Elevator", 1.5, 30, 0.8))
  plane.add_control(ControlSurface("Aileron", 2.0, 20, 0.7))
  plane.add_control(ControlSurface("Rudder", 1.2, 20, 0.6))
  plane

fn boeing_737()
  let plane = FlightVehicle("Boeing 737", 62000, 125, 35.8, clark_y())
  plane.add_control(ControlSurface("Elevator", 12, 30, 0.85))
  plane.add_control(ControlSurface("Aileron", 15, 20, 0.75))
  plane.add_control(ControlSurface("Rudder", 8, 20, 0.7))
  plane

fn f16()
  let plane = FlightVehicle("F-16 Fighting Falcon", 8300, 27.9, 10.7, naca_0012())
  plane.add_control(ControlSurface("Elevator", 3.5, 45, 0.9))
  plane.add_control(ControlSurface("Aileron", 4.0, 30, 0.85))
  plane.add_control(ControlSurface("Rudder", 2.5, 30, 0.8))
  plane

# ── Flight Envelope ──
class FlightEnvelope:
  fn init(self, vehicle)
    self.vehicle = vehicle
    self.v_never_exceed = 150
    self.v_stall = 0
    self.v_best_rate = 80
    self.v_best_glide = 70

  fn compute(self, max_altitude)
    self.v_stall = self.vehicle.stall_speed(0)

  fn summary(self)
    say("=== FLIGHT ENVELOPE ===")
    say("  V_S (stall): " + str(round(self.v_stall, 1)) + " m/s")
    say("  V_NE (never exceed): " + str(round(self.v_never_exceed, 1)) + " m/s")
    say("  V_Y (best rate): " + str(round(self.v_best_rate, 1)) + " m/s")
    say("  V_BG (best glide): " + str(round(self.v_best_glide, 1)) + " m/s")
    say("")

# ── Flight Data Point ──
class FlightDataPoint:
  fn init(self, time, altitude, velocity, alpha, theta, q, lift, drag)
    self.time = time
    self.altitude = altitude
    self.velocity = velocity
    self.alpha = alpha
    self.theta = theta
    self.q = q
    self.lift = lift
    self.drag = drag