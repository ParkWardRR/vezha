# 02 · Enclosure A — Upper Router Box

The router itself. Holds the Orange Pi, both radios, the adapter, all four
antennas and storage.

> [!IMPORTANT]
> **v1 is headless.** No display, no keys, no wheel, no toggle, no indicators,
> no front PCB — see [01 · The v1 scope cut](01-architecture.md#the-v1-scope-cut).
> This box is a sealed shell with four internal antennas and a USB-C power
> inlet. **Its size is now set by the Orange Pi and the antennas**, not by a
> display window or a control row.

Read [01-architecture.md](01-architecture.md) first.

> [!WARNING]
> No dimension here is a verified installed measurement. The board and card
> sizes are published figures for the bare parts. **Heatsink, adapter, mated
> antenna plugs, and cable bends are all excluded** and are exactly what will
> decide whether this closes.

## Contents and mounting

| Part | Dimensions | Mounting and clearance |
|---|---|---|
| **Orange Pi 5 Plus** | 100 × 75 mm board | On enclosure standoffs. **Clearance required on both faces** — E-key socket on top, M-key socket underneath. Published size excludes installed heatsink, adapter, and cable bends. |
| **Intel AX210** (uplink) | M.2 2230 · 22 × 30 × 2.4 mm | Slides into the **top-side E-key socket**, screws down at the 2230 standoff. Two MHF4 antenna leads snap onto the card. Wi-Fi over PCIe, Bluetooth over USB. |
| **Second Wi-Fi card** (private AP) | 22 × 30 mm **if 2230** — height unconfirmed | Mounts in the **adapter's** E-key socket with its own retaining screw. MT7922/RZ616 is a candidate, **not a locked part.** Verify antenna connector type and 5 GHz AP operation on the target Linux image before committing. |
| **M-key → E-key adapter** | **Installed size unverified** | Male M-key edge into the Orange Pi's **underside** socket; second radio into the adapter's female E-key socket. The host accepting 2280 modules does **not** tell you the adapter's size or the installed stack height. Choose a specific adapter **that routes PCIe**, then measure it with card and antenna plugs installed. |
| **4 × flex antennas** | 42 × 7 mm each, 100 mm MHF4 lead | Inside the narrow walls. Full placement in [06-antennas.md](04-antennas.md). |
| **Storage** | eMMC discussed, unconfirmed | — |
| **RTC backup cell** | 20 mm coin cell + holder, or a shrink-wrapped cell on a lead | On the Orange Pi's **2-pin 1.25 mm RTC header**. Placement is a thermal keep-out problem, not a space one — see [RTC backup cell](#rtc-backup-cell). |
| ~~Display~~ | — | **Retired in v1.** Was a Waveshare 4.26" e-paper whose 107 × 64 mm driver board set the faceplate's minimum size. [10](retired/display-epaper.md) |
| ~~Faceplate~~ | — | **Retired in v1.** No controls to carry, so no removable front part and no openings. |
| ~~PCB 1~~ | — | **Retired in v1.** [04](retired/pcb-1-front-control.md) · [12](retired/pcb-1-schematic.md) |

### What the cut removes from this box

Worth stating plainly, because it changes the mechanical problem rather than
just shortening the parts list:

- **No faceplate openings at all** — no display window, no key openings, no
  wheel opening, no RGB diffusers, no toggle bushing. The shell can be a
  closed form with only the USB-C inlet and any service access breaking it.
- **No printed plungers.** These were the highest-risk mechanical item in the
  build, needing a test coupon at two or three lengths before any faceplate
  could be ordered. That gate is gone.
- **An entire rigid layer leaves the Z stack** — faceplate, plunger travel,
  PCB 1 on its standoffs, the glass, and the driver board behind it. What
  remains is shell, SBC, and the underside M.2 stack.
- **Standoff height is no longer coupled to RGB optics.** It is now set only by
  the underside adapter stack, which was always the binding constraint.

## The double-sided problem

The single most important mechanical fact about this build:

> **One radio sits above the Orange Pi, the other hangs below it on an
> adapter.** The board cannot be mounted flat against a floor or a lid.

Standoff height has to account for the underside stack — adapter, plus card,
plus mated antenna plugs, plus the bend radius of the coax leaving them. That
figure is unmeasured and is one of the
[three dimensions nobody should guess](01-architecture.md#the-three-dimensions-nobody-should-guess).

## Antenna zones

Summarised here; full detail and test plan in [06-antennas.md](04-antennas.md).

- Four strips **inside the narrow walls** — top edge, upper-right sidewall,
  lower-left sidewall, bottom edge
- Broad screen and back faces stay **clear**
- Flat landing pad of plain plastic for each; 2 mm ABS is the reference wall
- Target roughly **20 mm from the main ground plane** where practical — a
  layout target, not a pass/fail spec
- **Not** directly behind battery or heatsink *(the display constraint is gone
  with the display — one fewer keep-out competing for wall space)*
- **No carbon-filled filament** anywhere in an antenna zone

### Lead routing is a layout input, not an afterthought

The leads are **100 mm**. Mock up all four **before** fixing board and antenna
positions — they may not reach every corner from where the cards actually sit,
and the two radios are on opposite faces of the board.

Check that **the lid opens without tugging on the MHF4 connectors.** Those are
tiny and they are the thing that will break during service.

## Shell and access

With no controls to carry, the removable faceplate loses its reason to exist as
a separate part. What replaces it is a decision, not a given:

- **Service access is still required.** The MHF4 connectors are the thing that
  will break during service, and the underside radio cannot be reached without
  opening the box. Whether that is a removable lid, a base plate, or a split
  along the seam is **open** — but it should be chosen for *assembly and
  service*, which is now the only thing driving it.
- **Keep the broad faces clear** for the reasons in
  [Antenna zones](#antenna-zones), unchanged by the cut.
- **One USB-C opening**, positioned per [Power entry](#power-entry) below.
- If a service cover is used, it is a candidate home for the **printed Wi-Fi
  join label** that replaced the `★` key's QR screen.

## Power entry

Enclosure A receives **5 V power only**, over a short **USB-C cable** from
Enclosure B into the Orange Pi's **dedicated USB-C power input**. That is the
whole interface — no signal, no telemetry.

Full rationale and the 3 A caveat:
[01 · Crossing the seam](01-architecture.md#crossing-the-seam).

**Mechanical consequences for this shell:**

- A **USB-C opening** positioned so the cable reaches the Orange Pi's power
  input without a tight bend
- **The enclosure latch retains the boxes**, not the cable
- Size the case around the **mated plug and its bend radius**, not the
  receptacle footprint
- No contact array, no alignment features, no detect pin — the earlier
  7-contact seam is removed

**No RF crosses the seam** — the power box must come off without disturbing
any PCIe or antenna connection.

## RTC backup cell

**Added 2026-11-18.** The Orange Pi 5 Plus has an onboard RTC and a **2-pin
1.25 mm backup-battery header**, so keeping time across a dead box costs a cell
and a lead — there is no RTC module to design in and no board change.

**Why a travel router cares, when a desk SBC does not:** Vezha is **fully dead
between trips** (no internal cell is decided), and the power box detaching or
the bank being unplugged means **hard power-cuts are the normal shutdown** — so
`fake-hwclock`'s saved timestamp is routinely stale. The first thing the box
does on arrival is join a strange network, and most of that work is
clock-sensitive:

| Depends on the clock | What a wrong one does |
|---|---|
| **Captive portal over HTTPS** | `certificate not yet valid` → the portal never renders → no uplink → **no NTP to fix the clock with** |
| **WireGuard** | The handshake carries a TAI64N timestamp; a peer **silently drops** handshakes older than the last it saw. A clock that rolled backwards = a tunnel that never comes up, with no visible error |
| **Tailscale** | TLS to the control plane fails; node key expiry is misjudged |
| **DNSSEC** | Signature inception/expiry rejects every answer |
| **Logs** | On a [headless v1](01-architecture.md#the-v1-scope-cut) with no at-rest status, timestamps are the only forensic surface left |

Without the cell this is not fatal — `fake-hwclock` / `systemd-timesyncd`
restore the last saved time and keep the clock monotonic, which covers the
WireGuard case most of the time. **The cell buys "correct at power-on" instead
of "usually recovers",** on a device that has to work on a hostile network
before anyone can intervene.

> [!WARNING]
> **Chemistry is unresolved, and it is not a free choice.** Confirm whether the
> header **trickle-charges** before fitting anything. These headers are
> typically a plain *backup* input, in which case an ML/LIR rechargeable never
> recharges — but if the board does charge it, a **primary CR2032 must not be
> fitted to it.** Read the board's schematic, not the wiki table.

**Mechanical consequences for this shell:**

- **Thermal is the binding constraint, not volume.** Coin cells are commonly
  rated to **60 °C**, inside a sealed box that already has an
  [unmeasured thermal problem](#thermal). Keep it off the heatsink and clear of
  the underside M.2 stack.
- **Not in an [antenna zone](#antenna-zones).** A 20 mm metal disc against a
  wall strip is the same keep-out the battery already had.
- **Reachable at service**, like the MHF4 connectors — a cell that needs the
  antennas disturbed to replace is a cell that never gets replaced.
- The lead is short. Mock it up with the board where it actually sits.

Verify with `cat /proc/driver/rtc` at
[bring-up step 2](09-software-and-bringup.md#bring-up-order).

## Thermal

Unresolved and untested. The stated preference is hardware that does not need
dedicated cooling, but **two Wi-Fi 6E radios under simultaneous sustained
load is exactly the case nobody has measured.** A heatsink exists in the
clearance budget above; whether it is sufficient is open.

Antenna zones and heatsink placement are in direct tension. Resolve it with
the RF test in [06-antennas.md](04-antennas.md) rather than by assumption.

## Open questions

- Installed stack height on the underside (adapter + card + mated plugs) —
  **now the only thing setting this box's thickness**
- Which M-key-to-E-key adapter, confirmed to route PCIe
- Second radio part, form factor height, and antenna connector type
- Heatsink size and whether active cooling is needed
- **RTC cell chemistry** — primary or rechargeable, decided by whether the
  Orange Pi's RTC header trickle-charges. Its mounting location is a thermal
  keep-out, [above](#rtc-backup-cell)
- **How the box opens for service** — lid, base plate, or seam split. Driven
  by assembly and MHF4 access, nothing else.
- Whether a replaceable top cap survives as the fallback for swapping the
  uplink antennas — it no longer has a faceplate to be part of
- ~~Display model and bracket geometry~~ — moot, [v1 is headless](01-architecture.md#the-v1-scope-cut)
- ~~PCB 1 outline and standoff height~~ — moot, there is no PCB 1
