# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Porkchop: Porkchop plot generator for launch windows
# C3 contours, departure/arrival dates, multi-body trajectories
# ═══════════════════════════════════════════════════════════════════

import "orbital_mechanics.zap"
import "visualize.zap"

# ── Porkchop Plot Generator ──
# Computes C3 (characteristic energy) for departure/arrival date pairs

class PorkchopPlot:
  fn init(self, origin, destination, mu_origin, mu_dest, r_origin, r_dest)
    self.origin = origin
    self.destination = destination
    self.mu_origin = mu_origin
    self.mu_dest = mu_dest
    self.r_origin = r_origin
    self.r_dest = r_dest

  # Compute C3 for a given transfer
  # Returns [departure_C3, arrival_C3, transfer_time, total_dV]
  fn compute_transfer(self, t_depart, t_arrive)
    # Simplified: assume circular coplanar orbits
    # In reality, need full ephemeris
    let a_transfer = (self.r_origin + self.r_dest) / 2
    let v_depart = sqrt(self.mu_origin * (2 / self.r_origin - 1 / a_transfer))
    let v_circ_origin = sqrt(self.mu_origin / self.r_origin)
    let dv_depart = abs(v_depart - v_circ_origin)
    let c3_depart = dv_depart * dv_depart

    let v_arrive = sqrt(self.mu_dest * (2 / self.r_dest - 1 / a_transfer))
    let v_circ_dest = sqrt(self.mu_dest / self.r_dest)
    let dv_arrive = abs(v_arrive - v_circ_dest)
    let c3_arrive = dv_arrive * dv_arrive

    let transfer_time = 3.14159265 * sqrt(a_transfer * a_transfer * a_transfer / self.mu_origin)
    let total_dv = dv_depart + dv_arrive

    [c3_depart, c3_arrive, transfer_time, total_dv]

  # Generate porkchop data grid
  fn generate(self, depart_start, depart_end, arrive_start, arrive_end, n_depart, n_arrive)
    let depart_step = (depart_end - depart_start) / (n_depart - 1)
    let arrive_step = (arrive_end - arrive_start) / (n_arrive - 1)

    let data = []
    let depart_idx = 0
    let t_dep = depart_start
    while t_dep <= depart_end + depart_step * 0.1:
      let row = []
      let arrive_idx = 0
      let t_arr = arrive_start
      while t_arr <= arrive_end + arrive_step * 0.1:
        let result = self.compute_transfer(t_dep, t_arr)
        row = row + [result]
        t_arr = t_arr + arrive_step
        arrive_idx = arrive_idx + 1
      data = data + [row]
      t_dep = t_dep + depart_step
      depart_idx = depart_idx + 1
    data

  # Find optimal launch window (minimum C3)
  fn find_optimal(self, data)
    let min_c3 = 999999
    let best = nil
    for i in range(len(data)):
      for j in range(len(data[i])):
        let c3_dep = data[i][j][0]
        let c3_arr = data[i][j][1]
        let total_c3 = c3_dep + c3_arr
        if total_c3 < min_c3:
          min_c3 = total_c3
          best = {"depart_idx": i, "arrive_idx": j, "c3_depart": c3_dep, "c3_arrive": c3_arr, "transfer_time": data[i][j][2], "total_dv": data[i][j][3], "total_c3": min_c3}
    best

# ── Lambert-based Porkchop (more accurate) ──
# Uses actual Lambert solver for each date pair

fn porkchop_lambert(origin_body, dest_body, mu_origin, mu_dest, r_origin, r_dest, depart_dates, arrive_dates)
  let results = []
  for t_dep in depart_dates:
    let row = []
    for t_arr in arrive_dates:
      let tof = t_arr - t_dep
      if tof > 0:
        # Compute positions at those times (simplified circular orbits)
        let theta_origin = 3.14159265 * 2 * t_dep / 365.25
        let theta_dest = 3.14159265 * 2 * t_arr / 365.25
        let pos1 = Vec3(r_origin * cos(theta_origin), r_origin * sin(theta_origin), 0)
        let pos2 = Vec3(r_dest * cos(theta_dest), r_dest * sin(theta_dest), 0)
        let lambert = lambert_universal(pos1, pos2, tof, mu_origin, 0)
        if lambert != nil:
          let v1 = lambert[0]
          let v2 = lambert[1]
          let v_circ1 = sqrt(mu_origin / r_origin)
          let v_circ2 = sqrt(mu_dest / r_dest)
          let dv1 = v1.length() - v_circ1
          let dv2 = v_circ2 - v2.length()
          if dv1 < 0:
            dv1 = -dv1
          if dv2 < 0:
            dv2 = -dv2
          let c3_1 = dv1 * dv1
          let c3_2 = dv2 * dv2
          row = row + [{"c3_depart": c3_1, "c3_arrive": c3_2, "tof": tof, "total_dv": dv1 + dv2, "v1": v1, "v2": v2}]
        el:
          row = row + [nil]
      el:
        row = row + [nil]
    results = results + [row]
  results

