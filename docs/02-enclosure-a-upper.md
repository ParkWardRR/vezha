# 02 · Enclosure A — Upper Router Box

The router itself. Holds the Orange Pi **on edge**, both radios, the adapter,
storage, a fan, an **OLED front panel**, and a **replaceable antenna cap** on
top.

**The box at a glance:**

| | |
|---|---|
| **SBC** | Orange Pi 5 Plus, **mounted on edge**, 40-pin header at the bottom |
| **Front panel** | **OLED**, output only — no keys, wheel, toggle or indicators |
| **Antennas** | All elements in the **replaceable top cap** |
| **Cooling** | **Active** — Noctua NF-A4x10 5V over a 50 × 46 × 12.6 mm heatsink, ≈ 27 mm stack |
| **Bottom** | **Closed, stable foot.** No opening, no header access |
| **Rear** | Service panel, cap screw ears, and the power module later |
| **Openings** | OLED window, fan inlet and exhaust, USB-C inlet |

Read [01-architecture.md](01-architecture.md) first.

> [!WARNING]
> No dimension here is a verified installed measurement. The board and card
> sizes are published figures for the bare parts. **Heatsink, fan, adapter,
> mated antenna plugs, and cable bends are all excluded** and are exactly what
> will decide whether this closes.

## Contents and mounting

