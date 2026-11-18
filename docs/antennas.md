# Vezha — Antenna Selection and Layout

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
| TE/Linx ANT-W63-WRT-MHF4 | 4.5 / 4.5 / 6.4 — **these are the WRT SMA variant's numbers; confirm the MHF4 datasheet before treating them as identical** | Fixed panel-mount dome, direct MHF4 lead. SMA version listed at 27.8 mm max height. | $15.31 ea, ~$31/pair | **Swap-in for the uplink** if grip, battery, or display compromise the internal pair. |
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
misreading worth stating explicitly. The actual starting layout is:

- **Top edge** and **upper right sidewall** → AX210 pair (hotel uplink)
- **Lower left sidewall** and **bottom edge** → MT7922 pair (private AP)

The broad screen and back faces stay clear in this first layout.

[Antenna layout sketch](antenna-layout.excalidraw "width=820 height=560")

The strips sit **inside the narrow plastic walls** — A1 flat against the
underside of the top wall, A2 flat against the inside of the right wall, B1 and
B2 mirroring on the left and bottom. They are not on the screen face.

| Design detail | What goes in the STL |
|---|---|
| AX210 (uplink) | Reserve the two upper corners, above the normal grip. One strip's long axis across the top, the other vertical down an upper sidewall near the opposite corner. A layout to test, not a validated optimum. |
| MT7922 (private AP) | Two other perimeter positions, as far from the AX210 elements as the case and lead lengths allow. One horizontal, one vertical. Do not bunch all four under the same top cap just to simplify routing. |
| Plastic and clearance | Flat landing pad on the inside of plain plastic for each strip. 2 mm ABS wall is a useful reference because Taoglas publishes data for it. Aim for ~20 mm from the main ground plane where practical — general guidance, not a hard minimum for this part. Keep strips out from directly behind the display, battery, and heatsink. **No carbon-filled filament in antenna zones.** |
| Cable routing | Mock up all four 100 mm leads **before** fixing board and antenna positions — the leads may not reach every corner. Route coax away from other elements, avoid tight bends and loops, and leave the MHF4 connectors enough slack that removing the lid does not tug on them. |

## Bench test before committing

Tape the strips in place and close the case. Do not peel the adhesive backing
or print dedicated mounts until this passes.

Against a **fixed 5 GHz upstream AP**, compare uplink RSSI, retry rate, and
end-to-end throughput across these conditions:

1. Case open vs. closed
2. Sitting on a table vs. held in a normal grip
3. Private radio idle vs. carrying traffic on a different 5 GHz channel

Then read the results:

- **Degrades mainly when the private radio is busy** → self-interference. Try
  more physical separation and wider channel spacing before buying antennas.
- **Degrades mainly on closing the case or gripping it** → move the AX210 pair
  first. Only then try the domes.

Do not make this call from the Octane's published gain alone; its datasheet
figures were taken in free space, not on a handheld.

## Open questions

- Confirm the ANT-W63-**MHF4** datasheet gain; the table's figures are from the
  SMA variant.
- No final antenna SKU, quantity, or geometry is committed.
- Whether the uplink needs external antennas at all is a bench-test outcome,
  not a design decision to make up front.
- 6 GHz AP operation remains unverified; do not assume it. See
  [handoff.md](handoff.md).
