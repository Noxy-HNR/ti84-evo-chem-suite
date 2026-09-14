"""ORBITAL.py -- animated Hund's-rule orbital filling for the TI-84 Evo.

Standalone program. Needs CHEMCORE.py on the calculator as well.

Enter a subshell such as 2p4 and watch the electrons drop in one at a
time: every orbital takes a single spin-up electron before any orbital
takes a second. Ends on the finished diagram, the unpaired count and
the paramagnetic / diamagnetic verdict.

Two ways in, because the Evo has no documented on-screen keyboard:
typing the notation at the shell prompt, or building it with the
arrow keys without leaving the graphics screen.
"""

import ti_draw as d
import ti_system as tis

from CHEMCORE import *

LEFT = 24
UP = 25
RIGHT = 26
DOWN = 34
SECOND = 21
CLEAR = 45
ENTER = 105

BLACK = (25, 40, 48)
WHITE = (248, 250, 249)
NAVY = (24, 47, 56)
TEAL = (15, 112, 94)
RED = (178, 57, 57)
GREY = (102, 121, 128)
PALE = (224, 235, 232)

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
    d.fill_rect(0, 0, 320, 210)


def header(text):
    color(NAVY)
    d.fill_rect(0, 0, 320, 25)
    color(TEAL)
    d.fill_rect(0, 24, 320, 2)
    color(WHITE)
    d.draw_text(4, 19, text[:31])


def footer(text):
    color(NAVY)
    d.fill_rect(0, 183, 320, 27)
    color(TEAL)
    d.fill_rect(0, 183, 320, 2)
    color(WHITE)
    d.draw_text(4, 203, text[:31])


