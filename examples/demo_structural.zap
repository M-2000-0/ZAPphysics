# ═══════════════════════════════════════════════════════════════════
# Demo: Structural Engineering — Truss & Beam analysis
# Run: zap run main.zap
# ═══════════════════════════════════════════════════════════════════

say("")
say("=== DEMO: Structural Engineering ===")

say("")
say("-- Truss Analysis: Simple Warren Truss --")

let truss = Truss()

let n0 = Node("N0", 0, 0)
n0.fix()
let n1 = Node("N1", 5, 0)
let n2 = Node("N2", 10, 0)
let n3 = Node("N3", 15, 0)
let n4 = Node("N4", 20, 0)
n4.fix()
let n5 = Node("N5", 2.5, 4)
let n6 = Node("N6", 7.5, 4)
let n7 = Node("N7", 12.5, 4)
let n8 = Node("N8", 17.5, 4)

# apply downward load at middle nodes
n6.apply_load(0, -10000)
n7.apply_load(0, -10000)

truss.add_node(n0)
truss.add_node(n1)
truss.add_node(n2)
truss.add_node(n3)
truss.add_node(n4)
truss.add_node(n5)
truss.add_node(n6)
truss.add_node(n7)
truss.add_node(n8)

let E = 200e9
let A = 0.001

truss.add_member(Member("M01", n0, n1, E, A))
truss.add_member(Member("M12", n1, n2, E, A))
truss.add_member(Member("M23", n2, n3, E, A))
truss.add_member(Member("M34", n3, n4, E, A))
truss.add_member(Member("M05", n0, n5, E, A))
truss.add_member(Member("M51", n5, n1, E, A))
truss.add_member(Member("M56", n5, n6, E, A))
truss.add_member(Member("M16", n1, n6, E, A))
truss.add_member(Member("M62", n6, n2, E, A))
truss.add_member(Member("M67", n6, n7, E, A))
truss.add_member(Member("M27", n2, n7, E, A))
truss.add_member(Member("M73", n7, n3, E, A))
truss.add_member(Member("M78", n7, n8, E, A))
truss.add_member(Member("M38", n3, n8, E, A))
truss.add_member(Member("M84", n8, n4, E, A))

truss.solve(20)
truss.summary()

say("")
say("-- Beam Analysis --")

let beam = Beam(5.0, 200e9, 8.33e-6)

say("  Beam: L=5m, E=200GPa, I=8.33e-6 m^4")
say("")
say("  Simply supported, 10kN center load:")
say("    max deflection: " + str(round(beam.max_deflection(10000) * 1000, 4)) + " mm")
say("    max bending moment: " + str(round(beam.max_bending_moment(10000), 1)) + " Nm")
say("    max shear: " + str(round(beam.max_shear(10000), 1)) + " N")
say("")
say("  Cantilever, 10kN end load:")
say("    max deflection: " + str(round(beam.cantilever_deflection(10000) * 1000, 4)) + " mm")
say("    max bending moment: " + str(round(beam.cantilever_moment(10000), 1)) + " Nm")
say("")
say("  Simply supported, 5kN/m uniform load:")
say("    max deflection: " + str(round(beam.uniform_deflection(5000) * 1000, 4)) + " mm")
say("")
say("  Euler buckling (K=1.0):")
say("    Pcr = " + str(round(beam.euler_buckling(1.0), 0)) + " N")
