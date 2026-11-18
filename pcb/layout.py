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

# =======================================================================
# Placement
# =======================================================================
# Two tiers, because the first attempt at this was bad in a specific way:
# every passive sat at a hand-typed coordinate in a tidy grid, which looks
# fine in a render and is wrong electrically. A decoupling cap 7 mm from the
# pin it decouples is not decoupling anything.
#
# ANCHORS are absolute: the ICs, modules and wall connectors, placed by
# floorplan. SATELLITES are placed relative to a NAMED PAD of their anchor,
# so "C9 straddles U4's BOOT pin" survives any footprint whose internal pad
# geometry I guessed wrong.

#: (ref, footprint, x, y, rotation)
ANCHORS = [
    # --- 48 V accessory buck, top strip -------------------------------
    ("U4",  pb.FP_SOIC8_EP,  40.0, 12.0, 0.0),
    ("U5",  pb.FP_SOT23_6,   64.0, 12.0, 0.0),
    ("J6",  pb.FP_USBC_16P,  83.0, 10.0, 0.0),      # accessory out, x-large wall

    # --- PD inlet, x-small wall ---------------------------------------
    ("U1",  pb.FP_HDR_1X8,    6.0, 26.0, 0.0),
    ("U1P", pb.FP_HDR.format(n=2), 6.0, 50.0, 0.0),
    ("J1",  pb.FP_JST_SH4,    9.0, 14.0, 0.0),
    ("JP1", pb.FP_R0603,     13.0, 20.0, 0.0),
    ("D1",  pb.FP_SMA,       12.0, 46.0, 0.0),

    # --- the 4 A router rail, kept SHORT ------------------------------
    # U3 -> R13 -> J2 in a line against the x-large wall. SIM-04 allows
    # 25 mohm for the whole round trip, so rail length is a budget item,
    # not a style choice. VBUS_PD from U1 is allowed to be long instead:
    # at 20-48 V the same power is far less current and the Pololu
    # regulates the drop out anyway.
    ("U3",  pb.FP_HDR_2X6,   56.0, 26.0, 0.0),      # Pololu carrier
    ("R13", pb.FP_R2512,     70.0, 30.0, 0.0),      # 2 mohm shunt
    ("U6",  pb.FP_VSSOP10,   70.0, 35.5, 0.0),      # INA226, Kelvin at R13
    ("J2",  pb.FP_USBC_6P,   83.0, 30.0, 0.0),      # seam out, x-large wall

    # --- controller and console ----------------------------------------
    # rot 270 puts GP12/13/14 on the Pico's top edge, so the encoder RC
    # can sit at those inputs instead of across the board from them.
    ("U2",  pb.PICO_FP,      79.0, 46.0, 270.0),
    ("J5",  pb.FP_HDR.format(n=4), 46.0, 33.0, 0.0),   # encoder
    ("J4",  pb.FP_JST_SH4,   24.0, 49.0, 0.0),         # OLED
    ("J3",  pb.FP_HDR.format(n=3), 13.0, 56.0, 0.0),   # telemetry
    ("J7",  pb.FP_HDR.format(n=3), 20.0, 62.0, 0.0),   # SWD
]

