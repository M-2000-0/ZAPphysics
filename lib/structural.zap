# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Structural: Truss & beam analysis
# ═══════════════════════════════════════════════════════════════════

class Node:
  fn init(self, id, x, y)
    self.id = id
    self.x = x
    self.y = y
    self.fx = 0
    self.fy = 0
    self.fixed_x = false
    self.fixed_y = false
    self.disp_x = 0
    self.disp_y = 0

  fn fix(self)
    self.fixed_x = true
    self.fixed_y = true

  fn fix_x(self)
    self.fixed_x = true

  fn fix_y(self)
    self.fixed_y = true

  fn apply_load(self, fx, fy)
    self.fx = self.fx + fx
    self.fy = self.fy + fy

  fn repr(self)
    "Node(" + self.id + " @(" + str(round(self.x, 2)) + "," + str(round(self.y, 2)) + "))"

class Member:
  fn init(self, id, node_a, node_b, E, A)
    self.id = id
    self.node_a = node_a
    self.node_b = node_b
    self.E = E
    self.A = A
    self.force = 0
    self.stress = 0
    self.strain = 0

  fn length(self)
    let dx = self.node_b.x - self.node_a.x
    let dy = self.node_b.y - self.node_a.y
    sqrt(dx * dx + dy * dy)

  fn stiffness(self)
    self.E * self.A / self.length()

  fn axial_force(self)
    let l = self.length()
    let dx = (self.node_b.x + self.node_b.disp_x) - (self.node_a.x + self.node_a.disp_x)
    let dy = (self.node_b.y + self.node_b.disp_y) - (self.node_a.y + self.node_a.disp_y)
    let new_len = sqrt(dx * dx + dy * dy)
    let delta = new_len - l
    self.strain = delta / l
    self.stress = self.E * self.strain
    self.force = self.stress * self.A
    self.force

  fn repr(self)
    self.id + ": " + self.node_a.id + "->" + self.node_b.id + " F=" + str(round(self.force, 2))

class Truss:
  fn init(self)
    self.nodes = []
    self.members = []
    self.solved = false

  fn add_node(self, node)
    self.nodes = self.nodes + [node]

  fn add_member(self, member)
    self.members = self.members + [member]

  fn find_node(self, id)
    for n in self.nodes:
      if n.id == id:
        ret n
    ret nil

  fn total_force_x(self)
    let total = 0
    for n in self.nodes:
      total = total + n.fx
    total

  fn total_force_y(self)
    let total = 0
    for n in self.nodes:
      total = total + n.fy
    total

  # Simplified direct stiffness method (iterative relaxation)
  fn solve(self, iterations)
    let n_nodes = len(self.nodes)
    let n_members = len(self.members)

    # Build global stiffness matrix (simplified: iterative relaxation)
    for iter in range(iterations):
      for m in self.members:
        let l0 = m.length()
        let dx = m.node_b.x - m.node_a.x
        let dy = m.node_b.y - m.node_a.y
        let cos_a = dx / l0
        let sin_a = dy / l0
        let k = m.stiffness()

        let dux = m.node_b.disp_x - m.node_a.disp_x
        let duy = m.node_b.disp_y - m.node_a.disp_y
        let extension = dux * cos_a + duy * sin_a
        let fx = k * extension * cos_a
        let fy = k * extension * sin_a

        if not m.node_a.fixed_x:
          m.node_a.disp_x = m.node_a.disp_x + fx / (k + 1) * 0.1
        if not m.node_a.fixed_y:
          m.node_a.disp_y = m.node_a.disp_y + fy / (k + 1) * 0.1
        if not m.node_b.fixed_x:
          m.node_b.disp_x = m.node_b.disp_x - fx / (k + 1) * 0.1
        if not m.node_b.fixed_y:
          m.node_b.disp_y = m.node_b.disp_y - fy / (k + 1) * 0.1

      # Apply external loads as displacements
      for n in self.nodes:
        if not n.fixed_x:
          n.disp_x = n.disp_x + n.fx * 0.0001
        if not n.fixed_y:
          n.disp_y = n.disp_y + n.fy * 0.0001

    # Calculate member forces
    for m in self.members:
      m.axial_force()

    self.solved = true

  fn summary(self)
    say("=== TRUSS ANALYSIS ===")
    say("  nodes: " + str(len(self.nodes)))
    say("  members: " + str(len(self.members)))
    say("")
    say("  Node displacements:")
    for n in self.nodes:
      say("    " + n.id + " disp=(" + str(round(n.disp_x, 6)) + ", " + str(round(n.disp_y, 6)) + ")")
    say("")
    say("  Member forces (tension +, compression -):")
    let max_force = 0
    let critical = ""
    for m in self.members:
      say("    " + m.id + ": " + str(round(m.force, 2)) + " N  stress=" + str(round(m.stress, 2)) + " Pa")
      if abs(m.force) > abs(max_force):
        max_force = m.force
        critical = m.id
    say("")
    say("  Critical member: " + critical + " (F=" + str(round(max_force, 2)) + " N)")

# Beam analysis
class Beam:
  fn init(self, length, E, I)
    self.length = length
    self.E = E
    self.I = I

  # Maximum deflection for simply supported beam with point load P at center
  fn max_deflection(self, P)
    let l = self.length
    P * l * l * l / (48 * self.E * self.I)

  # Maximum deflection for cantilever with point load P at end
  fn cantilever_deflection(self, P)
    let l = self.length
    P * l * l * l / (3 * self.E * self.I)

  # Maximum deflection for simply supported beam with uniform load w
  fn uniform_deflection(self, w)
    let l = self.length
    5 * w * l * l * l * l / (384 * self.E * self.I)

  # Maximum bending moment for simply supported with point load at center
  fn max_bending_moment(self, P)
    P * self.length / 4.0

  # Cantilever max bending moment
  fn cantilever_moment(self, P)
    P * self.length

  # Maximum shear force
  fn max_shear(self, P)
    P / 2.0

  # Cantilever shear
  fn cantilever_shear(self, P)
    P

  # Bending stress: sigma = M * c / I
  fn bending_stress(self, M, c)
    M * c / self.I

  # Section modulus: S = I / c
  fn section_modulus(self, c)
    self.I / c

  # Natural frequency (simply supported)
  fn natural_frequency(self, m)
    let pi = 3.14159265
    pi * pi / (self.length * self.length) * sqrt(self.E * self.I / m)

  # Critical buckling load (Euler)
  fn euler_buckling(self, K)
    let pi = 3.14159265
    pi * pi * self.E * self.I / (K * self.length * self.length)
