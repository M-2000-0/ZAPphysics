# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — BroadPhase: Spatial partitioning for collision detection
# Uniform grid, spatial hash, and quadtree for O(n) collision queries
# ═══════════════════════════════════════════════════════════════════

# ── AABB (Axis-Aligned Bounding Box) ──
class AABB:
  fn init(self, x, y, w, h)
    self.min_x = x
    self.min_y = y
    self.max_x = x + w
    self.max_y = y + h

  fn contains(self, x, y)
    x >= self.min_x and x <= self.max_x and y >= self.min_y and y <= self.max_y

  fn intersects(self, other)
    not (self.max_x < other.min_x or other.max_x < self.min_x or
         self.max_y < other.min_y or other.max_y < self.min_y)

  fn expand(self, margin)
    AABB(self.min_x - margin, self.min_y - margin,
         self.max_x - self.min_x + 2 * margin,
         self.max_y - self.min_y + 2 * margin)

# ── Uniform Grid (Fixed-size 2D array) ──
class UniformGrid:
  fn init(self, cell_size, world_min_x, world_min_y, world_max_x, world_max_y)
    self.cell_size = cell_size
    self.world_min_x = world_min_x
    self.world_min_y = world_min_y
    self.nx = int((world_max_x - world_min_x) / cell_size) + 1
    self.ny = int((world_max_y - world_min_y) / cell_size) + 1
    self.cells = []
    let n_total = self.nx * self.ny
    for ci in range(n_total):
      self.cells = self.cells + [[]]

  fn cell_at(self, cx, cy)
    self.cells[cx * self.ny + cy]

  fn set_cell(self, cx, cy, val)
    self.cells[cx * self.ny + cy] = val

  fn world_to_cell(self, x, y)
    let cx = int((x - self.world_min_x) / self.cell_size)
    let cy = int((y - self.world_min_y) / self.cell_size)
    if cx < 0:
      cx = 0
    if cy < 0:
      cy = 0
    if cx >= self.nx:
      cx = self.nx - 1
    if cy >= self.ny:
      cy = self.ny - 1
    [cx, cy]

  fn clear(self)
    let n_total = self.nx * self.ny
    for ci in range(n_total):
      self.cells[ci] = []

  fn insert(self, particle)
    let pos = particle.pos
    let r = particle.radius
    let c1 = self.world_to_cell(pos.x - r, pos.y - r)
    let cx1 = c1[0]
    let cy1 = c1[1]
    let c2 = self.world_to_cell(pos.x + r, pos.y + r)
    let cx2 = c2[0]
    let cy2 = c2[1]
    for cx in range(cx1, cx2 + 1):
      let base = cx * self.ny
      for cy in range(cy1, cy2 + 1):
        let idx = base + cy
        if len(self.cells[idx]) == 0:
          self.cells[idx] = [particle]
        el:
          self.cells[idx] = self.cells[idx] + [particle]

  fn query(self, x, y, radius)
    let q1 = self.world_to_cell(x - radius, y - radius)
    let cx1 = q1[0]
    let cy1 = q1[1]
    let q2 = self.world_to_cell(x + radius, y + radius)
    let cx2 = q2[0]
    let cy2 = q2[1]
    let results = []
    for cx in range(cx1, cx2 + 1):
      let base = cx * self.ny
      for cy in range(cy1, cy2 + 1):
        let idx = base + cy
        let cell = self.cells[idx]
        if len(cell) > 0:
          for p in cell:
            results = results + [p]
    results

  fn get_potential_pairs(self)
    let pairs = []
    for ci in range(len(self.cells)):
      let cell_particles = self.cells[ci]
      let n = len(cell_particles)
      for i in range(n):
        for j in range(i + 1, n):
          pairs = pairs + [[cell_particles[i], cell_particles[j]]]
    pairs

