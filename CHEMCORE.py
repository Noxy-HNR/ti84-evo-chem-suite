"""CHEMCORE.py -- shared chemistry logic for the CHEM 1450 suite.

Pure Python. Nothing here imports ti_draw or ti_system, so every
function can be exercised with plain desktop CPython long before it
reaches the calculator.

Imported by PTABLE.py, ORBITAL.py and RYDBERG.py, each of which is a
separate standalone program with its own menu loop. Transfer this file
to the calculator alongside them.

On TI hardware a cross-program import is written

    from CHEMCORE import *

and importing a program RUNS it, so this module deliberately defines
names and nothing else -- no top-level statements with side effects.

Style notes for the TI-84 Evo Python build:
  * no f-strings -- use .format() or concatenation
  * no file I/O, no typing, no dataclasses
  * element data stays packed in strings; 118 nested tuples costs
    noticeably more RAM than 118 short strings
"""

ELEMENTS = (
    "H|Hydrogen|1.008", "He|Helium|4.0026", "Li|Lithium|6.94",
    "Be|Beryllium|9.0122", "B|Boron|10.81", "C|Carbon|12.011",
    "N|Nitrogen|14.007", "O|Oxygen|15.999", "F|Fluorine|18.998",
    "Ne|Neon|20.18", "Na|Sodium|22.99", "Mg|Magnesium|24.305",
    "Al|Aluminum|26.982", "Si|Silicon|28.085", "P|Phosphorus|30.974",
    "S|Sulfur|32.06", "Cl|Chlorine|35.45", "Ar|Argon|39.948",
    "K|Potassium|39.098", "Ca|Calcium|40.078", "Sc|Scandium|44.956",
    "Ti|Titanium|47.867", "V|Vanadium|50.942", "Cr|Chromium|51.996",
    "Mn|Manganese|54.938", "Fe|Iron|55.845", "Co|Cobalt|58.933",
    "Ni|Nickel|58.693", "Cu|Copper|63.546", "Zn|Zinc|65.38",
    "Ga|Gallium|69.723", "Ge|Germanium|72.63", "As|Arsenic|74.922",
    "Se|Selenium|78.971", "Br|Bromine|79.904", "Kr|Krypton|83.798",
    "Rb|Rubidium|85.468", "Sr|Strontium|87.62", "Y|Yttrium|88.906",
    "Zr|Zirconium|91.224", "Nb|Niobium|92.906", "Mo|Molybdenum|95.95",
    "Tc|Technetium|98.0", "Ru|Ruthenium|101.07", "Rh|Rhodium|102.91",
    "Pd|Palladium|106.42", "Ag|Silver|107.87", "Cd|Cadmium|112.41",
    "In|Indium|114.82", "Sn|Tin|118.71", "Sb|Antimony|121.76",
    "Te|Tellurium|127.6", "I|Iodine|126.9", "Xe|Xenon|131.29",
    "Cs|Cesium|132.91", "Ba|Barium|137.33", "La|Lanthanum|138.91",
    "Ce|Cerium|140.12", "Pr|Praseodymium|140.91", "Nd|Neodymium|144.24",
    "Pm|Promethium|145.0", "Sm|Samarium|150.36", "Eu|Europium|151.96",
    "Gd|Gadolinium|157.25", "Tb|Terbium|158.93", "Dy|Dysprosium|162.5",
    "Ho|Holmium|164.93", "Er|Erbium|167.26", "Tm|Thulium|168.93",
    "Yb|Ytterbium|173.05", "Lu|Lutetium|174.97", "Hf|Hafnium|178.49",
    "Ta|Tantalum|180.95", "W|Tungsten|183.84", "Re|Rhenium|186.21",
    "Os|Osmium|190.23", "Ir|Iridium|192.22", "Pt|Platinum|195.08",
    "Au|Gold|196.97", "Hg|Mercury|200.59", "Tl|Thallium|204.38",
    "Pb|Lead|207.2", "Bi|Bismuth|208.98", "Po|Polonium|209.0",
    "At|Astatine|210.0", "Rn|Radon|222.0", "Fr|Francium|223.0",
    "Ra|Radium|226.0", "Ac|Actinium|227.0", "Th|Thorium|232.04",
    "Pa|Protactinium|231.04", "U|Uranium|238.03", "Np|Neptunium|237.0",
    "Pu|Plutonium|244.0", "Am|Americium|243.0", "Cm|Curium|247.0",
    "Bk|Berkelium|247.0", "Cf|Californium|251.0", "Es|Einsteinium|252.0",
    "Fm|Fermium|257.0", "Md|Mendelevium|258.0", "No|Nobelium|259.0",
    "Lr|Lawrencium|262.0", "Rf|Rutherfordium|267.0", "Db|Dubnium|270.0",
    "Sg|Seaborgium|269.0", "Bh|Bohrium|270.0", "Hs|Hassium|270.0",
    "Mt|Meitnerium|278.0", "Ds|Darmstadtium|281.0", "Rg|Roentgenium|282.0",
    "Cn|Copernicium|285.0", "Nh|Nihonium|286.0", "Fl|Flerovium|289.0",
    "Mc|Moscovium|290.0", "Lv|Livermorium|293.0", "Ts|Tennessine|294.0",
    "Og|Oganesson|294.0",
)

