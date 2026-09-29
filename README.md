> Current release instructions and controls are in [../README.md](../README.md).
> The desktop regression harness is now included in `../tests/`; generated transfer
> files live in `../release/`. Ion controls, full configurations, and orbital paging
> are available in PTABLE. This directory is the authoritative source.

# CHEM 1450 suite — TI-84 Evo

Eleven separate graphical programs plus three small shared modules, for
the TI-84 Evo Python App.

| File | What it is |
|---|---|
| `CHEMCORE.py` | Shared element data: configurations, ions, table positions, valence. Used by PTABLE and FORMULA. |
| `LEWCORE.py` | Shared Lewis-structure solver. Used by LEWIS and BONDING. |
| `POLCORE.py` | Shared textbook electronegativities and VSEPR shape data. Used by POLAR and BONDING. |
| `PTABLE.py` | Graphical periodic table, cursor navigation, element detail. |
| `ORBITAL.py` | Animated Hund's-rule orbital filling. |
| `RYDBERG.py` | Rydberg / photon-energy solver, worked out step by step. |
| `HYBRID.py` | Steric-number to hybridization and electron-geometry chart. |
| `VSEPR.py` | Interactive chart of electron regions, lone pairs, molecular shape, and hybridization. |
| `LEWIS.py` | Formula-driven Lewis structure builder with worksheet steps and resonance forms. |
| `BONDING.py` | "Completely describe the bonding": Lewis, shape, hybridization, every sigma/pi bond by orbital, polarity. |
| `POLAR.py` | Bond polarity from textbook EN values, bond ranking, the molecule symmetry rule. |
| `NAMER.py` | Ionic formulas and names, acid names, covalent prefixes, polyatomic-ion and acid flashcards. |
| `FORMULA.py` | Molar mass with work shown, % by mass, empirical and molecular formulas. |
| `QNUMS.py` | Quantum numbers: validate a set or work backwards and count orbitals/electrons. |

Each graphical program is standalone with its own screen loop. There is
no launcher. Transfer all fourteen files. PTABLE and FORMULA import
CHEMCORE, LEWIS imports LEWCORE, POLAR imports POLCORE, and BONDING
imports LEWCORE and POLCORE. ORBITAL, RYDBERG, NAMER, QNUMS, HYBRID and
VSEPR are self-contained. Pure-Python modules have no ti_draw or
ti_system imports and run on desktop Python. See the parent README for
why the shared code is split: a 38 KB CHEMCORE ran the Evo out of memory.

## Transferring

Connect the Evo over USB-C, open TI Connect Evo, and send all fourteen
`.py` files from `release/`. Then open the Python App and run any of
`PTABLE`, `ORBITAL`, `RYDBERG`, `HYBRID`, `VSEPR`, `LEWIS`, `BONDING`,
`POLAR`, `NAMER`, `FORMULA` or `QNUMS`. Programs load their shared
modules automatically; re-send a shared module whenever it changes.
If a `MemoryError` appears only after running other programs, press
TOOLS -> New Shell first (or reopen the Python app): imported programs
stay loaded.

### About the file names

These are named in TI's 8-character uppercase style rather than
`chemistry_core.py` / `periodic_table.py` / `orbitals.py` /
`rydberg.py`. TI program names have historically been capped at eight
characters, and every working Evo program to hand follows that
(`PERIODIC.py`, and your own `PTABLE`/`ORBITAL`/`RYDBERG`). I could not
find the Evo's naming rule stated anywhere in TI's published
documentation, so this is the conservative choice, not a verified one.

If the Evo does accept long lowercase names, renaming is safe: the only
coupling is the line `from CHEMCORE import *` at the top of each
program. Rename the file and that line together.

## Controls

**PTABLE**

    LEFT/RIGHT   previous / next atomic number
    UP/DOWN      move up or down the column
    ENTER        element detail
    CLEAR        exit

    In detail:   ENTER opens the orbital diagram for the outermost
                 subshell, LEFT/RIGHT step between elements,
                 CLEAR goes back.

