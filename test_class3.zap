class AABB:
  fn init(self, x, y)
    self.x = x
    self.y = y
  fn repr(self)
    "AABB"

say("before: " + str(AABB(1, 2)))
