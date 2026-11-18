# 03 · Enclosure B — Lower Power Box

Detachable. Holds **PCB 2** and nothing else of consequence: the power chain
that turns an external USB-C PD supply into regulated 5 V for the router.

Read [01-architecture.md](01-architecture.md) first.

> [!NOTE]
> **This supersedes the earlier "battery box" framing.** The current
> architecture takes power from an **external USB-C charger or bank**. Whether
> a cell ever lives inside this enclosure is an open question, not a
> requirement. Do not reserve volume for a battery without deciding that first.

## Contents

| Part | Dimensions | Mounting |
|---|---|---|
| **CentyLab RotoPD Pro** | **Outline, height, and mounting pattern all unverified** | **USB-C input at the enclosure wall.** Switched PD output to the Pololu's VIN/GND. Pico connects over 3.3 V I²C via Qwiic/STEMMA QT or the corresponding pins. Use the [vendor PCB files](https://github.com/CentyLab/RotoPD_Pro) or measure the actual board before drawing its carrier footprint. |
| **Raspberry Pi Pico 2** (non-wireless) | 51 × 21 × 1 mm bare PCB | Two options — see below. |
| **Pololu D42V55F5** (#5571) | 25.4 × 25.4 × 9 mm | Use [Pololu's drawing](https://www.pololu.com/product/5571) for the 2.54 mm through-hole pattern and the **three M2 mounting holes.** |
| **Seam connector** | TBD by selection | Keyed, latching, 5 V/GND, rated for full load. |

## Pico 2 mounting — pick one, it changes the height

| Option | How | Trade-off |
|---|---|---|
| **Low profile** | Solder the **castellated edges** directly to PCB 2 | Minimum stack height. Pico is not replaceable. |
| **Replaceable** | Two 20-pin rows of **2.54 mm** headers and sockets | Taller. Pico can be swapped or removed. |

If programming access is wanted in situ, **leave room for the overhanging
Micro-USB port** — and bring it to a wall opening or it is access in name only.

## Pololu wiring rule

The D42V55F5 duplicates its VIN, VOUT, and GND pins.

> **Use both sets of the duplicated pins in the carrier layout.** Do not rely
> on a single generic header contact to carry the main power path.

This is the full router current. A single 2.54 mm contact is not the place to
find out what its real rating is.

## Power chain through this box

```
USB-C wall input
  → RotoPD Pro            negotiates PD, provides switched output
  → Pololu D42V55F5       regulated 5 V
  → seam connector        keyed, latching
  → Enclosure A
```

The **Pico 2 is beside this path, not in it.** It talks to the RotoPD Pro over
I²C and gates the router rail.

> [!CAUTION]
> **Power the Pico from the RotoPD Pro's auxiliary 5 V output into VSYS — not
> from the Pololu rail.** The Pico may be needed to help bring that rail up, so
> it cannot depend on it. That auxiliary output is **0.4 A continuous**: it is
> for the controller, never for the Orange Pi.

## Enclosure sizing

Three measurements gate this box, and only one of them is about a PCB:

1. **RotoPD Pro outline, height, and mounting pattern** — unverified, and it
   is the part whose footprint is least knowable from the datasheet
2. **Mated seam connector clearance** — connector *and* cable bend, not the
   footprint
3. **Pico mounting choice** — castellated vs. socketed changes the stack

Draw this enclosure around the **mated** hardware. PCB footprints alone will
produce a box that does not close.

## USB-C input

The RotoPD Pro's USB-C input sits at the enclosure wall. Points to settle:

- Whether the receptacle is the RotoPD's own, brought to a wall cutout, or a
  panel-mount part wired to it
- Cable strain relief — this is the connector a handheld device gets yanked by
- [C3445864](08-sourcing.md#c3445864--usb-c-receptacle) was looked up as a
  candidate receptacle. **Its 48 V / 5 A rating is a contact rating, not a PD
  capability.** It is not selected.

## Thermal

The Pololu is a switching regulator in a small sealed box, potentially at
several amps. Its **6 A figure is a typical maximum, not a guarantee in a
compact enclosure.** Allow for airflow or a thermal path, and measure under
sustained load before closing the design.

## Open questions

- RotoPD Pro physical envelope and mounting — **blocking**
- Seam connector selection
- Pico mounting style
- Whether an internal cell is ever added, which would change this box entirely
- Charging behaviour: does the unit run while the bank is charging, through
  the same port?
- Regulator thermal path under sustained load
- PCB 2 outline — an output of the above, not an input

Full electrical requirements are in [05-pcb-2-power.md](05-pcb-2-power.md).
