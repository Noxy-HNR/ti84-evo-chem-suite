# NAMER.py -- formulas and names for the TI-84 Evo.
#
#     Ionic compound    pick a cation and an anion: crisscross, reduce,
#                       check the charges, formula and name
#     Acid name         -ide -> hydro-...-ic, -ate -> -ic, -ite -> -ous
#     Covalent name     prefixes for two nonmetals (dinitrogen tetroxide)
#     Flashcards        polyatomic ions, and acids, name <-> formula
#
# Self-contained: no CHEMCORE needed. The 9/14 notes treat naming as a
# skill built by practice, so the flashcards are the heart of this one.

import ti_draw as d
import ti_system as tis

try:
    import random
except ImportError:
    random = None

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

# (formula unit, name, charge, Roman numeral or "", polyatomic?)
# Metals with one fixed charge take no numeral (Tro's invariant list);
# Hg2 2+ is mercury(I) because each Hg carries +1.
CATIONS = (
    ("Li", "lithium", 1, "", False), ("Na", "sodium", 1, "", False),
    ("K", "potassium", 1, "", False), ("Rb", "rubidium", 1, "", False),
    ("Cs", "cesium", 1, "", False), ("Ag", "silver", 1, "", False),
    ("NH4", "ammonium", 1, "", True),
    ("Be", "beryllium", 2, "", False), ("Mg", "magnesium", 2, "", False),
    ("Ca", "calcium", 2, "", False), ("Sr", "strontium", 2, "", False),
    ("Ba", "barium", 2, "", False), ("Zn", "zinc", 2, "", False),
    ("Cd", "cadmium", 2, "", False), ("Al", "aluminum", 3, "", False),
    ("Fe", "iron", 2, "II", False), ("Fe", "iron", 3, "III", False),
    ("Cu", "copper", 1, "I", False), ("Cu", "copper", 2, "II", False),
    ("Co", "cobalt", 2, "II", False), ("Co", "cobalt", 3, "III", False),
    ("Cr", "chromium", 2, "II", False), ("Cr", "chromium", 3, "III", False),
    ("Mn", "manganese", 2, "II", False), ("Ni", "nickel", 2, "II", False),
    ("Sn", "tin", 2, "II", False), ("Sn", "tin", 4, "IV", False),
    ("Pb", "lead", 2, "II", False), ("Pb", "lead", 4, "IV", False),
    ("Hg2", "mercury", 2, "I", True), ("Hg", "mercury", 2, "II", False),
    ("Au", "gold", 1, "I", False), ("Au", "gold", 3, "III", False),
)

# (formula unit, name, charge size, polyatomic?, acid formula, acid name)
ANIONS = (
    ("F", "fluoride", 1, False, "HF", "hydrofluoric acid"),
    ("Cl", "chloride", 1, False, "HCl", "hydrochloric acid"),
    ("Br", "bromide", 1, False, "HBr", "hydrobromic acid"),
    ("I", "iodide", 1, False, "HI", "hydroiodic acid"),
    ("H", "hydride", 1, False, None, None),
    ("O", "oxide", 2, False, None, None),
    ("S", "sulfide", 2, False, "H2S", "hydrosulfuric acid"),
    ("Se", "selenide", 2, False, None, None),
    ("N", "nitride", 3, False, None, None),
    ("P", "phosphide", 3, False, None, None),
    ("OH", "hydroxide", 1, True, None, None),
    ("CN", "cyanide", 1, True, "HCN", "hydrocyanic acid"),
    ("NO3", "nitrate", 1, True, "HNO3", "nitric acid"),
    ("NO2", "nitrite", 1, True, "HNO2", "nitrous acid"),
    ("CH3COO", "acetate", 1, True, "CH3COOH", "acetic acid"),
    ("ClO4", "perchlorate", 1, True, "HClO4", "perchloric acid"),
    ("ClO3", "chlorate", 1, True, "HClO3", "chloric acid"),
    ("ClO2", "chlorite", 1, True, "HClO2", "chlorous acid"),
    ("ClO", "hypochlorite", 1, True, "HClO", "hypochlorous acid"),
    ("MnO4", "permanganate", 1, True, "HMnO4", "permanganic acid"),
    ("HCO3", "hydrogen carbonate", 1, True, None, None),
    ("HSO4", "hydrogen sulfate", 1, True, None, None),
    ("H2PO4", "dihydrogen phosphate", 1, True, None, None),
    ("CO3", "carbonate", 2, True, "H2CO3", "carbonic acid"),
    ("SO4", "sulfate", 2, True, "H2SO4", "sulfuric acid"),
    ("SO3", "sulfite", 2, True, "H2SO3", "sulfurous acid"),
    ("CrO4", "chromate", 2, True, "H2CrO4", "chromic acid"),
    ("Cr2O7", "dichromate", 2, True, "H2Cr2O7", "dichromic acid"),
    ("C2O4", "oxalate", 2, True, "H2C2O4", "oxalic acid"),
    ("O2", "peroxide", 2, True, None, None),
    ("HPO4", "hydrogen phosphate", 2, True, None, None),
    ("S2O3", "thiosulfate", 2, True, "H2S2O3", "thiosulfuric acid"),
    ("PO4", "phosphate", 3, True, "H3PO4", "phosphoric acid"),
    ("PO3", "phosphite", 3, True, "H3PO3", "phosphorous acid"),
)

