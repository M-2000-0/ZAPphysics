# ZapPhysics

**Physics & Chemistry simulation engine written entirely in Zap**

ZapPhysics is a modular physics and chemistry simulation engine built from scratch in the [Zap programming language](https://github.com/M-2000-0/ZAP). It provides 2D particle dynamics, collision detection, molecular modeling, chemical reactions, thermodynamics, and tensor-based N-body calculations.

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
zap run examples/springs.zap
zap run examples/collisions.zap
zap run examples/chemistry.zap
zap run examples/tensor.zap
```

## Project Structure

```
ZAPphysics/
├── main.zap                       # Entry point — runs all demos
│
├── lib/                           # Physics & chemistry modules
│   ├── vec2.zap                   # 2D vector operations
│   ├── particle.zap               # Point-mass with force accumulation
│   ├── forces.zap                 # Gravity, springs, drag, Coulomb
│   ├── collision.zap              # Elastic impulse-based collision
│   ├── world.zap                  # Simulation container & integrator
│   ├── elements.zap               # Periodic table (14 elements)
│   ├── molecule.zap               # Molecular modeling & bond energy
│   ├── reaction.zap               # Chemical reaction tracking
│   └── thermo.zap                 # Thermodynamics & gas laws
│
├── examples/                      # Demo simulations
│   ├── orbital.zap                # Orbital mechanics (gravity N-body)
│   ├── springs.zap                # Spring-mass system (Hooke's law)
│   ├── collisions.zap             # Elastic collisions
│   ├── chemistry.zap              # Molecules, reactions, thermodynamics
│   └── tensor.zap                 # Tensor N-body force matrix
│
└── zapphysics.zap                 # Monolithic version (all-in-one)
```

## Modules

### Physics Engine

| Module | Classes/Functions | Description |
|--------|------------------|-------------|
| `lib/vec2.zap` | `Vec2`, `vec2()` | 2D vector math: add, sub, scale, dot, normalize, dist, rotate, lerp |
| `lib/particle.zap` | `Particle` | Point-mass with position, velocity, force, kinetic energy, momentum |
| `lib/forces.zap` | `gravity()`, `spring_force()`, `drag_force()`, `coulomb_force()`, `damping_force()` | Force law implementations |
| `lib/collision.zap` | `collide()`, `check_collision()` | Elastic impulse-based collision detection & resolution |
| `lib/world.zap` | `World` | Simulation container: global forces, collision resolution, bounds, energy, center of mass, momentum |

### Chemistry Engine

| Module | Classes/Functions | Description |
|--------|------------------|-------------|
| `lib/elements.zap` | `Element`, H, He, C, N, O, F, Na, Cl, Fe, S, Ca, Mg, P, K | Periodic table with atomic properties |
| `lib/molecule.zap` | `Molecule`, `bond()`, 9 constructors | Molecular mass, bond energy, polarity, formula |
| `lib/reaction.zap` | `Reaction` | Reactants, products, enthalpy, exothermic/endothermic, mass conservation |
| `lib/thermo.zap` | 10 functions | Ideal gas law, Gibbs energy, Boltzmann, Arrhenius, heat capacity, RMS speed |

### New Functions (v2.0)

- `Vec2.rotate(theta)` — rotate vector by angle
- `Vec2.lerp(other, t)` — linear interpolation
- `Vec2.angle()` — angle from x-axis
- `Particle.speed()` — scalar speed
- `coulomb_force()` — electromagnetic force
- `damping_force()` — velocity-proportional drag
- `Molecule.formula()` — auto-generate chemical formula
- `Reaction.mass_conserved()` — check mass conservation
- `arrhenius_rate()` — reaction rate kinetics
- `root_mean_square_speed()` — molecular speed from temperature
- `boltzmann_probability()` — energy-probability distribution
- `heat_capacity_cv()`, `heat_capacity_cp()` — specific heat

## Physics Formulas

| Formula | Implementation |
|---------|---------------|
| Newton's gravity | `F = G * m1 * m2 / r^2` |
| Coulomb's law | `F = k * q1 * q2 / r^2` |
| Hooke's law | `F = -k * (x - x0)` |
| Kinetic energy | `KE = 0.5 * m * v^2` |
| Ideal gas law | `PV = nRT` |
| Gibbs free energy | `G = H - TdS` |
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

## Roadmap

- [ ] 3D vector support and 3D particle simulation
- [ ] Electromagnetic force simulation (Coulomb's law)
- [ ] Fluid dynamics (SPH - Smoothed Particle Hydrodynamics)
- [ ] Rigid body rotation and torque
- [ ] Structural engineering analysis (truss/beam solvers)
- [ ] Game physics library (platformer, top-down, ragdoll)
- [ ] Generative art via particle systems
- [ ] Real-time visualization output
- [ ] Periodic table with all 118 elements
- [ ] Reaction kinetics and rate equations

## License

MIT

## Author

[M-2000-0](https://github.com/M-2000-0)
