# ═══════════════════════════════════════════════════════════════════
# ZapPhysics v4.0
# Complete Physics & Chemistry + Engineering simulation engine for Zap
#
# Run all demos:  zap run main.zap
# ═══════════════════════════════════════════════════════════════════

# ── Core Physics ──
import "lib/vec2.zap"
import "lib/vec3.zap"
import "lib/particle.zap"
import "lib/particle3d.zap"
import "lib/forces.zap"
import "lib/collision.zap"
import "lib/world.zap"
import "lib/world3d.zap"

# ── Advanced Physics ──
import "lib/em.zap"
import "lib/sph.zap"
import "lib/rigid.zap"

# ── Engineering ──
import "lib/structural.zap"
import "lib/rocket.zap"
import "lib/aero.zap"
import "lib/orbital_mechanics.zap"
import "lib/flight.zap"
import "lib/porkchop.zap"
import "lib/broadphase.zap"
import "lib/constraint.zap"

# ── Game Physics ──
import "lib/game.zap"

# ── Chemistry ──
import "lib/elements.zap"
import "lib/molecule.zap"
import "lib/reaction.zap"
import "lib/thermo.zap"
import "lib/kinetics.zap"

# ── Visualization & Art ──
import "lib/visual.zap"
import "lib/visualize.zap"
import "lib/art.zap"

# ── Demos ──
import "examples/orbital.zap"
import "examples/springs.zap"
import "examples/collisions.zap"
import "examples/chemistry.zap"
import "examples/tensor.zap"
import "examples/demo3d.zap"
import "examples/demo_em.zap"
import "examples/demo_fluid.zap"
import "examples/demo_rigid.zap"
import "examples/demo_structural.zap"
import "examples/demo_game.zap"
import "examples/demo_art.zap"
import "examples/demo_visual.zap"
import "examples/demo_elements.zap"
import "examples/demo_kinetics.zap"
import "examples/demo_rocket.zap"
import "examples/demo_flight.zap"
import "examples/demo_orbital_mechanics.zap"
import "examples/demo_orbital3d.zap"
import "examples/demo_lambert.zap"
import "examples/demo_porkchop.zap"
import "examples/demo_broadphase.zap"
import "examples/demo_constraints.zap"

say("")
say("==============================================")
say("  All 22 demos complete!")
say("  ZapPhysics v4.0: physics + chemistry + engineering + aerospace.")
say("  22 demos: N-body, collision, chemistry, EM, SPH, rigid body,")
say("       structural, game, broadphase, rocket, aero, orbital, flight.")
say("==============================================")