# ----------------------------------------------------------------------
# Element accessors
# ----------------------------------------------------------------------

def element_count():
    return len(ELEMENTS)


def _rec(z):
    return ELEMENTS[z - 1].split("|")


def symbol(z):
    return _rec(z)[0]


def name(z):
    return _rec(z)[1]


def mass(z):
    return float(_rec(z)[2])


def find(query):
    """Accept an atomic number, a symbol or a full name. -> Z or None."""
    q = str(query).strip()
    if q == "":
        return None
    try:
        z = int(q)
        if 1 <= z <= len(ELEMENTS):
            return z
        return None
    except ValueError:
        pass
    q = q.lower()
    for i in range(len(ELEMENTS)):
        if _rec(i + 1)[0].lower() == q:
            return i + 1
    for i in range(len(ELEMENTS)):
        if _rec(i + 1)[1].lower() == q:
            return i + 1
    return None


# ----------------------------------------------------------------------
# Electron configuration
# ----------------------------------------------------------------------

ORB = "spdfgh"


def _madelung():
    """Subshells as (n, l) in Aufbau order: increasing n+l, ties by n."""
    out = []
    for s in range(1, 12):              # s = n + l
        for n in range(1, s + 1):       # n ascending -> l descending
            l = s - n
            if 0 <= l < n:
                out.append((n, l))
    return tuple(out)


ORDER = _madelung()

# Ground-state configurations that depart from strict Aufbau filling.
# Each entry maps Z -> the subshell occupancies that replace the ones
# Aufbau would predict, as {(n, l): electrons}. A count of 0 empties
# that subshell (palladium really is 5s0).
#
# Values checked field-by-field against the PubChem Periodic Table
# dataset. These are measured configurations, not computed ones -- a
# student revising from a "computed" Cr or Cu would learn it wrong.
EXCEPTIONS = {
    24:  {(4, 0): 1, (3, 2): 5},    # Cr  [Ar] 4s1 3d5
    29:  {(4, 0): 1, (3, 2): 10},   # Cu  [Ar] 4s1 3d10
    41:  {(5, 0): 1, (4, 2): 4},    # Nb  [Kr] 5s1 4d4
    42:  {(5, 0): 1, (4, 2): 5},    # Mo  [Kr] 5s1 4d5
    44:  {(5, 0): 1, (4, 2): 7},    # Ru  [Kr] 5s1 4d7
    45:  {(5, 0): 1, (4, 2): 8},    # Rh  [Kr] 5s1 4d8
    46:  {(5, 0): 0, (4, 2): 10},   # Pd  [Kr] 4d10   (no 5s at all)
    47:  {(5, 0): 1, (4, 2): 10},   # Ag  [Kr] 5s1 4d10
    57:  {(4, 3): 0, (5, 2): 1},    # La  [Xe] 6s2 5d1
    58:  {(4, 3): 1, (5, 2): 1},    # Ce  [Xe] 6s2 4f1 5d1
    64:  {(4, 3): 7, (5, 2): 1},    # Gd  [Xe] 6s2 4f7 5d1
    78:  {(6, 0): 1, (5, 2): 9},    # Pt  [Xe] 6s1 4f14 5d9
    79:  {(6, 0): 1, (5, 2): 10},   # Au  [Xe] 6s1 4f14 5d10
    89:  {(5, 3): 0, (6, 2): 1},    # Ac  [Rn] 7s2 6d1
    90:  {(5, 3): 0, (6, 2): 2},    # Th  [Rn] 7s2 6d2
    91:  {(5, 3): 2, (6, 2): 1},    # Pa  [Rn] 7s2 5f2 6d1
    92:  {(5, 3): 3, (6, 2): 1},    # U   [Rn] 7s2 5f3 6d1
    93:  {(5, 3): 4, (6, 2): 1},    # Np  [Rn] 7s2 5f4 6d1
    96:  {(5, 3): 7, (6, 2): 1},    # Cm  [Rn] 7s2 5f7 6d1
}


