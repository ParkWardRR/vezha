# Retired — cut from v1, kept on purpose

Nothing here is built in v1. Nothing here is deleted either.

On **2026-11-18** Vezha v1 was cut to a **headless** router: the upper box is a
sealed shell holding the SBC, radios, antennas and a USB-C inlet, and the
router's entire UI is the web UI. That removed the display, the front panel,
and the whole of PCB 1 — after all three had been specified, sourced,
simulated and in one case fully drawn.

**The work was finished, not abandoned.** It is kept so a v2 front panel
inherits it rather than rediscovering it.

Reasoning for the cut, and what it bought:
[01 · The v1 scope cut](../01-architecture.md#the-v1-scope-cut).

## What is here

| Document | What it was | Worth keeping for |
|---|---|---|
| [pcb-1-front-control.md](pcb-1-front-control.md) | Requirements for the front control board — `AIRPLANE` toggle, three keys, ANO wheel, four RGB indicators | The RGB driver design, the stale-indicator hazard, the faceplate and optics rules, the key-feel coupons |
| [pcb-1-schematic.md](pcb-1-schematic.md) | Net-by-net schematic. **Complete and believed correct** | **Its 40-pin header map is still correct and still useful** regardless of what is attached to the Orange Pi |
| [display-epaper.md](display-epaper.md) | Waveshare 4.26" e-paper, SKU `26376` — chosen 11-17, cut 11-18 | Refresh discipline, temperature limits, and what a slow panel does to a UI |

Retired simulation decks live in [`sim/retired/`](../../sim/retired/):
`11-i2c-pullups`, `12-led-driver-thermal`, `13-key-debounce`. All three still
parse and produce their recorded results.

## Two findings that outlived the board

Both were corrections to earlier mistakes, and both are worth reading before
anyone designs a v2 panel.

**1 · RC key debounce works — in a window, not above a floor.**
An earlier conclusion that hardware RC debounce "cannot work on a
switch-to-ground input" was **wrong**, and the error was the pass criterion
rather than the arithmetic. The deck asked whether the filter hides bounce
*entirely*, which almost nothing passes and which debounce does not require.
The right question is whether the input manufactures a **second edge after it
has already read a valid low**.

Corrected result — **10 kΩ pull-up, 1 kΩ series, 100 nF per key**:

| C | Peak after first valid low | |
|---|---|---|
| 1 nF | 3.300 V | ❌ |
| 10 nF | 2.195 V | ❌ |
| 47 nF | 1.086 V | ✅ best margin |
| **100 nF** | **1.627 V** | ✅ **chosen** |
| 220 nF | 2.314 V | ❌ |
| 470 nF | never reaches a valid low | ❌ |

**Too much capacitance fails too** — the cap stops discharging fully during
short closures. 100 nF over 47 nF for commonality with PCB 2's encoder RC.

The external 10 kΩ pull-up stays for a reason unrelated to bounce: **an
internal pull-up is not active before pinmux runs.**

**2 · The indicator current was overstated twice.**
PCB 1's RGB indicators were carried in the seam budget at ~240 mA, assuming
20 mA/channel. That was already stale at ~120 mA before the cut. **In v1 it is
zero** — nothing is attached to the 40-pin header.

## What v1 gives up

Recorded honestly in [09 · Background](../09-background.md):

- **No at-rest status of any kind.** A powered-down or wedged Vezha shows
  nothing. The e-paper would have held its last screen with power removed.
- **No hardware radio cut.** The original brief asked for physical radio
  controls; v1 does not meet that.
- **No home for the Wi-Fi join QR code.**

The only hardware panel in v1 is PCB 2's OLED and encoder, in the power box,
and it can show **power and PD state only**.
