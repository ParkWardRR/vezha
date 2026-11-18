"""Vezha power board — mechanical placement study.

    cad/.venv/bin/python pcb/layout.py

Writes `pcb/build/vezha-power.kicad_pcb`, then exports
`cad/build/power-board.step`, which enclosure_b.py picks up automatically in
place of its placeholder block.

WHAT THIS IS, PRECISELY
-----------------------
A **placement study**, not a finished board. It has a real outline, real
footprints from the KiCad libraries, and real 3D bodies, so the enclosure can
be checked against the actual parts instead of a guessed rectangle.

It has **no routing and no copper**. Do not send it anywhere.

The electrical truth lives in `power_board.py`, which generates a verified
netlist from 06. Joining the two — importing that netlist onto this board so
it can be routed and DRC'd — is the next step and needs KiCad's own tools,
because `kicad-cli` has no netlist-import command.

PLACEMENT RATIONALE
-------------------
Driven by the enclosure, which is the point of doing it this way:

  * **U1 (RotoPD) at one short edge** — its own USB-C jack is the PD inlet, so
    it must sit against the wall it comes through.
  * **J2 (seam out) at the opposite edge** — 01: the seam carries 5 V only and
    the power box detaches, so input and output face opposite walls.
  * **U3 (Pololu) adjacent to U1** — VBUS_PD is the full router current and
    the shortest heavy path is the one that wastes least in IR drop, which
    SIM-04 shows is already the binding constraint.
  * **U2 (Pico) along a long edge** — 03: "leave room for the overhanging
    Micro-USB port" if programming access in situ is wanted.
  * **R13 (2 mohm shunt) directly between U3 VOUT and J2** — it is in series
    with the whole rail; every millimetre of trace around it adds to the
    25 mohm loop budget.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from kiutils.board import Board
from kiutils.footprint import Footprint
from kiutils.items.common import Net, Position
from kiutils.items.gritems import GrLine

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "cad"))
from params import B  # noqa: E402

import power_board as pb  # noqa: E402

FP_ROOT = Path("/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints")
BUILD = Path(__file__).parent / "build"
CAD_BUILD = Path(__file__).resolve().parent.parent / "cad" / "build"

BOARD_X = float(B.pcb_x)
BOARD_Y = float(B.pcb_y)

#: (ref, "Lib:Footprint", x, y, rotation). Origin is the board's top-left in
#: KiCad's y-down page coordinates; values are mm from that corner.
PLACEMENT = [
    # ================= accessory port chain, top strip ==================
    # VBUS_PD enters at the x-small wall and the port exits at x-large, so
    # the chain runs left to right and the heavy input caps sit on U4's pin.
    ("C4",  pb.FP_C1210, 28.0, 8.0, 0.0),
    ("C5",  pb.FP_C1210, 28.0, 13.0, 0.0),
    ("C6",  pb.FP_C0603, 28.0, 17.0, 0.0),
    ("U4",  pb.FP_SOIC8_EP, 35.0, 12.0, 0.0),     # LMR38020, 80 V buck
    ("C9",  pb.FP_C0603, 35.0, 6.0, 0.0),         # BOOT cap, close to the pin
    ("R17", pb.FP_R0603, 35.0, 18.0, 0.0),        # RT
    ("R20", pb.FP_R0603, 30.0, 20.0, 0.0),        # U4 PG pull-up
    ("L1",  pb.FP_IND,   45.0, 12.0, 0.0),        # 22 uH
    ("C7",  pb.FP_C1210, 53.0, 9.0, 0.0),
    ("C8",  pb.FP_C0603, 53.0, 14.0, 0.0),
    ("R18", pb.FP_R0603, 48.0, 19.0, 0.0),        # FB top
    ("R19", pb.FP_R0603, 52.0, 19.0, 0.0),        # FB bottom
    ("U5",  pb.FP_SOT23_6, 61.0, 12.0, 0.0),      # TPS2553 limiter
    ("R5",  pb.FP_R0603, 61.0, 17.0, 0.0),        # R_ILIM, Config A
    ("R6",  pb.FP_R0603, 65.0, 17.0, 0.0),        # FAULT pull-up
    ("R3",  pb.FP_R0603, 70.0, 6.0, 0.0),         # CC1 Rp
    ("R4",  pb.FP_R0603, 70.0, 9.0, 0.0),         # CC2 Rp
    ("R21", pb.FP_R0603, 70.0, 12.0, 0.0),        # D+/D- BC1.2 short
    ("J6",  pb.FP_USBC_16P, 82.0, 12.0, 0.0),     # accessory out, x-large wall

    # ================= PD inlet edge (x small) ==========================
    ("U1",  pb.FP_HDR_1X8,  6.0, 24.0, 0.0),
    ("U1P", pb.FP_HDR.format(n=2), 6.0, 48.0, 0.0),
    ("J1",  pb.FP_JST_SH4,  12.0, 10.0, 0.0),
    ("JP1", pb.FP_R0603,    12.0, 46.0, 0.0),

    # ================= router rail ======================================
    ("U3",  pb.FP_HDR_2X6,  20.0, 26.0, 0.0),     # Pololu carrier
    ("R1",  pb.FP_R0603,    27.0, 26.0, 0.0),
    ("R2",  pb.FP_R0603,    27.0, 29.0, 0.0),
    ("R16", pb.FP_R0603,    27.0, 32.0, 0.0),
    ("RT1", pb.FP_R0603,    27.0, 35.0, 0.0),
    ("D1",  pb.FP_SMA,      14.0, 52.0, 0.0),
    ("R13", pb.FP_R2512,    44.0, 30.0, 0.0),     # 2 mohm shunt in the rail
    ("U6",  pb.FP_VSSOP10,  45.0, 36.0, 0.0),
    ("J2",  pb.FP_USBC_6P,  83.0, 36.0, 0.0),     # seam out, x-large wall

    # ================= console row ======================================
    ("J3",  pb.FP_HDR.format(n=3), 34.0, 24.0, 0.0),
    ("R14", pb.FP_R0603,    38.0, 24.0, 0.0),
    ("R15", pb.FP_R0603,    38.0, 27.0, 0.0),
    ("R7",  pb.FP_R0603,    50.0, 24.0, 0.0),
    ("R8",  pb.FP_R0603,    50.0, 27.0, 0.0),
    ("R9",  pb.FP_R0603,    50.0, 30.0, 0.0),
    ("R10", pb.FP_R0603,    54.0, 24.0, 0.0),
    ("R11", pb.FP_R0603,    54.0, 27.0, 0.0),
    ("R12", pb.FP_R0603,    54.0, 30.0, 0.0),
    ("C1",  pb.FP_C0603,    58.0, 24.0, 0.0),
    ("C2",  pb.FP_C0603,    58.0, 27.0, 0.0),
    ("C3",  pb.FP_C0603,    58.0, 30.0, 0.0),
    ("J5",  pb.FP_HDR.format(n=4), 64.0, 24.0, 0.0),
    ("J4",  pb.FP_JST_SH4,  72.0, 26.0, 0.0),

    # ================= controller =======================================
    ("U2",  pb.PICO_FP,     30.0, 64.0, 90.0),
    ("J7",  pb.FP_HDR.format(n=3), 22.0, 52.0, 0.0),
]


def footprint_extent(fp: Footprint, x: float, y: float, rot: float):
    """World-space (x0, y0, x1, y1) of a placed footprint, from its pads.

    Worth doing rather than eyeballing: KiCad footprint origins are not all
    at the part centre. RaspberryPi_Pico_Common_THT puts its origin at pin 1,
    so a "centre" placement hangs 40 mm off the board -- which is exactly the
    error this function was written to catch.
    """
    import math

    pts = []
    for pad in fp.pads:
        px, py = pad.position.X, pad.position.Y
        sx = (pad.size.X or 0) / 2
        sy = (pad.size.Y or 0) / 2
        for dx, dy in ((-sx, -sy), (sx, -sy), (sx, sy), (-sx, sy)):
            pts.append((px + dx, py + dy))
    if not pts:
        return None

    # KiCad's footprint rotation is the OPPOSITE sign to the standard
    # math-convention rotation, because its Y axis points down. Getting this
    # wrong is silent: the checker passes and the exported board has a part
    # hanging 47 mm off the edge. Verified against a re-imported STEP.
    a = math.radians(-rot)
    ca, sa = math.cos(a), math.sin(a)
    world = [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in pts]
    xs = [p[0] for p in world]
    ys = [p[1] for p in world]
    return min(xs), min(ys), max(xs), max(ys)


def check_placement(extents: dict[str, tuple], edge_margin: float = 1.0,
                    gap: float = 0.3) -> list[str]:
    """Footprints must sit inside the outline and not overlap each other."""
    problems = []
    for ref, (x0, y0, x1, y1) in sorted(extents.items()):
        if (x0 < edge_margin or y0 < edge_margin
                or x1 > BOARD_X - edge_margin or y1 > BOARD_Y - edge_margin):
            problems.append(
                f"{ref} outside the {BOARD_X:.0f}x{BOARD_Y:.0f} outline: "
                f"x {x0:.1f}..{x1:.1f}, y {y0:.1f}..{y1:.1f}"
            )

    refs = sorted(extents)
    for i, a in enumerate(refs):
        ax0, ay0, ax1, ay1 = extents[a]
        for b in refs[i + 1:]:
            bx0, by0, bx1, by1 = extents[b]
            ox = min(ax1, bx1) - max(ax0, bx0)
            oy = min(ay1, by1) - max(ay0, by0)
            if ox > -gap and oy > -gap:
                problems.append(
                    f"{a} overlaps {b} by {max(ox, 0):.1f} x {max(oy, 0):.1f} mm"
                )
    return problems


def load_footprint(spec: str) -> Footprint:
    lib, name = spec.split(":", 1)
    path = FP_ROOT / f"{lib}.pretty" / f"{name}.kicad_mod"
    if not path.exists():
        raise FileNotFoundError(f"footprint not found: {spec} -> {path}")
    return Footprint.from_file(str(path))


def parse_netlist(net_file: Path) -> dict[tuple[str, str], str]:
    """(ref, pin) -> net name, read from the generated KiCad netlist."""
    import re

    mapping: dict[tuple[str, str], str] = {}
    for block in net_file.read_text().split("(net\n")[1:]:
        m = re.search(r'\(name "([^"]+)"\)', block)
        if not m:
            continue
        name = m.group(1)
        refs = re.findall(r'\(ref "([^"]+)"\)', block)
        pins = re.findall(r'\(pin "([^"]+)"\)', block)
        for ref, pin in zip(refs, pins):
            mapping[(ref, pin)] = name
    return mapping


def assign_nets(board: Board, netmap: dict[tuple[str, str], str]) -> tuple[int, int]:
    """Write net names onto every pad, so the board is routable and DRC real.

    Without this, pads sit on "<no net>" and KiCad reports clearance and
    solder-mask-bridge errors between pads that are electrically the same
    point -- J6's A1/B12 and A4/B9 are stacked by design on the HRO part.
    """
    names = sorted({n for n in netmap.values()})
    board.nets = [Net(number=0, name="")]
    numbers = {}
    for i, name in enumerate(names, start=1):
        board.nets.append(Net(number=i, name=name))
        numbers[name] = i

    hit = miss = 0
    for fp in board.footprints:
        ref = fp.properties.get("Reference", "")
        for pad in fp.pads:
            name = netmap.get((ref, str(pad.number)))
            if name is None:
                miss += 1
                continue
            pad.net = Net(number=numbers[name], name=name)
            hit += 1
    return hit, miss


def outline(board: Board) -> None:
    """Board edge on Edge.Cuts. Without this, STEP export produces nothing."""
    corners = [(0, 0), (BOARD_X, 0), (BOARD_X, BOARD_Y), (0, BOARD_Y), (0, 0)]
    for (x1, y1), (x2, y2) in zip(corners, corners[1:]):
        board.graphicItems.append(
            GrLine(start=Position(x1, y1), end=Position(x2, y2),
                   layer="Edge.Cuts", width=0.1)
        )


def build_board() -> Board:
    board = Board.create_new()
    outline(board)

    placed, missing, extents = [], [], {}
    for ref, spec, x, y, rot in PLACEMENT:
        try:
            fp = load_footprint(spec)
        except FileNotFoundError as e:
            missing.append(f"{ref}: {e}")
            continue
        ext = footprint_extent(fp, x, y, rot)
        if ext:
            extents[ref] = ext
        # KiCad 10 footprints carry graphic groups whose ids kiutils writes
        # back as `(id )`, which KiCad then refuses to parse. They only group
        # silkscreen items for editing convenience, so dropping them costs
        # nothing here and makes the file loadable.
        fp.groups = []

        # 03 specifies the NON-WIRELESS Pico 2. RaspberryPi_Pico_Common_THT is
        # shared with the Pico W, so it carries the W's "Antenna Copper Keep
        # Out" zone. On a board with no radio that zone is not a real
        # constraint, and leaving it produces DRC violations against parts
        # that are perfectly legal here. The "USB Cable" zone goes with it.
        if ref == "U2" and getattr(fp, "zones", None):
            dropped = [getattr(z, "name", "?") for z in fp.zones]
            fp.zones = []
            print(f"  U2: dropped Pico-W-only zones {dropped} (non-wireless Pico 2)")
        fp.position = Position(x, y, rot)
        fp.layer = "F.Cu"
        # fp.properties is a DICT, not a list of objects. Iterating it yields
        # key strings, so the obvious loop silently sets nothing and every
        # footprint stays REF** -- which DRC reports but does not fail on.
        # The silkscreen text is "${REFERENCE}" and resolves from this.
        fp.properties["Reference"] = ref
        board.footprints.append(fp)
        placed.append(ref)

    if missing:
        raise RuntimeError("missing footprints:\n  " + "\n  ".join(missing))

    net_file = BUILD / "vezha-power.net"
    if net_file.exists():
        netmap = parse_netlist(net_file)
        hit, miss = assign_nets(board, netmap)
        print(f"  nets: {len(board.nets) - 1} nets, {hit} pads assigned, "
              f"{miss} pads left unconnected")

    return board, placed, extents


#: Minimal project file so DRC runs against real fab limits instead of
#: KiCad's generic defaults. Without it the INA226's 0.5 mm-pitch VSSOP-10
#: reports 8 clearance errors against its OWN pins: that package has 0.15 mm
#: pad gaps, under the 0.2 mm default. These numbers are JLCPCB's stated
#: minimums, which is where 06's BOM sources every part.
FAB_MIN_CLEARANCE = 0.127   # mm
FAB_MIN_TRACK = 0.127       # mm
FAB_MIN_VIA_DIA = 0.45      # mm
FAB_MIN_VIA_DRILL = 0.3     # mm


def write_project(pcb_path: Path) -> Path:
    import json

    proj = {
        "board": {"design_settings": {
            "rules": {
                "min_clearance": FAB_MIN_CLEARANCE,
                "min_track_width": FAB_MIN_TRACK,
                "min_via_diameter": FAB_MIN_VIA_DIA,
                "min_through_hole_diameter": FAB_MIN_VIA_DRILL,
            },
        }},
        "net_settings": {"classes": [{
            "name": "Default",
            "clearance": FAB_MIN_CLEARANCE,
            "track_width": 0.25,
            "via_diameter": FAB_MIN_VIA_DIA,
            "via_drill": FAB_MIN_VIA_DRILL,
        }]},
        "meta": {"filename": pcb_path.with_suffix(".kicad_pro").name, "version": 3},
    }
    out = pcb_path.with_suffix(".kicad_pro")
    out.write_text(json.dumps(proj, indent=2))
    return out


def main() -> int:
    BUILD.mkdir(parents=True, exist_ok=True)
    CAD_BUILD.mkdir(parents=True, exist_ok=True)

    board, placed, extents = build_board()
    pcb_path = BUILD / "vezha-power.kicad_pcb"
    board.to_file(str(pcb_path))
    proj_path = write_project(pcb_path)
    print(f"Board written: {pcb_path}")
    print(f"Project written: {proj_path}  (clearance {FAB_MIN_CLEARANCE} mm)")
    print(f"  outline {BOARD_X:.0f} x {BOARD_Y:.0f} mm, {len(placed)} footprints placed")

    issues = check_placement(extents)
    if issues:
        print(f"\n!! PLACEMENT: {len(issues)} problem(s)")
        for i in issues:
            print(f"   - {i}")
        print("\nNot exporting STEP from a board whose parts do not fit.")
        return 1
    print("  placement: all footprints inside the outline, no overlaps")

    # Cross-check against the netlist so the two halves cannot drift apart.
    net_file = BUILD / "vezha-power.net"
    if net_file.exists():
        import re
        refs = set(re.findall(r'\(ref "([^"]+)"\)', net_file.read_text()))
        refs = {r for r in refs if not r.startswith("N$")}
        unplaced = sorted(refs - set(placed))
        extra = sorted(set(placed) - refs)
        if unplaced:
            print(f"  !! in netlist but NOT placed: {unplaced}")
        if extra:
            print(f"  !! placed but not in netlist: {extra}")
        if not unplaced and not extra:
            print(f"  all {len(refs)} netlist components are placed")

    # --- DRC -------------------------------------------------------------
    # Silkscreen violations are reference text sitting over pads. On a board
    # with no routing and no silk cleanup they are expected and cosmetic, so
    # they are reported but do not fail the build. Anything else does.
    rpt = BUILD / "drc.rpt"
    d = subprocess.run(
        ["kicad-cli", "pcb", "drc", "-o", str(rpt), str(pcb_path)],
        capture_output=True, text=True, timeout=600,
    )
    if d.returncode != 0:
        print("DRC failed to run:\n" + (d.stderr or d.stdout)[-800:], file=sys.stderr)
        return 1
    import collections, re as _re
    kinds = collections.Counter(_re.findall(r"^\[([a-z_]+)\]", rpt.read_text(), _re.M))
    # Three classes. Silkscreen is reference text over pads -- a finishing
    # task. unconnected_items is every ratsnest line on an unrouted board,
    # which is what this is. Anything else is a real fault and fails.
    silk = {k: v for k, v in kinds.items() if k.startswith("silk")}
    unrouted = {k: v for k, v in kinds.items() if k == "unconnected_items"}
    hard = {k: v for k, v in kinds.items()
            if not k.startswith("silk") and k != "unconnected_items"}
    print(f"  DRC: {sum(silk.values())} silkscreen (cosmetic), "
          f"{sum(unrouted.values())} unrouted ratsnest (expected), "
          f"{sum(hard.values())} substantive")
    if hard:
        for k, v in sorted(hard.items(), key=lambda kv: -kv[1]):
            print(f"     !! {k}: {v}")
        return 1

    step = CAD_BUILD / "power-board.step"
    r = subprocess.run(
        ["kicad-cli", "pcb", "export", "step", "--force", "--subst-models",
         "--no-dnp", "-o", str(step), str(pcb_path)],
        capture_output=True, text=True, timeout=600,
    )
    if r.returncode != 0:
        print("STEP export failed:\n" + (r.stderr or r.stdout)[-1500:], file=sys.stderr)
        return 1
    print(f"STEP exported: {step}  ({step.stat().st_size // 1024} KB)")

    # Ground truth. The placement checker works from footprint pad geometry;
    # this works from what KiCad actually wrote. They disagreed once already
    # (rotation sign), and the disagreement was silent, so both now run.
    try:
        from build123d import import_step
        bb = import_step(str(step)).bounding_box()
        # KiCad exports with Y mirrored: the board occupies y -BOARD_Y..0.
        over = []
        if bb.min.X < -0.5 or bb.max.X > BOARD_X + 0.5:
            over.append(f"X {bb.min.X:.1f}..{bb.max.X:.1f} vs 0..{BOARD_X:.0f}")
        if bb.min.Y < -BOARD_Y - 0.5 or bb.max.Y > 0.5:
            over.append(f"Y {bb.min.Y:.1f}..{bb.max.Y:.1f} vs {-BOARD_Y:.0f}..0")
        if over:
            print("\n!! EXPORTED STEP EXCEEDS THE OUTLINE: " + "; ".join(over),
                  file=sys.stderr)
            return 1
        print(f"  STEP verified inside the outline; "
              f"stack height {bb.max.Z - bb.min.Z:.1f} mm")
    except ImportError:
        print("  (build123d not available -- skipped STEP geometry check)")
    print("enclosure_b.py will now use the real board instead of the placeholder.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
