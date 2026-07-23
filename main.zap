# ═══════════════════════════════════════════════════════════════════
# ZapPhysics v2.0
# Physics & Chemistry simulation engine for Zap
#
# Run all demos:  zap run main.zap
# Run one demo:   zap run examples/orbital.zap
# ═══════════════════════════════════════════════════════════════════

import "lib/vec2.zap"
import "lib/particle.zap"
import "lib/forces.zap"
import "lib/collision.zap"
import "lib/world.zap"
import "lib/elements.zap"
import "lib/molecule.zap"
import "lib/reaction.zap"
import "lib/thermo.zap"

say("==============================================")
say("  ZapPhysics v2.0")
say("  Physics & Chemistry engine for Zap")
say("==============================================")
say("")
say("  Modules loaded:")
say("    lib/vec2.zap       - 2D vector math")
say("    lib/particle.zap   - Point-mass particles")
say("    lib/forces.zap     - Gravity, springs, drag, Coulomb")
say("    lib/collision.zap  - Elastic collision resolution")
say("    lib/world.zap      - Simulation world & integrator")
say("    lib/elements.zap   - Periodic table (14 elements)")
say("    lib/molecule.zap   - Molecular modeling & bonds")
say("    lib/reaction.zap   - Chemical reaction tracking")
say("    lib/thermo.zap     - Thermodynamics & gas laws")
say("")
say("  Running all demos...")

import "examples/orbital.zap"
import "examples/springs.zap"
import "examples/collisions.zap"
import "examples/chemistry.zap"
import "examples/tensor.zap"

say("")
say("==============================================")
say("  All demos complete!")
say("  Zap powers physics + chemistry simulations.")
say("==============================================")