**ORBITAL** — pick "Type notation" and enter something like `2p4`, or
"Build with arrows" to assemble the subshell without the keyboard.
ENTER replays the animation, CLEAR returns to the menu.

**RYDBERG** — arrow keys throughout. In a worked answer, ENTER shows
the visible-spectrum bar and UP/DOWN scrolls back through the steps.

**HYBRID** — the chart maps 2–6 total regions (sigma bonds plus lone
pairs) to hybridization and electron-domain geometry. UP/DOWN highlights
a row, ENTER explains how to count regions, and CLEAR exits.

**VSEPR** — the worksheet chart maps total electron regions (sigma bonds
plus lone pairs) against central-atom lone pairs. The selected cell shows
AXmEn, molecular shape, approximate bond angle, hybridization, and a
schematic. Arrow keys move among the valid cells; ENTER shows a short
guide; CLEAR exits.

**LEWIS** — choose a common molecule/ion from the startup list or select
Custom formula. In the formula editor, UP/DOWN selects a row, LEFT/RIGHT
changes its element, and 2ND switches to count editing so UP/DOWN changes
the count (0–6). Select Charge to set an ion charge with LEFT/RIGHT.
ENTER draws the structure directly; LEFT/RIGHT cycles equivalent
resonance forms. Custom structures support one central atom and terminal
atoms; multi-center skeletons such as C2H6 are not supported.

**BONDING** — pick a molecule or ion from the list (or *Custom formula*,
which edits like LEWIS). LEFT/RIGHT turns the five pages (Lewis, Shape,
Orbitals, Polarity, Steps), UP/DOWN scrolls, CLEAR goes back.

**POLAR** — *Bond polarity*: LEFT/RIGHT picks an atom, UP/DOWN changes
it, ENTER shows the bond; 2ND on the result shows the cutoff scale and
notes. *Rank 4 bonds*: LEFT/RIGHT moves between the eight atom boxes,
UP/DOWN changes one, ENTER ranks. *Molecule rule*: UP/DOWN picks a row,
LEFT/RIGHT changes it.

**NAMER** — *Ionic compound*: UP/DOWN switches cation/anion, LEFT/RIGHT
chooses, ENTER builds. *Covalent name*: UP/DOWN picks a row, LEFT/RIGHT
changes it. *Flashcards*: ENTER reveals, LEFT/RIGHT next/previous, 2ND
flips name/formula, UP shuffles.

**FORMULA** — every editor works the same way: LEFT/RIGHT moves between
boxes, UP/DOWN changes one, ZOOM/TRACE jumps by 10, ENTER calculates.
Results page with LEFT/RIGHT. A molar mass of 0 skips the molecular
formula step.

**QNUMS** — LEFT/RIGHT picks the n, l, ml or ms box; UP/DOWN changes it
("any" means not given). A broken rule shows live under the boxes; ENTER
gives the full answer.

## Chemistry notes

**Electron configurations are the measured ground states, not a naive
Aufbau computation.** Configurations are generated from Z by the
Madelung (n+l) rule, then 19 elements are corrected to their real
configurations:

    Cr Cu Nb Mo Ru Rh Pd Ag La Ce Gd Pt Au Ac Th Pa U Np Cm

Chromium really is `4s1 3d5`, copper `4s1 3d10`, and palladium is
`4d10` with a completely empty 5s. A program that "computed" these
would hand you the wrong answer for exactly the elements most likely to
be on an exam, so the detail screen also flags them with
`! breaks Aufbau`.

Lawrencium is *not* in that list. PubChem gives Lr as
`[Rn] 5f14 6d1 7s2`, which is what plain Aufbau already produces, so it
needs no correction. Some texts print the 2015 measured
`[Rn] 5f14 7s2 7p1` instead — if your course uses that, add it to
`EXCEPTIONS` in `CHEMCORE.py`.

