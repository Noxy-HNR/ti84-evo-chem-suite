"""PTABLE.py -- graphical periodic table for the TI-84 Evo.

Standalone program. Needs CHEMCORE.py on the calculator as well.

    LEFT/RIGHT   previous / next atomic number
    ZOOM/TRACE   jump 10 at a time
    Y=           show or hide element symbols
    WINDOW       go straight to an atomic number
    UP/DOWN      move up or down the column
    ENTER        element detail
    CLEAR        exit

From the detail screen, ENTER opens the Hund's-rule orbital diagram
for that element's outermost subshell.
"""

import ti_draw as d
import ti_system as tis

from CHEMCORE import *

# Key codes for the Evo keypad. These are the values the hardware
# actually returns -- the TI-84 Plus CE uses a different set, so its
# published table is no help here.
LEFT = 24
UP = 25
RIGHT = 26
DOWN = 34
SECOND = 21
CLEAR = 45
ENTER = 105

# The five keys under the screen. Confirmed on the Evo, and the only
# spare buttons whose codes are known -- the number keys are not
# documented anywhere I could find, so nothing here depends on them.
YEQU = 11
WINDOW = 12
ZOOM = 13
TRACE = 14
GRAPH = 15

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NAVY = (18, 45, 73)
GREY = (188, 198, 207)
PALE = (238, 241, 244)
TEAL = (0, 119, 133)
RED = (200, 60, 60)

# One colour per block, so the shape of the table teaches the blocks
BLOCK_COLOR = {
    "s": (232, 106, 106),
    "p": (86, 148, 214),
    "d": (240, 190, 84),
    "f": (118, 196, 158),
}

# ----------------------------------------------------------------------
# Screen plumbing
# ----------------------------------------------------------------------
#
# use_buffer / paint_buffer are not in the published module list but do
# exist on the Evo, so probe for them and fall back to drawing straight
# to the screen if they are missing.

BUFFERED = False
try:
    if hasattr(d, "use_buffer") and hasattr(d, "paint_buffer"):
        d.use_buffer()
        BUFFERED = True
except:
    BUFFERED = False


def present():
    if BUFFERED:
        d.paint_buffer()


def color(c):
    d.set_color(c[0], c[1], c[2])


def screen(c=WHITE):
    color(c)
    d.fill_rect(-1, -1, 322, 212)


def header(text):
    color(NAVY)
    d.fill_rect(-1, -1, 322, 25)
    color(WHITE)
    d.draw_text(4, 19, text[:31])


def footer(text):
    color(NAVY)
    d.fill_rect(-1, 183, 322, 28)
    color(WHITE)
    d.draw_text(4, 203, text[:31])


# ----------------------------------------------------------------------
# 3x5 pixel font
# ----------------------------------------------------------------------
#
# draw_text is locked to 10 pixels per character, and a table cell is
# only 17 wide, so a two-letter symbol needs its own tiny font. Each
# row is three bits: 4 is the left pixel, 2 the middle, 1 the right.

GLYPH = {
    "A": (2, 5, 7, 5, 5), "B": (6, 5, 6, 5, 6), "C": (3, 4, 4, 4, 3),
    "D": (6, 5, 5, 5, 6), "E": (7, 4, 6, 4, 7), "F": (7, 4, 6, 4, 4),
    "G": (3, 4, 5, 5, 3), "H": (5, 5, 7, 5, 5), "I": (7, 2, 2, 2, 7),
    "J": (1, 1, 1, 5, 2), "K": (5, 5, 6, 5, 5), "L": (4, 4, 4, 4, 7),
    "M": (5, 7, 7, 5, 5), "N": (5, 6, 7, 3, 5), "O": (2, 5, 5, 5, 2),
    "P": (6, 5, 6, 4, 4), "Q": (2, 5, 5, 2, 1), "R": (6, 5, 6, 5, 5),
    "S": (3, 4, 2, 1, 6), "T": (7, 2, 2, 2, 2), "U": (5, 5, 5, 5, 7),
    "V": (5, 5, 5, 5, 2), "W": (5, 5, 7, 7, 5), "X": (5, 5, 2, 5, 5),
    "Y": (5, 5, 2, 2, 2), "Z": (7, 1, 2, 4, 7),
}


