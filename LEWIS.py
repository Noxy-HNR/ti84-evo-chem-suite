"""LEWIS.py -- worksheet-guided Lewis structure builder for TI-84 Evo.

Builds one-center molecules and ions from a formula, shows the Lewis method
one step at a time, and draws the final structure. Use arrow keys to edit;
ENTER advances; CLEAR backs up or exits.
"""

import math
import ti_draw as d
import ti_system as tis
from CHEMCORE import *

LEFT = 24
UP = 25
RIGHT = 26
DOWN = 34
CLEAR = 45
ENTER = 105
SECOND = 21

WHITE = (248, 250, 249)
BLACK = (25, 40, 48)
NAVY = (24, 47, 56)
GREY = (102, 121, 128)
PALE = (224, 235, 232)
TEAL = (15, 112, 94)
GOLD = (239, 211, 147)
RED = (178, 57, 57)
ELEMENT_CHOICES = ("H", "B", "C", "N", "O", "F", "Si", "P", "S",
                   "Cl", "Br", "I", "Xe")

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


def header(label):
    color(NAVY)
    d.fill_rect(0, 0, 320, 26)
    color(TEAL)
    d.fill_rect(0, 24, 320, 2)
    color(WHITE)
    d.draw_text(5, 19, label[:31])


def footer(label):
    color(NAVY)
    d.fill_rect(0, 189, 320, 21)
    color(TEAL)
    d.fill_rect(0, 189, 320, 2)
    color(WHITE)
    d.draw_text(4, 206, label[:31])


def formula_text(slots, charge):
    out = ""
    for atom, count in slots:
        if count:
            out += atom
            if count > 1:
                out += str(count)
    if not out:
        out = "(empty)"
    if charge:
        out += str(abs(charge)) + ("+" if charge > 0 else "-")
    return out


def draw_editor(slots, focus, charge, count_mode, message):
    screen()
    header("LEWIS STRUCTURE BUILDER")
    color(BLACK)
    d.draw_text(8, 47, "Choose formula atoms and counts:")
    for i in range(4):
        y = 72 + i * 23
        atom, count = slots[i]
        if i == focus:
            color(PALE)
            d.fill_rect(6, y - 14, 170, 20)
        color(TEAL if i == focus else BLACK)
        d.draw_text(12, y, ">" if i == focus else " ")
        d.draw_text(34, y, atom)
        d.draw_text(84, y, "count: " + str(count))
        d.draw_text(138, y, "COUNT" if i == focus and count_mode else
                    ("ATOM" if i == focus else ""))
    if focus == 4:
        color(PALE)
        d.fill_rect(184, 112, 124, 39)
    color(BLACK)
    d.draw_text(192, 73, "Formula")
    color(TEAL)
    d.draw_text(192, 92, formula_text(slots, charge)[:12])
    color(BLACK)
    d.draw_text(192, 123, "Charge")
    color(TEAL)
    d.draw_text(192, 142, str(charge))
    color(GREY)
    d.draw_text(10, 174, message[:30])
    footer("2ND FIELD  UP/DN  ENTER BUILD")
    present()


def wrap_line(line, width=29):
    words = line.split(" ")
    result = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if len(trial) > width and current:
            result.append(current)
            current = word
        else:
            current = trial
    if current:
        result.append(current)
    return result


def draw_steps(result, step_index, message):
    screen()
    header("LEWIS: WORKED METHOD")
    color(TEAL)
    d.draw_text(8, 45, "Formula: " + message[:16])
    color(GREY)
    d.draw_text(238, 45, str(step_index + 1) + "/" + str(len(result["steps"])))
    lines = wrap_line(result["steps"][step_index])
    color(BLACK)
    y = 76
    for line in lines[:4]:
        d.draw_text(10, y, line)
        y += 19
    color(GREY)
    d.draw_text(10, 151, "ENTER next step / show structure")
    footer("UP/DOWN STEP  ENTER DIAGRAM")
    present()


def _charge_label(value):
    if value == 0:
        return ""
    return ("+" if value > 0 else "-") + str(abs(value))


def _pair_marks(x, y, angle, count, spacing=7):
    # Draw each lone pair as two small electron dots.
    ux, uy = math.cos(angle), math.sin(angle)
    px, py = -uy, ux
    color(BLACK)
    for pair in range(count):
        shift = (pair - (count - 1) / 2.0) * spacing
        mx = x + int(ux * 17 + px * shift)
        my = y + int(uy * 17 + py * shift)
        d.fill_circle(mx - 2, my, 1)
        d.fill_circle(mx + 2, my, 1)


