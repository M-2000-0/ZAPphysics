# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Rocket: Rocket propulsion & vehicle design
# Tsiolkovsky equation, multi-stage analysis, thrust curves
# ═══════════════════════════════════════════════════════════════════

# ── Rocket Engine ──
class RocketEngine:
  fn init(self, name, isp, thrust, burn_time)
    self.name = name
    self.isp = isp
    self.thrust = thrust
    self.burn_time = burn_time
    self.g0 = 9.80665

  fn mass_flow_rate(self)
    self.thrust / (self.isp * self.g0)

  fn total_impulse(self)
    self.thrust * self.burn_time

  fn total_propellant(self)
    self.mass_flow_rate() * self.burn_time

  fn repr(self)
    self.name + " (Isp=" + str(self.isp) + "s, Thrust=" + str(self.thrust) + "N, burn=" + str(self.burn_time) + "s)"

# ── Rocket Stage ──
class RocketStage:
  fn init(self, name, engine, propellant_mass, dry_mass)
    self.name = name
    self.engine = engine
    self.propellant_mass = propellant_mass
    self.dry_mass = dry_mass
    self.color = "#e94560"

  fn total_mass(self)
    self.propellant_mass + self.dry_mass

  fn mass_ratio(self)
    self.total_mass() / self.dry_mass

  fn delta_v(self)
    self.engine.isp * self.engine.g0 * log(self.mass_ratio())

  fn burn_time(self)
    self.engine.burn_time

  fn repr(self)
    self.name + ": mass=" + str(self.total_mass()) + "kg, dV=" + str(round(self.delta_v(), 1)) + "m/s"

# ── Rocket Vehicle ──
class Rocket:
  fn init(self, name)
    self.name = name
    self.stages = []
    self.payload = 0
    self.g0 = 9.80665

  fn add_stage(self, stage)
    self.stages = self.stages + [stage]

  fn set_payload(self, mass)
    self.payload = mass

  fn total_mass(self)
    let total = self.payload
    for s in self.stages:
      total = total + s.total_mass()
    total

  fn total_delta_v(self)
    let dv = 0
    for s in self.stages:
      dv = dv + s.delta_v()
    dv

  fn total_burn_time(self)
    let t = 0
    for s in self.stages:
      t = t + s.burn_time()
    t

  fn total_impulse(self)
    let ti = 0
    for s in self.stages:
      ti = ti + s.engine.total_impulse()
    ti

  fn tsiolkovsky_delta_v(self)
    self.total_delta_v()

  fn simulate(self, dt, max_time)
    let results = []
    let t = 0
    let altitude = 0
    let velocity = 0
    let mass = self.total_mass()
    let stage_idx = 0
    let current_stage = self.stages[0]
    let prop_remaining = current_stage.propellant_mass

    while t < max_time and stage_idx < len(self.stages):
      let thrust = current_stage.engine.thrust
      let mdot = current_stage.engine.mass_flow_rate()

      let gravity_loss = self.g0
      let drag_loss = 0.5 * 0.5 * 1.225 * 0.1 * velocity * velocity / mass

      let net_force = thrust - mass * gravity_loss - drag_loss * mass
      if net_force < 0:
        net_force = 0

      let accel = net_force / mass
      velocity = velocity + accel * dt
      altitude = altitude + velocity * dt

      if prop_remaining > 0:
        prop_remaining = prop_remaining - mdot * dt
        mass = mass - mdot * dt

      results = results + [{"time": t, "altitude": altitude, "velocity": velocity, "mass": mass, "thrust": thrust}]

      if prop_remaining <= 0:
        stage_idx = stage_idx + 1
        if stage_idx < len(self.stages):
          current_stage = self.stages[stage_idx]
          prop_remaining = current_stage.propellant_mass
          results = results + [{"time": t, "altitude": altitude, "velocity": velocity, "mass": mass, "thrust": 0}]

      t = t + dt

    results

  fn thrust_curve(self, dt)
    let results = []
    let t = 0
    for s in self.stages:
      let mdot = s.engine.mass_flow_rate()
      let steps = int(s.burn_time() / dt)
      for i in range(steps):
        results = results + [{"time": t, "thrust": s.engine.thrust, "mass_flow": mdot}]
        t = t + dt
      results = results + [{"time": t, "thrust": 0, "mass_flow": 0}]
    results

  fn summary(self)
    say("=== ROCKET: " + self.name + " ===")
    say("  Payload: " + str(self.payload) + " kg")
    say("  Total mass: " + str(round(self.total_mass(), 1)) + " kg")
    say("  Total delta-v: " + str(round(self.total_delta_v(), 1)) + " m/s")
    say("  Total burn time: " + str(round(self.total_burn_time(), 1)) + " s")
    say("  Total impulse: " + str(round(self.total_impulse(), 1)) + " Ns")
    say("")
    for s in self.stages:
      say("  Stage: " + s.name)
      say("    Engine: " + s.engine.name)
      say("    Isp: " + str(s.engine.isp) + " s")
      say("    Thrust: " + str(s.engine.thrust) + " N")
      say("    Propellant: " + str(s.propellant_mass) + " kg")
      say("    Dry mass: " + str(s.dry_mass) + " kg")
      say("    Mass ratio: " + str(round(s.mass_ratio(), 2)))
      say("    Stage delta-v: " + str(round(s.delta_v(), 1)) + " m/s")
      say("")

# ── Common Rocket Engines ──
fn merlin_1d()
  RocketEngine("Merlin 1D", 311, 845100, 360)

fn raptor()
  RocketEngine("Raptor", 382, 2200000, 380)

fn f1()
  RocketEngine("F-1", 304, 6770000, 160)

fn rs_25()
  RocketEngine("RS-25", 452, 2279000, 512)

fn rutherford()
  RocketEngine("Rutherford", 311, 100000, 200)

# ── Rocket Equation (standalone) ──
fn rocket_equation(delta_v, isp)
  delta_v / (isp * 9.80665)

fn mass_ratio_from_delta_v(delta_v, isp)
  exp(delta_v / (isp * 9.80665))

fn propellant_fraction(delta_v, isp)
  let mr = mass_ratio_from_delta_v(delta_v, isp)
  1 - 1 / mr

fn payload_fraction(delta_v, isp)
  1 / mass_ratio_from_delta_v(delta_v, isp)