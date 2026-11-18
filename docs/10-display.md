# 10 · Display — 4.26" e-Paper *(retired)*

> [!CAUTION]
> **Retired 2026-11-18. Vezha v1 has no display.** Enclosure A is fully
> headless: no panel, no keys, no wheel, no indicators, no front PCB. The
> entire user interface is the web UI. See
> [01 · The v1 scope cut](01-architecture.md#the-v1-scope-cut).
>
> **Nothing in this document is a build instruction.** It is kept because the
> analysis below is the reason the display went away, and because a v2 that
> adds a panel should start from these findings rather than rediscover them.

**If you are returning to this for v2, the four findings that still hold:**

| Finding | Where |
|---|---|
| A 4 s full refresh and a ≥ 180 s minimum interval cannot drive a scroll wheel — any e-paper UI must be paged, not scrolled | [What this does to the UI](#what-this-does-to-the-ui) |
| 0–50 °C operating was the narrowest environmental limit in the whole build; it will not display in a cold car | [Environment](#environment) |
| The 107 × 64 mm driver board, not the glass, is what sets the faceplate's minimum size | [The consequence for Enclosure A](#the-consequence-for-enclosure-a) |
| Leaving the panel powered in a static state destroys it — the `PWR` pin must be driven, and an unclean shutdown is a dead-display failure mode | [Refresh discipline](#refresh-discipline-is-a-hard-requirement) |

A later comparison against monochrome OLED, run before the headless decision,
is summarised in [the v1 scope cut](01-architecture.md#the-v1-scope-cut).

---

*Original document follows, unedited.*

## Original: the chosen display for Enclosure A

**Superseded the Waveshare 3.5" HDMI touchscreen** discussed in
[09-background.md](09-background.md#enclosure-antenna-layout-and-controls).

Part: **Waveshare 4.26inch e-Paper display HAT**, SKU **26376** — 800 × 480,
black/white, SPI. Listed at **$31.99** (the page's own quantity tier says $30.99
at 1–9; the discrepancy is theirs, not a typo here).

Every figure below comes from the Waveshare product page and wiki manual,
checked 2026-11-17. **Where those two sources disagree, both numbers are given.**
Nothing here is measured.

## Why this is a good fit

Three properties earn it the slot, and they are not the obvious ones:

1. **It costs nothing to keep an image up.** `<35 mW` while refreshing,
   `<0.01 µA` standby. For a battery-powered unit the display stops being part
   of the power budget.
2. **It holds the image with power removed.** A powered-down Vezha still shows
   its last screen. The `★` key's Wi-Fi join QR code — see
   [04](04-pcb-1-front-control.md#control-behavior-and-wiring) — stays readable
   with the router off, which is a better behaviour than the HDMI panel could
   have offered.
3. **No touch layer.** It removes the USB touch load from the power budget
   in [09](09-background.md#power-and-portability), and leaves the ANO wheel and
   three keys as the sole input path. That matches the control scheme already
   specified rather than competing with it.

## Dimensions

**Read this table carefully — three different outlines get quoted for this
product and they are not interchangeable.**

| Figure | Size | What it is |
|---|---|---|
| **Active area** | **92.80 × 55.68 mm** | The visible image. 0.116 mm dot pitch × 800 × 480. **Cut the faceplate window to this.** |
| Panel, "screen only" | 129.33 × 62.37 × 0.926 mm | Manual's panel outline. **36 mm wider than the active area**, which strongly suggests it includes the folded-out flex tail. Treat as the worst-case envelope, not the glass. |
| Driver board (the "HAT") | 107.0 × 64.0 mm | Separate PCB. Thickness **not stated**. |
| Weight | 0.064 kg | — |

Diagonal checks out: √(92.80² + 55.68²) = 108.2 mm = 4.26″, confirming
92.80 × 55.68 mm is the glass.

### The consequence for Enclosure A

The driver board is **107 × 64 mm — larger than the Orange Pi's 100 × 75 mm
footprint in one axis.** The display is now one of the two biggest rigid parts
in the upper box, and the faceplate has to carry a ~93 × 56 mm window *plus* the
toggle, three keys, the wheel and four RGB diffusers.

This does not break the existing rule from
[02](02-enclosure-a-upper.md#faceplate-and-seam) — display opening stays
separate from control openings — but it does mean the faceplate's minimum size
is now set by the display, not by the control layout.

**Unverified and worth measuring before any faceplate is printed:** the bare
glass outline, where the flex tail exits and its bend radius, and the driver
board's thickness. The 129.33 mm figure is the one to distrust.

## Interface and wiring

SPI, 3-wire or 4-wire. `3.3 V / 5 V` with an onboard voltage translator.

It ships as a Raspberry Pi 40-pin HAT **but does not have to be used as one** —
the box includes a **GH1.25 9-pin cable, 20 cm**. That matters here, because
PCB 1 and the display would otherwise both want the same 40-pin header.

**Recommended topology:** display → 9-pin cable → **PCB 1** → the single keyed
harness already specified to the Orange Pi. The faceplate assembly stays one
serviceable unit with one cable to the SBC, and the 40-pin header keeps one
connector.

Nine signals, with the manual's Raspberry Pi **board** pin numbers:

| Signal | Function | RPi board pin |
|---|---|---|
| `VCC` | 3.3 V or 5 V in | 3.3 V |
| `GND` | Ground | GND |
| `DIN` | SPI MOSI | 19 |
| `CLK` | SPI SCK | 23 |
| `CS` | Chip select, active low | 24 |
| `DC` | Data/command select | 22 |
| `RST` | External reset, active low | 11 |
| `BUSY` | Busy status **output** | 18 |
| `PWR` | Panel power on/off control | 12 |

SPI mode 0 (the manual writes `CPHL=0, CPOL=0`; `CPHL` is a typo for `CPHA`).

Pin budget on the Orange Pi's 40-pin header is comfortable: 9 for the display,
2 for the I²C bus shared by the ANO and the TLC59116, and 4–5 GPIO for the
toggle and keys.

> [!NOTE]
> **Checked 2026-11-18: these Raspberry Pi pin numbers do map onto the Orange
> Pi 5 Plus, pin for pin.** SPI0 sits on physical 19/23/24 and all four control
> pins (22, 11, 18, 12) are plain GPIO there. No rewiring — see the
> [header table](12-pcb-1-schematic.md#the-orange-pi-5-plus-40-pin-header).
>
> **Software is a different matter.** The I²C bus on pins 3/5 is **I²C2**, not
> the Raspberry Pi's i2c-1, so code opening `/dev/i2c-1` talks to the wrong
> bus. Waveshare's examples also target `RPi.GPIO`-style access, so expect to
> port to `libgpiod` / `python-periphery` and to confirm which `spidev` node
> Armbian exposes. Waveshare documents Raspberry Pi, Jetson Nano, RDK X3,
> Arduino and STM32 — **Orange Pi is not on that list, and neither is the
> Pico.**

The absent Pico support is a point in favour of the first reading of the
[two-interfaces conflict](05-pcb-2-power.md#previously-flagged-conflicts--both-resolved): this panel is
the **Orange Pi's** display. If the PCB 2 OLED survives, it is a separate
power-box console, not a consolidation target.

## Refresh discipline is a hard requirement

This is the part that changes the design, not just the BOM.

| Behaviour | Figure |
|---|---|
| Full refresh | **4 s**, and it flickers |
| Partial refresh | Supported. **0.7 s** per the spec table, **~0.3 s** per the selection-table footnote — *unresolved* |
| Partial-refresh limit | After "several" partial refreshes a **full** refresh is required. One FAQ example says clear after 5 |
| Minimum refresh interval | Manual says **≥ 180 s**. A later bullet exempts "products that support the local brush function" and applies a 24-hour rule only to multi-colour panels — **the manual contradicts itself for this black/white part** |
| Refresh at least | Once every 24 hours (same contradiction applies) |
| Rated life | ~1,000,000 refreshes — a general FAQ answer, **not a rated spec for this SKU** |

Two rules that can destroy the panel, both stated by the manufacturer:

> [!CAUTION]
> **Never leave it powered in a static state.** The manual: *"If some e-paper
> screens are powered on for a long time, the screen will be damaged beyond
> repair."* Sleep or power off after **every** refresh. Note that after sleep,
> image data is ignored until the panel is re-initialised.
>
> **Burn-in is real.** Holding one image for a long time burns the screen. A
> status display that always shows the same idle screen is exactly the wrong
> usage pattern.

The `PWR` pin exists for this reason. It should be driven, not tied high.

This also lands on the shutdown path. If the Orange Pi crashes or loses power
mid-refresh and leaves the panel energised, the failure mode is a dead display,
not a stale one. Worth deciding whether the Pico — which
[05](05-pcb-2-power.md) already has booting before the Orange Pi — has any role
in guaranteeing the panel ends up asleep.

## What this does to the UI

**A 4 s full refresh and a ≥ 180 s guideline are incompatible with a live status
screen, and uncomfortable with a scroll wheel.**

The ANO wheel was specified to "rotate to browse, center to select". On a panel
with 0.3–0.7 s partial updates and a required full refresh every few of those,
per-detent visual feedback is not achievable. The wheel cannot drive a scrolling
list the way it would on an LCD.

What follows:

- **The UI has to be paged, not scrolled.** Discrete screens, with the wheel
  stepping between them and the center press confirming. Build the menu around
  a handful of pages, each a deliberate redraw.
- **The four RGB indicators become the live layer.** This was already the
  reasoning in [04](04-pcb-1-front-control.md#rfkill-is-not-an-interlock) —
  *"live feedback even when the display is showing a stale image"* — written
  about a hypothetical. With e-paper, **a stale image is the normal state.** The
  indicators are now the only thing that can show state changing in real time,
  which makes them load-bearing rather than decorative.
- **`AIRPLANE` feedback must not wait on a redraw.** Toggling the radios has to
  be visible immediately on the RGB indicator; the display catches up on its own
  schedule.

This is the one place the display choice should be re-examined. It is excellent
for *status at rest* — which is most of what a travel router needs to show — and
poor for *interaction*. If the intended experience is menu-driven configuration
on the device, that is a real mismatch and a small OLED or LCD would serve the
wheel better. If the intended experience is "glance at it to see what is going
on, configure over the web UI", the e-paper is the right call.

## Environment

| | |
|---|---|
| Operating temperature | **0 ~ 50 °C** |
| Storage | −25 ~ 60 °C (spec) · the FAQ separately says below 30 °C, < 55 %RH, 6 months max |
| Working humidity | 35–65 %RH |
| Viewing angle | > 170° (product page) · "almost 180°" (manual) |
| Use | Indoor recommended; outdoor display is **not** guaranteed or warranted |

> [!IMPORTANT]
> **0 °C is the narrowest environmental limit anywhere in this build.** The
> switches are rated −40 °C. A travel router that lives in a bag will see
> below-freezing transit, and the panel is only rated to −25 °C in *storage*.
> It will not display in a cold car. Accept this as a limitation of a device
> used indoors, or the display choice needs revisiting.

The manual also notes a cold-start colour cast: the panel wants 6 hours at 25 °C
before a refresh for correct appearance. Treat first-boot-after-transit oddness
as expected, not a fault.

## Grayscale is ambiguous

The pages list **"Grey Scale: 4"** alongside "Display Color: Black/White", while
the pixel format is described as 1 bit (`0` black, `1` white). How 4-level grey
is driven is undocumented. **Do not design a UI that needs grey** until it is
confirmed on hardware.

The **driver IC is not named** on either page.

## Open questions

- Bare glass outline, flex tail exit and bend radius, driver-board thickness —
  **measure, do not look up.**
- Partial refresh: 0.3 s or 0.7 s.
- Whether the ≥ 180 s refresh interval applies to this panel, and what that
  means for how often status may update.
- Porting Waveshare's Raspberry Pi examples to the Orange Pi 5 Plus —
  `spidev` exposure and GPIO library on Armbian Minimal.
- Whether 4-level grey is usable.
- Who guarantees the panel ends up asleep on an unclean shutdown.
- Whether paged navigation on e-paper is the experience wanted, or whether the
  wheel argues for a different display class.
- Mounting: its own bracket, per
  [02](02-enclosure-a-upper.md#contents-and-mounting) — geometry not designed.