| Part | Dimensions | Mounting and clearance |
|---|---|---|
| **Orange Pi 5 Plus** | 100 × 75 mm board | **Mounted on edge**, 40-pin header at the bottom. **Clearance required on both faces** — E-key socket one side, M-key socket the other; both grow into the case depth. Published size excludes installed heatsink, fan, adapter, and cable bends. **No vendor drawing retrieved** — [mechanical reference](https://drive.google.com/file/d/1rW0tlabPHQ-_rhFcBBpHRGK9TQmT1JEP/view). |
| **Alternate SBC** *(requested, not chosen)* | Orange Pi **5**, rev **V1.3.2** · published model 100 × 62 mm | 13 mm narrower, which comes off box depth on an edge mount. **No revision-specific drawing verified, and it is probably not socket-compatible** — [01](01-architecture.md#the-alternate-board-and-why-it-is-not-a-drop-in). |
| **Intel AX210** (uplink) | M.2 2230 · 22 × 30 × 2.4 mm | Slides into the **top-side E-key socket**, screws down at the 2230 standoff. Two MHF4 antenna leads snap onto the card. Wi-Fi over PCIe, Bluetooth over USB. |
| **Second Wi-Fi card** (private AP) | 22 × 30 mm **if 2230** — height unconfirmed | Mounts in the **adapter's** E-key socket with its own retaining screw. MT7922/RZ616 is a candidate, **not a locked part.** Verify antenna connector type and 5 GHz AP operation on the target Linux image before committing. |
| **M-key → E-key adapter** | **Installed size unverified** | Male M-key edge into the Orange Pi's **underside** socket; second radio into the adapter's female E-key socket. The host accepting 2280 modules does **not** tell you the adapter's size or the installed stack height. Choose a specific adapter **that routes PCIe**, then measure it with card and antenna plugs installed. |
| **Flex antennas** · Taoglas FXP830.24.0100B · **ordered** | 42 ± 0.4 × 7 ± 0.3 mm body · 100 ± 3 mm Ø0.81 mm coax · I-PEX MHF4 | **In the replaceable top cap**, adhered to its inside face. **Quantity was not recorded on the order.** Full placement in [04-antennas.md](04-antennas.md#the-antenna-cap). |
| **Fan** · Noctua NF-A4x10 5V | **40 × 40 × 12 mm** installed with anti-vibration pads (40 × 40 × 11 mm without; 40 × 40 × 10 mm nominal) | **Design to 12 mm.** Needs an inlet *and* an exhaust opening. 3-pin, **no PWM input** — [Thermal](#thermal). |
| **Display** · **OLED** | Model not fixed. Adafruit **5297** is the candidate: **20.076 × 20.076 mm** active, −40 to +70 °C, I²C | **Front panel, output only.** Tiny next to the SBC's 100 mm edge, so **it does not drive the footprint** — [The display](#the-display). |
| **Storage** | **eMMC — now a requirement, not a preference** | The Orange Pi has **one** M.2 M-key socket and the private-AP radio occupies it, so **there is no NVMe slot left**. If NVMe is ever wanted, the radio topology has to change. [10 · What the board provides](10-measurement-protocol.md#what-the-board-actually-provides) |
| **RTC backup cell** | 20 mm coin cell + holder, or a shrink-wrapped cell on a lead | On the Orange Pi's **2-pin 1.25 mm RTC header**. Placement is a thermal keep-out problem, not a space one — see [RTC backup cell](#rtc-backup-cell). |
| **Heatsink** — Orange Pi 5 Plus aluminium | **50 × 46 × 12.6 mm** (L × W × H) | Over the SoC, with the fan above it across a clearance gap — ≈ 27 mm block. **No SKU or drawing.** [Thermal](#thermal) |
| **No control faceplate** | — | The front face carries an OLED window and nothing else. No keys, wheel, toggle, indicators, plungers or PCB 1. [Retired work](retired/pcb-1-front-control.md) |

> [!CAUTION]
> **The 50 × 46 × 12.6 mm heatsink figure is supplied, not verified.** No SKU,
> no drawing. Two rules:
>
> 1. **It is not a board dimension.** Do not confuse it with the SBC's
>    100 × 75 mm.
> 2. **The fan sits above it across a clearance gap**, so the installed
>    thermal block is ≈ 27 mm, not 12.6 mm. The gap itself has no specified
>    depth. [Thermal](#thermal)

## The board mounts on edge

Both board faces are vertical, so **both M.2 stacks grow into the case
depth.** Neither is "underneath" anything and the box's thickness is not
hostage to the adapter.

The measurement that matters:

> **Face A stack + board + Face B stack** must fit across the box's depth, as
> one assembled figure with mated antenna plugs and coax bends included.

Still unmeasured, and one of the
[dimensions nobody should guess](01-architecture.md#the-dimensions-nobody-should-guess) —
procedure at [measurement 1](10-measurement-protocol.md#1--underside-m2-stack).

**The 40-pin header faces the floor.** The antenna cap goes on the edge
opposite it and the display faces forward off a broad face.

**The bottom is a closed, stable foot.** No opening, and **no 40-pin header
access** — the header is internal only, carrying the display ribbon. **The
power module mounts on the back**, which makes the rear face the congested
one: service panel, cap screw ears, fan exhaust and the module all want it.
[Handoff · rear-face congestion](../handoff/README.md#watch-items)

> [!WARNING]
> **The depth budget does not close.** The M.2 stack, the board, the ≈ 27 mm
> cooling block and the panel share one axis, landing at **≈ 51–57 mm**
> against the brief's 30 mm placeholder.
> [Handoff · the depth budget](../handoff/README.md#03--run-the-depth-budget--it-does-not-close)

## Antenna zones — the top cap

All elements mount to the **inside face of the nonmetallic top cap**, above
the SBC. Full detail and test plan in
[04-antennas.md](04-antennas.md#the-antenna-cap).

- **Reserve a 42 × 7 mm body footprint per element**, plus clearance where its
  cable exits
- **Space the elements apart** and evaluate different orientations — no
  spacing minimum or element coordinates have been set
- The cap must be **nonmetallic**, with **no carbon-filled filament**
- **Keep elements off** metal, the heatsink, and the PCB
- Broad faces and narrow walls stay **clear of antennas**

> [!IMPORTANT]
> **This placement is proposed, not RF-validated.** All four elements sit in
> one small chamber, so **inter-radio isolation** is the thing the bench test
> has to clear — and the [hard requirement](01-architecture.md#radio-topology)
> is two 5 GHz radios running at once.

### Lead routing is a layout input, not an afterthought

The leads are **100 ± 3 mm**. The elements all sit at the top of the box; the
radios sit on **opposite faces** of a board standing on edge, so **the lead
from the far face must cross the board's thickness and still reach the cap.**

Mock up every lead **before** fixing board and cap geometry. Check that
**removing the cap does not tug on the MHF4 connectors** — the cap comes off
for antenna swaps, so that is a routine action, not a service-only one.

## Shell and access

The shell breaks in four places:

- **An OLED window** on the front face — [The display](#the-display)
- **A fan inlet and a fan exhaust**, on different faces so the fan does not
  short-circuit its own airflow. Final vent geometry is the
  [last design step](../handoff/README.md#phase-5--ventilation-and-airflow)
- **A removable rear service panel.** The MHF4 connectors are what break
  during service, and the far-face radio cannot be reached without opening
  the box
- **A USB-C opening**, positioned per [Power entry](#power-entry) below

> [!NOTE]
> **This is a ventilated box, not a sealed one.** That brings dust ingress,
> acoustic leakage, and an airflow path that has to actually cross the
> heatsink rather than short-circuiting between two adjacent holes.

The **printed Wi-Fi join label** that replaced the `★` key's QR screen could
instead be rendered on the panel — but see the size caveat under
[The display](#the-display).

## How it opens

**A perimeter band, with both broad faces as separate plates.**

| Part | Carries | Opens? |
|---|---|---|
| **Perimeter band** | USB-C inlet, fan openings | No |
| **Front face** | The OLED window | Service only |
| **Rear face** | Service panel, cap screw ears, the power module later | **Yes, for service** |
| **Top cap** | **Every antenna element** and their coax | **Yes, for antenna swaps** |
| **Bottom** | Nothing — **closed stable foot** | No |

Two consequences worth designing around:

- **How the on-edge board is retained is open.** An edge bracket, a slot in
  the band, or a carrier on one broad face. Whichever is chosen must keep the
  service property: opening the box should expose the M.2 stack and **both**
  sets of MHF4 connectors without a teardown.
- **The top cap is load-bearing.** It carries every antenna element in the
  product, so removing it means **moving live coax** — cap removal needs
  slack and clearance designed in, not assumed.

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
| **Logs** | Timestamps are the main forensic surface. Less critical than it was — [the panel](#the-display) can now show at-rest status — but the panel cannot show history |

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
- **Not in an [antenna zone](#antenna-zones--the-top-cap).** Easier
  than it was — the elements are all in the top cap now, so a 20 mm metal disc
  anywhere in the main body is clear of them. **Keep it out of the cap.**
- **Reachable at service**, like the MHF4 connectors — a cell that needs the
  antennas disturbed to replace is a cell that never gets replaced.
- The lead is short. Mock it up with the board where it actually sits.

Verify with `cat /proc/driver/rtc` at
[bring-up step 2](09-software-and-bringup.md#bring-up-order).

## The display

**An OLED on the front face, output only.** No keys, wheel, toggle or
indicators — the panel shows status and nothing takes input.

**The exact model is not fixed.** The candidate is the **Adafruit 5297**,
which is already the power board's console display — using the same part in
both boxes means one part number, one driver, one spare.

| | Adafruit 5297 |
|---|---|
| Active area | **20.076 × 20.076 mm** |
| Interface | **I²C**, 4-pin JST-SH STEMMA QT / Qwiic — 3.3 V, GND, SDA, SCL |
| Operating temp | **−40 to +70 °C** |
| Already used | Yes — [the power board console](05-power-board.md#adafruit-5297-oled) |

### Why OLED rather than e-paper

- **It is live.** Status that updates in seconds, not on a refresh cycle
  measured in seconds-to-minutes.
- **The temperature problem goes away.** E-paper panels in this class are
  rated **0–50 °C**; the 5297 is rated **−40 to +70 °C**. In a box with two
  Wi-Fi 6E radios, a heatsink and a fan — and in a cold car on the other end
  — that is the difference between in-spec and not.
- **One part across both enclosures**, with a driver already written for the
  console.

### What OLED costs

> [!IMPORTANT]
> **No status at rest.** E-paper holds its last image with power removed; an
> OLED shows nothing when the device is off. A wedged boot and a powered-off
> box look identical from outside the case. That was e-paper's single real
> advantage and it is given up here deliberately.

> [!WARNING]
> **A Wi-Fi join QR is marginal at 20 mm square.** A QR for a strong
> passphrase needs roughly **≥ 0.5 mm per module** to scan reliably, and
> 20.076 mm does not leave much room. If rendering the join QR on the panel
> matters, **a larger OLED is the change to make** — decide that before the
> window is cut, because it moves the front-face geometry.

> [!NOTE]
> **OLEDs burn in on static images.** A status panel is exactly the static-
> image case. Budget for a screensaver, periodic pixel shift, or a timeout —
> a firmware concern, but one that is cheaper to plan for than to retrofit.

### What is unresolved

- **The exact model and size**, driven mainly by the QR question above
- **Window, bezel and panel retention**, which follow from the model
- **Where the module and its cable sit** relative to a board standing on edge
- **How it reaches the host.** There is no PCB 1, so it hangs off the Orange
  Pi's 40-pin header — I²C plus 3.3 V. The retired
  [40-pin header map](retired/pcb-1-front-control.md) is the starting point
- **What it displays.** Uplink state, client count and rail status are the
  obvious candidates; none is specified

## Thermal

**Active cooling: a Noctua NF-A4x10 5V fan over a 50 × 46 × 12.6 mm
heatsink.** Planned, **not validated** — two Wi-Fi 6E radios under
simultaneous sustained load is the case that drove it, and that case has
never been run.

### The stack

```
    vented surface → intake air
            ▼
    FAN        40 × 40 × 12 mm installed
            ▼
    gap        "small" — depth not specified
    HEATSINK   50 × 46 × 12.6 mm
    ──────────────────────────────
    Orange Pi 5 Plus
```

The fan is in **push/intake** configuration: it draws outside air through a
vented surface and forces it into the fins, rather than extracting from the
case. **The block is ≈ 27 mm including the gap** — the largest single term in
[the depth budget](../handoff/README.md#03--run-the-depth-budget--it-does-not-close).

Two numbers are missing: **the clearance gap**, which is a direct depth term
and chokes the fan if too small, and **the exhaust**, since only the intake
is specified.

### The fan

| | |
|---|---|
| **Part** | Noctua **NF-A4x10 5V** |
| **Price** | ~$16 · **estimate, not a quote** |
| **Supply** | **5 V** |
| **Connector** | **3-pin: GND, 5 V, RPM tach** |
| **PWM input** | **None** |
| **Nominal size** | 40 × 40 × 10 mm |
| **Without pads** | 40 × 40 × **11** mm |
| **Installed with pads** | 40 × 40 × **12** mm ← **design to this** |
| **Mounting** | Above the heatsink, across a small clearance gap |
| **Input current** | **Not retrieved** — [spec page](https://noctua.at/en/products/nf-a4x10-5v/specifications) rate-limited |

> [!WARNING]
> **The nominal 10 mm figure is wrong for this box by 2 mm.** The model name
> says 10 mm; the part is 11 mm without its anti-vibration pads and 12 mm
> with them. **Size the pocket at 12 mm.** Omitting the pads to recover 1 mm
> trades it for vibration transmitted into a printed shell.

### Three things to resolve

**1 · It cannot be speed-controlled by PWM.** The part has a tachometer output
and no PWM input. Three options, all with costs:

| Option | Cost |
|---|---|
| Run it flat out, always | Audible. This is a device used in **hotel rooms, at night** |
| Voltage-control it from the host | Needs a driver circuit that does not exist in any schematic here |
| Switch it on/off thermally | Cycling noise is more noticeable than constant noise |

**None of the three is specified.** [The power board](05-power-board.md) has
no fan output — the fan is in Enclosure A, the power board is in the rear
module, and **only 5 V crosses between them.** So the fan hangs off the
Orange Pi, which is a host-side decision not yet made.

**2 · The tach wire needs a reader, or it is a dead conductor.** It is the
only way to know the fan is still turning inside a closed box — and the OLED
is somewhere to show it.

**3 · It adds continuous current to a rail already over budget.** The
[seam loop](01-architecture.md#constraint-2--ir-drop-which-binds-first) is
pinned at 25 mΩ and the Pi alone is specified at 4 A. The fan's input current
**has not been retrieved** — fold it into the peak-current measurement rather
than assuming it rounds to zero.

### Airflow is the last design step

Vent geometry depends on the final internal layout and on where the rear
module lands, so it is deliberately
[the last phase](../handoff/README.md#phase-5--ventilation-and-airflow). What
it has to achieve:

- An intake directly above the fan with enough open area not to choke it
- An exhaust that is **not adjacent** to the intake, or the fan recirculates
  its own air. **Only the intake is specified** — exhaust position is open
- A path that **crosses the heatsink** rather than taking a short free route
  between two holes
- **No conflict with the rear module**, which wants the same face as the
  likely exhaust
- **No metal** in or near the antenna cap — no mesh inserts

The fan, the heatsink and the panel all land in the same unmeasured volume.
Resolve it with measurement, not assumption.

## Open questions

The enclosure work is being executed — [the handoff](../handoff/README.md)
carries the live version of most of these with phase gates attached.

- **The depth budget does not close.** The M.2 stack, the board, the ≈ 27 mm
  cooling block and the panel share one axis: **≈ 51–57 mm** against a 30 mm
  placeholder.
  [Handoff · depth budget](../handoff/README.md#03--run-the-depth-budget--it-does-not-close)
- **Installed M.2 stack height** (adapter + card + mated plugs + coax bend) —
  **15.9 mm of stacked guesses**, and the largest untrusted term in that
  budget. A board with cards installed is on hand; this is measurable today.
  [10 · Measurement 1](10-measurement-protocol.md#1--underside-m2-stack)
- **The fan-to-heatsink clearance gap**, and **which surface the fan draws
  through** — rear or top. [Thermal](#thermal)
- **The board's mounting holes and port positions.** The vendor
  [mechanical drawing](https://drive.google.com/file/d/1rW0tlabPHQ-_rhFcBBpHRGK9TQmT1JEP/view)
  has **not been retrieved**, and an edge mount needs both
- **How the on-edge board is retained** — edge bracket, slot in the band, or
  a carrier on one broad face. [How it opens](#how-it-opens)
- **OLED model and size**, driven by whether the Wi-Fi join QR has to render
  on it. [The display](#the-display)
- **Fan speed control**, or the decision to run it flat out
- **Vent pattern and airflow direction** — the
  [last design step](../handoff/README.md#phase-5--ventilation-and-airflow)
- **Rear-face allocation.** Service panel, cap screw ears, fan exhaust and
  the power module all want the same surface
- Which M-key-to-E-key adapter, confirmed to route PCIe — the Sintech M-key
  to A/E-key card is the candidate. Routes PCIe ×1, carries USB 2.0 on a
  separate flying cable, installed size unmeasured.
  [10 · Candidate](10-measurement-protocol.md#candidate-sintech-m-key-to-ae-key-adapter)
- Second radio part, form factor height, and antenna connector type
- **Which SBC** — 5 Plus, or the Orange Pi 5 V1.3.2, which is
  [probably not socket-compatible](01-architecture.md#the-alternate-board-and-why-it-is-not-a-drop-in)
- **RTC cell chemistry** — primary or rechargeable, decided by whether the
  Orange Pi's RTC header trickle-charges. [Above](#rtc-backup-cell)
