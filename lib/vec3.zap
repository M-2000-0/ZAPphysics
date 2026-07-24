# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Vec3: 3D Vector Operations
# ═══════════════════════════════════════════════════════════════════

class Vec3:
  fn init(self, x, y, z)
    self.x = x
    self.y = y
    self.z = z

  fn add(self, other)
    Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

  fn sub(self, other)
    Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

  fn scale(self, s)
    Vec3(self.x * s, self.y * s, self.z * s)

  fn dot(self, other)
    self.x * other.x + self.y * other.y + self.z * other.z

  fn cross(self, other)
    Vec3(
      self.y * other.z - self.z * other.y,
      self.z * other.x - self.x * other.z,
      self.x * other.y - self.y * other.x
    )

  fn length(self)
    sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

  fn length_sq(self)
    self.x * self.x + self.y * self.y + self.z * self.z

  fn normalize(self)
    let mag = self.length()
    if mag > 1e-10:
      self.scale(1.0 / mag)
    el:
      Vec3(0, 0, 0)

  fn dist(self, other)
    self.sub(other).length()

  fn lerp(self, other, t)
    Vec3(
      self.x + (other.x - self.x) * t,
      self.y + (other.y - self.y) * t,
      self.z + (other.z - self.z) * t
    )

  fn rotate_x(self, theta)
    let c = cos(theta)
    let s = sin(theta)
    Vec3(self.x, self.y * c - self.z * s, self.y * s + self.z * c)

  fn rotate_y(self, theta)
    let c = cos(theta)
    let s = sin(theta)
    Vec3(self.x * c + self.z * s, self.y, -self.x * s + self.z * c)

  fn rotate_z(self, theta)
    let c = cos(theta)
    let s = sin(theta)
    Vec3(self.x * c - self.y * s, self.x * s + self.y * c, self.z)

  fn project(self, axis)
    let d = self.dot(axis) / axis.dot(axis)
    axis.scale(d)

  fn reject(self, axis)
    self.sub(self.project(axis))

  fn angle_between(self, other)
    let d = self.dot(other) / (self.length() * other.length())
    if d > 1:
      d = 1
    if d < -1:
      d = -1
    acos(d)

  fn min(self, other)
    let mx = self.x
    let my = self.y
    let mz = self.z
    if other.x < mx:
      mx = other.x
    if other.y < my:
      my = other.y
    if other.z < mz:
      mz = other.z
    Vec3(mx, my, mz)

  fn max(self, other)
    let mx = self.x
    let my = self.y
    let mz = self.z
    if other.x > mx:
      mx = other.x
    if other.y > my:
      my = other.y
    if other.z > mz:
      mz = other.z
    Vec3(mx, my, mz)

  fn abs(self)
    Vec3(abs(self.x), abs(self.y), abs(self.z))

  fn to_list(self)
    [self.x, self.y, self.z]

  fn repr(self)
    "Vec3(" + str(round(self.x, 4)) + ", " + str(round(self.y, 4)) + ", " + str(round(self.z, 4)) + ")"

fn vec3(x, y, z) Vec3(x, y, z)
fn vec3_zero() Vec3(0, 0, 0)
fn vec3_up() Vec3(0, 1, 0)
fn vec3_forward() Vec3(0, 0, -1)
fn vec3_right() Vec3(1, 0, 0)
