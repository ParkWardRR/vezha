"""Enclosure A -- upper router box. Headless v1.

SKELETON. This builds and exports, and the envelope tracks params.py, but it
is not a design. What it deliberately does encode, because the docs are blunt
about them, are the constraints that make this box hard:

  1. Clearance on BOTH faces of the Orange Pi. One radio sits above the board,
     one hangs below on an adapter, so standoff height is set by the underside
     stack -- "now the only thing setting this box's thickness" (01, open
     questions). It is modelled here as a keep-out volume, not a number buried
     in a sketch.
  2. Antennas live inside the NARROW walls; the broad faces stay clear.
  3. One USB-C opening, sized off the mated plug and its bend radius -- not
     the receptacle footprint.

Nothing here is ready to print. Every TBD in `python params.py` is a thing
that can still move this geometry.
"""

from __future__ import annotations

from build123d import Box, Pos

import lib
from params import A, COMMON

CORNER_R = 3.0


def underside_keepout():
    """The adapter + card + mated plugs + coax bend, as a solid.

    Modelled so a future fit check is a boolean, not an argument. It hangs
    below the SBC plane, which is why the board cannot sit on the floor.
    """
    return Pos(0, 0, float(A.standoff_h) / 2) * Box(
        float(A.ax210_x) + 2 * float(A.coax_bend_r),
        float(A.ax210_y) + 2 * float(A.coax_bend_r),
        float(A.standoff_h),
    )


def sbc_keepout():
    """Orange Pi board plus the top-side radio and heatsink headroom."""
    z0 = float(A.standoff_h)
    board = Pos(0, 0, z0 + float(A.sbc_pcb_t) / 2) * Box(
        float(A.sbc_x), float(A.sbc_y), float(A.sbc_pcb_t)
    )
    above = Pos(0, 0, z0 + float(A.sbc_pcb_t) + float(A.headroom) / 2) * Box(
        float(A.sbc_x), float(A.sbc_y), float(A.headroom)
    )
    return board + above


def antenna_pads():
    """Four flex strips flat against the narrow walls.

    04-antennas.md: top edge, upper-right sidewall, lower-left sidewall,
    bottom edge. Broad faces stay clear. Returned as keep-out solids so they
    can be differenced against anything that tries to occupy a wall.
    """
    t, w, ln = float(A.ant_t), float(A.ant_w), float(A.ant_len)
    z = float(A.interior_z) / 2
    ix, iy = float(A.interior_x) / 2, float(A.interior_y) / 2

    strips = [
        Pos(0, iy - t / 2, z) * Box(ln, t, w),          # top edge
        Pos(0, -iy + t / 2, z) * Box(ln, t, w),          # bottom edge
        Pos(ix - t / 2, iy / 2, z) * Box(t, ln, w),      # upper-right sidewall
        Pos(-ix + t / 2, -iy / 2, z) * Box(t, ln, w),    # lower-left sidewall
    ]
    out = strips[0]
    for s in strips[1:]:
        out = out + s
    return out


def usbc_inlet():
    """Single 5 V inlet. Position is provisional; the cable must reach the
    Orange Pi's power input without a tight bend (02, Power entry)."""
    return lib.wall_cutout(
        width=float(COMMON.usbc_recept_w) + 1.0,
        height=float(COMMON.usbc_recept_h) + 1.0,
        thickness=float(COMMON.wall),
        x=float(A.interior_x) / 4,
        y=-float(A.interior_y) / 2,
        z=float(COMMON.usbc_recept_h),
        axis="y",
    )


def build():
    """Three printed parts, per the service-access decision in params.A.

    The band carries all four antenna zones and is never opened. The base
    plate carries the SBC, so pulling it takes the board and the whole
    underside M.2 stack out together. The top cap is the antenna hedge.
    """
    assert A.SERVICE_ACCESS == "band-with-two-plates", A.SERVICE_ACCESS

    shell = lib.band(A.outer_x, A.outer_y, A.interior_z, COMMON.wall,
                     corner_r=CORNER_R)
    shell = shell - usbc_inlet()

    # Standoffs rise from the BASE PLATE, not from the band. This is the whole
    # point of the decision: the board leaves with the plate.
    base = lib.plate(A.outer_x, A.outer_y, A.plate_t, COMMON.wall,
                     corner_r=CORNER_R)
    base = base + Pos(0, 0, float(A.plate_t)) * lib.standoff_grid(
        A.standoff_h, COMMON.standoff_od, COMMON.standoff_id,
        float(A.sbc_x) - 2 * float(A.sbc_hole_inset),
        float(A.sbc_y) - 2 * float(A.sbc_hole_inset),
    )

    cap = lib.plate(A.outer_x, A.outer_y, A.cap_t, COMMON.wall,
                    corner_r=CORNER_R)

    return {
        "enclosure-a-band": shell,
        "enclosure-a-base-plate": base,
        "enclosure-a-top-cap": cap,
        "enclosure-a-keepout-underside": underside_keepout(),
        "enclosure-a-keepout-sbc": sbc_keepout(),
        "enclosure-a-keepout-antennas": antenna_pads(),
    }


if __name__ == "__main__":
    print(lib.summarise({n: lib.emit(p, n) for n, p in build().items()}))