def mini_text(x, y, text):
    """Draw text in the 3x5 font with the current colour.

    Set pixels are emitted as horizontal runs rather than one call per
    pixel; on a 156 MHz core that is the difference between a table
    that snaps up and one that visibly crawls.
    """
    for ch in text:
        rows = GLYPH.get(ch)
        if rows:
            for r in range(5):
                bits = rows[r]
                run = 0
                for col in range(3):
                    if bits & (4 >> col):
                        run += 1
                    elif run:
                        d.fill_rect(x + col - run, y + r, run, 1)
                        run = 0
                if run:
                    d.fill_rect(x + 3 - run, y + r, run, 1)
        x += 4


def mini_width(text):
    return len(text) * 4 - 1


# ----------------------------------------------------------------------
# Table geometry
# ----------------------------------------------------------------------

CW = 17          # cell width
CH = 13          # cell height
PITCH = 15       # row to row
X0 = 7
Y0 = 31
FGAP = 8         # blank strip above the lanthanide / actinide rows

N = element_count()


def _cell_xy(z):
    col, row = table_position(z)
    x = X0 + (col - 1) * CW
    y = Y0 + (row - 1) * PITCH
    if row >= 8:
        y += FGAP
    return x, y


# Work the geometry out once, at load. table_position() is a chain of
# range tests, and recomputing it for 118 cells on every repaint was
# pure waste.
CELLS = tuple(_cell_xy(z) for z in range(1, N + 1))

# Cells grouped by block, so a full repaint sets the colour four times
# instead of 118 times. On a 156 MHz core the call count is what you
# feel, and this is the difference between the table appearing at once
# and it crawling in.
BLOCKS = ("s", "p", "d", "f")
BLOCK_MEMBERS = {}
for _b in BLOCKS:
    BLOCK_MEMBERS[_b] = tuple(z for z in range(1, N + 1) if block_of(z) == _b)

SHOW_SYMBOLS = False     # off by default: symbols cost ~8 calls a cell


def cell_xy(z):
    return CELLS[z - 1]


