"""HYBRID.py -- steric number to hybridization chart for the TI-84 Evo.

Standalone reference chart for CHEM 1450. The steric number is the number
of sigma-bonded regions plus lone pairs around the central atom.

UP/DOWN highlights a chart row. ENTER explains how to count regions.
CLEAR exits.
"""

import ti_draw as d
import ti_system as tis


UP = 25
DOWN = 34
CLEAR = 45
ENTER = 105

BLACK = (25, 40, 48)
WHITE = (248, 250, 249)
NAVY = (24, 47, 56)
GREY = (102, 121, 128)
PALE = (224, 235, 232)
TEAL = (15, 112, 94)

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


def draw_hybrid(x, y, exponent, d_suffix, ink):
    """Draw sp with a raised exponent and optional d using calculator text."""
    color(ink)
    d.draw_text(x, y, "sp")
    # Draw superscripts separately so the calculator needs only ASCII glyphs.
    if exponent:
        d.draw_text(x + 20, y - 8, str(exponent))
    if d_suffix:
        d.draw_text(x + 30, y, "d")
        if d_suffix == 2:
            d.draw_text(x + 40, y - 8, "2")


ROWS = (
    ("2", 0, "Linear", 0),
    ("3", 2, "Trigonal planar", 0),
    ("4", 3, "Tetrahedral", 0),
    ("5", 3, "Trigonal", 1),
    ("6", 3, "Octahedral", 2),
)


def draw_chart(selected):
    screen()
    header("HYBRIDIZATION CHART")

    color(BLACK)
    d.draw_text(8, 43, "Count sigma bonds and lone pairs")
    d.draw_text(8, 60, "on the central atom.")

    color(TEAL)
    d.draw_text(12, 79, "Total")
    d.draw_text(102, 79, "Hybrid")
    d.draw_text(174, 79, "Geometry")
    d.draw_line(8, 83, 312, 83)

    baselines = (103, 122, 141, 160, 181)
    for i, row in enumerate(ROWS):
        total, exponent, geometry, d_suffix = row
        y = baselines[i]
        if i == selected:
            color(TEAL)
            d.fill_rect(7, y - 17, 306, 19)
            color(WHITE)
        else:
            color(BLACK)

        d.draw_text(33, y, total)
        draw_hybrid(104, y, exponent, d_suffix,
                    WHITE if i == selected else BLACK)
        if i == 3:
            d.draw_text(166, y, "Trigonal bipyr.")
        else:
            d.draw_text(166, y, geometry)

    footer("UP/DN ROW  ENTER INFO  CLEAR")
    present()


def draw_note():
    screen()
    header("COUNTING REGIONS")
    color(BLACK)
    d.draw_text(10, 53, "A single bond has one sigma")
    d.draw_text(10, 72, "bond: count it as one region.")
    d.draw_text(10, 103, "A double or triple bond still")
    d.draw_text(10, 122, "counts as one sigma region.")
    d.draw_text(10, 153, "Each lone pair counts as one")
    d.draw_text(10, 172, "region around the central atom.")
    footer("ENTER CHART  CLEAR EXIT")
    present()


def main():
    selected = 0
    showing_note = False
    while True:
        if showing_note:
            draw_note()
        else:
            draw_chart(selected)

        key = tis.wait_key()
        if key == CLEAR:
            if showing_note:
                showing_note = False
            else:
                break
        elif key == ENTER:
            showing_note = not showing_note
        elif not showing_note and key == UP:
            selected = (selected - 1) % len(ROWS)
        elif not showing_note and key == DOWN:
            selected = (selected + 1) % len(ROWS)

    screen()
    present()


main()
