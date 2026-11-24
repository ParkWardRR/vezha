# 09 · Software, Network Behaviour and Bring-up

What the router has to *do*, and the order to prove it in.

> [!IMPORTANT]
> **Nothing in this document is implemented.** These are design tasks and a
> bring-up order, not features. No OS has been booted, no radio brought up, no
> portal or VPN exercised.
>
> This is also the **only** live document covering software. The rest of the
> repo is hardware. Where the two meet — the seam, the power sequencing, the
> radios — the hardware docs win on *what exists*, and this one owns *what it
> has to do*.

## The goal, restated

Vezha joins whatever uplink is available and presents **one familiar private
SSID**, so devices are set up once rather than at every hotel.

**Hard requirement:** two independent Wi-Fi radios — a **5 GHz upstream client
and a 5 GHz downstream private AP, simultaneously.** A 2.4 + 5 GHz split, or a
shared-radio repeater, does not meet it.

### First usable version

Battery-powered, and it must:

1. Join hotel Wi-Fi
2. Handle **captive portal sign-in**
3. Keep the **private 5 GHz SSID up during uplink changes**
4. Route client traffic through a **VPN when enabled**

**The VPN technology and the fallback policy are not selected.**

## Where v1 departs from the original brief

Everything else in the scope cut was simplification. This one is a loss, and
it is recorded here so it is not quietly forgotten.

> [!WARNING]
> The original brief asked for **physical controls for radio enable/disable and
> for restarting the hotel-login workflow** — including changing the uplink MAC
> for a fresh login.
>
> **v1 does not meet that.** Enclosure A has a display but
> [no controls](01-architecture.md#no-controls-in-v1); every one of those
> actions moves to the web UI.

That paragraph is the reason a front panel was specified in the first place.
Re-read it before v2 — the finished design is preserved in
[retired/](retired/pcb-1-front-control.md).

**What the display does and does not recover.** Enclosure A's OLED gives back
*status*, not *control* — it can show uplink state, client count and the
Wi-Fi join details, which the headless revision could not. It does **not**
give back any way to act on what it shows. And because it is driven by the
Orange Pi, **a host that fails to boot shows nothing**: the panel reports on
the router, so it cannot report that the router is dead.

There are two panels and they see different things:

| | Driven by | Shows | Live when |
|---|---|---|---|
| **Enclosure A OLED** | The Orange Pi | Router state | The host has booted |
| **Power module OLED + encoder** | The Pico 2 | Power and PD state only | Always — the Pico boots first |

Neither can speak for the other: **no signal crosses between the boxes.**
See [05](05-power-board.md).

## Software this adds

Three host-side jobs that did not exist in the headless revision. None is
implemented.

- **Drive the OLED.** [Adafruit 5297](https://www.adafruit.com/product/5297),
  SH1107 over **I²C** on the 40-pin header. The pin map, the 3.3 V supply and
  the bus address are all unspecified.
- **Mitigate burn-in.** A status panel is a static image, which is the OLED
  failure mode. A screensaver, periodic pixel shift or timeout is cheaper to
  plan for than to retrofit — the module datasheet says afterimage clears if
  the display is left unused for a while, so a timeout may be enough.
- **Read the fan tachometer.** The fan is 3-pin with a tach output and **no
  PWM input**, so there is no speed control to write — but the tach is the
  only way to know the fan still turns inside a closed box, and the OLED is
  somewhere to report it. Whether the fan is switched at all is
  [an open hardware question](02-enclosure-a-upper.md#thermal).

**What to show is not decided.** Uplink state, client count, rail voltage and
the Wi-Fi join details are the obvious candidates. Worth settling early: it
decides whether the 20 mm panel is big enough, because a scannable join QR is
marginal at that size and a larger OLED moves the front-face geometry.
[02 · The display](02-enclosure-a-upper.md#the-display)

## Software direction

None of this is a commitment.

| Area | Leading option | Standing |
|---|---|---|
| OS | **Armbian Minimal** on the Orange Pi 5 Plus | Leading start point |
| Management UI | **RaspAP** as an optional web frontend | Not a proven turnkey fit. **Direct Linux networking config is the fallback** if RaspAP's interface management gets in the way |
| Alternative path | **OpenWrt + Travelmate** for saved uplinks and automatic reconnect | A separate software path, not chosen |
| VPN | **WireGuard** or **Tailscale** | Both mentioned, **neither selected** |

**Bring the two radios up directly before adding any management UI.** A
management layer that owns the interfaces makes radio bring-up harder to debug,
not easier.

## Network behaviour to design

These are the decisions that make the product work, and none has been made.

**Keep the private Wi-Fi independent of uplink recovery.** Client devices must
stay associated across uplink drops, re-authentication and network changes.
This is the single behaviour that distinguishes Vezha from a repeater.

Work through, explicitly:

- Initial hotel **captive-portal login**, and **re-authentication** when the
  portal expires
- **Uplink reconnect** and switching between saved networks
- **VPN bring-up and recovery** after an uplink change
- **What happens to client traffic while the tunnel is down** — fail closed,
  fail open, or hold. This is a policy decision with a security consequence,
  not an implementation detail
- **How portal login works before the tunnel is established** — the portal
  must be reachable while the VPN is not yet up
- **What the clock reads before NTP can run.** The portal is HTTPS, WireGuard
  rejects a clock that moved backwards, and neither works until the uplink is
  already up. Decide the ordering — RTC, `fake-hwclock` fallback, and when
  `systemd-timesyncd` is allowed to step the clock.
  [02 · RTC backup cell](02-enclosure-a-upper.md#rtc-backup-cell)

## Bring-up order

Each step depends on the one before it. Do not reorder.

1. **Confirm the parts and the topology.** Both PCIe cards connect, and **both
   enumerate at the same time.** See
   [01 · Radio topology](01-architecture.md#radio-topology).
2. **Boot Armbian Minimal.** AX210 in client mode, MT7922 in AP mode, real
   client traffic with **both links on 5 GHz**. Record kernel, firmware,
   country setting, channels, stability. **Check the RTC in the same
   session:** `cat /proc/driver/rtc` with the backup cell fitted, then cut
   power for several minutes and confirm the date survives the dead box —
   [02 · RTC backup cell](02-enclosure-a-upper.md#rtc-backup-cell).
3. **Exercise travel conditions.** Captive-portal login, reconnect, VPN
   recovery. Verify the **private SSID stays up when the uplink drops.**
4. **Measure.** Power at the board, battery runtime, and RF with the enclosure
   open, closed and held normally — see
   [04 · Bench test](04-antennas.md#bench-test-before-committing).
5. **Freeze** the enclosure and parts list only after the above.

> [!NOTE]
> Steps 1 and 2 are also what resolve the repo's two largest hardware unknowns:
> **peak current at the Orange Pi** and the **sealed-box thermal derating**.
> Instrument for both while the case is open — see
> [05 · Measurement](05-power-board.md#measurement-before-trusting-any-of-this).

## Deferred

- **Physical radio controls and at-rest status** — the finished front-panel
  design is in [retired/](retired/pcb-1-front-control.md)
- **LiDAR-assisted Wi-Fi mapping** — a stretch goal that should stay separate
  from core router bring-up
- **6 GHz AP operation** — unverified, and not assumed anywhere. See
  [04 · Open questions](04-antennas.md#open-questions)

## History

The original project handoff, written before the mechanical and power
architecture existed, is preserved at
[retired/original-handoff.md](retired/original-handoff.md). Its hardware,
power and repository sections are fully superseded; the software direction
above is the part that survived.
