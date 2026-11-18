# 04 · PCB 1 — Front Control Board

The front panel of [Enclosure A](02-enclosure-a-upper.md). Read
[01-architecture.md](01-architecture.md) first.


Status: **design settled enough to buy test parts; mechanics not frozen.**
Buy the switches and wheel *before* committing the mechanical stack. Panel
cutouts must come from the manufacturer's current drawing, never from a
nominal bushing diameter.

> **Revision note.** This supersedes an earlier four-key layout
> (`LINK` / `MAC` / `F1` / `F2`). Adding the ANO navigation wheel makes two
> general-purpose function keys redundant, so the front row drops to three
> action keys and the wheel handles browsing and selection.

## Concept

A **removable front faceplate** on the upper router box, carrying:

- A locking `AIRPLANE` toggle on one shoulder, clamped through the faceplate
- Three action keys — `LINK`, `MAC`, `★` — on a custom front board
- An **ANO navigation wheel** for scrolling, navigation, and selection

Dedicated keys cover the actions worth a physical control; the wheel covers
everything menu-shaped, without duplicating its five buttons as separate keys.

Everything wires to the Orange Pi in the upper box. **Nothing mounts to the
removable power box.** Keep the display opening separate from the control
openings so a display change does not force a new button PCB.

The display is a **4.26" SPI e-paper panel** — see
[10-display.md](10-display.md). Its nine-wire cable is expected to land on
**this board** and share the single keyed harness to the Orange Pi, rather than
contending for the same 40-pin header. Reserve the connector.

## Bill of materials

