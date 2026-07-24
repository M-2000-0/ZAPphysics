import "lib/game.zap"

say("Game demo starting...")

let player = PlatformerBody("Hero", 10, 0, 32, 48)
let ground_y = 400
let platform1 = AABB(0, 300, 200, 20)
let platform2 = AABB(250, 250, 150, 20)
let wall = AABB(500, 0, 20, 400)

say("  Player: " + str(player))
say("  Ground Y: " + str(ground_y))

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
say("Platformer done!")
