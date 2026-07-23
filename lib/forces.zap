# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Force Laws: Gravity, Springs, Drag, Electromagnetic
# ═══════════════════════════════════════════════════════════════════

fn gravity(a, b, g_const)
  let diff = b.pos.sub(a.pos)
  let dlen = diff.length()
  let dist = dlen
  if dlen < 0.1:
    dist = 0.1
  let strength = g_const * a.mass * b.mass / (dist * dist)
  let dir = diff.normalize()
  dir.scale(strength)

fn spring_force(a, b, k, rest_len)
  let diff = b.pos.sub(a.pos)
  let dist = diff.length()
  let stretch = dist - rest_len
  let dir = diff.normalize()
  dir.scale(k * stretch)

fn drag_force(vel, coefficient)
  vel.scale(-coefficient)

fn coulomb_force(a, b, k_const)
  let diff = b.pos.sub(a.pos)
  let dlen = diff.length()
  let dist = dlen
  if dlen < 0.1:
    dist = 0.1
  let strength = k_const * a.charge * b.charge / (dist * dist)
  let dir = diff.normalize()
  dir.scale(strength)

fn damping_force(vel, coeff)
  vel.scale(-coeff * vel.length())
