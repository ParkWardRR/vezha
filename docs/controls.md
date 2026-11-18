# Vezha — Physical Controls and Faceplate

Status: **design settled enough to buy test parts; mechanics not frozen.**
Buy the switches and wheel *before* committing the mechanical stack. Panel
cutouts must come from the manufacturer's current drawing, never from a
nominal bushing diameter.

> **Revision note.** This supersedes an earlier four-key layout
> (`LINK` / `MAC` / `F1` / `F2`). Adding the ANO navigation wheel makes two
> general-purpose function keys redundant, so the front row drops to three
> action keys and the wheel handles browsing and selection.

## Concept

A **removable front faceplate** on the upper router box, carrying:

- A locking `AIRPLANE` toggle on one shoulder, clamped through the faceplate
- Three action keys — `LINK`, `MAC`, `★` — on a custom front board
- An **ANO navigation wheel** for scrolling, navigation, and selection

Dedicated keys cover the actions worth a physical control; the wheel covers
everything menu-shaped, without duplicating its five buttons as separate keys.

Everything wires to the Orange Pi in the upper box. **Nothing mounts to the
removable power box.** Keep the display opening separate from the control
openings so a display change does not force a new button PCB.

## Bill of materials

| Qty | Part | Approx. USD | Where it mounts |
|---:|---|---:|---|
| 1 | [Adafruit #6310 — pre-soldered ANO I²C module](https://www.adafruit.com/product/6310) | $13.95 | Own standoffs or bracket behind the faceplate, wheel exposed. Short STEMMA QT cable to the front board. **This is the assembled I²C version**, not the bare wheel or the passive breakout. |
| 5 | [APEM Ultramec 6C](https://www.apem.com/en-us/pcb-switches/tactile-switches/ultramec-6c), exact PN `6CJ1NOPR` | $3.07 ea | Top-actuated SMD switches on the faceplate-facing side of the front PCB. **Populate three, keep two spares.** |
| 5 | APEM/MEC 10G caps — `10G09` black, `10G08` red | ~$1–2 ea (estimate) | Fit by hand after assembly. Black for `LINK` and `★`; red or recessed for `MAC`. The floating cap option helps align switch PCB to front panel. |
| 1 | [NKK locking toggle](https://www.nkkswitches.eu/products/Toggles/M/M2012LL4G01/), order `MN12LL4G01` | ~$11 | Clamps through the faceplate with its bushing and nut. Leads run to the front board — **do not mount it to the PCB.** Give the lever a protective recess with room to pull it. |

**Budget ~$45–50** for controls including spares, before cables, shipping, and
PCB assembly.

### If the 6C feels too firm

The 6C is firm at about **3.6 N** — test one before committing to the panel.
The lighter alternative is [C&K KSC series](https://www.ckswitches.com/products/switches/product-details/Tactile/KSC/)
`KSC221J LFS`, roughly 2 N at about $0.52.

It is **not a drop-in replacement**: different footprint, and it needs a
separate plunger design rather than the MEC cap system. Start with the MEC —
the switch-and-cap combination is what makes this a straightforward premium
front panel.

## Control behavior and wiring

| Control | Default behavior | Connection |
|---|---|---|
| `AIRPLANE` | Maintained `RADIOS / OFF`. Read it before bringing up wireless; keep Ethernet available. | **Dedicated Orange Pi GPIO, independent of the ANO.** |
| `LINK` | Tap: uplink / IP / portal status. Hold: retry the uplink. | One GPIO per key, switch to ground. |
| `MAC` | Tap: show current uplink MAC. Hold 2 s: rotate it and reconnect. Factory-MAC restore stays in the menu. | Same switch as `LINK`, but **cap set lower** so it feels different and is harder to hit by accident. |
| `★` | Wi-Fi join QR code; user-assignable later. | One GPIO. For a second shortcut, reserve a fourth footprint but **do not cut the first faceplate for it.** |
| ANO wheel | Rotate to browse, center to select, left to go back. Leave the other directions unassigned until there is a real use. | 3.3 V, GND, SDA, SCL over STEMMA QT; default address `0x49`. An `INT` wire or test pad is optional for event-driven input — **it is not carried on the four-wire QT cable.** |
| `RECOVERY` *(optional, hidden)* | Boot a known wired management profile. **No factory wipe.** | Reserve the footprint behind a pinhole by the Ethernet ports or inside the service cover — not on the front row. |

### rfkill is not an interlock

`AIRPLANE` on a GPIO is a **software-controlled radio block**, not a hardware
disable, unless a verified hardware path is added. A Linux
[`rfkill`](https://networkmanager.dev/docs/rfkill/) implementation can disagree
with the switch position.

Consequence: put one small LED beside `AIRPLANE` and drive it from **confirmed
radio-off state**, not from switch position. That gives live feedback even when
the display is showing a stale image.

## Before sending the board to JLCPCB

**Assembly availability and switch choice are separate decisions.** There is no
verified JLCPCB assembly-library listing for `6CJ1NOPR` — check the exact
manufacturer part number in the assembly quote.

If JLC cannot source it: leave those three positions unpopulated and install
DigiKey parts with paste and hot air or a small reflow setup. The switch uses
**J-leads**, so do not plan around hand-soldering with an iron. The ANO,
keycaps, and toggle are final mechanical assembly items regardless.

## Mechanical test coupon

Buy the ANO and switches **before** freezing the mechanical stack. Print a small
faceplate coupon with the wheel opening and **two cap openings — one flush, one
recessed.** With the real parts mounted, check:

1. All four wheel directions and the center press without the wheel rubbing
2. Caps return freely with no preload
3. The recessed `MAC` position feels distinct from the flush keys
4. The toggle pulls easily against its locking detent

Then set standoff height and PCB outlines.

That test says more about how premium the finished controls feel than the
switch force spec alone.

## Shell layout

**Outside.** `AIRPLANE` in a shallow pocket at one end of the faceplate — enough
finger clearance to pull the locking lever, but below the surrounding case
profile so it does not snag in a bag. Action keys in a row below the display;
wheel positioned for thumb reach.

**Inside.** Front PCB parallel to the faceplate on four standoffs. Display on
its **own bracket**, so pressing buttons does not flex the display mount or load
its ribbon. Toggle leads to the front board, then one keyed, detachable harness
from that board to the Orange Pi.

For a printed prototype, print the faceplate separately and use a thin mounting
land or a small metal insert for the toggle rather than assuming its nut clears
the full printed wall.

## Open questions

- JLCPCB assembly sourcing for `6CJ1NOPR` — unverified.
- NKK MN12LL4G01 full panel cutout and max panel thickness, from the current
  drawing (nominal is Ø6.5 mm).
- ANO wheel opening diameter and standoff height — set from the test coupon.
- Whether 3.6 N is acceptable, or the build moves to the C&K KSC at ~2 N with a
  new footprint and plunger.
- How `AIRPLANE` is read and enforced in software, and what drives the
  confirmed-off LED. Relates to uplink recovery in [handoff.md](handoff.md).
