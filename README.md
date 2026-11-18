<div align="center">

# Vezha — Fabrication Brief

### Handheld travel router · two enclosures · two PCBs

**This repo is a design brief, not a product.**
It exists so a mechanical designer and a PCB designer can build the
physical hardware. It is not documentation for using a finished device —
there isn't one yet.

<br>

[![Scope](https://img.shields.io/badge/scope-2%20enclosures%20%2B%202%20PCBs-0F766E?style=flat-square)](#scope-of-work)
[![Stage](https://img.shields.io/badge/stage-Rev%20A%20design-orange?style=flat-square)](#what-is-decided-vs-open)
[![Mechanical](https://img.shields.io/badge/mechanical-not%20started-red?style=flat-square)](#scope-of-work)
[![PCB 1](https://img.shields.io/badge/PCB%201-spec%20ready-success?style=flat-square)](docs/controls.md)
[![PCB 2](https://img.shields.io/badge/PCB%202-blocked%20on%20measurement-red?style=flat-square)](docs/power.md)
[![Prototype](https://img.shields.io/badge/prototype-coupons%20first-yellow?style=flat-square)](#ground-rules)
[![License](https://img.shields.io/badge/license-Blue%20Oak%201.0.0-0F766E?style=flat-square)](LICENSE.md)

[![Host](https://img.shields.io/badge/host-Orange%20Pi%205%20Plus-F47B20?style=flat-square)](#what-the-device-does)
[![SoC](https://img.shields.io/badge/SoC-Rockchip%20RK3588-0E7C7B?style=flat-square)](#what-the-device-does)
[![Radios](https://img.shields.io/badge/radios-2%C3%97%20M.2%20PCIe-0071C5?style=flat-square)](#constraints-that-drive-the-design)
[![Antennas](https://img.shields.io/badge/antennas-4%C3%97%20internal%20flex-blueviolet?style=flat-square)](docs/antennas.md)
[![Power](https://img.shields.io/badge/power-USB--C%20PD%20%E2%86%92%205%20V-333333?style=flat-square)](docs/handoff.md#power-and-portability)
[![Controls](https://img.shields.io/badge/controls-toggle%20%2B%203%20keys%20%2B%20wheel-795548?style=flat-square)](docs/controls.md)
[![Indicators](https://img.shields.io/badge/indicators-4%C3%97%20RGB%20I%C2%B2C-FF6F00?style=flat-square)](docs/controls.md#rgb-indicators)
[![Assembly](https://img.shields.io/badge/assembly-JLCPCB-2E7D32?style=flat-square)](docs/controls.md#before-sending-the-board-to-jlcpcb)

[![Last commit](https://img.shields.io/github/last-commit/ParkWardRR/vezha?style=flat-square)](https://github.com/ParkWardRR/vezha/commits/main)
[![Issues](https://img.shields.io/github/issues/ParkWardRR/vezha?style=flat-square)](https://github.com/ParkWardRR/vezha/issues)
[![Repo size](https://img.shields.io/github/repo-size/ParkWardRR/vezha?style=flat-square)](https://github.com/ParkWardRR/vezha)

</div>

---

> [!IMPORTANT]
> **Read this first.** Every part number, price, and dimension in this repo is
> a *candidate*, not a verified selection. Nothing has been bought, printed,
> or bench-tested. Panel cutouts must come from current manufacturer drawings,
> never from the nominal figures quoted here. Where a document says a value is
> unverified, it means exactly that — do not design against it.

## Scope of work

Two enclosures and two PCBs, designed to go together.

### Enclosures

| | Enclosure | Contents | Notes |
|---|---|---|---|
| **A** | **Upper router box** | Orange Pi 5 Plus, two M.2 Wi-Fi cards, four internal antennas, storage, display, front faceplate with all controls and indicators | Carries everything electronic except power. The **faceplate is removable** and is its own part. |
| **B** | **Lower power box** | Battery / USB-C PD input, power conversion to regulated 5 V | **Detachable from A.** No controls, no indicators, no radios mount here. |

The two boxes stack into one handheld unit. **Nothing from the upper box may
depend on the lower box being attached** beyond power.

### PCBs

| | Board | Function | Lives in |
|---|---|---|---|
| **1** | **Front control board** | APEM 6C switches (3 populated of 5), four RGB indicators, TI TLC59116 I²C LED driver, landing pads for the NKK toggle leads, STEMMA QT header to the ANO wheel, one keyed harness connector to the Orange Pi | Enclosure **A**, on standoffs behind the faceplate |
| **2** | **Power board** | USB-C PD sink and negotiation, conversion to regulated 5 V, box-to-box power interconnect | Enclosure **B** |

> [!NOTE]
> Board 1 is specified in detail in [controls.md](docs/controls.md) and is
> ready to design against. Board 2 is scoped in [power.md](docs/power.md) but
> **blocked** — its design cannot start until the system's actual current draw
> is measured. Enclosure B's dimensions are an output of that work, not an
> input.

## What the device does

Enough context to make the mechanical decisions make sense.

Vezha is a battery-powered travel router. One Wi-Fi card joins the hotel or
public network as a client; the second broadcasts a private network for the
owner's own devices. **Both must operate on 5 GHz simultaneously** — that
single requirement is why there are two M.2 cards, four antennas, and a
thermal problem worth taking seriously.

```mermaid
flowchart TB
    subgraph A["ENCLOSURE A — upper router box"]
        direction TB
        FACE["<b>Faceplate</b> (removable part)<br/>toggle · 3 keys · ANO wheel · 4 RGB windows · display"]:::face
        PCB1["<b>PCB 1</b> — front control board<br/>switches · RGB · TLC59116 · ANO header"]:::pcb
        PI["<b>Orange Pi 5 Plus</b><br/>2 × M.2 Wi-Fi · storage"]:::core
        ANT["<b>4 × flex antennas</b><br/>top · left wall · right wall · bottom"]:::ant
        FACE --- PCB1
        PCB1 -->|keyed harness| PI
        PI --- ANT
    end
    subgraph B["ENCLOSURE B — lower power box (detachable)"]
        PCB2["<b>PCB 2</b> — power board<br/>USB-C PD sink → regulated 5 V"]:::pcb
        BATT["battery"]:::core
        BATT --- PCB2
    end
    PCB2 ==>|"5 V, box-to-box<br/>power only"| PI

    classDef face fill:#ede9fe,stroke:#7c3aed,color:#0f172a
    classDef pcb fill:#dcfce7,stroke:#16a34a,color:#0f172a
    classDef core fill:#dbeafe,stroke:#2563eb,color:#0f172a
    classDef ant fill:#ffedd5,stroke:#ea580c,color:#0f172a
```

## Constraints that drive the design

These are the requirements most likely to be violated by a reasonable-looking
design, so they are called out rather than left in the detail docs.

| # | Constraint | Consequence for the build |
|---|---|---|
| 1 | **Two M.2 PCIe Wi-Fi cards must fit and enumerate together** | Slot/adapter topology and physical clearance are unresolved. This is the first thing to confirm, before any shell geometry. |
| 2 | **Four internal antennas, two per radio, kept apart** | Antennas go inside the *narrow walls* — top edge, left wall, right wall, bottom edge. Broad screen and back faces stay clear. Do not bunch all four under one cap to simplify routing. |
| 3 | **Antenna leads are 100 mm** | Mock up cable routes **before** fixing board and antenna positions. The leads may not reach every corner. |
| 4 | **No metal or carbon-filled filament in antenna zones** | Keep antennas away from display, battery, and heatsink. Target ~20 mm from the main ground plane where practical. |
| 5 | **Display mounts on its own bracket** | Pressing a button must not flex the display mount or load its ribbon. |
| 6 | **Display opening separate from control openings** | A display change must not force a new button PCB. |
| 7 | **Toggle clamps to the faceplate, not the PCB** | Its solder lugs run as leads to PCB 1. For a printed prototype, use a thin mounting land or metal insert — do not assume its nut clears the full printed wall. |
| 8 | **Indicator light must not leak** | RGB light goes through a flush diffuser above each label, with opaque walls between indicators. Keycaps stay opaque. No glow around the cap. |
| 9 | **Low power, no dedicated cooling preferred** | Hardware selection favours parts that do not need active cooling — but two 6E radios under simultaneous load is an untested thermal case. |

## Document map

| Document | For whom | Contents |
|---|---|---|
| **[controls.md](docs/controls.md)** | **PCB + mechanical** | The most complete spec here. Faceplate concept, control BOM with exact part numbers, switch/cap/toggle mounting, RGB indicator design and driver, JLCPCB assembly caveats, test coupons. |
| **[antennas.md](docs/antennas.md)** | **Mechanical** | Antenna candidates with published gain, the four-position internal layout with a sketch, wall/clearance rules, and the RF bench test that must pass before the enclosure is frozen. |
| **[power.md](docs/power.md)** | **PCB 2 + mechanical** | What the power board must do, what it has to power, why its design is blocked on measurement, and the box-to-box interconnect requirements. |
| **[handoff.md](docs/handoff.md)** | Background | Project-wide state: hardware status, power budget, software plans, open questions. Start here for *why*, not *what to build*. |
| **[parts-sourcing.md](docs/parts-sourcing.md)** | Procurement | How to query JLCPCB/LCSC for availability and price, and parts checked so far. |

## What is decided vs open

**Decided enough to design around**

- Two enclosures (upper router box + detachable power box), two PCBs
- Removable faceplate as a separate part
- Control set: locking `AIRPLANE` toggle, three action keys (`LINK`, `MAC`,
  `★`), ANO navigation wheel
- One RGB indicator per control, lit through the faceplate, not the keycap
- Four internal flex antennas, two per radio, in the narrow walls

**Open — do not design against these yet**

- M.2 slot topology and whether both cards physically fit
- Final antenna SKU and geometry
- USB-C PD profile, converter, battery, and therefore the size of Enclosure B
- Display model, and whether it gains real menus (which would change the
  control layout)
- Thermal solution
- JLCPCB assembly sourcing for the 6C switches, the TLC59116, and the RGB LEDs

## Ground rules

1. **Coupons before parts.** Print a faceplate coupon with the wheel opening,
   two cap openings (one flush, one recessed), and one light pipe. Check the
   optics in a dark room *and* in daylight before ordering the real faceplate.
2. **Drawings, not nominals.** Every panel cutout comes from the current
   manufacturer drawing. The NKK toggle's Ø6.5 mm and the 6C's 8 × 8 × 2.5 mm
   body are **not** cutout dimensions.
3. **Choose optics and LED together.** They set the standoff height, so they
   cannot be picked after the stack is frozen.
4. **Confirm sourcing in the assembly quote**, not from a datasheet link.
5. **Freeze the enclosure last.** The RF bench test in
   [antennas.md](docs/antennas.md) can still move antenna positions, and
   antenna positions move walls.

## License

[Blue Oak Model License 1.0.0](LICENSE.md) — SPDX `BlueOak-1.0.0`. A
plain-language permissive license with an explicit patent grant and liability
disclaimer.

Blue Oak covers *software*. Once the STLs and PCB design files exist, a
hardware license such as CERN-OHL-S or CERN-OHL-P would fit those better — the
two can coexist, scoped by directory.