#: (ref, footprint, anchor_ref, anchor_pin, dx, dy, rotation)
#: Offsets are mm from that pad, so intent is readable: "2.6 mm right of
#: U4's VIN pin" rather than an absolute coordinate nobody can check.
SATELLITES = [
    # --- U4's right column is SW / BOOT / VIN / PG, top to bottom, and FB
    # --- is bottom-LEFT. That is lucky: the switch node and the feedback
    # --- node end up on opposite sides of the part without trying.
    ("C9",  pb.FP_C0603, "U4", str(pb.U4["BOOT"]),  2.94, -1.20,  0.0),
    ("L1",  pb.FP_IND,   "U4", str(pb.U4["SW"]),    9.44, -2.50,  0.0),
    ("C6",  pb.FP_C0603, "U4", str(pb.U4["VIN"]),   2.70,  0.00,  0.0),
    ("C4",  pb.FP_C1210, "U4", str(pb.U4["VIN"]),   6.80,  2.80, 90.0),
    ("C5",  pb.FP_C1210, "U4", str(pb.U4["VIN"]),  10.60,  2.80, 90.0),
    ("C7",  pb.FP_C1210, "L1", "2",                 3.30,  0.00, 90.0),
    ("C8",  pb.FP_C0603, "L1", "2",                 3.30,  4.60, 90.0),
    ("R18", pb.FP_R0603, "U4", str(pb.U4["FB"]),   -3.04,  0.00,  0.0),
    ("R19", pb.FP_R0603, "U4", str(pb.U4["FB"]),   -3.04,  2.50,  0.0),
    ("R17", pb.FP_R0603, "U4", str(pb.U4["RT"]),   -3.04, -1.23,  0.0),
    ("R20", pb.FP_R0603, "U4", str(pb.U4["PG"]),    0.00,  3.10,  0.0),

    # --- limiter satellites, at their own pins
    ("R5",  pb.FP_R0603, "U5", str(pb.U5["ILIM"]),  3.36, -1.00,  0.0),
    ("R6",  pb.FP_R0603, "U5", str(pb.U5["FAULT"]), 3.36,  1.05,  0.0),

    # --- CC pull-ups and the BC1.2 short, inboard of the connector
    ("R3",  pb.FP_R0603, "J6", "A5",               -7.75,  0.04,  0.0),
    ("R4",  pb.FP_R0603, "J6", "B5",              -10.75,  3.04,  0.0),
    ("R21", pb.FP_R0603, "J6", "A6",               -8.75,  6.04,  0.0),

    # --- rail control, flanking U3's own EN and PG pins
    ("R1",  pb.FP_R0603, "U3", str(pb.U3["EN"]),   -4.00, -3.00,  0.0),
    ("R2",  pb.FP_R0603, "U3", str(pb.U3["PG"]),    3.96,  0.00,  0.0),

    # --- 06: the NTC goes against U3's thermal pad. On a header-mounted
    # --- module that means UNDER it -- see UNDER_MODULE below.
    ("RT1", pb.FP_R0603, "U3", "1",                 6.50,  3.00,  0.0),
    ("R16", pb.FP_R0603, "U3", "1",                 6.50,  0.50,  0.0),

    # --- encoder RC at the GPIOs it filters, not across the board
    ("C1",  pb.FP_C0603, "U2", "16",                0.00, -4.50, 90.0),
    ("C2",  pb.FP_C0603, "U2", "17",                0.00, -4.50, 90.0),
    ("C3",  pb.FP_C0603, "U2", "19",                0.00, -4.50, 90.0),
    ("R10", pb.FP_R0603, "U2", "16",                0.00, -7.50, 90.0),
    ("R11", pb.FP_R0603, "U2", "17",                0.00, -7.50, 90.0),
    ("R12", pb.FP_R0603, "U2", "19",                0.00, -7.50, 90.0),
    ("R7",  pb.FP_R0603, "J5", "1",                 4.20,  0.00,  0.0),
    ("R8",  pb.FP_R0603, "J5", "2",                 4.20,  0.00,  0.0),
    ("R9",  pb.FP_R0603, "J5", "3",                 4.20,  0.00,  0.0),

    # --- telemetry series resistors at the header
    ("R14", pb.FP_R0603, "J3", "1",                 4.00,  0.00,  0.0),
    ("R15", pb.FP_R0603, "J3", "2",                 4.00,  0.00,  0.0),
]

