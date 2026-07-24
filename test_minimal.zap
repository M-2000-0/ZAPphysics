class AABB:
  fn init(self, x, y, w, h)
    self.x = x
    self.y = y
    self.w = w
    self.h = h
  fn repr(self) "AABB"

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
  fn step(self, dt)
    self.apply_gravity(dt)
    self.vx = self.vx * 0.95
    self.x = self.x + self.vx * dt
    self.y = self.y + self.vy * dt
  fn apply_gravity(self, dt)
    self.vy = self.vy + self.gravity * dt
  fn resolve_ground(self, ground_y)
    if self.y + self.h >= ground_y:
      self.y = ground_y - self.h
      self.vy = 0
      self.on_ground = true
  fn speed(self)
    sqrt(self.vx * self.vx + self.vy * self.vy)
  fn repr(self)
    self.name + "@(" + str(round(self.x, 1)) + "," + str(round(self.y, 1)) + ")"

say("-- Platformer Physics --")
let player = PlatformerBody("Hero", 10, 0, 32, 48)
let ground_y = 400
say("  Player: " + str(player))
say("  Ground Y: " + str(ground_y))
say("  Simulating platformer movement (60 frames)...")
for frame in range(60):
  if frame < 15:
    player.move_right()
  if frame == 20:
    player.jump()
  if frame > 30 and frame < 45:
    player.move_right()
  if frame == 35:
    player.jump()
  player.step(1.0 / 60.0)
  player.resolve_ground(ground_y)
say("  Final: " + str(player) + "  on_ground=" + str(player.on_ground) + "  speed=" + str(round(player.speed(), 1)))
