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
| Key switches | APEM Ultramec 6C `6CJ1NOPR` | 5 | 🔵 Candidate | $3.07 ea |
| Keycaps | APEM/MEC `10G09` black, `10G08` red | 5 | 🔵 Candidate | ~$1–2 ea (est.) |
| Toggle | NKK `MN12LL4G01` | 1 | 🔵 Candidate | ~$11 |
| LED driver | TI `TLC59116IPWR` | 1 | 🔵 Candidate | — |
| RGB LEDs | Common-anode SMD | 4 | 🔴 **Unresolved** | — |
| Light pipes / diffusers | — | 4 | 🔴 **Unresolved** | — |
| Switch alt (SMD) | C&K `KSC221J LFS` | — | 🔵 Candidate | ~$0.52 |
| Switch alt (through-hole) | MEC Multimec 5G `5GTH935` | — | 🔵 Candidate | — |

**Controls subtotal ≈ $45–50** including spares, before cables, shipping, and
PCB assembly.

Notes:
- Populate **3 of 5** switches; keep 2 spare. 6C is firm at ~3.6 N — test one.
  (LCSC's listing says 3.7 N.)
- C&K alt is **not a drop-in**: different footprint, needs its own plunger.
- Multimec 5G alt is **through-hole** — solderable with an iron, 3.5 N, 10 M
  cycles — but it is 10 × 10 × 6.4 mm against the 6C's 8 × 8 × 2.5 mm and takes
  the `1Z`/`1S` cap families, **not** the 10G caps above. Also not a drop-in.
- **RGB LED and its optic must be chosen as a pair** — they set standoff height.
- TLC59116 must be strapped to an address **not** colliding with the ANO's `0x49`.

**JLCPCB assembly availability, checked 2026-11-17** — full results and codes in
[08-sourcing.md](08-sourcing.md#looked-up-so-far):

- ✅ `TLC59116IPWR` (`C131194`) in stock, 3,611 · $1.11 @100.
- ❌ `6CJ1NOPR` (`C5518654`), NKK `MN12LL4G01` (`C20103999`), and both keycaps
  are **zero stock with no pre-order** — JLC cannot place them. Only the switch
  matters: the toggle is panel-mount and the caps press on by hand, so neither
  was ever a machine-placed part. Source all three from DigiKey.
- ❌ The through-hole alternatives are **also** zero stock at LCSC — Multimec
  `5GTH935`/`5GTH920` and the whole C&K `PTS645` range. Fine if you are hand-
  sourcing, but there is no JLC fallback for them later. The only through-hole
  tactiles actually in stock are generic Alps `SKHH` (6 × 6 mm, ~$0.09–0.17).
- ✅ The C&K alt `KSC221JLFS` (`C221726`) is in stock at 16,623 · $0.46 @100 —
  the only tactile switch here JLC can actually place.
- Every part checked is an `expand` (extended) library part, so each distinct one
  adds a feeder fee to an assembly order.

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

1. **Buy one of each control first.** One NKK toggle, one 6C switch with cap,
   one ANO, one RGB LED with its optic. Print the test coupons in
   [04](04-pcb-1-front-control.md) before committing to a four-indicator board.
2. **Confirm JLCPCB assembly sourcing in the quote**, not from a catalog
   search. The catalog check on 2026-11-17 says the TLC59116 is in stock and the
   6C switch, toggle and keycaps are not; the RGB LED has no part number yet. A
   catalog snapshot is not a commitment — the quote is.
3. **Measure, don't look up**, the three dimensions in
   [01-architecture.md](01-architecture.md#the-three-dimensions-nobody-should-guess).

Lookup method and price checking: [08-sourcing.md](08-sourcing.md).