def draw_symbol(z):
    x, y = CELLS[z - 1]
    sym = symbol(z).upper()
    mini_text(x + (CW - mini_width(sym)) // 2, y + 3, sym)


def draw_cell(z, selected=False):
    """Repaint one cell. Used for the two cells that change as the
    cursor moves, so holding an arrow key stays responsive."""
    x, y = CELLS[z - 1]
    if selected:
        color(NAVY)
        d.fill_rect(x, y, CW - 1, CH - 1)
        color(WHITE)
        mini_text(x + (CW - mini_width(symbol(z).upper())) // 2, y + 3,
                  symbol(z).upper())
    else:
        color(BLOCK_COLOR.get(block_of(z), GREY))
        d.fill_rect(x, y, CW - 1, CH - 1)
        if SHOW_SYMBOLS:
            color(BLACK)
            draw_symbol(z)


def fill_table(cursor):
    """Paint all 118 cells, grouped by colour.

    Cells are drawn one pixel short of the pitch, so the white ground
    shows through as the grid lines. That removes a draw_rect and a
    set_pen from every cell -- 236 calls saved -- and looks the same.
    """
    for b in BLOCKS:
        color(BLOCK_COLOR[b])
        for z in BLOCK_MEMBERS[b]:
            x, y = CELLS[z - 1]
            d.fill_rect(x, y, CW - 1, CH - 1)

    if SHOW_SYMBOLS:
        color(BLACK)
        for z in range(1, N + 1):
            if z != cursor:
                draw_symbol(z)

    # placeholders in the empty group-3 slots, so the two detached
    # strips visibly belong under the main body of the table
    color(GREY)
    for row in (6, 7):
        x = X0 + 2 * CW
        y = Y0 + (row - 1) * PITCH
        d.fill_rect(x, y, CW - 1, CH - 1)
    color(WHITE)
    mini_text(X0 + 2 * CW + 3, Y0 + 5 * PITCH + 3, "LA")
    mini_text(X0 + 2 * CW + 3, Y0 + 6 * PITCH + 3, "AC")

    draw_cell(cursor, True)


def title_for(z):
    return str(z) + " " + symbol(z) + " " + name(z)


SOFTKEYS = ("SYMBOL", "GOTO", "-10", "+10", "EXIT")


def softkeys():
    """Label the five keys under the screen, the way the calculator's
    own menus do. These are the only extra keys whose codes are
    confirmed on the Evo."""
    color(NAVY)
    d.fill_rect(-1, 183, 322, 28)
    color(WHITE)
    d.set_pen("thin", "solid")
    for i in range(1, 5):
        d.draw_line(i * 64, 184, i * 64, 210)
    for i in range(5):
        label = SOFTKEYS[i]
        x = i * 64 + (64 - len(label) * 10) // 2
        d.draw_text(x, 204, label)


def draw_table(cursor):
    screen(WHITE)
    header(title_for(cursor))
    fill_table(cursor)
    softkeys()
    present()


def vertical_move(z, step):
    """Move one row up or down, staying in the same column.

    Rows are ragged, so walk outward from the target row and take the
    nearest occupied column rather than assuming one exists.
    """
    col, row = table_position(z)
    target = row + step
    while 1 <= target <= 9:
        best = None
        best_gap = 99
        for cand in range(1, element_count() + 1):
            c2, r2 = table_position(cand)
            if r2 != target:
                continue
            gap = abs(c2 - col)
            if gap < best_gap:
                best_gap = gap
                best = cand
        if best is not None:
            return best
        target += step
    return z


# ----------------------------------------------------------------------
# Orbital diagram for the outermost subshell
# ----------------------------------------------------------------------

def draw_arrow(x, y, up):
    """A spin arrow inside an orbital box."""
    d.set_pen("thin", "solid")
    if up:
        d.draw_line(x, y + 14, x, y + 2)
        d.draw_line(x, y + 2, x - 3, y + 6)
        d.draw_line(x, y + 2, x + 3, y + 6)
    else:
        d.draw_line(x, y + 2, x, y + 14)
        d.draw_line(x, y + 14, x - 3, y + 10)
        d.draw_line(x, y + 14, x + 3, y + 10)


def draw_boxes(n, l, boxes, top):
    """Orbital boxes centred on screen. Returns the row height used."""
    count = len(boxes)
    bw = 26
    gap = 6
    total = count * bw + (count - 1) * gap
    if total > 300:                      # f subshells need tighter boxes
        bw = 18
        gap = 3
        total = count * bw + (count - 1) * gap
    x = (320 - total) // 2
    for i in range(count):
        bx = x + i * (bw + gap)
        color(WHITE)
        d.fill_rect(bx, top, bw, 20)
        color(BLACK)
        d.set_pen("thin", "solid")
        d.draw_rect(bx, top, bw, 20)
        if boxes[i] >= 1:
            color(TEAL)
            draw_arrow(bx + bw // 2 - 4, top, True)
        if boxes[i] == 2:
            color(RED)
            draw_arrow(bx + bw // 2 + 4, top, False)
    # subshell label under the row
    color(BLACK)
    label = subshell_label(n, l)
    d.draw_text((320 - len(label) * 10) // 2, top + 38, label)
    return 44


def orbital_screen(z):
    n, l, count = outermost_subshell(z)
    boxes = hund_fill(l, count)
    screen(WHITE)
    header(symbol(z) + "  " + subshell_label(n, l) + str(count))
    draw_boxes(n, l, boxes, 52)
    color(BLACK)
    d.draw_text(10, 132, "Unpaired e-: " + str(unpaired(boxes)))
    d.draw_text(10, 152, magnetism(boxes))
    d.draw_text(10, 172, "Outermost subshell only")
    footer("CLR BACK")
    present()
    while True:
        k = tis.wait_key()
        if k in (CLEAR, ENTER, SECOND):
            return


# ----------------------------------------------------------------------
# Detail screen
# ----------------------------------------------------------------------

def wrap(text, width=29):
    words = text.split(" ")
    lines = []
    line = ""
    for w in words:
        trial = w if not line else line + " " + w
        if len(trial) <= width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def draw_detail(z):
    shells = electron_configuration(z)
    screen(WHITE)
    header(title_for(z))

    color(BLACK)
    y = 42
    d.draw_text(8, y, "Mass    " + str(mass(z)) + " u")
    y += 18
    d.draw_text(8, y, "Group   " + group_label(z))
    y += 18
    d.draw_text(8, y, "Period  " + str(period_of(z)))
    y += 18
    d.draw_text(8, y, "Block   " + block_of(z))
    y += 18
    d.draw_text(8, y, "Valence " + str(valence_electrons(z)) + " e-")

    # The heading and the flag share a line on purpose. There is only
    # room for three wrapped configuration lines above the footer, and
    # gold and chromium are exactly the elements where a student most
    # needs to be told the pattern breaks.
    y = 132
    color(TEAL)
    d.draw_text(8, y, "Configuration")
    if is_exception(z):
        color(RED)
        d.draw_text(150, y, "! breaks Aufbau")

    y += 17
    color(BLACK)
    for line in wrap(config_string(shells))[:3]:
        d.draw_text(8, y, line)
        y += 16

    footer("ENT ORBITAL  L/R ELEM  CLR")
    present()


def detail_screen(z):
    while True:
        draw_detail(z)
        k = tis.wait_key()
        if k == CLEAR:
            return z
        if k == ENTER:
            orbital_screen(z)
        elif k == RIGHT and z < element_count():
            z += 1
        elif k == LEFT and z > 1:
            z -= 1


# ----------------------------------------------------------------------
# Main loop
# ----------------------------------------------------------------------

def ask_element(current):
    """Pick an atomic number by digits. -> Z, or None if cancelled.

    Three digit slots reach any element in a handful of presses, where
    stepping there with LEFT/RIGHT could take 117.
    """
    digits = [(current // 100) % 10, (current // 10) % 10, current % 10]
    pos = 2
    while True:
        z = digits[0] * 100 + digits[1] * 10 + digits[2]
        ok = 1 <= z <= N

        screen(WHITE)
        header("Go to element")
        color(GREY)
        d.draw_text(10, 50, "Atomic number 1 to " + str(N))

        for i in range(3):
            x = 92 + i * 46
            if i == pos:
                color(NAVY)
                d.fill_rect(x - 6, 70, 42, 46)
                color(WHITE)
            else:
                color(BLACK)
            d.draw_text(x + 6, 102, str(digits[i]))

        if ok:
            color(TEAL)
            d.draw_text(10, 146, "= " + symbol(z) + "  " + name(z)[:20])
        else:
            color(RED)
            d.draw_text(10, 146, "no element " + str(z))
        color(GREY)
        d.draw_text(10, 170, "UP/DN digit,  L/R move")
        footer("ENT GO   CLR CANCEL")
        present()

        k = tis.wait_key()
        if k in (CLEAR, GRAPH):
            return None
        if k == ENTER and ok:
            return z
        if k == LEFT:
            pos = (pos - 1) % 3
        elif k == RIGHT:
            pos = (pos + 1) % 3
        elif k == UP:
            digits[pos] = (digits[pos] + 1) % 10
        elif k == DOWN:
            digits[pos] = (digits[pos] - 1) % 10


def clamp(z):
    if z < 1:
        return 1
    if z > N:
        return N
    return z


def table_loop():
    global SHOW_SYMBOLS
    cursor = 1
    draw_table(cursor)
    while True:
        k = tis.wait_key()
        if k in (CLEAR, GRAPH):
            return

        if k == YEQU:                       # toggle the element symbols
            SHOW_SYMBOLS = not SHOW_SYMBOLS
            draw_table(cursor)
            continue
        if k == WINDOW:                     # jump straight to an element
            picked = ask_element(cursor)
            cursor = picked if picked else cursor
            draw_table(cursor)
            continue
        if k == ENTER:
            cursor = detail_screen(cursor)
            draw_table(cursor)
            continue

        previous = cursor
        if k == RIGHT:
            cursor = clamp(cursor + 1)
        elif k == LEFT:
            cursor = clamp(cursor - 1)
        elif k == TRACE:
            cursor = clamp(cursor + 10)
        elif k == ZOOM:
            cursor = clamp(cursor - 10)
        elif k == UP:
            cursor = vertical_move(cursor, -1)
        elif k == DOWN:
            cursor = vertical_move(cursor, 1)

        if cursor != previous:
            # repaint only the two cells that changed, so holding an
            # arrow key scrolls smoothly instead of redrawing 118 cells
            draw_cell(previous, False)
            draw_cell(cursor, True)
            header(title_for(cursor))
            present()


def main():
    try:
        table_loop()
    finally:
        screen(WHITE)
        present()


main()
