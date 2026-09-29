# POLCORE.py -- polarity and shape data, shared by POLAR and BONDING.
#
# Tro's one-decimal Pauling electronegativities (the notes' values:
# F 4.0, O 3.5, N 3.0, Cl 3.0, C 2.5, H 2.1) stored as integer TENTHS,
# so 2.5 - 2.1 is exactly 4 (0.4, "barely polar") rather than the
# float 0.3999... that would read as nonpolar. Values that differ
# between textbook editions are left out rather than guessed.
# Pure Python; importing it only defines names.

EN_TEXT = {
    "H": 21,
    "Li": 10, "Be": 15, "B": 20, "C": 25, "N": 30, "O": 35, "F": 40,
    "Na": 9, "Mg": 12, "Al": 15, "Si": 18, "P": 21, "S": 25, "Cl": 30,
    "K": 8, "Ca": 10, "Ti": 15, "Cr": 16, "Mn": 15, "Fe": 18, "Co": 18,
    "Ni": 18, "Cu": 19, "Zn": 16, "Ga": 16, "Ge": 18, "As": 20,
    "Se": 24, "Br": 28,
    "Rb": 8, "Sr": 10, "Ag": 19, "Cd": 17, "Sn": 18, "Sb": 19,
    "Te": 21, "I": 25, "Xe": 26,
    "Cs": 7, "Ba": 9,
}

EN_ORDER = (
    "H", "Li", "Be", "B", "C", "N", "O", "F", "Na", "Mg", "Al", "Si",
    "P", "S", "Cl", "K", "Ca", "Ti", "Cr", "Mn", "Fe", "Co", "Ni", "Cu",
    "Zn", "Ga", "Ge", "As", "Se", "Br", "Rb", "Sr", "Ag", "Cd", "Sn",
    "Sb", "Te", "I", "Xe", "Cs", "Ba",
)


def tenths(value):
    # 21 -> '2.1'. Formats the integer-tenths values above.
    return str(value // 10) + "." + str(value % 10)


def en_text(sym):
    if sym not in EN_TEXT:
        raise ValueError("No textbook EN stored for " + str(sym) + ".")
    return EN_TEXT[sym]


def bond_polarity(a, b):
    # Classify an a-b bond by the course cutoffs (9/25 notes).
    #
    # Below 0.4 nonpolar covalent; 0.4 to 2.0 polar covalent; above 2.0
    # ionic. -> (delta in tenths, kind, negative end or None). The
    # negative end is where the dipole arrow points.
    ea = en_text(a)
    eb = en_text(b)
    delta = abs(ea - eb)
    if delta < 4:
        kind = "nonpolar covalent"
    elif delta <= 20:
        kind = "polar covalent"
    else:
        kind = "ionic"
    neg = None
    if ea > eb:
        neg = a
    elif eb > ea:
        neg = b
    return delta, kind, neg


def bond_caveat(a, b):
    # Where the bare cutoffs and the course disagree, say so.
    #
    # -> list of short lines (28 chars max), empty when there is nothing
    # to add. The cutoffs are rough: Si-F is 2.2 yet F3SiH is drawn as a
    # covalent molecule (9/23), and a metal-nonmetal pair counts as ionic
    # for naming even below 2.0 (9/14).
    pair = (a, b) if a < b else (b, a)
    if pair == ("Cl", "H"):
        return ["Key: ionic* = HCl in water", "Pure gas: polar covalent"]
    delta, kind, neg = bond_polarity(a, b)
    ka = element_kind(a)
    kb = element_kind(b)
    if kind == "ionic" and "metal" not in (ka, kb):
        return ["Both nonmetals: very polar", "covalent in practice"]
    if kind != "ionic" and "metal" in (ka, kb) and (
            "nonmetal" in (ka, kb)):
        return ["Metal + nonmetal: call it", "ionic for naming (9/14)"]
    if delta == 4 or delta == 20:
        return ["On a cutoff: borderline"]
    return []


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


# VSEPR shapes and hybridization (9/16 - 9/28 notes)
GEOMETRY = {2: "linear", 3: "trigonal planar", 4: "tetrahedral",
            5: "trigonal bipyramidal", 6: "octahedral"}
HYBRIDS = {2: "sp", 3: "sp2", 4: "sp3", 5: "sp3d", 6: "sp3d2"}
HYBRID_MIX = {2: "1 s + 1 p", 3: "1 s + 2 p", 4: "1 s + 3 p",
              5: "1 s + 3 p + 1 d", 6: "1 s + 3 p + 2 d"}
# (electron groups, lone pairs) -> (molecular shape, bond angle)
SHAPES = {
    (2, 0): ("linear", "180"),
    (3, 0): ("trigonal planar", "120"),
    (3, 1): ("bent", "<120"),
    (4, 0): ("tetrahedral", "109.5"),
    (4, 1): ("trigonal pyramidal", "<109.5"),
    (4, 2): ("bent", "<109.5"),
    (5, 0): ("trigonal bipyramidal", "90 & 120"),
    (5, 1): ("seesaw", "<90 & <120"),
    (5, 2): ("T-shaped", "<90"),
    (5, 3): ("linear", "180"),
    (6, 0): ("octahedral", "90"),
    (6, 1): ("square pyramidal", "<90"),
    (6, 2): ("square planar", "90"),
}
# shapes where identical outer atoms always cancel (9/23 quick rule)
SYMMETRIC = ((2, 0), (3, 0), (4, 0), (5, 0), (5, 3), (6, 0), (6, 2))


def unhybridized_p(groups):
    # p orbitals a central atom keeps out of its hybrids -- the ones
    # that can make pi bonds. sp keeps 2, sp2 keeps 1, sp3 and up none.
    used = groups - 1
    if used > 3:
        used = 3
    return 3 - used


def molecule_polarity(groups, lone_pairs, outer, bond_kinds):
    # The 9/23 quick rule. outer: outer-atom symbols; bond_kinds:
    # bond_polarity kinds. -> (is_polar, reason).
    if len(outer) == 1:
        if bond_kinds[0] == "nonpolar covalent":
            return False, "one nonpolar bond"
        return True, "one polar bond, can't cancel"
    same = True
    for atom in outer:
        if atom != outer[0]:
            same = False
    if (groups, lone_pairs) in SYMMETRIC and same:
        return False, "symmetric + identical bonds"
    if all(k == "nonpolar covalent" for k in bond_kinds):
        return False, "no polar bonds to add up"
    if not same:
        return True, "outer atoms differ"
    return True, "shape is not symmetric"
