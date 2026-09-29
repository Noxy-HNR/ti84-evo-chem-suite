# FORMULA.py -- molar mass and empirical formulas for the TI-84 Evo.
#
#     Molar mass       build a formula; get the mass with the work shown,
#                      % by mass, the empirical formula (lowest ratio),
#                      and whether it is ionic or covalent
#     % -> empirical   percent (or gram) data -> moles -> divide by the
#                      smallest -> whole numbers; add a molar mass to get
#                      the molecular formula
#
# Editing works the same everywhere: LEFT/RIGHT moves between boxes,
# UP/DOWN changes the box, ZOOM/TRACE jumps by 10. Needs CHEMCORE.py.

import ti_draw as d
import ti_system as tis
# Free the garbage left from compiling this program before the next
# import has to find room. Harmless where gc is missing.
try:
    import gc
    gc.collect()
except:
    pass
from CHEMCORE import *

# Formula math, carried here: only FORMULA uses it, and keeping it out
# of CHEMCORE keeps that module small enough to compile on the Evo.
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def formula_text(pairs):
    # [('C', 2), ('H', 4), ('O', 2)] -> 'C2H4O2'.
    out = ""
    for sym, n in pairs:
        out += sym + (str(n) if n != 1 else "")
    return out


def molar_mass(pairs):
    # Sum of count x atomic mass, in g/mol.
    total = 0.0
    for sym, n in pairs:
        z = find(sym)
        if z is None:
            raise ValueError("Unknown element " + str(sym) + ".")
        total += n * mass(z)
    return total