ALIASES = {"hydrogen carbonate": "bicarbonate",
           "hydrogen sulfate": "bisulfate"}

# Covalent binary naming: (symbol, element name, -ide name), listed in
# the usual formula order -- the element written first comes earlier.
COVALENT = (
    ("Xe", "xenon", "xenide"), ("B", "boron", "boride"),
    ("Si", "silicon", "silicide"), ("C", "carbon", "carbide"),
    ("As", "arsenic", "arsenide"), ("P", "phosphorus", "phosphide"),
    ("N", "nitrogen", "nitride"), ("H", "hydrogen", "hydride"),
    ("Te", "tellurium", "telluride"), ("Se", "selenium", "selenide"),
    ("S", "sulfur", "sulfide"), ("I", "iodine", "iodide"),
    ("Br", "bromine", "bromide"), ("Cl", "chlorine", "chloride"),
    ("O", "oxygen", "oxide"), ("F", "fluorine", "fluoride"),
)
PREFIX = ("", "mono", "di", "tri", "tetra", "penta", "hexa", "hepta",
          "octa", "nona", "deca")
COMMON = {"H2O": "water", "NH3": "ammonia", "CH4": "methane",
          "H2O2": "hydrogen peroxide"}

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


def wrap(text, width=30):
    lines = []
    line = ""
    for w in str(text).split(" "):
        trial = w if not line else line + " " + w
        if len(trial) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = w[:width]
    if line:
        lines.append(line)
    return lines


# ----------------------------------------------------------------------
# The chemistry
# ----------------------------------------------------------------------

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def ion_text(unit, charge, sign):
    return unit + " " + (str(charge) if charge > 1 else "") + sign


def cation_name(c):
    return c[1] + ("(" + c[3] + ")" if c[3] else "")


def part(unit, n, poly):
    # One ion's share of the formula: Ca, Cl2, (OH)2, (NH4)2.
    if n == 1:
        return unit
    if poly:
        return "(" + unit + ")" + str(n)
    return unit + str(n)


