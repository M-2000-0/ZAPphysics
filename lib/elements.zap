# ═══════════════════════════════════════════════════════════════════
# ZapPhysics — Elements: All 118 elements of the periodic table
# ═══════════════════════════════════════════════════════════════════

class Element:
  fn init(self, symbol, name, atomic_number, mass)
    self.symbol = symbol
    self.name = name
    self.atomic_number = atomic_number
    self.mass = mass
    self.electronegativity = 0
    self.valence = 1

  fn repr(self)
    self.symbol

# --- Period 1 ---
let H = Element("H", "Hydrogen", 1, 1.008)
H.electronegativity = 2.20
H.valence = 1

let He = Element("He", "Helium", 2, 4.003)
He.electronegativity = 0
He.valence = 0

# --- Period 2 ---
let Li = Element("Li", "Lithium", 3, 6.941)
Li.electronegativity = 0.98
Li.valence = 1

let Be = Element("Be", "Beryllium", 4, 9.012)
Be.electronegativity = 1.57
Be.valence = 2

let B = Element("B", "Boron", 5, 10.81)
B.electronegativity = 2.04
B.valence = 3

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

let Ne = Element("Ne", "Neon", 10, 20.180)
Ne.electronegativity = 0
Ne.valence = 0

# --- Period 3 ---
let Na = Element("Na", "Sodium", 11, 22.990)
Na.electronegativity = 0.93
Na.valence = 1

let Mg = Element("Mg", "Magnesium", 12, 24.305)
Mg.electronegativity = 1.31
Mg.valence = 2

let Al = Element("Al", "Aluminium", 13, 26.982)
Al.electronegativity = 1.61
Al.valence = 3

let Si = Element("Si", "Silicon", 14, 28.086)
Si.electronegativity = 1.90
Si.valence = 4

let P = Element("P", "Phosphorus", 15, 30.974)
P.electronegativity = 2.19
P.valence = 3

let S = Element("S", "Sulfur", 16, 32.06)
S.electronegativity = 2.58
S.valence = 2

let Cl = Element("Cl", "Chlorine", 17, 35.45)
Cl.electronegativity = 3.16
Cl.valence = 1

let Ar = Element("Ar", "Argon", 18, 39.948)
Ar.electronegativity = 0
Ar.valence = 0

# --- Period 4 ---
let K = Element("K", "Potassium", 19, 39.098)
K.electronegativity = 0.82
K.valence = 1

let Ca = Element("Ca", "Calcium", 20, 40.078)
Ca.electronegativity = 1.00
Ca.valence = 2

let Sc = Element("Sc", "Scandium", 21, 44.956)
Sc.electronegativity = 1.36
Sc.valence = 3

let Ti = Element("Ti", "Titanium", 22, 47.867)
Ti.electronegativity = 1.54
Ti.valence = 4

let V = Element("V", "Vanadium", 23, 50.942)
V.electronegativity = 1.63
V.valence = 5

let Cr = Element("Cr", "Chromium", 24, 51.996)
Cr.electronegativity = 1.66
Cr.valence = 6

let Mn = Element("Mn", "Manganese", 25, 54.938)
Mn.electronegativity = 1.55
Mn.valence = 7

let Fe = Element("Fe", "Iron", 26, 55.845)
Fe.electronegativity = 1.83
Fe.valence = 3

let Co = Element("Co", "Cobalt", 27, 58.933)
Co.electronegativity = 1.88
Co.valence = 3

let Ni = Element("Ni", "Nickel", 28, 58.693)
Ni.electronegativity = 1.91
Ni.valence = 2

let Cu = Element("Cu", "Copper", 29, 63.546)
Cu.electronegativity = 1.90
Cu.valence = 2

let Zn = Element("Zn", "Zinc", 30, 65.38)
Zn.electronegativity = 1.65
Zn.valence = 2

let Ga = Element("Ga", "Gallium", 31, 69.723)
Ga.electronegativity = 1.81
Ga.valence = 3

let Ge = Element("Ge", "Germanium", 32, 72.63)
Ge.electronegativity = 2.01
Ge.valence = 4

let As = Element("As", "Arsenic", 33, 74.922)
As.electronegativity = 2.18
As.valence = 3

let Se = Element("Se", "Selenium", 34, 78.971)
Se.electronegativity = 2.55
Se.valence = 2

let Br = Element("Br", "Bromine", 35, 79.904)
Br.electronegativity = 2.96
Br.valence = 1

let Kr = Element("Kr", "Krypton", 36, 83.798)
Kr.electronegativity = 3.00
Kr.valence = 0

# --- Period 5 ---
let Rb = Element("Rb", "Rubidium", 37, 85.468)
Rb.electronegativity = 0.82
Rb.valence = 1

let Sr = Element("Sr", "Strontium", 38, 87.62)
Sr.electronegativity = 0.95
Sr.valence = 2

let Y = Element("Y", "Yttrium", 39, 88.906)
Y.electronegativity = 1.22
Y.valence = 3

