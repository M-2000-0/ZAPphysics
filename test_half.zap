class AABB:
  fn init(self, x, y, w, h)
    self.x = x
    self.y = y
    self.w = w
    self.h = h

  fn left(self) self.x
  fn right(self) self.x + self.w
  fn top(self) self.y
  fn bottom(self) self.y + self.h
  fn center_x(self) self.x + self.w / 2
  fn center_y(self) self.y + self.h / 2

  fn contains_point(self, px, py)
    px >= self.x and px <= self.x + self.w and py >= self.y and py <= self.y + self.h

  fn overlaps(self, other)
    self.x < other.x + other.w and self.x + self.w > other.x
    and self.y < other.y + other.h and self.y + self.h > other.y

  fn intersection(self, other)
    let ix = if self.x > other.x: self.x el: other.x
    let iy = if self.y > other.y: self.y el: other.y
    let ir = if self.x + self.w < other.x + other.w: self.x + self.w el: other.x + other.w
    let ib = if self.y + self.h < other.y + other.h: self.y + self.h el: other.y + other.h
    if ir > ix and ib > iy:
      AABB(ix, iy, ir - ix, ib - iy)
    el:
      AABB(0, 0, 0, 0)

  fn area(self) self.w * self.h

  fn repr(self)
    "AABB(" + str(round(self.x, 2)) + "," + str(round(self.y, 2)) + " " + str(round(self.w, 2)) + "x" + str(round(self.h, 2)) + ")"

class PlatformerBody:
  fn init(self, name, x, y, w, h)
    self.name = name
    self.x = x
  fn repr(self) self.name

say(str(AABB(0,0,10,10)))
say(str(PlatformerBody("Hero", 10, 0, 32, 48)))
