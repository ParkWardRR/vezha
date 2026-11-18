# 05 · PCB 2 — Power Board

A custom carrier in [Enclosure B](03-enclosure-b-lower.md) that mounts three
modules, drives a small console, and gates power to the router.

Read [01-architecture.md](01-architecture.md) first.

## What the board is

A carrier plus a power-sequencing controller. It does not implement PD or
regulation itself — it mounts modules that do, and provides interconnect,
control wiring, a front-panel console, and the mechanical anchor.

| Module | Function |
|---|---|
| **CentyLab RotoPD Pro** | Negotiates a PD contract over its **built-in USB-C jack**; provides switched VBUS |
| **Raspberry Pi Pico 2** | Controller. Sequences the rail, drives the console, talks to the router |
| **Pololu D42V55F5** (#5571) | Steps negotiated VBUS down to **regulated 5 V @ 4 A** for the Orange Pi |
| **Adafruit 5297 OLED** | Front-panel display |
| **Alps Alpine EC11E15244B2** | Front-panel push encoder, 30 detents |
| **HRO TYPE-C-31-M-12** (`C165948`) | Side-facing 5 V accessory output |

## Module interfaces

### CentyLab RotoPD Pro

- **Use its built-in USB-C jack as the PD input.** No separate input
  receptacle on PCB 2 — bring the RotoPD's own jack to the enclosure wall.
- Route **negotiated VBUS and ground to the buck's VIN/GND.**
- **SDA/SCL to the Pico.**

### Raspberry Pi Pico 2 (non-wireless)

- **Keep the USB port accessible for programming.** Bring it to a wall opening
  or it is access in name only.
- **Reserve an unpopulated 3-pin footprint (TX, RX, GND).** Telemetry across
  the seam is **dropped** — the seam is USB-C power only. The footprint keeps
  it a cable job rather than a respin if it is wanted later.
- **The Pico and display boot before the Orange Pi.** This is a sequencing
  requirement, not a preference.
- Powered from the **RotoPD auxiliary 5 V into VSYS** — see
  [the three rules](#three-rules-that-must-survive-layout).

### Pololu D42V55F5

- Supplies **5 V / 4 A to the Orange Pi** through a **dedicated keyed 2-pin
  power connector.**
- **EN and PG both interface to the Pico.**
- **The buck defaults off at startup.**

> [!CAUTION]
> **"Defaults off" is a layout requirement, not firmware.** The Pico's GPIO is
> high-impedance at reset, so **EN needs a pull-down to ground** on the board.
> Without it the rail state during Pico reset is undefined, and the router can
> come up before any PD contract has been validated.
>
> **PG is an input to the Pico** — it is how firmware confirms the rail
> actually came up, rather than assuming it did after asserting EN.

### Adafruit 5297 OLED

- **4-pin JST-SH STEMMA QT / Qwiic cable: 3.3 V, GND, SDA, SCL.**
- **Use the Pico's second I²C bus** — keeps the console off the bus that talks
  to the RotoPD Pro, so a wedged display cannot block PD control.

### Alps Alpine EC11E15244B2

- Push encoder, **30 detents**.
- **Keyed 4-pin harness: A, B, push switch, GND.**
- A, B and the switch need pull-ups and debouncing — RC on-board or internal
  pull-ups plus firmware debounce. Decide before layout; the RC parts need
  footprints.

## Accessory USB-C output port

Side-facing, **power only**, 5 V. Part is HRO `TYPE-C-31-M-12`, JLCPCB
`C165948`.

> [!CAUTION]
> **Do not connect this port to raw PD VBUS.** VBUS may be at 9, 12, 15 or
> 20 V depending on the negotiated contract. Putting that on a port a user
> plugs a phone into destroys the phone.

### Requirements

- **USB-C source detection** — Rp pull-ups on **both CC1 and CC2** (the
  receptacle is reversible, so both must be presented). Apply VBUS only after
  a sink's Rd is detected.
- **Current limiting** — a load switch or eFuse with a defined limit, not just
  a fuse.
- Verify the receptacle's actual pin count and footprint from the HRO drawing
  before layout.

### Proposed current limit

Here is the analysis behind the recommendation.

| Scenario | Total on the 5 V rail | As % of the buck's 6 A figure |
|---|---|---|
| Orange Pi alone | 4.0 A | 67 % |
| Pi + 0.5 A accessory | 4.5 A | 75 % |
| Pi + 0.9 A accessory | 4.9 A | 82 % |
| Pi + 1.5 A accessory | 5.5 A | 92 % |
| Pi + 3.0 A accessory | 7.0 A | **117 % — over** |

That table flatters the design, because **6 A is a *typical maximum*, not a
rating in a sealed printed box with no airflow:**

| Derating of the 6 A figure | Usable cap | Headroom above the Pi's 4 A |
|---|---|---|
| 90 % | 5.4 A | +1.4 A |
| 80 % | 4.8 A | +0.8 A |
| 70 % | 4.2 A | +0.2 A |
| **60 %** | **3.6 A** | **−0.4 A — short of the Pi alone** |

> [!WARNING]
> **At 60 % derating the buck cannot supply the Orange Pi by itself.** The
> accessory port is not the first thing at risk here — the router rail is.
> This is unmeasured, and it is the single most important measurement on this
> board.

### Recommendation: give the accessory port its own regulator

**Yes — the accessory port needs its own regulator.** Feed a small dedicated
buck from PD VBUS, in parallel with the Pololu, rather than tapping the 5 V
router rail.

Four reasons:

1. **The margin being spent is unmeasured.** Adding a second variable load to
   a rail whose real capacity is unknown spends headroom that may not exist.
2. **Fault isolation.** A shorted or inrushing accessory on a shared rail
   causes a voltage dip *before* any limiter reacts. On the router rail, that
   is an unplanned reboot. A separate regulator contains it.
3. **Thermal separation.** Two converters each running moderately warm is a
   better thermal outcome in a sealed box than one running hard.
4. **It costs almost nothing extra.** "Do not connect to raw PD VBUS" already
   requires conversion or switching between VBUS and the port. Making that a
   dedicated buck rather than a load switch buys isolation for a handful of
   parts.

**Proposed figures for the dedicated regulator:**

| Parameter | Value |
|---|---|
| Advertised | **5 V @ 1.0 A** — Rp for Default USB (**56 kΩ ±20 %** to 5 V on CC1 and CC2) |
| Current limit | **~1.25 A** — trips *above* the advertised value, not at it |
| Raise to 1.5 A? | Only with **22 kΩ ±5 % Rp** and after the thermal measurement below |

**If a dedicated regulator is rejected** and the port must share the router
rail: hard-limit it to **0.5 A**, advertise Default USB, and treat it as a
trickle-charge port only — and do not do even that until the Pololu's real
derated capacity in the closed enclosure has been measured.

## Three rules that must survive layout

> [!CAUTION]
> **1 · Do not power the Pico from the Pololu rail.** The Pico brings that
> rail up; a controller that depends on its own output cannot start the
> system. Pico runs off the **RotoPD auxiliary 5 V into VSYS.**

> [!CAUTION]
> **2 · The auxiliary output is 0.4 A continuous.** It powers the controller
> and the console. It is **not** a source for the Orange Pi, and the OLED and
> encoder must fit inside that budget.

> [!CAUTION]
> **3 · The Pico verifies an adequate PD contract before asserting EN.**
> Bringing the Orange Pi up on an insufficient contract is the failure this
> architecture exists to prevent. The buck defaults off; the Pico confirms the
> contract, asserts EN, then checks PG.

## Boot sequence

```
power applied
  → RotoPD Pro negotiates PD contract
  → aux 5 V brings up Pico 2 + OLED          ← console is live first
  → Pico reads contract over I²C bus 1
  → contract adequate?  ── no ──→ report on OLED, leave EN low
            │ yes
  → Pico asserts buck EN
  → Pico checks PG                            ← confirms, not assumes
  → USB-C source: sink Rd detected?  ── no ──→ hold VBUS off
            │ yes
  → 5 V reaches Orange Pi over the USB-C seam
  → Orange Pi boots independently              ← no telemetry link
```

## Connectors

| Connector | Pins | Carries | Keyed |
|---|---:|---|---|
| **Seam output** | — | 5 V, GND over **USB-C** — power only | By the standard |
| OLED | 4 | 3.3 V, GND, SDA, SCL (JST-SH STEMMA QT) | Yes, by type |
| Encoder | 4 | A, B, push switch, GND | **Yes** |
| RotoPD I²C | — | SDA, SCL to Pico bus 1 | — |

> [!IMPORTANT]
> **The seam is USB-C, 5 V power only.** No signal, no detect pin, no custom
> contact array. USB-C source detection on the output — Rp on CC1/CC2, VBUS
> only after a sink's Rd appears — does the gating a detect contact would have.
>
> **Caveat:** USB-C tops out at **3 A at 5 V** and the Orange Pi is specified
> at 4 A. See [01 · The 3 A problem](01-architecture.md#the-3-a-problem).

## I²C bus allocation

| Bus | Devices | Rationale |
|---|---|---|
| **Bus 1** | RotoPD Pro | Power control. Must not be blocked by UI traffic. |
| **Bus 2** | Adafruit 5297 OLED | Console. A wedged display must not stall PD control. |

Check pull-ups on each bus once populated — the RotoPD and the STEMMA QT
cable may both carry their own.

## Headroom summary

| Figure | Standing |
|---|---|
| Orange Pi 5 Plus | **5 V at 4 A** specified |
| Pololu D42V55F5 | **6 A typical maximum** — unvalidated in enclosure |
| RotoPD auxiliary | **0.4 A continuous** — Pico + OLED + encoder only |
| Accessory port | **1.0 A proposed**, on its own regulator |

## Measurement, before trusting any of this

Measure voltage **at the Orange Pi** — not at the regulator, not at the
charger. Cable and connector drop at several amps is the failure mode.

1. **Cold boot** — the inrush case
2. **Both radios active**, passing traffic simultaneously on 5 GHz
3. **Intended USB load applied**
4. **Buck case temperature in the closed enclosure at sustained 4 A** — this
   produces the real derating figure and decides whether the accessory port is
   viable at all

Also confirm which PD profiles the chosen charger actually offers, from the
device rather than its marketing copy.

## Previously-flagged conflicts — both resolved

**1 · Seam is no longer power-only** — **resolved.** The UART is dropped; the
seam is USB-C, 5 V power only. The governing rule in
[01](01-architecture.md) holds again as written.

**2 · Two competing user interfaces** — **resolved**, as a side effect of the
above. With no telemetry link, this board's OLED can only show power and PD
state, so it cannot substitute for a router UI. The split is clean:

| | Interface | Shows |
|---|---|---|
| **Enclosure A** | 4.26" e-paper, ANO wheel, three keys — see [10](10-display.md) | Router state |
| **Enclosure B** | OLED + EC11 encoder | Input voltage, negotiated PD contract, rail status, fault reason |

## Open questions

- RotoPD Pro mounting pattern, outline, height — still blocking
- Dedicated accessory regulator part
- Seam USB-C receptacle part, and whether the Pi stays under 3 A
- Encoder debounce: RC on board vs. firmware
- Measured buck derating in the closed enclosure
- Pico mounting: castellated vs. 2.54 mm sockets

Mechanical context in [03-enclosure-b-lower.md](03-enclosure-b-lower.md).