Configurations are written in **filling order** (`4s` before `3d`),
which is the order the course asks you to write them in.

Valence counts key on the period rather than on the largest occupied
shell. That is what keeps palladium at 10 instead of 18.

Atomic masses are the IUPAC conventional values from a standard
gen-chem table.

**Lewis structures** come from a solver that tries every bond
arrangement and keeps the one with the smallest largest formal charge,
then the most zeros, then any negative charge on the more electronegative
atom. It reproduces the notes' worked examples (O=C=O; ClO4- with Cl at 0
and 4 resonance forms; formate with 2). The earlier version drew CO2 as
O#C-O and left ClO4- at Cl +3. SO2 now comes out O=S=O, which follows
the course method but differs from the octet-only form some texts use.

**Bond polarity** uses Tro's one-decimal Pauling values (the ones in the
notes), stored as integer tenths so C-H is exactly 0.4, not 0.39999.
`LEWIS_EN` holds revised values and is used only to rank atoms.

**Rydberg** uses `Rb = 1.097e-2 nm^-1`, so wavelengths come out in
nanometres directly, matching the course formula sheet. Answers are
rounded to **four significant figures** — the constant only carries
four, so reporting `656.3355 nm` would claim precision the input never
had.

## How this was verified

`CHEMCORE.py` is plain Python with no calculator imports, so it can be
exercised directly:

```python
from CHEMCORE import *
config_string(electron_configuration(24))   # 1s2 2s2 2p6 3s2 3p6 4s1 3d5
from LEWCORE import *
build_lewis([("C", 1), ("O", 2)])["bonds"]  # [2, 2]: O=C=O
```

Before release it was checked against a desktop harness (the current replacement is included in `../tests/`) that confirmed:

- every configuration sums to Z, and no subshell exceeds its capacity
- the 19 exceptions match PubChem field by field
- valence equals the group number across the whole main group and
  d block — the case that catches palladium
- Hund's rule for every s/p/d/f occupancy, with the animation's fill
  order replaying to the same result
- the Rydberg solvers against the known hydrogen lines: H-α 656.3 nm,
  H-β 486.1 nm, Lyman-α 121.5 nm, Paschen 1876 nm, plus round trips
  through energy and kJ/mol

The three programs were also driven under stand-in `ti_draw` /
`ti_system` modules — importing a program *is* running it, exactly as
on the calculator — validating that colours stay in range, nothing is
drawn off the 320×210 screen, no text is wider than the display, and
no text is painted over before it is ever shown.

## What is verified, and what is not

Grounded in TI's documentation, the community Evo reference, and a
working Evo program:

- Screen is 320×210, origin top-left, `get_screen_dim()` → `[319, 209]`
- `draw_text` is a fixed 10 px per character; `y` is the baseline
- `set_color(r, g, b)` takes three ints, `set_pen` takes two strings
- Evo key codes: left 24, up 25, right 26, down 34, `2nd` 21,
  `clear` 45, `enter` 105
- `from PROGRAM import *` is TI's cross-program import, and importing
  **runs** the program — which is why `CHEMCORE.py` defines names and
  nothing else

Two things are deliberately defensive:

- `use_buffer()` / `paint_buffer()` are not in TI's published function
  list but are used by a working Evo program, so they are probed with
  `hasattr` and fall back to unbuffered drawing.
- `input()` is the one call that could not be confirmed against the
  hardware docs. TI documents the CE as returning to the shell on
  `CLEAR`, while the Evo keeps a graphics screen up throughout, so
  mixing a shell prompt into a drawn screen is untested. `ORBITAL`
  offers typed entry because that is the natural way to enter `2p4`,
  but if the prompt is unavailable it falls through to the arrow
  picker. `RYDBERG` never calls `input()` at all.

The TI-84 Plus CE keypad map on education.ti.com does **not** apply to
the Evo — it gives `enter` as 13 and `clear` as 9, against the Evo's
105 and 45.
