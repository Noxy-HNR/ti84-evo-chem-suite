# POLAR.py -- bond and molecule polarity for the TI-84 Evo.
#
#     Bond polarity     pick two atoms: EN values, the difference, the
#                       bond type, and which way the dipole arrow points
#     Rank bonds        up to four bonds sorted most to least polar
#     Molecule rule     the 9/23 quick rule: symmetric shape AND
#                       identical outer atoms -> nonpolar
#     Class problem     the 9/25 slide answers (HCl, HF, F2, N2, NaCl)
#
# Uses the course's textbook electronegativities (F 4.0, O 3.5, N 3.0,
# Cl 3.0, C 2.5, H 2.1) and cutoffs: below 0.4 nonpolar covalent, 0.4
# to 2.0 polar covalent, above 2.0 ionic. Needs CHEMCORE.py.

import ti_draw as d
import ti_system as tis
# Free the garbage left from compiling this program before the next
# import has to find room. Harmless where gc is missing.
try:
    import gc
    gc.collect()
except:
    pass
from POLCORE import *

LEFT = 24
UP = 25
RIGHT = 26
DOWN = 34
SECOND = 21
CLEAR = 45
ENTER = 105

WHITE = (248, 250, 249)
BLACK = (25, 40, 48)
NAVY = (24, 47, 56)
GREY = (102, 121, 128)
PALE = (224, 235, 232)
TEAL = (15, 112, 94)
RED = (178, 57, 57)
GOLD = (239, 211, 147)

# Every element with a stored textbook EN, in atomic-number order
EN_LIST = EN_ORDER

BUFFERED = False
try:
    if hasattr(d, "use_buffer") and hasattr(d, "paint_buffer"):
        d.use_buffer()
        BUFFERED = True
except:
    BUFFERED = False


def color(rgb):
    d.set_color(rgb[0], rgb[1], rgb[2])


def present():
    if BUFFERED:
        d.paint_buffer()


def screen():
    color(WHITE)
    d.fill_rect(0, 0, 320, 210)


def header(text):
    color(NAVY)
    d.fill_rect(0, 0, 320, 25)
    color(TEAL)
    d.fill_rect(0, 24, 320, 2)
    color(WHITE)
    d.draw_text(5, 19, text[:31])


def footer(text):
    color(NAVY)
    d.fill_rect(0, 190, 320, 20)
    color(TEAL)
    d.fill_rect(0, 190, 320, 2)
    color(WHITE)
    d.draw_text(5, 207, text[:31])


def step(sym, by):
    return EN_LIST[(EN_LIST.index(sym) + by) % len(EN_LIST)]


# ----------------------------------------------------------------------
# One bond
# ----------------------------------------------------------------------

def draw_arrow(x1, x2, y):
    # Dipole arrow from the d+ end (x1) to the d- end (x2), with the
    # small cross on the tail that marks the positive end.
    d.draw_line(x1, y, x2, y)
    d.draw_line(x1, y - 1, x2, y - 1)
    head = 7 if x2 > x1 else -7
    d.fill_poly([x2, x2 - head, x2 - head], [y, y - 5, y + 5])
    d.draw_line(x1 + (4 if x2 > x1 else -4), y - 6,
                x1 + (4 if x2 > x1 else -4), y + 5)


def draw_bond(a, b):
    delta, kind, neg = bond_polarity(a, b)
    ea = en_text(a)
    eb = en_text(b)
    screen()
    header("POLAR: " + a + "-" + b + " bond")

    ax, bx, y = 90, 230, 70
    ionic = kind == "ionic"
    if not ionic:
        color(BLACK)
        d.draw_line(ax + len(a) * 5 + 8, y - 5, bx - len(b) * 5 - 8, y - 5)
    for sym, x in ((a, ax), (b, bx)):
        color(NAVY)
        d.draw_text(x - len(sym) * 5, y + 2, sym)
        if neg is None:
            continue
        if ionic:
            color(RED)
            d.draw_text(x + len(sym) * 5 + 1, y - 10,
                        "-" if sym == neg else "+")
        else:
            color(RED if sym == neg else TEAL)
            d.draw_text(x - 10, y - 20, "d-" if sym == neg else "d+")
    if neg is not None and not ionic:
        color(RED)
        if neg == b:
            draw_arrow(ax + 8, bx - 8, 92)
        else:
            draw_arrow(bx - 8, ax + 8, 92)

    color(BLACK)
    d.draw_text(8, 116, a + " " + tenths(ea) + "    " + b + " "
                + tenths(eb))
    hi, lo = (ea, eb) if ea >= eb else (eb, ea)
    d.draw_text(8, 133, "dEN = " + tenths(hi) + " - " + tenths(lo) + " = "
                + tenths(delta))
    color(TEAL)
    d.draw_text(8, 150, kind)
    notes = bond_caveat(a, b)
    if ionic:
        lines = ["e- transferred: no bond line"]
    elif neg is None:
        lines = ["same pull: no dipole arrow"]
    else:
        lines = ["arrow points to " + neg + " (d-)"]
    if notes:
        lines = notes
    color(GREY)
    for i, text in enumerate(lines[:2]):
        d.draw_text(8, 167 + i * 17, text[:30])
    footer("2ND MORE  CLEAR BACK")
    present()
    return notes


