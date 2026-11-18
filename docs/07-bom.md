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
| Display | Waveshare 4.26" e-Paper HAT, SKU `26376` | 🟡 **Chosen** | $31.99 | 800 × 480 B/W, SPI. Active area 92.80 × 55.68 mm; driver board **107 × 64 mm**. Supersedes the 3.5" HDMI touchscreen. **Own bracket.** Full details and its refresh/temperature limits: [10-display.md](10-display.md). |
| Heatsink | — | 🔴 Unresolved | — | Thermal case untested. |

## PCB 1 — front control board

| Part | PN | Qty | Status | Price |
|---|---|---:|---|---|
| Nav wheel | Adafruit #6310 ANO I²C module | 1 | 🔵 Candidate | $13.95 |
| Key switches | **C&K `KSC221JLFS`** · LCSC `C221726` | 5 | 🟡 **Chosen** | $0.76 ea · $0.46 @100 |
| Plungers | Printed — no catalogue part | 3 | 🔴 **Design work** | — |
| Toggle | NKK `MN12LL4G01` | 1 | 🔵 Candidate | ~$11 |
| LED driver | TI `TLC59116IPWR` · LCSC `C131194` | 1 | 🟡 **Chosen** | $1.79 ea · $1.11 @100 |
| RGB LEDs | Common-anode SMD | 4 | 🔴 **Unresolved** | — |
| Light pipes / diffusers | — | 4 | 🔴 **Unresolved** | — |
| Switch, rejected | APEM Ultramec 6C `6CJ1NOPR` | — | ⬜ Rejected | $3.07 DigiKey · 0 stock at JLC |
| Switch, rejected | MEC Multimec 5G `5GTH935` | — | ⬜ Rejected | Through-hole, 0 stock at LCSC |

**Controls subtotal ≈ $29–32** including spares, before cables, shipping, and
PCB assembly. *(Down from ~$45–50: the switch went from $3.07 to $0.76 and the
$1–2 keycaps became printed plungers.)*

Notes:
- Populate **3 of 5** switches; keep 2 spare.
- **The KSC has no cap system.** Three printed plungers replace the MEC 10G
  caps, and **travel is only 0.6 mm** against the 6C's 2.5 mm. The plunger
  stack is now the highest-risk mechanical item on the front panel — see
  [04](04-pcb-1-front-control.md#plunger-design).
- At ~2 N the keys are lighter than the 6C's ~3.6 N. `MAC` stays recessed.
- **RGB LED and its optic must be chosen as a pair** — they set standoff height.
- TLC59116 must be strapped to an address **not** colliding with the ANO's `0x49`.

**JLCPCB assembly, checked 2026-11-17** — codes and price ladders in
[08-sourcing.md](08-sourcing.md#looked-up-so-far):

- ✅ Switch `C221726` — 16,623 in stock. ✅ Driver `C131194` — 3,611 in stock.
- 🔴 **The RGB LED is the only unsourced placed part**, and therefore the
  critical path to an assembly quote for this board.
- Both chosen parts are `expand` (extended) library, so each carries a feeder
  fee. Confirm in the quote, not from the catalog.
- The rejected switches and both keycaps read **zero stock with no pre-order**
  at LCSC, as do all the through-hole alternatives (Multimec 5G, C&K `PTS645`).
  That is what settled the choice.

## PCB 2 — power board

| Part | PN | Status | Dimensions |
|---|---|---|---|
| PD negotiation | CentyLab RotoPD Pro | 🟡 Chosen | **Outline, height, mounting pattern all unverified** |
| Controller | Raspberry Pi Pico 2 (non-wireless) | 🟡 Chosen | 51 × 21 × 1 mm bare |
| 5 V regulator | Pololu D42V55F5 (#5571) | 🟡 Chosen | 25.4 × 25.4 × 9 mm · 3 × M2 holes |
| Seam output | USB-C receptacle, part TBD | 🔴 **Unresolved** | **5 V power only.** Advertise 5 V/3 A (10 kΩ Rp) if the Pi measures under 3 A — see [01](01-architecture.md#the-3-a-problem) |
| Seam cable | Short USB-C to USB-C | 🔴 **Unresolved** | Captive or detachable, TBD |
| USB-C receptacle | GCT USB4120-03-C (`C3445864`) | 🔵 Candidate | 48 V / 5 A **contact** rating — not a PD capability. JLC stock 1,253 as of 2026-11-17. |

## Power source

| Item | Status | Notes |
|---|---|---|
| External USB-C PD charger / bank | 🔴 **Unresolved** | Anker 10,000 mAh PowerIQ discussed; **exact model and PD profiles unconfirmed.** Advertised wattage does not establish it can run this. |
| Internal cell | 🔴 Open question | Whether Enclosure B ever contains one is undecided. |

## Not purchasable yet

Outputs of design work, not catalogue items:

- Enclosure A shell + removable faceplate (3D printed)
- Enclosure B shell (3D printed)
- PCB 1 and PCB 2 fabrication and assembly

## Before ordering anything

1. **Buy one of each control first.** One NKK toggle, a few KSC switches, one
   ANO, one RGB LED with its optic. Print the test coupons — including plungers
   at two or three lengths — in [04](04-pcb-1-front-control.md) before
   committing to a four-indicator board.
2. **Confirm JLCPCB assembly sourcing in the quote**, not from a catalog
   search. As of 2026-11-17 the switch and driver are both in stock and the RGB
   LED has no part number yet. A catalog snapshot is not a commitment — the
   quote is.
3. **Measure, don't look up**, the three dimensions in
   [01-architecture.md](01-architecture.md#the-three-dimensions-nobody-should-guess).

Lookup method and price checking: [08-sourcing.md](08-sourcing.md).