def capacity(l):
    """Electrons that fit in a subshell of azimuthal number l: 2(2l+1)."""
    return 4 * l + 2


def aufbau_configuration(z):
    """Strict Aufbau fill, no exceptions applied. -> [(n, l, count), ...]"""
    shells = []
    left = z
    for (n, l) in ORDER:
        if left <= 0:
            break
        put = capacity(l)
        if left < put:
            put = left
        shells.append((n, l, put))
        left -= put
    return shells


def electron_configuration(z):
    """Ground-state configuration, Aufbau order, exceptions applied.

    Returns [(n, l, count), ...] in filling order, which is the order
    CHEM 1450 asks you to write it in (4s before 3d).
    """
    shells = aufbau_configuration(z)
    over = EXCEPTIONS.get(z)
    if not over:
        return shells

    counts = {}
    for (n, l, c) in shells:
        counts[(n, l)] = c
    for key in over:
        counts[key] = over[key]

    out = []
    for (n, l) in ORDER:
        c = counts.get((n, l), 0)
        if c > 0:
            out.append((n, l, c))
    return out


def is_exception(z):
    return z in EXCEPTIONS


def config_string(shells):
    """'1s2 2s2 2p6 ...' full form, no noble-gas shorthand."""
    parts = []
    for (n, l, c) in shells:
        parts.append(str(n) + ORB[l] + str(c))
    return " ".join(parts)


def subshell_label(n, l):
    return str(n) + ORB[l]


# ----------------------------------------------------------------------
# Position in the table -> group, period, block
# ----------------------------------------------------------------------
#
# Columns are 1..18. Rows 1..7 are the main rows; rows 8 and 9 hold the
# lanthanide and actinide series as they are printed under the table.

def table_position(z):
    """-> (column, row). Rows 8 and 9 are the f-block strips."""
    if z == 1:
        return 1, 1
    if z == 2:
        return 18, 1
    if 3 <= z <= 4:
        return z - 2, 2
    if 5 <= z <= 10:
        return z + 8, 2
    if 11 <= z <= 12:
        return z - 10, 3
    if 13 <= z <= 18:
        return z, 3
    if 19 <= z <= 36:
        return z - 18, 4
    if 37 <= z <= 54:
        return z - 36, 5
    if 55 <= z <= 56:
        return z - 54, 6
    if 57 <= z <= 71:
        return z - 54, 8            # lanthanides, columns 3..17
    if 72 <= z <= 86:
        return z - 68, 6            # columns 4..18
    if 87 <= z <= 88:
        return z - 86, 7
    if 89 <= z <= 103:
        return z - 86, 9            # actinides, columns 3..17
    return z - 100, 7               # 104..118 -> columns 4..18


def period_of(z):
    col, row = table_position(z)
    if row == 8:
        return 6
    if row == 9:
        return 7
    return row


def group_of(z):
    """1..18, or None for the lanthanide / actinide strips."""
    col, row = table_position(z)
    if row >= 8:
        return None
    return col


def block_of(z):
    col, row = table_position(z)
    if row >= 8:
        return "f"
    if z == 2:
        return "s"                  # helium sits in group 18 but is 1s2
    if col <= 2:
        return "s"
    if col <= 12:
        return "d"
    return "p"


