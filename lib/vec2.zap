# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Vec2: 2D Vector Operations
# ═══════════════════════════════════════════════════════════════════

class Vec2:
  fn init(self, x, y)
    self.x = x
    self.y = y

  fn add(self, other)
    Vec2(self.x + other.x, self.y + other.y)

  fn sub(self, other)
    Vec2(self.x - other.x, self.y - other.y)

  fn scale(self, s)
    Vec2(self.x * s, self.y * s)

  fn dot(self, other)
    self.x * other.x + self.y * other.y

  fn length(self)
    sqrt(self.x * self.x + self.y * self.y)

  fn normalize(self)
    let mag = self.length()
    if mag > 0:
      self.scale(1.0 / mag)
    el:
      Vec2(0, 0)

  fn dist(self, other)
    self.sub(other).length()

  fn angle(self)
    atan2(self.y, self.x)

  fn rotate(self, theta)
    let c = cos(theta)
    let s = sin(theta)
    Vec2(self.x * c - self.y * s, self.x * s + self.y * c)

  fn lerp(self, other, t)
    Vec2(self.x + (other.x - self.x) * t, self.y + (other.y - self.y) * t)

  fn repr(self)
    "Vec2(" + str(round(self.x, 4)) + ", " + str(round(self.y, 4)) + ")"

fn vec2(x, y) Vec2(x, y)
