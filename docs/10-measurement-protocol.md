# 10 · Measurement Protocol — the dimensions nobody should guess

**Added 2026-11-18, extended 2026-11-23.** A handful of figures gate every
enclosure dimension. This document exists so that taking them is a short
unambiguous job rather than a research exercise — and so whoever does the
mechanical work is not guessing at what matters.

**Two of them no longer need parts to arrive.** The Orange Pi is on the desk
with its Wi-Fi cards installed, and the SBC's mechanical drawing is a link
away. Those are the two blocking the
[enclosure handoff](../handoff/README.md).

> [!IMPORTANT]
> **No measurement in this document has been taken.** It is the procedure,
> not the result.

## Why these and not others

[01 · The dimensions nobody should guess](01-architecture.md#the-dimensions-nobody-should-guess)
names them. One of the original three is already retired.
They are not the only unknowns — they are the ones where a wrong guess is only
discovered after a case has been printed or a board fabricated:

| # | Dimension | Gates | Currently assumed |
|---|---|---|---|
| 1 | **M.2 stack** — adapter + card + mated plugs + coax bend | **Enclosure A depth** (changed 2026-11-23 — it was thickness, before the board was stood [on edge](01-architecture.md#what-on-edge-mounting-means)). The largest untrusted term in the depth budget | **15.9 mm**, from four stacked guesses |
| ~~2~~ | ~~**RotoPD Pro envelope**~~ — **resolved 2026-11-18 from the vendor repo**, no measurement needed | — | **24.40 × 35.80 mm**, real [geometry](06-power-board-schematic.md#u1--rotopd-pro-mechanical--resolved-from-the-vendor-repo) |
| 3 | **Mated USB-C plug + cable bend radius** | Every USB-C opening in both boxes | **25 mm** |
| **4** | **Thermal stack** — does the fan bolt onto the heatsink? *(added 2026-11-23)* | Enclosure A depth, by 12 mm | **12.6 mm** heatsink; fan **unknown** whether additive |
| **5** | **SBC hole pattern and port positions** — *not a measurement; a file to open* | Board retention, every port cutout | **Nothing.** [Drawing not retrieved](https://drive.google.com/file/d/1rW0tlabPHQ-_rhFcBBpHRGK9TQmT1JEP/view) |

Everything else in [02](02-enclosure-a-upper.md) and
[03](03-enclosure-b-lower.md) can be sized once these are known.

> [!IMPORTANT]
> **Measurement 1 is now cheap and nobody has taken it.** An Orange Pi 5 Plus
> **with the Wi-Fi cards installed is physically on hand** as of 2026-11-23.
> The 15.9 mm figure is four stacked guesses and it is the biggest term in a
> depth budget that currently **does not close** —
> [handoff · depth budget](../handoff/README.md#03--run-the-depth-budget--it-does-not-currently-close).
> This is the highest value-per-minute task in the project right now.

> [!TIP]
> **Measurement 5 is not a measurement at all, which is the point.** This
> document already records the lesson from the RotoPD envelope: *check the
> vendor's repository before scheduling a measurement.* A mechanical file for
> the SBC exists and has never been opened. Do that before reaching for
> calipers.

---

## 0 · Prerequisite — select the M.2 adapter

**Status: candidate proposed 2026-11-18** — the Sintech M-key to A/E-key
card, [assessed below](#candidate-sintech-m-key-to-ae-key-adapter). This
blocks measurement 1 until one is in hand, and it is a sourcing decision,
not a measurement.

### What the board actually provides

Confirmed from published specifications (not from a board in hand):

| Socket | Location | Electrical | Intended module |
|---|---|---|---|
| **M.2 M-key** | **underside** | **PCIe 3.0 ×4** | 2280 NVMe SSD |
| **M.2 E-key** | top side | PCIe 2.0 ×1 + USB 2.0 + PCM/UART | 2230 Wi-Fi |

Two consequences the architecture documents do not currently draw out:

> [!IMPORTANT]
> **Using the M-key slot for the private-AP radio forecloses NVMe storage.**
> It is the only M-key socket on the board. [02](02-enclosure-a-upper.md) lists
> storage as "eMMC discussed, unconfirmed" — that is now a *requirement*, not a
> preference. If NVMe is ever wanted, the radio topology has to change.

> [!NOTE]
> **The adapter path is the faster slot, which reads backwards.** The private
> AP sits behind PCIe 3.0 (using one lane of four), while the hotel uplink
> AX210 on the native E-key gets PCIe 2.0 ×1. Neither is a bottleneck for
> Wi-Fi 6E, but do not assume the adapter is the compromised path.

### Candidate: Sintech M-key to A/E-key adapter

**Proposed 2026-11-18.** "Sintech M.2 M-Key / M.2 A/E Key, NGFF Key-E Card
to M.2 Key M Adapter Card, compatible with Intel 7260, 8260, 9260."

What the listings support, and what they do not:

| | Status |
|---|---|
| **Routes PCIe** | **Likely yes** — described as PCIe ×1 plus USB 2.0, and every card it names (7260, 8260, 9260) is a discrete PCIe part, not CNVi. That is the right signature |
| **Accepts an E-key / A+E-key card** | Yes, that is the product's purpose |
| **Works with MT7922 / RZ616** | **Unverified.** The named-compatibility list is Intel-only and retailer-written. The adapter is electrically generic, so it ought to, but nobody has said so |
| **Installed dimensions** | **Still unknown.** The 11.4 × 8 × 1.7 cm figure in listings is the shipping box. Measurement 1 below is unchanged |

> [!WARNING]
> **USB 2.0 leaves on a separate 5-pin cable, not through the M-key edge.**
> The M.2 M-key connector has no USB 2.0 pins — that is an E-key signal — so
> an adapter must bring it out some other way.
>
> For this build that is probably acceptable: the card in this socket is the
> **private AP**, which needs Wi-Fi only, and Bluetooth is handled by the
> AX210 in the native top-side E-key socket. But it means **the second
> radio's Bluetooth will not work unless that cable is routed to a USB
> header**, and the cable itself is one more thing inside an enclosure whose
> thickness is already the binding dimension.

One caution on substitutions: a related Sintech listing claims AX200/AX201
compatibility. **AX201 is CNVi** and cannot work on a generic PCIe adapter,
so treat that listing's compatibility claims as unreliable and judge any
card by whether it is discrete PCIe.

### Selection requirements

1. **Must route PCIe.** [01](01-architecture.md) already warns "not all do."
   Some adapters wire only USB, which yields a Bluetooth-only card.
2. **Must accept the second radio's key.** E-key or A+E key.
3. **Must not be CNVi-only.** Adapter listings commonly exclude Intel
   **CNVi / CNVio2** cards, which are not standalone PCIe devices and need
   host silicon that RK3588 does not have. This disqualifies Intel AX201,
   AX211 and similar. It does **not** affect the AX210 (discrete PCIe) or the
   MT7922/RZ616 candidate — but it does mean "an Intel Wi-Fi card" is not a
   safe substitution rule.
4. **Check pin pass-through.** Adapters are reported to have signal conflicts
   against the specification; designs that pass only the required signals
   (one PCIe lane plus USB 2.0) are the safer class.
5. **Published mechanical drawing, or accept measuring it blind.** The
   adapter's installed height is measurement 1's dominant term.

### What to verify on arrival, before measuring

```sh
lspci                      # the second radio must enumerate as a PCIe device
lspci -vv | grep -i -A2 'network'
dmesg | grep -iE 'pcie|mt7922|rz616'
```

If it appears only under `lsusb`, the adapter does not route PCIe and the
part is wrong. Stop there — no measurement is worth taking.

---

## 1 · Underside M.2 stack

**Feeds:** `A.adapter_t`, `A.radio2_t`, `A.mhf4_plug_h`, `A.coax_bend_r`
→ `A.underside_stack` → `A.standoff_h` → Enclosure A thickness.

Measure **assembled**, not part by part. The point is the installed stack.

1. Fit the adapter into the Orange Pi's underside M-key socket and screw it
   down at its standoff.
2. Fit the second radio into the adapter's E-key socket and screw it down.
3. **Snap both MHF4 antenna leads on.** They are a significant fraction of
   the height and are the term most often forgotten.
4. Lay the assembly on a flat surface, board face down is wrong — support the
   Orange Pi by its edges so the stack hangs free.
5. With calipers or a depth gauge, measure from the **underside of the Orange
   Pi PCB** to the **lowest point of the stack**, including the mated plugs.
6. Separately, with the coax routed as it will actually run, measure the
   lowest point of the **cable bend**. This is usually below the connectors.

Record the larger of (5) and (6) as the installed stack. Add nothing for
safety here — the clearance allowance is already a separate parameter
(`COMMON.clearance_slip`).

> [!WARNING]
> [02](02-enclosure-a-upper.md) is explicit that the published 100 × 75 mm
> board size excludes the heatsink, the fan, the adapter and cable bends.
> While the assembly is apart, take these too — all three are free at this
> point and all three land in the same depth budget:
>
> - **Installed heatsink height** (`A.heatsink_h`). The supplied figure is
>   **12.6 mm**; the older guess was 15 mm. Confirm which is real.
> - **Whether the fan mounts on top of the heatsink**, and the combined
>   height if so — [measurement 4](#4--the-thermal-stack).
> - **The opposite face's stack**, which on an edge-mounted board adds into
>   the same axis as everything above.

## 2 · RotoPD Pro envelope — resolved, no measurement needed

**Nothing to do here.** On 2026-11-18 the vendor repository turned out to
ship both the KiCad board and a STEP assembly, so the outline, the
mounting-hole positions and diameter, the connector placement and every
component height came straight out of the files.

The numbers are in
[06 · U1 · RotoPD Pro mechanical](06-power-board-schematic.md#u1--rotopd-pro-mechanical--resolved-from-the-vendor-repo).
Headlines: **24.40 × 35.80 mm**, two **M2.5** holes **18.00 mm** apart, and a
**13.00 mm** assembly that drops to **4.70 mm** of components once the screw
terminal is removed.

> [!NOTE]
> Worth remembering as a method, not just a result. 06 had concluded these
> "need the `.kicad_pcb` or the physical board, not another email" — which
> was right, and the `.kicad_pcb` was publicly available the whole time.
> **Check the vendor's repository before scheduling a measurement.**

One thing left to look at, and it does not need calipers: the STEP is
**0.97 mm longer in Y** than the Edge.Cuts outline, so some part projects
past a board edge. Identify which before cutting the wall opening for the
USB-C jack.

## 3 · Mated USB-C plug and bend radius

**Feeds:** `COMMON.usbc_plug_bend`, and every USB-C opening in both
enclosures.

[02](02-enclosure-a-upper.md) is specific: *"Size the case around the mated
plug and its bend radius, not the receptacle footprint."*

1. Use the **cable you actually intend to ship or use**, not a sample. Thick
   high-current USB-C cables bend far worse than thin ones, and this device
   carries up to 5 A.
2. Mate it to a receptacle of the chosen part.
3. Measure from the receptacle's mating face to the **far side of the cable
   where it has returned to parallel with the wall**. That total — plug body
   plus the bend — is the number, not the plug body alone.
4. Repeat for the seam cable in Enclosure B, which is short and therefore
   bends worse. Take the **worst** case.

## 4 · The thermal stack

**Added 2026-11-23.** **Feeds:** `A.heatsink_h`, `A.fan_h` → Enclosure A
depth.

The question is one line long and the answer is worth 12 mm:

> **Does the Noctua NF-A4x10 5V bolt onto the 50 × 46 × 12.6 mm heatsink, or
> is 12.6 mm already a finned assembly with a fan in it?**

1. With the heatsink on the board, measure from the **board's top face** to
   the **highest point of the heatsink**. Expect ~12.6 mm; confirm it.
2. Offer the fan up in its intended position. Measure the **combined** height
   the same way, from the board face.
3. **Record both**, not just the total — the design needs to know whether the
   fan can be deleted later without a reprint.
4. Note how the fan is retained: long screws through the fins, a shroud, or
   adhesive pads. That decides whether the case has to hold it.

> [!WARNING]
> **Measure the fan with its anti-vibration pads fitted.** The part is
> 40 × 40 × **10 mm** by model name, **11 mm** bare and **12 mm** with pads.
> The enclosure is being designed to 12 mm.

## 5 · The SBC mechanical drawing — a file, not a measurement

**Added 2026-11-23.** **Feeds:** board retention, every port cutout, the
40-pin header position.

**[Orange Pi 5 Plus mechanical files](https://drive.google.com/file/d/1rW0tlabPHQ-_rhFcBBpHRGK9TQmT1JEP/view)**
— supplied, **never opened.**

From it, extract and record:

1. **Mounting hole pattern** — positions and diameter. The brief requires the
   board be supported on its actual holes.
2. **Port positions and heights** along every edge, so cutouts come from the
   drawing rather than from the 100 × 75 mm outline.
3. **The 40-pin header's position** on the bottom edge, its envelope, and —
   if the drawing shows it — **pin direction.** If it does not, that stays an
   open question for the client.
4. **Component heights** on both faces, which feed the depth budget alongside
   [measurement 1](#1--underside-m2-stack).

If the link is permission-restricted, that is a request to make on day one —
it blocks the whole mechanical phase.

---

## Recording results

Write each measured value straight into the document that owns it —
[02](02-enclosure-a-upper.md) for Enclosure A, [03](03-enclosure-b-lower.md)
for Enclosure B, [06](06-power-board-schematic.md) for anything that changes
the power board's carrier — and say in the table that it is a **measured**
figure with the date, not a published one.

That distinction is the whole point. Both enclosure documents currently open
by warning that their numbers are published figures for bare parts, and the
three above are the ones where being wrong is only discovered after a case has
been printed or a board fabricated.

Two things to re-check after any of these lands:

- **Enclosure A's depth** is the sum of both M.2 stacks, the board, the
  heatsink, the fan and the panel. A new figure in any of them moves the whole
  box, and the budget is currently **over** the proposed envelope —
  [handoff · depth budget](../handoff/README.md#03--run-the-depth-budget--it-does-not-currently-close).
- **Standoff height in Enclosure B** must still clear the Pololu's **1.4 mm
  below-board protrusion** ([06 · U3](06-power-board-schematic.md)) plus
  trimmed through-hole leads. That constraint is checkable without any
  measurement and is easy to break while changing others.

## Sources

Specifications cited for the Orange Pi 5 Plus sockets and the adapter
disqualifiers are vendor and press publications, not measurements:

- [CNX Software — Orange Pi 5 Plus M.2 sockets](https://www.cnx-software.com/2023/05/10/orange-pi-5-plus-sbc-switches-to-rockchip-rk3588-soc-brings-dual-hdmi-2-1-dual-2-5gbe-m-2-pcie-sockets/)
- [CircuitPython Blinka — Orange Pi 5 Plus board listing](https://circuitpython.org/blinka/orange_pi_5_plus/)
- [Gateworks — M.2 E-key radios use one PCIe lane plus USB 2.0](https://www.gateworks.com/new-mini-pcie-to-m-2-e-key-adapter-for-wifi-radios/)
- [Example M-key to A+E key adapter listing, with the CNVi/CNVio2 exclusion](https://www.amazon.com/M-Key-Wireless-Network-Express-Adapter/dp/B0BGCWQY67)
- [CentyLab RotoPD Pro vendor repository](https://github.com/CentyLab/RotoPD_Pro)
