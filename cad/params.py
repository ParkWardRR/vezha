"""Every dimension Vezha's two enclosures depend on, in one place.

The point of this file is not to hold numbers. It is to hold *which numbers
nobody has measured yet.*

The docs are emphatic about this -- 02-enclosure-a-upper.md opens with "No
dimension here is a verified installed measurement", and 01-architecture.md
names "the three dimensions nobody should guess". So every value here carries
its provenance and a verified flag, arithmetic propagates that flag, and the
build prints what is still a guess on every run.

Usage:
    from params import A, B, COMMON, report
    width = float(A.interior_x)        # Dim -> float for build123d

Run `python params.py` to print the provenance table.
"""

from __future__ import annotations

import operator
from dataclasses import dataclass
from typing import Callable

MM = 1.0

_REGISTRY: list["Dim"] = []


@dataclass(frozen=True)
class Dim:
    """A length in mm that knows where it came from and whether it is real."""

    value: float
    source: str
    verified: bool = False
    note: str = ""
    name: str = ""

    # -- use anywhere build123d wants a number -----------------------------
    def __float__(self) -> float:
        return float(self.value)

    def __repr__(self) -> str:
        mark = "ok " if self.verified else "TBD"
        return f"<{mark} {self.name or '?'}={self.value:g}mm>"

    @property
    def label(self) -> str:
        return self.name or f"{self.value:g}"

    # -- arithmetic that carries provenance forward ------------------------
    def _combine(self, other, op: Callable, sym: str) -> "Dim":
        o = other if isinstance(other, Dim) else Dim(float(other), "literal", True)
        return Dim(
            op(self.value, o.value),
            f"{self.label} {sym} {o.label}",
            self.verified and o.verified,
            name="(derived)",
        )

    def __add__(self, o):
        return self._combine(o, operator.add, "+")

    __radd__ = __add__

    def __sub__(self, o):
        return self._combine(o, operator.sub, "-")

    def __rsub__(self, o):
        return Dim(float(o), "literal", True)._combine(self, operator.sub, "-")

    def __mul__(self, o):
        return self._combine(o, operator.mul, "*")

    __rmul__ = __mul__

    def __truediv__(self, o):
        return self._combine(o, operator.truediv, "/")


def D(name: str, value: float, source: str, verified: bool = False, note: str = "") -> Dim:
    """Declare a dimension and register it for the provenance report."""
    d = Dim(value, source, verified, note, name)
    _REGISTRY.append(d)
    return d


def dmax(*dims) -> Dim:
    """max() that keeps the verified flag (unverified if any input is)."""
    best = max(dims, key=float)
    return Dim(
        float(best),
        "max(" + ", ".join(getattr(d, "label", str(d)) for d in dims) + ")",
        all(getattr(d, "verified", True) for d in dims),
        name="(derived)",
    )


# =======================================================================
# Shared / process
# =======================================================================
class COMMON:
    wall = D(
        "wall", 2.0,
        "02-enclosure-a-upper.md -- '2 mm ABS is the reference wall'",
        verified=True,
        note="Reference wall for the antenna landing pads. Not yet a print-validated thickness.",
    )
    # FDM fit allowances. Chosen, not measured -- they must survive a test coupon.
    clearance_slip = D("clearance_slip", 0.30, "FDM fit allowance, chosen not measured")
    clearance_press = D("clearance_press", 0.10, "FDM fit allowance, chosen not measured")
    standoff_od = D("standoff_od", 5.0, "M2.5 boss, chosen not measured")
    standoff_id = D("standoff_id", 2.1, "M2.5 self-tapping pilot, chosen not measured")

    # USB-C. Both enclosures have one opening; neither is sized off a real plug.
    usbc_recept_w = D("usbc_recept_w", 9.0, "generic USB-C receptacle, part TBD")
    usbc_recept_h = D("usbc_recept_h", 3.3, "generic USB-C receptacle, part TBD")
    usbc_plug_bend = D(
        "usbc_plug_bend", 25.0,
        "GUESS -- 01-architecture.md: size the case around the mated plug and "
        "its bend radius, not the receptacle footprint",
        note="One of the three dimensions nobody should guess. Measure a real "
             "plug with the intended cable before any opening is cut.",
    )


