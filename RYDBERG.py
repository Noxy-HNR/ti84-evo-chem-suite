"""RYDBERG.py -- hydrogen transitions worked out step by step.

Standalone program. Needs CHEMCORE.py on the calculator as well.

    1/L = Rb (1/nf^2 - 1/ni^2)      Rb = 1.097e-2 nm^-1
    E   = hc / L

Three modes, matching CHEMCORE:
    1  ni and nf are known      -> wavelength and energy
    2  wavelength or energy and one level known -> the other level
    3  energy in kJ/mol         -> J per photon, then wavelength

Every mode draws the substituted equation and the intermediate values,
not just the answer, because that is what the course asks you to show.

Numbers are entered with the arrow keys rather than at a shell prompt:
the Evo keeps the graphics screen up for the whole program, so nothing
here has to hand the screen back to the shell to read a value.
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

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NAVY = (18, 45, 73)
TEAL = (0, 119, 133)
RED = (200, 60, 60)
GREY = (150, 160, 170)
PALE = (238, 241, 244)

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


def pause(seconds):
    try:
        tis.sleep(seconds)
    except:
        try:
            tis.wait(seconds)
        except:
            pass


# ----------------------------------------------------------------------
# Input widgets
# ----------------------------------------------------------------------

def pick_int(title, prompt, value, low, high):
    """Spin a small integer with UP/DOWN. -> int, or None if cancelled."""
    while True:
        screen(WHITE)
        header(title)
        color(GREY)
        d.draw_text(10, 56, prompt[:31])
        color(NAVY)
        d.fill_rect(120, 78, 80, 52)
        color(WHITE)
        text = str(value)
        d.draw_text(160 - len(text) * 5, 114, text)
        color(GREY)
        d.draw_text(10, 156, "range " + str(low) + " to " + str(high))
        footer("UP/DN VALUE   ENT OK")
        present()

        k = tis.wait_key()
        if k == CLEAR:
            return None
        if k == ENTER:
            return value
        if k == UP and value < high:
            value += 1
        elif k == DOWN and value > low:
            value -= 1
        elif k == RIGHT and value + 10 <= high:
            value += 10
        elif k == LEFT and value - 10 >= low:
            value -= 10


def ask_value(title, prompt, unit, digits=None):
    """Enter a number as NNNN.N with the arrow keys.

    Four whole digits and one decimal covers every wavelength and
    molar energy this course uses, and needs no shell prompt.
    """
    if digits is None:
        digits = [0, 6, 5, 6, 3]
    pos = 0
    while True:
        screen(WHITE)
        header(title)
        color(GREY)
        d.draw_text(10, 52, prompt[:31])

        x0 = 60
        for i in range(5):
            x = x0 + i * 34 + (14 if i == 4 else 0)
            if i == pos:
                color(NAVY)
                d.fill_rect(x - 4, 72, 32, 44)
                color(WHITE)
            else:
                color(BLACK)
            d.draw_text(x + 3, 104, str(digits[i]))
        color(BLACK)
        d.draw_text(x0 + 4 * 34 - 2, 104, ".")

        value = (digits[0] * 1000 + digits[1] * 100 + digits[2] * 10
                 + digits[3] + digits[4] / 10.0)
        color(TEAL)
        d.draw_text(10, 148, "= " + sci(value) + " " + unit)
        color(GREY)
        d.draw_text(10, 170, "UP/DN digit, L/R move")
        footer("ENT OK   CLR CANCEL")
        present()

        k = tis.wait_key()
        if k == CLEAR:
            return None
        if k == ENTER:
            if value > 0:
                return value
        elif k == LEFT:
            pos = (pos - 1) % 5
        elif k == RIGHT:
            pos = (pos + 1) % 5
        elif k == UP:
            digits[pos] = (digits[pos] + 1) % 10
        elif k == DOWN:
            digits[pos] = (digits[pos] - 1) % 10


def choose(title, items):
    """Small arrow-driven menu. -> index, or -1 if cancelled."""
    selected = 0
    while True:
        screen(WHITE)
        header(title)
        for i in range(len(items)):
            y = 62 + i * 30
            if i == selected:
                color(TEAL)
                d.fill_rect(8, y - 20, 304, 26)
                color(WHITE)
            else:
                color(BLACK)
            d.draw_text(16, y, items[i][:29])
        footer("UP/DN MOVE  ENT SELECT")
        present()

        k = tis.wait_key()
        if k == CLEAR:
            return -1
        if k == ENTER:
            return selected
        if k == UP:
            selected = (selected - 1) % len(items)
        elif k == DOWN:
            selected = (selected + 1) % len(items)


# ----------------------------------------------------------------------
# Step display
# ----------------------------------------------------------------------

VISIBLE_LINES = 8
LINE_TOP = 44
LINE_PITCH = 17


def draw_steps(title, steps, top, foot):
    screen(WHITE)
    header(title)
    color(BLACK)
    for row in range(VISIBLE_LINES):
        i = top + row
        if i >= len(steps):
            break
        line = steps[i]
        # the final answer of each block is worth picking out
        if line.startswith("L = ") or line.startswith("E = ") \
                or line.startswith("nearest"):
            color(TEAL)
        else:
            color(BLACK)
        d.draw_text(8, LINE_TOP + row * LINE_PITCH, line[:31])
    if len(steps) > VISIBLE_LINES:
        color(GREY)
        d.draw_text(250, 178, str(top + 1) + "-"
                    + str(min(top + VISIBLE_LINES, len(steps))))
    footer(foot)
    present()


def animate_steps(title, steps):
    """Reveal the working one line at a time, the way it would be
    written out on paper.

    Once the page is full it scrolls rather than stopping, so the run
    finishes on the answer instead of leaving it below the fold.
    Returns the scroll position it ended at.
    """
    for shown in range(1, len(steps) + 1):
        top = max(0, shown - VISIBLE_LINES)
        draw_steps(title, steps[:shown], top, "working...")
        pause(0.22)
    return max(0, len(steps) - VISIBLE_LINES)


def step_screen(title, steps, lam=None):
    # start where the animation left off -- on the answer, with the
    # earlier lines one UP press away
    top = animate_steps(title, steps)
    foot = "UP/DN SCROLL  CLR BACK"
    if lam is not None:
        foot = "ENT SPECTRUM  CLR BACK"
    while True:
        draw_steps(title, steps, top, foot)
        k = tis.wait_key()
        if k == CLEAR:
            return
        if k == UP and top > 0:
            top -= 1
        elif k == DOWN and top + VISIBLE_LINES < len(steps):
            top += 1
        elif k == ENTER and lam is not None:
            spectrum_screen(lam)


# ----------------------------------------------------------------------
# Visible spectrum bar
# ----------------------------------------------------------------------

BAR_X = 16
BAR_W = 288
BAR_Y = 74
BAR_H = 46


def bar_x_for(lam):
    frac = (lam - VIS_MIN) / (VIS_MAX - VIS_MIN)
    return BAR_X + int(frac * BAR_W)


def spectrum_screen(lam):
    screen(WHITE)
    header("Visible spectrum")

    # one vertical strip per pixel across 380-700 nm
    d.set_pen("thin", "solid")
    for i in range(BAR_W):
        nm = VIS_MIN + (VIS_MAX - VIS_MIN) * i / float(BAR_W)
        r, g, b = visible_color(nm)
        d.set_color(r, g, b)
        d.fill_rect(BAR_X + i, BAR_Y, 1, BAR_H)

    color(BLACK)
    d.draw_rect(BAR_X, BAR_Y, BAR_W, BAR_H)
    color(GREY)
    d.draw_text(BAR_X - 4, BAR_Y + BAR_H + 18, "380")
    d.draw_text(BAR_X + BAR_W - 60, BAR_Y + BAR_H + 18, "700 nm")

    region = spectrum_region(lam)
    if is_visible(lam):
        x = bar_x_for(lam)
        color(BLACK)
        d.set_pen("medium", "solid")
        d.draw_line(x, BAR_Y - 12, x, BAR_Y + BAR_H + 6)
        # a small pointer above the bar
        d.fill_poly([x - 5, x + 5, x], [BAR_Y - 12, BAR_Y - 12, BAR_Y - 3])
        label = sci(lam) + " nm"
        tx = x - len(label) * 5
        if tx < 2:
            tx = 2
        if tx > 320 - len(label) * 10:
            tx = 320 - len(label) * 10
        d.draw_text(tx, BAR_Y - 18, label)
    else:
        # clear of the 380/700 axis labels above
        color(RED)
        d.draw_text(10, 158, sci(lam) + " nm is " + region)
        color(GREY)
        arrow = "<- shorter" if lam < VIS_MIN else "longer ->"
        d.draw_text(10, 178, arrow + ", off this bar")

    if is_visible(lam):
        color(BLACK)
        d.draw_text(10, 158, region + ",  " + sci(lam) + " nm")

    footer("CLR BACK")
    present()
    while True:
        k = tis.wait_key()
        if k in (CLEAR, ENTER, SECOND):
            return


# ----------------------------------------------------------------------
# The three modes
# ----------------------------------------------------------------------

def mode_levels():
    ni = pick_int("Mode 1: levels", "Starting level  ni", 3, 1, 30)
    if ni is None:
        return
    nf = pick_int("Mode 1: levels", "Ending level  nf", 2, 1, 30)
    if nf is None:
        return
    if ni == nf:
        message("ni and nf must differ.")
        return

    lam, e, steps, kind = from_levels(ni, nf)
    head = [str(ni) + " -> " + str(nf) + "  (" + kind + ")"]
    series = series_for(nf)
    if series:
        head.append(series + " series")
    head.append("")
    steps = head + steps
    steps.append("")
    steps.append(spectrum_region(lam) + " light")
    step_screen("ni=" + str(ni) + " nf=" + str(nf), steps, lam)


def mode_find_level():
    which = choose("Mode 2: find a level", (
        "Know wavelength (nm)",
        "Know energy (1e-19 J)",
    ))
    if which < 0:
        return

    if which == 0:
        lam = ask_value("Wavelength", "Wavelength in nm", "nm")
        if lam is None:
            return
        pre = []
    else:
        scaled = ask_value("Energy", "Energy, times 1e-19 J", "e-19 J",
                           [0, 0, 0, 3, 0])
        if scaled is None:
            return
        e = scaled * 1e-19
        lam = energy_to_wavelength(e)
        pre = [
            "E = " + sci(e) + " J",
            "L = hc / E",
            "L = " + sci(lam) + " nm",
            "",
        ]

    known = choose("Which level do you know?", (
        "I know nf (the end)",
        "I know ni (the start)",
    ))
    if known < 0:
        return
    known_is = "nf" if known == 0 else "ni"

    n = pick_int("Known level", "Value of " + known_is, 2, 1, 30)
    if n is None:
        return

    raw, near, steps = solve_for_n(lam, n, known_is)
    steps = pre + steps
    if raw is not None:
        gap = abs(raw - near)
        steps.append("")
        if gap > 0.05:
            steps.append("off a whole n by " + sci(gap, 2))
            steps.append("check the wavelength")
        else:
            steps.append("clean whole-number fit")
    step_screen("Solve for " + ("ni" if known_is == "nf" else "nf"),
                steps, lam)


def mode_molar():
    kj = ask_value("Mode 3: kJ/mol", "Energy in kJ/mol", "kJ/mol",
                   [0, 1, 8, 2, 0])
    if kj is None:
        return
    e, lam, steps = from_molar_energy(kj)
    steps = steps + ["", spectrum_region(lam) + " light"]
    step_screen("kJ/mol -> photon", steps, lam)


def message(text):
    screen(WHITE)
    header("Check that again")
    color(RED)
    d.draw_text(10, 80, text[:31])
    footer("any key")
    present()
    tis.wait_key()


# ----------------------------------------------------------------------
# Main menu
# ----------------------------------------------------------------------

MODES = (
    "1  ni and nf -> L, E",
    "2  L or E + one n -> n",
    "3  kJ/mol -> J, L",
    "   Show the spectrum",
    "   Quit",
)


def main():
    try:
        while True:
            pick = choose("RYDBERG SOLVER", MODES)
            if pick in (-1, 4):
                return
            if pick == 0:
                mode_levels()
            elif pick == 1:
                mode_find_level()
            elif pick == 2:
                mode_molar()
            elif pick == 3:
                lam = ask_value("Spectrum", "Wavelength in nm", "nm")
                if lam is not None:
                    spectrum_screen(lam)
    finally:
        screen(WHITE)
        present()


main()
