class AABB:
  fn init(self, x, y, w, h)
    self.x = x
    self.y = y
    self.w = w
    self.h = h

  fn repr(self)
    "AABB(" + str(round(self.x, 2)) + "," + str(round(self.y, 2)) + " " + str(round(self.w, 2)) + "x" + str(round(self.h, 2)) + ")"

class PlatformerBody:
  fn init(self, name, x, y, w, h)
    self.name = name
    self.x = x
  fn repr(self) self.name

say(str(AABB(0,0,10,10)))
say(str(PlatformerBody("Hero", 10, 0, 32, 48)))
