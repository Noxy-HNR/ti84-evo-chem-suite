# QNUMS.py -- quantum numbers, forwards and backwards, for the TI-84 Evo.
#
# Set any of n, l, ml and ms -- or leave them "any" -- and press ENTER:
#
#   * all four set: says whether the set is allowed, and if not, which
#     rule it breaks (no n = 0; l up to n-1; ml from -l to +l)
#   * some set: works backwards (9/2 notes) -- lists every orbital that
#     fits and counts the orbitals and electrons, e.g. "how many
#     electrons can have n = 3, ml = -1?" -> 3p and 3d -> 4 electrons
#
# LEFT/RIGHT picks a box, UP/DOWN changes it, CLEAR exits.
# Self-contained: no CHEMCORE needed.

import ti_draw as d
import ti_system as tis

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

LETTERS = "spdfghi"
NMAX = 7                   # the periodic table stops at n = 7

# option lists for each box; None means "any". n and l deliberately
# include impossible values (n = 0, l > n - 1) so they can be tested.
N_OPTS = [None] + list(range(0, NMAX + 1))
L_OPTS = [None] + list(range(0, 7))
ML_OPTS = [None] + list(range(-6, 7))
MS_OPTS = [None, 1, -1]            # +1/2 and -1/2

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
# The rules
# ----------------------------------------------------------------------

def ms_text(ms):
    return "+1/2" if ms > 0 else "-1/2"


def signed(v):
    return ("+" if v > 0 else "") + str(v)


def ml_range(l):
    if l == 0:
        return "0"
    return "-" + str(l) + "..+" + str(l)


def problems(n, l, ml):
    # Rule violations among the values that are set. -> lines.
    bad = []
    if n == 0:
        bad.append("No n = 0: energy levels")
        bad.append("  start at n = 1")
    if n and l is not None and l > n - 1:
        bad.append("l must be 0 to n-1 = " + str(n - 1))
        bad.append("  so there is no " + str(n) + LETTERS[l]
                   + " subshell")
    if l is not None and ml is not None and abs(ml) > l:
        bad.append("ml must be -l to +l:")
        bad.append("  for l = " + str(l) + ", ml = " + ml_range(l))
    if n and l is None and ml is not None and abs(ml) > n - 1:
        bad.append("ml = " + signed(ml) + " needs l >= "
                   + str(abs(ml)) + ",")
        bad.append("  but l <= n-1 = " + str(n - 1))
    return bad


def orbitals(n, l, ml):
    # Every (n, l, ml) allowed by the values that are set.
    out = []
    shells = [n] if n else range(1, NMAX + 1)
    for nn in shells:
        subs = [l] if l is not None else range(nn)
        for ll in subs:
            if ll > nn - 1:
                continue
            mls = [ml] if ml is not None else range(-ll, ll + 1)
            for mm in mls:
                if abs(mm) <= ll:
                    out.append((nn, ll, mm))
    return out


def subshell_lines(found, per):
    # Group orbitals by subshell: '3p  ml -1..+1  3 orb'.
    lines = []
    seen = []
    for nn, ll, mm in found:
        if (nn, ll) in seen:
            continue
        seen.append((nn, ll))
        mls = [m for (a, b, m) in found if (a, b) == (nn, ll)]
        if len(mls) == 1:
            span = signed(mls[0])
        else:
            span = signed(mls[0]) + ".." + signed(mls[-1])
        count = len(mls)
        lines.append(str(nn) + LETTERS[ll] + "  ml " + span + "  "
                     + str(count) + " orb, " + str(count * per) + " e-")
    return lines


def analyze(n, l, ml, ms):
    # -> (title, lines).
    bad = problems(n, l, ml)
    if bad:
        return "NOT ALLOWED", bad + ["", "Rules: n = 1, 2, 3...",
                                     "  l = 0 to n-1",
                                     "  ml = -l to +l",
                                     "  ms = +1/2 or -1/2"]

    per = 1 if ms is not None else 2
    if n is not None and l is not None and ml is not None and \
            ms is not None:
        name = str(n) + LETTERS[l]
        return "VALID SET", [
            "n = " + str(n) + ": energy level " + str(n),
            "l = " + str(l) + ": " + LETTERS[l] + " shape -> " + name,
            "ml = " + signed(ml) + ": one of the",
            "  " + str(2 * l + 1) + " " + name + " orbitals",
            "ms = " + ms_text(ms) + ": spin "
            + ("up" if ms > 0 else "down"),
            "One electron in " + name + ".",
            "(Pauli: no other electron in",
            " the atom has all four same)"]

    if n is None:
        return "WORK BACKWARDS", backwards(l, ml, ms)

    found = orbitals(n, l, ml)
    lines = []
    if l is None and ml is None:
        lines.append("Shell n = " + str(n) + ": l = 0.." + str(n - 1))
        lines.append("  orbitals = n^2 = " + str(n * n))
        lines.append("  electrons = 2n^2 = " + str(2 * n * n))
    lines.extend(subshell_lines(found, per))
    lines.append("Total: " + str(len(found)) + " orbital"
                 + ("" if len(found) == 1 else "s") + ", "
                 + str(len(found) * per) + " e-")
    if ms is not None:
        lines.append("  (ms set: 1 e- per orbital)")
    else:
        lines.append("  (2 e- per orbital, +/- 1/2)")
    return "COUNT", lines