# =======================================================================
# Enclosure A -- upper router box (headless, v1)
# =======================================================================
class A:
    # -- Orange Pi 5 Plus -------------------------------------------------
    sbc_x = D("sbc_x", 100.0, "02 -- Orange Pi 5 Plus published board size", verified=True)
    sbc_y = D("sbc_y", 75.0, "02 -- Orange Pi 5 Plus published board size", verified=True)
    sbc_pcb_t = D("sbc_pcb_t", 1.6, "assumed 1.6 mm FR-4, not stated in docs")
    sbc_hole_inset = D("sbc_hole_inset", 3.5, "GUESS -- mounting pattern not captured in docs")

    # -- Top-side radio: Intel AX210 in the E-key socket -------------------
    ax210_x = D("ax210_x", 22.0, "02 -- M.2 2230", verified=True)
    ax210_y = D("ax210_y", 30.0, "02 -- M.2 2230", verified=True)
    ax210_t = D("ax210_t", 2.4, "02 -- M.2 2230 card thickness", verified=True)

    # -- Heatsink ---------------------------------------------------------
    heatsink_h = D(
        "heatsink_h", 15.0,
        "GUESS -- 02 'Heatsink ... excluded and are exactly what will decide "
        "whether this closes'; 02#thermal: size and need both unresolved",
    )

    # -- Underside stack: THE binding dimension for this box ---------------
    adapter_t = D(
        "adapter_t", 6.0,
        "GUESS -- 02 'M-key -> E-key adapter: Installed size unverified'",
        note="Pick a specific adapter that routes PCIe, then measure it.",
    )
    radio2_t = D(
        "radio2_t", 2.4,
        "GUESS -- 02 'Second Wi-Fi card ... height unconfirmed'; MT7922/RZ616 "
        "is a candidate, not a locked part",
    )
    mhf4_plug_h = D(
        "mhf4_plug_h", 2.5,
        "GUESS -- mated MHF4 plug height, not captured in docs",
    )
    coax_bend_r = D(
        "coax_bend_r", 5.0,
        "GUESS -- 02 'plus the bend radius of the coax leaving them. That "
        "figure is unmeasured'",
    )

    #: 01-architecture.md#open-questions: "now the only thing setting this
    #: box's thickness". Every input below is a guess, so this is too.
    underside_stack = (adapter_t + radio2_t + mhf4_plug_h + coax_bend_r)

    # -- Antennas ---------------------------------------------------------
    ant_len = D("ant_len", 42.0, "02/04 -- flex antenna strip", verified=True)
    ant_w = D("ant_w", 7.0, "02/04 -- flex antenna strip", verified=True)
    ant_t = D("ant_t", 1.0, "assumed flex strip + adhesive, not stated")
    ant_lead = D("ant_lead", 100.0, "02/04 -- MHF4 lead length", verified=True)
    ant_gnd_clearance = D(
        "ant_gnd_clearance", 20.0,
        "02 -- 'roughly 20 mm from the main ground plane where practical'",
        verified=True,
        note="A layout target, not a pass/fail spec.",
    )

    # -- RTC backup cell --------------------------------------------------
    rtc_cell_d = D("rtc_cell_d", 20.0, "02#rtc-backup-cell -- 20 mm coin cell", verified=True)
    rtc_holder_h = D("rtc_holder_h", 5.0, "GUESS -- holder not selected; chemistry unresolved")

    # -- Service access ---------------------------------------------------
    # DECIDED 2026-11-18. 02 left this open: "lid, base plate, or seam split.
    # Driven by assembly and MHF4 access, nothing else."
    #
    # Answer: a PERIMETER BAND with BOTH BROAD FACES as separate plates.
    #   * 02 requires the broad faces stay clear of antennas, and all four
    #     strips live in the narrow walls. So making the broad faces removable
    #     costs no antenna real estate, while a mid-height seam split would
    #     cut straight through the strips.
    #   * The SBC mounts to the BASE PLATE on its standoffs. Pull the base and
    #     the board leaves with it, exposing the underside M.2 stack and both
    #     sets of MHF4 connectors at once -- which 02 names as the thing that
    #     breaks during service and the reason access is required at all.
    #   * The TOP CAP stays replaceable, which is exactly the hedge 04 asks
    #     for: swap only the uplink antenna pair for domes without touching
    #     anything else. 02 listed its survival as an open question; this
    #     keeps it.
    # Cost: two gasket/seam lines instead of one, and the band needs enough
    # stiffness on its own. Neither is a reason to cut antenna zones instead.
    SERVICE_ACCESS = "band-with-two-plates"
    plate_t = D("plate_t", 2.5, "chosen -- base plate carries the SBC, so it is stiffer than a wall")
    cap_t = D("cap_t", 2.0, "chosen -- top cap carries nothing but itself")

    # -- Derived interior -------------------------------------------------
    sbc_margin = D("sbc_margin", 4.0, "chosen cable/assembly margin around the SBC")
    standoff_h = underside_stack + COMMON.clearance_slip
    headroom = dmax(heatsink_h, ax210_t + 3.0)

    interior_x = sbc_x + 2 * sbc_margin + 2 * ant_t
    interior_y = sbc_y + 2 * sbc_margin + 2 * ant_t
    interior_z = standoff_h + sbc_pcb_t + headroom

    outer_x = interior_x + 2 * COMMON.wall
    outer_y = interior_y + 2 * COMMON.wall
    #: Band height + the two broad plates, not 2x wall: the plates differ in
    #: thickness because only the base carries the board.
    outer_z = interior_z + plate_t + cap_t


