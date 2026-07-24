# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Visual: ASCII visualization output
# ═══════════════════════════════════════════════════════════════════

# Render particles to an ASCII grid
fn ascii_render_particles(particles, width, height, x_min, x_max, y_min, y_max)
  let grid = []
  for r in range(height):
    let row = ""
    for c in range(width):
      row = row + "."
    grid = grid + [row]

  for p in particles:
    let px = 0
    if x_max > x_min:
      px = (p.pos.x - x_min) / (x_max - x_min) * (width - 1)
    let py = 0
    if y_max > y_min:
      py = (p.pos.y - y_min) / (y_max - y_min) * (height - 1)
    let ix = int(px)
    let iy = int(height - 1 - py)
    if ix >= 0 and ix < width and iy >= 0 and iy < height:
      let row = grid[iy]
      let new_row = ""
      for k in range(len(row)):
        if k == ix:
          new_row = new_row + "#"
        el:
          new_row = new_row + row[k]
      grid[iy] = new_row

  for r in range(height):
    say("  " + grid[r])

# Render a heat map from density values
fn ascii_heatmap(values, width, height)
  let chars = " .:-=+*#%@"
  let n = len(chars) - 1
  let max_val = 0
  for v in values:
    if v > max_val:
      max_val = v

  for r in range(height):
    let row = ""
    for c in range(width):
      let idx = r * width + c
      if idx < len(values):
        let normalized = 0
        if max_val > 0:
          normalized = values[idx] / max_val
        let ci = normalized * n
        if ci >= len(chars):
          ci = len(chars) - 1
        let ci_int = int(ci)
        if ci_int < 0:
          ci_int = 0
        row = row + chars[ci_int]
      el:
        row = row + " "
    say("  " + row)

# Render a bar chart in ASCII
fn ascii_bar_chart(values, labels, max_width)
  let max_val = 0
  for v in values:
    if v > max_val:
      max_val = v

  for i in range(len(values)):
    let label = ""
    if i < len(labels):
      label = labels[i]
    el:
      label = str(i)
    let bar_len = 0
    if max_val > 0:
      bar_len = values[i] / max_val * max_width
    let bar_len_int = int(bar_len)
    let bar = ""
    for j in range(bar_len_int):
      bar = bar + "#"
    say("  " + label + " | " + bar + " " + str(round(values[i], 2)))

# Render a sparkline
fn ascii_sparkline(values)
  let chars = " _.-=:!|%&#@"
  let n = len(chars) - 1
  let max_val = 0
  let min_val = 999999
  for v in values:
    if v > max_val:
      max_val = v
    if v < min_val:
      min_val = v
  let range = max_val - min_val
  let line = ""
  for v in values:
    let normalized = 0
    if range > 0:
      normalized = (v - min_val) / range
    let ci = normalized * n
    if ci >= len(chars):
      ci = len(chars) - 1
    let ci_int = int(ci)
    if ci_int < 0:
      ci_int = 0
    line = line + chars[ci_int]
  line

# Render 2D vector field
fn ascii_vector_field(field_fn, width, height, x_min, x_max, y_min, y_max)
  let arrows = " .oO@*+x#"
  for r in range(height):
    let row = ""
    for c in range(width):
      let x = x_min + (x_max - x_min) * c / (width - 1)
      let y = y_min + (y_max - y_min) * (height - 1 - r) / (height - 1)
      let fx = field_fn(x, y, 0)
      let fy = field_fn(x, y, 1)
      let mag = sqrt(fx * fx + fy * fy)
      let ci = mag * 2
      if ci >= len(arrows):
        ci = len(arrows) - 1
    let ci_int = int(ci)
    if ci_int < 0:
      ci_int = 0
    row = row + arrows[ci_int]
    say("  " + row)

# Box drawing for diagrams
fn ascii_box(x, y, w, h)
  let top = "+"
  for i in range(w):
    top = top + "-"
  top = top + "+"
  say(top)
  for r in range(h):
    let line = "|"
    for c in range(w):
      line = line + " "
    line = line + "|"
    say(line)
  let bottom = "+"
  for i in range(w):
    bottom = bottom + "-"
  bottom = bottom + "+"
  say(bottom)
