# ═══════════════════════════════════════════════════════════════════
# Demo: Tensor N-body — Force matrix using Zap tensors
# Run via: zap run main.zap (imports all libs + examples)
# ═══════════════════════════════════════════════════════════════════

say("")
say("=== DEMO: Tensor N-body Force Matrix ===")

let positions = tensor([0, 0, 10, 0, 0, 10, -5, -5], [4, 2])
let masses = tensor([100, 1, 2, 0.5], [4, 1])

say("  positions: " + str(positions))
say("  masses: " + str(masses))

say("")
say("  Pairwise distance matrix:")
let n = 4
for i in range(n):
  let row = ""
  for j in range(n):
    let dx = positions.data[i][0] - positions.data[j][0]
    let dy = positions.data[i][1] - positions.data[j][1]
    let dist = sqrt(dx * dx + dy * dy)
    row = row + str(round(dist, 2)) + "  "
  say("    " + row)

say("")
say("  Gravitational force matrix (G=50):")
let G_val = 50
for i in range(n):
  let row = ""
  for j in range(n):
    if i == j:
      row = row + "  0.00  "
    el:
      let dx = positions.data[j][0] - positions.data[i][0]
      let dy = positions.data[j][1] - positions.data[i][1]
      let dist = sqrt(dx * dx + dy * dy)
      let force = G_val * masses.data[i][0] * masses.data[j][0] / max(dist * dist, 0.01)
      row = row + str(round(force, 2)) + "  "
  say("    " + row)

say("")
say("  Tensor operations enable fast N-body calculations!")
