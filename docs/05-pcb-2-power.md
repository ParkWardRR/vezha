# 05 · PCB 2 — Power Board

A custom carrier board in Enclosure B that mounts three modules and wires them
into one controlled power chain.

Read [01-architecture.md](01-architecture.md) first.

> [!NOTE]
> **This supersedes the earlier version of this document,** which said the
> power board was blocked on measurement with no architecture chosen. The
> architecture is now settled: RotoPD Pro → Pololu → detachable connector,
> with a Pico 2 as controller. Measurement is still required to *validate* it,
> but layout can begin.

## What the board is

A carrier. It does not implement PD or regulation itself — it mounts modules
that do, and provides the interconnect, the control wiring, and the mechanical
anchor.

| Module | Function |
|---|---|
| **CentyLab RotoPD Pro** | Negotiates a PD contract with the external USB-C charger; provides a **switched** output |
| **Raspberry Pi Pico 2** (non-wireless) | Controller. Talks to the RotoPD Pro over 3.3 V I²C, gates the router rail |
| **Pololu D42V55F5** (#5571) | Steps the negotiated PD voltage down to **regulated 5 V** |

## Power chain

```
external USB-C charger
  → RotoPD Pro        PD negotiation, switched output
  → Pololu D42V55F5   regulated 5 V
  → seam connector    keyed, latching, 5 V + GND only
  → Orange Pi         dedicated USB-C power input
```

### Control topology

The Pico is **a controller beside the path, not a load inside it.**

- **Pico ← RotoPD Pro auxiliary 5 V output, into VSYS.** Not the Pololu rail.
- **Pico ↔ RotoPD Pro over 3.3 V I²C**, via Qwiic/STEMMA QT or the
  corresponding pins.

## Three rules that must survive layout

> [!CAUTION]
> **1 · Do not power the Pico from the Pololu rail.**
> The Pico may be required to help bring that rail up. A controller that
> depends on the rail it controls cannot start the system.

> [!CAUTION]
> **2 · The auxiliary output is 0.4 A continuous.**
> It powers the controller. It is **not** a source for the Orange Pi, and not
> somewhere to hang additional loads without re-checking the budget.

> [!CAUTION]
> **3 · The Pico verifies an adequate PD contract before enabling the router
> rail.** Bringing the Orange Pi up on an insufficient contract is the exact
> failure this architecture exists to prevent. Sequencing is a firmware
> requirement, but it constrains the board: the enable path must be under Pico
> control, not hard-wired.

## Carrier wiring

| Net | Requirement |
|---|---|
| RotoPD switched output → Pololu VIN/GND | Main power path. **Use both sets of the Pololu's duplicated VIN, VOUT and GND pins** — do not rely on a single generic header contact. |
| Pololu VOUT → seam connector | Full router current. Conductor sizing and connector rating both matter here. |
| RotoPD aux 5 V → Pico VSYS | Controller supply only. |
| Pico ↔ RotoPD I²C | 3.3 V. Check pull-ups once both are populated. |
| Pico enable → RotoPD switched output | The gating path for rule 3. |

## Headroom is not proven

| Figure | Standing |
|---|---|
| Orange Pi 5 Plus | Specifies **5 V at 4 A** |
| Pololu D42V55F5 | **6 A is a *typical maximum*** — not a guarantee, and not inside a sealed compact enclosure |
| RotoPD aux output | **0.4 A continuous**, controller only |

The margin between a 4 A requirement and a 6 A typical maximum is thinner than
it looks once enclosure temperature is included. **It is not validated.**

## Measurement, before trusting any of this

Measure voltage **at the Orange Pi** — not at the regulator, not at the
charger. Cable and connector drop at several amps is the failure mode.

Record under all three conditions:

1. **Cold boot** — the inrush case
2. **Both radios active**, passing traffic simultaneously on 5 GHz
3. **Intended USB load applied**

Also confirm which PD profiles the chosen charger or bank *actually* offers,
from the device itself rather than its marketing copy.

## What this board has to power

| Load | Notes |
|---|---|
| Orange Pi 5 Plus (RK3588) | 5 V at 4 A specified |
| 2 × M.2 Wi-Fi cards | **Both transmitting at once** is the worst case and the one most likely to be under-budgeted |
| Storage | eMMC discussed, unconfirmed |
| Display | Optional touchscreen adds to the budget |
| USB peripherals | Unquantified |
| PCB 1 indicators | Four RGB LEDs off the 5 V rail — small, not zero |

## Open questions

- **RotoPD Pro mounting pattern, outline, and height** — blocks the carrier
  footprint and the enclosure
- Pico mounting: castellated-edge solder vs. 2.54 mm sockets
- Seam connector part
- Actual measured system draw — still unmeasured
- Regulator thermal path at sustained current
- Whether an internal cell is added, and the charge management that would need
- Firmware: PD contract validation thresholds and the enable sequence

Mechanical context in [03-enclosure-b-lower.md](03-enclosure-b-lower.md).
