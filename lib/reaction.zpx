# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Reaction: Chemical reaction tracking
# ═══════════════════════════════════════════════════════════════════

class Reaction:
  fn init(self, name, reactants, products, enthalpy)
    self.name = name
    self.reactants = reactants
    self.products = products
    self.enthalpy = enthalpy

  fn is_exothermic(self)
    self.enthalpy < 0

  fn is_endothermic(self)
    self.enthalpy > 0

  fn total_reactant_mass(self)
    let m = 0
    for mol in self.reactants:
      m = m + mol.molecular_mass()
    m

  fn total_product_mass(self)
    let m = 0
    for mol in self.products:
      m = m + mol.molecular_mass()
    m

  fn energy_per_gram(self)
    let mass = self.total_reactant_mass()
    if mass > 0:
      self.enthalpy / mass
    el:
      0

  fn mass_conserved(self)
    abs(self.total_reactant_mass() - self.total_product_mass()) < 0.001

  fn repr(self)
    let r = ""
    let first = true
    for mol in self.reactants:
      if first:
        r = mol.name
        first = false
      el:
        r = r + " + " + mol.name
    let p = ""
    first = true
    for mol in self.products:
      if first:
        p = mol.name
        first = false
      el:
        p = p + " + " + mol.name
    r + " -> " + p + "  (dH=" + str(self.enthalpy) + " kJ/mol)"
