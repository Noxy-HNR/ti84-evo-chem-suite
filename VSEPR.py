"""VSEPR.py -- interactive VSEPR chart for the TI-84 Evo.

Rows are total electron regions (sigma bonds plus lone pairs); columns
are lone pairs on the central atom. UP/DOWN and LEFT/RIGHT move through
valid AXmEn entries. ENTER explains the selected geometry. CLEAR exits.
"""

import math
import ti_draw as d
import ti_system as tis


LEFT = 24
UP = 25
RIGHT = 26
DOWN = 34
CLEAR = 45
ENTER = 105

BLACK = (25, 40, 48)
WHITE = (248, 250, 249)
NAVY = (24, 47, 56)
GREY = (102, 121, 128)
PALE = (224, 235, 232)
TEAL = (15, 112, 94)
GOLD = (239, 211, 147)

DATA = {
    (2, 0): ("Li", "Linear", "180 deg", "sp"),
    (3, 0): ("TP", "Trigonal planar", "120 deg", "sp^2"),
    (3, 1): ("Be", "Bent", "<120 deg", "sp^2"),
    (4, 0): ("Te", "Tetrahedral", "109.5 deg", "sp^3"),
    (4, 1): ("Py", "Trigonal pyramidal", "~107 deg", "sp^3"),
    (4, 2): ("Be", "Bent", "~104.5 deg", "sp^3"),
    (5, 0): ("TB", "Trigonal bipyramidal", "90/120/180", "sp^3d"),
    (5, 1): ("Se", "Seesaw", "<90, 120 deg", "sp^3d"),
    (5, 2): ("T", "T-shaped", "~90 deg", "sp^3d"),
    (5, 3): ("Li", "Linear", "180 deg", "sp^3d"),
    (6, 0): ("Oc", "Octahedral", "90 deg", "sp^3d^2"),
    (6, 1): ("SP", "Square pyramidal", "~90 deg", "sp^3d^2"),
    (6, 2): ("Sq", "Square planar", "90 deg", "sp^3d^2"),
    (6, 3): ("T", "T-shaped", "~90 deg", "sp^3d^2"),
    (6, 4): ("Li", "Linear", "180 deg", "sp^3d^2"),
}

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
    d.draw_text(5, 19, text)


def footer(text):
    color(NAVY)
    d.fill_rect(0, 190, 320, 20)
    color(TEAL)
    d.fill_rect(0, 190, 320, 2)
    color(WHITE)
    d.draw_text(5, 207, text[:31])


def formula(regions, lone_pairs):
    bonded = regions - lone_pairs
    x = "X" if bonded == 1 else "X" + str(bonded)
    if lone_pairs == 0:
        return "A" + x
    e = "E" if lone_pairs == 1 else "E" + str(lone_pairs)
    return "A" + x + e