def draw_structure(result, formula, resonance_index):
    screen()
    header("LEWIS: " + formula[:23])
    ligands = result["ligands"]
    center = result["center"]
    cx, cy = 158, 105
    radius = 65 if len(ligands) >= 5 else 58
    positions = []
    for i in range(len(ligands)):
        angle = -math.pi / 2.0 + 2.0 * math.pi * i / len(ligands)
        positions.append((cx + int(math.cos(angle) * radius),
                          cy + int(math.sin(angle) * radius), angle))
    forms = result["resonance"]
    orders = forms[resonance_index % len(forms)]
    charges = []
    central_lone = result["electrons"] - 2 * sum(orders) - sum(
        [8 - 2 * orders[i] if atom != "H" else 0
         for i, atom in enumerate(ligands)])
    # Hydrogen's duet needs no nonbonding electrons; other terminal shells
    # have octets, and bond orders consume two electrons each.
    central_charge = LEWIS_VALENCE[center] - central_lone - sum(orders)
    for i, atom in enumerate(ligands):
        lone_e = 0 if atom == "H" else 8 - 2 * orders[i]
        charges.append(LEWIS_VALENCE[atom] - lone_e - orders[i])

    # Bonds, offset for double and triple lines.
    color(BLACK)
    for i, (x, y, angle) in enumerate(positions):
        order = orders[i]
        px, py = -math.sin(angle), math.cos(angle)
        offsets = [0] if order == 1 else ([-2, 2] if order == 2 else [-3, 0, 3])
        for offset in offsets:
            d.draw_line(cx + int(px * offset), cy + int(py * offset),
                        x - int(math.cos(angle) * 9) + int(px * offset),
                        y - int(math.sin(angle) * 9) + int(py * offset))

    # Terminal atom labels and lone pairs.
    for i, (x, y, angle) in enumerate(positions):
        atom = ligands[i]
        lp_count = 0 if atom == "H" else (8 - 2 * orders[i]) // 2
        color(TEAL)
        d.draw_text(x - len(atom) * 5, y + 4, atom)
        q = _charge_label(charges[i])
        if q:
            color(RED)
            d.draw_text(x + 10, y - 8, q[:3])
        # Position lone pairs on the sides facing away from the bond.
        _pair_marks(x, y, angle + math.pi / 2.0, lp_count)
    color(NAVY)
    d.fill_circle(cx, cy, 15)
    color(WHITE)
    d.draw_text(cx - len(center) * 5, cy + 4, center)
    if central_lone > 0:
        _pair_marks(cx, cy, -math.pi / 2.0, central_lone // 2, 8)
    if central_charge:
        color(RED)
        d.draw_text(cx + 11, cy - 12, _charge_label(central_charge)[:3])

    color(GREY)
    d.draw_text(8, 171, "Formal charges are shown at each atom.")
    footer("LEFT/RIGHT RESONANCE  CLEAR BACK")
    present()


def draw_error(message):
    screen()
    header("LEWIS BUILDER")
    color(RED)
    d.draw_text(8, 65, "Cannot build this formula:")
    color(BLACK)
    for i, line in enumerate(wrap_line(message, 28)[:4]):
        d.draw_text(8, 89 + i * 18, line)
    color(GREY)
    d.draw_text(8, 160, "This version uses one central")
    d.draw_text(8, 176, "atom and terminal atoms only.")
    footer("ENTER BACK TO FORMULA")
    present()


def main():
    slots = [["H", 2], ["O", 1], ["C", 0], ["N", 0]]
    focus = 0
    charge = 0
    count_mode = False
    mode = "edit"
    message = "H2O is loaded as an example."
    result = None
    formula = ""
    step = 0
    resonance = 0
    error = ""
    while True:
        if mode == "edit":
            draw_editor(slots, focus, charge, count_mode, message)
        elif mode == "steps":
            draw_steps(result, step, formula)
        elif mode == "diagram":
            draw_structure(result, formula, resonance)
        else:
            draw_error(error)
        key = tis.wait_key()
        if key == CLEAR:
            if mode == "edit":
                break
            if mode in ("steps", "error"):
                mode = "edit"
            else:
                mode = "steps"
        elif mode == "edit":
            if key == UP:
                if count_mode and focus < 4:
                    slots[focus][1] = min(6, slots[focus][1] + 1)
                else:
                    focus = (focus - 1) % 5
            elif key == DOWN:
                if count_mode and focus < 4:
                    slots[focus][1] = max(0, slots[focus][1] - 1)
                else:
                    focus = (focus + 1) % 5
            elif key == LEFT:
                if focus == 4:
                    charge = max(-3, charge - 1)
                else:
                    atom, count = slots[focus]
                    slots[focus][0] = ELEMENT_CHOICES[(ELEMENT_CHOICES.index(atom) - 1) % len(ELEMENT_CHOICES)]
            elif key == RIGHT:
                if focus == 4:
                    charge = min(3, charge + 1)
                else:
                    atom, count = slots[focus]
                    slots[focus][0] = ELEMENT_CHOICES[(ELEMENT_CHOICES.index(atom) + 1) % len(ELEMENT_CHOICES)]
            elif key == ENTER:
                # Charge is edited on the last row with a small key gesture.
                try:
                    result = build_lewis([(s[0], s[1]) for s in slots if s[1]], charge)
                    formula = formula_text(slots, charge)
                    step = 0
                    resonance = 0
                    mode = "steps"
                except Exception as exc:
                    error = str(exc)
                    mode = "error"
            elif key == SECOND:
                count_mode = not count_mode
        elif mode == "steps":
            if key == UP:
                step = max(0, step - 1)
            elif key == DOWN:
                step = min(len(result["steps"]) - 1, step + 1)
            elif key == ENTER:
                if step < len(result["steps"]) - 1:
                    step += 1
                else:
                    mode = "diagram"
        elif mode == "diagram":
            if key == LEFT or key == RIGHT:
                resonance = (resonance + 1) % len(result["resonance"])
        elif mode == "error" and key == ENTER:
            mode = "edit"
    screen()
    present()


main()