def centre(y, text, c=BLACK):
    color(c)
    d.draw_text((320 - len(text) * 10) // 2, y, text[:31])


def pause(seconds):
    """sleep() is the documented name; wait() is the older spelling."""
    try:
        tis.sleep(seconds)
    except:
        try:
            tis.wait(seconds)
        except:
            pass


# ----------------------------------------------------------------------
# Orbital drawing
# ----------------------------------------------------------------------

BOX_TOP = 78


def box_metrics(count):
    """Box width, gap and left edge for a row of `count` orbitals.

    An f subshell is seven boxes wide, so the boxes shrink rather than
    running off a 320 pixel screen.
    """
    bw, gap = 30, 8
    if count > 5:
        bw, gap = 20, 4
    if count > 7:
        bw, gap = 16, 3
    total = count * bw + (count - 1) * gap
    return bw, gap, (320 - total) // 2


def draw_arrow(x, top, up, height=24):
    d.set_pen("thin", "solid")
    head = 4
    if up:
        d.draw_line(x, top + height - 2, x, top + 3)
        d.draw_line(x, top + 3, x - head, top + 3 + head)
        d.draw_line(x, top + 3, x + head, top + 3 + head)
    else:
        d.draw_line(x, top + 3, x, top + height - 2)
        d.draw_line(x, top + height - 2, x - head, top + height - 2 - head)
        d.draw_line(x, top + height - 2, x + head, top + height - 2 - head)


def draw_empty_boxes(count):
    bw, gap, x0 = box_metrics(count)
    for i in range(count):
        bx = x0 + i * (bw + gap)
        color(WHITE)
        d.fill_rect(bx, BOX_TOP, bw, 28)
        color(BLACK)
        d.set_pen("thin", "solid")
        d.draw_rect(bx, BOX_TOP, bw, 28)


def draw_electron(count, index, second):
    """Put one electron into orbital `index`.

    `second` picks the paired spin-down arrow, drawn to the right of
    the spin-up one so a filled orbital reads as a genuine pair.
    """
    bw, gap, x0 = box_metrics(count)
    bx = x0 + index * (bw + gap)
    offset = bw // 4
    if second:
        color(RED)
        draw_arrow(bx + bw // 2 + offset, BOX_TOP, False)
    else:
        color(TEAL)
        draw_arrow(bx + bw // 2 - offset, BOX_TOP, True)


def draw_ml_labels(l):
    """m_l values under each box: -l .. +l."""
    count = 2 * l + 1
    bw, gap, x0 = box_metrics(count)
    color(GREY)
    for i in range(count):
        ml = i - l
        text = str(ml)
        bx = x0 + i * (bw + gap)
        d.draw_text(bx + (bw - len(text) * 10) // 2, BOX_TOP + 46, text)


def animate(n, l, count):
    label = subshell_label(n, l) + str(count)
    width = 2 * l + 1
    seq = fill_sequence(l, count)

    screen(WHITE)
    header("Filling " + label)
    centre(56, "Hund's rule, one at a time", GREY)
    draw_empty_boxes(width)
    draw_ml_labels(l)
    footer("filling...")
    present()
    pause(0.45)

    placed = [0] * width
    for step in range(len(seq)):
        idx = seq[step]
        draw_electron(width, idx, placed[idx] == 1)
        placed[idx] += 1
        # repaint the counter line each frame
        color(WHITE)
        d.fill_rect(0, 140, 320, 22)
        centre(158, "electron " + str(step + 1) + " of " + str(count), NAVY)
        present()
        pause(0.32)

    boxes = hund_fill(l, count)
    color(WHITE)
    d.fill_rect(0, 140, 320, 22)
    return result_screen(n, l, count, boxes)


def result_screen(n, l, count, boxes):
    label = subshell_label(n, l) + str(count)
    u = unpaired(boxes)
    mag = magnetism(boxes)

    color(WHITE)
    d.fill_rect(0, 138, 320, 45)
    color(BLACK)
    d.draw_text(14, 156, "Unpaired electrons: " + str(u))
    color(RED if mag == "Paramagnetic" else TEAL)
    d.draw_text(14, 176, mag)
    header(label + "   done")
    footer("ENT AGAIN   CLR MENU")
    present()

    while True:
        k = tis.wait_key()
        if k in (CLEAR, SECOND):
            return False
        if k == ENTER:
            return True


def show_error(message):
    screen(WHITE)
    header("Not a subshell")
    color(RED)
    d.draw_text(10, 70, message[:31])
    color(BLACK)
    d.draw_text(10, 104, "Examples: 2p4  3d7  1s2")
    d.draw_text(10, 124, "n first, then s p d f,")
    d.draw_text(10, 144, "then how many electrons.")
    footer("any key")
    present()
    tis.wait_key()


# ----------------------------------------------------------------------
# Getting a subshell out of the user
# ----------------------------------------------------------------------

def ask_typed():
    """Read notation at the shell prompt.

    This leaves the graphics screen for as long as the prompt is up;
    the caller redraws afterwards. If the build will not give us a
    prompt at all, fall back to the arrow picker rather than dying.
    """
    try:
        print("")
        print("Subshell notation, e.g. 2p4")
        print("(blank cancels)")
        raw = input("> ")
    except:
        return "NOINPUT"
    if raw is None or str(raw).strip() == "":
        return None
    return raw


def draw_picker(n, l, count, field):
    screen(WHITE)
    header("Build a subshell")
    parts = [str(n), ORB[l], str(count)]
    labels = ["n", "type", "e-"]
    widths = [60, 60, 60]
    x = 40
    for i in range(3):
        active = i == field
        color(NAVY if active else PALE)
        d.fill_rect(x, 70, widths[i], 44)
        color(WHITE if active else BLACK)
        d.draw_text(x + (widths[i] - len(parts[i]) * 10) // 2, 100, parts[i])
        color(NAVY if active else GREY)
        d.draw_text(x + (widths[i] - len(labels[i]) * 10) // 2, 132, labels[i])
        x += widths[i] + 10

    color(BLACK)
    d.draw_text(10, 160, "= " + subshell_label(n, l) + str(count))
    cap = capacity(l)
    if l >= n:
        color(RED)
        d.draw_text(10, 178, "no such subshell")
    elif count > cap:
        color(RED)
        d.draw_text(10, 178, "max " + str(cap) + " electrons")
    else:
        color(GREY)
        d.draw_text(10, 178, "holds up to " + str(cap))
    footer("L/R FIELD UP/DN VAL ENT OK")
    present()


def ask_picked():
    """Build a subshell with the arrow keys only.

    Nothing here depends on a keyboard prompt, so it works even if the
    shell is unavailable while the graphics screen is up.
    """
    n, l, count = 2, 1, 4
    field = 0
    while True:
        draw_picker(n, l, count, field)
        k = tis.wait_key()
        if k == CLEAR:
            return None
        if k == ENTER:
            if l < n and count <= capacity(l):
                return n, l, count
        elif k == LEFT:
            field = (field - 1) % 3
        elif k == RIGHT:
            field = (field + 1) % 3
        elif k in (UP, DOWN):
            step = 1 if k == UP else -1
            if field == 0:
                n = min(8, max(1, n + step))
                if l >= n:
                    l = n - 1
            elif field == 1:
                l = min(3, max(0, l + step))
                if l >= n:
                    n = l + 1
            else:
                count = min(capacity(l), max(0, count + step))
            if count > capacity(l):
                count = capacity(l)


# ----------------------------------------------------------------------
# Menu
# ----------------------------------------------------------------------

ITEMS = (
    "Type notation (2p4)",
    "Build with arrows",
    "Quit",
)


def draw_menu(selected):
    screen(WHITE)
    header("ORBITAL DIAGRAMS")
    color(GREY)
    d.draw_text(10, 48, "Hund's rule, animated")
    for i in range(len(ITEMS)):
        y = 82 + i * 30
        if i == selected:
            color(PALE)
            d.fill_rect(8, y - 20, 304, 26)
            color(TEAL)
            d.fill_rect(8, y - 20, 3, 26)
            color(BLACK)
        else:
            color(BLACK)
        d.draw_text(18, y, ITEMS[i])
    footer("UP/DN MOVE  ENT SELECT")
    present()


def menu():
    selected = 0
    while True:
        draw_menu(selected)
        k = tis.wait_key()
        if k == CLEAR:
            return -1
        if k == ENTER:
            return selected
        if k == UP:
            selected = (selected - 1) % len(ITEMS)
        elif k == DOWN:
            selected = (selected + 1) % len(ITEMS)


def run_subshell(n, l, count):
    again = animate(n, l, count)
    while again:
        again = animate(n, l, count)


def main():
    try:
        while True:
            choice = menu()
            if choice in (-1, 2):
                return

            picked = None
            if choice == 0:
                raw = ask_typed()
                if raw == "NOINPUT":
                    picked = ask_picked()
                elif raw is None:
                    continue
                else:
                    try:
                        picked = parse_subshell(raw)
                    except ValueError as err:
                        show_error(str(err))
                        continue
            else:
                picked = ask_picked()

            if picked is not None:
                run_subshell(picked[0], picked[1], picked[2])
    finally:
        screen(WHITE)
        present()


main()