def draw_matrix(selected_regions, selected_pairs):
    color(TEAL)
    d.draw_text(7, 43, "REG")
    d.draw_text(43, 43, "LP")
    for lp in range(5):
        x = 66 + lp * 26
        d.draw_text(x + 7, 60, str(lp))

    for regions in range(2, 7):
        y = 79 + (regions - 2) * 21
        color(BLACK)
        d.draw_text(10, y, str(regions))
        for lp in range(5):
            x = 60 + lp * 26
            item = DATA.get((regions, lp))
            if item:
                if (regions, lp) == (selected_regions, selected_pairs):
                    color(TEAL)
                    d.fill_rect(x, y - 16, 25, 19)
                    color(WHITE)
                else:
                    color(BLACK)
                label = item[0]
                d.draw_text(x + max(0, (25 - len(label) * 10) // 2), y,
                            label)
            else:
                color(GREY)
                d.draw_text(x + 10, y, "-")

    color(GREY)
    d.draw_line(194, 34, 194, 184)


def draw_sketch(regions, lone_pairs):
    """A small 2-D domain sketch for the selected AXmEn entry."""
    bonded = regions - lone_pairs
    cx, cy = 257, 151
    radius = 28
    points = []
    for i in range(bonded):
        angle = -math.pi / 2.0 + (2.0 * math.pi * i / max(1, bonded))
        points.append((cx + int(math.cos(angle) * radius),
                       cy + int(math.sin(angle) * radius)))
    color(GREY)
    for x, y in points:
        d.draw_line(cx, cy, x, y)
    color(TEAL)
    for x, y in points:
        d.fill_circle(x, y, 3)
        d.draw_text(x - 5, y + 4, "X")
    color(NAVY)
    d.fill_circle(cx, cy, 5)
    color(WHITE)
    d.draw_text(cx - 5, cy + 4, "A")

    # Lone-pair marks sit around the center, opposite the bond directions.
    for i in range(lone_pairs):
        angle = math.pi / 2.0 + (2.0 * math.pi * i / max(1, lone_pairs))
        px = cx + int(math.cos(angle) * 15)
        py = cy + int(math.sin(angle) * 15)
        color(NAVY)
        d.fill_circle(px - 2, py, 1)
        d.fill_circle(px + 2, py, 1)


def draw_detail(regions, lone_pairs):
    item = DATA[(regions, lone_pairs)]
    name, angle, hybrid = item[1], item[2], item[3]
    x = 202
    color(BLACK)
    # Shape names wrap at the right pane width.
    if len(name) > 11:
        words = name.split(" ")
        first = ""
        second = ""
        for word in words:
            trial = word if not first else first + " " + word
            if len(trial) <= 11:
                first = trial
            else:
                second = word if not second else second + " " + word
        d.draw_text(x, 48, first[:11])
        d.draw_text(x, 64, second[:11])
        base = 82
    else:
        d.draw_text(x, 54, name)
        base = 72
    d.draw_text(x, base, formula(regions, lone_pairs))
    d.draw_text(x, base + 16, hybrid)
    d.draw_text(x, base + 32, angle[:11])
    draw_sketch(regions, lone_pairs)


def draw_chart(regions, lone_pairs):
    screen()
    header("VSEPR: REGIONS + LONE PAIRS")
    draw_matrix(regions, lone_pairs)
    draw_detail(regions, lone_pairs)
    footer("ARROWS MOVE  ENTER NOTE  CLEAR")
    present()


def draw_note():
    screen()
    header("HOW TO READ THE TABLE")
    color(BLACK)
    d.draw_text(9, 51, "Row = total electron regions:")
    d.draw_text(9, 69, "sigma bonds + lone pairs.")
    d.draw_text(9, 99, "Column = lone pairs on A.")
    d.draw_text(9, 129, "Each cell gives AXmEn, the")
    d.draw_text(9, 147, "molecular shape, and a sketch.")
    d.draw_text(9, 177, "LP = lone pair; X = bonded atom.")
    footer("ENTER CHART  CLEAR EXIT")
    present()


def move(regions, lone_pairs, dr, dc):
    r = regions + dr
    lp = lone_pairs + dc
    if r < 2 or r > 6 or lp < 0 or lp > 4:
        return regions, lone_pairs
    if (r, lp) not in DATA:
        return regions, lone_pairs
    return r, lp


def main():
    regions = 4
    lone_pairs = 0
    note = False
    while True:
        if note:
            draw_note()
        else:
            draw_chart(regions, lone_pairs)
        key = tis.wait_key()
        if key == CLEAR:
            if note:
                note = False
            else:
                break
        elif key == ENTER:
            note = not note
        elif not note and key == UP:
            regions, lone_pairs = move(regions, lone_pairs, -1, 0)
        elif not note and key == DOWN:
            regions, lone_pairs = move(regions, lone_pairs, 1, 0)
        elif not note and key == LEFT:
            regions, lone_pairs = move(regions, lone_pairs, 0, -1)
        elif not note and key == RIGHT:
            regions, lone_pairs = move(regions, lone_pairs, 0, 1)
    screen()
    present()


main()