def backwards(l, ml, ms):
    # n is unknown, so there is no upper limit to count to: describe
    # the pattern instead (9/2: 'working backwards').
    lines = []
    if l is not None:
        letter = LETTERS[l]
        lines.append("l = " + str(l) + " -> " + letter + " subshell")
        lines.append("ml = " + ml_range(l) + " -> " + str(2 * l + 1)
                     + " orbital" + ("" if l == 0 else "s"))
        lines.append("holds " + str(2 * (2 * l + 1)) + " electrons")
        lines.append("n can be " + str(l + 1) + " or higher:")
        first = [str(k) + letter for k in range(l + 1, min(l + 4, NMAX + 1))]
        lines.append("  " + ", ".join(first) + "...")
        lines.append("smallest n = " + str(l + 1) + " (l <= n-1)")
        if ml is not None:
            lines.append("ml = " + signed(ml) + ": 1 orbital in each")
        if ms is not None:
            lines.append("ms = " + ms_text(ms) + ": 1 e- per orbital")
    elif ml is not None:
        m = abs(ml)
        lines.append("ml = " + signed(ml) + " needs l >= " + str(m))
        allowed = [LETTERS[k] for k in range(m, 4)]
        lines.append("  so l = " + str(m) + ", " + str(m + 1)
                     + "... (" + " ".join(allowed) + "...)")
        lines.append("smallest n = " + str(m + 1))
        if m == 0:
            lines.append("ml = 0 fits every subshell:")
            lines.append("  one of each set of boxes")
        if ms is not None:
            lines.append("ms = " + ms_text(ms) + ": 1 e- per orbital")
    elif ms is not None:
        lines.append("ms = " + ms_text(ms) + " (spin "
                     + ("up" if ms > 0 else "down") + ")")
        lines.append("Every orbital holds one")
        lines.append("  electron of each spin.")
    else:
        lines = ["Set at least one number.",
                 "Rules (9/2 notes):",
                 "  n = 1, 2, 3...  (no n = 0)",
                 "  l = 0 to n-1  (s p d f)",
                 "  ml = -l to +l  (the boxes)",
                 "  ms = +1/2 or -1/2",
                 "Orbitals in shell n: n^2",
                 "Electrons in shell n: 2n^2"]
    return lines


# ----------------------------------------------------------------------
# Screens
# ----------------------------------------------------------------------

LABELS = ("n", "l", "ml", "ms")


def value_text(box, value):
    if value is None:
        return "any"
    if box == 1:
        # "1 (p)", not "1p": in the l box, 1p would read as the
        # subshell that cannot exist
        return str(value) + " (" + LETTERS[value] + ")"
    if box == 2:
        return signed(value)
    if box == 3:
        return ms_text(value)
    return str(value)


def draw_editor(values, pos):
    screen()
    header("QNUMS: quantum numbers")
    for b in range(4):
        x = 12 + b * 76
        color(GREY)
        d.draw_text(x + 30 - len(LABELS[b]) * 5, 56, LABELS[b])
        if b == pos:
            color(NAVY)
            d.fill_rect(x, 66, 64, 36)
            color(WHITE)
        else:
            color(PALE)
            d.fill_rect(x, 66, 64, 36)
            color(BLACK)
        text = value_text(b, values[b])
        d.draw_text(x + 32 - len(text) * 5, 91, text)
    # live check, so a bad combination shows before ENTER
    bad = problems(values[0], values[1], values[2])
    if bad:
        color(RED)
        d.draw_text(8, 130, bad[0][:30])
        d.draw_text(8, 147, bad[1][:30])
    else:
        color(TEAL)
        d.draw_text(8, 130, "So far this is allowed.")
    color(GREY)
    d.draw_text(8, 168, "'any' = unknown / not given")
    d.draw_text(8, 185, "L/R box  UP/DN value")
    footer("ENT SOLVE  CLEAR EXIT")
    present()


def show(title, lines):
    top = 0
    while True:
        screen()
        header("QNUMS: " + title)
        for row in range(8):
            i = top + row
            if i >= len(lines):
                break
            text = lines[i]
            if title == "NOT ALLOWED" and i < len(lines) - 5:
                color(RED)
            elif text.startswith("Total") or text.startswith("One elec"):
                color(TEAL)
            else:
                color(BLACK)
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


def main():
    opts = (N_OPTS, L_OPTS, ML_OPTS, MS_OPTS)
    # the classic backwards question: n = 3, ml = -1, how many e-?
    idx = [N_OPTS.index(3), 0, ML_OPTS.index(-1), 0]
    pos = 0
    while True:
        values = [opts[b][idx[b]] for b in range(4)]
        draw_editor(values, pos)
        key = tis.wait_key()
        if key == CLEAR:
            break
        if key == LEFT:
            pos = (pos - 1) % 4
        elif key == RIGHT:
            pos = (pos + 1) % 4
        elif key == UP:
            idx[pos] = (idx[pos] + 1) % len(opts[pos])
        elif key == DOWN:
            idx[pos] = (idx[pos] - 1) % len(opts[pos])
        elif key == ENTER:
            title, lines = analyze(values[0], values[1], values[2],
                                   values[3])
            show(title, lines)
    screen()
    present()


main()
