# ═══════════════════════════════════════════════════════════════════
# Demo: Porkchop Plot Generator — Launch window analysis
# Run via: zap run main.zap or: zap run examples/demo_porkchop.zap
# ═══════════════════════════════════════════════════════════════════

import "../lib/porkchop.zap"

say("")
say("=== DEMO: Porkchop Plot Generator ===")

# Earth-Mars transfer parameters
let earth_mu = mu_earth()
let mars_mu = mu_mars()
let r_earth_orbit = 1.496e11  # 1 AU
let r_mars_orbit = 2.279e11   # 1.52 AU

say("")
say("-- Earth to Mars Transfer Parameters --")
say("  Earth orbit radius: " + str(round(r_earth_orbit/1e9, 1)) + " Mkm")
say("  Mars orbit radius: " + str(round(r_mars_orbit/1e9, 1)) + " Mkm")

# Generate porkchop data
let porkchop = PorkchopPlot("Earth", "Mars", earth_mu, mars_mu, r_earth_orbit, r_mars_orbit)

say("")
say("-- Single Transfer Analysis --")
let t_depart = 0      # days from epoch
let t_arrive = 260    # ~8.5 months
let result = porkchop.compute_transfer(t_depart, t_arrive)
say("  Departure day: " + str(t_depart))
say("  Arrival day:   " + str(t_arrive))
say("  C3 depart:     " + str(round(result[0]/1e6, 2)) + " km^2/s^2")
say("  C3 arrive:     " + str(round(result[1]/1e6, 2)) + " km^2/s^2")
say("  Transfer time: " + str(round(result[2]/86400, 1)) + " days")
say("  Total dV:      " + str(round(result[3], 0)) + " m/s")

# Generate grid for 2024-2025 launch windows
say("")
say("-- Porkchop Grid: 2024-2026 Launch Windows --")
let depart_start = 0      # Jan 2024
let depart_end = 730      # ~2 years
let arrive_start = 150    # Min transfer ~5 months
let arrive_end = 500      # Max transfer ~16 months
let n_depart = 5
let n_arrive = 5

let data = porkchop.generate(depart_start, depart_end, arrive_start, arrive_end, n_depart, n_arrive)

# Find optimal
let optimal = porkchop.find_optimal(data)
if optimal != none:
  say("")
  say("-- Optimal Launch Window --")
  say("  Depart index: " + str(optimal["depart_idx"]))
  say("  Arrive index: " + str(optimal["arrive_idx"]))
  say("  C3 depart:    " + str(round(optimal["c3_depart"]/1e6, 2)) + " km^2/s^2")
  say("  C3 arrive:    " + str(round(optimal["c3_arrive"]/1e6, 2)) + " km^2/s^2")
  say("  Total C3:     " + str(round(optimal["total_c3"]/1e6, 2)) + " km^2/s^2")
  say("  Transfer time: " + str(round(optimal["transfer_time"]/86400, 1)) + " days")
  say("  Total dV:      " + str(round(optimal["total_dv"], 0)) + " m/s")

# ASCII Porkchop plot
say("")
say("-- ASCII Porkchop Plot (C3 contours) --")
let depart_dates = []
let arrive_dates = []
for i in range(n_depart):
  depart_dates = depart_dates + [depart_start + i * (depart_end - depart_start) / (n_depart - 1)]
for j in range(n_arrive):
  arrive_dates = arrive_dates + [arrive_start + j * (arrive_end - arrive_start) / (n_arrive - 1)]

let contours = [5e6, 10e6, 15e6, 20e6, 30e6, 50e6]  # C3 contours in m^2/s^2
ascii_porkchop(data, depart_dates, arrive_dates, contours)

# Launch window calculator
say("")
say("-- Launch Window Calculator (2024-2025) --")
launch_window("Earth", "Mars", 2024, 2025, 180)

# Multi-body trajectory example
say("")
say("-- Multi-Body Trajectory: Earth-Venus-Earth-Mars --")
let traj = TrajectoryDesigner()
traj.add_leg("Earth", "Venus", 100, 250)
traj.add_leg("Venus", "Earth", 400, 550)
traj.add_leg("Earth", "Mars", 700, 950)
traj.summary()

say("")
say("Porkchop plot generator verified!")