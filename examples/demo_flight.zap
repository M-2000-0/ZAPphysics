# ═══════════════════════════════════════════════════════════════════
# Demo: Flight Dynamics — Aircraft aerodynamics & performance
# Run via: zap run main.zap or: zap run examples/demo_flight.zap
# ═══════════════════════════════════════════════════════════════════

import "../lib/aero.zap"
import "../lib/flight.zap"

say("")
say("=== DEMO: Flight Dynamics ===")

# ── Design aircraft ──
let plane = cessna_172()

say("")
say("-- Aircraft Design --")
plane.summary()

# ── Flight envelope ──
let envelope = FlightEnvelope(plane)
envelope.compute(3000)
say("-- Flight Envelope --")
envelope.summary()

# ── Aerodynamic analysis ──
say("")
say("-- Aerodynamic Analysis at various speeds --")
say("  Speed (m/s) | Lift (N) | Drag (N) | L/D  | Cl   | Cd")
say("  " + "-" * 60)
for v in [30, 50, 70, 90, 110, 130]:
  let aero = plane.aerodynamics(v, 1000, 5)
  let lift = aero[0]
  let drag = aero[1]
  let cl = aero[2]
  let cd = aero[3]
  let ld = 0
  if drag > 0:
    ld = lift / drag
  say("  " + str(v) + "        | " + str(round(lift, 0)) + "   | " + str(round(drag, 1)) + "  | " + str(round(ld, 1)) + " | " + str(round(cl, 3)) + " | " + str(round(cd, 4)))

# ── Simulate flight ──
say("")
say("-- Simulating flight (takeoff to landing) --")
let dt = 0.1
let flight_data = plane.simulate(50000, dt, 120, 0, 40, 5)

# Print flight summary
say("  Simulated " + str(len(flight_data)) + " data points")
let max_alt = 0
let max_vel = 0
for d in flight_data:
  if d["altitude"] > max_alt:
    max_alt = d["altitude"]
  if d["velocity"] > max_vel:
    max_vel = d["velocity"]
say("  Max altitude: " + str(round(max_alt, 1)) + " m")
say("  Max velocity: " + str(round(max_vel, 1)) + " m/s")
if len(flight_data) > 0:
  say("  Final altitude: " + str(round(flight_data[len(flight_data) - 1]["altitude"], 1)) + " m")

# ── Airfoil comparison ──
say("")
say("-- Airfoil Comparison --")
let airfoils = [naca_2412(), naca_0012(), clark_y(), wf_116()]
for af in airfoils:
  say("  " + af.name + ": Cl_max=" + str(af.cl_max) + ", Cd0=" + str(af.cd0) + ", AR=" + str(af.ar) + ", stall=" + str(round(af.stall_angle(), 1)) + "deg")

# ── Aircraft comparison ──
say("")
say("-- Aircraft Comparison --")
let aircraft = [cessna_172(), boeing_737(), f16()]
for a in aircraft:
  say("  " + a.name + ": mass=" + str(a.mass) + "kg, wing=" + str(a.s) + "m^2, loading=" + str(round(a.wing_loading(), 0)) + "N/m^2, AR=" + str(round(a.aspect_ratio(), 1)))

say("")
say("Flight dynamics verified!")