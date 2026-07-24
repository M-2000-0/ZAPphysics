# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Game: Game physics (platformer, top-down, ragdoll)
# ═══════════════════════════════════════════════════════════════════

import "lib/vec2.zap"

class AABB:
  fn init(self, x, y, w, h)
    self.x = x
    self.y = y
    self.w = w
    self.h = h

  fn left(self)
    self.x

  fn right(self)
    self.x + self.w

  fn top(self)
    self.y

  fn bottom(self)
    self.y + self.h

  fn center_x(self)
    self.x + self.w / 2

  fn center_y(self)
    self.y + self.h / 2

  fn contains_point(self, px, py)
    px >= self.x and px <= self.x + self.w and py >= self.y and py <= self.y + self.h

  fn overlaps(self, other)
    let a = self.x < other.x + other.w and self.x + self.w > other.x
    let b = self.y < other.y + other.h and self.y + self.h > other.y
    a and b

  fn intersection(self, other)
    let ix = other.x
    if self.x > other.x:
      ix = self.x
    let iy = other.y
    if self.y > other.y:
      iy = self.y
    let ir = self.x + self.w
    if self.x + self.w < other.x + other.w:
      ir = other.x + other.w
    let ib = self.y + self.h
    if self.y + self.h < other.y + other.h:
      ib = other.y + other.h
    if ir > ix and ib > iy:
      AABB(ix, iy, ir - ix, ib - iy)
    el:
      AABB(0, 0, 0, 0)

  fn area(self)
    self.w * self.h

  fn repr(self)
    "AABB(" + str(round(self.x, 2)) + "," + str(round(self.y, 2)) + " " + str(round(self.w, 2)) + "x" + str(round(self.h, 2)) + ")"

# Platformer body with gravity, jumping, ground detection
class PlatformerBody:
  fn init(self, name, x, y, w, h)
    self.name = name
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.vx = 0
    self.vy = 0
    self.on_ground = false
    self.gravity = 980
    self.max_speed = 300
    self.jump_force = -450
    self.move_speed = 200
    self.friction = 0.85
    self.air_control = 0.6

  fn aabb(self)
    AABB(self.x, self.y, self.w, self.h)

  fn move_left(self)
    let ctrl = self.air_control
    if self.on_ground:
      ctrl = 1
    self.vx = self.vx - self.move_speed * ctrl

  fn move_right(self)
    let ctrl = self.air_control
    if self.on_ground:
      ctrl = 1
    self.vx = self.vx + self.move_speed * ctrl

  fn jump(self)
    if self.on_ground:
      self.vy = self.jump_force
      self.on_ground = false

  fn apply_gravity(self, dt)
    self.vy = self.vy + self.gravity * dt

  fn step(self, dt)
    self.apply_gravity(dt)
    if self.on_ground:
      self.vx = self.vx * self.friction
    el:
      self.vx = self.vx * 0.95
    if self.vx > self.max_speed:
      self.vx = self.max_speed
    if self.vx < -self.max_speed:
      self.vx = -self.max_speed
    self.x = self.x + self.vx * dt
    self.y = self.y + self.vy * dt

  fn resolve_ground(self, ground_y)
    if self.y + self.h >= ground_y:
      self.y = ground_y - self.h
      self.vy = 0
      self.on_ground = true

  fn resolve_collision_aabb(self, other)
    let my_box = self.aabb()
    if my_box.overlaps(other):
      let ix = my_box.intersection(other)
      if ix.w > 0 and ix.h > 0:
        if ix.w < ix.h:
          if self.x + self.w / 2 < other.x + other.w / 2:
            self.x = self.x - ix.w
          el:
            self.x = self.x + ix.w
          self.vx = 0
        el:
          if self.y + self.h / 2 < other.y + other.h / 2:
            self.y = self.y - ix.h
            self.vy = 0
            self.on_ground = true
          el:
            self.y = self.y + ix.h
            self.vy = 0

  fn speed(self)
    sqrt(self.vx * self.vx + self.vy * self.vy)

  fn repr(self)
    self.name + "@(" + str(round(self.x, 1)) + "," + str(round(self.y, 1)) + ")"