def bond_detail(a, b, notes):
    # Second screen: the cutoff scale and any course caveats.
    delta, kind, neg = bond_polarity(a, b)
    screen()
    header("POLAR: " + a + "-" + b + " notes")
    color(BLACK)
    rows = ["Course cutoffs (9/25):",
            "  < 0.4   nonpolar covalent",
            "  0.4-2.0 polar covalent",
            "  > 2.0   ionic",
            "This bond: " + tenths(delta)]
    rows.extend(["  " + n for n in notes])
    if neg is not None and kind != "ionic":
        rows.append("Arrow: from " + (a if neg == b else b) + " (+) to "
                    + neg + " (-)")
    for i, text in enumerate(rows[:8]):
        color(TEAL if i == 4 else BLACK)
        d.draw_text(8, 48 + i * 17, text[:30])
    footer("ANY KEY: BACK")
    present()
    tis.wait_key()


def pick_bond():
    a, b = "H", "Cl"
    side = 1
    while True:
        screen()
        header("POLAR: pick two atoms")
        for i, sym in enumerate((a, b)):
            x = 60 + i * 130
            active = i == side
            color(NAVY if active else PALE)
            d.fill_rect(x - 10, 60, 90, 56)
            color(WHITE if active else BLACK)
            d.draw_text(x + 35 - len(sym) * 5, 94, sym)
            color(TEAL if active else GREY)
            d.draw_text(x + 35 - 15, 138, tenths(en_text(sym)))
        color(GREY)
        d.draw_text(8, 164, "L/R atom  UP/DN element")
        d.draw_text(8, 181, "EN from the textbook table")
        footer("ENT CHECK  CLEAR BACK")
        present()
        key = tis.wait_key()
        if key == CLEAR:
            return
        if key in (LEFT, RIGHT):
            side = 1 - side
        elif key in (UP, DOWN):
            by = 1 if key == UP else -1
            if side == 0:
                a = step(a, by)
            else:
                b = step(b, by)
        elif key == ENTER:
            while True:
                notes = draw_bond(a, b)
                k = tis.wait_key()
                if k == SECOND:
                    bond_detail(a, b, notes)
                else:
                    break


# ----------------------------------------------------------------------
# Ranking several bonds
# ----------------------------------------------------------------------

def rank_bonds():
    # the classic hydrogen-halide set, ready to edit
    slots = ["H", "F", "H", "Cl", "H", "Br", "H", "I"]
    pos = 1
    while True:
        screen()
        header("POLAR: rank 4 bonds")
        for row in range(4):
            y = 56 + row * 26
            for col in range(2):
                i = row * 2 + col
                x = 60 + col * 110
                if i == pos:
                    color(NAVY)
                    d.fill_rect(x - 6, y - 17, 60, 22)
                    color(WHITE)
                else:
                    color(BLACK)
                d.draw_text(x + 24 - len(slots[i]) * 5, y, slots[i])
            color(GREY)
            d.draw_text(144, y, "-")
            d.draw_text(8, y, str(row + 1) + ".")
        color(GREY)
        d.draw_text(8, 172, "L/R move  UP/DN element")
        footer("ENT RANK  CLEAR BACK")
        present()
        key = tis.wait_key()
        if key == CLEAR:
            return
        if key == LEFT:
            pos = (pos - 1) % 8
        elif key == RIGHT:
            pos = (pos + 1) % 8
        elif key in (UP, DOWN):
            slots[pos] = step(slots[pos], 1 if key == UP else -1)
        elif key == ENTER:
            show_ranking(slots)


def show_ranking(slots):
    bonds = []
    for row in range(4):
        a, b = slots[row * 2], slots[row * 2 + 1]
        delta, kind, neg = bond_polarity(a, b)
        bonds.append((delta, a + "-" + b, kind))
    bonds.sort(key=lambda t: -t[0])
    screen()
    header("POLAR: most -> least")
    top = bonds[0][0] if bonds[0][0] else 1
    for i, (delta, label, kind) in enumerate(bonds):
        y = 54 + i * 30
        color(BLACK)
        d.draw_text(8, y, str(i + 1) + ". " + label)
        d.draw_text(118, y, tenths(delta))
        # bar length stands in for arrow size (9/23 notes)
        width = 1 + (130 * delta) // top if delta else 1
        color(RED if kind == "ionic" else (TEAL if delta else GREY))
        d.fill_rect(170, y - 12, width, 10)
    # label both ends outright, as the instructor asks (9/4 notes)
    color(TEAL)
    d.draw_text(8, 172, "top = MOST, bottom = LEAST")
    ties = [bonds[i][1] for i in range(3) if bonds[i][0] == bonds[i + 1][0]]
    if ties:
        color(GREY)
        d.draw_text(8, 186, "(equal dEN values tie)")
    footer("ANY KEY: BACK")
    present()
    tis.wait_key()