let Zr = Element("Zr", "Zirconium", 40, 91.224)
Zr.electronegativity = 1.33
Zr.valence = 4

let Nb = Element("Nb", "Niobium", 41, 92.906)
Nb.electronegativity = 1.6
Nb.valence = 5

let Mo = Element("Mo", "Molybdenum", 42, 95.95)
Mo.electronegativity = 2.16
Mo.valence = 6

let Tc = Element("Tc", "Technetium", 43, 98)
Tc.electronegativity = 1.9
Tc.valence = 7

let Ru = Element("Ru", "Ruthenium", 44, 101.07)
Ru.electronegativity = 2.2
Ru.valence = 8

let Rh = Element("Rh", "Rhodium", 45, 102.91)
Rh.electronegativity = 2.28
Rh.valence = 6

let Pd = Element("Pd", "Palladium", 46, 106.42)
Pd.electronegativity = 2.20
Pd.valence = 4

let Ag = Element("Ag", "Silver", 47, 107.87)
Ag.electronegativity = 1.93
Ag.valence = 1

let Cd = Element("Cd", "Cadmium", 48, 112.41)
Cd.electronegativity = 1.69
Cd.valence = 2

let In = Element("In", "Indium", 49, 114.82)
In.electronegativity = 1.78
In.valence = 3

let Sn = Element("Sn", "Tin", 50, 118.71)
Sn.electronegativity = 1.96
Sn.valence = 4

let Sb = Element("Sb", "Antimony", 51, 121.76)
Sb.electronegativity = 2.05
Sb.valence = 3

let Te = Element("Te", "Tellurium", 52, 127.60)
Te.electronegativity = 2.1
Te.valence = 2

let I = Element("I", "Iodine", 53, 126.90)
I.electronegativity = 2.66
I.valence = 1

let Xe = Element("Xe", "Xenon", 54, 131.29)
Xe.electronegativity = 2.6
Xe.valence = 0

# --- Period 6 ---
let Cs = Element("Cs", "Cesium", 55, 132.91)
Cs.electronegativity = 0.79
Cs.valence = 1

let Ba = Element("Ba", "Barium", 56, 137.33)
Ba.electronegativity = 0.89
Ba.valence = 2

let La = Element("La", "Lanthanum", 57, 138.91)
La.electronegativity = 1.1
La.valence = 3

let Ce = Element("Ce", "Cerium", 58, 140.12)
Ce.electronegativity = 1.12
Ce.valence = 3

let Pr = Element("Pr", "Praseodymium", 59, 140.91)
Pr.electronegativity = 1.13
Pr.valence = 3

let Nd = Element("Nd", "Neodymium", 60, 144.24)
Nd.electronegativity = 1.14
Nd.valence = 3

let Pm = Element("Pm", "Promethium", 61, 145)
Pm.electronegativity = 1.13
Pm.valence = 3

let Sm = Element("Sm", "Samarium", 62, 150.36)
Sm.electronegativity = 1.17
Sm.valence = 3

let Eu = Element("Eu", "Europium", 63, 151.96)
Eu.electronegativity = 1.2
Eu.valence = 3

let Gd = Element("Gd", "Gadolinium", 64, 157.25)
Gd.electronegativity = 1.2
Gd.valence = 3

let Tb = Element("Tb", "Terbium", 65, 158.93)
Tb.electronegativity = 1.1
Tb.valence = 3

let Dy = Element("Dy", "Dysprosium", 66, 162.50)
Dy.electronegativity = 1.22
Dy.valence = 3

let Ho = Element("Ho", "Holmium", 67, 164.93)
Ho.electronegativity = 1.23
Ho.valence = 3

let Er = Element("Er", "Erbium", 68, 167.26)
Er.electronegativity = 1.24
Er.valence = 3

let Tm = Element("Tm", "Thulium", 69, 168.93)
Tm.electronegativity = 1.25
Tm.valence = 3

let Yb = Element("Yb", "Ytterbium", 70, 173.05)
Yb.electronegativity = 1.1
Yb.valence = 3

let Lu = Element("Lu", "Lutetium", 71, 174.97)
Lu.electronegativity = 1.27
Lu.valence = 3

let Hf = Element("Hf", "Hafnium", 72, 178.49)
Hf.electronegativity = 1.3
Hf.valence = 4

let Ta = Element("Ta", "Tantalum", 73, 180.95)
Ta.electronegativity = 1.5
Ta.valence = 5

let W = Element("W", "Tungsten", 74, 183.84)
W.electronegativity = 2.36
W.valence = 6

let Re = Element("Re", "Rhenium", 75, 186.21)
Re.electronegativity = 1.9
Re.valence = 7

let Os = Element("Os", "Osmium", 76, 190.23)
Os.electronegativity = 2.2
Os.valence = 8

let Ir = Element("Ir", "Iridium", 77, 192.22)
Ir.electronegativity = 2.20
Ir.valence = 6

let Pt = Element("Pt", "Platinum", 78, 195.08)
Pt.electronegativity = 2.28
Pt.valence = 4