# =======================================================================
# Enclosure B -- lower power box (detachable)
# =======================================================================
class B:
    # -- CentyLab RotoPD Pro ----------------------------------------------
    # 06 narrowed this: the header pinout is now known from vendor artwork,
    # but 06 "What is still open" is explicit that the outline, hole
    # coordinates/diameter and tallest component remain unknown and "need the
    # .kicad_pcb or the physical board, not another email."
    rotopd_x = D("rotopd_x", 40.0, "GUESS -- 06: outline still blocking (vendor repo: CentyLab/RotoPD_Pro)")
    rotopd_y = D("rotopd_y", 30.0, "GUESS -- 06: outline still blocking (vendor repo: CentyLab/RotoPD_Pro)")
    rotopd_h = D("rotopd_h", 12.0, "GUESS -- 06: tallest component unknown")
    #: 06 U1: switched VBUS leaves on a 2-position 5 mm SCREW TERMINAL on the
    #: edge opposite the USB-C jack -- "an assembly and enclosure constraint,
    #: not just a schematic one".
    #:
    #: DECIDED 2026-11-18: REMOVE IT, solder heavy wire to the pads.
    #:   * That path is VBUS_PD, up to 5 A at up to 48 V (06 power domains).
    #:   * A screw terminal is the worse joint for that in a travel device --
    #:     it loosens under the vibration and thermal cycling this product is
    #:     defined by. A soldered joint does not.
    #:   * It is never field-disconnected. Removing the module means
    #:     desoldering it regardless, so the terminal buys no serviceability.
    #:   * It was setting the box height: ~22 mm vs the encoder's 20 mm.
    #: Cost: must be removed before the module is mounted, and it forecloses
    #: a quick module swap. Both acceptable for a soldered-down carrier.
    ROTOPD_SCREW_TERMINAL = False
    rotopd_screw_terminal_h = D(
        "rotopd_screw_terminal_h", 10.0,
        "GUESS -- 06: 2-pos 5 mm screw terminal, height never measured",
        note="Only charged to the height budget if ROTOPD_SCREW_TERMINAL is True. "
             "Decided False -- see the comment above.",
    )
    rotopd_terminal_charge = (
        rotopd_screw_terminal_h if ROTOPD_SCREW_TERMINAL
        else D("rotopd_terminal_removed", 0.0,
               "DECIDED 2026-11-18 -- terminal removed, wires soldered to pads",
               verified=True)
    )
    rotopd_mount_holes = D(
        "rotopd_mount_holes", 2.0,
        "06 U1 -- two mounting holes at the top corners flanking the USB-C jack",
        note="Count is confirmed from vendor artwork; positions and diameter "
             "are not dimensioned anywhere published.",
    )

    # -- Raspberry Pi Pico 2 (non-wireless) -------------------------------
    pico_x = D("pico_x", 51.0, "03 -- bare PCB", verified=True)
    pico_y = D("pico_y", 21.0, "03 -- bare PCB", verified=True)
    pico_t = D("pico_t", 1.0, "03 -- bare PCB", verified=True)

    #: 03 -- "pick one, it changes the height". Set to "castellated" or "socketed".
    PICO_MOUNT = "socketed"
    pico_stack_castellated = D("pico_stack_castellated", 0.0, "03 -- soldered flat to the power board", verified=True)
    pico_stack_socketed = D("pico_stack_socketed", 11.0, "GUESS -- 2.54 mm header + socket pair, not measured")
    pico_usb_overhang = D(
        "pico_usb_overhang", 1.5,
        "03 -- 'leave room for the overhanging Micro-USB port'; value is a guess",
    )

    # -- Pololu D42V55F5 (#5571) ------------------------------------------
    # Fully dimensioned in 06 from the Pololu family drawing (dev code reg34a).
    # 03's "25.4 x 25.4 x 9 mm" is the rounded summary; these are the real
    # numbers, and the 9 mm splits ABOVE and BELOW the board -- which matters,
    # because the below-board part eats into standoff height, not headroom.
    pololu_x = D("pololu_x", 25.4, "06 U3 -- Pololu family dimension drawing", verified=True)
    pololu_y = D("pololu_y", 25.4, "06 U3 -- Pololu family dimension drawing", verified=True)
    pololu_board_t = D("pololu_board_t", 1.57, "06 U3 -- board thickness", verified=True)
    pololu_above = D(
        "pololu_above", 6.1, "06 U3 -- height above board, items 5570-5577", verified=True,
        note="Items 5578/5579 are 8.0 mm. If the part number changes to one of "
             "those, the enclosure height changes with it.",
    )
    pololu_below = D("pololu_below", 1.4, "06 U3 -- height below board", verified=True)
    pololu_total_h = pololu_above + pololu_board_t + pololu_below   # 9.07 mm
    # 06 is precise here and 03 was not: 2.18 mm is the HOLE DIAMETER,
    # 2.2 mm is the inset from each edge. They are different numbers.
    pololu_hole_d = D("pololu_hole_d", 2.18, "06 U3 -- 3 holes, #2/M2", verified=True)
    pololu_hole_pitch = D("pololu_hole_pitch", 21.1, "06 U3 -- 21.1 x 21.1 mm pattern", verified=True)
    pololu_hole_inset = D("pololu_hole_inset", 2.2, "06 U3 -- 2.2 mm in from each edge", verified=True)

    # -- Power board (the one PCB) ----------------------------------------
    # Not yet drawn. Once it exists, do NOT retype it here:
    #   kicad-cli pcb export step --output cad/build/power-board.step board.kicad_pcb
    # and let enclosure_b.py import the real solid.
    pcb_t = D("pcb_t", 1.6, "assumed 1.6 mm FR-4; power board not yet drawn")
    pcb_x = D("pcb_x", 80.0, "GUESS -- power board outline not yet drawn")
    pcb_y = D("pcb_y", 60.0, "GUESS -- power board outline not yet drawn")
    pcb_margin = D("pcb_margin", 3.0, "chosen assembly margin around the power board")
    standoff_h = D("standoff_h", 4.0, "chosen; clears through-hole lead length under the board")

    # -- Panel ------------------------------------------------------------
    # CONTRADICTION IN THE DOCS, surfaced rather than silently resolved:
    #   01-architecture.md asserts "Enclosure B carries the only panel" and
    #   lists OLED + encoder as settled by the v1 scope cut.
    #   06-power-board-schematic.md "What is still open" lists "Whether
    #   Enclosure B has a front panel at all -- decides whether J4 and J5
    #   exist."
    # Those cannot both be true. Until one doc wins, this is a switch, because
    # it changes both the box height and whether the lid has openings.
    HAS_PANEL = True
    oled_x = D("oled_x", 20.076, "01 -- Adafruit 5297 active area cited in the scope-cut reasoning")
    oled_y = D("oled_y", 20.076, "01 -- Adafruit 5297 active area cited in the scope-cut reasoning")
    oled_board_h = D("oled_board_h", 8.0, "GUESS -- module not selected")
    encoder_h = D("encoder_h", 20.0, "GUESS -- push encoder not selected")

    # -- Derived interior -------------------------------------------------
    pico_stack = pico_stack_socketed if PICO_MOUNT == "socketed" else pico_stack_castellated

    #: Above-board height only. The Pololu's 1.4 mm below-board protrusion is
    #: charged to standoff height, not to headroom.
    _above_board = [
        rotopd_h + rotopd_terminal_charge,
        pololu_above,
        pico_stack + pico_t,
    ]
    if HAS_PANEL:
        _above_board += [encoder_h, oled_board_h]
    tallest_part = dmax(*_above_board)

    #: 06 U3: the regulator hangs 1.4 mm below its own board, so the standoffs
    #: must clear that as well as through-hole lead length.
    standoff_min = pololu_below + D("lead_protrusion", 1.5, "GUESS -- trimmed TH lead length")

    interior_x = pcb_x + 2 * pcb_margin
    interior_y = pcb_y + 2 * pcb_margin
    interior_z = standoff_h + pcb_t + tallest_part

    outer_x = interior_x + 2 * COMMON.wall
    outer_y = interior_y + 2 * COMMON.wall
    outer_z = interior_z + 2 * COMMON.wall


