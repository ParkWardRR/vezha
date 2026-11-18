# 10 · Measurement Protocol — the three dimensions nobody should guess

**Added 2026-11-18.** Everything dimensional in
[`cad/params.py`](../cad/params.py) is gated on three measurements that need
physical parts. This document exists so that when the parts arrive, taking them
is a short unambiguous job rather than a research exercise.

> [!IMPORTANT]
> **No measurement in this document has been taken.** It is the procedure, not
> the result. `cad/build.py` currently reports **36 of 60 dimensions
> unverified**, and `--strict` exits non-zero by design until that changes.

## Why these three and not others

[01 · The three dimensions nobody should guess](01-architecture.md) names them.
They are not the only unknowns — they are the ones where a wrong guess is only
discovered after a case has been printed or a board fabricated:

| # | Dimension | Gates | Currently assumed |
|---|---|---|---|
| 1 | **Underside M.2 stack** — adapter + card + mated plugs + coax bend | Enclosure A thickness. [02 open questions](02-enclosure-a-upper.md#open-questions) calls it "now the only thing setting this box's thickness" | **15.9 mm**, from four stacked guesses |
| 2 | **RotoPD Pro envelope** — outline, height, mounting holes | Enclosure B footprint and the power board's carrier | **40 × 30 × 12 mm**, all invented |
| 3 | **Mated USB-C plug + cable bend radius** | Every USB-C opening in both boxes | **25 mm** |

Each maps to named values in `params.py`. Nothing else needs editing.

---

## 0 · Prerequisite — select the M.2 adapter

**Status: not selected.** This blocks measurement 1 entirely, and it is a
sourcing decision, not a measurement.

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
> board size excludes the heatsink, the adapter and cable bends. While the
> assembly is apart, also measure the **installed heatsink height**
> (`A.heatsink_h`, currently a 15 mm guess) — it is free to take at this point
> and it sets the other side of the Z stack.

## 2 · RotoPD Pro envelope

**Feeds:** `B.rotopd_x`, `B.rotopd_y`, `B.rotopd_h`, and the power board's
carrier footprint in [`pcb/layout.py`](../pcb/layout.py).

[06](06-power-board-schematic.md) resolved the *pinout* from vendor artwork but
states the outline, hole coordinates and diameter "need the `.kicad_pcb` or the
physical board, not another email."

**Prefer the vendor PCB files** — <https://github.com/CentyLab/RotoPD_Pro>
gives exact geometry without tolerance stack-up. Only measure if they are
unusable.

If measuring:

1. Outline X and Y at the extremes, including any overhanging connector body.
2. **Tallest component above the board**, which sets `B.rotopd_h`.
3. The two mounting holes flanking the USB-C jack: diameter, and X/Y from a
   defined board corner. Pick one corner and stay with it.
4. **Measure with the screw terminal already removed**, per the
   [2026-11-18 decision](../cad/params.py) to solder the VBUS path to its
   pads. Measuring it fitted records ~10 mm that will not exist.

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

---

## Recording results

For each value, in [`cad/params.py`](../cad/params.py):

1. Replace the number.
2. Replace the `source` string with how it was measured and on what date.
3. Set `verified=True`.

Then:

```sh
cad/.venv/bin/python cad/build.py --strict
```

`--strict` fails while any dimension remains a guess, so it goes green only
when the model is entirely real. The derived envelopes flip from `TBD` to `ok`
automatically — a derived value is verified only if every input is, so there
is no way to mark an envelope real while an input is still invented.

Watch for `violations()` in the same output: it checks constraints that do not
need measurements, such as the standoffs clearing the Pololu's 1.4 mm
below-board protrusion. A new measurement can break one of those.

## Sources

Specifications cited for the Orange Pi 5 Plus sockets and the adapter
disqualifiers are vendor and press publications, not measurements:

- [CNX Software — Orange Pi 5 Plus M.2 sockets](https://www.cnx-software.com/2023/05/10/orange-pi-5-plus-sbc-switches-to-rockchip-rk3588-soc-brings-dual-hdmi-2-1-dual-2-5gbe-m-2-pcie-sockets/)
- [CircuitPython Blinka — Orange Pi 5 Plus board listing](https://circuitpython.org/blinka/orange_pi_5_plus/)
- [Gateworks — M.2 E-key radios use one PCIe lane plus USB 2.0](https://www.gateworks.com/new-mini-pcie-to-m-2-e-key-adapter-for-wifi-radios/)
- [Example M-key to A+E key adapter listing, with the CNVi/CNVio2 exclusion](https://www.amazon.com/M-Key-Wireless-Network-Express-Adapter/dp/B0BGCWQY67)
- [CentyLab RotoPD Pro vendor repository](https://github.com/CentyLab/RotoPD_Pro)