# ----------------------------------------------------------------------
# The molecule rule
# ----------------------------------------------------------------------

SHAPE_ORDER = ((2, 0, "CO2"), (3, 0, "BF3"), (3, 1, "SO2"), (4, 0, "CH4"),
               (4, 1, "NH3"), (4, 2, "H2O"), (5, 0, "PCl5"), (5, 1, "SF4"),
               (5, 2, "ClF3"), (5, 3, "XeF2"), (6, 0, "SF6"),
               (6, 1, "BrF5"), (6, 2, "XeF4"))


def molecule_rule():
    sel = 3
    same = True
    polar_bonds = True
    field = 0
    while True:
        groups, lp, example = SHAPE_ORDER[sel]
        shape, angle = SHAPES[(groups, lp)]
        n = groups - lp
        outer = ["X"] * n if same else ["X"] * (n - 1) + ["Y"]
        kinds = ["polar covalent" if polar_bonds else "nonpolar covalent"] * n
        is_polar, why = molecule_polarity(groups, lp, outer, kinds)

        screen()
        header("POLAR: molecule rule")
        rows = (("Shape", shape + " (" + example + ")"),
                ("Outer atoms", "all same" if same else "not all same"),
                ("Bonds", "polar" if polar_bonds else "nonpolar"))
        for i, (label, value) in enumerate(rows):
            y = 60 + i * 34
            if i == field:
                color(PALE)
                d.fill_rect(4, y - 30, 312, 34)
            color(GREY)
            d.draw_text(8, y - 14, label)
            color(TEAL if i == field else BLACK)
            d.draw_text(8, y + 2, ("<" + value + ">")[:30])
        symmetric = (groups, lp) in SYMMETRIC
        color(GREY)
        d.draw_text(8, 158, "Symmetric shape: "
                    + ("yes" if symmetric else "no"))
        color(RED if is_polar else TEAL)
        d.draw_text(8, 177, ("POLAR" if is_polar else "NONPOLAR") + ": "
                    + why[:20])
        footer("UP/DN ROW  L/R CHANGE  CLR")
        present()

        key = tis.wait_key()
        if key == CLEAR:
            return
        if key == UP:
            field = (field - 1) % 3
        elif key == DOWN:
            field = (field + 1) % 3
        elif key in (LEFT, RIGHT):
            by = 1 if key == RIGHT else -1
            if field == 0:
                sel = (sel + by) % len(SHAPE_ORDER)
            elif field == 1:
                same = not same
            else:
                polar_bonds = not polar_bonds


# ----------------------------------------------------------------------
# The 9/25 class problem
# ----------------------------------------------------------------------

def class_problem():
    rows = [("HCl", "H", "Cl", "ionic*"),
            ("HF", "H", "F", "polar"),
            ("F2", "F", "F", "nonpolar"),
            ("N2", "N", "N", "nonpolar"),
            ("NaCl", "Na", "Cl", "ionic")]
    screen()
    header("POLAR: 9/25 class problem")
    color(GREY)
    d.draw_text(8, 44, "cmpd  dEN  key answer")
    for i, (name, a, b, key) in enumerate(rows):
        delta = bond_polarity(a, b)[0]
        y = 64 + i * 19
        color(BLACK)
        d.draw_text(8, y, name)
        d.draw_text(68, y, tenths(delta))
        color(RED if key.startswith("ionic") else TEAL)
        d.draw_text(118, y, key)
    color(GREY)
    d.draw_text(8, 164, "*HCl in water = acid, ionic;")
    d.draw_text(8, 181, " pure gas: polar (dEN 0.9)")
    footer("ANY KEY: BACK")
    present()
    tis.wait_key()


# ----------------------------------------------------------------------

ITEMS = ("Bond polarity (2 atoms)", "Rank 4 bonds", "Molecule rule (9/23)",
         "Class problem (9/25)")


def main():
    sel = 0
    while True:
        screen()
        header("POLAR: bonds & molecules")
        for i, item in enumerate(ITEMS):
            y = 58 + i * 26
            if i == sel:
                color(PALE)
                d.fill_rect(4, y - 17, 312, 22)
                color(TEAL)
            else:
                color(BLACK)
            d.draw_text(14, y, item)
        color(GREY)
        d.draw_text(8, 168, "EN: F 4.0 O 3.5 N 3.0 C 2.5")
        d.draw_text(8, 185, "cutoffs 0.4 and 2.0")
        footer("UP/DN MOVE ENT OPEN CLR EXIT")
        present()
        key = tis.wait_key()
        if key == CLEAR:
            break
        if key == UP:
            sel = (sel - 1) % len(ITEMS)
        elif key == DOWN:
            sel = (sel + 1) % len(ITEMS)
        elif key == ENTER:
            if sel == 0:
                pick_bond()
            elif sel == 1:
                rank_bonds()
            elif sel == 2:
                molecule_rule()
            else:
                class_problem()
    screen()
    present()


main()
