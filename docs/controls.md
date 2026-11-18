# Vezha — Physical Controls and Faceplate

Status: **design notes.** No switch, button, or faceplate geometry is
confirmed. Prices are rough estimates, not verified quotes. Panel cutouts
must come from the manufacturer's current drawing, never from a nominal
bushing diameter.

## Concept

A **removable front faceplate** on the upper router box, carrying:

- A locking `AIRPLANE` toggle on one shoulder, clamped directly to the faceplate
- Four low-profile buttons — `LINK`, `MAC`, `F1`, `F2` — soldered to a small
  daughterboard behind the faceplate, with only their caps coming through

Everything wires to the Orange Pi in the upper box. **Nothing mounts to the
removable power box.**

Keeping the display opening separate from the control openings means a display
change does not force a new button PCB.

## What the controls do

| Control | Default action | Why it earns a spot |
|---|---|---|
| `AIRPLANE` | `RADIOS / OFF`: disable both Wi-Fi radios and Bluetooth if present. Leave Ethernet up. | A maintained switch gives a physical position checkable without the display. Read it before bringing up wireless. |
| `LINK` | Tap: show uplink, management IP, portal status. Hold 2 s: retry the current uplink **without** changing its MAC. | The button most likely to get used when a hotel connection stalls. |
| `MAC` | Hold 2 s: rotate the **uplink** MAC and reconnect. Tap: show current MAC without changing it. | Makes a connection-breaking action deliberate. Leaves the client-facing AP untouched. |
| `F1` | Show/hide the Wi-Fi join QR code. | Harmless, useful default when adding a device. |
| `F2` | Show management address and a captive-portal help page. Reassignable later to cycle saved uplink profiles or toggle a guest AP. | Keep the default read-only until real use shows what gets reached for. |
| `RECOVERY` *(optional, hidden)* | Boot a known wired management profile. **No factory wipe.** | Reserve the footprint. Behind a pinhole by the Ethernet ports or inside the service cover — not on the front row. |

"Restore previous MAC" and "restore factory MAC" belong in the web UI as
separate actions, not on the front panel.

### rfkill is not an interlock

A Linux [`rfkill`](https://networkmanager.dev/docs/rfkill/) implementation is a
**software block, not a hardware interlock.** The switch position and the
radios' actual state can disagree.

Consequence for the design: put one small LED beside `AIRPLANE` and drive it
from **confirmed radio-off state**, not from the switch position. That gives
live feedback even when the display is showing a stale image.

### Feel

Give `MAC` a slightly recessed cap — it is the one control that breaks a
working connection. Keep `LINK`, `F1`, and `F2` at the same height.

## Hardware and mounting

| Part | Candidate | Where it mounts | Approx. USD |
|---|---|---|---|
| Airplane toggle | [NKK MN12LL4G01](https://www.nkkswitches.eu/products/Toggles/M/M2012LL4G01/) — gold contact, locking, two-position; replaces the older M2012LL4G01 | Through the **upper faceplate**, secured by its bushing hardware, solder lugs facing inward. Nominal panel cutout Ø6.5 mm — **check the current drawing** for full cutout and allowable panel thickness before machining. | ~$11 at [Mouser](https://www.mouser.com/ProductDetail/NKK-Switches/MN12LL4G01?qs=17ckDYBRdenkt/sbdVj6rg==) |
| Four front keys | [APEM Ultramec 6C + 10G caps](https://www.apem.com/en-us/pcb-switches/tactile-switches/ultramec-6c) | Solder to a **front-panel daughterboard** on standoffs behind the faceplate; caps protrude through. Switch body is 8 × 8 × 2.5 mm — that is **not** the cap opening or the key spacing. | ~$4–7 per key with cap (estimate) |
| No-PCB prototype alternative | [APEM IS ISR3SAD900](https://www.apem.com/en-us/panel-switches/pushbutton-switches/is/isr3sad900) | Each switch has its own threaded bushing, mounts straight to the faceplate, wires from behind. Easier one-off, bulkier than a shared key PCB. Use APEM's drawing for the cutout. | ~$10–15 each (estimate) |
| If the display becomes menu-driven | [APEM Ultranavimec](https://www.apem.com/pcb-switches/mec-tactile-switches-and-accessories) five-way | Five switches on a PCB under one Ø22.14 mm nav cap. Use **instead of** `F1`/`F2` if the display gets real menus. Keep `AIRPLANE` and `MAC` separate. | Not verified |

## Upper shell layout

**Outside.** `AIRPLANE` sits in a shallow pocket at one end of the faceplate —
enough finger clearance to pull the locking lever, but below the surrounding
case profile so it does not snag in a bag. Four keys in a single row below the
display if there is room; otherwise a 2 × 2 cluster on the opposite shoulder.

**Inside.** Key PCB parallel to the faceplate on four standoffs. Display on its
**own bracket**, so pressing buttons does not flex the display mount or load its
ribbon. Bring the toggle's solder-lug leads to the key PCB, then run one keyed,
detachable harness from that PCB to the Orange Pi.

For a printed prototype, print the faceplate separately and use a thin mounting
land or a small metal insert for the toggle rather than assuming its nut clears
the full printed wall.

## Order first

One NKK toggle and **one** 6C switch with a 10G cap. Print a small test coupon
with the toggle pocket and one key opening, then check:

1. The toggle pulls easily against the locking detent
2. The cap returns without rubbing
3. The key feels right at the intended recess depth

Commit to the four-key daughterboard only after that passes. These are the
dimensions and tolerances that cannot be settled without the actual parts and
final faceplate geometry.

## Open questions

- NKK MN12LL4G01 full panel cutout and max panel thickness — from the current
  drawing, not the nominal Ø6.5 mm.
- Ultramec 6C cap opening and key pitch — the 8 × 8 mm body does not give these.
- Whether the display gets real menus, which would swap `F1`/`F2` for the
  five-way nav control.
- How `AIRPLANE` is read and enforced in software, and what drives the
  confirmed-off LED. Relates to the uplink recovery design in
  [handoff.md](handoff.md).
