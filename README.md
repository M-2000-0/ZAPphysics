# ZapPhysics

**Physics & Chemistry simulation engine written entirely in Zap**

ZapPhysics is a complete physics and chemistry simulation engine built from scratch in the [Zap programming language](https://github.com/M-2000-0/ZAP). It provides 2D particle dynamics, collision detection, molecular modeling, chemical reactions, thermodynamics, and tensor-based N-body calculations -- all in ~670 lines of pure Zap code.

## Features

### Physics Engine
- **Vec2** -- 2D vector math (add, subtract, scale, dot product, normalize, distance)
- **Particle** -- Mass, position, velocity, force accumulation, kinetic energy, momentum
- **World** -- Gravity, boundary enforcement, collision resolution, energy tracking, center of mass
- **Force Laws** -- Gravitational attraction, Hooke's law springs, viscous drag
- **Collisions** -- Elastic collision detection & impulse response with overlap resolution

### Chemistry Engine
- **Element** -- Atomic properties (symbol, mass, electronegativity, valence)
- **Molecule** -- Molecular mass, bond energy, polarity calculations
- **Reaction** -- Reactants, products, enthalpy, exothermic/endothermic classification, energy-per-gram
- **Thermodynamics** -- Ideal gas law, Gibbs free energy, entropy, Kelvin conversion
- **Pre-built molecules** -- H2O, CO2, CH4, NaCl, H2, O2, Fe2O3, H2SO4

### Tensor Physics
- Pairwise distance matrices for N-body systems
- Gravitational force matrices using Zap's native tensor operations

## Quick Start

### Prerequisites
- [Zap language](https://github.com/M-2000-0/ZAP) installed and on your PATH

### Run the demos
```bash
zap run zapphysics.zap
```

This runs all 5 demo simulations:
1. **Orbital Mechanics** -- Star with 3 orbiting bodies under mutual gravity
2. **Spring-Mass System** -- Damped harmonic oscillations with Hooke's law
3. **Elastic Collisions** -- 3-body collision dynamics with impulse resolution
4. **Chemistry Lab** -- Molecule properties, reactions, and thermodynamics
5. **Tensor N-body** -- Force matrix computation using Zap tensors

## Architecture

```
zapphysics.zap
├── Vec2              (lines 8-41)    2D vector operations
├── Particle          (lines 45-72)   Point-mass with force accumulation
├── Force Laws        (lines 76-94)   Gravity, springs, drag
├── Collision         (lines 98-118)  Elastic impulse-based collision
├── World             (lines 122-203) Simulation container & integrator
├── Element           (lines 211-265) Periodic table data
├── Molecule          (lines 310-341) Molecular modeling
├── Reaction          (lines 370-419) Chemical reaction tracking
├── Thermodynamics    (lines 423-437) Gas laws & Gibbs energy
└── Demos             (lines 444-646) 5 runnable simulations
```

## Example Output

```
==============================================
  ZapPhysics v1.0
  Physics & Chemistry engine for Zap
==============================================

=== PHYSICS DEMO: Orbital Mechanics ===

-- Initial state --
=== PHYSICS WORLD SUMMARY ===
  time: 0s
  steps: 0
  particles: 4
  total energy: 0.5831
  center of mass: (-0.01, -0.02)
  Star@(0,0) vel=(0,0) KE=0
  Planet-A@(10,0) vel=(0,8) KE=32
  Planet-B@(0,-12) vel=(6,0) KE=36
  Comet@(-15,5) vel=(3,2) KE=0.65
```

## Physics Formulas Implemented

| Formula | Implementation |
|---------|---------------|
| Newton's gravity | `F = G * m1 * m2 / r^2` |
| Hooke's law | `F = -k * (x - x0)` |
| Kinetic energy | `KE = 0.5 * m * v^2` |
| Ideal gas law | `PV = nRT` |
| Gibbs free energy | `G = H - TdS` |
| Impulse-based collision | `j = -(1+e) * v_n / (1/m1 + 1/m2)` |
| Center of mass | `R = sum(mi * ri) / sum(mi)` |

## Built With Zap

This engine demonstrates Zap's capabilities for scientific computing:
- **Classes** with methods for clean OOP design
- **List comprehensions** and `for` loops for iteration
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
