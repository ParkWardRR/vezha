# 07 · Bill of Materials

Every part named across this repo, with its standing. **Nothing here has been
ordered.**

> [!CAUTION]
> **Status is the most important column.** "Candidate" means someone suggested
> it and nobody has validated it. Verify any part before ordering, and verify
> any *dimension* before machining to it.

## Status key

| | Meaning |
|---|---|
| ✅ **On hand** | Physically owned |
| 🟡 **Chosen** | Decided, not purchased |
| 🔵 **Candidate** | Proposed, not validated |
| 🔴 **Unresolved** | No part selected |
| ⬜ **Dropped** | Previously considered, now superseded |

## Enclosure A — upper router box

| Part | PN | Status | Price | Notes |
|---|---|---|---|---|
| SBC | Orange Pi 5 Plus (RK3588) | 🟡 Chosen | — | 100 × 75 mm bare board. Clearance needed **both faces**. |
| Uplink radio | Intel AX210 | ✅ **On hand** | — | M.2 2230, 22 × 30 × 2.4 mm. Top-side E-key socket. |
| AP radio | MediaTek MT7922 / AMD RZ616 | 🔵 Candidate | — | 2230 assumed, **height unconfirmed**. Verify antenna connector type and 5 GHz AP operation first. |
| M.2 adapter | M-key → E-key | 🔴 **Unresolved** | — | Must **route PCIe**. Installed stack height unmeasured. |
| Antennas ×4 | Taoglas FXP830.24.0100B | 🔵 Candidate | $7.31 ea · ~$29/4 | 42 × 7 mm, 100 mm MHF4 lead. Estimate, not a live quote. |
| Antenna alt (uplink) | TE/Linx ANT-W63-WRT-MHF4 | 🔵 Candidate | $15.31 ea · ~$31/pr | Dome. **Gain figures quoted are the SMA variant's** — verify the MHF4 datasheet. |
| Antenna alt | TE/Linx ANT-W63WS1-SMA | 🔵 Candidate | $12.27 ea | Blade, needs MHF4→SMA bulkheads. Not pocketable. |
| Antenna alt | Octane SA-2400/5800 | 🔵 Candidate | ~$79 ea (GSA) | **No full 6 GHz coverage.** Not a verified retail price. |
| Storage | eMMC | 🔴 Unresolved | — | Discussed only. |
| RTC backup cell | CR2032 + holder, **or** ML2032 / LIR2032 rechargeable | 🔴 **Unresolved** — chemistry | ~$2–5 | **No RTC part to buy.** The Orange Pi 5 Plus already carries the RTC chip and a **2-pin 1.25 mm** backup-battery header; this is a cell and a lead. **Confirm whether that header trickle-charges before fitting a rechargeable** — if it is a plain backup input, a rechargeable never recharges, and if it does charge, a primary CR2032 must not go on it. Coin cells are commonly rated to 60 °C: keep it off the heatsink. Why it is here: [02](02-enclosure-a-upper.md#rtc-backup-cell). |
| RTC battery lead | 2-pin **1.25 mm pitch** pigtail (JST GH / PicoBlade-class) | 🔵 Candidate | ~$1 | Mates the Orange Pi's RTC header. **Verify pitch, housing and polarity against the board itself** — 1.25 mm is the published wiki figure, and the neighbouring 1.5 mm ZH-class housings will part-mate and mislead. |
| RTC chip (on the SBC) | **HYM8563TS** | 🔵 **Unverified** | — | Named in one third-party spec listing, not confirmed against the board or schematic. Affects nothing to order; it decides the Linux driver and the `cat /proc/driver/rtc` check in [09](09-software-and-bringup.md#bring-up-order). |
| UART header (Pi side) | — | ⬜ **Likely none needed** | — | The 5 Plus ships with its 40-pin header populated and usually has a separate debug UART header. **Verify before buying.** Do not use the console UART for telemetry — see [05](05-power-board.md#telemetry-header). |
| Display | Waveshare 4.26" e-Paper HAT, SKU `26376` | ⬜ **Dropped** | ~~$31.99~~ | **v1 is headless** — [the scope cut](01-architecture.md#the-v1-scope-cut). Chosen 2026-11-17, cut 2026-11-18. Analysis kept in [10](retired/display-epaper.md). |
| Heatsink | — | 🔴 Unresolved | — | Thermal case untested. |

## PCB 1 — front control board ⬜ **Dropped entirely**

> [!CAUTION]
> **Buy none of these.** PCB 1 is not built in v1 —
> [the scope cut](01-architecture.md#the-v1-scope-cut). Every part below was
> chosen and sourced before the cut; the table is kept so a v2 front panel does
> not repeat the sourcing work. Stock figures are from 2026-11-17 and will have
> moved.

| Part | PN | Qty | Was | Price |
|---|---|---:|---|---|
| Nav wheel | Adafruit #6310 ANO I²C module | 1 | 🔵 Candidate | $13.95 |
| Key switches | C&K `KSC221JLFS` · LCSC `C221726` | 5 | 🟡 Chosen | $0.76 ea · $0.46 @100 |
| Plungers | Printed — no catalogue part | 3 | 🔴 Design work | — |
| Toggle | NKK `MN12LL4G01` | 1 | 🔵 Candidate | ~$11 |
| LED driver | TI `TLC59116IPWR` · LCSC `C131194` | 1 | 🟡 Chosen | $1.79 ea · $1.11 @100 |
| RGB LEDs | MEIHUA `MHPA2525RGBDT-S` · LCSC `C404285` | 4 | 🟡 Chosen | $0.091 ea |
| LED current-set R | 1.87 kΩ 1 % on `REXT` — sets 10 mA/ch | 1 | 🟡 Chosen | — |
| Display connector | JST GH 9-pin `SM09B-GHS-TB` · LCSC `C265420` | 1 | 🟡 Chosen | $0.39 |
| Diffuser windows | Printed into the faceplate | 4 | 🔴 Design work | — |
| Switch, rejected | APEM Ultramec 6C `6CJ1NOPR` | — | ⬜ Rejected | $3.07 DigiKey · 0 stock at JLC |
| Switch, rejected | MEC Multimec 5G `5GTH935` | — | ⬜ Rejected | Through-hole, 0 stock at LCSC |

**≈ $29–32 of parts, plus a board and its assembly, removed from v1.** The
larger saving is not the money: it is the fabrication of a second PCB, a
removable faceplate with six opening types, and the plunger coupon that gated
ordering it.

**Findings worth keeping for v2** — the reasoning, not just the part numbers:

- Every placed part was sourced with an LCSC code and in stock. Both chosen
  parts are `expand` library, so each carries a feeder fee — confirm in the
  quote, not the catalog.
- The rejected switches and both keycap systems read **zero stock with no
  pre-order**, as did all through-hole alternatives. That, not feel, is what
  settled the switch choice.
- **The KSC has no cap system**, and travel is **0.35 mm nominal** against the
  6C's 2.5 mm. Printed plungers against that travel were the highest-risk
  mechanical item in the build.
- **RGB LED and optic must be chosen as a pair** — together they set standoff
  height.
- TLC59116 must be strapped clear of the ANO's `0x49`; `0x60` was chosen.

## Power board

| Part | PN | Status | Dimensions |
|---|---|---|---|
| PD negotiation | CentyLab RotoPD Pro | 🟢 **Resolved** | **24.40 × 35.80 mm** · 2 × M2.5 (⌀2.7 mm), **18.00 mm apart** · assembly spans 13.00 mm, **4.70 mm with the screw terminal removed**. From the [vendor repo](https://github.com/CentyLab/RotoPD_Pro), not a measurement — [geometry](06-power-board-schematic.md#u1--rotopd-pro-mechanical--resolved-from-the-vendor-repo) |
| Controller | Raspberry Pi Pico 2 (non-wireless) | 🟡 Chosen | 51 × 21 × 1 mm bare |
| 5 V regulator | Pololu **D42V55F5 (#5571)** | 🟢 **Decided 2026-11-18** | 25.4 × 25.4 mm, **1.57 mm** board · **6.1 mm above, 1.4 mm below** (9.07 mm total — the 9 mm figure is the *whole stack*, not height above board) · 3 holes ⌀2.18 mm on a 21.1 × 21.1 mm pattern. **The 5.3 V #5572 is ruled out**: the Orange Pi's USB-C input is fixed 5 V and the vendor warns above 5 V damages the board. This leaves the **seam loop over budget** — [06](06-power-board-schematic.md#u3-is-the-50-v-part) |
| Seam output | USB-C receptacle, part TBD | 🔴 **Unresolved — now the binding item** | **5 V power only.** No longer an independent part choice: a 6-pin power-only receptacle brings out **two** VBUS and two GND contacts where a 16-pin part brings out **four of each**, and paralleling them is one of the few levers on the loop-resistance budget — [06](06-power-board-schematic.md#u3-is-the-50-v-part) |
| Seam cable | Short USB-C to USB-C | 🔴 **Unresolved — now the binding item** | Captive or detachable. Cable conductor resistance is a large share of the loop, and a 5 A-rated cable is still specified to drop up to 250 mV — [06](06-power-board-schematic.md#u3-is-the-50-v-part) |
| USB-C receptacle | GCT USB4120-03-C (`C3445864`) | 🔵 Candidate | 48 V / 5 A **contact** rating — not a PD capability. JLC stock 1,253 as of 2026-11-17. |

### Power board — measurement and debug hardware

Added as cheap insurance: each is small money at design time and expensive or
impossible once the boards are made and the boxes closed. Rationale and
rankings in [05](05-power-board.md#cheap-insurance-worth-adding-now).
JLCPCB codes checked 2026-11-18. **All four are `expand`**, so each adds a
feeder fee — worth weighing against placing them at all.

| Part | PN | Status | Price | Notes |
|---|---|---|---|---|
| Current/voltage monitor | TI **INA226AIDGSR** · JLC `C49851` | 🟡 **Chosen** | ~$1–2 | **High-side in the 5 V output**, between Pololu VOUT and the USB-C seam receptacle — measures what the Orange Pi actually receives. On **I²C bus 1** (rail-critical). Defaults to `0x40`, strappable `0x40`–`0x4F` — **verify no collision with the RotoPD Pro.** VSSOP-10, stock 56,084. **Avoid `C2653870`** (DGST, stock 17). |
| Sense resistor | TA-I **RLP25FEER002** · JLC `C160590` | 🟡 **Chosen** | — | 2512, 2 W, ±1 %, ±50 ppm/°C, stock 32,253. 8.0 mV at 4 A = 9.8 % of INA226 range · 1.25 mA resolution · **32 mW loss, so 2 W is ample** — pick on stock. Alt `C154685` (RALEC 3 W, stock 27,568). Kelvin-connect it. |
| Temperature sensor | Murata **NCP18XH103F03RB** · JLC `C13564` | 🟡 **Chosen** | ~10 ¢ | 0603, 10 kΩ, B = 3380 K, ±1 %, stock 261,587. Against the **Pololu's thermal pad**, to a Pico ADC. Measures sealed-box derating with the lid closed. Enables thermal foldback. **Generic "NTC" rows are all zero stock** — match this code. |
| Telemetry header | XFCN **PZ254V-11-03P** · JLC `C2937625` | 🟡 **Chosen** | ~5 ¢ | 1×3P vertical through-hole, 3 A/250 V, stock 1,030,846. TX/RX/GND, **populated but unwired in Rev A**. Silkscreen `TX→RX`. **`C492402` is the same MPN at zero stock — match the code, not the MPN.** |
| Telemetry series R | 100–330 Ω ×2 | 🔴 **Unresolved** | ~2 ¢ | On TX and RX. Makes a reversed header survivable. |
| SWD header | 3-pin 2.54 mm | 🔴 **Unresolved** | ~10 ¢ | SWCLK, SWDIO, GND. The only way in when firmware crashes before USB enumerates. |
| Rail test points | Probe pads | 🔴 **Unresolved** | free | PD VBUS, Pololu VOUT, 3.3 V, several GND — **plus a pair at the USB-C seam output**, so "voltage at the Orange Pi under load" does not mean probing connector pins. |
| Isolation jumpers | 0 Ω | 🔴 **Unresolved** | ~1 ¢ | On buck EN and each I²C bus, for sectioned bench bring-up. |
| Pico reset | Pad or button on `RUN` | 🔴 **Unresolved** | ~5 ¢ | BOOTSEL is unreachable once enclosed. |

> [!NOTE]
> **The INA226 and the NTC are the two that matter.** They convert the
> project's two largest unknowns — whether the Pi stays under USB-C's 3 A
> limit at 5 V, and how far the Pololu derates in a sealed box — from
> one-off bench measurements into continuous readings taken with the case
> closed. They also give the Pico a basis for overcurrent shutdown and
> thermal foldback alongside the PD contract check it already performs.

## Power source

| Item | Status | Notes |
|---|---|---|
| External USB-C PD charger / bank | 🔴 **Unresolved** | Anker 10,000 mAh PowerIQ discussed; **exact model and PD profiles unconfirmed.** Advertised wattage does not establish it can run this. |
| Internal cell | 🔴 Open question | Whether Enclosure B ever contains one is undecided. |

## Not purchasable yet

Outputs of design work, not catalogue items:

- Enclosure A shell, with service access (3D printed) — **no faceplate in v1**
- Enclosure B shell (3D printed)
- **the power board** fabrication and assembly — the only board in v1

## Before ordering anything

1. **Measure, don't look up** — but check the vendor's repository first.
   What were three gating dimensions are now **two**: the RotoPD envelope came
   out of CentyLab's published KiCad and STEP files on 2026-11-18 without a
   physical part. See
   [10 · Measurement protocol](10-measurement-protocol.md). The underside M.2
   stack and the mated USB-C plug still need hardware in hand.
2. ~~**Settle the regulator first.**~~ — **done 2026-11-18: the 5.0 V
   #5571**, forced by the Orange Pi's fixed-5 V input rather than chosen on
   merit. **Order that part number only.** What it did not settle is the seam
   loop, which is now the open problem —
   [06](06-power-board-schematic.md#u3-is-the-50-v-part).
3. **Confirm JLCPCB assembly sourcing in the quote**, not from a catalog
   search. A catalog snapshot is not a commitment. This now applies only to
   the power board's measurement and debug hardware, all four of which are `expand`
   library and each of which adds a feeder fee.

Lookup method and price checking: [08-sourcing.md](08-sourcing.md).
