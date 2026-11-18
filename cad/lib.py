"""Shared build123d helpers and the export/render pipeline.

Geometry convention for both enclosures:
  * origin at the centre of the tray's inner floor
  * +Z up, +X long axis, +Y short axis
  * the tray is open-topped; the lid is a separate solid

That matters because the power board's real outline arrives as a STEP file
from `kicad-cli pcb export step`, and it has to land in a known frame.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from build123d import (
    Align,
    Axis,
    Box,
    Cylinder,
    Pos,
    export_step,
    export_stl,
    fillet,
)

BUILD = Path(__file__).parent / "build"

# Align a solid so its local origin sits at its bottom face centre.
BOTTOM = (Align.CENTER, Align.CENTER, Align.MIN)


def tray(outer_x, outer_y, outer_z, wall, corner_r=0.0):
    """Open-topped box. Floor sits at z=-wall, inner floor at z=0."""
    ox, oy, oz, w = map(float, (outer_x, outer_y, outer_z, wall))

    body = Box(ox, oy, oz, align=BOTTOM)
    if corner_r:
        body = fillet(body.edges().filter_by(Axis.Z), float(corner_r))

    cavity = Box(ox - 2 * w, oy - 2 * w, oz, align=BOTTOM)
    part = body - Pos(0, 0, w) * cavity
    # Drop so the inner floor is the z=0 plane.
    return Pos(0, 0, -w) * part


def lid(outer_x, outer_y, wall, lip_depth=3.0, lip_clearance=0.3, corner_r=0.0):
    """Flat cap with a downward lip that slips inside the tray walls."""
    ox, oy, w = map(float, (outer_x, outer_y, wall))
    ld, lc = float(lip_depth), float(lip_clearance)

    plate = Box(ox, oy, w, align=BOTTOM)
    if corner_r:
        plate = fillet(plate.edges().filter_by(Axis.Z), float(corner_r))

    lip_outer = Box(ox - 2 * w - 2 * lc, oy - 2 * w - 2 * lc, ld, align=BOTTOM)
    lip_inner = Box(ox - 4 * w - 2 * lc, oy - 4 * w - 2 * lc, ld, align=BOTTOM)
    return plate + Pos(0, 0, -ld) * (lip_outer - lip_inner)


def standoff(height, outer_d, pilot_d):
    """Screw boss rising from the inner floor (z=0)."""
    h, od, pid = float(height), float(outer_d), float(pilot_d)
    return Cylinder(od / 2, h, align=BOTTOM) - Cylinder(pid / 2, h, align=BOTTOM)


def standoff_grid(height, outer_d, pilot_d, span_x, span_y):
    """Four bosses on a rectangular pattern, centred on the origin."""
    one = standoff(height, outer_d, pilot_d)
    sx, sy = float(span_x) / 2, float(span_y) / 2
    out = None
    for x in (-sx, sx):
        for y in (-sy, sy):
            part = Pos(x, y, 0) * one
            out = part if out is None else out + part
    return out


def wall_cutout(width, height, thickness, x=0.0, y=0.0, z=0.0, axis="y"):
    """A rectangular hole to subtract from a wall.

    axis="y" cuts through a wall whose normal is Y (the long sidewalls);
    axis="x" cuts through a wall whose normal is X (the short end walls).
    """
    w, h, t = float(width), float(height), float(thickness) * 3
    box = Box(w, t, h) if axis == "y" else Box(t, w, h)
    return Pos(float(x), float(y), float(z)) * box


# -----------------------------------------------------------------------
# Export
# -----------------------------------------------------------------------
def emit(part, name: str, render: bool = True) -> dict[str, Path]:
    """Write STEP + STL, and a headless PNG if f3d is on PATH."""
    BUILD.mkdir(parents=True, exist_ok=True)
    out = {}

    step = BUILD / f"{name}.step"
    export_step(part, str(step))
    out["step"] = step

    stl = BUILD / f"{name}.stl"
    export_stl(part, str(stl))
    out["stl"] = stl

    if render and shutil.which("f3d"):
        png = BUILD / f"{name}.png"
        try:
            subprocess.run(
                ["f3d", str(stl), "--output", str(png),
                 "--resolution", "1200,900", "--camera-direction", "-0.6,-0.6,-1",
                 "--up", "+Z", "--grid", "--no-background"],
                check=True, capture_output=True, timeout=120,
            )
            out["png"] = png
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            pass  # a missing preview is not a build failure

    return out


def summarise(results: dict[str, dict[str, Path]]) -> str:
    lines = []
    for name, files in results.items():
        bits = "  ".join(f"{k}:{v.name}" for k, v in files.items())
        lines.append(f"  {name:<22} {bits}")
    return "\n".join(lines)
