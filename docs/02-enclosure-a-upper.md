# 02 · Enclosure A — Upper Router Box

The router itself. Holds the Orange Pi **on edge**, both radios, the adapter,
storage, a fan, an e-paper front panel, and a replaceable antenna cap on top.

> [!IMPORTANT]
> **Substantially revised 2026-11-23, and three of this document's settled
> decisions moved.** The box is no longer a sealed headless shell:
>
> | | Was | Now |
> |---|---|---|
> | **SBC mounting** | Flat on standoffs, on the base plate | **On edge** |
> | **Front panel** | None — headless | **3.7" GooDisplay e-paper**, output only |
> | **Antennas** | Four strips inside the narrow walls | **All elements in the replaceable top cap** |
> | **Cooling** | Passive if possible; "active?" was open | **Active — Noctua NF-A4x10 5V planned** |
> | **Openings** | One USB-C inlet | USB-C inlet, **display window, fan inlet and exhaust** |
>
> **The controls did not come back** — no keys, no wheel, no toggle, no
> indicators, no PCB 1. See
> [01 · The 2026-11-23 revision](01-architecture.md#the-2026-11-23-revision).

Read [01-architecture.md](01-architecture.md) first.

> [!WARNING]
> No dimension here is a verified installed measurement. The board and card
> sizes are published figures for the bare parts. **Heatsink, fan, adapter,
> mated antenna plugs, and cable bends are all excluded** and are exactly what
> will decide whether this closes.

## Contents and mounting

| Part | Dimensions | Mounting and clearance |
|---|---|---|
| **Orange Pi 5 Plus** | 100 × 75 mm board | **Mounted on edge** (decided 2026-11-23). **Clearance required on both faces** — E-key socket one side, M-key socket the other; on edge both grow into the same plan dimension. Published size excludes installed heatsink, fan, adapter, and cable bends. **No vendor drawing retrieved** — [mechanical reference](https://drive.google.com/file/d/1rW0tlabPHQ-_rhFcBBpHRGK9TQmT1JEP/view). |
| **Alternate SBC** *(requested, not chosen)* | Orange Pi **5**, rev **V1.3.2** · published model 100 × 62 mm | 13 mm narrower, which comes off box depth on an edge mount. **No revision-specific drawing verified, and it is probably not socket-compatible** — [01](01-architecture.md#the-alternate-board-and-why-it-is-not-a-drop-in). |
| **Intel AX210** (uplink) | M.2 2230 · 22 × 30 × 2.4 mm | Slides into the **top-side E-key socket**, screws down at the 2230 standoff. Two MHF4 antenna leads snap onto the card. Wi-Fi over PCIe, Bluetooth over USB. |
| **Second Wi-Fi card** (private AP) | 22 × 30 mm **if 2230** — height unconfirmed | Mounts in the **adapter's** E-key socket with its own retaining screw. MT7922/RZ616 is a candidate, **not a locked part.** Verify antenna connector type and 5 GHz AP operation on the target Linux image before committing. |
| **M-key → E-key adapter** | **Installed size unverified** | Male M-key edge into the Orange Pi's **underside** socket; second radio into the adapter's female E-key socket. The host accepting 2280 modules does **not** tell you the adapter's size or the installed stack height. Choose a specific adapter **that routes PCIe**, then measure it with card and antenna plugs installed. |
| **Flex antennas** · Taoglas FXP830.24.0100B · **ordered** | 42 ± 0.4 × 7 ± 0.3 mm body · 100 ± 3 mm Ø0.81 mm coax · I-PEX MHF4 | **In the replaceable top cap**, adhered to its inside face (changed 2026-11-23 — they were in the narrow walls). **Quantity was not recorded on the order.** Full placement in [04-antennas.md](04-antennas.md#the-antenna-cap--decided-2026-11-23). |
| **Fan** · Noctua NF-A4x10 5V | **40 × 40 × 12 mm** installed with anti-vibration pads (40 × 40 × 11 mm without; 40 × 40 × 10 mm nominal) | **Design to 12 mm.** Needs an inlet *and* an exhaust opening, which is what stops this being a sealed shell. 3-pin, **no PWM input** — [Thermal](#thermal--active-cooling-planned-2026-11-23). |
| **Display** · GooDisplay e-paper, 3.7" | Panel outline **92.99 × 53 × 1.0 mm** for the 416 × 240 candidates; driver board **41 × 22 mm** | **Front panel, output only.** Exact model not chosen. Smaller than the SBC's 100 mm edge, so **it does not drive the footprint** — [The display](#the-display--reinstated-2026-11-23). |
| **Storage** | **eMMC — now a requirement, not a preference** | The Orange Pi has **one** M.2 M-key socket and the private-AP radio occupies it, so **there is no NVMe slot left**. If NVMe is ever wanted, the radio topology has to change. [10 · What the board provides](10-measurement-protocol.md#what-the-board-actually-provides) |
| **RTC backup cell** | 20 mm coin cell + holder, or a shrink-wrapped cell on a lead | On the Orange Pi's **2-pin 1.25 mm RTC header**. Placement is a thermal keep-out problem, not a space one — see [RTC backup cell](#rtc-backup-cell). |
| **Heatsink** — Orange Pi 5 Plus aluminium | **50 × 46 × 12.6 mm** (L × W × H) | Over the SoC. **No SKU or drawing**, and whether the fan stacks on it is unanswered — see the warning below. |
| ~~Faceplate~~ | — | Still no *control* faceplate. The front face now carries a **display window** and nothing else. |
| ~~PCB 1~~ | — | **Still retired.** [04](retired/pcb-1-front-control.md) · [12](retired/pcb-1-schematic.md) |

> [!CAUTION]
> **The 50 × 46 × 12.6 mm figure is attributed but not verified.** It is the
> **Orange Pi 5 Plus aluminium heatsink**, named as such on 2026-11-23. Three
> rules for it:
>
> 1. **It is not a board dimension.** Do not confuse it with the SBC's
>    100 × 75 mm, which it superficially resembles in magnitude.
> 2. **It is not confirmed to include or exclude the fan, and that is the
>    biggest open number in the box.** A 12.6 mm heatsink with a 12 mm fan
>    bolted on is a **24.6 mm** thermal block; a 12.6 mm assembly that already
>    contains the fan is half that. **Nobody has said which**, and it is one
>    question to the client —
>    [handoff · Phase 0.2](../handoff/README.md#02--resolve-whether-the-heatsink-and-fan-stack--blocking).
> 3. **It supersedes nothing.** The 15 mm `A.heatsink_h` guess in
>    [10](10-measurement-protocol.md) was a guess; this is a supplied figure
>    with no SKU or drawing behind it, not a measurement.

### What the scope cut still removes from this box

The control half of [the cut](01-architecture.md#the-v1-scope-cut) holds, and
it is still most of the mechanical saving:

- **No key openings, no wheel opening, no RGB diffusers, no toggle bushing.**
  The front face has a display window; it does not have a control row.
- **No printed plungers.** These were the highest-risk mechanical item in the
  build, needing a test coupon at two or three lengths before any faceplate
  could be ordered. That gate is still gone.
- **No PCB 1 on standoffs**, and no faceplate as a separate load-bearing part.

**What came back is thinner than what left.** The retired stack was faceplate
+ plunger travel + PCB 1 + glass + a 107 × 64 mm driver board. The replacement
is a **1.0 mm panel** and a **41 × 22 mm** adapter board.

## The double-sided problem — dissolved by the edge mount

This document used to open on the single most important mechanical fact about
the build: one radio above the board, one below, so it could not lie flat and
standoff height had to swallow the whole underside stack.

**Mounting the board on edge retires that framing.** Both faces are vertical.
Neither stack is "underneath" anything, and the box's thickness is no longer
hostage to the adapter.

What replaces it is a **plan-width** problem, and it is the same measurement:

> **Face A stack + board + Face B stack** must fit across the box's depth,
> measured as one assembled figure with mated antenna plugs and coax bends
> included.

That figure is still unmeasured and still one of the
[dimensions nobody should guess](01-architecture.md#the-dimensions-nobody-should-guess) —
[measurement 1](10-measurement-protocol.md#1--underside-m2-stack) is unchanged
in procedure, only in which box dimension it feeds.

> [!WARNING]
> **The edge mount is not free.** It reopens how the board is retained — see
> [How it opens](#how-it-opens--reasoning-superseded-2026-11-23) — and it puts
> **both** M.2 stacks into the case *depth*, where they now compete with the
> heatsink, the fan and the display for one axis. **That budget does not
> currently close** against the 30 mm the enclosure brief proposes:
> [handoff · the depth budget](../handoff/README.md#03--run-the-depth-budget--it-does-not-currently-close).

**The rotation is settled: the 40-pin header faces the floor.** Fixed
2026-11-23 by the [enclosure brief](../handoff/01-brief-upright-case.md). That
one choice resolves a lot — the antenna cap goes on the edge *opposite* the
header, the display faces forward off a broad face, and the bottom becomes the
service and expansion edge where the power module later mates.

## Antenna zones — moved to the top cap

**Changed 2026-11-23.** The four narrow-wall positions are withdrawn. All
elements now mount to the **inside face of the nonmetallic top cap**, above
the SBC. Full detail and test plan in
[04-antennas.md](04-antennas.md#the-antenna-cap--decided-2026-11-23).

- **Reserve a 42 × 7 mm body footprint per element**, plus clearance where its
  cable exits
- **Space the elements apart** and evaluate different orientations — no
  spacing minimum or element coordinates have been set
- The cap must be **nonmetallic**, with **no carbon-filled filament**
- **Keep elements off** metal, the heatsink, and the PCB
- Broad faces and narrow walls are now **clear of antennas** — which removes
  the keep-out that justified the current opening scheme

> [!IMPORTANT]
> **This placement is proposed, not RF-validated.** It also undoes a reason
> [04](04-antennas.md) gave for the old layout — that spreading the elements
> kept the two radios physically separated "rather than crowding all four
> elements under the top cap." **Crowding them under the top cap is now the
> plan.** Inter-radio isolation is the specific thing the bench test has to
> clear, and the [hard requirement](01-architecture.md#radio-topology) is two
> 5 GHz radios running at once.

### Lead routing is a layout input, not an afterthought

The leads are **100 ± 3 mm** and this got harder, not easier. The elements all
sit at the top of the box; the radios sit on **opposite faces** of a board
standing on edge. **The lead from the far face must cross the board's
thickness and still reach the cap.**

Mock up every lead **before** fixing board and cap geometry. Check that
**removing the cap does not tug on the MHF4 connectors** — the cap is designed
to come off for antenna swaps, so this is now a routine action rather than a
service-only one.

## Shell and access

The shell now breaks in four places, not one:

- **A USB-C opening**, positioned per [Power entry](#power-entry) below.
- **A display window** on the front face — [The display](#the-display--reinstated-2026-11-23).
- **A fan inlet and a fan exhaust.** Two openings, not one, and they have to
  be on different faces or the fan short-circuits its own airflow.
- **Service access**, which is still required: the MHF4 connectors are what
  break during service, and the far-face radio cannot be reached without
  opening the box.

> [!NOTE]
> **The sealed-shell premise is gone.** Earlier revisions could treat this box
> as a closed form broken only by a power inlet. With a fan it is a
> **ventilated** box, which brings in dust ingress, acoustic leakage and an
> airflow path that has to actually cross the heatsink rather than
> short-circuiting between two adjacent holes.

The **printed Wi-Fi join label** that replaced the `★` key's QR screen now has
a better home: the e-paper can render it. See
[The display](#the-display--reinstated-2026-11-23).

## How it opens — reasoning superseded 2026-11-23

> [!WARNING]
> **The decision below may still be right, but the argument for it has been
> inverted and one of its two consequences is now impossible.** Re-confirm
> before cutting anything.

**Decided 2026-11-18: a perimeter band, with BOTH broad faces as separate
plates.** The deciding evidence was that all four antenna strips lived in the
**narrow walls** while the **broad faces stayed clear** — so making the broad
faces removable cost no antenna area, where a mid-height seam split would have
cut straight through the strips.

**As of 2026-11-23 that evidence no longer exists.** The antennas are in the
top cap. The narrow walls are clear, the broad faces are clear, and *no* seam
line cuts an antenna zone. **The constraint that picked this scheme is gone**,
which does not make the scheme wrong — it makes it unjustified.

| Part | Carried (2026-11-18) | Carries now |
|---|---|---|
| **Perimeter band** | All four antenna zones, the USB-C inlet | USB-C inlet, fan openings — **no antennas** |
| **Base plate** | The Orange Pi, flat on standoffs | **Cannot carry an on-edge board this way** |
| **Top cap** | Nothing structural | **Every antenna element**, and their coax |
| **Front face** | Nothing | **The display window** |

Two things that fell out of the original decision, re-examined:

- ~~**The SBC mounts to the base plate.**~~ **Broken by the edge mount.** The
  property it bought — pull the base, the board comes with it, exposing both
  sets of MHF4 connectors at once — is still the right goal, but an on-edge
  board needs an edge bracket, a slot in the band, or a carrier bonded to one
  broad face. **Pick the one that preserves that service property.**
- **The replaceable top cap survives, and is now load-bearing.** It went from
  "nothing structural" to carrying every antenna element in the product. The
  hedge it existed for — swap the uplink pair for domes — still works, but
  removing the cap now means **moving live coax**, so cap removal needs slack
  and clearance designed in rather than assumed.

**Cost of the decision:** two seam lines instead of one, and the band has to
be stiff enough on its own. With the antennas out of the walls, **a simpler
scheme may now be available** — that is the thing to re-check.

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
| **Logs** | Timestamps are the main forensic surface. Less critical than it was — [the panel](#the-display--reinstated-2026-11-23) can now show at-rest status — but the panel cannot show history |

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
  [unmeasured thermal problem](#thermal--active-cooling-planned-2026-11-23). Keep it off the heatsink and clear of
  the underside M.2 stack.
- **Not in an [antenna zone](#antenna-zones--moved-to-the-top-cap).** Easier
  than it was — the elements are all in the top cap now, so a 20 mm metal disc
  anywhere in the main body is clear of them. **Keep it out of the cap.**
- **Reachable at service**, like the MHF4 connectors — a cell that needs the
  antennas disturbed to replace is a cell that never gets replaced.
- The lead is short. Mock it up with the board where it actually sits.

Verify with `cat /proc/driver/rtc` at
[bring-up step 2](09-software-and-bringup.md#bring-up-order).

## The display — reinstated 2026-11-23

**A 3.7" GooDisplay e-paper panel returns to the front face.** Family and size
are fixed; **the exact model is not chosen.** It is an **output surface only**
— the controls stayed cut.

### Why this is a much smaller problem than last time

The Waveshare 4.26" panel was cut partly because **its 107 × 64 mm driver
board set the faceplate's minimum size.** That does not happen here:

| | Retired Waveshare 4.26" | GooDisplay 3.7" |
|---|---|---|
| Driver board | **107 × 64 mm** — set the footprint | **41 × 22 mm** (DESPI-C02) |
| Panel outline | — | **92.99 × 53 × 1.0 mm** |
| Full refresh | 4 s | **2 s** (GDEY037T03) |
| Partial refresh | ≥ 180 s minimum interval | **0.3 s** (GDEY037T03) |

**Both figures are smaller than the SBC's 100 mm edge**, so with the board
standing on edge the display does not drive a single enclosure dimension. The
original objection is answered by the geometry.

### Candidates

All three share a 24-pin 0.5 mm FPC and SPI. Published by Good Display; **none
verified against a part in hand.**

| Model | Resolution · active area | Colour | Refresh | Operating temp |
|---|---|---|---|---|
| **GDEY037T03** ← suggested default | 416 × 240 · 81.54 × 47.04 mm | B/W, 4-level grey on request | **2 s full · 0.3 s partial** | **0–50 °C** |
| GDEM037F36 | 416 × 240 · 81.54 × 47.04 mm | Black/white/red/yellow | 20 s full · 12 s fast | **0–40 °C** |
| GDEH037E01 | 480 × 720 · 50.40 × 75.60 mm | Spectra 6, full colour | Not published | 0–50 °C |

> [!CAUTION]
> **Operating temperature is the deciding spec, not resolution or colour.**
> E-paper's 0–50 °C ceiling was a stated reason for preferring OLED during the
> original panel debate, and it lands in a box that now has **two Wi-Fi 6E
> radios under sustained load and an unmeasured thermal problem.** The
> four-colour GDEM037F36 narrows that to **0–40 °C** and takes 20 s to
> refresh — a poor trade for a status panel inside a warm sealed-ish box.
> **GDEY037T03 is the defensible default** until the thermal measurement
> exists.
>
> The lower bound matters too: **0 °C**. This is a travel device, and a cold
> car or an unheated room puts the panel below spec while the radios are still
> fine.

### What is unresolved

- **The exact model**, including whether a bare panel plus a DESPI-C02 adapter
  or an integrated module is wanted
- **How it reaches the host.** There is no PCB 1. It needs **SPI on the Orange
  Pi's 40-pin header** plus 3.3 V — the retired
  [40-pin header map](retired/pcb-1-front-control.md) is the starting point,
  and [01](01-architecture.md#the-v1-scope-cut) had recorded the header as
  "nothing attached"
- **Window, bezel and panel retention.** The active area is inset from the
  92.99 × 53 mm outline, so the window is cut to the active area and the
  bezel hides the margin and the flex tail
- **Where the flex tail and the adapter board sit** relative to a board
  standing on edge
- **What it displays**, which is the question that cut it the first time. The
  honest v1 answer is the one the scope cut named: a **Wi-Fi join QR and SSID**
  — the `★` key's screen, which had become a printed label with nowhere to
  live. A 416 × 240 panel at 81.54 mm wide clears the ≥ 0.5 mm-per-module bar
  that made the 20 mm OLED marginal.

## Thermal — active cooling planned 2026-11-23

**The open question "whether active cooling is needed" is answered: a fan is
planned.** The stated preference had been hardware needing no dedicated
cooling; **two Wi-Fi 6E radios under simultaneous sustained load** is the case
that overruled it. It remains **untested** — a fan is planned, not validated.

### The fan

| | |
|---|---|
| **Part** | Noctua **NF-A4x10 5V** — planned, not purchased |
| **Price** | ~$16 · **user estimate, not a quote** |
| **Supply** | **5 V** |
| **Connector** | **3-pin: GND, 5 V, RPM tach** |
| **PWM input** | **None** |
| **Nominal size** | 40 × 40 × 10 mm |
| **Measured without pads** | 40 × 40 × **11** mm |
| **Installed with pads** | 40 × 40 × **12** mm ← **design to this** |
| **Spec page** | [noctua.at](https://noctua.at/en/products/nf-a4x10-5v/specifications) — **not retrieved; the page rate-limited on 2026-11-23** |

> [!WARNING]
> **The nominal 10 mm figure is wrong for this box by 2 mm.** Noctua's model
> name says 10 mm; the part is 11 mm without its anti-vibration pads and
> 12 mm with them. **Size the pocket at 12 mm.** Omitting the pads to recover
> 1 mm trades it for vibration transmitted into a printed shell.

### Three consequences nobody has resolved

**1 · It cannot be speed-controlled by PWM.** The part has a tachometer output
and **no PWM input**. That leaves three options, all with costs:

| Option | Cost |
|---|---|
| Run it flat out, always | Audible. This is a device used in **hotel rooms, at night** |
| Voltage-control it from the host | Needs a driver circuit that does not exist in any schematic here |
| Switch it on/off thermally | Cycling noise is more noticeable than constant noise |

**Nothing in this repo specifies any of the three**, and [the power
board](05-power-board.md) has no fan output — the fan is in Enclosure A and
the power board is in Enclosure B, with **only 5 V crossing the seam.** So it
must hang off the Orange Pi, which is a host-side decision not yet made.

**2 · The tach wire needs a reader, or it is a dead conductor.** It is the only
way to know the fan is still turning inside a closed box with
[no at-rest status](01-architecture.md#the-v1-scope-cut) — except that there
*is* now a display that could show it.

**3 · It adds continuous current to a rail that is already over budget.** The
[seam loop](01-architecture.md#constraint-2--ir-drop-which-binds-first) is
pinned at 25 mΩ and the Pi alone is specified at 4 A. The fan's input current
**has not been retrieved** — fold it into the peak-current measurement rather
than assuming it rounds to zero.

### Fan and antennas are no longer in tension — but fan and display are

This document used to say antenna zones and heatsink placement were in direct
tension. **That tension is resolved**: the antennas moved to the top cap, the
heatsink stays near the SoC, and they no longer compete.

The replacement tension is **thermal against the panel**. The e-paper is rated
**0–50 °C**, which is a lower ceiling than the SoC, the radios or the
antennas (the Taoglas elements are rated −40 to +85 °C). **The display is now
the most heat-sensitive part in the box**, and it is mounted on the front
face. Route the exhaust away from it.

Resolve all of this with measurement, not assumption — and note that the fan,
the heatsink envelope and the panel all land in the same unmeasured volume.

## Open questions

**The enclosure work is now being executed** — see
[the handoff](../handoff/README.md), which carries the live version of most of
these with phase gates attached.

- **The depth budget does not close.** Both M.2 stacks, the board, the
  heatsink, the fan and the panel share one axis, and the total lands at
  **≈ 37–51 mm** against the brief's 30 mm placeholder.
  [Handoff · depth budget](../handoff/README.md#03--run-the-depth-budget--it-does-not-currently-close)
- **Installed M.2 stack height** (adapter + card + mated plugs + coax bend) —
  still **15.9 mm of stacked guesses**, and now the largest untrusted term in
  that budget. A board with cards installed is on hand; this is measurable
  today. [10 · Measurement 1](10-measurement-protocol.md#1--underside-m2-stack)
- **Whether the fan stacks on the heatsink** — a 12 mm swing, and one question
  to answer. [Above](#thermal--active-cooling-planned-2026-11-23)
- **The board's mounting holes and port positions.** The vendor
  [mechanical drawing](https://drive.google.com/file/d/1rW0tlabPHQ-_rhFcBBpHRGK9TQmT1JEP/view)
  has **not been retrieved**, and an edge mount needs both
- **How the on-edge board is retained** — edge bracket, slot in the band, or a
  carrier on one broad face. Must preserve the service access the
  base-plate scheme was chosen for.
  [Above](#how-it-opens--reasoning-superseded-2026-11-23)
- **Display model**, host interface and window geometry —
  [above](#the-display--reinstated-2026-11-23)
- **Fan speed control**, or the decision to run it flat out. No PWM input
  exists on the chosen part
- Which M-key-to-E-key adapter, confirmed to route PCIe — **candidate
  proposed 2026-11-18**, the Sintech M-key to A/E-key card. Routes PCIe ×1,
  but carries USB 2.0 on a separate flying cable and its installed size is
  still unmeasured. See
  [10 · Candidate](10-measurement-protocol.md#candidate-sintech-m-key-to-ae-key-adapter)
- Second radio part, form factor height, and antenna connector type
- **Which SBC** — 5 Plus, or the requested Orange Pi 5 V1.3.2, which is
  [probably not socket-compatible](01-architecture.md#the-alternate-board-and-why-it-is-not-a-drop-in)
- **RTC cell chemistry** — primary or rechargeable, decided by whether the
  Orange Pi's RTC header trickle-charges. Its mounting location is a thermal
  keep-out, [above](#rtc-backup-cell)
- ~~Heatsink size and whether active cooling is needed~~ — **answered
  2026-11-23**: a 50 × 46 × 12.6 mm heatsink and a Noctua NF-A4x10 5V fan.
  [Above](#thermal--active-cooling-planned-2026-11-23)
- ~~Board rotation on edge~~ — **settled 2026-11-23**: the 40-pin header faces
  the floor
- ~~Whether a replaceable top cap survives~~ — **yes, and it now carries every
  antenna element.** [Above](#how-it-opens--reasoning-superseded-2026-11-23)
- ~~Display model and bracket geometry — moot, v1 is headless~~ — **reopened
  2026-11-23.** The panel is back
- ~~PCB 1 outline and standoff height~~ — still moot, there is no PCB 1
