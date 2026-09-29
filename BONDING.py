# BONDING.py -- "completely describe the bonding" for the TI-84 Evo.
#
# Pages: Lewis, Shape, Orbitals, Polarity, Steps. LEFT/RIGHT turns
# pages, UP/DOWN scrolls, CLEAR goes back. Needs LEWCORE and POLCORE.

import ti_draw as d
import ti_system as tis
# Free the garbage left from compiling this program before the next
# import has to find room. Harmless where gc is missing.
try:
    import gc
    gc.collect()
except:
    pass
from LEWCORE import *
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

ELEMENT_CHOICES = ("H", "B", "C", "N", "O", "F", "Si", "P", "S",
                   "Cl", "Br", "I", "Xe")

# (menu label, atoms, charge). atoms None with a str charge marks a
# hand-built two-center molecule; None/None is the custom editor.
PRESETS = (
    ("CH4 methane", (("C", 1), ("H", 4)), 0),
    ("H2O water", (("H", 2), ("O", 1)), 0),
    ("C2H4 ethylene", None, "C2H4"),
    ("NH3 ammonia", (("N", 1), ("H", 3)), 0),
    ("CO2", (("C", 1), ("O", 2)), 0),
    ("HCN", (("H", 1), ("C", 1), ("N", 1)), 0),
    ("CH2O formaldehyde", (("C", 1), ("H", 2), ("O", 1)), 0),
    ("C2H2 acetylene", None, "C2H2"),
    ("BF3", (("B", 1), ("F", 3)), 0),
    ("BH3", (("B", 1), ("H", 3)), 0),
    ("BF4-", (("B", 1), ("F", 4)), -1),
    ("NH4+", (("N", 1), ("H", 4)), 1),
    ("F3SiH", (("Si", 1), ("F", 3), ("H", 1)), 0),
    ("HCO2- formate", (("H", 1), ("C", 1), ("O", 2)), -1),
    ("ClO4- perchlorate", (("Cl", 1), ("O", 4)), -1),
    ("NO3- nitrate", (("N", 1), ("O", 3)), -1),
    ("CO3^2- carbonate", (("C", 1), ("O", 3)), -2),
    ("SO4^2- sulfate", (("S", 1), ("O", 4)), -2),
    ("SO2", (("S", 1), ("O", 2)), 0),
    ("CO", (("C", 1), ("O", 1)), 0),
    ("CN-", (("C", 1), ("N", 1)), -1),
    ("PCl5", (("P", 1), ("Cl", 5)), 0),
    ("SF4", (("S", 1), ("F", 4)), 0),
    ("ClF3", (("Cl", 1), ("F", 3)), 0),
    ("XeF4", (("Xe", 1), ("F", 4)), 0),
    ("SF6", (("S", 1), ("F", 6)), 0),
    ("Custom formula...", None, None),
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


def wrap(text, width=30):
    words = str(text).split(" ")
    lines = []
    line = ""
    for w in words:
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


def indent(text, prefix="  "):
    # Wrap text to fit after prefix, prefixing every line.
    return [prefix + ln for ln in wrap(text, 30 - len(prefix))]


# ----------------------------------------------------------------------
# Describing a one-center structure
# ----------------------------------------------------------------------

BOND_WORD = ("", "single", "double", "triple")
BOND_MARK = ("", "-", "=", "#")


def ao(sym):
    # The atomic orbital an outer atom bonds with. Terminal atoms do
    # not hybridize in this course (9/28): H uses 1s, the rest their
    # valence p.
    if sym == "H":
        return "1s"
    return str(PERIOD[sym]) + "p"


def fc_text(q):
    if q > 0:
        return "+" + str(q)
    return str(q)


def charge_text(q):
    if q == 0:
        return ""
    return (str(abs(q)) if abs(q) > 1 else "") + ("+" if q > 0 else "-")


def electron_sum(r, charge):
    # 'Cl 7 + O 6x4 + 1 = 32' -- the step 1 arithmetic.
    order = [r["center"]]
    for atom in r["ligands"]:
        if atom not in order:
            order.append(atom)
    parts = []
    for atom in order:
        n = r["ligands"].count(atom) + (1 if atom == r["center"] else 0)
        v = str(LEWIS_VALENCE[atom])
        parts.append(atom + " " + v + ("x" + str(n) if n > 1 else ""))
    text = " + ".join(parts)
    if charge < 0:
        text += " + " + str(-charge)
    elif charge > 0:
        text += " - " + str(charge)
    return text + " = " + str(r["electrons"])


def groups_by(r):
    # Outer atoms grouped by (element, bond order), first-seen order,
    # using the first resonance form. -> [(atom, order, count, index)]
    out = []
    for i, atom in enumerate(r["ligands"]):
        order = r["bonds"][i]
        found = False
        for g in out:
            if g[0] == atom and g[1] == order:
                g[2] += 1
                found = True
        if not found:
            out.append([atom, order, 1, i])
    return out


def lewis_page(r, charge):
    c = r["center"]
    lines = ["Valence e-:"]
    lines.extend(indent(electron_sum(r, charge)))
    if len(r["ligands"]) == 1:
        lines.append("Two atoms: no center needed")
    else:
        lines.append("Central atom: " + c + " (least EN)")
    for atom, order, n, i in groups_by(r):
        mark = c + BOND_MARK[order] + atom
        lines.append(str(n) + "x " + mark + "  " + BOND_WORD[order]
                     + " bond")
        lone = r["terminal_lone"][i] // 2
        lines.append("   " + atom + ": " + str(lone) + " lone pair"
                     + ("" if lone == 1 else "s") + ", FC "
                     + fc_text(r["charges"][i]))
    lines.append(c + ": " + str(r["lone_pairs"]) + " lone pair"
                 + ("" if r["lone_pairs"] == 1 else "s") + ", FC "
                 + fc_text(r["central_charge"]))
    total = r["central_charge"] + sum(r["charges"])
    lines.append("FC sum " + fc_text(total) + " = overall charge")
    shell = 2 * sum(r["bonds"]) + 2 * r["lone_pairs"]
    if shell > 8:
        lines.append(c + " holds " + str(shell) + " e-: expanded")
        lines.append("  octet, OK for period 3+")
    forms = len(r["resonance"])
    if forms > 1:
        lines.append("Resonance: " + str(forms) + " equivalent forms")
        lines.append("  (real ion = their average)")
    return lines


def shape_page(r):
    if len(r["ligands"]) == 1:
        return ["Two atoms only.",
                "Any two-atom molecule is", "  linear.",
                "No central atom, so no",
                "  electron-group count."]
    groups = r["regions"]
    lp = r["lone_pairs"]
    shape, angle = SHAPES.get((groups, lp), ("?", "?"))
    x = len(r["ligands"])
    axe = "AX" + (str(x) if x > 1 else "")
    if lp:
        axe += "E" + (str(lp) if lp > 1 else "")
    lines = ["Groups on " + r["center"] + ": " + str(groups),
             "  " + str(x) + " bonded + " + str(lp) + " lone pair"
             + ("" if lp == 1 else "s")]
    if max(r["bonds"]) > 1:
        lines.append("  (a double/triple bond")
        lines.append("   counts as ONE group)")
    lines.append("Electron geometry:")
    lines.append("  " + GEOMETRY.get(groups, "?"))
    lines.append("Molecular shape:")
    lines.append("  " + shape)
    lines.append("Bond angle: " + angle + " deg")
    lines.append("VSEPR class: " + axe)
    return lines


def orbitals_page(r):
    c = r["center"]
    ligands = r["ligands"]
    bonds = r["bonds"]
    sigma = len(ligands)
    pi = sum(b - 1 for b in bonds)
    lines = []
    if len(ligands) == 1:
        lig = ligands[0]
        lines.append("No interior atom, so")
        lines.append("  nothing hybridizes.")
        lines.append("sigma: 1   pi: " + str(pi))
        lines.append("sigma " + c + "(" + ao(c) + ")-" + lig + "("
                     + ao(lig) + ")")
        lines.append("  head-on overlap")
        if pi:
            lines.append("pi " + c + "(" + ao(c) + ")-" + lig + "("
                         + ao(lig) + ") x" + str(pi))
            lines.append("  side-by-side overlap")
        return lines

    groups = r["regions"]
    hyb = HYBRIDS.get(groups, "?")
    lines.append(c + " is " + hyb + " (" + HYBRID_MIX.get(groups, "?")
                 + ")")
    lines.append("  = " + str(groups) + " hybrid orbitals")
    lines.append("Outer atoms: no hybrids")
    lines.append("sigma: " + str(sigma) + "   pi: " + str(pi))

    seen = []
    for atom in ligands:
        if atom not in seen:
            seen.append(atom)
            n = ligands.count(atom)
            lines.append("sigma " + c + "(" + hyb + ")-" + atom + "("
                         + ao(atom) + ") x" + str(n))

    if pi:
        free_p = unhybridized_p(groups)
        cp = str(PERIOD[c]) + "p"
        shown = 0
        for atom in seen:
            n = sum(bonds[i] - 1 for i in range(len(ligands))
                    if ligands[i] == atom)
            take = min(n, free_p - shown)
            if take > 0:
                lines.append("pi " + c + "(" + cp + ")-" + atom + "("
                             + ao(atom) + ") x" + str(take))
                shown += take
        if shown:
            lines.append("  pi = sideways p overlap")
        if pi > shown:
            # sp3 Cl with 3 pi bonds (ClO4-) has no p orbitals left;
            # the extra bonds lean on d orbitals, which this course's
            # model does not assign. Say so instead of inventing one.
            left = pi - shown
            lines.append(str(left) + " pi bond" + (" uses " if left == 1
                         else "s use ") + c + " d")
            lines.append("  orbitals (expanded octet),")
            lines.append("  beyond this course's model")

    lp = r["lone_pairs"]
    if lp:
        lines.append(str(lp) + " lone pair" + ("" if lp == 1 else "s")
                     + " sit" + ("s" if lp == 1 else "") + " in")
        lines.append("  " + c + " " + hyb + " hybrid orbital"
                     + ("" if lp == 1 else "s"))
    return lines


def polarity_page(r, charge):
    c = r["center"]
    lines = []
    kinds = []
    seen = []
    for atom in r["ligands"]:
        if atom in seen:
            continue
        seen.append(atom)
        delta, kind, neg = bond_polarity(c, atom)
        kinds.append(kind)
        short = kind.split(" ")[0]
        lines.append(c + "-" + atom + "  dEN " + tenths(delta) + "  "
                     + short)
        if neg:
            lines.append("  arrow points to " + neg)
        for note in bond_caveat(c, atom):
            lines.append("  " + note)
    every = []
    for atom in r["ligands"]:
        every.append(bond_polarity(c, atom)[1])
    groups = r["regions"]
    polar, why = molecule_polarity(groups, r["lone_pairs"],
                                   r["ligands"], every)
    lines.append("Molecule: " + ("POLAR" if polar else "NONPOLAR"))
    lines.append("  " + why)
    if charge:
        lines.append("Still an ion: charge " + fc_text(charge))
    return lines


def describe(r, charge):
    steps = []
    for s in r["steps"]:
        steps.extend(wrap(s))
    return [
        ("Lewis", lewis_page(r, charge)),
        ("Shape", shape_page(r)),
        ("Orbitals", orbitals_page(r)),
        ("Polarity", polarity_page(r, charge)),
        ("Steps", steps),
    ]


# ----------------------------------------------------------------------
# Two-center molecules, worked by hand from the 9/28 notes
# ----------------------------------------------------------------------

HAND = {
    "C2H4": [
        ("Lewis", [
            "Valence e-:", "  C 4x2 + H 1x4 = 12",
            "Two centers: C and C", "H2C=CH2",
            "1x C=C  double bond", "4x C-H  single bond",
            "Each C: 0 lone pairs, FC 0", "Each H: FC 0",
            "No resonance forms"]),
        ("Shape", [
            "Each C: 3 groups",
            "  C=C counts as ONE group",
            "  + two C-H = 3, 0 lone pairs",
            "Around each C:", "  trigonal planar",
            "Bond angle: 120 deg",
            "Whole molecule is FLAT"]),
        ("Orbitals", [
            "Each C is sp2 (1 s + 2 p)",
            "  one 2p left on each C,",
            "  sticking out of the plane",
            "sigma: 5   pi: 1",
            "sigma C(sp2)-C(sp2) x1",
            "sigma C(sp2)-H(1s) x4",
            "pi C(2p)-C(2p) x1",
            "  sideways: above and below",
            "  the plane",
            "No lone pairs",
            "The pi bond stops C=C",
            "  from twisting (cis/trans)"]),
        ("Polarity", [
            "C-H  dEN 0.4  polar",
            "  arrow points to C",
            "  On a cutoff: borderline",
            "C=C  dEN 0.0  nonpolar",
            "Molecule: NONPOLAR",
            "  (symmetric, identical",
            "   bonds on each side)"]),
        ("Steps", [
            "1. Valence e- = 12.",
            "2. Two C in the middle,",
            "   two H on each C.",
            "3. 5 single bonds use 10 e-.",
            "4. H duets are full.",
            "5. 2 e- left: one C gets",
            "   a lone pair, other has 6.",
            "6. Lone pair -> C=C bond;",
            "   both C now have octets.",
            "7. All FC 0."]),
    ],
    "C2H2": [
        ("Lewis", [
            "Valence e-:", "  C 4x2 + H 1x2 = 10",
            "Two centers: C and C", "H-C#C-H (# = triple)",
            "1x C#C  triple bond", "2x C-H  single bond",
            "Each C: 0 lone pairs, FC 0", "Each H: FC 0"]),
        ("Shape", [
            "Each C: 2 groups",
            "  C#C counts as ONE group",
            "  + one C-H = 2, 0 lone pairs",
            "Around each C: linear",
            "Bond angle: 180 deg",
            "Whole molecule is a line"]),
        ("Orbitals", [
            "Each C is sp (1 s + 1 p)",
            "  two 2p left on each C",
            "sigma: 3   pi: 2",
            "sigma C(sp)-C(sp) x1",
            "sigma C(sp)-H(1s) x2",
            "pi C(2p)-C(2p) x2",
            "  sideways, at right angles",
            "  to each other",
            "No lone pairs"]),
        ("Polarity", [
            "C-H  dEN 0.4  polar",
            "  arrow points to C",
            "  On a cutoff: borderline",
            "C#C  dEN 0.0  nonpolar",
            "Molecule: NONPOLAR",
            "  (linear and symmetric)"]),
        ("Steps", [
            "1. Valence e- = 10.",
            "2. C-C in the middle, one H",
            "   on each C.",
            "3. 3 single bonds use 6 e-.",
            "4. 4 e- left go on the C's.",
            "5. Neither C has an octet:",
            "   turn 2 lone pairs into",
            "   bonds -> C#C triple.",
            "6. All FC 0."]),
    ],
}


# ----------------------------------------------------------------------
# Screens
# ----------------------------------------------------------------------

VISIBLE = 8
TOP = 50
PITCH = 17


def draw_page(label, pages, page, top):
    title, lines = pages[page]
    screen()
    header(label[:13] + " " + title + " " + str(page + 1) + "/"
           + str(len(pages)))
    for row in range(VISIBLE):
        i = top + row
        if i >= len(lines):
            break
        text = lines[i]
        if (text.startswith("Molecule:") or text.startswith("sigma:")
                or " is sp" in text or text.startswith("Groups on")):
            color(TEAL)
        elif text.startswith("  (a") or "beyond" in text:
            color(GREY)
        else:
            color(BLACK)
        d.draw_text(8, TOP + row * PITCH, text[:30])
    if len(lines) > VISIBLE:
        color(GREY)
        tag = str(top + 1) + "-" + str(min(top + VISIBLE, len(lines)))
        tag += "/" + str(len(lines))
        d.draw_text(315 - len(tag) * 10, 186, tag)
    footer("L/R PAGE  UP/DN  CLEAR BACK")
    present()


def view(label, pages):
    page = 0
    top = 0
    while True:
        draw_page(label, pages, page, top)
        key = tis.wait_key()
        if key == CLEAR:
            return
        if key == RIGHT:
            page = (page + 1) % len(pages)
            top = 0
        elif key == LEFT:
            page = (page - 1) % len(pages)
            top = 0
        elif key == DOWN and top + VISIBLE < len(pages[page][1]):
            top += 1
        elif key == UP and top > 0:
            top -= 1


def draw_menu(selected):
    screen()
    header("BONDING: describe it all")
    first = max(0, min(selected - 3, len(PRESETS) - VISIBLE))
    for row in range(VISIBLE):
        i = first + row
        if i >= len(PRESETS):
            break
        y = TOP + row * PITCH
        if i == selected:
            color(PALE)
            d.fill_rect(4, y - 15, 312, 17)
            color(TEAL)
        else:
            color(BLACK)
        d.draw_text(12, y, PRESETS[i][0][:29])
    color(GREY)
    d.draw_text(8, 186, str(selected + 1) + "/" + str(len(PRESETS)))
    footer("UP/DN MOVE ENT OPEN CLR EXIT")
    present()


def draw_editor(slots, focus, charge, count_mode, message):
    screen()
    header("BONDING: custom formula")
    for i in range(5):
        y = 52 + i * 22
        if i == focus:
            color(PALE)
            d.fill_rect(4, y - 16, 312, 20)
        color(TEAL if i == focus else BLACK)
        if i < 4:
            sym, n = slots[i]
            left = "<" + sym + ">" if (i == focus and not count_mode) \
                else " " + sym + " "
            num = "[" + str(n) + "]" if (i == focus and count_mode) \
                else " " + str(n) + " "
            d.draw_text(12, y, "Element " + left)
            d.draw_text(186, y, "count " + num)
        else:
            d.draw_text(12, y, "Charge  <" + fc_text(charge) + ">")
    color(GREY)
    d.draw_text(8, 168, message[:30])
    d.draw_text(8, 185, "2ND: element/count")
    footer("ENT BUILD  CLEAR MENU")
    present()


def draw_error(message):
    screen()
    header("CANNOT BUILD THAT")
    color(RED)
    for i, line in enumerate(wrap(message)[:3]):
        d.draw_text(8, 60 + i * 18, line)
    color(BLACK)
    d.draw_text(8, 125, "Use one central atom with")
    d.draw_text(8, 143, "outer atoms around it,")
    d.draw_text(8, 161, "2 to 7 atoms in all.")
    footer("ENT EDIT  CLEAR MENU")
    present()


def formula_label(slots, charge):
    out = ""
    for sym, n in slots:
        if n:
            out += sym + (str(n) if n > 1 else "")
    return out + charge_text(charge)


def open_preset(i):
    label, atoms, charge = PRESETS[i]
    if atoms is None:
        return label.split(" ")[0], HAND[charge]
    r = build_lewis(list(atoms), charge)
    return label.split(" ")[0], describe(r, charge)


def main():
    mode = "menu"
    selected = 0
    slots = [["C", 1], ["H", 4], ["O", 0], ["N", 0]]
    focus = 0
    charge = 0
    count_mode = False
    error = ""
    while True:
        if mode == "menu":
            draw_menu(selected)
        elif mode == "edit":
            draw_editor(slots, focus, charge, count_mode,
                        "Formula: " + formula_label(slots, charge))
        else:
            draw_error(error)
        key = tis.wait_key()

        if mode == "menu":
            if key == CLEAR:
                break
            if key == UP:
                selected = (selected - 1) % len(PRESETS)
            elif key == DOWN:
                selected = (selected + 1) % len(PRESETS)
            elif key == ENTER:
                if PRESETS[selected][1] is None and \
                        PRESETS[selected][2] is None:
                    mode = "edit"
                else:
                    try:
                        label, pages = open_preset(selected)
                        view(label, pages)
                    except Exception as exc:
                        error = str(exc)
                        mode = "error"
        elif mode == "edit":
            if key == CLEAR:
                mode = "menu"
            elif key == SECOND and focus < 4:
                count_mode = not count_mode
            elif key == UP:
                if count_mode and focus < 4:
                    slots[focus][1] = min(6, slots[focus][1] + 1)
                else:
                    focus = (focus - 1) % 5
            elif key == DOWN:
                if count_mode and focus < 4:
                    slots[focus][1] = max(0, slots[focus][1] - 1)
                else:
                    focus = (focus + 1) % 5
            elif key in (LEFT, RIGHT):
                step = 1 if key == RIGHT else -1
                if focus == 4:
                    charge = max(-3, min(3, charge + step))
                elif not count_mode:
                    k = ELEMENT_CHOICES.index(slots[focus][0])
                    slots[focus][0] = ELEMENT_CHOICES[
                        (k + step) % len(ELEMENT_CHOICES)]
            elif key == ENTER:
                try:
                    atoms = []
                    for sym, n in slots:
                        if n:
                            found = False
                            for a in atoms:
                                if a[0] == sym:
                                    a[1] += n
                                    found = True
                            if not found:
                                atoms.append([sym, n])
                    r = build_lewis([(a[0], a[1]) for a in atoms], charge)
                    view(formula_label(slots, charge), describe(r, charge))
                except Exception as exc:
                    error = str(exc)
                    mode = "error"
        else:
            if key == CLEAR:
                mode = "menu"
            elif key == ENTER:
                mode = "edit"
    screen()
    present()


main()
