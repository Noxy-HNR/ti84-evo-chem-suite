# LEWCORE.py -- the Lewis-structure solver, shared by LEWIS and BONDING.
#
# One central atom with outer atoms, the CHEM 1450 method. Every bond
# arrangement is tried and ranked the way the course checks structures.
# Pure Python; importing it only defines names.

LEWIS_VALENCE = {
    "H": 1, "B": 3, "C": 4, "N": 5, "O": 6, "F": 7,
    "Si": 4, "P": 5, "S": 6, "Cl": 7, "Br": 7, "I": 7,
    "Xe": 8,
}
LEWIS_EN = {
    "H": 2.20, "B": 2.04, "C": 2.55, "N": 3.04, "O": 3.44,
    "F": 3.98, "Si": 1.90, "P": 2.19, "S": 2.58, "Cl": 3.16,
    "Br": 2.96, "I": 2.66, "Xe": 2.60,
}
LEWIS_EXPANDED = ("P", "S", "Cl", "Br", "I", "Xe")

# Row of the table for each atom LEWIS knows -- all BONDING needs to
# name an orbital (2p, 3p...), without loading the whole periodic table.
PERIOD = {"H": 1, "B": 2, "C": 2, "N": 2, "O": 2, "F": 2, "Si": 3, "P": 3,
          "S": 3, "Cl": 3, "Br": 4, "I": 5, "Xe": 5}


def _lewis_charge(atom, lone_e, bond_order):
    return LEWIS_VALENCE[atom] - lone_e - bond_order


def _en_rank(atom):
    # LEWIS_EN in hundredths, as an int.
    #
    # Summing floats over equivalent resonance forms in a different order
    # can land a hair apart and split a genuine tie, so the scoring below
    # works in exact integers.
    return int(round(LEWIS_EN[atom] * 100))


def _lewis_score(atoms_all, fcs):
    # Rank a candidate structure; lower is better.
    #
    # In the order the course checks them (9/18, 9/23 notes):
    #   1. largest |formal charge| -- a +2 or +3 is "the giveaway that
    #      more work is needed", so it outranks everything else
    #   2. total |formal charge| -- as many atoms at zero as possible
    #   3. sum of FC x EN -- any negative charge belongs on the more
    #      electronegative atom, which is what picks 3 double bonds over
    #      4 for ClO4- (Cl at 0, -1 on an oxygen, not -1 on chlorine)
    worst = 0
    total = 0
    placed = 0
    for i in range(len(fcs)):
        q = fcs[i]
        if abs(q) > worst:
            worst = abs(q)
        total += abs(q)
        placed += q * _en_rank(atoms_all[i])
    return (worst, total, placed)


