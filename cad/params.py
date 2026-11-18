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

    # -- Derived interior -------------------------------------------------
    sbc_margin = D("sbc_margin", 4.0, "chosen cable/assembly margin around the SBC")
    standoff_h = underside_stack + COMMON.clearance_slip
    headroom = dmax(heatsink_h, ax210_t + 3.0)

    interior_x = sbc_x + 2 * sbc_margin + 2 * ant_t
    interior_y = sbc_y + 2 * sbc_margin + 2 * ant_t
    interior_z = standoff_h + sbc_pcb_t + headroom

    outer_x = interior_x + 2 * COMMON.wall
    outer_y = interior_y + 2 * COMMON.wall
    outer_z = interior_z + 2 * COMMON.wall


# =======================================================================
# Enclosure B -- lower power box (detachable)
# =======================================================================
class B:
    # -- CentyLab RotoPD Pro ----------------------------------------------
    # 03: "Outline, height, and mounting pattern all unverified". The least
    # knowable footprint in the build -- use the vendor PCB files or measure.
    rotopd_x = D("rotopd_x", 40.0, "GUESS -- 03: outline unverified (vendor repo: CentyLab/RotoPD_Pro)")
    rotopd_y = D("rotopd_y", 30.0, "GUESS -- 03: outline unverified (vendor repo: CentyLab/RotoPD_Pro)")
    rotopd_h = D("rotopd_h", 12.0, "GUESS -- 03: height unverified")

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
    pololu_x = D("pololu_x", 25.4, "03 -- Pololu #5571 drawing", verified=True)
    pololu_y = D("pololu_y", 25.4, "03 -- Pololu #5571 drawing", verified=True)
    pololu_h = D("pololu_h", 9.0, "03 -- Pololu #5571 drawing", verified=True)
    pololu_m2_hole = D("pololu_m2_hole", 2.2, "03 -- three M2 mounting holes", verified=True)

    # -- Power board (the one PCB) ----------------------------------------
    # Not yet drawn. Once it exists, do NOT retype it here:
    #   kicad-cli pcb export step --output cad/build/power-board.step board.kicad_pcb
    # and let enclosure_b.py import the real solid.
    pcb_t = D("pcb_t", 1.6, "assumed 1.6 mm FR-4; power board not yet drawn")
    pcb_x = D("pcb_x", 80.0, "GUESS -- power board outline not yet drawn")
    pcb_y = D("pcb_y", 60.0, "GUESS -- power board outline not yet drawn")
    pcb_margin = D("pcb_margin", 3.0, "chosen assembly margin around the power board")
    standoff_h = D("standoff_h", 4.0, "chosen; clears through-hole lead length under the board")

    # -- Panel: 03 says this box carries the only hardware UI --------------
    oled_x = D("oled_x", 20.076, "01 -- Adafruit 5297 active area cited in the scope-cut reasoning")
    oled_y = D("oled_y", 20.076, "01 -- Adafruit 5297 active area cited in the scope-cut reasoning")
    oled_board_h = D("oled_board_h", 8.0, "GUESS -- module not selected")
    encoder_h = D("encoder_h", 20.0, "GUESS -- push encoder not selected")

    # -- Derived interior -------------------------------------------------
    pico_stack = pico_stack_socketed if PICO_MOUNT == "socketed" else pico_stack_castellated
    tallest_part = dmax(rotopd_h, pololu_h, pico_stack + pico_t, encoder_h, oled_board_h)

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
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    print(report())
