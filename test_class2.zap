class AABB:
  fn init(self, x, y, w, h)
    self.x = x
    self.y = y
    self.w = w
    self.h = h
  fn repr(self) "AABB"

class PlatformerBody:
  fn init(self, name)
    self.name = name
  fn repr(self) self.name

say(str(AABB(0,0,10,10)))
say(str(PlatformerBody("Hero")))