def empirical(pairs):
    # Reduce subscripts by their GCD. -> (empirical pairs, factor).
    g = 0
    for sym, n in pairs:
        g = gcd(g, n)
    if g == 0:
        raise ValueError("Formula has no atoms.")
    return [(sym, n // g) for sym, n in pairs], g


def empirical_from_grams(pairs):
    # Classic mass-data route to an empirical formula.
    #
    # pairs: [(symbol, grams)], or percentages read as grams of a 100 g
    # sample. -> (moles, ratios, multiplier, whole-number pairs); the
    # counts are None when no multiplier up to 6 lands every ratio within
    # 0.1 of a whole number (the usual rounding allowance).
    moles = []
    for sym, grams in pairs:
        z = find(sym)
        if z is None:
            raise ValueError("Unknown element " + str(sym) + ".")
        if grams <= 0:
            raise ValueError("Masses must be positive.")
        moles.append(grams / mass(z))
    smallest = min(moles)
    ratios = [m / smallest for m in moles]
    for mult in (1, 2, 3, 4, 5, 6):
        fits = True
        for r in ratios:
            x = r * mult
            if abs(x - int(x + 0.5)) > 0.1:
                fits = False
                break
        if fits:
            counts = [(pairs[i][0], int(ratios[i] * mult + 0.5))
                      for i in range(len(pairs))]
            return moles, ratios, mult, counts
    return moles, ratios, None, None


def sci(x, digits=4):
    # Format a number to `digits` SIGNIFICANT figures.
    #
    # Significant figures, not decimal places: the Rydberg constant on
    # the formula sheet carries four of them, so reporting a wavelength
    # as 656.3355 nm would claim precision the input never had.
    #
    # The exponent comes from formatting rather than from math.log10,
    # which keeps this module free of imports.
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


LEFT = 24
UP = 25
RIGHT = 26
DOWN = 34
SECOND = 21
CLEAR = 45
ENTER = 105
ZOOM = 13
TRACE = 14

WHITE = (248, 250, 249)
BLACK = (25, 40, 48)
NAVY = (24, 47, 56)
GREY = (102, 121, 128)
PALE = (224, 235, 232)
TEAL = (15, 112, 94)
RED = (178, 57, 57)

N = element_count()

# (menu label, [(Z, count), ...]) -- the label keeps parentheses the
# element list cannot, e.g. Ca3(PO4)2 is Ca 3, P 2, O 8.
PRESETS = (
    ("Custom formula...", None),
    ("H2O water", ((1, 2), (8, 1))),
    ("CO2", ((6, 1), (8, 2))),
    ("NaCl", ((11, 1), (17, 1))),
    ("CaF2", ((20, 1), (9, 2))),
    ("C6H12O6 glucose", ((6, 6), (1, 12), (8, 6))),
    ("C13H21NO3 salbutamol", ((6, 13), (1, 21), (7, 1), (8, 3))),
    ("CH3COOH acetic acid", ((6, 2), (1, 4), (8, 2))),
    ("H3PO4 phosphoric acid", ((1, 3), (15, 1), (8, 4))),
    ("Ca3(PO4)2", ((20, 3), (15, 2), (8, 8))),
    ("C2H4 ethylene", ((6, 2), (1, 4))),
)

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


# ----------------------------------------------------------------------
# Number formatting
# ----------------------------------------------------------------------

def places(text):
    # Decimal places in a tabulated value: '22.99' -> 2.
    if "." not in text:
        return 0
    return len(text) - text.index(".") - 1


def fixed(x, dp):
    # x to dp decimal places, as text.
    if dp <= 0:
        return str(int(x + (0.5 if x >= 0 else -0.5)))
    return "{:.{p}f}".format(x, p=dp)


# ----------------------------------------------------------------------
# Molar mass pages
# ----------------------------------------------------------------------

def pairs_of(rows):
    # Editor rows -> [(symbol, count)], merging repeats, skipping 0.
    out = []
    for z, n in rows:
        if n <= 0:
            continue
        sym = symbol(z)
        found = False
        for p in out:
            if p[0] == sym:
                p[1] += n
                found = True
        if not found:
            out.append([sym, n])
    return [(p[0], p[1]) for p in out]


def mass_pages(pairs):
    total = molar_mass(pairs)
    # addition rule: the sum keeps the fewest decimal places of the
    # masses that went into it (counts are exact)
    dp = min(places(mass_text(find(s))) for s, n in pairs)
    work = []
    for sym, n in pairs:
        mt = mass_text(find(sym))
        part = n * mass(find(sym))
        if n == 1:
            work.append(sym + ": " + mt)
        else:
            work.append(sym + ": " + str(n) + " x " + mt + " = "
                        + fixed(part, places(mt)))
    work.append("Total = " + fixed(total, dp) + " g/mol")
    work.append("(" + str(dp) + " decimals: the least")
    work.append(" precise mass in the sum)")

    pct = []
    for sym, n in pairs:
        part = n * mass(find(sym))
        pct.append(sym + ": " + fixed(100 * part / total, 2) + " %")
    pct.append("= element mass / " + fixed(total, dp))
    pct.append("  x 100")

    emp, factor = empirical(pairs)
    subs = ", ".join(str(n) for s, n in pairs)
    e_lines = ["Subscripts: " + subs,
               "Greatest common factor: " + str(factor),
               "Empirical: " + formula_text(emp)]
    if factor > 1:
        e_lines.append("Molecular = " + str(factor) + " x empirical")
        e_lines.append("Empirical mass: " + fixed(molar_mass(emp), dp))
    else:
        e_lines.append("Already the lowest ratio:")
        e_lines.append("  empirical = molecular")

    kinds = [element_kind(s) for s, n in pairs]
    t_lines = []
    for sym, n in pairs:
        t_lines.append(sym + ": " + element_kind(sym))
    if "metal" in kinds and ("nonmetal" in kinds or "metalloid" in kinds):
        t_lines.append("Metal + nonmetal -> IONIC")
        t_lines.append("Formula = lowest ion ratio")
        t_lines.append("  (a formula unit, 9/14)")
        if factor > 1:
            t_lines.append("Ionic formulas are always")
            t_lines.append("  reduced: " + formula_text(emp))
    elif "metal" in kinds:
        t_lines.append("Metals only: a metal/alloy")
    else:
        t_lines.append("All nonmetals -> COVALENT")
        t_lines.append("A molecule: the formula is")
        t_lines.append("  the actual atom count")
    return [("Molar mass", work), ("% by mass", pct),
            ("Empirical", e_lines), ("Ionic?", t_lines)]


# ----------------------------------------------------------------------
# Percent -> empirical pages
# ----------------------------------------------------------------------

def percent_pages(pairs, molar):
    # pairs: [(symbol, grams or %)]; molar: molar mass or 0.
    moles, ratios, mult, counts = empirical_from_grams(pairs)
    work = ["Assume a 100 g sample:",
            "  % becomes grams"]
    total = 0.0
    for i, (sym, g) in enumerate(pairs):
        total += g
        mt = mass_text(find(sym))
        work.append(sym + ": " + fixed(g, 2) + " / " + mt)
        work.append("   = " + sci(moles[i]) + " mol")
    small = min(moles)
    work.append("Divide by smallest, " + sci(small) + ":")
    for i, (sym, g) in enumerate(pairs):
        work.append("  " + sym + ": " + fixed(ratios[i], 3))
    result = []
    if counts is None:
        result.append("No multiplier up to x6 gives")
        result.append("  whole numbers. Recheck the")
        result.append("  data or your rounding.")
    else:
        if mult > 1:
            result.append("Not whole yet: multiply")
            result.append("  every ratio by " + str(mult))
            for i, (sym, g) in enumerate(pairs):
                result.append("  " + sym + ": " + fixed(ratios[i] * mult, 2)
                              + " -> " + str(counts[i][1]))
        else:
            result.append("Ratios are already whole:")
            for sym, n in counts:
                result.append("  " + sym + ": " + str(n))
        emp = formula_text(counts)
        emass = molar_mass(counts)
        result.append("Empirical: " + emp)
        result.append("Empirical mass: " + fixed(emass, 2))
        if molar:
            n = molar / emass
            whole = int(n + 0.5)
            result.append("n = " + fixed(molar, 2) + " / "
                          + fixed(emass, 2))
            result.append("  = " + fixed(n, 2))
            if whole >= 1 and abs(n - whole) <= 0.1:
                result.append("Molecular: " + formula_text(
                    [(s, c * whole) for s, c in counts]))
            else:
                result.append("n is not whole: recheck")
    if abs(total - 100.0) > 0.5:
        result.append("Note: values add to " + fixed(total, 1))
        result.append("  (fine if they are grams)")
    return [("Moles", work), ("Result", result)]


# ----------------------------------------------------------------------
# Screens
# ----------------------------------------------------------------------

def view(label, pages):
    page = 0
    top = 0
    while True:
        title, lines = pages[page]
        screen()
        header(label[:14] + " " + title + " " + str(page + 1) + "/"
               + str(len(pages)))
        for row in range(8):
            i = top + row
            if i >= len(lines):
                break
            text = lines[i]
            key_line = (text.startswith("Total") or
                        text.startswith("Empirical:") or
                        text.startswith("Molecular:") or
                        "IONIC" in text or "COVALENT" in text)
            color(TEAL if key_line else BLACK)
            d.draw_text(8, 50 + row * 17, text[:30])
        if len(lines) > 8:
            color(GREY)
            tag = str(top + 1) + "-" + str(min(top + 8, len(lines)))
            d.draw_text(315 - len(tag) * 10, 186, tag)
        footer("L/R PAGE  UP/DN  CLEAR BACK")
        present()
        key = tis.wait_key()
        if key == CLEAR:
            return
        if key == RIGHT:
            page = (page + 1) % len(pages)
            top = 0
        elif key == LEFT:
            page = (page - 1) % len(pages)
            top = 0
        elif key == DOWN and top + 8 < len(lines):
            top += 1
        elif key == UP and top > 0:
            top -= 1


def box(x, y, w, text, active):
    if active:
        color(NAVY)
        d.fill_rect(x, y - 16, w, 21)
        color(WHITE)
    else:
        color(PALE)
        d.fill_rect(x, y - 16, w, 21)
        color(BLACK)
    d.draw_text(x + (w - len(text) * 10) // 2, y, text)


def clamp_z(z):
    return 1 + (z - 1) % N


def edit_formula(rows):
    # Five element/count rows. -> rows, or None if cancelled.
    rows = [list(r) for r in rows]
    while len(rows) < 5:
        rows.append([1, 0])
    pos = 0                       # slot = row * 2 + (0 element, 1 count)
    while True:
        screen()
        header("FORMULA: build a formula")
        for r in range(5):
            y = 52 + r * 22
            color(GREY)
            d.draw_text(8, y, str(r + 1))
            box(40, y, 50, symbol(rows[r][0]), pos == r * 2)
            color(GREY)
            d.draw_text(104, y, "x")
            box(130, y, 50, str(rows[r][1]), pos == r * 2 + 1)
            if rows[r][1]:
                color(GREY)
                d.draw_text(196, y, name(rows[r][0])[:11])
        pairs = pairs_of(rows)
        color(TEAL)
        d.draw_text(8, 169, ("= " + formula_text(pairs))[:30] if pairs
                    else "(all counts are 0)")
        color(GREY)
        d.draw_text(8, 186, "ZOOM/TRACE: jump 10")
        footer("L/R BOX UP/DN VALUE ENT GO")
        present()
        key = tis.wait_key()
        if key == CLEAR:
            return None
        r, c = pos // 2, pos % 2
        if key == LEFT:
            pos = (pos - 1) % 10
        elif key == RIGHT:
            pos = (pos + 1) % 10
        elif key in (UP, DOWN, ZOOM, TRACE):
            by = {UP: 1, DOWN: -1, TRACE: 10, ZOOM: -10}[key]
            if c == 0:
                rows[r][0] = clamp_z(rows[r][0] + by)
            else:
                rows[r][1] = min(99, max(0, rows[r][1] + by))
        elif key == ENTER and pairs:
            return rows


def edit_percent(state):
    # Four element/percent rows plus an optional molar mass.
    #
    # state: [[Z, [d, d, d, d]] x4, [d, d, d, d, d]] -- percents are
    # NN.NN, the molar mass NNN.NN (0 skips the molecular step).
    slots = []
    for r in range(4):
        slots.append((r, -1))
        for k in range(4):
            slots.append((r, k))
    for k in range(5):
        slots.append((4, k))
    pos = 0
    while True:
        screen()
        header("FORMULA: % -> empirical")
        for r in range(4):
            y = 48 + r * 22
            z, digits = state[r]
            box(8, y, 42, symbol(z), slots[pos] == (r, -1))
            x = 70
            for k in range(4):
                box(x, y, 22, str(digits[k]), slots[pos] == (r, k))
                x += 24 if k != 1 else 36
            color(GREY)
            d.draw_text(118, y, ".")
            d.draw_text(184, y, "%")
        y = 142
        color(GREY)
        d.draw_text(8, y, "M")
        x = 40
        for k in range(5):
            box(x, y, 22, str(state[4][k]), slots[pos] == (4, k))
            x += 24 if k != 2 else 36
        d.draw_text(112, y, ".")
        d.draw_text(180, y, "g/mol")
        color(GREY)
        d.draw_text(8, 168, "M = 0 skips molecular formula")
        d.draw_text(8, 185, "0.00 % rows are ignored")
        footer("L/R BOX UP/DN VALUE ENT GO")
        present()
        key = tis.wait_key()
        if key == CLEAR:
            return None
        r, k = slots[pos]
        if key == LEFT:
            pos = (pos - 1) % len(slots)
        elif key == RIGHT:
            pos = (pos + 1) % len(slots)
        elif key in (UP, DOWN, ZOOM, TRACE):
            by = {UP: 1, DOWN: -1, TRACE: 10, ZOOM: -10}[key]
            if k == -1:
                state[r][0] = clamp_z(state[r][0] + by)
            elif key in (UP, DOWN):
                digits = state[4] if r == 4 else state[r][1]
                digits[k] = (digits[k] + by) % 10
        elif key == ENTER:
            pairs = percent_pairs(state)
            if pairs:
                return state


def percent_pairs(state):
    out = []
    for r in range(4):
        z, dg = state[r]
        value = dg[0] * 10 + dg[1] + dg[2] / 10.0 + dg[3] / 100.0
        if value > 0:
            out.append((symbol(z), value))
    return out


def molar_value(state):
    dg = state[4]
    return dg[0] * 100 + dg[1] * 10 + dg[2] + dg[3] / 10.0 + dg[4] / 100.0


def formula_menu():
    sel = 0
    custom = [[6, 1], [1, 4]]      # kept, so a tweak starts from the last try
    while True:
        screen()
        header("FORMULA: molar mass")
        first = max(0, min(sel - 3, len(PRESETS) - 8))
        for row in range(8):
            i = first + row
            if i >= len(PRESETS):
                break
            y = 50 + row * 17
            if i == sel:
                color(PALE)
                d.fill_rect(4, y - 15, 312, 17)
                color(TEAL)
            else:
                color(BLACK)
            d.draw_text(12, y, PRESETS[i][0][:29])
        footer("UP/DN MOVE ENT OPEN CLR BACK")
        present()
        key = tis.wait_key()
        if key == CLEAR:
            return
        if key == UP:
            sel = (sel - 1) % len(PRESETS)
        elif key == DOWN:
            sel = (sel + 1) % len(PRESETS)
        elif key == ENTER:
            label, rows = PRESETS[sel]
            if rows is None:
                rows = edit_formula(custom)
                if rows is None:
                    continue
                custom = rows
                label = formula_text(pairs_of(rows))
            else:
                label = label.split(" ")[0]
            view(label, mass_pages(pairs_of(rows)))


ITEMS = ("Molar mass & empirical", "% composition -> empirical")


def main():
    sel = 0
    # the classic textbook data: 40.00% C, 6.70% H, 53.30% O, and a
    # molar mass of 180.16 g/mol -> CH2O and C6H12O6
    percent_state = [[6, [4, 0, 0, 0]], [1, [0, 6, 7, 0]],
                     [8, [5, 3, 3, 0]], [7, [0, 0, 0, 0]],
                     [1, 8, 0, 1, 6]]
    while True:
        screen()
        header("FORMULA: mass & empirical")
        for i, item in enumerate(ITEMS):
            y = 60 + i * 26
            if i == sel:
                color(PALE)
                d.fill_rect(4, y - 17, 312, 22)
                color(TEAL)
            else:
                color(BLACK)
            d.draw_text(14, y, item)
        color(GREY)
        d.draw_text(8, 150, "Masses: IUPAC table values")
        d.draw_text(8, 167, "Sums keep the fewest decimals")
        footer("UP/DN MOVE ENT OPEN CLR EXIT")
        present()
        key = tis.wait_key()
        if key == CLEAR:
            break
        if key in (UP, DOWN):
            sel = 1 - sel
        elif key == ENTER:
            if sel == 0:
                formula_menu()
            else:
                got = edit_percent(percent_state)
                if got is not None:
                    try:
                        view("% data", percent_pages(
                            percent_pairs(got), molar_value(got)))
                    except ValueError as exc:
                        view("% data", [("Error", [str(exc)[:30]])])
    screen()
    present()


main()
