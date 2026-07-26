import "lib/vec2.zap"
import "lib/vec3.zap"
import "lib/orbital_mechanics.zap"

let r1_vec = Vec3(7000000, 0, 0)
let r2_vec = Vec3(42000000, 0, 0)
let dt = 5 * 3600
let mu = 3.986e14
let result = lambert(r1_vec, r2_vec, dt, mu, true)
if result != none:
  say("lambert[0]=" + str(result[0]))
  say("lambert[1]=" + str(result[1]))
  say("lambert[2]=" + str(result[2]))
el:
  say("No solution")
say("done")