let Au = Element("Au", "Gold", 79, 196.97)
Au.electronegativity = 2.54
Au.valence = 3

let Hg = Element("Hg", "Mercury", 80, 200.59)
Hg.electronegativity = 2.00
Hg.valence = 2

let Tl = Element("Tl", "Thallium", 81, 204.38)
Tl.electronegativity = 1.62
Tl.valence = 1

let Pb = Element("Pb", "Lead", 82, 207.2)
Pb.electronegativity = 1.87
Pb.valence = 2

let Bi = Element("Bi", "Bismuth", 83, 208.98)
Bi.electronegativity = 2.02
Bi.valence = 3

let Po = Element("Po", "Polonium", 84, 209)
Po.electronegativity = 2.0
Po.valence = 4

let At = Element("At", "Astatine", 85, 210)
At.electronegativity = 2.2
At.valence = 1

let Rn = Element("Rn", "Radon", 86, 222)
Rn.electronegativity = 2.2
Rn.valence = 0

# --- Period 7 ---
let Fr = Element("Fr", "Francium", 87, 223)
Fr.electronegativity = 0.7
Fr.valence = 1

let Ra = Element("Ra", "Radium", 88, 226)
Ra.electronegativity = 0.9
Ra.valence = 2

let Ac = Element("Ac", "Actinium", 89, 227)
Ac.electronegativity = 1.1
Ac.valence = 3

let Th = Element("Th", "Thorium", 90, 232.04)
Th.electronegativity = 1.3
Th.valence = 4

let Pa = Element("Pa", "Protactinium", 91, 231.04)
Pa.electronegativity = 1.5
Pa.valence = 5

let U = Element("U", "Uranium", 92, 238.03)
U.electronegativity = 1.38
U.valence = 6

let Np = Element("Np", "Neptunium", 93, 237)
Np.electronegativity = 1.36
Np.valence = 7

let Pu = Element("Pu", "Plutonium", 94, 244)
Pu.electronegativity = 1.28
Pu.valence = 8

let Am = Element("Am", "Americium", 95, 243)
Am.electronegativity = 1.13
Am.valence = 8

let Cm = Element("Cm", "Curium", 96, 247)
Cm.electronegativity = 1.28
Cm.valence = 8

let Bk = Element("Bk", "Berkelium", 97, 247)
Bk.electronegativity = 1.3
Bk.valence = 8

let Cf = Element("Cf", "Californium", 98, 251)
Cf.electronegativity = 1.3
Cf.valence = 8

let Es = Element("Es", "Einsteinium", 99, 252)
Es.electronegativity = 1.3
Es.valence = 8

let Fm = Element("Fm", "Fermium", 100, 257)
Fm.electronegativity = 1.3
Fm.valence = 8

let Md = Element("Md", "Mendelevium", 101, 258)
Md.electronegativity = 1.3
Md.valence = 8

let No = Element("No", "Nobelium", 102, 259)
No.electronegativity = 1.3
No.valence = 8

let Lr = Element("Lr", "Lawrencium", 103, 266)
Lr.electronegativity = 1.3
Lr.valence = 3

let Rf = Element("Rf", "Rutherfordium", 104, 267)
Rf.electronegativity = 0
Rf.valence = 4

let Db = Element("Db", "Dubnium", 105, 268)
Db.electronegativity = 0
Db.valence = 5

let Sg = Element("Sg", "Seaborgium", 106, 269)
Sg.electronegativity = 0
Sg.valence = 6

let Bh = Element("Bh", "Bohrium", 107, 270)
Bh.electronegativity = 0
Bh.valence = 7

let Hs = Element("Hs", "Hassium", 108, 277)
Hs.electronegativity = 0
Hs.valence = 8

let Mt = Element("Mt", "Meitnerium", 109, 278)
Mt.electronegativity = 0
Mt.valence = 3

let Ds = Element("Ds", "Darmstadtium", 110, 281)
Ds.electronegativity = 0
Ds.valence = 4

let Rg = Element("Rg", "Roentgenium", 111, 282)
Rg.electronegativity = 0
Rg.valence = 3

let Cn = Element("Cn", "Copernicium", 112, 285)
Cn.electronegativity = 0
Cn.valence = 2

let Nh = Element("Nh", "Nihonium", 113, 286)
Nh.electronegativity = 0
Nh.valence = 3

let Fl = Element("Fl", "Flerovium", 114, 289)
Fl.electronegativity = 0
Fl.valence = 4

let Mc = Element("Mc", "Moscovium", 115, 290)
Mc.electronegativity = 0
Mc.valence = 5

let Lv = Element("Lv", "Livermorium", 116, 293)
Lv.electronegativity = 0
Lv.valence = 6

let Ts = Element("Ts", "Tennessine", 117, 294)
Ts.electronegativity = 0
Ts.valence = 7

let Og = Element("Og", "Oganesson", 118, 294)
Og.electronegativity = 0
Og.valence = 8
