# 03 · Enclosure B — Power Module

Detachable. Holds **the power board** and nothing else of consequence: the power chain
that turns an external USB-C PD supply into regulated 5 V for the router.

Read [01-architecture.md](01-architecture.md) first.

> [!IMPORTANT]
> **It mounts on the back, not underneath — changed 2026-11-23.** This
> document still calls it the "lower" box throughout, and the filename still
> says so. **Enclosure A's bottom is now a closed, stable foot**, so the
> module moved to Enclosure A's **rear face**.
>
> **What does not change:** it is still detachable, still carries exactly the
> same contents, and **still only 5 V over USB-C crosses between the two
> boxes.** Every electrical decision in here stands.
>
> **What does change:** the seam cable route and the module's mounting
> interface to Enclosure A's rear face.

> [!NOTE]
> **This supersedes the earlier "battery box" framing.** The current
> architecture takes power from an **external USB-C charger or bank**. Whether
> a cell ever lives inside this enclosure is an open question, not a
> requirement. Do not reserve volume for a battery without deciding that first.

## Contents

| Part | Dimensions | Mounting |
|---|---|---|
| **CentyLab RotoPD Pro** | **24.40 × 35.80 mm**, 2 × M2.5 (⌀2.7 mm) 18.00 mm apart. Assembly spans 13.00 mm; **4.70 mm** once the screw terminal is removed. [Full geometry](06-power-board-schematic.md#u1--rotopd-pro-mechanical--resolved-from-the-vendor-repo) | **USB-C input at the enclosure wall.** Switched PD output to the Pololu's VIN/GND. Pico connects over 3.3 V I²C via Qwiic/STEMMA QT or the corresponding pins. Use the [vendor PCB files](https://github.com/CentyLab/RotoPD_Pro) or measure the actual board before drawing its carrier footprint. |
| **Raspberry Pi Pico 2** (non-wireless) | 51 × 21 × 1 mm bare PCB | Two options — see below. |
| **Pololu D42V55F5** (#5571) | 25.4 × 25.4 × 9 mm | Use [Pololu's drawing](https://www.pololu.com/product/5571) for the 2.54 mm through-hole pattern and the **three M2 mounting holes.** |
| **Seam output** | USB-C receptacle, part TBD | **5 V power only** to Enclosure A. Recessed contacts, so no exposed-metal hazard when detached. |

## The VBUS screw terminal

**Decided 2026-11-18: remove it, and solder heavy wire to its pads.**

[06 · U1](06-power-board-schematic.md#u1--rotopd-pro) establishes that the
RotoPD Pro's switched VBUS output leaves on a **2-position 5 mm screw
terminal** on the edge opposite the USB-C jack, and calls it "an assembly and
enclosure constraint, not just a schematic one". It was the tallest thing on
the board, at roughly 10 mm above the module.

Why remove rather than keep:

- That path is `VBUS_PD` — **up to 5 A at up to 48 V**. A screw terminal is
  the worse joint for it in a device defined by being carried around:
  vibration and thermal cycling are exactly what loosens one. A soldered
  joint is not.
- **It is never field-disconnected.** Removing the module means desoldering
  it from its header anyway, so the terminal buys no serviceability it does
  not already have.
- It was setting this box's height on its own.

**Cost of the decision:** the terminal has to come off before the module is
mounted, and a quick module swap is foreclosed. Both are acceptable on a
carrier the module is soldered to regardless.

**Measure the module with the terminal already removed** — see
[10](10-measurement-protocol.md). Measuring it fitted records ~10 mm that
will not exist.

## Pico 2 mounting — pick one, it changes the height

| Option | How | Trade-off |
|---|---|---|
| **Low profile** | Solder the **castellated edges** directly to the power board | Minimum stack height. Pico is not replaceable. |
| **Replaceable** | Two 20-pin rows of **2.54 mm** headers and sockets | Taller. Pico can be swapped or removed. |

If programming access is wanted in situ, **leave room for the overhanging
Micro-USB port** — and bring it to a wall opening or it is access in name only.

## The console — decided

**Decided 2026-11-18: Enclosure B keeps the OLED and the push encoder.**

This was a live contradiction, not just an unknown.
[01](01-architecture.md#no-controls-in-v1) asserts that B "carries the only
panel" and treats the console as settled by the v1 scope cut, while this
document and [06](06-power-board-schematic.md) both still listed it as open
and **blocking**. It is resolved in favour of 01.

Consequences, all of which were already specified and are now simply live:

- **J4 (OLED, 4-pin JST-SH) and J5 (encoder) exist** and stay populated.
- **I²C0 is the OLED's bus.** 06 allocates it deliberately: I²C1 is
  rail-critical and carries PD control plus the current measurement the
  shutdown decision depends on, so a wedged display cannot stall it.
- **The encoder RC is populated** — 10 kΩ / 1 kΩ / 100 nF per channel, the
  values [SIM-05](06-power-board-schematic.md#sim-05--encoder-debounce)
  fixes, plus a Gray-code decoder in firmware.
- **This box's lid needs openings** for the display window and the encoder
  shaft, and its height now has to clear the encoder — which, with the
  [screw terminal removed](#the-vbus-screw-terminal), is the tallest thing
  above the board.

Still to choose: the OLED module itself, its bracket, and the encoder knob.
[01](01-architecture.md) cites the Adafruit 5297's 20.076 × 20.076 mm active
area in its scope-cut reasoning; that is a reference point, not a committed
part.

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
  → USB-C receptacle      5 V power only
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
2. **Mated USB-C plug clearance** — plug *and* cable bend, not the
   receptacle footprint
3. **Pico mounting choice** — castellated vs. socketed changes the stack

Draw this enclosure around the **mated** hardware. PCB footprints alone will
produce a box that does not close.

## Wall openings

This box has **four** things reaching a wall, not one. All four constrain the
shell before the power board's outline does.

| Opening | Part | Face |
|---|---|---|
| **PD input** | RotoPD Pro's **own built-in USB-C jack** | Input end |
| **Accessory output** | HRO TYPE-C-31-M-12 | **Side**-facing |
| **Programming** | Pico 2 Micro-USB, overhanging | Wherever the Pico lands |
| **Console** | OLED window + encoder shaft | **Front panel** |

### PD input

**Resolved:** the RotoPD Pro's **built-in USB-C jack is the PD input.** There
is no separate input receptacle on the power board — bring the module's own jack to the
wall. That fixes the RotoPD's position relative to the shell, so its
unverified outline now constrains the enclosure in two ways at once.

Cable strain relief still matters — this is the connector a handheld device
gets yanked by.

> [!NOTE]
> [C3445864](08-sourcing.md#c3445864--usb-c-receptacle) is **no longer a
> candidate for the input.** The RotoPD's own jack supersedes it.

### Accessory output

Side-facing, **5 V power only**, on its **own regulator** — never raw PD
VBUS, which can be at 20 V. Electrical requirements and the proposed 1.0 A
limit are in [05-power-board.md](05-power-board.md#accessory-usb-c-output-port).

### Front-panel console

> [!WARNING]
> **Unresolved:** whether this console is *additional to* the controls in
> Enclosure A, or *replaces* them. See
> [05 · Unresolved conflicts](05-power-board.md#previously-flagged-conflicts--both-resolved). Do not
> cut a front panel for either box until this is settled — it decides whether
> Enclosure B has a user-facing face at all.

If it stays: the OLED needs a window and bracket, the encoder needs a bushing
cutout and knob clearance, and both must be reachable with the box attached to
Enclosure A.

## Thermal

The Pololu is a switching regulator in a small sealed box, potentially at
several amps. Its **6 A figure is a typical maximum, not a guarantee in a
compact enclosure.** Allow for airflow or a thermal path, and measure under
sustained load before closing the design.

## Open questions

- ~~RotoPD Pro physical envelope and mounting~~ — **resolved 2026-11-18**
  from the vendor repo's KiCad board and STEP assembly. No longer blocking.
  [Geometry](06-power-board-schematic.md#u1--rotopd-pro-mechanical--resolved-from-the-vendor-repo)
- Seam USB-C receptacle part, and whether the cable is captive
- ~~**Whether Enclosure B has a front panel at all**~~ — **decided
  2026-11-18: YES.** The OLED and encoder stay. J4 and J5 exist, and this
  box carries the only hardware UI in v1, as [01](01-architecture.md) always
  assumed. The contradiction with 06's open list is resolved in favour of
  01.
- Accessory port regulator, and its thermal contribution in this box
- OLED bracket and encoder knob
- Pico mounting style
- Whether an internal cell is ever added, which would change this box entirely
- Charging behaviour: does the unit run while the bank is charging, through
  the same port?
- Regulator thermal path under sustained load
- Power board outline — an output of the above, not an input

Full electrical requirements are in [05-power-board.md](05-power-board.md).