def series_name(z):
    if 57 <= z <= 71:
        return "Lanthanide"
    if 89 <= z <= 103:
        return "Actinide"
    return None


def group_label(z):
    g = group_of(z)
    if g is None:
        return series_name(z) + " series"
    return str(g)


# ----------------------------------------------------------------------
# Valence electrons
# ----------------------------------------------------------------------

def valence_electrons(z):
    """Electrons in the outermost shell (n == period), plus the
    (n-1)d electrons for the d block and the (n-2)f / (n-1)d electrons
    for the f block -- the usual general-chemistry convention.

    Keying on the period rather than on the largest occupied n is what
    keeps palladium right: Pd is 4d10 with an empty 5s, so "largest n
    present" would answer 18 instead of 10.
    """
    p = period_of(z)
    b = block_of(z)
    v = 0
    for (n, l, c) in electron_configuration(z):
        if n == p:
            v += c
        elif b == "d" and l == 2 and n == p - 1:
            v += c
        elif b == "f" and ((l == 3 and n == p - 2) or (l == 2 and n == p - 1)):
            v += c
    return v


# ----------------------------------------------------------------------
# Hund's rule orbital filling
# ----------------------------------------------------------------------

def parse_subshell(text):
    """Parse notation like '2p4', '3d 7', '1S2'. -> (n, l, count).

    Raises ValueError carrying a message short enough to draw on screen.
    """
    s = str(text).strip().lower().replace(" ", "")
    if len(s) < 2:
        raise ValueError("Too short. Try 2p4.")

    i = 0
    while i < len(s) and s[i].isdigit():
        i += 1
    if i == 0:
        raise ValueError("Start with n, e.g. 2p4.")
    n = int(s[:i])

    if i >= len(s):
        raise ValueError("Missing subshell letter.")
    letter = s[i]
    if letter not in ORB:
        raise ValueError("Letter must be s p d f g h.")
    l = ORB.index(letter)
    i += 1

    if i >= len(s):
        count = capacity(l)          # a bare "2p" means a full 2p
    else:
        rest = s[i:]
        if not rest.isdigit():
            raise ValueError("Electron count must be a number.")
        count = int(rest)

    if n < 1:
        raise ValueError("n must be 1 or more.")
    if l >= n:
        raise ValueError("No " + str(n) + ORB[l] + " subshell exists.")
    if count > capacity(l):
        raise ValueError(str(n) + ORB[l] + " holds at most "
                         + str(capacity(l)) + ".")
    return n, l, count


def hund_fill(l, count):
    """Fill the 2l+1 orbitals following Hund's rule.

    Returns one entry per orbital, each 0, 1 or 2: every orbital takes
    a single spin-up electron before any of them takes a second.
    """
    boxes = [0] * (2 * l + 1)
    for e in range(count):
        boxes[e % len(boxes)] += 1
    return boxes


def fill_sequence(l, count):
    """The order electrons land in, as a list of orbital indexes.

    Entry k is where electron k goes, so an animation can just walk the
    list one step at a time. Same Hund ordering as hund_fill.
    """
    width = 2 * l + 1
    return [e % width for e in range(count)]


def unpaired(boxes):
    u = 0
    for b in boxes:
        if b == 1:
            u += 1
    return u


def magnetism(boxes):
    """-> 'Paramagnetic' or 'Diamagnetic'."""
    if unpaired(boxes) > 0:
        return "Paramagnetic"
    return "Diamagnetic"


def outermost_subshell(z):
    """The last subshell to receive electrons. -> (n, l, count)."""
    return electron_configuration(z)[-1]


def box_row_text(boxes):
    """Plain-text orbital diagram, handy when testing on a desktop.
    A single electron is 'u', a pair is 'ud'."""
    cells = []
    for b in boxes:
        if b == 0:
            cells.append("[  ]")
        elif b == 1:
            cells.append("[u ]")
        else:
            cells.append("[ud]")
    return "".join(cells)


# ----------------------------------------------------------------------
# Rydberg and photon energy
# ----------------------------------------------------------------------
#
# The CHEM 1450 formula sheet gives the Rydberg constant in nm^-1, so
# every wavelength in this module is in nanometres.

