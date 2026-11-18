# Vezha — PCB 2: Power Board

Status: **requirements only.** No value in this document has been measured or
validated. There is no schematic, no converter selection, and no battery
decision. This exists so the power board can be scoped — not built.

> [!CAUTION]
> **Do not design to the numbers below.** The only hard figure anyone has
> quoted is a 5 V / 5 A bench-supply *target*, and that was a sizing guess, not
> a measurement of this system. The real current budget comes from step 1 of
> [Work order](#work-order).

## Function

PCB 2 lives in **Enclosure B** (the detachable lower power box). It:

1. Accepts USB-C input and **negotiates a suitable higher-voltage PD profile**
2. Converts that down to **regulated 5 V** for the board in Enclosure A
3. Delivers it across the **box-to-box interconnect**

That interconnect carries **power only**. Enclosure A must not depend on
Enclosure B for anything else — no data, no control, no indicators.

## What it has to power

The complete build, all at once:

| Load | Notes |
|---|---|
| Orange Pi 5 Plus (RK3588) | Base SBC load |
| 2 × M.2 Wi-Fi cards | **Both radios transmitting simultaneously** is the worst case, and the one most likely to be under-budgeted |
| Storage | eMMC discussed, unconfirmed |
| USB peripheral load | Unquantified |
| Display | Optional touchscreen adds to the budget |
| PCB 1 indicators | Four RGB LEDs off the 5 V rail — small, but not zero |

## Known candidates, none validated

| Item | Candidate | Standing |
|---|---|---|
| Supply target | Regulated 5 V / 5 A | A **supply-sizing target**, not measured consumption. Do not treat as the requirement. |
| Converter | Geekworm Pi5-5V5APD | Discussed as a candidate. Not validated in this build. |
| Battery | Anker 10,000 mAh PowerIQ | **Exact model and PD output profiles unconfirmed.** Advertised wattage and capacity do **not** establish that it can power the finished unit. |
| USB-C receptacle | [C3445864](parts-sourcing.md#c3445864--usb-c-receptacle) — GCT USB4120-03-C | Looked up, not selected. |

> [!WARNING]
> The C3445864 receptacle is rated **48 V / 5 A at the contacts.** That is a
> connector rating, **not** a PD capability. Negotiating above 5 V / 3 A still
> requires a PD sink controller, and 5 A specifically requires an e-marked
> cable. Do not read the connector's rating as a power budget.

## Work order

Design work on this board is **blocked** until the measurements exist.

1. **Measure the real load.** Instrument the assembled upper box and record
   current draw at the board under: cold boot, both radios passing traffic
   simultaneously, and USB load applied. This produces the actual budget.
2. **Verify the PD source.** Confirm which PD profiles the chosen bank
   actually offers — from the device, not its marketing copy.
3. **Measure voltage at the board**, not at the supply, under each of the
   conditions in step 1. Cable and connector drop at several amps is the
   failure mode here.
4. **Then** select the converter and size the board.
5. **Then** test battery runtime, which determines the battery, which
   determines the size of Enclosure B.

Enclosure B's dimensions are an **output** of this process, not an input.
It cannot be modelled until at least step 5.

## Interconnect requirements

- **Detachable** — Enclosure B separates from A as a normal operation
- **Keyed** — must not be connectable backwards
- **Power only** — no data or control crosses the boundary
- Must carry the full worst-case current with acceptable drop, measured at the
  receiving end in Enclosure A
- Mechanical retention is an enclosure problem, not solved by the connector
  alone

## Open questions

- Actual system current draw — **everything else depends on this**
- PD profile to negotiate, and the sink controller to do it
- Converter selection
- Battery model, chemistry, and whether it is an off-the-shelf bank or an
  internal cell with its own charge management
- Charging behaviour: does the unit run while charging, and from the same port?
- Box-to-box connector selection
- Thermal behaviour of the converter under sustained load
- Runtime target — no figure has been set

See [handoff.md](handoff.md#power-and-portability) for how this sits in the
wider project.
