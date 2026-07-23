# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Collision: Elastic impulse-based collision resolution
# ═══════════════════════════════════════════════════════════════════

fn collide(a, b)
  let diff = b.pos.sub(a.pos)
  let dist = diff.length()
  let min_dist = a.radius + b.radius
  if dist < min_dist:
    if dist > 0:
      let normal = diff.normalize()
      let rel_vel = a.vel.sub(b.vel)
      let vel_along_normal = rel_vel.dot(normal)
      if vel_along_normal > 0:
        ret
      let e = 0.9
      let j = -(1 + e) * vel_along_normal
      j = j / (1.0 / a.mass + 1.0 / b.mass)
      let impulse = normal.scale(j)
      a.vel = a.vel.sub(impulse.scale(1.0 / a.mass))
      b.vel = b.vel.add(impulse.scale(1.0 / b.mass))
      let overlap = min_dist - dist
      let total_mass = a.mass + b.mass
      a.pos = a.pos.sub(normal.scale(overlap * b.mass / total_mass))
      b.pos = b.pos.add(normal.scale(overlap * a.mass / total_mass))

fn check_collision(a, b)
  let diff = b.pos.sub(a.pos)
  let dist = diff.length()
  dist < (a.radius + b.radius)
