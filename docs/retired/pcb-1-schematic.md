# Retired · PCB 1 — Schematic

> [!CAUTION]
> **Retired 2026-11-18. PCB 1 is not built in v1.** Enclosure A is fully
> headless and this board has no contents left to carry. See
> [01 · The v1 scope cut](../01-architecture.md#no-controls-in-v1) and the
> requirements document it came from, [04](pcb-1-front-control.md).
>
> The design is **complete and believed correct** — it was cut for scope, not
> for a fault. Three simulation decks (`sim/11`, `sim/12`, `sim/13`) back it and
> are retired alongside it; their results are preserved in
> [Simulation results](#simulation-results) below.
>
> **The one section still worth reading in v1** is
> [the Orange Pi 5 Plus 40-pin header](#the-orange-pi-5-plus-40-pin-header).
> That pin map was derived from the vendor's own GPIO library rather than
> assumed from Raspberry Pi compatibility, and it stays correct no matter what
> is attached — including the finding that I²C lands on **I²C2, not `i2c-1`**.

---

*Original document follows, unedited.*

## Original: net-by-net schematic for the front control board

Requirements and the reasoning behind each part choice live in
[04-pcb-1-front-control.md](pcb-1-front-control.md); this is the electrical
design that follows from them.

Companion to [11-pcb-2-schematic.md](../06-power-board-schematic.md). Simulation decks
are `sim/11`, `sim/12`, `sim/13`.

> [!NOTE]
> **The host pin map is now resolved** — see [Host interface](#host-interface-j1).
> It came from the vendor's own GPIO library, not from assuming Raspberry Pi
> compatibility. I²C and SPI do land on the Raspberry Pi positions, but **the
> bus numbers differ**, which is the part that would have bitten in software.

## What the board is

A passive-ish front panel: three keys, a panel toggle, an I²C LED driver with
four RGB indicators, and a breakout for the e-paper display. It has **no
regulator and no controller** — every rail arrives from the Orange Pi and every
decision is made by the host.

That is deliberate. The power board is the board that must survive the host being absent;
PCB 1 only exists while the router is up.

## Power domains

| Rail | Source | Used by | Worst-case draw |
|---|---|---|---|
| **+3V3** | Orange Pi header | U1 logic, all pull-ups, display logic | ~15 mA |
| **+5V** | Orange Pi header | **LED anodes only** | **120 mA** (12 ch × 10 mA) |
| **GND** | Orange Pi header | everything | — |

The 5 V rail carries only LED anode current. 120 mA is the all-white
self-test; a realistic status display is one or two indicators, under 30 mA.

> [!NOTE]
> **Tell the power board about the 120 mA.** The seam budget in
> [11](../06-power-board-schematic.md) sizes the router rail. If the indicators were
> assumed negligible, they are not — they are up to 120 mA on the 5 V rail,
> drawn through the same seam.

Why the anodes are on 5 V and not 3.3 V: the chosen LED's green and blue dice
run to **3.6 V** Vf. A 3.3 V rail cannot guarantee full current into them, and
the TLC59116 needs output headroom on top. 5 V is required for blue and green,
and is wasteful for red — which is what sets the current choice below.

## Reference designators

| Ref | Part | LCSC | Package | Stock 2026-11-18 | Function |
|---|---|---|---|---:|---|
| **U1** | TI TLC59116IPWR | `C131194` | TSSOP-28 | 3,611 | 16-ch I²C constant-current LED sink |
| **D1–D4** | MEIHUA MHPA2525RGBDT-S | `C404285` | SMD 2.6 × 2.4 mm | 8,253 | RGB indicators, **common anode**, white frosted |
| **SW1–SW5** | C&K KSC221JLFS | `C221726` | SMD J-lead 6.2 mm | 16,623 | keys — **populate 3, SW4/SW5 are spare footprints** |
| **R1** | **1.87 kΩ** 1 % | — | 0603 | — | U1 `REXT` → 10 mA/channel — [SIM-12](#sim-12--led-driver-dissipation) |
| **R2, R3** | **2.2 kΩ** 1 % | — | 0603 | — | I²C SDA/SCL pull-ups to +3V3 — [SIM-11](#sim-11--ic-pull-ups) |
| **R4** | 10 kΩ | — | 0603 | — | U1 `RESET` pull-up to +3V3 |
| **R5–R8** | 10 kΩ | — | 0603 | — | key / toggle pull-ups to +3V3 |
| **R9–R12** | 1 kΩ | — | 0603 | — | key / toggle series R — [SIM-13](#sim-13--key-debounce) |
| **C1–C4** | **100 nF** X7R | — | 0603 | — | key / toggle RC — [SIM-13](#sim-13--key-debounce) |
| **C5** | 100 nF X7R | — | 0603 | — | U1 VCC decoupling, at the pin |
| **C6** | 10 µF X5R 16 V | — | 0805 | — | +3V3 bulk |
| **C7** | 10 µF X5R 16 V | — | 0805 | — | **+5V bulk, at the LED anodes** |
| **JP1–JP4** | 0 Ω, fitted to GND | — | 0603 | — | U1 A3–A0 address straps |
| **J1** | 2×20 2.54 mm shrouded header | — | TH | — | host interface — the only cable to the SBC |
| **J2** | JST GH `SM09B-GHS-TB(LF)(SN)` | `C265420` | SMD 9P side-entry | 7,140 | e-paper display |
| **J3** | 4-pin JST-SH | — | SMD | — | STEMMA QT to the ANO module |
| **J4** | 1×3 header or JST-PH | — | — | — | `AIRPLANE` toggle leads |

Every placed part is `expand` library, so each adds a JLCPCB feeder fee.

**R1's value is the one to not substitute.** It sets LED current, and 931 Ω —
the value TI's datasheet example uses — overheats the driver in this enclosure.

## Host interface (J1)

One 2×20 IDC ribbon from the Orange Pi's 40-pin header to PCB 1. PCB 1 fans out
to the display, the ANO and the toggle. A point-to-point harness would have
needed ~17 conductors; this uses one standard keyed cable instead.

### The Orange Pi 5 Plus 40-pin header

Source: the vendor's own GPIO library, [`orangepi-xunlong/wiringOP`](https://github.com/orangepi-xunlong/wiringOP)
(`next` branch) — `physNames_5PLUS[]` in `gpio/readall.c` for the functions and
`physToGpio_5PLUS[]` in `wiringPi/wiringPi.c` for the GPIO numbers. **The two
tables are independent and they agree**: every function name matches the
bank/pin derived from its GPIO number. That cross-check is why this is trusted.

| Pin | Function | GPIO | | Pin | Function | GPIO |
|---:|---|---|---|---:|---|---|
| 1 | 3.3 V | — | | 2 | 5 V | — |
| **3** | **I²C2 SDA** | GPIO0_C0 (16) | | 4 | 5 V | — |
| **5** | **I²C2 SCL** | GPIO0_B7 (15) | | 6 | GND | — |
| 7 | PWM14 | GPIO1_D6 (62) | | 8 | GPIO1_A1 | 33 |
| 9 | GND | — | | 10 | GPIO1_A0 | 32 |
| **11** | GPIO1_A4 | 36 | | **12** | GPIO3_A1 | 97 |
| **13** | GPIO1_A7 | 39 | | 14 | GND | — |
| **15** | GPIO1_B0 | 40 | | **16** | GPIO3_B5 | 109 |
| 17 | 3.3 V | — | | **18** | GPIO3_B6 | 110 |
| **19** | **SPI0_TXD** | GPIO1_B2 (42) | | 20 | GND | — |
| 21 | SPI0_RXD | GPIO1_B1 (41) | | **22** | GPIO1_A2 | 34 |
| **23** | **SPI0_CLK** | GPIO1_B3 (43) | | **24** | **SPI0_CS0** | GPIO1_B4 (44) |
| 25 | GND | — | | 26 | SPI0_CS1 | GPIO1_B5 (45) |
| 27 | GPIO1_B7 | 47 | | 28 | GPIO1_B6 | 46 |
| **29** | GPIO1_D7 | 63 | | 30 | GND | — |
| **31** | GPIO3_A0 | 96 | | 32 | GPIO1_A3 | 35 |
| **33** | GPIO3_C2 | 114 | | 34 | GND | — |
| **35** | GPIO3_A2 | 98 | | 36 | GPIO3_A5 | 101 |
| **37** | GPIO3_C1 | 113 | | 38 | GPIO3_A4 | 100 |
| 39 | GND | — | | 40 | GPIO3_A3 | 99 |

**The good news, and the trap.** I²C sits on pins 3/5 and SPI0 on 19/21/23/24 —
the same physical positions as a Raspberry Pi. So Waveshare's Raspberry Pi
wiring for the e-paper HAT maps **pin-for-pin** onto this board, including all
four control pins, which are plain GPIO here. No rewiring.

But the bus *numbers* are not the Raspberry Pi's: this is **I²C2**, not i2c-1.
Code that opens `/dev/i2c-1` will talk to the wrong bus or nothing at all. That
is the part that would have been missed by assuming compatibility.

### Assignment

| Function | Pin | GPIO | Notes |
|---|---:|---|---|
| +3V3 | 1 | — | |
| +5V | 2 | — | LED anodes only |
| GND | 6, 9, 14, 20, 25, 30, 34, 39 | — | use several on the ribbon |
| I²C `SDA` | 3 | GPIO0_C0 | **I²C2**, shared U1 + ANO |
| I²C `SCL` | 5 | GPIO0_B7 | |
| Display `DIN` | 19 | SPI0_TXD | |
| Display `CLK` | 23 | SPI0_CLK | |
| Display `CS` | 24 | SPI0_CS0 | |
| Display `DC` | 22 | GPIO1_A2 | matches Waveshare's RPi map |
| Display `RST` | 11 | GPIO1_A4 | matches Waveshare's RPi map |
| Display `BUSY` | 18 | GPIO3_B6 | **input to host** |
| Display `PWR` | 12 | GPIO3_A1 | must be driven, not tied high |
| `LINK` | 13 | GPIO1_A7 | active low |
| `MAC` | 15 | GPIO1_B0 | active low |
| `★` | 16 | GPIO3_B5 | active low |
| `AIRPLANE` | 29 | GPIO1_D7 | active low |
| U1 `RESET` | 31 | GPIO3_A0 | **output**, active low |
| *(reserved)* `SW4` | 33 | GPIO3_C2 | footprint only |
| *(reserved)* `SW5` | 35 | GPIO3_A2 | footprint only |
| *(reserved)* ANO `INT` | 37 | GPIO3_C1 | test pad only |

**Pin 7 is deliberately unused** — it defaults to PWM14 rather than plain GPIO.

### Still to confirm

- Run `gpio readall` on the actual board and diff it against the table above.
  A library table is strong evidence, not a schematic.
- Which `/dev/spidevX.Y` Armbian exposes for SPI0, and whether the overlay is
  enabled by default.
- **Whether any of these pins have onboard pull-ups or a boot-time strapping
  role.** wiringOP does not say, and this is the one gap left. A key input tied
  to a strapping pin would hold the board out of boot.
- `libgpiod` addresses lines as chip + offset, not by these numbers. Translate
  before writing firmware.

## Nets

### I²C bus — U1 and the ANO share it

```
            +3V3
             │
       ┌─────┴─────┐
      R2 2.2k    R3 2.2k
       │           │
  ─────┼───────────┼──── SDA ──┬── U1.27 (SDA)
       │           │           └── J3.SDA ── ANO module (0x49)
  ─────┘           └──── SCL ──┬── U1.26 (SCL)
                               └── J3.SCL ── ANO module
                               └── J1 ── host
```

**R2/R3 = 2.2 kΩ.** The bus as originally drawn — relying on the ANO module's
~10 kΩ pull-ups alone — does not meet I²C rise time at realistic capacitance.
2.2 kΩ in parallel with the module's 10 kΩ gives 1.8 kΩ, a 229 ns rise at
150 pF, and sinks 1.6 mA against the 3 mA budget. See
[SIM-11](#sim-11--ic-pull-ups).

> [!WARNING]
> **Measure the Orange Pi header's own I²C pull-ups before fitting R2/R3.**
> If the SBC fits 2.2 kΩ as well, the three-way parallel total is 990 Ω — just
> above the 967 Ω floor for a valid low, with almost no margin. If it does,
> raise R2/R3 to 3.3 kΩ or omit them. The ANO's 10 kΩ is also *typical for
> Adafruit STEMMA QT*, not confirmed for #6310.

### Keys and toggle (SW1–SW3, J4)

Identical network ×4 — three keys and the toggle:

```
+3V3 ── R5 10k ──┬── R9 1k ──── J1 (host GPIO, active low)
                 │
              SW1 (to GND)
                 │
                C1 100nF
                 │
                GND
```

Values from [SIM-13](#sim-13--key-debounce). The filter works on **asymmetric
time constants** — discharge through R9 alone is fast, so the closure stays
crisp; recharge through R9 + R5 is slow, so a brief contact opening cannot climb
back to a logic high and fake a second edge.

- **R5–R8 = 10 kΩ**, external and not the SBC's internal pull-up: an internal
  pull-up is not active before pinmux runs, so the input would float until then.
- **R9–R12 = 1 kΩ.** Cannot be raised to filter on its own — at 3.3 kΩ the
  closed-switch level is 0.819 V, already an invalid low.
- **C1–C4 = 100 nF.** A *window*, not a floor: 220 nF and above fail, because
  the cap stops discharging fully during short closures.

`AIRPLANE` uses the same network. It is a **maintained** toggle, so it has no
bounce burst to speak of, but the RC costs nothing and the symmetry is worth
more than the saved parts.

> **The toggle does not mount to the PCB.** Its leads land on J4. See
> [04](pcb-1-front-control.md#bill-of-materials).

**SW4 and SW5 are footprints only.** They are the two spare switch positions —
routed to J1, not populated, and **not cut into the first faceplate**.

### LED driver (U1) and indicators (D1–D4)

```
 +5V ──┬── C7 10uF ── GND
       │
       ├── D1.A (common anode) ──┬── D1.R ── U1.OUT0
       │                          ├── D1.G ── U1.OUT1
       │                          └── D1.B ── U1.OUT2
       ├── D2.A ── … ── U1.OUT3/4/5
       ├── D3.A ── … ── U1.OUT6/7/8
       └── D4.A ── … ── U1.OUT9/10/11
                                   (OUT12–OUT15 unused, left floating)

+3V3 ──┬── U1.28 VCC ── C5 100nF ── GND
       ├── C6 10uF ── GND
       └── R4 10k ── U1.25 RESET ── J1 (host GPIO, active low)

U1.1  REXT ── R1 1.87k ── GND
U1.2–5  A0–A3 ── JP1–JP4 (0R) ── GND        → address 0x60
U1.10, 19, 24  GND
```

**Channel map.** Four indicators × 3 channels = 12 of 16 outputs. The datasheet
states unused outputs may be left floating.

| Indicator | Label | Channels |
|---|---|---|
| D1 | `AIRPLANE` | OUT0 / OUT1 / OUT2 |
| D2 | `LINK` | OUT3 / OUT4 / OUT5 |
| D3 | `MAC` | OUT6 / OUT7 / OUT8 |
| D4 | `★` | OUT9 / OUT10 / OUT11 |

**R1 = 1.87 kΩ sets 10 mA/channel**, from `IOUT = (1.25 V / Rext) × 15`. TI's
own example value of 931 Ω gives 20 mA and **overheats the part in this
enclosure** — 0.688 W, Tj 115 °C at 60 °C ambient. See
[SIM-12](#sim-12--led-driver-dissipation).

**Address 0x60.** The slave address is `110` + A3 A2 A1 A0, so the device can
only occupy 0x60–0x6F. It therefore **cannot collide with the ANO's 0x49** —
that was never a real risk. It *can* collide with its own LED All Call default
at **0x68** (enabled at power-up) and SWRST at **0x6B**, both of which 0x60
avoids. The datasheet is explicit that the address pins have **no internal
pull-ups** and must each be tied high or low, hence JP1–JP4 as fitted 0 Ω links
rather than no-connects.

**R4 and the reset path.** The datasheet requires a pull-up on `RESET` whether
or not anything drives it. Given that, routing it to a host GPIO costs one pin
and buys the only way to blank the indicators when the I²C bus is wedged —
`SWRST` is a bus command and needs a working bus. Power-on and external reset
both leave all channels deselected, i.e. **LEDs off**, which is the safe state.

Free diagnostics worth using: U1 has open-circuit detection and per-channel plus
global overtemperature shutdown (~170 °C), readable from `EFLAG1`/`EFLAG2`.

### Display breakout (J2)

The display's own 20 cm GH1.25 9-pin cable plugs into J2; PCB 1 passes the
signals to J1. No buffering — the HAT has its own onboard level translator and
accepts 3.3 V logic.

| J2 | Signal | Direction (host's view) |
|---|---|---|
| — | `VCC` 3.3 V | — |
| — | `GND` | — |
| — | `DIN` | out (SPI MOSI) |
| — | `CLK` | out (SPI SCK) |
| — | `CS` | out |
| — | `DC` | out |
| — | `RST` | out |
| — | `BUSY` | **in** |
| — | `PWR` | out |

> [!WARNING]
> **The J2 pin numbers are deliberately blank.** Waveshare's 9-pin order is
> theirs, not a standard, and it must be read off the HAT silkscreen before the
> footprint is committed. Do not infer it from the signal list in
> [10](display-epaper.md#interface-and-wiring) — that list is alphabetical by
> function, not physical order.

`PWR` must be driven, not tied high. The panel can be damaged by being left
powered in a static state — see
[10](display-epaper.md#refresh-discipline-is-a-hard-requirement).

### ANO module (J3)

Four-wire STEMMA QT: +3V3, GND, SDA, SCL. The module is pre-assembled with its
own pull-ups and sits at **0x49**.

`INT` is **not** carried on the four-wire QT cable. A test pad routed to J1
keeps event-driven input open as a later option; Rev A polls.

## Simulation results

Decks in `sim/`, run in the `vezha-sim` podman container on fucina. Each deck
carries its own question, device facts, pass criteria and result.

### SIM-11 · I²C pull-ups

**The question.** 04: "combined bus pull-up value with both devices populated".

**The finding: the bus as drawn does not work.** With only the ANO's ~10 kΩ,
rise time at a realistic 150 pF is 1271 ns — failing even 100 kHz, with 400 kHz
failing at every capacitance tested including an optimistic 50 pF.

| R_total | t_r @150 pF | 100 kHz | 400 kHz | sink |
|---|---|---|---|---|
| 10 kΩ *(as drawn)* | 1271 ns | ❌ | ❌ | 0.29 mA |
| 4.7 kΩ | 597 ns | ✅ | ❌ | 0.62 mA |
| 3.3 kΩ | 419 ns | ✅ | ❌ | 0.88 mA |
| **1.8 kΩ** | **229 ns** | ✅ | ✅ | 1.61 mA |
| 1.0 kΩ | 127 ns | ✅ | ✅ | 2.90 mA |
| 820 Ω | 104 ns | ✅ | ✅ | **3.54 mA — over budget** |

**Conclusion.** R2/R3 = 2.2 kΩ, giving 1.8 kΩ with the module's 10 kΩ. Do not
go lower: with a hypothetical 2.2 kΩ on the SBC as well, 1.8 kΩ here would put
the three-way total at 901 Ω, under the 967 Ω floor.

### SIM-12 · LED driver dissipation

**The question.** What a 5 V anode rail costs the driver, and what current to
set.

**The finding.** A constant-current sink burns whatever the LED does not. With
the chosen LED's worst-case Vf — red 1.6 V, green/blue 2.4 V — the chip drops
**3.4 V on red** and 2.6 V on green/blue. Red is the hottest channel despite
being the dimmest colour, and four red channels make 44 % of the heat.

| I/channel | Rext | P total | Tj @60 °C, θ 80 |
|---|---|---|---|
| 20.1 mA | 931 Ω | 0.693 W | **115 °C** ❌ |
| 15.6 mA | 1.2 kΩ | 0.537 W | 103 °C ❌ |
| 12.5 mA | 1.5 kΩ | 0.430 W | 94 °C |
| **10.0 mA** | **1.87 kΩ** | **0.345 W** | **88 °C** ✅ |
| 6.3 mA | 3.0 kΩ | 0.215 W | 77 °C |

**Conclusion.** R1 = 1.87 kΩ. Nothing is lost: at 10 mA the LED still produces
half of 250–1600 mcd through a diffuser, far more than an indicator needs, and
firmware can scale further down through the IREF gain bits.

60 °C ambient is the honest figure — Enclosure A is a sealed print with an
RK3588 in it and no measured thermal solution.

Ballast resistors on the red channels are **not** needed at 10 mA. Keep the
option on record: TI's datasheet recommends exactly that when VLED is high or Vf
differs between channels, which is this case.

### SIM-13 · Key debounce

**The question.** 04 and 05 both asked: RC on board, or firmware?

> [!NOTE]
> **This deck was corrected on 2026-11-18.** Its first version concluded
> hardware RC could not work, from a pass criterion that asked whether bounce is
> hidden *entirely* rather than whether a **second edge** appears after the
> input has already read a valid low. It also used an invented 5 ms bounce
> burst; the C&K datasheet specifies **≤ 1 ms**.

**The finding.** Fit the RC — and the usable range is a window, not a floor.

| Cf | Peak after first valid low | Verdict |
|---|---|---|
| 1 nF | 3.300 V | ❌ |
| 10 nF | 2.195 V | ❌ |
| 47 nF | 1.086 V | ✅ best margin |
| **100 nF** | **1.627 V** | ✅ **chosen** |
| 220 nF | 2.314 V | ❌ |
| 470 nF | never reaches a valid low | ❌ |

**Conclusion.** 10 kΩ / 1 kΩ / 100 nF. 100 nF over 47 nF for commonality with
the power board's encoder RC — one BOM line across both boards, and the power board validated that
value against a harder stimulus. 47 nF is the fallback if the coupon shows
double presses.

## Open items on this board

- ~~J1 pin assignment~~ — **resolved 2026-11-18** from the vendor's GPIO
  library. Confirm with `gpio readall` on the board, and check none of the
  chosen pins is a boot strapping pin.
- **Measure** the SBC header's I²C pull-ups before fitting R2/R3.
- **Read** Waveshare's 9-pin cable order off the HAT silkscreen before
  committing J2's footprint.
- **Confirm** the `KSC221JLFS` land pattern against the C&K datasheet — the
  figures in [04](pcb-1-front-control.md#6--switch-land-pattern) are read
  off a scanned drawing.
- **Confirm** the ANO module's actual pull-up value.
- Board outline and standoff height are mechanical outputs — see
  [02](../02-enclosure-a-upper.md) and the test coupon in
  [04](pcb-1-front-control.md#mechanical-test-coupon).
