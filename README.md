<div align="center">

# Vezha — Fabrication Brief

### Handheld travel router · two enclosures · two PCBs

**This repo is a design brief, not a product.**
It exists so a mechanical designer and a PCB designer can build the
physical hardware. It is not documentation for using a finished device —
there isn't one yet.

<br>

[![Scope](https://img.shields.io/badge/scope-2%20enclosures%20%2B%202%20PCBs-0F766E?style=flat-square)](#scope-of-work)
[![Stage](https://img.shields.io/badge/stage-Rev%20A%20design-orange?style=flat-square)](#decision-status)
[![Architecture](https://img.shields.io/badge/architecture-settled-success?style=flat-square)](docs/01-architecture.md)
[![Enclosure A](https://img.shields.io/badge/enclosure%20A-ready%20to%20design-success?style=flat-square)](docs/02-enclosure-a-upper.md)
[![Enclosure B](https://img.shields.io/badge/enclosure%20B-blocked%20on%203%20dims-red?style=flat-square)](docs/03-enclosure-b-lower.md)
[![PCB 1](https://img.shields.io/badge/PCB%201-spec%20ready-success?style=flat-square)](docs/04-pcb-1-front-control.md)
[![PCB 2](https://img.shields.io/badge/PCB%202-spec%20ready-success?style=flat-square)](docs/05-pcb-2-power.md)
[![License](https://img.shields.io/badge/license-Blue%20Oak%201.0.0-0F766E?style=flat-square)](LICENSE.md)

[![Host](https://img.shields.io/badge/host-Orange%20Pi%205%20Plus-F47B20?style=flat-square)](docs/02-enclosure-a-upper.md)
[![SoC](https://img.shields.io/badge/SoC-Rockchip%20RK3588-0E7C7B?style=flat-square)](docs/02-enclosure-a-upper.md)
[![Uplink](https://img.shields.io/badge/uplink-AX210%20·%20top%20E--key-0071C5?style=flat-square&logo=intel&logoColor=white)](docs/01-architecture.md#radio-topology)
[![AP](https://img.shields.io/badge/AP-MT7922%20·%20M%E2%86%92E%20adapter-EC1C24?style=flat-square)](docs/01-architecture.md#radio-topology)
[![Bands](https://img.shields.io/badge/5%20GHz-simultaneous%20up%20%2B%20down-success?style=flat-square)](#the-hard-requirement)
[![Antennas](https://img.shields.io/badge/antennas-4%C3%97%20internal%20flex-blueviolet?style=flat-square)](docs/06-antennas.md)

[![PD](https://img.shields.io/badge/PD-CentyLab%20RotoPD%20Pro-333333?style=flat-square)](docs/05-pcb-2-power.md)
[![Controller](https://img.shields.io/badge/controller-Pi%20Pico%202-C51A4A?style=flat-square&logo=raspberrypi&logoColor=white)](docs/05-pcb-2-power.md)
[![Regulator](https://img.shields.io/badge/5%20V-Pololu%20D42V55F5-00843D?style=flat-square)](docs/05-pcb-2-power.md)
[![Controls](https://img.shields.io/badge/controls-toggle%20%2B%203%20keys%20%2B%20wheel-795548?style=flat-square)](docs/04-pcb-1-front-control.md)
[![Indicators](https://img.shields.io/badge/indicators-4%C3%97%20RGB%20I%C2%B2C-FF6F00?style=flat-square)](docs/04-pcb-1-front-control.md#rgb-indicators)
[![Assembly](https://img.shields.io/badge/assembly-JLCPCB-2E7D32?style=flat-square)](docs/07-bom.md)

[![Last commit](https://img.shields.io/github/last-commit/ParkWardRR/vezha?style=flat-square)](https://github.com/ParkWardRR/vezha/commits/main)
[![Issues](https://img.shields.io/github/issues/ParkWardRR/vezha?style=flat-square)](https://github.com/ParkWardRR/vezha/issues)
[![Repo size](https://img.shields.io/github/repo-size/ParkWardRR/vezha?style=flat-square)](https://github.com/ParkWardRR/vezha)

</div>

---

> [!IMPORTANT]
> **Read this first.** Every part number, price, and dimension here is a
> *candidate* unless marked otherwise. Nothing has been bought, printed, or
> bench-tested. Panel cutouts come from current manufacturer drawings, never
> from the nominal figures quoted here. Where a document says a value is
> unverified, it means exactly that — **do not design against it.**

## Start here

**→ [docs/01-architecture.md](docs/01-architecture.md)** — the system split,
radio topology, and power path. Everything else assumes it.

## Scope of work

A **two-piece** handheld router: two enclosures, two PCBs, designed together.

| | Deliverable | Contents | Status |
|---|---|---|---|
| **A** | **Upper router box** | Orange Pi 5 Plus, both Wi-Fi radios, M→E adapter, four antennas, storage, display, removable faceplate | Ready to design |
| **B** | **Lower power box** | PCB 2 only — detachable | Blocked on 3 measurements |
| **1** | **Front control board** | 3 key switches, 4 RGB indicators + TLC59116 driver, toggle landing, ANO header, harness to the Pi | Spec ready |
| **2** | **Power board** | Carrier for RotoPD Pro + Pico 2 + Pololu regulator | Spec ready |

**The governing rule:** both radios and all antennas stay in Enclosure A, so
**the power box detaches without disturbing any PCIe or antenna connection.**
Only 5 V and ground cross the seam.

## The hard requirement

**Two independent Wi-Fi radios, both on 5 GHz, at the same time** — a 5 GHz
upstream client *and* a 5 GHz downstream private AP, concurrently.

A 2.4 + 5 GHz split does not meet it. A shared-radio repeater does not meet
it. This single requirement is why there are two M.2 cards on opposite faces
of the board, four antennas, and a thermal case nobody has measured.

## Radio topology

The thing most likely to be got wrong:

| Radio | Role | Socket |
|---|---|---|
| **Intel AX210** | Hotel uplink | Orange Pi **top-side M.2 E-key**, directly |
| **MT7922 / RZ616** | Private AP | **Underside M-key** → **M→E adapter** → adapter's E-key |

One radio sits **above** the Orange Pi; the other hangs **below** it on an
adapter. The board cannot mount flat against a floor or a lid, and the
published 100 × 75 mm figure excludes heatsink, adapter, and cable bends.

## Power path

```
external USB-C charger
  → RotoPD Pro        PD negotiation, switched output
  → Pololu D42V55F5   regulated 5 V
  → seam connector    keyed, latching, 5 V + GND only
  → Orange Pi         dedicated USB-C power input
```

The **Pico 2 sits beside that path, not in it** — it controls the RotoPD Pro
over I²C and gates the router rail. It is powered from the RotoPD's auxiliary
5 V into VSYS, **never** from the Pololu rail it may be needed to bring up.

## The three dimensions nobody should guess

These decide **whether the two boxes actually close.** Measurements to take,
not values to look up:

1. **CentyLab RotoPD Pro** mounting pattern, outline, and height
2. **Underside adapter stack height** — adapter + card + mated antenna plugs
3. **Mated power connector clearance** — connector *and* cable bend

## Documents

| | Document | For | Contents |
|---|---|---|---|
| **01** | **[Architecture](docs/01-architecture.md)** | **Everyone** | The split, radio topology, power path, decision status. **Read first.** |
| **02** | [Enclosure A — upper](docs/02-enclosure-a-upper.md) | Mechanical | Contents and mounting, the double-sided board problem, antenna zones, faceplate, seam, thermal |
| **03** | [Enclosure B — lower](docs/03-enclosure-b-lower.md) | Mechanical | Power box contents, Pico mounting options, sizing, USB-C input |
| **04** | [PCB 1 — front control](docs/04-pcb-1-front-control.md) | PCB + mechanical | Switches, caps, toggle, ANO wheel, RGB indicators and driver, assembly caveats, test coupons |
| **05** | [PCB 2 — power](docs/05-pcb-2-power.md) | PCB | Carrier wiring, the three rules that must survive layout, headroom, measurement plan |
| **06** | [Antennas](docs/06-antennas.md) | RF + mechanical | Four placements with orientation, candidates and gain, tri-band clarification, RF bench test |
| **07** | [BOM](docs/07-bom.md) | Procurement | Every part with status, price, and what is unresolved |
| **08** | [Sourcing](docs/08-sourcing.md) | Procurement | JLCPCB/LCSC lookup method |
| **09** | [Background](docs/09-background.md) | Context | Original handoff. Partly superseded — kept for the *why* |
| **10** | [Display](docs/10-display.md) | Mechanical + software | 4.26" e-paper: dimensions, SPI wiring, refresh discipline, what it does to the UI |

## Decision status

**Settled — design against these**

- Two enclosures, two PCBs, power-only seam
- Both radios and all antennas in Enclosure A
- AX210 top-side E-key; second radio on an underside M→E adapter
- RotoPD Pro → Pololu → detachable connector → Orange Pi
- Pico 2 controller, powered from RotoPD auxiliary via VSYS
- Four internal flex antennas, two per radio, inside the narrow walls
- Controls: locking `AIRPLANE` toggle, three keys, ANO wheel, one RGB
  indicator per control lit through the faceplate
- Display: Waveshare 4.26" e-paper over SPI, no touch — [10](docs/10-display.md)

**Open — do not design against these**

- Second radio part and height; antenna connector type unconfirmed
- Which M→E adapter (must route PCIe)
- RotoPD Pro physical envelope — **blocks Enclosure B**
- Seam connector, thermal solution, final antenna SKU
- Power source: external bank vs. internal cell
- **Key switch termination** — SMD 6C (hot air) vs through-hole Multimec 5G
  (iron, new caps, +3.9 mm stack) vs C&K (machine-placed, lighter touch).
  [04](docs/04-pcb-1-front-control.md#switch-options)
- RGB LED part and optic — the last unsourced part on PCB 1

## Ground rules

1. **Coupons before parts.** Print a faceplate coupon with the wheel opening,
   two cap openings (flush and recessed), and one light pipe. Check optics in
   a dark room *and* daylight before ordering the real faceplate.
2. **Drawings, not nominals.** The NKK toggle's Ø6.5 mm and the 6C's
   8 × 8 × 2.5 mm body are **not** cutout dimensions.
3. **Choose optics and LED together** — they set standoff height.
4. **Measure mated hardware.** Size both boxes around connectors *with* their
   cables, not around PCB footprints.
5. **Confirm sourcing in the assembly quote**, not from a datasheet link.
6. **Freeze the enclosures last.** The RF test in
   [06](docs/06-antennas.md) can still move antenna positions, and antenna
   positions move walls.

## License

[Blue Oak Model License 1.0.0](LICENSE.md) — SPDX `BlueOak-1.0.0`. A
plain-language permissive license with an explicit patent grant and liability
disclaimer.

Blue Oak covers *software*. Once the STLs and PCB design files exist, a
hardware license such as CERN-OHL-S or CERN-OHL-P would fit those better — the
two can coexist, scoped by directory.
