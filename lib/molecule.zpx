# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Molecule: Molecular modeling and bond energy
# ═══════════════════════════════════════════════════════════════════

fn bond(a, b)
  [a, b]

fn bond_energy_value(bond_pair)
  let a1 = bond_pair[0].symbol
  let a2 = bond_pair[1].symbol
  let key = a1 + "-" + a2
  if key == "H-H":
    ret 436
  if key == "O-O":
    ret 146
  if key == "N-N":
    ret 163
  if key == "C-C":
    ret 348
  if key == "C-H":
    ret 413
  if key == "C-O":
    ret 360
  if key == "C-N":
    ret 305
  if key == "O-H":
    ret 463
  if key == "N-H":
    ret 391
  if key == "H-Cl":
    ret 431
  if key == "Na-Cl":
    ret 411
  if key == "C=O":
    ret 799
  if key == "O=O":
    ret 498
  if key == "N=O":
    ret 630
  if key == "Fe-O":
    ret 409
  if key == "S-O":
    ret 265
  if key == "P-O":
    ret 335
  if key == "K-Cl":
    ret 427
  ret 350

class Molecule:
  fn init(self, name, atoms, bonds)
    self.name = name
    self.atoms = atoms
    self.bonds = bonds

  fn molecular_mass(self)
    let total = 0
    for atom in self.atoms:
      total = total + atom.mass
    total

  fn bond_energy(self)
    let energy = 0
    for b in self.bonds:
      energy = energy + bond_energy_value(b)
    energy

  fn polarity(self)
    let diff = 0
    for b in self.bonds:
      let e1 = b[0].electronegativity
      let e2 = b[1].electronegativity
      diff = diff + abs(e1 - e2)
    diff

  fn atom_count(self)
    len(self.atoms)

  fn formula(self)
    let syms = []
    let nums = []
    for atom in self.atoms:
      let sym = atom.symbol
      let found = false
      for k in range(len(syms)):
        if syms[k] == sym:
          nums[k] = nums[k] + 1
          found = true
      if not found:
        syms = syms + [sym]
        nums = nums + [1]
    let result = ""
    for k in range(len(syms)):
      result = result + syms[k]
      if nums[k] > 1:
        result = result + str(nums[k])
    result

  fn repr(self)
    self.name + " (mass=" + str(round(self.molecular_mass(), 3)) + " g/mol)"

# ── Common Molecule Constructors ──────────────────────────────────

fn make_water()
  Molecule("H2O", [H, H, O], [bond(H, O), bond(H, O)])

fn make_co2()
  Molecule("CO2", [C, O, O], [bond(C, O), bond(C, O)])

fn make_methane()
  Molecule("CH4", [C, H, H, H, H], [bond(C, H), bond(C, H), bond(C, H), bond(C, H)])

fn make_nacl()
  Molecule("NaCl", [Na, Cl], [bond(Na, Cl)])

fn make_hydrogen()
  Molecule("H2", [H, H], [bond(H, H)])

fn make_oxygen()
  Molecule("O2", [O, O], [bond(O, O)])

fn make_iron_oxide()
  Molecule("Fe2O3", [Fe, Fe, O, O, O], [bond(Fe, O), bond(Fe, O), bond(Fe, O), bond(Fe, O)])

fn make_sulfuric_acid()
  Molecule("H2SO4", [H, H, S, O, O, O, O], [bond(H, O), bond(H, O), bond(S, O), bond(S, O), bond(S, O), bond(S, O)])

fn make_ammonia()
  Molecule("NH3", [N, H, H, H], [bond(N, H), bond(N, H), bond(N, H)])

fn make_glucose()
  Molecule("C6H12O6", [C, C, C, C, C, C, H, H, H, H, H, H, H, H, H, H, H, H, O, O, O, O, O, O],
           [bond(C, C), bond(C, C), bond(C, C), bond(C, C), bond(C, C),
            bond(C, O), bond(C, O), bond(C, O), bond(C, O), bond(C, O), bond(C, O),
            bond(O, H), bond(O, H), bond(O, H), bond(O, H), bond(O, H), bond(O, H)])