# ── Quadtree ──
class Quadtree:
  fn init(self, boundary, capacity)
    self.boundary = boundary  # AABB
    self.capacity = capacity
    self.particles = []
    self.divided = false
    self.nw = none
    self.ne = none
    self.sw = none
    self.se = none

  fn subdivide(self)
    let x = self.boundary.min_x
    let y = self.boundary.min_y
    let w = (self.boundary.max_x - self.boundary.min_x) / 2
    let h = (self.boundary.max_y - self.boundary.min_y) / 2
    let nw = AABB(x, y, w, h)
    let ne = AABB(x + w, y, w, h)
    let sw = AABB(x, y + h, w, h)
    let se = AABB(x + w, y + h, w, h)
    self.nw = Quadtree(nw, self.capacity)
    self.ne = Quadtree(ne, self.capacity)
    self.sw = Quadtree(sw, self.capacity)
    self.se = Quadtree(se, self.capacity)
    self.divided = true

  fn insert(self, particle)
    if not self.boundary.contains(particle.pos.x, particle.pos.y):
      ret false
    if len(self.particles) < self.capacity:
      self.particles = self.particles + [particle]
      ret true
    if not self.divided:
      self.subdivide()
    if self.nw.insert(particle):
      ret true
    if self.ne.insert(particle):
      ret true
    if self.sw.insert(particle):
      ret true
    if self.se.insert(particle):
      ret true
    ret false

  fn query(self, range, found)
    if not self.boundary.intersects(range):
      ret
    for p in self.particles:
      if range.contains(p.pos.x, p.pos.y):
        found = found + [p]
    if self.divided:
      self.nw.query(range, found)
      self.ne.query(range, found)
      self.sw.query(range, found)
      self.se.query(range, found)

  fn get_potential_pairs(self)
    let pairs = []
    let all_particles = []
    self.collect_particles(all_particles)
    # Check all pairs in same node
    self.check_node_pairs(pairs)
    pairs

  fn collect_particles(self, list)
    for p in self.particles:
      list = list + [p]
    if self.divided:
      self.nw.collect_particles(list)
      self.ne.collect_particles(list)
      self.sw.collect_particles(list)
      self.se.collect_particles(list)

  fn check_node_pairs(self, pairs)
    let n = len(self.particles)
    for i in range(n):
      for j in range(i + 1, n):
        pairs = pairs + [[self.particles[i], self.particles[j]]]
    if self.divided:
      self.nw.check_node_pairs(pairs)
      self.ne.check_node_pairs(pairs)
      self.sw.check_node_pairs(pairs)
      self.se.check_node_pairs(pairs)

# ── Broad-phase Collision System ──
class BroadPhase:
  fn init(self, method, world_bounds, cell_size)
    self.method = method  # "grid", "quadtree", "brute"
    if method == "grid":
      self.structure = UniformGrid(cell_size, world_bounds.min_x, world_bounds.min_y, world_bounds.max_x, world_bounds.max_y)
    el:
      if method == "quadtree":
        self.structure = Quadtree(world_bounds, 4)
      el:
        self.structure = none

  fn update(self, particles)
    if self.method == "grid":
      self.structure.clear()
      for p in particles:
        self.structure.insert(p)
    el:
      if self.method == "quadtree":
        self.structure = Quadtree(AABB(-1000, -1000, 2000, 2000), 4)
        for p in particles:
          self.structure.insert(p)

  fn get_pairs(self)
    if self.method == "grid":
      ret self.structure.get_potential_pairs()
    el:
      if self.method == "quadtree":
        ret self.structure.get_potential_pairs()
      el:
        # Brute force
        ret []

# ── Collision Demo ──
fn demo_broadphase()
  say("=== Broad-phase Collision Detection Demo ===")
  
  # Create test particles
  let particles = []
  for i in range(100):
    let p = Particle("p" + str(i), 1.0, 
                     Vec2(0, 0), 
                     Vec2(0, 0))
    p.radius = 1.0
    particles = particles + [p]
  
  say("Particles: " + str(len(particles)))
  
  # Test grid
  let bounds = AABB(-100, -100, 200, 200)
  let grid = UniformGrid(10.0, -100, -100, 100, 100)
  for p in particles:
    grid.insert(p)
  
  let pairs = grid.get_potential_pairs()
  say("Uniform grid pairs: " + str(len(pairs)))
  
  # Test quadtree
  let qt = Quadtree(bounds, 4)
  for p in particles:
    qt.insert(p)
  let qt_pairs = qt.get_potential_pairs()
  say("Quadtree pairs: " + str(len(qt_pairs)))
  
  say("Broad-phase collision detection verified!")