def ionic(c, a):
    # -> (formula, name, steps). Crisscross, then reduce the ratio of
    # ION UNITS -- never the atoms inside one -- so Hg2Cl2 and Na2O2 stay
    # whole instead of collapsing to HgCl and NaO.
    qc, qa = c[2], a[2]
    raw_c, raw_a = qa, qc
    g = gcd(raw_c, raw_a)
    nc, na = raw_c // g, raw_a // g
    formula = part(c[0], nc, c[4]) + part(a[0], na, a[3])
    name = cation_name(c) + " " + a[1]
    steps = [
        "Cation: " + ion_text(c[0], qc, "+"),
        "  " + cation_name(c),
        "Anion:  " + ion_text(a[0], qa, "-"),
        "  " + a[1],
        "Crisscross the charges:",
        "  " + str(raw_c) + " " + c[0] + " : " + str(raw_a) + " " + a[0],
    ]
    if g > 1:
        steps.append("Reduce " + str(raw_c) + ":" + str(raw_a) + " -> "
                     + str(nc) + ":" + str(na))
    else:
        steps.append("Already lowest ratio")
    steps.append("Check: " + str(nc) + "(+" + str(qc) + ") + " + str(na)
                 + "(-" + str(qa) + ") = 0")
    if (c[4] and nc > 1) or (a[3] and na > 1):
        steps.append("Polyatomic ion x2+ -> ( )")
    if c[0] == "Hg2" or a[0] == "O2":
        steps.append("Never reduce inside an ion:")
        steps.append("  " + (c[0] if c[0] == "Hg2" else a[0])
                     + " stays whole")
    if c[3]:
        per = {"I": 1, "II": 2, "III": 3, "IV": 4}[c[3]]
        steps.append("(" + c[3] + ") = " + str(per) + "+ on each "
                     + c[0].rstrip("2"))
    steps.append("Formula: " + formula)
    for ln in wrap("Name: " + name):
        steps.append(ln)
    return formula, name, steps


def acid(a):
    # -> steps for turning an anion into its acid.
    rule = "-ide -> hydro- ...-ic acid"
    if a[1].endswith("ate"):
        rule = "-ate -> -ic acid"
    elif a[1].endswith("ite"):
        rule = "-ite -> -ous acid"
    steps = [
        "Anion: " + ion_text(a[0], a[2], "-"),
        "  " + a[1],
        "Add " + str(a[2]) + " H+ to cancel " + str(a[2]) + "-",
        "Rule: " + rule,
    ]
    if a[0] == "CH3COO":
        steps.append("Organic acid: H goes last")
    steps.append("Formula: " + a[4])
    for ln in wrap("Name: " + a[5]):
        steps.append(ln)
    return steps


def covalent(i1, n1, i2, n2):
    # -> (formula, name, notes). No mono on the first element; a or o
    # at the end of a prefix drops before 'oxide' (monoxide, tetroxide).
    s1, name1, ide1 = COVALENT[i1]
    s2, name2, ide2 = COVALENT[i2]
    first = (PREFIX[n1] if n1 > 1 else "") + name1
    pre = PREFIX[n2]
    if pre[-1] in "ao" and ide2[0] == "o":
        pre = pre[:-1]
    name = first + " " + pre + ide2
    formula = s1 + (str(n1) if n1 > 1 else "") + s2 + \
        (str(n2) if n2 > 1 else "")
    notes = []
    if formula in COMMON:
        notes.append("Common name: " + COMMON[formula])
    if i1 > i2:
        notes.append("Usually written " + s2 + " first")
    if i1 == i2:
        notes.append("Same element twice?")
    return formula, name, notes


# ----------------------------------------------------------------------
# Screens
# ----------------------------------------------------------------------

def show_lines(title, lines):
    top = 0
    while True:
        screen()
        header(title)
        for row in range(8):
            i = top + row
            if i >= len(lines):
                break
            text = lines[i]
            color(TEAL if text.startswith("Formula") or
                  text.startswith("Name") else BLACK)
            d.draw_text(8, 50 + row * 17, text[:30])
        if len(lines) > 8:
            color(GREY)
            tag = str(top + 1) + "-" + str(min(top + 8, len(lines)))
            d.draw_text(315 - len(tag) * 10, 186, tag)
        footer("UP/DN SCROLL  CLEAR BACK")
        present()
        key = tis.wait_key()
        if key == CLEAR:
            return
        if key == DOWN and top + 8 < len(lines):
            top += 1
        elif key == UP and top > 0:
            top -= 1