RB = 1.097e-2          # nm^-1
PLANCK = 6.626e-34     # J s
LIGHT = 2.998e8        # m/s
AVOGADRO = 6.022e23    # 1/mol
HC_NM = PLANCK * LIGHT * 1e9   # J nm, so that E = HC_NM / lambda(nm)


def sci(x, digits=4):
    """Format a number to `digits` SIGNIFICANT figures.

    Significant figures, not decimal places: the Rydberg constant on
    the formula sheet carries four of them, so reporting a wavelength
    as 656.3355 nm would claim precision the input never had.

    The exponent comes from formatting rather than from math.log10,
    which keeps this module free of imports.
    """
    if x == 0:
        return "0"
    s = "{:.{d}e}".format(x, d=digits - 1)
    mant, exp = s.split("e")
    exp = int(exp)
    if -4 < exp < 5:
        # close enough to 1 to write out longhand
        dec = digits - 1 - exp
        if dec <= 0:
            # more whole digits than we are entitled to show, so round
            # off the mantissa instead of printing the lot
            return "{:.0f}".format(float(mant) * (10 ** exp))
        out = "{:.{d}f}".format(x, d=dec)
        if "." in out:
            out = out.rstrip("0").rstrip(".")
        return out
    if "." in mant:
        mant = mant.rstrip("0").rstrip(".")
    return mant + "e" + str(exp)


def photon_energy(lam_nm):
    """E = hc / lambda, with lambda in nm -> joules."""
    return HC_NM / lam_nm


def energy_steps(lam_nm):
    """Worked lines for E = hc/lambda. -> (steps, energy_J)"""
    e = photon_energy(lam_nm)
    return [
        "E = hc / L",
        "E = (6.626e-34)(2.998e8)",
        "     / (" + sci(lam_nm) + " x 1e-9 m)",
        "E = " + sci(e) + " J",
    ], e


def from_levels(ni, nf):
    """Mode 1: given ni and nf, find lambda and E.

    -> (lambda_nm, energy_J, steps, kind), kind being 'emission'
    when the electron falls and 'absorption' when it climbs.
    """
    if ni < 1 or nf < 1:
        raise ValueError("n must be 1 or more.")
    if ni == nf:
        raise ValueError("ni and nf must differ.")

    inv = RB * (1.0 / (nf * nf) - 1.0 / (ni * ni))
    kind = "emission" if inv > 0 else "absorption"
    lam = 1.0 / abs(inv)
    steps = [
        "1/L = Rb (1/nf^2 - 1/ni^2)",
        "1/L = 1.097e-2 (1/" + str(nf) + "^2",
        "       - 1/" + str(ni) + "^2)",
        "1/L = 1.097e-2 x",
        "   (" + sci(1.0 / (nf * nf), 3)
        + " - " + sci(1.0 / (ni * ni), 3) + ")",
        "1/L = " + sci(inv) + " /nm",
    ]
    if kind == "absorption":
        steps.append("negative -> absorption")
    steps.append("L = 1 / " + sci(abs(inv)))
    steps.append("L = " + sci(lam) + " nm")
    esteps, e = energy_steps(lam)
    steps.extend(esteps)
    return lam, e, steps, kind


def _nearest_int(x):
    return int(x + 0.5)