| Qty | Part | Approx. USD | Where it mounts |
|---:|---|---:|---|
| 1 | [Adafruit #6310 — pre-soldered ANO I²C module](https://www.adafruit.com/product/6310) | $13.95 | Own standoffs or bracket behind the faceplate, wheel exposed. Short STEMMA QT cable to the front board. **This is the assembled I²C version**, not the bare wheel or the passive breakout. |
| 5 | [APEM Ultramec 6C](https://www.apem.com/en-us/pcb-switches/tactile-switches/ultramec-6c), exact PN `6CJ1NOPR` | $3.07 ea | Top-actuated SMD switches on the faceplate-facing side of the front PCB. **Populate three, keep two spares.** |
| 5 | APEM/MEC 10G caps — `10G09` black, `10G08` red | ~$1–2 ea (estimate) | Fit by hand after assembly. Black for `LINK` and `★`; red or recessed for `MAC`. The floating cap option helps align switch PCB to front panel. |
| 1 | [NKK locking toggle](https://www.nkkswitches.eu/products/Toggles/M/M2012LL4G01/), order `MN12LL4G01` | ~$11 | Clamps through the faceplate with its bushing and nut. Leads run to the front board — **do not mount it to the PCB.** Give the lever a protective recess with room to pull it. |

**Budget ~$45–50** for controls including spares, before cables, shipping, and
PCB assembly.

### Switch options

Three live paths. The 6C is still the default, but it is the only one that
cannot be machine-assembled *or* hand-soldered with an iron.

| | **APEM Ultramec 6C** `6CJ1NOPR` | **MEC Multimec 5G** `5GTH935` | **C&K** `KSC221JLFS` |
|---|---|---|---|
| Termination | **J-bend SMD** | **Through-hole** | SMD |
| Body | 8 × 8 mm, h **2.5 mm** | 10 × 10 mm, h **6.4 mm** | 6.2 × 6.2 mm |
| Force | ~3.6 N (LCSC lists 3.7 N) | 2.0 / **3.5** / 6.5 N options | ~2 N |
| Rated life | 3,000,000 cycles | **10,000,000 cycles** | — |
| Caps | **10G** series (`10G09`/`10G08`) | `1Z` / `1S` families — **not 10G** | None — needs a custom plunger |
| JLC can place it | ❌ 0 stock | ❌ 0 stock (DigiKey instead) | ✅ 16,623 in stock |
| Hand assembly | Paste + hot air only | **Iron** | Paste + hot air only |

**The through-hole path is real but it is not a swap.** Multimec 5G is the 6C's
through-hole sibling and 3.5 N sits right on the 6C's ~3.6 N, so the *feel*
carries over and rated life triples. What does not carry over:

- **The caps.** APEM lists the 10G series against the 6C and the `1Z`/`1S`
  families against the 5G, **with no overlap.** `10G09` and `10G08` are not
  listed as fitting the 5G. Going through-hole means reselecting both caps.
- **The footprint**, 10 × 10 mm against 8 × 8 mm.
- **The body height** — 6.4 mm against 2.5 mm. That is **+3.9 mm between the PCB
  and the faceplate**, which feeds straight into standoff height and the test
  coupon in [Mechanical test coupon](#mechanical-test-coupon).

Neither APEM page states that the two series are mechanically interchangeable.
Treat a 6C → 5G move as a footprint and faceplate change, not a part
substitution. *(APEM's own 5G product page prints "35 N" where the series page
says 3.5 N — a site glitch, but confirm the force on the datasheet.)*

The C&K alternative stays the only switch here JLC can actually place, at
~$0.46 in hundreds. It is **not a drop-in** either: different footprint, and it
needs a separate plunger design rather than the MEC cap system.

So the choice is a three-way trade, not a fallback ladder: **6C** keeps the
premium cap system and costs you a hot-air station; **5G** gets you an iron and
longer life at the price of new caps, a new footprint and 3.9 mm more stack;
**C&K** gets a fully machine-assembled board at a lighter 2 N with plunger
design work. The test coupon decides it.

## Control behavior and wiring

| Control | Default behavior | Connection |
|---|---|---|
| `AIRPLANE` | Maintained `RADIOS / OFF`. Read it before bringing up wireless; keep Ethernet available. | **Dedicated Orange Pi GPIO, independent of the ANO.** |
| `LINK` | Tap: uplink / IP / portal status. Hold: retry the uplink. | One GPIO per key, switch to ground. |
| `MAC` | Tap: show current uplink MAC. Hold 2 s: rotate it and reconnect. Factory-MAC restore stays in the menu. | Same switch as `LINK`, but **cap set lower** so it feels different and is harder to hit by accident. |
| `★` | Wi-Fi join QR code; user-assignable later. | One GPIO. For a second shortcut, reserve a fourth footprint but **do not cut the first faceplate for it.** |
| ANO wheel | Rotate to browse, center to select, left to go back. Leave the other directions unassigned until there is a real use. | 3.3 V, GND, SDA, SCL over STEMMA QT; default address `0x49`. An `INT` wire or test pad is optional for event-driven input — **it is not carried on the four-wire QT cable.** |
| `RECOVERY` *(optional, hidden)* | Boot a known wired management profile. **No factory wipe.** | Reserve the footprint behind a pinhole by the Ethernet ports or inside the service cover — not on the front row. |

### rfkill is not an interlock

`AIRPLANE` on a GPIO is a **software-controlled radio block**, not a hardware
disable, unless a verified hardware path is added. A Linux
[`rfkill`](https://networkmanager.dev/docs/rfkill/) implementation can disagree
with the switch position.

Consequence: the `AIRPLANE` indicator must be driven from **confirmed
radio-off state**, not from switch position. That gives live feedback even when
the display is showing a stale image. See
[RGB indicators](#rgb-indicators) below.

With the e-paper display now chosen, **a stale image is the normal state** — a
full redraw takes 4 s and the panel is not meant to be refreshed constantly.
That promotes the RGB indicators from a nicety to the only real-time feedback
the panel has. See [10-display.md](10-display.md#what-this-does-to-the-ui).

## RGB indicators

**One independently programmable RGB indicator beside each control** —
`AIRPLANE`, `LINK`, `MAC`, `★`.

Keep the APEM 6C switches and their **opaque** caps. The light goes through a
**separate flush diffuser above each label**, not through the keycap. This gives
a readable panel without changing how the buttons feel.

### Parts (Rev A)

| Part | Choice |
|---|---|
| LED driver | [TI TLC59116IPWR](https://www.ti.com/product/TLC59116) — 16-channel I²C constant-current driver. Four RGB LEDs use 12 channels, leaving four spare. Independent 8-bit brightness per color channel, so the Orange Pi sets color *and* brightness per indicator. |
| LEDs | Four **common-anode** SMD RGB LEDs on the **faceplate-facing side** of the PCB. Short frosted light pipe or diffuser each, with **opaque walls between indicators** so light does not bleed into the neighbouring opening. **Pick the LED and its optic together before finalizing standoff height.** |
| Wiring | Shares the Orange Pi's 3.3 V I²C bus with the ANO, but **strapped to a distinct address** from the ANO's `0x49`. Switches stay separate GPIO inputs. LED anodes off the upper box's **5 V** rail, driver logic on **3.3 V**. Check combined I²C pull-ups on the assembled board. |
| Brightness | Set the driver's current-set resistor for a modest peak current, then tune each color in software. Start from a **dim hotel-room preset**. Use short pulses for acknowledgements rather than constant blinking — the driver's group blink is shared, so per-key patterns must be done in software. |

### What the lights mean

| Control | Default behavior |
|---|---|
| `AIRPLANE` | Solid amber **only after the router confirms its radios are blocked.** Meaning is fixed — not user-assignable. |
| `LINK` | Green online · amber captive portal or reconnecting · red uplink down. |
| `MAC` | Normally dark. Pulse amber while the change is in progress, then briefly green on success or red on failure. Ongoing internet status stays with `LINK`. |
| `★` | User-configurable. Default dim white while the Wi-Fi QR page is open, dark otherwise. |

### Stale-indicator hazard

If `AIRPLANE` means *confirmed*, that indicator needs a way to **go dark when
the router stops reporting status.** An I²C driver retains its last setting
while powered, so an Orange Pi crash would otherwise leave stale amber lit —
the panel would claim the radios are off when nothing is confirming it.

- **Reserve a footprint** for a watchdog-controlled reset on the driver.
- **For Rev A without it:** treat the toggle as the *requested* state and the
  LED as the *last software-confirmed* state. Neither is a hardware RF
  guarantee.

### Optical prototype

Prototype **one key and one light pipe in the same printed coupon** as the
mechanical test below, before ordering the faceplate. Check it in a dark room
*and* in daylight. The target is an even, readable dot with **no visible
hotspot and no glow leaking around the keycap.**

The driver is in JLCPCB stock (see below); the RGB LED has no part number yet,
so its stock and optic pairing are still open. Confirm both in the assembly
quote before locking footprints.

## Before sending the board to JLCPCB

**Assembly availability and switch choice are separate decisions.**

JLCPCB catalog check, 2026-11-17 — codes and price ladders in
[08-sourcing.md](08-sourcing.md#looked-up-so-far):

| Part | Code | JLC can place it? |
|---|---|---|
| TI `TLC59116IPWR` | `C131194` | ✅ Yes — 3,611 in stock |
| APEM/MEC `6CJ1NOPR` | `C5518654` | ❌ No — 0 stock, no pre-order |
| C&K `KSC221JLFS` *(alt)* | `C221726` | ✅ Yes — 16,623 in stock |
| RGB LED | — | 🔴 No part number chosen |

**Only the switch is a real sourcing problem.** The toggle is panel-mount with
leads to the board and the caps press on by hand — see the
[bill of materials](#bill-of-materials) above. Neither was ever going to be
machine-placed, so their zero stock at JLC is not a blocker, just a note that
they come from DigiKey. The ANO is a module on its own standoffs.

For the switch, keeping the 6C means **leaving the three positions unpopulated**
and installing DigiKey parts with paste and hot air or a small reflow setup. The
6C uses **J-leads**, so do not plan around hand-soldering with an iron — that
constraint is the strongest argument for the through-hole 5G in
[Switch options](#switch-options), which an iron handles.

Restocking does not change the economics — JLC quotes the 6C at $3.94 in
hundreds against $3.07 at DigiKey.

With the switch hand-installed on any of the three paths, PCB 1's JLC BOM comes
down to the **driver, the RGB LEDs, passives and connectors** — all placeable
once the LED is chosen. That is the board to quote.

## Mechanical test coupon

Buy the ANO and switches **before** freezing the mechanical stack. Print a small
faceplate coupon with the wheel opening and **two cap openings — one flush, one
recessed.** With the real parts mounted, check:

1. All four wheel directions and the center press without the wheel rubbing
2. Caps return freely with no preload
3. The recessed `MAC` position feels distinct from the flush keys
4. The toggle pulls easily against its locking detent

If the through-hole 5G is in play, **coupon both switch bodies.** They differ by
3.9 mm in height and take different caps, so one coupon cannot answer for both.

Then set standoff height and PCB outlines.

That test says more about how premium the finished controls feel than the
switch force spec alone.

## Shell layout

**Outside.** `AIRPLANE` in a shallow pocket at one end of the faceplate — enough
finger clearance to pull the locking lever, but below the surrounding case
profile so it does not snag in a bag. Action keys in a row below the display;
wheel positioned for thumb reach.

**Inside.** Front PCB parallel to the faceplate on four standoffs. Display on
its **own bracket**, so pressing buttons does not flex the display mount or load
its ribbon. Toggle leads to the front board, then one keyed, detachable harness
from that board to the Orange Pi.

The e-paper's **107 × 64 mm driver board** mounts behind the panel and needs its
own space — it is larger in one axis than the Orange Pi itself. The faceplate's
minimum size is now set by the display window, not by the control row.

For a printed prototype, print the faceplate separately and use a thin mounting
land or a small metal insert for the toggle rather than assuming its nut clears
the full printed wall.

## Open questions

- ~~JLCPCB assembly sourcing for `6CJ1NOPR` and the TLC59116IPWR driver~~ —
  checked 2026-11-17: driver in stock, switch not. RGB LED sourcing stays open
  because no part number is chosen.
- **Switch termination: SMD 6C or through-hole 5G.** Decides the footprint, the
  cap series, and 3.9 mm of standoff height. See
  [Switch options](#switch-options).
- Which cap replaces `10G09`/`10G08` if the 5G is chosen — the `1Z` and `1S`
  families are what APEM lists, none of them verified here.
- Display connector on this board, and whether SPI is routed through it to the
  Orange Pi — see [10-display.md](10-display.md#interface-and-wiring).
- Whether paged e-paper navigation suits the ANO wheel at all —
  [10](10-display.md#what-this-does-to-the-ui).
- RGB LED part and its matching optic — must be chosen as a pair, and they set
  the standoff height.
- I²C address strapping for the TLC59116 (must not collide with ANO `0x49`),
  and combined bus pull-up value with both devices populated.
- Whether Rev A carries the watchdog-reset footprint for the LED driver.
- NKK MN12LL4G01 full panel cutout and max panel thickness, from the current
  drawing (nominal is Ø6.5 mm).
- ANO wheel opening diameter and standoff height — set from the test coupon.
- Whether 3.6 N is acceptable, or the build moves to the C&K KSC at ~2 N with a
  new footprint and plunger.
- How `AIRPLANE` is read and enforced in software, and what drives the
  confirmed-off LED. Relates to uplink recovery in [09-background.md](09-background.md).