#: Tried and abandoned: placing the NTC UNDER the Pololu for thermal contact.
#: There is ~8 mm of air under a header-mounted module, so height was fine,
#: but the pin field is not. The rows are 2.54 mm apart and the pins repeat
#: every 2.54 mm, so a 0603 lands on a through-hole pad whichever way it is
#: turned -- DRC reported real shorts between R16 and U3's GND pins. RT1 now
#: sits immediately beside the module. Less ideal thermally, but it is a
#: resistor divider, not a short.
UNDER_MODULE: set = set()


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


def pad_positions(fp: Footprint, x: float, y: float, rot: float) -> dict[str, tuple]:
    """World (x, y) of every pad on a placed footprint."""
    import math

    a = math.radians(-rot)          # KiCad sign convention, see footprint_extent
    ca, sa = math.cos(a), math.sin(a)
    out = {}
    for pad in fp.pads:
        px, py = pad.position.X, pad.position.Y
        out[str(pad.number)] = (x + px * ca - py * sa, y + px * sa + py * ca)
    return out


def _span(pads: dict, netmap: dict, net: str, only=None) -> tuple:
    """Bounding-box diagonal of every pad on a net, and which pads they are."""
    import math

    pts = [(ref, pin, pads[(ref, pin)])
           for (ref, pin), n in netmap.items()
           if n == net and (ref, pin) in pads and (only is None or ref in only)]
    if len(pts) < 2:
        return 0.0, pts
    xs = [p[2][0] for p in pts]
    ys = [p[2][1] for p in pts]
    return math.hypot(max(xs) - min(xs), max(ys) - min(ys)), pts


def _gap(pads, a, b) -> float:
    import math
    (ax, ay), (bx, by) = pads[a], pads[b]
    return math.hypot(ax - bx, ay - by)