# Top-down body (no gravity, friction-based movement)
class TopDownBody:
  fn init(self, name, x, y, radius)
    self.name = name
    self.x = x
    self.y = y
    self.vx = 0
    self.vy = 0
    self.radius = radius
    self.friction = 0.92
    self.max_speed = 250
    self.accel = 800

  fn move_toward(self, tx, ty, dt)
    let dx = tx - self.x
    let dy = ty - self.y
    let dist = sqrt(dx * dx + dy * dy)
    if dist > 1:
      self.vx = self.vx + dx / dist * self.accel * dt
      self.vy = self.vy + dy / dist * self.accel * dt

  fn step(self, dt)
    let spd = sqrt(self.vx * self.vx + self.vy * self.vy)
    if spd > self.max_speed:
      self.vx = self.vx / spd * self.max_speed
      self.vy = self.vy / spd * self.max_speed
    self.x = self.x + self.vx * dt
    self.y = self.y + self.vy * dt
    self.vx = self.vx * self.friction
    self.vy = self.vy * self.friction

  fn distance_to(self, other)
    let dx = other.x - self.x
    let dy = other.y - self.y
    sqrt(dx * dx + dy * dy)

  fn collides(self, other)
    let dx = other.x - self.x
    let dy = other.y - self.y
    let dist = sqrt(dx * dx + dy * dy)
    dist < self.radius + other.radius

  fn speed(self)
    sqrt(self.vx * self.vx + self.vy * self.vy)

  fn resolve_collision(self, other)
    let dx = other.x - self.x
    let dy = other.y - self.y
    let dist = sqrt(dx * dx + dy * dy)
    if dist < self.radius + other.radius and dist > 0.01:
      let nx = dx / dist
      let ny = dy / dist
      let overlap = self.radius + other.radius - dist
      self.x = self.x - nx * overlap * 0.5
      self.y = self.y - ny * overlap * 0.5
      other.x = other.x + nx * overlap * 0.5
      other.y = other.y + ny * overlap * 0.5
      let dvx = self.vx - other.vx
      let dvy = self.vy - other.vy
      let dvn = dvx * nx + dvy * ny
      if dvn > 0:
        self.vx = self.vx - dvn * nx * 0.8
        self.vy = self.vy - dvn * ny * 0.8
        other.vx = other.vx + dvn * nx * 0.8
        other.vy = other.vy + dvn * ny * 0.8

  fn repr(self)
    self.name + "@(" + str(round(self.x, 1)) + "," + str(round(self.y, 1)) + ")"

# Ragdoll bone (connects two joints)
class RagdollBone:
  fn init(self, joint_a, joint_b, length)
    self.joint_a = joint_a
    self.joint_b = joint_b
    self.length = length

# Ragdoll joint (constrained particle)
class RagdollJoint:
  fn init(self, name, x, y, mass)
    self.name = name
    self.x = x
    self.y = y
    self.vx = 0
    self.vy = 0
    self.mass = mass
    self.fixed = false

  fn step(self, dt)
    if not self.fixed:
      self.x = self.x + self.vx * dt
      self.y = self.y + self.vy * dt

# Ragdoll (collection of joints and bones with distance constraints)
class Ragdoll:
  fn init(self)
    self.joints = []
    self.bones = []
    self.gravity = 600
    self.damping = 0.99

  fn add_joint(self, j)
    self.joints = self.joints + [j]

  fn add_bone(self, b)
    self.bones = self.bones + [b]

  fn step(self, dt, constraint_iterations)
    for j in self.joints:
      if not j.fixed:
        j.vy = j.vy + self.gravity * dt
      j.step(dt)

    for iter in range(constraint_iterations):
      for b in self.bones:
        let dx = b.joint_b.x - b.joint_a.x
        let dy = b.joint_b.y - b.joint_a.y
        let dist = sqrt(dx * dx + dy * dy)
        if dist > 0.01:
          let diff = (dist - b.length) / dist * 0.5
          let nx = dx * diff
          let ny = dy * diff
          if not b.joint_a.fixed:
            b.joint_a.x = b.joint_a.x + nx
            b.joint_a.y = b.joint_a.y + ny
          if not b.joint_b.fixed:
            b.joint_b.x = b.joint_b.x - nx
            b.joint_b.y = b.joint_b.y - ny

    for j in self.joints:
      j.vx = j.vx * self.damping
      j.vy = j.vy * self.damping

  fn center(self)
    let cx = 0
    let cy = 0
    for j in self.joints:
      cx = cx + j.x
      cy = cy + j.y
    let n = len(self.joints)
    if n > 0:
      Vec2(cx / n, cy / n)
    el:
      Vec2(0, 0)