def pick_two(title, left_items, right_items, left_label, right_label,
             describe_left, describe_right, start=(0, 0)):
    # Two side-by-side pickers. -> (i, j) or None. start restores the
    # last choice, so coming back from a result does not mean scrolling
    # all the way to iron(III) again.
    i, j = start
    side = 0
    while True:
        screen()
        header(title)
        for k, (label, text, sub) in enumerate((
                (left_label, describe_left(i)[0], describe_left(i)[1]),
                (right_label, describe_right(j)[0],
                 describe_right(j)[1]))):
            y = 56 + k * 62
            active = k == side
            if active:
                color(PALE)
                d.fill_rect(4, y - 16, 312, 56)
            color(GREY)
            d.draw_text(8, y, label)
            color(TEAL if active else BLACK)
            d.draw_text(8, y + 19, ("<" + text + ">")[:30])
            color(BLACK)
            d.draw_text(8, y + 36, sub[:30])
        color(GREY)
        d.draw_text(8, 185, "UP/DN side  L/R choose")
        footer("ENT BUILD  CLEAR BACK")
        present()
        key = tis.wait_key()
        if key == CLEAR:
            return None
        if key in (UP, DOWN):
            side = 1 - side
        elif key in (LEFT, RIGHT):
            by = 1 if key == RIGHT else -1
            if side == 0:
                i = (i + by) % len(left_items)
            else:
                j = (j + by) % len(right_items)
        elif key == ENTER:
            return i, j


def ionic_mode():
    last = (0, 0)
    while True:
        picked = pick_two(
            "NAMER: ionic compound", CATIONS, ANIONS, "Cation", "Anion",
            lambda i: (ion_text(CATIONS[i][0], CATIONS[i][2], "+"),
                       cation_name(CATIONS[i])),
            lambda j: (ion_text(ANIONS[j][0], ANIONS[j][2], "-"),
                       ANIONS[j][1]), last)
        if picked is None:
            return
        last = picked
        formula, name, steps = ionic(CATIONS[picked[0]], ANIONS[picked[1]])
        show_lines("NAMER: " + formula, steps)


ACIDS = [a for a in ANIONS if a[4]]


def acid_mode():
    j = 0
    while True:
        a = ACIDS[j]
        screen()
        header("NAMER: acid from anion")
        color(GREY)
        d.draw_text(8, 52, "Anion")
        color(TEAL)
        d.draw_text(8, 72, ("<" + ion_text(a[0], a[2], "-") + ">")[:30])
        color(BLACK)
        d.draw_text(8, 90, a[1])
        color(GREY)
        d.draw_text(8, 124, "-ide  -> hydro-...-ic acid")
        d.draw_text(8, 141, "-ate  -> -ic acid")
        d.draw_text(8, 158, "-ite  -> -ous acid")
        d.draw_text(8, 185, str(j + 1) + "/" + str(len(ACIDS)))
        footer("L/R CHOOSE ENT NAME CLR BACK")
        present()
        key = tis.wait_key()
        if key == CLEAR:
            return
        if key in (LEFT, UP):
            j = (j - 1) % len(ACIDS)
        elif key in (RIGHT, DOWN):
            j = (j + 1) % len(ACIDS)
        elif key == ENTER:
            show_lines("NAMER: " + a[4], acid(a))


def covalent_mode():
    sel = [3, 1, 14, 2]         # carbon x1, oxygen x2 -> carbon dioxide
    field = 0
    while True:
        formula, name, notes = covalent(sel[0], sel[1], sel[2], sel[3])
        screen()
        header("NAMER: covalent name")
        labels = ("1st element", "  how many", "2nd element", "  how many")
        values = (COVALENT[sel[0]][0], str(sel[1]),
                  COVALENT[sel[2]][0], str(sel[3]))
        for k in range(4):
            y = 50 + k * 20
            if k == field:
                color(PALE)
                d.fill_rect(4, y - 16, 312, 20)
            color(GREY)
            d.draw_text(8, y, labels[k])
            color(TEAL if k == field else BLACK)
            d.draw_text(170, y, "<" + values[k] + ">")
        color(BLACK)
        d.draw_text(8, 139, formula)
        color(TEAL)
        for i, ln in enumerate(wrap(name)[:2]):
            d.draw_text(8, 156 + i * 17, ln)
        if notes and len(wrap(name)) < 2:
            color(GREY)
            d.draw_text(8, 173, notes[0][:30])
        footer("UP/DN ROW  L/R CHANGE  CLR")
        present()
        key = tis.wait_key()
        if key == CLEAR:
            return
        if key == UP:
            field = (field - 1) % 4
        elif key == DOWN:
            field = (field + 1) % 4
        elif key in (LEFT, RIGHT):
            by = 1 if key == RIGHT else -1
            if field in (0, 2):
                sel[field] = (sel[field] + by) % len(COVALENT)
            else:
                sel[field] = min(10, max(1, sel[field] + by))


