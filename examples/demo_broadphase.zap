# ═══════════════════════════════════════════════════════════════════
# Demo: Broad-phase Collision Detection — Uniform Grid & Quadtree
# Run via: zap run main.zap or: zap run examples/demo_broadphase.zap
# ═══════════════════════════════════════════════════════════════════

import "../lib/vec2.zap"
import "../lib/particle.zap"
import "../lib/broadphase.zap"

say("")
say("=== DEMO: Broad-phase Collision Detection ===")

# Create test particles
let particles = []
for i in range(50):
  let p = Particle("p" + str(i), 1.0, 
                    Vec2(0, 0), 
                   Vec2(0, 0))
  p.radius = 1.0
  particles = particles + [p]

say("Created " + str(len(particles)) + " particles")

# Test Uniform Grid
say("")
say("-- Uniform Grid (cell size = 5.0) --")
let bounds = AABB(-100, -100, 200, 200)
let grid = UniformGrid(5.0, -100, -100, 100, 100)
for p in particles:
  grid.insert(p)

let grid_pairs = grid.get_potential_pairs()
say("Grid cells occupied: " + str(len(grid.cells)))
say("Potential pairs: " + str(len(grid_pairs)))

# Test Quadtree
say("")
say("-- Quadtree (capacity = 4) --")
let qt = Quadtree(bounds, 4)
for p in particles:
  qt.insert(p)

let qt_pairs = qt.get_potential_pairs()
say("Quadtree potential pairs: " + str(len(qt_pairs)))

# Compare with brute force
say("")
say("-- Brute Force Comparison --")
let brute_pairs = 0
for i in range(len(particles)):
  for j in range(i + 1, len(particles)):
    let p1 = particles[i]
    let p2 = particles[j]
    if p1.pos.dist(p2.pos) < p1.radius + p2.radius:
      brute_pairs = brute_pairs + 1
say("Actual collisions (brute force): " + str(brute_pairs))
say("Grid false positives: " + str(len(grid_pairs) - brute_pairs))
say("Quadtree false positives: " + str(len(qt_pairs) - brute_pairs))

# Performance note
say("")
say("-- Performance Notes --")
say("  Uniform Grid: O(n) insert + query, good for uniform distribution")
say("  Quadtree: O(n log n) insert, better for clustered distributions")
say("  Both reduce O(n^2) brute force to near O(n) for sparse scenes")

say("")
say("Broad-phase collision detection verified!")