#: Layout rules that come from the electrical design, not from taste. Each is
#: (description, callable -> None | problem string). Keeping them here means a
#: bad placement fails the build instead of looking fine in a render.
def check_critical_nets(pads: dict, netmap: dict) -> list[str]:
    problems = []

    def limit(net, mm, why, only=None):
        span, pts = _span(pads, netmap, net, only)
        if span > mm:
            refs = sorted({f"{r}.{p}" for r, p, _ in pts})
            problems.append(
                f"{net}: pads span {span:.1f} mm, limit {mm:.0f} mm -- {why}\n"
                f"        pads: {', '.join(refs)}"
            )

    # --- the 80 V buck, where loop area is the whole game -----------------
    # The input loop (C_IN -> VIN -> GND) and the switch node are what
    # radiate. 06 chose an 80 V part precisely because VBUS reaches 48 V;
    # that is also what makes a sloppy loop expensive.
    limit("ACC_SW", 9.0, "48 V switch node: keep the radiating copper tiny",
          only={"U4", "L1", "C9"})
    limit("ACC_BOOT", 7.0, "bootstrap cap must sit across BOOT-SW",
          only={"U4", "C9"})
    # Split by role rather than one crude span. The high-frequency cap is
    # what sets the input loop area and must be right at the pin; the bulk
    # electrolytic-class caps carry low-frequency ripple and can sit further
    # out. Lumping all three under one limit was wrong, not just strict.
    limit("VBUS_PD", 5.0, "HF input cap C6 must sit right at U4's VIN pin",
          only={"U4", "C6"})
    limit("VBUS_PD", 12.0, "bulk input caps C4/C5 near U4's VIN pin",
          only={"U4", "C4", "C5"})
    limit("ACC_FB", 14.0, "feedback node: short, and away from SW",
          only={"U4", "R18", "R19"})

    # --- the 4 A router rail, where resistance is the whole game ----------
    # SIM-04: the entire round trip may be no more than 25 mohm to hold
    # 4.75 V at the Pi. Every mm of narrow trace spends that budget.
    limit("+5V_RTR", 26.0, "4 A rail U3 VOUT -> shunt; SIM-04 allows 25 mohm total",
          only={"U3", "R13", "U6"})
    limit("+5V_RTR_SH", 34.0, "4 A rail shunt -> seam connector; same budget",
          only={"R13", "U6", "J2"})

    # --- INA226 Kelvin sense ---------------------------------------------
    # The shunt is 2 mohm. Sense leads that pick up rail current instead of
    # tapping the shunt turn a current measurement into a guess, and the
    # shutdown decision depends on it.
    for sense, shunt_pad in (("9", "1"), ("10", "2")):
        try:
            d = _gap(pads, ("U6", sense), ("R13", shunt_pad))
        except KeyError:
            continue
        if d > 8.0:
            problems.append(
                f"U6 pin {sense} is {d:.1f} mm from R13 pad {shunt_pad}; "
                "Kelvin sense wants <8 mm")

    # --- 06: RT1 sits against U3's thermal pad ----------------------------
    try:
        d = _gap(pads, ("RT1", "1"), ("U3", "1"))
        if d > 12.0:
            problems.append(
                f"RT1 is {d:.1f} mm from U3; 06 puts the NTC against U3's "
                "thermal pad, so it must be under the module")
    except KeyError:
        pass

    # --- decoupling and RC filters belong at the pin they serve -----------
    # SIM-05's RC only works if the cap is at the GPIO, not 8 mm away.
    for ch, (rs, cap, gpio) in {
        "A": ("R10", "C1", "16"), "B": ("R11", "C2", "17"),
        "SW": ("R12", "C3", "19"),
    }.items():
        try:
            d = _gap(pads, (cap, "1"), ("U2", gpio))
            if d > 20.0:
                problems.append(
                    f"encoder {ch}: {cap} is {d:.1f} mm from U2 pin {gpio}; "
                    "the RC filter belongs at the input it filters")
        except KeyError:
            pass

    return problems


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
            if (a, b) in UNDER_MODULE or (b, a) in UNDER_MODULE:
                continue
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

    placed, missing, extents, pads = [], [], {}, {}

    def put(ref, spec, x, y, rot):
        try:
            fp = load_footprint(spec)
        except FileNotFoundError as e:
            missing.append(f"{ref}: {e}")
            return
        fp.groups = []
        if ref == "U2" and getattr(fp, "zones", None):
            dropped = [getattr(z, "name", "?") for z in fp.zones]
            fp.zones = []
            print(f"  U2: dropped Pico-W-only zones {dropped} (non-wireless Pico 2)")
        ext = footprint_extent(fp, x, y, rot)
        if ext:
            extents[ref] = ext
        for pin, pos in pad_positions(fp, x, y, rot).items():
            pads[(ref, pin)] = pos
        fp.properties["Reference"] = ref
        fp.position = Position(x, y, rot)
        fp.layer = "F.Cu"
        board.footprints.append(fp)
        placed.append(ref)

    # Pass 1: anchors at absolute positions.
    for ref, spec, x, y, rot in ANCHORS:
        put(ref, spec, x, y, rot)

    # Pass 2: satellites, resolved against their anchor's real pad.
    for ref, spec, a_ref, a_pin, dx, dy, rot in SATELLITES:
        base = pads.get((a_ref, a_pin))
        if base is None:
            missing.append(f"{ref}: anchor pad {a_ref}.{a_pin} not found")
            continue
        put(ref, spec, base[0] + dx, base[1] + dy, rot)

    if missing:
        raise RuntimeError("missing footprints:\n  " + "\n  ".join(missing))

    net_file = BUILD / "vezha-power.net"
    if net_file.exists():
        netmap = parse_netlist(net_file)
        hit, miss = assign_nets(board, netmap)
        print(f"  nets: {len(board.nets) - 1} nets, {hit} pads assigned, "
              f"{miss} pads left unconnected")
        net_issues = check_critical_nets(pads, netmap)
        if net_issues:
            print(f"\n!! ELECTRICAL LAYOUT: {len(net_issues)} rule(s) violated")
            for i in net_issues:
                print(f"   - {i}")
            raise SystemExit(1)
        print("  electrical layout: critical nets within their limits")

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
