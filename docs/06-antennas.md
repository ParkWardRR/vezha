# 06 · Antennas — Selection, Placement, RF Test

Four internal flex antennas, **two per radio**, inside the narrow walls of
[Enclosure A](02-enclosure-a-upper.md).

Status: **research notes.** Nothing here is purchased, measured, or
bench-tested. Gain figures are manufacturer-published, and prices are as
discussed on 2026-11-17 and unverified against a live retail quote. Treat
every part number and price as a candidate to re-check before ordering.

## Leading plan

Start with **four Taoglas flex antennas, two per radio**, mounted inside the
enclosure walls, and design the STL with a **replaceable top cap**.

The top cap is the hedge. If the internal AX210 pair struggles on weak hotel
Wi-Fi, swap only that pair for two TE/Linx low-profile domes — direct MHF4,
full 6 GHz coverage, no whips protruding. That keeps the pocketable default
without closing the door on a better uplink.

Both Wi-Fi cards (Intel AX210, MediaTek MT7922/RZ616) use **MHF4** connectors.
Anything with an SMA male connector needs an MHF4-to-SMA **female** bulkhead
pigtail — not RP-SMA.

## Comparison

Gain is published dBi at 2.4 / 5 / 6 GHz. These are catalog figures measured in
free space, not performance in this enclosure.

| Antenna | Gain 2.4 / 5 / 6 GHz | Mount and connector | Approx. USD | Role |
|---|---|---|---|---|
| **Taoglas FXP830.24.0100B** | 2.14 / 5.33 / 6.49 free space; 3.46 / 6.86 / 8.09 on 2 mm ABS | 42 × 7 mm internal adhesive strip, 100 mm MHF4 lead | $7.31 ea, ~$29 for four | **Default pick.** No holes, no pigtails, no protrusions. |
| TE/Linx ANT-W63-WRT-MHF4 | 4.5 / 4.5 / 6.4 — **these are the WRT SMA variant's numbers; confirm the MHF4 datasheet before treating them as identical** | Fixed panel-mount dome, direct MHF4 lead. SMA version listed at 27.8 mm max height. | $15.31 ea, ~$31/pair | **Swap-in for the uplink** if grip or battery compromise the internal pair. |
| TE/Linx ANT-W63WS1-SMA | 7.7 / 5.8 / 4.7 | 85.5 mm tilting blade, SMA male → needs MHF4-to-SMA bulkheads | $12.27 ea, ~$25/pair before pigtails | Better for tabletop use with adjustable orientation. Not pocketable. |
| Octane SA-2400/5800 | 2.2 @ 2.45 GHz / 4.4 @ 5.65 GHz / **no full 6 GHz coverage** (spec stops at 6.0 GHz) | 67 mm rigid stub, SMA bulkhead → needs MHF4-to-SMA bulkheads | ~$79 ea on a GSA schedule; **not a verified retail price** | Ruggedness only. No demonstrated gain advantage and poor value here. |

### How to read those numbers

The band that matters is **5 GHz**, since both links must run there
simultaneously. The Taoglas lists 5.33 dBi in free space against the Octane's
4.4 dBi at one specific frequency — that is not an apples-to-apples win for
either part.

Two reasons not to pick on catalog gain:

1. **Peak gain is the strongest direction, not coverage in all directions.** A
   handheld unit gets held and rotated arbitrarily; pattern matters more than peak.
2. **Mounting changes the result.** Taoglas's own data shows the FXP830 reading
   higher on 2 mm ABS than in free space.

Buy the dome, if needed, to get the element out from behind the device's metal
and your hand — not because its catalog gain is higher.

## Enclosure layout

**Not** one antenna each on front, top, back, and bottom. That was a
misreading worth stating explicitly.

### The four positions

Viewed from the screen side. Each radio gets **one horizontal strip and one
vertical strip.**

| Radio | Placement | Orientation |
|---|---|---|
| **Intel AX210** — hotel uplink | Inside the **top wall**, toward the upper-left corner | Long axis **across the top** |
| **Intel AX210** — hotel uplink | Inside the **upper-right sidewall** | Long axis **down the side** |
| **MT7922** — private AP | Inside the **lower-left sidewall** | Long axis **down the side** |
| **MT7922** — private AP | Inside the **bottom wall** | Long axis **across the bottom** |

