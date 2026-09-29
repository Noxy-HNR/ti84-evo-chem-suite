# CHEMCORE.py -- shared element data for the CHEM 1450 suite.
#
# Elements, electron configurations (with the 19 measured exceptions),
# ions, table positions, valence electrons and Hund's-rule boxes. Used
# by PTABLE and FORMULA; pure Python, no calculator imports.
#
# Kept lean on purpose: a program imports this with
#     from CHEMCORE import *
# and the calculator has to compile the whole file in memory to do it.
# At 38 KB it ran out (MemoryError on every program that imported it),
# so the Lewis, polarity and Rydberg code now live elsewhere. Comments
# instead of docstrings: the parser allocates docstrings, not comments.
# Importing runs this file, so it only defines names.

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


def mass_text(z):
    # The mass exactly as tabulated, e.g. '22.99' -- its decimal
    # places set how far a molar-mass sum can be rounded.
    return _rec(z)[2]


def find(query):
    # Accept an atomic number, a symbol or a full name. -> Z or None.
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


ORB = "spdfgh"


def _madelung():
    # Subshells as (n, l) in Aufbau order: increasing n+l, ties by n.
    out = []
    for s in range(1, 12):              # s = n + l
        for n in range(1, s + 1):       # n ascending -> l descending
            l = s - n
            if 0 <= l < n:
                out.append((n, l))
    return tuple(out)


ORDER = _madelung()


# Ground states that break strict Aufbau, as {(n, l): electrons} that
# replace the Aufbau count; 0 empties a subshell (Pd is 5s0). Checked
# against PubChem: measured configurations, not computed ones.
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
    # Electrons that fit in a subshell of azimuthal number l: 2(2l+1).
    return 4 * l + 2


def aufbau_configuration(z):
    # Strict Aufbau fill, no exceptions applied. -> [(n, l, count), ...]
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
    # Ground-state configuration, Aufbau order, exceptions applied.
    #
    # Returns [(n, l, count), ...] in filling order, which is the order
    # CHEM 1450 asks you to write it in (4s before 3d).
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


def ion_configuration(z, charge=0):
    # Textbook isolated-ion model, not measured configurations for every ion.
    #
    # Positive charge removes highest-n electrons first (ns before (n-1)d).
    # Negative charge fills the next available subshell; limited to main-group
    # anions up to the next noble gas. Does not model ligand-field splitting.
    if z != int(z) or not 1 <= z <= element_count():
        raise ValueError("Atomic number must be 1-118")
    if charge != int(charge) or not -4 <= charge <= 8 or charge > z:
        raise ValueError("Charge must be -4 to +8")
    if charge == 0:
        return electron_configuration(z)
    counts = {}
    for n, l, count in electron_configuration(z):
        counts[(n, l)] = count
    if charge > 0:
        # Remove the outer shell first, then reverse filling order. Using n alone
        # throughout would incorrectly remove core 5p before valence 4f in Sm3+.
        outer_n = max(n for n, l in counts)
        removal = sorted(counts, key=lambda key: (key[0] == outer_n,
                         key[0] + key[1], key[0]), reverse=True)
        for key in removal:
            take = min(charge, counts[key])
            counts[key] -= take
            charge -= take
            if charge == 0:
                break
    else:
        next_noble = None
        for noble in (2, 10, 18, 36, 54, 86, 118):
            if noble > z:
                next_noble = noble
                break
        if (block_of(z) not in ("s", "p") or next_noble is None
                or z - charge > next_noble or group_of(z) == 18):
            raise ValueError("Use a main-group anion")
        left = -charge
        for key in ORDER:
            put = min(left, capacity(key[1]) - counts.get(key, 0))
            counts[key] = counts.get(key, 0) + put
            left -= put
            if not left:
                break
    return [(n, l, counts.get((n, l), 0)) for n, l in ORDER
            if counts.get((n, l), 0) > 0]


def ion_label(z, charge):
    if charge == 0:
        return symbol(z)
    return symbol(z) + str(abs(charge)) + ("+" if charge > 0 else "-")


def is_exception(z):
    return z in EXCEPTIONS


def config_string(shells):
    # '1s2 2s2 2p6 ...' full form, no noble-gas shorthand.
    parts = []
    for (n, l, c) in shells:
        parts.append(str(n) + ORB[l] + str(c))
    return " ".join(parts)


def subshell_label(n, l):
    return str(n) + ORB[l]


# Columns 1..18; rows 1..7 main, 8 and 9 the lanthanide/actinide strips.
def table_position(z):
    # -> (column, row). Rows 8 and 9 are the f-block strips.
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
    # 1..18, or None for the lanthanide / actinide strips.
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


def valence_electrons(z):
    # Electrons in the outermost shell (n == period), plus the
    # (n-1)d electrons for the d block and the (n-2)f / (n-1)d electrons
    # for the f block -- the usual general-chemistry convention.
    #
    # Keying on the period rather than on the largest occupied n is what
    # keeps palladium right: Pd is 4d10 with an empty 5s, so "largest n
    # present" would answer 18 instead of 10.
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


def hund_fill(l, count):
    # Fill the 2l+1 orbitals following Hund's rule.
    #
    # Returns one entry per orbital, each 0, 1 or 2: every orbital takes
    # a single spin-up electron before any of them takes a second.
    boxes = [0] * (2 * l + 1)
    for e in range(count):
        boxes[e % len(boxes)] += 1
    return boxes


def unpaired(boxes):
    u = 0
    for b in boxes:
        if b == 1:
            u += 1
    return u


METALLOIDS = ("B", "Si", "Ge", "As", "Sb", "Te")


NONMETALS = ("H", "He", "C", "N", "O", "F", "Ne", "P", "S", "Cl", "Ar",
             "Se", "Br", "Kr", "I", "Xe", "Rn")


def element_kind(sym):
    # 'metal', 'metalloid' or 'nonmetal' -- the staircase split the
    # 9/14 notes use to call a compound ionic or covalent.
    if sym in NONMETALS:
        return "nonmetal"
    if sym in METALLOIDS:
        return "metalloid"
    return "metal"