# =======================================================================
# Provenance reporting
# =======================================================================
def unverified() -> list[Dim]:
    return [d for d in _REGISTRY if not d.verified]


def violations() -> list[str]:
    """Constraints that are checkable today, regardless of what is unmeasured."""
    out = []
    if float(B.standoff_h) < float(B.standoff_min):
        out.append(
            f"B.standoff_h {float(B.standoff_h):.2f} mm < {float(B.standoff_min):.2f} mm "
            "required to clear the Pololu's below-board protrusion (06 U3: 1.4 mm) "
            "plus trimmed through-hole leads"
        )
    if float(A.ant_gnd_clearance) > float(A.interior_z):
        out.append(
            f"A antenna-to-groundplane target {float(A.ant_gnd_clearance):.1f} mm "
            f"exceeds interior height {float(A.interior_z):.1f} mm"
        )
    return out


def report() -> str:
    lines = ["", "Dimension provenance", "=" * 78]
    for d in _REGISTRY:
        mark = "  ok" if d.verified else " TBD"
        lines.append(f"{mark}  {d.name:<24} {d.value:>8.2f} mm   {d.source}")
        if d.note:
            lines.append(f"{'':>6}{'':<24} {'':>8}      note: {d.note}")

    n = len(unverified())
    lines += [
        "=" * 78,
        f"{len(_REGISTRY)} dimensions, {n} still unverified.",
        "",
        "Derived envelopes (a derived value is verified only if every input is):",
    ]
    for label, d in [
        ("A outer", (A.outer_x, A.outer_y, A.outer_z)),
        ("B outer", (B.outer_x, B.outer_y, B.outer_z)),
    ]:
        ok = all(x.verified for x in d)
        lines.append(
            f"  {'ok ' if ok else 'TBD'} {label}  "
            f"{float(d[0]):.1f} x {float(d[1]):.1f} x {float(d[2]):.1f} mm"
        )
    lines += [
        "",
        "The three dimensions nobody should guess (01-architecture.md):",
        f"  TBD  A underside stack      {float(A.underside_stack):>7.2f} mm  "
        "(adapter + card + mated plugs + coax bend)",
        f"  TBD  B RotoPD Pro envelope  "
        f"{float(B.rotopd_x):.1f} x {float(B.rotopd_y):.1f} x {float(B.rotopd_h):.1f} mm",
        f"  TBD  mated USB-C + bend     {float(COMMON.usbc_plug_bend):>7.2f} mm",
    ]

    v = violations()
    if v:
        lines += ["", "CONSTRAINT VIOLATIONS (checkable now, not waiting on measurements):"]
        lines += [f"  !! {x}" for x in v]
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    print(report())
