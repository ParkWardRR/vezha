# 02 · Enclosure A — Upper Router Box

The router itself. Holds the Orange Pi, both radios, the adapter, all four
antennas, storage, the display, and the removable faceplate.

Read [01-architecture.md](01-architecture.md) first.

> [!WARNING]
> No dimension here is a verified installed measurement. The board and card
> sizes are published figures for the bare parts. **Heatsink, adapter, mated
> antenna plugs, and cable bends are all excluded** and are exactly what will
> decide whether this closes.

## Contents and mounting

| Part | Dimensions | Mounting and clearance |
|---|---|---|
| **Orange Pi 5 Plus** | 100 × 75 mm board | On enclosure standoffs. **Clearance required on both faces** — E-key socket on top, M-key socket underneath. Published size excludes installed heatsink, adapter, and cable bends. |
| **Intel AX210** (uplink) | M.2 2230 · 22 × 30 × 2.4 mm | Slides into the **top-side E-key socket**, screws down at the 2230 standoff. Two MHF4 antenna leads snap onto the card. Wi-Fi over PCIe, Bluetooth over USB. |
| **Second Wi-Fi card** (private AP) | 22 × 30 mm **if 2230** — height unconfirmed | Mounts in the **adapter's** E-key socket with its own retaining screw. MT7922/RZ616 is a candidate, **not a locked part.** Verify antenna connector type and 5 GHz AP operation on the target Linux image before committing. |
| **M-key → E-key adapter** | **Installed size unverified** | Male M-key edge into the Orange Pi's **underside** socket; second radio into the adapter's female E-key socket. The host accepting 2280 modules does **not** tell you the adapter's size or the installed stack height. Choose a specific adapter **that routes PCIe**, then measure it with card and antenna plugs installed. |
| **4 × flex antennas** | 42 × 7 mm each, 100 mm MHF4 lead | Inside the narrow walls. Full placement in [06-antennas.md](06-antennas.md). |
| **Storage** | eMMC discussed, unconfirmed | — |
| **Display** | Model not chosen | **Own bracket.** Pressing a button must not flex the display mount or load its ribbon. |
| **Faceplate** | Separate removable part | Carries toggle, three keys, ANO wheel, four RGB windows. See [04-pcb-1-front-control.md](04-pcb-1-front-control.md). |
| **PCB 1** | Outline TBD | On standoffs parallel to the faceplate, behind it. One keyed detachable harness to the Orange Pi. |

## The double-sided problem

The single most important mechanical fact about this build:

> **One radio sits above the Orange Pi, the other hangs below it on an
> adapter.** The board cannot be mounted flat against a floor or a lid.

Standoff height has to account for the underside stack — adapter, plus card,
plus mated antenna plugs, plus the bend radius of the coax leaving them. That
figure is unmeasured and is one of the
[three dimensions nobody should guess](01-architecture.md#the-three-dimensions-nobody-should-guess).

## Antenna zones

Summarised here; full detail and test plan in [06-antennas.md](06-antennas.md).

- Four strips **inside the narrow walls** — top edge, upper-right sidewall,
  lower-left sidewall, bottom edge
- Broad screen and back faces stay **clear**
- Flat landing pad of plain plastic for each; 2 mm ABS is the reference wall
- Target roughly **20 mm from the main ground plane** where practical — a
  layout target, not a pass/fail spec
- **Not** directly behind display, battery, or heatsink
- **No carbon-filled filament** anywhere in an antenna zone

### Lead routing is a layout input, not an afterthought

The leads are **100 mm**. Mock up all four **before** fixing board and antenna
positions — they may not reach every corner from where the cards actually sit,
and the two radios are on opposite faces of the board.

Check that **the lid opens without tugging on the MHF4 connectors.** Those are
tiny and they are the thing that will break during service.

## Faceplate and seam

- Faceplate is its **own part**, removable
- **Display opening separate from control openings** — a display change must
  not force a new button PCB
- `AIRPLANE` toggle clamps **through the faceplate** with its bushing and nut,
  leads running to PCB 1. For a printed prototype use a thin mounting land or
  a metal insert — do not assume the nut clears the full printed wall
- RGB light exits through **flush diffusers above each label**, with opaque
  walls between indicators. Keycaps stay opaque, no glow around the cap

## Power entry

Enclosure A receives **5 V, ground, and UART telemetry** from Enclosure B
through **one combined 7-contact connector** at the seam. A short lead runs
from the power contacts to the Orange Pi's **dedicated USB-C power input**,
and from TX/RX to the Pi's UART pins.

Full contact map, staggering and safety rules:
[01 · Crossing the seam](01-architecture.md#crossing-the-seam).

**Mechanical consequences for this shell:**

- **Spring pins live on this side**, flat pads on Enclosure B — Enclosure A
  has no power source of its own, so its pins are dead metal when detached
- **The enclosure latch retains the boxes, not the connector**
- A **DETECT contact is tied to GND inside this box.** That is how Enclosure B
  knows it is safe to energise the rail — so this shell must guarantee the
  contact is made whenever the boxes are latched
- Size the case around the **mated pair with its cable**, not the footprint

**No RF crosses the seam** — the power box must come off without disturbing
any PCIe or antenna connection.

## Thermal

Unresolved and untested. The stated preference is hardware that does not need
dedicated cooling, but **two Wi-Fi 6E radios under simultaneous sustained
load is exactly the case nobody has measured.** A heatsink exists in the
clearance budget above; whether it is sufficient is open.

Antenna zones and heatsink placement are in direct tension. Resolve it with
the RF test in [06-antennas.md](06-antennas.md) rather than by assumption.

## Open questions

- Installed stack height on the underside (adapter + card + mated plugs)
- Which M-key-to-E-key adapter, confirmed to route PCIe
- Second radio part, form factor height, and antenna connector type
- Display model and bracket geometry
- Heatsink size and whether active cooling is needed
- PCB 1 outline and standoff height — the latter is set by the RGB optics,
  see [04-pcb-1-front-control.md](04-pcb-1-front-control.md)
- Whether the faceplate's replaceable top cap concept survives, kept as the
  fallback for swapping the uplink antennas
