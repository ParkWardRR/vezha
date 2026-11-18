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
    """A length in mm that knows where it came from and how solid it is.

    Three states, because "unverified" was doing too much work:

      verified=True   a vendor drawing, a published spec, a standard, or our
                      own settled design decision. Nothing to do.
      assumed=True    a deliberate assumption with a stated basis. The model
                      proceeds on it; `validate_later()` is the punch list.
      neither         open. No basis yet. `--strict` still fails on these.

    Arithmetic propagates both flags, so a derived value is only as solid as
    its weakest input: assumed + verified = assumed.
    """

    value: float
    source: str
    verified: bool = False
    note: str = ""
    name: str = ""
    assumed: bool = False

    @property
    def status(self) -> str:
        if self.verified:
            return "ok"
        return "ASSUME" if self.assumed else "OPEN"

    @property
    def settled(self) -> bool:
        """Good enough to build on, whether proven or assumed."""
        return self.verified or self.assumed

    # -- use anywhere build123d wants a number -----------------------------
    def __float__(self) -> float:
        return float(self.value)

    def __repr__(self) -> str:
        return f"<{self.status} {self.name or '?'}={self.value:g}mm>"

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
            assumed=(self.settled and o.settled),
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


def D(name: str, value: float, source: str, verified: bool = False,
      note: str = "", assumed: bool = False) -> Dim:
    """Declare a dimension and register it for the provenance report."""
    d = Dim(value, source, verified, note, name, assumed)
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
        assumed=all(getattr(d, "settled", True) for d in dims),
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
    clearance_slip = D("clearance_slip", 0.3, "CHOSEN -- FDM slip fit; validate with a print coupon",
        assumed=True)
    clearance_press = D("clearance_press", 0.1, "CHOSEN -- FDM press fit; validate with a print coupon",
        assumed=True)
    standoff_od = D("standoff_od", 5.0, "CHOSEN -- M2.5 self-tapping boss, 5 mm OD",
        verified=True)
    standoff_id = D("standoff_id", 2.1, "CHOSEN -- M2.5 self-tapping pilot",
        verified=True)

    # USB-C. Both enclosures have one opening; neither is sized off a real plug.
    usbc_recept_w = D("usbc_recept_w", 9.0, "ASSUMED -- USB-C plug interface 8.34 mm + clearance",
        assumed=True)
    usbc_recept_h = D("usbc_recept_h", 3.3, "ASSUMED -- USB-C plug interface 2.56 mm + clearance",
        assumed=True)
    usbc_plug_bend = D("usbc_plug_bend", 30.0, "ASSUMED -- ~20 mm overmold + bend allowance for a 5 A cable",
        assumed=True,
        note="One of the three dimensions nobody should guess. Measure a real "
             "plug with the intended cable before any opening is cut.")


