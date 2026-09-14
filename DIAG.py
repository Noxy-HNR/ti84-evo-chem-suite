"""DIAG.py -- throwaway. Tells us what this calculator actually does.

Transfer it, run it, and report what you see. It answers three things
I could not settle from TI's documentation:

  1. does anything I draw actually reach the screen
  2. does this build have use_buffer / paint_buffer
  3. what key code does each number key send

Nothing here depends on the rest of the suite. Delete it afterwards.
"""

import ti_draw as d
import ti_system as tis


# ----------------------------------------------------------------------
# Part 1: shell report. print() needs no graphics, so this shows up
# even if every drawing call silently goes nowhere.
# ----------------------------------------------------------------------

print("")
print("== DIAG: what this build has ==")

NAMES = ("use_buffer", "paint_buffer", "show_draw", "clear",
         "fill_rect", "draw_rect", "draw_text", "set_color",
         "set_pen", "get_screen_dim")
missing = []
for fn in NAMES:
    ok = hasattr(d, fn)
    if not ok:
        missing.append(fn)
    print(("  " + fn + " ").ljust(18, ".") + (" yes" if ok else " NO"))

try:
    print("  screen dim: " + str(d.get_screen_dim()))
except:
    print("  screen dim: FAILED")

buffered = False
try:
    d.use_buffer()
    buffered = True
    print("  use_buffer(): ok")
except:
    print("  use_buffer(): FAILED or absent")

print("")
print("Now look at the SCREEN.")
print("Press any key here to draw.")
tis.wait_key()


# ----------------------------------------------------------------------
# Part 2: draw something impossible to miss.
# ----------------------------------------------------------------------

def show():
    if buffered:
        try:
            d.paint_buffer()
        except:
            pass


d.set_color(255, 255, 255)
d.fill_rect(0, 0, 320, 210)

d.set_color(200, 30, 30)
d.fill_rect(20, 30, 280, 70)
d.set_color(255, 255, 255)
d.draw_text(34, 60, "IF YOU SEE THIS")
d.draw_text(34, 85, "RED BOX -- SAY SO")

# a strip of small filled squares, the same way the table draws cells
d.set_color(0, 0, 0)
d.draw_text(20, 130, "cells below:")
for i in range(16):
    d.set_color(30 + i * 12, 90, 200 - i * 10)
    d.fill_rect(20 + i * 17, 140, 15, 12)

# one-pixel runs, which is how the tiny element symbols are drawn
d.set_color(0, 0, 0)
d.draw_text(20, 180, "dots:")
for i in range(20):
    d.fill_rect(80 + i * 4, 168, 1, 1)
    d.fill_rect(80 + i * 4, 172, 2, 1)

show()
tis.wait_key()


# ----------------------------------------------------------------------
# Part 3: key codes. This is the part I most need.
# ----------------------------------------------------------------------

WANT = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        ".", "(-) negative", "DEL", "ENTER")

found = []
idx = 0
while idx < len(WANT):
    d.set_color(255, 255, 255)
    d.fill_rect(0, 0, 320, 210)
    d.set_color(18, 45, 73)
    d.fill_rect(0, 0, 320, 30)
    d.set_color(255, 255, 255)
    d.draw_text(6, 22, "KEY CODES  " + str(idx + 1) + " of " + str(len(WANT)))

    d.set_color(0, 0, 0)
    d.draw_text(20, 70, "press the key:")
    d.set_color(200, 30, 30)
    d.draw_text(20, 105, WANT[idx])
    d.set_color(120, 130, 140)
    d.draw_text(20, 150, "press CLEAR(45) to skip")
    if found:
        d.draw_text(20, 175, "last: " + found[-1][:24])
    show()

    k = tis.wait_key()
    if k != 45 or WANT[idx] == "CLEAR":
        found.append(WANT[idx] + " = " + str(k))
    idx += 1

# ----------------------------------------------------------------------
# Results go to the shell, where they can be scrolled and read back.
# ----------------------------------------------------------------------

d.set_color(255, 255, 255)
d.fill_rect(0, 0, 320, 210)
d.set_color(0, 0, 0)
d.draw_text(20, 90, "Done -- read the SHELL")
d.draw_text(20, 115, "for the codes.")
show()

print("")
print("== KEY CODES -- send me these ==")
for line in found:
    print("  " + line)
if missing:
    print("  MISSING: " + ", ".join(missing))
print("  buffered: " + str(buffered))
print("== end ==")
