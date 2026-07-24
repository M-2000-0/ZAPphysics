# ZapPhysics v4.0

**Physics, Chemistry & Engineering simulation engine written entirely in Zap**

ZapPhysics is a modular physics, chemistry, and engineering simulation engine built from scratch in the [Zap programming language](https://github.com/M-2000-0/ZAP). It provides 2D particle dynamics, collision detection, molecular modeling, chemical reactions, thermodynamics, tensor-based N-body calculations, rocket propulsion, aerodynamics, orbital mechanics, and flight dynamics.

## Quick Start

### Prerequisites
- [Zap language](https://github.com/M-2000-0/ZAP) installed and on your PATH

### Run all demos
```bash
zap run main.zap
```

### Run a single demo
```bash
zap run examples/orbital.zap
zap run examples/demo_rocket.zap
zap run examples/demo_flight.zap
zap run examples/demo_orbital_mechanics.zap
```

## Project Structure

```
ZAPphysics/
├── main.zap                       # Entry point — runs all demos
│
├── lib/                           # Physics, chemistry & engineering modules
│   ├── vec2.zap                   # 2D vector operations
│   ├── vec3.zap                   # 3D vector operations
│   ├── particle.zap               # Point-mass with force accumulation
│   ├── particle3d.zap             # 3D point-mass particle
│   ├── forces.zap                 # Gravity (with softening), springs, drag, Coulomb
│   ├── collision.zap              # Elastic impulse-based collision
│   ├── world.zap                  # Simulation container & integrator (KE+PE energy)
│   ├── em.zap                     # Electromagnetic forces (Coulomb, Lorentz)
│   ├── sph.zap                    # SPH fluid dynamics
│   ├── rigid.zap                  # Rigid body rotation & torque
│   ├── structural.zap             # Truss & beam engineering analysis
│   ├── rocket.zap                 # Rocket propulsion & multi-stage design
│   ├── aero.zap                   # Aerodynamics & flight mechanics
│   ├── orbital_mechanics.zap      # Orbital elements, Hohmann transfers, interplanetary
│   ├── flight.zap                 # Flight dynamics & control surfaces
│   ├── elements.zap               # Periodic table (118 elements)
│   ├── molecule.zap               # Molecular modeling & bond energy
│   ├── reaction.zap               # Chemical reaction tracking
│   ├── thermo.zap                 # Thermodynamics & gas laws
│   ├── kinetics.zap               # Reaction rate equations & equilibrium
│   ├── visual.zap                 # ASCII visualization (charts, heatmaps, fields)
│   ├── visualize.zap              # HTML+Canvas visualization via built-in HTTP server
│   ├── broadphase.zap             # Uniform Grid & Quadtree collision broadphase
│   └── art.zap                    # Generative art particle systems
│
├── examples/                      # Demo simulations
│   ├── orbital.zap                # Orbital mechanics (gravity N-body, energy conservation)
│   ├── springs.zap                # Spring-mass system (Hooke's law)
│   ├── collisions.zap             # Elastic collisions
│   ├── chemistry.zap              # Molecules, reactions, thermodynamics
│   ├── tensor.zap                 # Tensor N-body force matrix
│   ├── demo3d.zap                 # 3D particle simulation
│   ├── demo_em.zap                # Electromagnetic forces
│   ├── demo_fluid.zap             # SPH fluid dynamics
│   ├── demo_rigid.zap             # Rigid body rotation & torque
│   ├── demo_structural.zap        # Truss & beam analysis
│   ├── demo_game.zap              # Game physics (platformer, ragdoll)
│   ├── demo_art.zap               # Generative art particle systems
│   ├── demo_visual.zap            # ASCII visualization
│   ├── demo_elements.zap          # Periodic table (118 elements)
│   ├── demo_kinetics.zap          # Reaction kinetics
│   ├── demo_broadphase.zap        # Uniform Grid & Quadtree collision detection
│   ├── demo_rocket.zap            # Rocket design & flight simulation
│   ├── demo_flight.zap            # Airplane design & flight dynamics
│   ├── demo_orbital3d.zap         # 3D orbital mechanics
│   ├── demo_lambert.zap           # Lambert's problem solver
│   └── demo_porkchop.zap          # Porkchop plot for launch windows
│
└── zapphysics.zap                 # Monolithic version (all-in-one)
```

## Modules

### Physics Engine

| Module | Classes/Functions | Description |
|--------|------------------|-------------|
| `lib/vec2.zap` | `Vec2`, `vec2()` | 2D vector math: add, sub, scale, dot, normalize, dist, rotate, lerp |
| `lib/vec3.zap` | `Vec3`, `vec3()` | 3D vector math: cross, rotate, project, reject |
| `lib/particle.zap` | `Particle` | Point-mass with position, velocity, force, kinetic energy, momentum |
| `lib/forces.zap` | `gravity()`, `spring_force()`, `drag_force()`, `coulomb_force()`, `damping_force()`, `gravity_potential()` | Force laws with softening for gravity |
| `lib/collision.zap` | `collide()`, `check_collision()` | Elastic impulse-based collision detection & resolution |
| `lib/world.zap` | `World` | Simulation container: gravity forces, collision, bounds, KE+PE energy, center of mass, momentum |

### Advanced Physics

| Module | Classes/Functions | Description |
|--------|------------------|-------------|
| `lib/em.zap` | `Charge`, `coulomb_force()`, `electric_field()`, `lorentz_force()` | Coulomb's law, electric fields, Lorentz force |
| `lib/sph.zap` | `FluidParticle`, `FluidWorld` | Smoothed Particle Hydrodynamics fluid simulation |
| `lib/rigid.zap` | `RigidBody` | Rigid body rotation, torque, angular momentum, inertia |
| `lib/broadphase.zap` | `UniformGrid`, `Quadtree` | Spatial partitioning for fast collision detection |

### Engineering Modules

| Module | Classes/Functions | Description |
|--------|------------------|-------------|
| `lib/rocket.zap` | `RocketEngine`, `RocketStage`, `Rocket` | Tsiolkovsky equation, multi-stage design, thrust curves, flight simulation |
| `lib/aero.zap` | `Airfoil`, `Airplane` | Lift/drag coefficients, airfoil analysis, flight performance, glide ratio |
| `lib/orbital_mechanics.zap` | `OrbitalElements`, `OrbitPropagator`, `InterplanetaryTransfer` | Hohmann transfers, bi-elliptic, orbital elements, interplanetary trajectories |
| `lib/flight.zap` | `FlightVehicle`, `ControlSurface`, `FlightEnvelope` | Angle of attack, stability, control surfaces, flight envelopes |
| `lib/structural.zap` | `Node`, `Member`, `Truss`, `Beam` | Truss analysis, beam deflection, buckling, bending stress |

### Chemistry Engine

| Module | Classes/Functions | Description |
|--------|------------------|-------------|
| `lib/elements.zap` | `Element`, H, He, C, N, O, F, Na, Cl, Fe, S, Ca, Mg, P, K | Periodic table with atomic properties (118 elements) |
| `lib/molecule.zap` | `Molecule`, `bond()` | Molecular mass, bond energy, polarity, formula |
| `lib/reaction.zap` | `Reaction` | Reactants, products, enthalpy, exothermic/endothermic, mass conservation |
| `lib/thermo.zap` | 10 functions | Ideal gas law, Gibbs energy, Boltzmann, Arrhenius, heat capacity, RMS speed |
| `lib/kinetics.zap` | 8 functions | Reaction rate equations, equilibrium constants |

### Visualization

| Module | Classes/Functions | Description |
|--------|------------------|-------------|
| `lib/visual.zap` | `ascii_render_particles()`, `ascii_heatmap()`, `ascii_bar_chart()`, `ascii_sparkline()`, `ascii_vector_field()`, `ascii_box()` | ASCII visualization for terminal output |
| `lib/visualize.zap` | `orbital_viz_html()`, `rocket_viz_html()`, `flight_viz_html()`, `serve_viz()`, `save_viz()` | HTML+Canvas visualization served via Zap's built-in HTTP server |
| `lib/art.zap` | `Emitter`, `GravityWell`, `ArtWorld` | Generative art particle systems |

## Key Features

### Energy Conservation (Fixed)
The orbital mechanics simulation now correctly tracks both kinetic and potential energy:
- `World.total_energy()` returns KE + PE (gravitational potential energy)
- Gravitational softening prevents singularities at close range (softening parameter = 5.0)
- Energy drift is now < 0.2% for orbital simulations (was > 1000% before)

### HTML+Canvas Visualization
Zap is both backend and frontend — it computes physics and serves interactive visualizations:
- `orbital_viz_html()` — particle positions, trails, energy charts
- `rocket_viz_html()` — rocket cross-section, thrust curves, trajectories
- `flight_viz_html()` — flight paths, altitude/velocity profiles
- `serve_viz()` — starts a web server to view visualizations in a browser
- `save_viz()` — saves visualizations to files

### Rocket Engineering
- Tsiolkovsky rocket equation
- Multi-stage rocket design
- Common engines: Merlin 1D, Raptor, F-1, RS-25, Rutherford
- Thrust curve generation
- Flight trajectory simulation with gravity and drag losses

### Aerodynamics
- Airfoil analysis (NACA 2412, NACA 0012, Clark Y, Wortmann FX 60-153)
- Lift and drag coefficient calculations
- Best glide speed and ratio
- Stall speed calculations
- Flight envelope analysis

### Orbital Mechanics
- Hohmann transfers (LEO to GEO, LEO to Moon)
- Bi-elliptic transfers
- Orbital elements from state vectors
- Interplanetary transfers (Earth to Mars)
- Oberth effect calculations
- Gravity assist calculations

### Flight Dynamics
- Control surface modeling (elevator, aileron, rudder)
- Angle of attack and sideslip
- Pitch stability and damping
- Flight envelope (stall, never-exceed, best glide)
- Aircraft: Cessna 172, Boeing 737, F-16

## Physics Formulas

| Formula | Implementation |
|---------|---------------|
| Newton's gravity | `F = G * m1 * m2 / (r^2 + eps^2)` (softened) |
| Gravitational PE | `U = -G * m1 * m2 / sqrt(r^2 + eps^2)` |
| Coulomb's law | `F = k * q1 * q2 / r^2` |
| Hooke's law | `F = -k * (x - x0)` |
| Kinetic energy | `KE = 0.5 * m * v^2` |
| Tsiolkovsky | `dV = Isp * g0 * ln(m0/mf)` |
| Hohmann transfer | `dV = sqrt(mu/r1) * (sqrt(2*r2/(r1+r2)) - 1)` |
| Vis-viva equation | `v^2 = mu * (2/r - 1/a)` |
| Ideal gas law | `PV = nRT` |
| Gibbs free energy | `G = H - TdS` |
| Lift coefficient | `Cl = 2*pi*alpha` (thin airfoil) |
| Drag polar | `Cd = Cd0 + Cl^2 / (pi * AR * e)` |
| Impulse collision | `j = -(1+e) * v_n / (1/m1 + 1/m2)` |
| Center of mass | `R = sum(mi * ri) / sum(mi)` |
| Arrhenius rate | `k = A * exp(-Ea / RT)` |
| RMS speed | `v = sqrt(3RT / M)` |

## Built With Zap

This engine demonstrates Zap's capabilities for scientific computing:
- **Classes** with methods for clean OOP design
- **`import`** for modular multi-file projects
- **Tensors** for matrix-based calculations
- **`say()`/`str()`** with custom `repr()` methods for readable output
- **Higher-order force functions** for composable physics
- **`http_server()`/`serve()`** for built-in web visualization
- **`json_save()`** for file I/O
- **Math functions**: `sqrt`, `log`, `exp`, `sin`, `cos`, `floor`, `ceil`

## License

MIT

## Author

[M-2000-0](https://github.com/M-2000-0)