# =======================================================================
# Enclosure A -- upper router box (headless, v1)
# =======================================================================
class A:
    # -- Orange Pi 5 Plus -------------------------------------------------
    sbc_x = D("sbc_x", 100.0, "02 -- Orange Pi 5 Plus published board size", verified=True)
    sbc_y = D("sbc_y", 75.0, "02 -- Orange Pi 5 Plus published board size", verified=True)
    sbc_pcb_t = D("sbc_pcb_t", 1.6, "STANDARD -- 1.6 mm FR-4",
        verified=True)
    sbc_hole_inset = D("sbc_hole_inset", 3.5, "ASSUMED -- typical SBC mounting-hole inset",
        assumed=True)

    # -- Top-side radio: Intel AX210 in the E-key socket -------------------
    ax210_x = D("ax210_x", 22.0, "02 -- M.2 2230", verified=True)
    ax210_y = D("ax210_y", 30.0, "02 -- M.2 2230", verified=True)
    ax210_t = D("ax210_t", 2.4, "02 -- M.2 2230 card thickness", verified=True)

    # -- Heatsink ---------------------------------------------------------
    heatsink_h = D("heatsink_h", 15.0, "ASSUMED -- mid-size passive heatsink on RK3588",
        assumed=True)

    # -- Underside stack: THE binding dimension for this box ---------------
    adapter_t = D("adapter_t", 6.5, "ASSUMED -- adapter PCB 1.6 mm + E-key socket body",
        assumed=True,
        note="Pick a specific adapter that routes PCIe, then measure it.")
    radio2_t = D("radio2_t", 2.38, "SPEC -- M.2 2230-S3 single-sided module thickness",
        verified=True)
    mhf4_plug_h = D("mhf4_plug_h", 1.5, "ASSUMED -- mated MHF4 connector height",
        assumed=True)
    coax_bend_r = D("coax_bend_r", 5.0, "ASSUMED -- min bend radius for 1.13 mm coax",
        assumed=True)

    #: 01-architecture.md#open-questions: "now the only thing setting this
    #: box's thickness". Every input below is a guess, so this is too.
    underside_stack = (adapter_t + radio2_t + mhf4_plug_h + coax_bend_r)

    # -- Antennas ---------------------------------------------------------
    ant_len = D("ant_len", 42.0, "02/04 -- flex antenna strip", verified=True)
    ant_w = D("ant_w", 7.0, "02/04 -- flex antenna strip", verified=True)
    ant_t = D("ant_t", 1.0, "ASSUMED -- flex strip plus adhesive",
        assumed=True)
    ant_lead = D("ant_lead", 100.0, "02/04 -- MHF4 lead length", verified=True)
    ant_gnd_clearance = D(
        "ant_gnd_clearance", 20.0,
        "02 -- 'roughly 20 mm from the main ground plane where practical'",
        verified=True,
        note="A layout target, not a pass/fail spec.",
    )

    # -- RTC backup cell --------------------------------------------------
    rtc_cell_d = D("rtc_cell_d", 20.0, "02#rtc-backup-cell -- 20 mm coin cell", verified=True)
    rtc_holder_h = D("rtc_holder_h", 5.0, "ASSUMED -- 20 mm coin cell holder height",
        assumed=True)

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
    plate_t = D("plate_t", 2.5, "CHOSEN -- base plate carries the SBC, stiffer than a wall",
        verified=True)
    cap_t = D("cap_t", 2.0, "CHOSEN -- top cap carries nothing but itself",
        verified=True)

    # -- Derived interior -------------------------------------------------
    sbc_margin = D("sbc_margin", 4.0, "CHOSEN -- cable/assembly margin around the SBC",
        verified=True)
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
    rotopd_x = D("rotopd_x", 40.0, "ASSUMED CONSERVATIVE -- outline still unpublished; oversized on purpose",
        assumed=True)
    rotopd_y = D("rotopd_y", 30.0, "ASSUMED CONSERVATIVE -- outline still unpublished; oversized on purpose",
        assumed=True)
    rotopd_h = D("rotopd_h", 12.0, "ASSUMED CONSERVATIVE -- tallest component unknown",
        assumed=True)
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
    rotopd_screw_terminal_h = D("rotopd_screw_terminal_h", 10.0, "ASSUMED -- not charged; terminal removed by decision",
        assumed=True,
        note="Only charged to the height budget if ROTOPD_SCREW_TERMINAL is True. "
             "Decided False -- see the comment above.")
    rotopd_terminal_charge = (
        rotopd_screw_terminal_h if ROTOPD_SCREW_TERMINAL
        else D("rotopd_terminal_removed", 0.0,
               "DECIDED 2026-11-18 -- terminal removed, wires soldered to pads",
               verified=True)
    )
    rotopd_mount_holes = D("rotopd_mount_holes", 2.0, "06 U1 -- two holes confirmed from vendor artwork",
        verified=True,
        note="Count is confirmed from vendor artwork; positions and diameter "
             "are not dimensioned anywhere published.")

    # -- Raspberry Pi Pico 2 (non-wireless) -------------------------------
    pico_x = D("pico_x", 51.0, "03 -- bare PCB", verified=True)
    pico_y = D("pico_y", 21.0, "03 -- bare PCB", verified=True)
    pico_t = D("pico_t", 1.0, "03 -- bare PCB", verified=True)

    #: 03 -- "pick one, it changes the height". Set to "castellated" or "socketed".
    PICO_MOUNT = "socketed"
    pico_stack_castellated = D("pico_stack_castellated", 0.0, "03 -- soldered flat to the power board", verified=True)
    pico_stack_socketed = D("pico_stack_socketed", 11.0, "ASSUMED -- 2.54 mm socket + header pair",
        assumed=True)
    pico_usb_overhang = D("pico_usb_overhang", 1.5, "ASSUMED -- Micro-USB overhang past the board edge",
        assumed=True)

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
    pcb_t = D("pcb_t", 1.6, "DRAWN -- standard 1.6 mm FR-4, KiCad board default",
        verified=True)
    pcb_x = D("pcb_x", 90.0, "DRAWN -- pcb/layout.py board outline",
        verified=True)
    pcb_y = D("pcb_y", 70.0, "DRAWN -- pcb/layout.py board outline",
        verified=True)
    pcb_margin = D("pcb_margin", 3.0, "CHOSEN -- assembly margin around the power board",
        verified=True)
    standoff_h = D("standoff_h", 4.0, "CHOSEN -- clears Pololu underside 1.4 mm + trimmed leads",
        verified=True)

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
    oled_x = D("oled_x", 20.076, "VENDOR -- Adafruit 5297 active area, cited in 01",
        verified=True)
    oled_y = D("oled_y", 20.076, "VENDOR -- Adafruit 5297 active area, cited in 01",
        verified=True)
    oled_board_h = D("oled_board_h", 8.0, "ASSUMED -- Adafruit 5297 module height incl. connector",
        assumed=True)
    encoder_h = D("encoder_h", 20.0, "ASSUMED -- EC11 encoder body plus shaft above the board",
        assumed=True)

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
    standoff_min = pololu_below + D("lead_protrusion", 1.5, "ASSUMED -- trimmed through-hole lead length",
        assumed=True)

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
    """Open values: no basis at all. These are what --strict fails on."""
    return [d for d in _REGISTRY if not d.settled]


