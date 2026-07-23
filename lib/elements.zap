# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Elements: Periodic table data
# ═══════════════════════════════════════════════════════════════════

class Element:
  fn init(self, symbol, name, atomic_number, mass)
    self.symbol = symbol
    self.name = name
    self.atomic_number = atomic_number
    self.mass = mass
    self.electronegativity = 2.5
    self.valence = 1

  fn repr(self)
    self.symbol

let H = Element("H", "Hydrogen", 1, 1.008)
H.electronegativity = 2.20
H.valence = 1

let He = Element("He", "Helium", 2, 4.003)
He.electronegativity = 0
He.valence = 0

let C = Element("C", "Carbon", 6, 12.011)
C.electronegativity = 2.55
C.valence = 4

let N = Element("N", "Nitrogen", 7, 14.007)
N.electronegativity = 3.04
N.valence = 3

let O = Element("O", "Oxygen", 8, 15.999)
O.electronegativity = 3.44
O.valence = 2

let F = Element("F", "Fluorine", 9, 18.998)
F.electronegativity = 3.98
F.valence = 1

let Na = Element("Na", "Sodium", 11, 22.990)
Na.electronegativity = 0.93
Na.valence = 1

let Cl = Element("Cl", "Chlorine", 17, 35.45)
Cl.electronegativity = 3.16
Cl.valence = 1

let Fe = Element("Fe", "Iron", 26, 55.845)
Fe.electronegativity = 1.83
Fe.valence = 3

let S = Element("S", "Sulfur", 16, 32.06)
S.electronegativity = 2.58
S.valence = 2

let Ca = Element("Ca", "Calcium", 20, 40.078)
Ca.electronegativity = 1.00
Ca.valence = 2

let Mg = Element("Mg", "Magnesium", 12, 24.305)
Mg.electronegativity = 1.31
Mg.valence = 2

let P = Element("P", "Phosphorus", 15, 30.974)
P.electronegativity = 2.19
P.valence = 3

let K = Element("K", "Potassium", 19, 39.098)
K.electronegativity = 0.82
K.valence = 1

let Ca_elem = Ca
