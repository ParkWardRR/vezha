# Retired · Original Project Handoff

> [!WARNING]
> **Fully retired. Historical record only.** This was the first handoff,
> written before the mechanical and power architecture existed. It is kept
> because it is the origin of several requirements, not because any of it is
> current.
>
> **Nothing here should be designed against.** Where it disagrees with a live
> document, the live document wins — always.
>
> | This document | Superseded by |
> |---|---|
> | Power is a 5 V / 5 A bench-supply target, converter undecided | [01](../01-architecture.md) · [05](../05-power-board.md) — RotoPD Pro → Pololu → Pico-gated rail |
> | Radio fit and slot topology undetermined | [01](../01-architecture.md) · [02](../02-enclosure-a-upper.md) — AX210 top-side E-key, second radio on an underside adapter |
> | A battery lives in the portable build | [03](../03-enclosure-b-lower.md) — external USB-C source; internal cell is an open question |
> | A touchscreen, then an e-paper panel, then physical controls | [01 · The v1 scope cut](../01-architecture.md#the-v1-scope-cut) — **v1 is headless** |
> | Repo owner, URL and creation status unverified | Repo exists and is public |
> | Software direction, captive portal, VPN, bring-up order | **[09 · Software and bring-up](../09-software-and-bringup.md)** — carried forward live |
>
> The software sections were the only part still load-bearing. They now live in
> [09](../09-software-and-bringup.md); what remains below is kept verbatim as
> the record of where the project started.

## Goal

Build a compact, handheld travel router that extends my home network when
I travel. Vezha joins the available uplink, and my devices
connect to one familiar private SSID instead of being set up individually
on each hotel's network.

Hard requirement: two independent Wi-Fi radios, with a 5 GHz upstream
client and a 5 GHz downstream private AP operating simultaneously.
A 2.4 GHz + 5 GHz split, or a shared-radio repeater, does not meet the goal.

First usable version: battery-powered, joins hotel Wi-Fi, handles captive
portal sign-in, keeps the private 5 GHz SSID up during uplink changes,
and routes client traffic through a VPN when enabled. The VPN technology
and fallback policy have not been selected.

## Hardware and current status

| Area | What we know |
|---|---|
| Host | Orange Pi 5 Plus (RK3588) is the leading platform. The 4 GB variant was discussed; purchase and assembly are not confirmed. |
| Uplink radio | I own an Intel AX210 M.2 Wi-Fi 6E card. Latest proposed role: hotel/public Wi-Fi client. |
| Private AP radio | MediaTek MT7922 / AMD RZ616 is the latest proposed AP candidate. Validate stable 5 GHz AP operation on the actual kernel, firmware, and regulatory configuration. Do not assume 6 GHz AP support. |
| Radio fit | Target two laptop-sized PCIe Wi-Fi cards. Exact slot/adapter topology, physical clearance, and simultaneous enumeration still need verification. |
| Alternate radios | Earlier design considered using the MT7922 as the uplink and an AsiaRF AW7916-AED as the private AP if the enclosure can fit it. MT7925 was discussed as a compact Wi-Fi 7 alternative, not chosen. |
| Buying preference | Favor low-power Wi-Fi 6E hardware that does not require dedicated cooling. Used cards from eBay are an option. |
| Storage | eMMC was discussed, not confirmed. |

## Power and portability

The complete build needs to power the SBC, two radios, storage, and some
USB peripheral load. A touchscreen may add to that budget. *(Moot as of
2026-11-18 — [v1 has no display at all](../01-architecture.md#the-v1-scope-cut),
so nothing in Enclosure A draws power except the SBC and its peripherals.)*

The previous bench supply target was a regulated 5 V / 5 A. This is a
supply-sizing target, not measured system consumption. The portable
concept is to negotiate a suitable higher-voltage USB-C PD profile and
convert it to regulated 5 V for the board. The Geekworm Pi5-5V5APD
module was discussed as a candidate, not validated in this build.

An Anker 10,000 mAh PowerIQ bank came up, but the exact model and its PD
output profiles are unconfirmed. Do not assume its advertised wattage or
capacity means it can directly power the finished unit. Verify the PD
profile and measure voltage at the board under cold boot, simultaneous
radio traffic, and USB load. Runtime, thermal behavior, and the final
power bank/converter/cable combination are open.

## Software and network behavior

Armbian Minimal is the leading starting point for the Orange Pi 5 Plus.
Bring up the two radios directly before adding a management UI. RaspAP
was discussed as an optional web frontend, not a proven turnkey fit.
Direct Linux networking configuration is the fallback if RaspAP's
interface management gets in the way.

OpenWrt with Travelmate was discussed as a separate software path for
saved uplinks and automatic reconnect. Neither OpenWrt nor RaspAP is a
final commitment. WireGuard and Tailscale were mentioned in repo-topic
discussion, not selected as the VPN stack.

Keep private Wi-Fi independent of uplink recovery. Work through initial
hotel captive-portal login, reauthentication, uplink reconnects, and how
to bring up and recover the VPN. Decide explicitly what happens to client
traffic while the tunnel is down and how portal login works before the
tunnel is established. These are design tasks, not implemented features.

## Enclosure, antenna layout, and controls

Design a custom 3D-printed STL enclosure for handheld use. The leading
antenna concept is four internal Taoglas flex antennas, two per radio,
with a replaceable top cap to keep alternatives open. Stub antennas,
Octane/dome-style options, and intermediate options were discussed;
no final antenna SKU or geometry is confirmed.

Do not interpret the earlier layout discussion as one antenna each on
the front, top, back, and bottom. Temporarily mount the antennas and
compare open case, closed case, and normal hand grip before committing
to adhesive or printed mounts. The prior suggestion was to reposition
the AX210 pair first if gripping or closing the case hurts the uplink,
then try alternative antennas if needed.

Optional UI: Waveshare 3.5-inch HDMI touchscreen was suggested. Physical
controls for radio enable/disable and restarting the hotel-login
workflow were discussed, including changing the uplink MAC for a fresh
login. No display, switch wiring, or button assignments are confirmed.

**Superseded 2026-11-17:** the display became the Waveshare 4.26-inch
e-Paper HAT (SKU 26376), SPI rather than HDMI and with no touch layer.
See [10-display.md](display-epaper.md).

**Superseded again 2026-11-18 — and this one closes the thread.** Vezha v1
has **no display and no physical controls.** The original ask above, "physical
controls for radio enable/disable and restarting the hotel-login workflow,"
is **not met in v1**; both move to the web UI. That is the one place the v1
scope cut departs from the original brief rather than merely simplifying it —
see [01 · The v1 scope cut](../01-architecture.md#the-v1-scope-cut). Worth
re-reading before v2, because this paragraph is the reason a front panel was
specified in the first place.

LiDAR-assisted Wi-Fi mapping is a stretch goal and should stay separate
from the core router bring-up.

## Repository and identity

Project: Vezha
Planned GitHub repo: vezha
README title: Vezha — Travel Router
Description: A travel router for taking your home network on the road.
Tagline: Your network, wherever you land.
Suggested topics: travel-router, router, networking, homelab, self-hosted

Do not add stack-specific tags until the repo actually contains the
relevant configuration or docs. The repo owner, URL, contents, and
creation status have not been verified.

## Next work, in order

1. Confirm the actual parts on hand and how both PCIe cards connect to
   the board. Verify that both enumerate at the same time.
2. Boot Armbian Minimal. Put the AX210 in client mode and the MT7922 in
   AP mode, then pass real client traffic with both links on 5 GHz.
   Record kernel, firmware, country setting, channels, and stability.
3. Exercise hotel-style captive-portal login, reconnect, and VPN
   recovery. Verify that the private SSID stays up when uplink drops.
4. Measure power at the board and test battery runtime. Compare RF
   performance with the enclosure open, closed, and held normally.
5. Freeze the enclosure and parts list only after those tests. Add the
   touchscreen, physical controls, and surveying features afterward.

Treat suggestions as candidates, not purchases or successful tests.
There is no confirmed dual-radio bench result, final BOM, runtime
measurement, enclosure revision, or working VPN/portal implementation
in this handoff.
