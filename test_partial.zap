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
    let ctrl = if self.on_ground: 1 el: self.air_control
    self.vx = self.vx - self.move_speed * ctrl

  fn move_right(self)
    let ctrl = if self.on_ground: 1 el: self.air_control
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

  fn speed(self) sqrt(self.vx * self.vx + self.vy * self.vy)

  fn repr(self)
    self.name + "@(" + str(round(self.x, 1)) + "," + str(round(self.y, 1)) + ")"
