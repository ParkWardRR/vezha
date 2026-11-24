# 04 · Antennas — Selection, Placement, RF Test

Four internal flex antennas, **two per radio**, in the **replaceable antenna
cap** on top of [Enclosure A](02-enclosure-a-upper.md).

> [!IMPORTANT]
> **Placement changed on 2026-11-23.** The four narrow-wall positions below
> are **withdrawn**; all elements now mount inside the top cap. The part is
> **ordered**, and its datasheet figures have been read and are reproduced
> here rather than quoted from a catalog. The cap's mechanical spec is in
> [handoff · Phase 2](../handoff/README.md#phase-2--the-replaceable-antenna-cap).

Status: **the part is ordered; nothing is measured or bench-tested.** The
placement is proposed and **not RF-validated.** Prices are as discussed on
2026-11-17 and unverified against a live retail quote.

## The antenna cap — decided 2026-11-23

All elements mount to the **inside face of a nonmetallic, replaceable cap**
above the SBC, on the board edge **opposite the 40-pin header.**

| | |
|---|---|
| **Location** | Top of Enclosure A, above the SBC |
| **Replaceable** | Yes — lift-off, two rear-access M3 screws into heat-set inserts in the main case |
| **Mount surface** | Inside face of the cap, front and rear walls |
| **Reserve per element** | **42 × 7 mm** body footprint, plus cable-exit clearance |
| **Spacing** | **Space elements apart**; evaluate different orientations. No minimum set |
| **Keep clear of** | Metal of any kind, the heatsink, the PCB. **No carbon-filled filament**, no foil liner, no conductive coating, no metal trim |
| **Element coordinates** | **Not set** |
| **Element-to-radio map** | **Not set** — which element feeds which card is undecided |

### What this placement has to prove

> [!WARNING]
> **Concentrating all four elements in one cap is the specific risk.** The
> withdrawn layout deliberately spread them around the walls to keep the two
> radios physically separated — this document's own words were that it did so
> "rather than crowding all four elements under the top cap for easier
> routing." **Crowding them under the top cap is now the plan.**
>
> **Inter-radio isolation is what could fail**, and
> [the hard requirement](01-architecture.md#radio-topology) is two 5 GHz
> radios transmitting at once. The [bench test](#bench-test-before-committing)
> is no longer a formality.

Verification list, none of it done:

1. **Cable reach** — 100 ± 3 mm to each NIC, from a cap above a board standing
   on edge, with the far-face radio's lead crossing the board thickness
2. **MHF 4 mating** against the actual cards, both of them
3. **Clearance during cap removal** — the cap is designed to come off, so this
   is a routine action, not a service-only one
4. **RF performance with the cap installed**, not open

### Why the cap is the right place for them anyway

- **The cap is cheap and replaceable.** Reprinting a cap to move an element
  5 mm costs a few hours of print time; moving a wall-mounted element means
  reprinting the shell.
- **It is the top of the device**, furthest from the hand in normal grip, and
  the uplink is the marginal link.
- **It is guaranteed nonmetallic and empty.** No board, no heatsink, no
  battery, no fasteners through the chamber.
- **The elements come out with the cap**, so an antenna swap disturbs nothing
  else — the hedge this architecture was built around.

The cost is routing: **the leads got longer, not shorter**, and they now run
up past the cooling stack.

## The part — datasheet figures

**Taoglas FXP830.24.0100B**, ordered.
[Datasheet](https://www.taoglas.com/datasheets/FXP830.24.0100B.pdf) (rev.
SPE-14-8-022-G) · [product page](https://www.taoglas.com/product/fxp830-24-0100b/)

| | |
|---|---|
| Body | **42 ± 0.4 × 7 ± 0.3 mm**, polymer FPCB |
| Thickness | **Not given by the datasheet** — see below |
| Cable | **100 ± 3 mm** of **Ø0.81 mm** FEP coax, grey |
| Connector | **I-PEX MHF4**, HSC compatible, brass/gold |
| **Mated connector** | **2.1 ± 0.4 mm** tall, body 3.46 ± 0.6 mm long |
| Adhesive | **3M 467** double-sided, brown liner, pre-cut |
| Bands | **2400–2500 · 5150–5850 · 5925–7125 MHz** |
| Impedance · polarization · pattern | 50 Ω · linear · omnidirectional |
| Max input power | 10 W |
| Operating / storage temp | **−40 to +85 °C** |
| Weight | 7 g |

**Quantity ordered was not recorded.** The plan is four.

> [!CAUTION]
> **The body thickness is missing from the datasheet, and it matters less
> than the connector.**
>
> | Where | What it says |
> |---|---|
> | Introduction prose | `42*7*.01mm` → **0.01 mm** |
> | Specification table | `42 x 7 x mm` → **the field is blank** |
> | Mechanical drawing | **no thickness callout at all** |
>
> 0.01 mm is 10 µm, thinner than kitchen foil and not plausible for a polymer
> FPCB. A 0.1 mm figure has been quoted elsewhere but appears nowhere in the
> datasheet.
>
> **Design to the connector.** The mated MHF4 at **2.1 ± 0.4 mm** *is*
> dimensioned, is an order of magnitude larger than either candidate film
> thickness, and is what actually sets clearance behind the cap wall. Add the
> 3M 467 adhesive on top. This is why the cap brief says not to fix a recess
> depth until the real assembly is in hand.

Both Wi-Fi cards (Intel AX210, MediaTek MT7922/RZ616) use **MHF4** connectors.
Anything with an SMA male connector needs an MHF4-to-SMA **female** bulkhead
pigtail — not RP-SMA.

### The fallback is unchanged

If the internal pair struggles on weak hotel Wi-Fi, swap **only the uplink
pair** for two TE/Linx low-profile domes — direct MHF4, full 6 GHz coverage,
no whips protruding. The replaceable cap is what makes that a cheap
experiment rather than a redesign.

## Comparison

Gain is published dBi at 2.4 / 5 / 6 GHz. These are catalog figures measured in
free space, not performance in this enclosure.

| Antenna | Gain 2.4 / 5 / 6 GHz | Mount and connector | Approx. USD | Role |
|---|---|---|---|---|
| **Taoglas FXP830.24.0100B** | 2.14 / 5.33 / 6.49 free space; 3.46 / 6.86 / 8.09 on 2 mm ABS | 42 × 7 mm internal adhesive strip, 100 mm Ø0.81 mm MHF4 lead | $7.31 ea, ~$29 for four | ✅ **Ordered 2026-11-23.** No holes, no pigtails, no protrusions. Gain figures above are now confirmed against the datasheet. |
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

### Plastic, clearance, routing

| Design detail | What goes in the STL |
|---|---|
| Landing pads | A **smooth flat area** of plain plastic per 42 × 7 mm element, **not a deep recess** — recess depth cannot be set until the real assembly and adhesive are checked. 2 mm wall is the reference because Taoglas publishes data on 2 mm ABS. |
| Reserved area | Keep **ribs, screw bosses, embossed labels and cable clips out** of the candidate mounting areas on the cap's front and rear interior walls. |
| Ground plane | Aim for roughly **20 mm from the main ground plane** where practical — general guidance, **not a hard minimum**, and the datasheet states the part operates in free space, ground-plane independent. |
| Keep clear of | Metal of any kind, the heatsink, the PCB, the RTC cell. **No carbon-filled filament, foil liner, conductive coating or metal trim** in the cap. |
| Cable routing | Mock up all four **100 ± 3 mm** leads **before** fixing board and cap geometry. The two radios sit on **opposite faces** of a board standing on edge, so the far-face lead must cross the board thickness *and* reach the cap. Avoid tight bends and loops. **Check the cap lifts without tugging on the MHF4 connectors** — it is designed to come off. |
| Strain relief | **Below the seam**, accessible, and never clamping or sharply bending the micro-coax. |

### The withdrawn narrow-wall layout

> [!NOTE]
> **Superseded 2026-11-23 by [the cap](#the-antenna-cap--decided-2026-11-23).**
> Kept because the reasoning still describes the trade being made, and
> because the bench test is partly designed to find out whether abandoning it
> was a mistake.

Viewed from the screen side, each radio got **one horizontal strip and one
vertical strip**, inside the narrow plastic walls, with the broad faces clear:

| Radio | Placement | Orientation |
|---|---|---|
| **Intel AX210** — hotel uplink | Inside the **top wall**, toward the upper-left corner | Long axis **across the top** |
| **Intel AX210** — hotel uplink | Inside the **upper-right sidewall** | Long axis **down the side** |
| **MT7922** — private AP | Inside the **lower-left sidewall** | Long axis **down the side** |
| **MT7922** — private AP | Inside the **bottom wall** | Long axis **across the bottom** |

[Antenna layout sketch](antenna-layout.excalidraw "width=820 height=560")
*(draws the withdrawn layout)*

**Why it was arranged that way**, and what is lost by moving to the cap:

- **The top pair stayed above the normal grip** — that is the hotel uplink,
  the link most likely to be marginal. **The cap keeps this property and
  improves it**; the cap is higher than the top wall was.
- **The lower pair kept the two radios physically separated** rather than
  crowding all four elements under the top cap. **This property is lost.** It
  is the one the bench test has to re-earn through spacing and orientation
  inside the cap.
- **The crossed orientations** were a starting point for a device that gets
  picked up and rotated. **Still available** — orientation within the cap is
  explicitly open.

> [!WARNING]
> **Grip sensitivity was the reason the lower pair sat where it did.** With
> every element in the cap, grip loading changes character: the hand is now
> *always* below all four elements rather than over one pair. That is
> plausibly better, and it is **not** established. Test in **both hands**
> before bonding anything.

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

Keep the **replaceable cap as the fallback for the AX210.** The two
low-profile domes are a way to move the uplink elements away from the
enclosure internals and your hand — **not an automatic gain upgrade.**

Do not make this call from the Octane's published gain alone; its datasheet
figures were taken in free space, not on a handheld.

### Add one test condition for the cap

> [!IMPORTANT]
> **Test with the cap both screwed down and lifted.** The cap is a removable
> part with a 4–5 mm locating skirt and two M3 fasteners near its lower
> corners, and all four elements ride on it. Seating it changes the
> surroundings of every element at once — which is a failure mode the
> wall-mounted layout did not have.
>
> Also test **isolation between the two pairs specifically.** With all four
> elements in one small chamber, uplink-to-AP coupling is the measurement
> that decides whether this placement survives.

## Open questions

- **Element coordinates, spacing and orientation inside the cap** — none are
  set, and they are the main Phase 3 output.
  [Handoff · Phase 3](../handoff/README.md#phase-3--antenna-placement-and-rf-validation)
- **Which element feeds which radio.** The port map is undecided; the
  withdrawn layout had assigned it and that assignment is void.
- **Quantity ordered.** Four is the plan; the order quantity was not recorded.
- **Inter-radio isolation with all four elements in one cap** — the specific
  risk this placement takes on.
- Confirm the ANT-W63-**MHF4** datasheet gain; the table's figures are from the
  SMA variant.
- Whether the uplink needs external antennas at all is a bench-test outcome,
  not a design decision to make up front.
- Antenna connector type on the **second radio** is unconfirmed — the lead and
  mating assumptions here are based on MHF4. See
  [02-enclosure-a-upper.md](02-enclosure-a-upper.md).
- **6 GHz AP operation remains unverified.** Do not assume it. A tri-band
  antenna does not establish it. See [09-software-and-bringup.md](09-software-and-bringup.md).
- ~~No final antenna SKU~~ — **the Taoglas FXP830.24.0100B is ordered.**
