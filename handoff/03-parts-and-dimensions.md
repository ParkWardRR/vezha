# 03 · Parts, Dimensions and Links

Every number you need in one place, **each tagged with where it came from.**

> [!CAUTION]
> **Read the provenance column before designing to any figure.** This project
> has a standing rule that a published body size is never a cutout dimension,
> and roughly half the numbers below are published figures, vendor estimates
> or stacked guesses rather than measurements.

## Provenance key

| | Meaning |
|---|---|
| 🟢 **Verified** | Read off a vendor drawing or datasheet in hand |
| 🟡 **Published** | Vendor's published figure for the bare part — real, but excludes installed hardware |
| 🟠 **Supplied** | Given by the client; plausible, not traced to a drawing |
| 🔴 **Guess** | A stacked estimate. Do not cut to it |

---

## Compute

| Item | Figure | Provenance | Notes |
|---|---|---|---|
| **Orange Pi 5 Plus** board | **100 × 75 mm** | 🟡 Published | Bare board. **Excludes** heatsink, fan, M.2 adapter, mated antenna plugs, cable bends |
| PCB thickness | ~1.6 mm | 🔴 Guess | Typical FR4. Not confirmed for this board |
| Mounting holes | **Not retrieved** | — | The brief says support the board by its *actual* mounting holes. Get them from the drawing below |
| **Mechanical drawing** | [Google Drive](https://drive.google.com/file/d/1rW0tlabPHQ-_rhFcBBpHRGK9TQmT1JEP/view) | 🔴 **Not retrieved** | **Phase 0 blocker.** Authority for hole pattern, connector positions, component heights |
| Board orientation | **40-pin header at the bottom edge** | 🟢 Specified | Settles which edge faces the floor. [Brief](01-brief-upright-case.md) |
| Header pin direction | **Unconfirmed** | 🔴 | The brief is explicit: a bottom access opening does **not** imply the stock pins point downward |

### Alternate board — not a drop-in

| Item | Figure | Provenance | Notes |
|---|---|---|---|
| Orange Pi **5**, rev **V1.3.2** | **100 × 62 mm** | 🟡 Published *model* | 13 mm narrower. **Revision-specific drawing not verified** |

> [!WARNING]
> **Do not treat the Orange Pi 5 as a smaller 5 Plus.** The radio design needs
> *both* an M.2 M-key socket and a native top-side M.2 E-key socket. Published
> specs for the Orange Pi 5 describe **one M-key socket and no native E-key**.
> If that holds, the uplink card has nowhere to go and the radio topology has
> to be redesigned rather than adjusted. Settle the socket question before the
> footprint one. [Detail](../docs/01-architecture.md#the-alternate-board-and-why-it-is-not-a-drop-in)

---

## Cooling

| Item | Figure | Provenance | Notes |
|---|---|---|---|
| **Heatsink** — Orange Pi 5 Plus aluminium | **50 × 46 × 12.6 mm** (L × W × H) | 🟠 Supplied | No SKU or drawing. Height is the number that matters and it is untraced |
| **Fan** — [Noctua NF-A4x10 5V](https://noctua.at/en/products/nf-a4x10-5v/specifications) | **40 × 40 × 10 mm** nominal | 🟡 Published | This is the *model name* figure |
| Fan, bare | 40 × 40 × **11** mm | 🟠 Supplied | Without anti-vibration pads |
| **Fan, installed** | 40 × 40 × **12** mm | 🟠 Supplied | **With pads. Design the pocket to this.** |
| Fan supply | **5 V** | 🟢 Specified | |
| Fan connector | **3-pin: GND, 5 V, RPM tach** | 🟢 Specified | |
| Fan PWM input | **None** | 🟢 Specified | Not a PWM fan. Speed cannot be controlled by PWM |
| Fan price | ~$16 USD | 🟠 Supplied | Client estimate, not a quote |
| Fan input current | **Not retrieved** | 🔴 | Noctua's spec page rate-limited on 2026-11-23. Needed for the 5 V budget |

> [!CAUTION]
> **Two cooling traps.**
>
> **1 · The fan is not 10 mm.** The model name says 10 mm, the part is 11 mm
> bare and **12 mm with its anti-vibration pads.** Pocket at 12 mm. Dropping
> the pads to recover 1 mm trades it for vibration straight into a printed
> shell — in a handheld, that is the wrong trade.
>
> **2 · Nobody has said whether the heatsink and fan stack.** A 12.6 mm
> heatsink with a 12 mm fan bolted to it is a **24.6 mm** thermal block. A
> 12.6 mm assembly that already *includes* a fan is half that. **This is the
> single largest uncertainty in the depth budget** —
> [Phase 0](README.md#phase-0--inputs-and-sanity-checks).

---

## Display

**An OLED on the front face, output only.** No controls anywhere on the
device.

**The exact model is not fixed.** The candidate is the **Adafruit 5297**,
already used as the power board's console display — the same part in both
boxes means one part number, one driver, one spare.

| | Adafruit 5297 |
|---|---|
| Active area | **20.076 × 20.076 mm** |
| Interface | **I²C**, 4-pin JST-SH STEMMA QT / Qwiic — 3.3 V, GND, SDA, SCL |
| Operating temp | **−40 to +70 °C** |
| Provenance | 🟡 Published; already specified for [the power board](../docs/05-power-board.md#adafruit-5297-oled) |

> [!WARNING]
> **20 mm square is small for a front panel, and that is the open question.**
> A Wi-Fi join QR for a strong passphrase needs roughly **≥ 0.5 mm per
> module** to scan reliably, which is marginal at 20.076 mm. **If the join QR
> has to render on the panel, a larger OLED is needed** — and that moves the
> front-face geometry. Settle it before cutting the window.

> [!NOTE]
> **The display does not drive the enclosure footprint.** It is far smaller
> than the board's 100 mm edge. It is also **not** a thermal weak point —
> −40 to +70 °C is wider than e-paper's typical 0–50 °C, which is part of why
> OLED was chosen.
>
> What OLED gives up: **no status at rest.** It shows nothing with the power
> off, where e-paper holds its last image. And **static images burn in**, so
> a status panel needs a screensaver, pixel shift or timeout in firmware.

## Antennas

**Taoglas FXP830.24.0100B** — adhesive flex dipole, **ordered.**
[Datasheet](https://www.taoglas.com/datasheets/FXP830.24.0100B.pdf) ·
[Product page](https://www.taoglas.com/product/fxp830-24-0100b/)

All figures below are 🟢 **read from the datasheet** (rev. SPE-14-8-022-G)
unless noted.

| Item | Figure |
|---|---|
| Body | **42 ± 0.4 × 7 ± 0.3 mm** |
| Body thickness | **See the warning below — the datasheet does not give one** |
| Cable | **100 ± 3 mm** of **Ø0.81 mm** coax, grey, FEP |
| Connector | **I-PEX MHF4** (HSC compatible), brass / gold |
| **Mated connector height** | **2.1 ± 0.4 mm**, body 3.46 ± 0.6 mm long |
| Adhesive | **3M 467** double-sided, brown liner, with a cutting line |
| Bands | **2400–2500 · 5150–5850 · 5925–7125 MHz** |
| Peak gain, 2 mm ABS | 3.46 / 6.86 / 8.09 dBi |
| Peak gain, free space | 2.14 / 5.33 / 6.49 dBi |
| Impedance · polarization | 50 Ω · linear · omnidirectional |
| Operating temp | **−40 to +85 °C** |
| Weight | 7 g each |
| Quantity planned | **4** (per the cap brief) — 🟠 the ordered quantity was not recorded |

> [!CAUTION]
> **The antenna body thickness is genuinely missing from the datasheet, and
> it does not matter as much as you would think.**
>
> | Where | What it says |
> |---|---|
> | Introduction prose | `42*7*.01mm` → **0.01 mm** |
> | Specification table | `42 x 7 x mm` → **the field is blank** |
> | Mechanical drawing | **No thickness callout at all** |
>
> 0.01 mm is 10 µm — thinner than kitchen foil, and not plausible for a
> polymer FPCB. A figure of 0.1 mm has been quoted elsewhere but is not in
> the datasheet.
>
> **Design to the connector, not the film.** The **mated MHF4 at
> 2.1 ± 0.4 mm** is dimensioned, is an order of magnitude larger than either
> candidate thickness, and is what actually sets clearance behind the cap
> wall. Add the 3M 467 adhesive on top of it. The cap brief already says not
> to specify a recess depth until the real assembly is checked — this is why.

---

## Radios and the M.2 stack

| Item | Figure | Provenance | Notes |
|---|---|---|---|
| **Intel AX210** (uplink) | 22 × 30 × 2.4 mm, M.2 2230 | 🟡 Published | **On hand.** Native top-side E-key socket |
| **MT7922 / RZ616** (AP) | 22 × 30 mm assumed | 🔴 Candidate | Height unconfirmed, part not locked |
| **M-key → E-key adapter** | **Unmeasured** | 🔴 | Must route PCIe. Sintech card is the candidate |
| **Far-face M.2 stack** — adapter + card + mated plugs + coax bend | **15.9 mm** | 🔴 **Guess** | Four stacked guesses. [Measurement procedure](../docs/10-measurement-protocol.md#1--underside-m2-stack) |

> [!IMPORTANT]
> **One radio sits on each face of the board.** The uplink card is in the
> board's native top-side E-key socket; the AP card hangs off the opposite
> face on an adapter. Standing the board upright turns both into **horizontal
> growth into the case depth** rather than a thickness problem — but it means
> the depth budget has to carry *both* stacks plus the board. This is the
> second-largest uncertainty after the cooling stack.

---

## Fasteners and hardware

| Item | Figure | Notes |
|---|---|---|
| Cap retention | **2 × M3 rear-access screws** | Socket or button head. **Not** countersunk into thin ears |
| Threaded inserts | **M3 heat-set**, in the **main case** | [Prusa guidance](https://www.prusa3d.com/product/heat-set-inserts-m3-standard-100-pcs/). **Size the bore from the chosen insert's drawing, never from "M3"** |
| Screw clearance hole | **~3.4 mm** starting point | Verify against printer and hardware |
| Locating skirt depth | **4–5 mm** | Skirt locates, screws retain |
| Skirt sliding clearance | **0.25–0.35 mm per mating side** | FDM starting tolerance. Coupon first |
| Nominal wall | **2 mm** | |

---

## Style reference

[**Lilygo T-Beam SUPREME TS1 Case by Alley Cat**](https://www.printables.com/model/705817-lilygo-t-beam-supreme-ts1-case-by-alley-cat)
— the specific things wanted from it:

- **Curved features** rather than a hard rectangular box
- **Slots for a strap**
- **Textured surface lines**

Treat it as a visual language reference, not a geometry reference.

---

## Everything linked, in one list

**Client-supplied**
- [Orange Pi 5 Plus mechanical files](https://drive.google.com/file/d/1rW0tlabPHQ-_rhFcBBpHRGK9TQmT1JEP/view) — **not yet retrieved**
- [Lilygo T-Beam SUPREME case — style reference](https://www.printables.com/model/705817-lilygo-t-beam-supreme-ts1-case-by-alley-cat)

**Datasheets and vendors**
- [Noctua NF-A4x10 5V specifications](https://noctua.at/en/products/nf-a4x10-5v/specifications)
- [Taoglas FXP830.24.0100B datasheet (PDF)](https://www.taoglas.com/datasheets/FXP830.24.0100B.pdf)
- [Adafruit 5297 OLED](https://www.adafruit.com/product/5297)
- [Prusa M3 heat-set inserts](https://www.prusa3d.com/product/heat-set-inserts-m3-standard-100-pcs/)
- [CentyLab RotoPD Pro repository](https://github.com/CentyLab/RotoPD_Pro) — for the later power module

**Board references**
- [CNX Software — Orange Pi 5 Plus M.2 sockets](https://www.cnx-software.com/2023/05/10/orange-pi-5-plus-sbc-switches-to-rockchip-rk3588-soc-brings-dual-hdmi-2-1-dual-2-5gbe-m-2-pcie-sockets/)
- [CircuitPython Blinka — Orange Pi 5 Plus board listing](https://circuitpython.org/blinka/orange_pi_5_plus/)

**This repo**
- [Handoff plan](README.md) — start here
- [Brief · upright case](01-brief-upright-case.md) · [Brief · antenna cap](02-brief-antenna-cap.md)
- [01 · Architecture](../docs/01-architecture.md) — the system split and why
- [02 · Enclosure A](../docs/02-enclosure-a-upper.md) — this box, in detail
- [03 · Enclosure B](../docs/03-enclosure-b-lower.md) — the later lower module
- [04 · Antennas](../docs/04-antennas.md) — placement and the RF test
- [05 · Power board requirements](../docs/05-power-board.md) · [06 · Schematic](../docs/06-power-board-schematic.md)
- [07 · BOM](../docs/07-bom.md) · [08 · Sourcing](../docs/08-sourcing.md)
- [10 · Measurement protocol](../docs/10-measurement-protocol.md)