def solve_for_n(lam_nm, known_n, known_is):
    """Mode 2: given lambda and one level, find the other level.

    known_is is 'nf' or 'ni'. -> (raw, nearest, steps), or
    (None, None, steps) when no level fits. A real transition needs a
    whole number, so the raw value and the nearest integer both come
    back and the caller can show the gap between them.
    """
    if lam_nm <= 0:
        raise ValueError("Wavelength must be positive.")
    if known_n < 1:
        raise ValueError("n must be 1 or more.")

    inv = 1.0 / (RB * lam_nm)
    k2 = 1.0 / (known_n * known_n)
    steps = [
        "1/L = Rb (1/nf^2 - 1/ni^2)",
        "1/(Rb L) = 1/nf^2 - 1/ni^2",
        "1/(1.097e-2 x " + sci(lam_nm) + ")",
        "   = " + sci(inv),
    ]

    if known_is == "nf":
        target = k2 - inv           # 1/ni^2 = 1/nf^2 - 1/(Rb L)
        steps.append("1/ni^2 = 1/" + str(known_n) + "^2 - " + sci(inv))
        label = "ni"
    else:
        target = k2 + inv           # 1/nf^2 = 1/(Rb L) + 1/ni^2
        steps.append("1/nf^2 = " + sci(inv) + " + 1/" + str(known_n) + "^2")
        label = "nf"

    steps.append("1/" + label + "^2 = " + sci(target))
    if target <= 0:
        steps.append("No level fits that L.")
        return None, None, steps

    raw = (1.0 / target) ** 0.5
    near = _nearest_int(raw)
    steps.append(label + " = sqrt(1 / " + sci(target) + ")")
    steps.append(label + " = " + sci(raw))
    steps.append("nearest whole n = " + str(near))
    return raw, near, steps


def energy_to_wavelength(e_j):
    """lambda = hc / E, with E in joules -> nm."""
    if e_j <= 0:
        raise ValueError("Energy must be positive.")
    return HC_NM / e_j


def from_molar_energy(kj_per_mol):
    """Mode 3: kJ/mol -> J per photon by way of Avogadro, then lambda.

    -> (energy_J, lambda_nm, steps)
    """
    if kj_per_mol <= 0:
        raise ValueError("Energy must be positive.")
    j_per_mol = kj_per_mol * 1000.0
    e = j_per_mol / AVOGADRO
    lam = energy_to_wavelength(e)
    steps = [
        sci(kj_per_mol) + " kJ/mol x 1000",
        "   = " + sci(j_per_mol) + " J/mol",
        "E = (J/mol) / Na",
        "E = " + sci(j_per_mol) + " / 6.022e23",
        "E = " + sci(e) + " J/photon",
        "L = hc / E",
        "L = 1.986e-25 / " + sci(e),
        "L = " + sci(lam) + " nm",
    ]
    return e, lam, steps


# ----------------------------------------------------------------------
# Visible spectrum helpers
# ----------------------------------------------------------------------

VIS_MIN = 380.0
VIS_MAX = 700.0


def visible_color(lam_nm):
    """Approximate sRGB for a visible wavelength. -> (r, g, b).
    Outside 380-700 nm this returns a dark grey."""
    L = lam_nm
    if L < VIS_MIN or L > VIS_MAX:
        return 60, 60, 60
    if L < 440:
        r, g, b = -(L - 440) / 60.0, 0.0, 1.0
    elif L < 490:
        r, g, b = 0.0, (L - 440) / 50.0, 1.0
    elif L < 510:
        r, g, b = 0.0, 1.0, -(L - 510) / 20.0
    elif L < 580:
        r, g, b = (L - 510) / 70.0, 1.0, 0.0
    elif L < 645:
        r, g, b = 1.0, -(L - 645) / 65.0, 0.0
    else:
        r, g, b = 1.0, 0.0, 0.0
    if L < 420:                      # dim the ends the way the eye sees them
        f = 0.3 + 0.7 * (L - 380) / 40.0
    elif L > 645:
        f = 0.3 + 0.7 * (700 - L) / 55.0
    else:
        f = 1.0
    return int(r * f * 255), int(g * f * 255), int(b * f * 255)


def is_visible(lam_nm):
    return VIS_MIN <= lam_nm <= VIS_MAX


def spectrum_region(lam_nm):
    if lam_nm < 10:
        return "X-ray"
    if lam_nm < VIS_MIN:
        return "Ultraviolet"
    if lam_nm <= VIS_MAX:
        return "Visible"
    if lam_nm < 1e6:
        return "Infrared"
    return "Microwave"


SERIES = (
    (1, "Lyman", "UV"),
    (2, "Balmer", "visible"),
    (3, "Paschen", "IR"),
    (4, "Brackett", "IR"),
    (5, "Pfund", "IR"),
)


def series_for(nf):
    for (n, nm, where) in SERIES:
        if n == nf:
            return nm + " (" + where + ")"
    return None