# ── Generate ASCII Porkchop Plot ──
fn ascii_porkchop(data, depart_dates, arrive_dates, c3_contours)
  let n_rows = len(data)
  let n_cols = 0
  if n_rows > 0:
    n_cols = len(data[0])
  el:
    n_cols = 0
  say("=== PORKCHOP PLOT: C3 Contours ===")
  say("  X: Arrival Date | Y: Departure Date | Values: C3 (km^2/s^2)")
  say("")
  # Header
  let header = "     "
  for j in range(n_cols):
    let date = arrive_dates[j]
    header = header + str(int(date)) + " "
  say(header)
  for i in range(n_rows):
    let line = str(int(depart_dates[i])) + " |"
    for j in range(n_cols):
      let cell = data[i][j]
      if cell != nil:
        let c3 = 0
        if cell["total_c3"] != nil:
          c3 = cell["total_c3"]
        el:
          c3 = cell["c3_depart"] + cell["c3_arrive"]
        let char = "."
        for k in range(len(c3_contours)):
          if c3 <= c3_contours[k]:
            char = str(k)
            break
        line = line + char
      el:
        line = line + " "
    say(line)
  say("")
  say("Contours (C3 km^2/s^2):")
  for k in range(len(c3_contours)):
    say("  " + str(k) + ": <= " + str(c3_contours[k]))

# ── Multi-body Trajectory Designer ──
class TrajectoryDesigner:
  fn init(self)
    self.legs = []

  fn add_leg(self, origin, destination, depart_date, arrive_date)
    self.legs = self.legs + [{"origin": origin, "destination": destination, "depart": depart_date, "arrive": arrive_date}]

  fn compute_total_dv(self)
    let total = 0
    for leg in self.legs:
      # Simplified: would use Lambert solver
      total = total + 3000  # placeholder
    total

  fn summary(self)
    say("=== TRAJECTORY DESIGN ===")
    for leg in self.legs:
      say("  " + leg["origin"] + " -> " + leg["destination"] + " @ " + str(leg["depart"]) + " to " + str(leg["arrive"]))
    say("  Estimated total dV: " + str(self.compute_total_dv()) + " m/s")

# ── Launch Window Calculator ──
fn launch_window(origin, destination, year_start, year_end, step_days)
  say("=== LAUNCH WINDOWS: " + origin + " -> " + destination + " ===")
  say("  Year range: " + str(year_start) + " - " + str(year_end))
  say("  Step: " + str(step_days) + " days")
  say("")

  let windows = []
  let t = year_start * 365.25
  let t_end = year_end * 365.25

  while t <= t_end:
    # Synodic period approximation
    let t_arr = t + 260  # ~8.5 months for Earth-Mars
    let porkchop = PorkchopPlot(origin, destination, mu_earth(), mu_mars(), 1.496e11, 2.279e11)
    let result = porkchop.compute_transfer(t, t_arr)
    if result[3] < 6000:  # dV < 6 km/s
      windows = windows + [{"depart": t, "arrive": t_arr, "c3_depart": result[0], "c3_arrive": result[1], "dV": result[3]}]
    t = t + step_days

  for w in windows:
    let dep_year = int(w["depart"] / 365.25)
    let dep_day = int(w["depart"] % 365.25)
    let arr_year = int(w["arrive"] / 365.25)
    let arr_day = int(w["arrive"] % 365.25)
    say("  Depart: " + str(dep_year) + "-" + str(dep_day) + " | Arrive: " + str(arr_year) + "-" + str(arr_day) + " | C3: " + str(round(w["c3_depart"], 1)) + " | dV: " + str(round(w["dV"], 0)) + " m/s")
  
  say("  Total windows found: " + str(len(windows)))