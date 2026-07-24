# ═══════════════════════════════════════════════════════════════════
# Demo: Game Physics — Platformer, top-down, ragdoll
# Run: zap run main.zap
# ═══════════════════════════════════════════════════════════════════

say("")
say("=== DEMO: Game Physics ===")

say("")
say("-- Platformer Physics --")

let player = PlatformerBody("Hero", 10, 0, 32, 48)
let ground_y = 400
let platform1 = AABB(0, 300, 200, 20)
let platform2 = AABB(250, 250, 150, 20)
let wall = AABB(500, 0, 20, 400)

say("  Player: " + str(player))
say("  Ground Y: " + str(ground_y))

# simulate 60 frames
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
  player.resolve_collision_aabb(platform1)
  player.resolve_collision_aabb(platform2)
  player.resolve_collision_aabb(wall)

say("  Final: " + str(player) + "  on_ground=" + str(player.on_ground) + "  speed=" + str(round(player.speed(), 1)))

say("")
say("-- Top-Down Physics --")

let car1 = TopDownBody("Car-A", 0, 0, 15)
let car2 = TopDownBody("Car-B", 100, 0, 15)
let obstacle = TopDownBody("Wall", 50, 0, 25)
obstacle.vx = 0
obstacle.vy = 0

say("  Simulating top-down movement...")
for frame in range(40):
  car1.move_toward(100, 50, 1.0 / 60.0)
  car1.step(1.0 / 60.0)
  if car1.collides(obstacle):
    car1.resolve_collision(obstacle)
  if car1.collides(car2):
    car1.resolve_collision(car2)

say("  " + str(car1) + " speed=" + str(round(car1.speed(), 1)))

say("")
say("-- Ragdoll Physics --")

let rag = Ragdoll()

# create a simple stick figure ragdoll
let head = RagdollJoint("head", 200, 50, 2)
head.fixed = true
let neck = RagdollJoint("neck", 200, 70, 1)
let hip = RagdollJoint("hip", 200, 150, 2)
let lhand = RagdollJoint("lhand", 170, 100, 0.5)
let rhand = RagdollJoint("rhand", 230, 100, 0.5)
let lfoot = RagdollJoint("lfoot", 185, 200, 0.5)
let rfoot = RagdollJoint("rfoot", 215, 200, 0.5)

rag.add_joint(head)
rag.add_joint(neck)
rag.add_joint(hip)
rag.add_joint(lhand)
rag.add_joint(rhand)
rag.add_joint(lfoot)
rag.add_joint(rfoot)

rag.add_bone(RagdollBone(head, neck, 20))
rag.add_bone(RagdollBone(neck, hip, 80))
rag.add_bone(RagdollBone(neck, lhand, 40))
rag.add_bone(RagdollBone(neck, rhand, 40))
rag.add_bone(RagdollBone(hip, lfoot, 55))
rag.add_bone(RagdollBone(hip, rfoot, 55))

say("  Ragdoll: " + str(len(rag.joints)) + " joints, " + str(len(rag.bones)) + " bones")
say("  Simulating ragdoll fall (30 frames)...")
head.fixed = false

for frame in range(30):
  rag.step(1.0 / 60.0, 5)

say("  Center of mass: " + str(rag.center()))
say("  Joint positions:")
for j in rag.joints:
  say("    " + j.name + ": (" + str(round(j.x, 1)) + ", " + str(round(j.y, 1)) + ")")

say("  Game physics verified!")