def build_lewis(atoms, charge=0):
    # Build the best central-atom Lewis structure.
    #
    # atoms is [(symbol, count), ...]. This models one central atom with
    # terminal ligands, the structures used in the CHEM 1450 method.
    # Returns a dict containing the structure, resonance alternatives,
    # charges, and worksheet-style steps. Raises ValueError if unsupported.
    #
    # Every bond-order assignment is tried (1 to 3 per outer atom, H fixed
    # at 1 -- at most 3**6 = 729) and scored by _lewis_score. The earlier
    # greedy version committed to the first tied choice and kept piling
    # bonds onto one atom, which drew CO2 as O#C-O instead of O=C=O, and
    # it never moved past four single bonds on an expanded-octet center,
    # which left ClO4- at Cl +3 -- the structure the 9/23 notes reject.
    flat = []
    for atom, count in atoms:
        if atom not in LEWIS_VALENCE:
            raise ValueError("No Lewis data for " + str(atom) + ".")
        for unused in range(int(count)):
            flat.append(atom)
    if len(flat) < 2 or len(flat) > 7:
        raise ValueError("Use 2 to 7 total atoms in this builder.")
    candidates = [a for a in set(flat) if a != "H"]
    if not candidates:
        raise ValueError("Hydrogen cannot be the central atom.")
    center = min(candidates, key=lambda a: LEWIS_EN[a])
    ligands = list(flat)
    ligands.remove(center)
    if len(ligands) > 6:
        raise ValueError("This screen supports up to 6 outer atoms.")

    electrons = sum(LEWIS_VALENCE[a] for a in flat) - int(charge)
    if electrons % 2:
        raise ValueError("Odd electron count: a radical, not built here.")

    # Shell the center may end with. Boron is happy at 6 (BH3, 9/16);
    # period 3+ centers may expand (7 bonds = 14 e- on Cl in ClO4-);
    # period 2 centers never pass 8. Scoring stops runaway bonding.
    if center == "B":
        low, high = 6, 8
    elif center in LEWIS_EXPANDED:
        low, high = 8, 16
    else:
        low, high = 8, 8

    k = len(ligands)
    atoms_all = [center] + ligands
    free = [i for i in range(k) if ligands[i] != "H"]
    orders = [1] * k
    best = None
    forms = []
    while True:
        lone = [0 if a == "H" else 8 - 2 * orders[i]
                for i, a in enumerate(ligands)]
        bond_sum = sum(orders)
        c_lone = electrons - 2 * bond_sum - sum(lone)
        shell = 2 * bond_sum + c_lone
        if c_lone >= 0 and not c_lone % 2 and low <= shell <= high:
            fcs = [_lewis_charge(center, c_lone, bond_sum)]
            for i in range(k):
                fcs.append(_lewis_charge(ligands[i], lone[i], orders[i]))
            score = _lewis_score(atoms_all, fcs)
            if best is None or score < best:
                best = score
                forms = [list(orders)]
            elif score == best:
                forms.append(list(orders))
        # odometer over the non-hydrogen positions, orders 1..3
        j = 0
        while j < len(free):
            p = free[j]
            if orders[p] < 3:
                orders[p] += 1
                break
            orders[p] = 1
            j += 1
        if j == len(free):
            break

    if not forms:
        raise ValueError("Electron count cannot make a valid Lewis structure.")

    # Keep the tied forms that share the first one's bond total, so the
    # central lone pairs -- and so the drawn geometry -- stay fixed as
    # LEWIS cycles through them.
    resonance = [f for f in forms if sum(f) == sum(forms[0])]
    bonds = list(resonance[0])
    terminal_lone = [0 if a == "H" else 8 - 2 * bonds[i]
                     for i, a in enumerate(ligands)]
    central_lone = electrons - 2 * sum(bonds) - sum(terminal_lone)
    central_charge = _lewis_charge(center, central_lone, sum(bonds))
    charges = [_lewis_charge(ligands[i], terminal_lone[i], bonds[i])
               for i in range(k)]
    central_shell = 2 * sum(bonds) + central_lone

    # worksheet steps, stage by stage as the notes teach them
    single_lone = sum(0 if a == "H" else 6 for a in ligands)
    single_center = electrons - 2 * k - single_lone
    multiple = sum(1 for b in bonds if b > 1)
    steps = [
        "1. Valence e- = " + str(electrons) + " (charge included).",
        "2. Central atom " + center + ": least EN, never H.",
        "3. " + str(k) + " single bonds use " + str(2 * k) + " e-.",
        "4. Outer octets/duets: " + str(single_lone) + " e- as dots.",
        "5. Left for center: " + str(single_center) + " e-.",
    ]
    if multiple:
        steps.append("6. Lone pairs -> bonds: " + str(multiple)
                     + " multiple bond(s)")
        steps.append("   to fill octets and lower FC.")
    else:
        steps.append("6. No multiple bonds needed.")
    steps.append("   Center shell = " + str(central_shell) + " e-.")
    steps.append("7. FC sum = " + str(central_charge + sum(charges))
                 + " (matches charge).")
    return {
        "center": center, "ligands": ligands, "bonds": bonds,
        "terminal_lone": terminal_lone, "central_lone": central_lone,
        "central_charge": central_charge, "charges": charges,
        "electrons": electrons, "steps": steps, "resonance": resonance,
        "regions": len(ligands) + central_lone // 2,
        "lone_pairs": central_lone // 2,
    }
