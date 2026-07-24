# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Art: Generative art via particle systems
# ═══════════════════════════════════════════════════════════════════

class ArtParticle:
  fn init(self, x, y, vx, vy, life, color)
    self.x = x
    self.y = y
    self.vx = vx
    self.vy = vy
    self.life = life
    self.max_life = life
    self.color = color
    self.size = 1
    self.decay = 1.0

  fn alive(self)
    self.life > 0

  fn progress(self)
    1.0 - self.life / self.max_life

  fn step(self, dt)
    self.x = self.x + self.vx * dt
    self.y = self.y + self.vy * dt
    self.life = self.life - dt
    self.size = self.size * self.decay

  fn repr(self)
    self.color + "@" + str(round(self.x, 1)) + "," + str(round(self.y, 1))

# Particle Emitter
class Emitter:
  fn init(self, x, y, rate)
    self.x = x
    self.y = y
    self.rate = rate
    self.particles = []
    self.emit_count = 0
    self.spread = 1.0
    self.speed = 100
    self.life_min = 1.0
    self.life_max = 3.0
    self.colors = ["red", "orange", "yellow"]

  fn set_colors(self, colors)
    self.colors = colors

  fn emit(self)
    let angle = (self.emit_count * 0.618033988749895) * 6.283185307179586
    let spd = self.speed * (0.5 + (self.emit_count * 0.173827) - floor(self.emit_count * 0.173827))
    let vx = cos(angle) * spd * self.spread
    let vy = sin(angle) * spd * self.spread
    let life = self.life_min + (self.life_max - self.life_min) * (self.emit_count * 0.314159 - floor(self.emit_count * 0.314159))
    let ci = self.emit_count - floor(self.emit_count / len(self.colors)) * len(self.colors)
    let color = self.colors[ci]
    let p = ArtParticle(self.x, self.y, vx, vy, life, color)
    self.particles = self.particles + [p]
    self.emit_count = self.emit_count + 1

  fn emit_n(self, n)
    for i in range(n):
      self.emit()

  fn burst(self, count)
    for i in range(count):
      let angle = i * 6.283185307179586 / count
      let vx = cos(angle) * self.speed
      let vy = sin(angle) * self.speed
      let life = self.life_min + (self.life_max - self.life_min) * 0.5
      let ci = i - floor(i / len(self.colors)) * len(self.colors)
      let color = self.colors[ci]
      let p = ArtParticle(self.x, self.y, vx, vy, life, color)
      self.particles = self.particles + [p]
      self.emit_count = self.emit_count + 1

  fn step(self, dt)
    let alive = []
    for p in self.particles:
      p.step(dt)
      if p.alive():
        alive = alive + [p]
    self.particles = alive

  fn count(self)
    len(self.particles)

  fn summary(self)
    say("  emitter (" + str(round(self.x, 1)) + "," + str(round(self.y, 1)) + "): " + str(self.count()) + " particles")

# Gravity well (attractor)
class GravityWell:
  fn init(self, x, y, strength)
    self.x = x
    self.y = y
    self.strength = strength

  fn apply_to(self, particle, dt)
    let dx = self.x - particle.x
    let dy = self.y - particle.y
    let dist = sqrt(dx * dx + dy * dy)
    if dist > 5:
      let force = self.strength / (dist * dist)
      particle.vx = particle.vx + dx / dist * force * dt
      particle.vy = particle.vy + dy / dist * force * dt

# Art World (manages emitters and particles)
class ArtWorld:
  fn init(self, width, height)
    self.width = width
    self.height = height
    self.emitters = []
    self.wells = []
    self.time = 0
    self.total_spawned = 0

  fn add_emitter(self, e)
    self.emitters = self.emitters + [e]

  fn add_well(self, w)
    self.wells = self.wells + [w]

  fn step(self, dt)
    for e in self.emitters:
      e.emit_n(e.rate)
      e.step(dt)
      self.total_spawned = self.total_spawned + e.rate
      for p in e.particles:
        for w in self.wells:
          w.apply_to(p, dt)
        # wrap around screen
        if p.x < 0:
          p.x = p.x + self.width
        if p.x > self.width:
          p.x = p.x - self.width
        if p.y < 0:
          p.y = p.y + self.height
        if p.y > self.height:
          p.y = p.y - self.height
    self.time = self.time + dt

  fn total_particles(self)
    let total = 0
    for e in self.emitters:
      total = total + e.count()
    total

  fn summary(self)
    say("=== ART WORLD ===")
    say("  time: " + str(round(self.time, 2)) + "s")
    say("  emitters: " + str(len(self.emitters)))
    say("  gravity wells: " + str(len(self.wells)))
    say("  total particles: " + str(self.total_particles()))
    say("  total spawned: " + str(self.total_spawned))
    for e in self.emitters:
      e.summary()
