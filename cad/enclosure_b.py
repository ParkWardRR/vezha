"""Enclosure B -- lower power box. Detachable.

SKELETON. Holds the power board and nothing else of consequence.

The one thing worth getting right here from day one is where the board
outline comes from. 03 says the RotoPD Pro's "outline, height, and mounting
pattern [are] all unverified" and that it is the part least knowable from a
datasheet. So the moment the power board exists in KiCad:

    kicad-cli pcb export step --subst-models --force \
        -o cad/build/power-board.step path/to/power-board.kicad_pcb

and this module imports that solid instead of the placeholder block. The
board outline is then never retyped, which is the whole reason for choosing
an OCCT-based CAD kernel over OpenSCAD.
"""

from __future__ import annotations

from pathlib import Path

from build123d import Box, Pos, import_step

import lib
from params import B, COMMON

CORNER_R = 3.0

#: Written by `kicad-cli pcb export step`. Absent until the board is drawn.
PCB_STEP = lib.BUILD / "power-board.step"


def power_board():
    """The real board if KiCad has exported it, else a flagged placeholder."""
    if PCB_STEP.exists():
        return import_step(str(PCB_STEP)), True
    block = Pos(0, 0, float(B.standoff_h) + float(B.pcb_t) / 2) * Box(
        float(B.pcb_x), float(B.pcb_y), float(B.pcb_t)
    )
    return block, False


def component_keepouts():
    """Tallest parts, as keep-out solids above the board plane.

    The Pico entry depends on B.PICO_MOUNT -- 03 is explicit that castellated
    vs. socketed "changes the height", so it is a switch, not a constant.
    """
    z0 = float(B.standoff_h) + float(B.pcb_t)

    def at(x, y, w, d, h):
        return Pos(x, y, z0 + h / 2) * Box(w, d, h)

    # 06 U1: the switched VBUS screw terminal sits on the edge opposite the
    # USB-C jack and is part of this module's height until someone decides to
    # remove it and solder to the pads instead.
    rotopd = at(-float(B.pcb_x) / 4, 0,
                float(B.rotopd_x), float(B.rotopd_y),
                float(B.rotopd_h) + float(B.rotopd_screw_terminal_h))
    # 06 U3: only 6.1 mm of the Pololu's 9.07 mm stack is above the board.
    # The other 1.4 mm hangs below and is charged to standoff height instead.
    pololu = at(float(B.pcb_x) / 4, float(B.pcb_y) / 4,
                float(B.pololu_x), float(B.pololu_y), float(B.pololu_above))
    pico = at(float(B.pcb_x) / 4, -float(B.pcb_y) / 4,
              float(B.pico_x), float(B.pico_y),
              float(B.pico_stack) + float(B.pico_t))
    return rotopd + pololu + pico


def panel_keepouts():
    """OLED + push encoder, if this box has a panel at all.

    01 says it carries the only hardware UI in v1; 06 still lists "whether
    Enclosure B has a front panel at all" as open. B.HAS_PANEL is the switch
    until that is settled -- it changes box height and lid openings both.
    """
    if not B.HAS_PANEL:
        return None
    z0 = float(B.standoff_h) + float(B.pcb_t)
    oled = Pos(-float(B.pcb_x) / 4, -float(B.pcb_y) / 4,
               z0 + float(B.oled_board_h) / 2) * Box(
        float(B.oled_x), float(B.oled_y), float(B.oled_board_h))
    enc = Pos(0, -float(B.pcb_y) / 3, z0 + float(B.encoder_h) / 2) * Box(
        12.0, 12.0, float(B.encoder_h))
    return oled + enc


def usbc_openings():
    """Three USB-C ports pass through this shell (01 + 03):
      * PD input from the external charger
      * 5 V seam output to Enclosure A
      * accessory 5 V out
    Positions are provisional. Size them off mated plugs, not receptacles.
    """
    w = float(COMMON.usbc_recept_w) + 1.0
    h = float(COMMON.usbc_recept_h) + 1.0
    t = float(COMMON.wall)
    z = h
    cuts = [
        lib.wall_cutout(w, h, t, x=-float(B.interior_x) / 2, y=0, z=z, axis="x"),
        lib.wall_cutout(w, h, t, x=float(B.interior_x) / 2, y=float(B.interior_y) / 5, z=z, axis="x"),
        lib.wall_cutout(w, h, t, x=float(B.interior_x) / 2, y=-float(B.interior_y) / 5, z=z, axis="x"),
    ]
    out = cuts[0]
    for c in cuts[1:]:
        out = out + c
    return out


def build():
    body = lib.tray(B.outer_x, B.outer_y, B.outer_z, COMMON.wall, corner_r=CORNER_R)
    body = body - usbc_openings()
    body = body + lib.standoff_grid(
        B.standoff_h, COMMON.standoff_od, COMMON.standoff_id,
        float(B.pcb_x) - 8.0, float(B.pcb_y) - 8.0,
    )
    cover = lib.lid(B.outer_x, B.outer_y, COMMON.wall, corner_r=CORNER_R)

    board, is_real = power_board()
    parts = {
        "enclosure-b-tray": body,
        "enclosure-b-lid": cover,
        "enclosure-b-keepout-components": component_keepouts(),
        "enclosure-b-power-board": board,
    }
    if is_real:
        bb = board.bounding_box()
        bx, by, bz = bb.size.X, bb.size.Y, bb.size.Z
        ix, iy, iz = float(B.interior_x), float(B.interior_y), float(B.interior_z)
        print(f"  board fit: {bx:.1f} x {by:.1f} x {bz:.1f} mm "
              f"in {ix:.1f} x {iy:.1f} x {iz:.1f} mm interior")
        for axis, got, have in (("X", bx, ix), ("Y", by, iy), ("Z", bz, iz)):
            if got > have:
                print(f"     !! board exceeds interior in {axis} by {got - have:.1f} mm")
            else:
                print(f"     {axis} clearance {have - got:.1f} mm")
        print("     NOTE: this STEP contains the HEADERS for U1 and U3, not the\n"
              "     RotoPD and Pololu module bodies that sit on them. Their\n"
              "     heights are carried by component_keepouts() instead.")

    panel = panel_keepouts()
    if panel is not None:
        parts["enclosure-b-keepout-panel"] = panel
    else:
        print("  note: B.HAS_PANEL is False -- no OLED/encoder keep-out emitted.")
    if not is_real:
        print(f"  note: {PCB_STEP.name} not found -- using a placeholder board block.")
        print("        Draw the power board in KiCad, then `kicad-cli pcb export step`.")
    return parts


if __name__ == "__main__":
    print(lib.summarise({n: lib.emit(p, n) for n, p in build().items()}))