# ----------------------------------------------------------------------
# Flashcards
# ----------------------------------------------------------------------

def ion_deck():
    deck = []
    for c in CATIONS:
        if c[4]:
            label = c[1] + ("(" + c[3] + ") ion" if c[3] else "")
            deck.append((label, ion_text(c[0], c[2], "+"), ""))
    for a in ANIONS:
        if a[3]:
            deck.append((a[1], ion_text(a[0], a[2], "-"),
                         ALIASES.get(a[1], "")))
    return deck


def acid_deck():
    deck = []
    for a in ACIDS:
        deck.append((a[5], a[4], "from " + a[1]))
    return deck


def shuffle(deck):
    if random is None:
        return deck
    deck = list(deck)
    for i in range(len(deck) - 1, 0, -1):
        k = random.randint(0, i)
        deck[i], deck[k] = deck[k], deck[i]
    return deck


def flashcards(title, deck):
    order = list(deck)
    i = 0
    shown = False
    flip = False             # False: name on the front; True: formula
    while True:
        front, back, extra = order[i]
        if flip:
            front, back = back, front
        screen()
        header("CARDS: " + title + " " + str(i + 1) + "/"
               + str(len(order)))
        color(PALE)
        d.fill_rect(10, 36, 300, 58)
        color(NAVY)
        for k, ln in enumerate(wrap(front, 28)[:2]):
            d.draw_text(20, 60 + k * 20, ln)
        if shown:
            color(TEAL)
            for k, ln in enumerate(wrap(back, 28)[:2]):
                d.draw_text(20, 122 + k * 20, ln)
            if extra:
                color(GREY)
                d.draw_text(20, 164, extra[:28])
        else:
            color(GREY)
            d.draw_text(20, 122, "ENTER to reveal")
        color(GREY)
        d.draw_text(8, 185, "2ND flip  UP shuffle")
        footer("L/R NEXT  ENT SHOW  CLR BACK")
        present()
        key = tis.wait_key()
        if key == CLEAR:
            return
        if key == ENTER:
            shown = not shown
        elif key == RIGHT:
            i = (i + 1) % len(order)
            shown = False
        elif key == LEFT:
            i = (i - 1) % len(order)
            shown = False
        elif key == SECOND:
            flip = not flip
            shown = False
        elif key == UP:
            order = shuffle(order)
            i = 0
            shown = False


# ----------------------------------------------------------------------

ITEMS = ("Ionic compound", "Acid name", "Covalent (prefix) name",
         "Flashcards: polyatomic ions", "Flashcards: acids")


def main():
    sel = 0
    while True:
        screen()
        header("NAMER: formulas & names")
        for i, item in enumerate(ITEMS):
            y = 56 + i * 24
            if i == sel:
                color(PALE)
                d.fill_rect(4, y - 17, 312, 22)
                color(TEAL)
            else:
                color(BLACK)
            d.draw_text(14, y, item)
        color(GREY)
        d.draw_text(8, 185, "practice builds this skill")
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
                ionic_mode()
            elif sel == 1:
                acid_mode()
            elif sel == 2:
                covalent_mode()
            elif sel == 3:
                flashcards("ions", ion_deck())
            else:
                flashcards("acids", acid_deck())
    screen()
    present()


main()