[Antenna layout sketch](antenna-layout.excalidraw "width=820 height=560")

The strips sit **inside the narrow plastic walls.** The broad screen and back
faces stay clear.

### Why this arrangement

- **The top pair stays above the normal grip** — that is the hotel uplink, the
  link most likely to be marginal.
- **The lower pair keeps the two radios physically separated** rather than
  crowding all four elements under the top cap for easier routing.
- **The crossed orientations** are a starting point for a device that gets
  picked up and rotated, not a guarantee of better performance.

> [!WARNING]
> **The lower pair is the one to watch for grip sensitivity.** Test it in
> **both hands** before locking the mounts into the STL. A hand over the
> lower-left sidewall is a natural way to hold this device.

### Plastic, clearance, routing

| Design detail | What goes in the STL |
|---|---|
| Landing pads | A flat pad of **plain plastic** for each 42 × 7 mm strip. 2 mm ABS is the reference wall because Taoglas publishes data for it. |
| Ground plane | Aim for roughly **20 mm from the main ground plane** where practical — general guidance, **not a hard minimum** for this part. |
| Keep clear of | Battery, heatsink. **No carbon-filled filament** in antenna zones. *(The display keep-out is gone — [v1 is headless](01-architecture.md#the-v1-scope-cut) — which frees the whole front face.)* |
| Cable routing | Mock up all four **100 mm** leads **before** fixing board and antenna positions — they may not reach every corner, and the two radios sit on **opposite faces** of the Orange Pi. Avoid tight bends and loops. **Check the lid opens without tugging on the MHF4 connectors.** |

## Tri-band: what it changes and what it doesn't

**You do not need separate strips for 2.4, 5, and 6 GHz.** The candidate
[Taoglas FXP830](https://www.taoglas.com/product/fxp830-24-0100b/) covers all
three bands.

> The count of four comes from **two antenna paths per radio** — not from the
> number of bands.

Two things a tri-band antenna does **not** do:

1. It does not establish that the MT7922 can run a **6 GHz AP** in Vezha's
   software configuration. That remains unverified — see
   [Open questions](#open-questions).
2. It does not change the first acceptance test, which is still **simultaneous
   5 GHz** uplink and private AP.

The ~$29-for-four figure is an estimate, not a live quote.

## Bench test before committing

Tape the strips in place and close the case. Do not peel the adhesive backing
or print dedicated mounts until this passes.

Against a **fixed 5 GHz upstream AP**, compare uplink RSSI, retry rate, and
end-to-end throughput across these conditions:

1. Case **open vs. closed**
2. **On the table vs. held** in a normal grip — and in **both hands**
3. Private radio **idle vs. carrying traffic** on a different 5 GHz channel

### Record the downstream client too

> [!IMPORTANT]
> Also record the **downstream client's RSSI and retry rate**, not just the
> uplink's. Without it, a **grip problem on the lower pair** looks identical to
> a weak hotel uplink — and the two have opposite fixes.

### Reading the results

| Symptom | Diagnosis | Try first |
|---|---|---|
| Degrades mainly when **both radios are busy** | Self-interference | **Wider channel separation** and more physical separation — before buying antennas |
| Degrades mainly on **closing or gripping** the case | Enclosure or hand loading | **Move the affected pair first.** Only then try different antennas |
| Downstream degrades but uplink is fine | Lower pair grip sensitivity | Reposition the lower pair |

Keep the **replaceable top cap as a fallback for the AX210.** The two
low-profile domes are a way to move the uplink elements away from the
enclosure internals and your hand — **not an automatic gain upgrade.**

Do not make this call from the Octane's published gain alone; its datasheet
figures were taken in free space, not on a handheld.

## Open questions

- Confirm the ANT-W63-**MHF4** datasheet gain; the table's figures are from the
  SMA variant.
- No final antenna SKU, quantity, or geometry is committed.
- Whether the uplink needs external antennas at all is a bench-test outcome,
  not a design decision to make up front.
- Antenna connector type on the **second radio** is unconfirmed — the lead and
  mating assumptions here are based on MHF4. See
  [02-enclosure-a-upper.md](02-enclosure-a-upper.md).
- **6 GHz AP operation remains unverified.** Do not assume it. A tri-band
  antenna does not establish it. See [09-background.md](09-background.md).