def validate_later() -> list[Dim]:
    """The punch list. Deliberate assumptions the build is proceeding on."""
    return [d for d in _REGISTRY if d.assumed and not d.verified]


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
    n_open = len(unverified())
    n_ass = len(validate_later())
    n_ok = len(_REGISTRY) - n_open - n_ass

    lines = [
        "",
        f"Dimensions: {n_ok} settled, {n_ass} assumed, {n_open} open.",
        "=" * 78,
    ]
    if n_open:
        lines.append("OPEN -- no basis at all:")
        for d in unverified():
            lines.append(f"  OPEN  {d.name:<24} {d.value:>8.2f} mm   {d.source}")
        lines.append("")

    lines.append("ASSUMED -- proceeding on these; validate per docs/10:")
    for d in validate_later():
        lines.append(f"  {d.name:<26} {d.value:>8.2f} mm   {d.source}")
        if d.note:
            lines.append(f"  {'':<26} {'':>8}      note: {d.note}")

    lines += [
        "",
        "Derived envelopes (a derived value is only as solid as its inputs):",
    ]
    for label, d in [
        ("A outer", (A.outer_x, A.outer_y, A.outer_z)),
        ("B outer", (B.outer_x, B.outer_y, B.outer_z)),
    ]:
        st = ("ok" if all(x.verified for x in d)
              else "ASSUME" if all(x.settled for x in d) else "OPEN")
        lines.append(
            f"  {st:>6}  {label}  "
            f"{float(d[0]):.1f} x {float(d[1]):.1f} x {float(d[2]):.1f} mm"
        )
    lines += [
        "",
        "The three that still want real parts (01-architecture.md, docs/10):",
        f"  A underside stack      {float(A.underside_stack):>7.2f} mm  "
        "(adapter + card + mated plugs + coax bend)",
        f"  B RotoPD Pro envelope  "
        f"{float(B.rotopd_x):.1f} x {float(B.rotopd_y):.1f} x {float(B.rotopd_h):.1f} mm",
        f"  mated USB-C + bend     {float(COMMON.usbc_plug_bend):>7.2f} mm",
    ]

    v = violations()
    if v:
        lines += ["", "CONSTRAINT VIOLATIONS (checkable now, not waiting on measurements):"]
        lines += [f"  !! {x}" for x in v]
    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    print(report())
