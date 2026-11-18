<div align="center">

# Vezha

### Your network, wherever you land.

**A handheld travel router that carries your home network with you.**
One radio joins the hotel Wi-Fi. The other broadcasts your own private
5 GHz network. Your devices never notice the difference.

<br>

[![Status](https://img.shields.io/badge/status-design%20%26%20research-orange?style=flat-square)](#project-status)
[![Stage](https://img.shields.io/badge/stage-pre--hardware-red?style=flat-square)](#project-status)
[![Docs](https://img.shields.io/badge/docs-4%20pages-brightgreen?style=flat-square)](#documentation)
[![License](https://img.shields.io/badge/license-Blue%20Oak%201.0.0-0F766E?style=flat-square)](LICENSE.md)
[![SPDX](https://img.shields.io/badge/SPDX-BlueOak--1.0.0-0F766E?style=flat-square)](https://spdx.org/licenses/BlueOak-1.0.0.html)

[![Last commit](https://img.shields.io/github/last-commit/ParkWardRR/vezha?style=flat-square)](https://github.com/ParkWardRR/vezha/commits/main)
[![Commit activity](https://img.shields.io/github/commit-activity/m/ParkWardRR/vezha?style=flat-square)](https://github.com/ParkWardRR/vezha/commits/main)
[![Issues](https://img.shields.io/github/issues/ParkWardRR/vezha?style=flat-square)](https://github.com/ParkWardRR/vezha/issues)
[![Repo size](https://img.shields.io/github/repo-size/ParkWardRR/vezha?style=flat-square)](https://github.com/ParkWardRR/vezha)
[![Stars](https://img.shields.io/github/stars/ParkWardRR/vezha?style=flat-square)](https://github.com/ParkWardRR/vezha/stargazers)

[![SBC](https://img.shields.io/badge/SBC-Orange%20Pi%205%20Plus-F47B20?style=flat-square)](#hardware)
[![SoC](https://img.shields.io/badge/SoC-Rockchip%20RK3588-0E7C7B?style=flat-square)](#hardware)
[![Uplink](https://img.shields.io/badge/uplink-Intel%20AX210-0071C5?style=flat-square&logo=intel&logoColor=white)](#hardware)
[![AP](https://img.shields.io/badge/AP-MediaTek%20MT7922-EC1C24?style=flat-square)](#hardware)
[![Wi-Fi](https://img.shields.io/badge/Wi--Fi-6E-1F8ACB?style=flat-square)](#hardware)
[![Bands](https://img.shields.io/badge/5%20GHz-simultaneous%20up%20%2B%20down-success?style=flat-square)](#the-hard-requirement)

[![OS](https://img.shields.io/badge/OS-Armbian%20Minimal-1A1A1A?style=flat-square&logo=linux&logoColor=white)](docs/handoff.md#software-and-network-behavior)
[![Alt OS](https://img.shields.io/badge/alt-OpenWrt%20%2B%20Travelmate-00B5E2?style=flat-square&logo=openwrt&logoColor=white)](docs/handoff.md#software-and-network-behavior)
[![VPN](https://img.shields.io/badge/VPN-undecided-lightgrey?style=flat-square)](docs/handoff.md#software-and-network-behavior)
[![WireGuard](https://img.shields.io/badge/WireGuard-candidate-88171A?style=flat-square&logo=wireguard&logoColor=white)](docs/handoff.md#software-and-network-behavior)
[![Tailscale](https://img.shields.io/badge/Tailscale-candidate-242424?style=flat-square&logo=tailscale&logoColor=white)](docs/handoff.md#software-and-network-behavior)

[![Enclosure](https://img.shields.io/badge/enclosure-3D%20printed%20STL-FF6F00?style=flat-square)](docs/antennas.md#enclosure-layout)
[![Antennas](https://img.shields.io/badge/antennas-4%C3%97%20Taoglas%20flex-blueviolet?style=flat-square)](docs/antennas.md)
[![Power](https://img.shields.io/badge/power-USB--C%20PD-333333?style=flat-square)](docs/handoff.md#power-and-portability)
[![Controls](https://img.shields.io/badge/controls-AIRPLANE%20%2B%203%20keys%20%2B%20wheel-795548?style=flat-square)](docs/controls.md)
[![Front board](https://img.shields.io/badge/front%20board-JLCPCB-2E7D32?style=flat-square)](docs/controls.md#before-sending-the-board-to-jlcpcb)
[![Form factor](https://img.shields.io/badge/form%20factor-handheld-9C27B0?style=flat-square)](docs/antennas.md#enclosure-layout)

</div>

---

> [!WARNING]
> **This repo is a design, not a build.** Nothing here has been assembled,
> measured, or bench-tested. There is no confirmed dual-radio result, no
> frozen BOM, no runtime measurement, and no working VPN or captive-portal
> implementation. Part numbers, prices, and layouts are candidates to
> re-verify — not selections. See [Project status](#project-status).

## The problem

Every hotel, rental, and conference network means setting up each device
again: joining the SSID, clicking through a captive portal, losing the
printers and shares and hostnames you had at home. Devices that can't easily
run a VPN client — a work laptop with locked-down MDM, a streaming stick, a
console — are stuck on the hotel's network with whoever else is on it.

Vezha puts one box between your devices and that mess. It deals with the
hotel network once. Your devices join one familiar private SSID, everywhere,
and reach home through a tunnel the router maintains on their behalf.

## The hard requirement

**Two independent Wi-Fi radios, both on 5 GHz, at the same time** — a 5 GHz
upstream client *and* a 5 GHz downstream private AP running concurrently.

This is the constraint that rules out most off-the-shelf travel routers and
most single-card builds:

- A 2.4 GHz + 5 GHz split does **not** meet the goal — it leaves the private
  network on the slow, congested band.
- A shared-radio repeater does **not** meet the goal — it halves throughput
  and ties the private SSID's fate to the uplink.

Everything else in this project is downstream of that one requirement.

## How it works

```mermaid
flowchart LR
    HOTEL([Hotel / public<br/>5 GHz AP]):::ext
    subgraph VEZHA["Vezha — Orange Pi 5 Plus (RK3588)"]
        direction LR
        AX210["<b>Intel AX210</b><br/>client mode<br/><i>5 GHz uplink</i>"]:::up
        ROUTE["routing · NAT · DNS<br/>captive-portal handling<br/>VPN tunnel"]:::core
        MT["<b>MediaTek MT7922</b><br/>AP mode<br/><i>5 GHz private SSID</i>"]:::ap
        AX210 --> ROUTE --> MT
    end
    HOME([Home network<br/>over VPN]):::ext
    DEV([Your devices<br/>laptop · phone · console]):::ext

    HOTEL -.->|"joins, signs in<br/>to portal"| AX210
    MT -.->|"one familiar SSID"| DEV
    ROUTE ==>|encrypted tunnel| HOME

    classDef ext fill:#f1f5f9,stroke:#64748b,color:#0f172a
    classDef up fill:#dbeafe,stroke:#2563eb,color:#0f172a
    classDef ap fill:#ffedd5,stroke:#ea580c,color:#0f172a
    classDef core fill:#dcfce7,stroke:#16a34a,color:#0f172a
```

The private SSID is deliberately **independent of uplink recovery**: when the
hotel link drops, re-authenticates, or gets swapped for a different network,
your devices stay associated and don't need to be touched.

## Hardware

| Part | Choice | Status |
|---|---|---|
| Host | Orange Pi 5 Plus (RK3588) | Leading platform — not purchased |
| Uplink radio | Intel AX210 (Wi-Fi 6E) | **On hand**, role assigned |
| AP radio | MediaTek MT7922 / AMD RZ616 | Candidate — 5 GHz AP operation unvalidated |
| Antennas | 4 × Taoglas FXP830 flex, 2 per radio | Candidate — [comparison](docs/antennas.md) |
| Power | USB-C PD → regulated 5 V | Profile and converter unresolved |
| Storage | eMMC | Discussed, unconfirmed |
| Controls | `AIRPLANE` toggle + 3 keys + ANO wheel | [Designed](docs/controls.md), not ordered |
| Enclosure | Custom 3D-printed, replaceable top cap | Not designed |

> [!NOTE]
> 6 GHz AP operation is **not** assumed. The AX210 and MT7922 are 6E-capable
> parts, but AP-mode 6 GHz depends on kernel, firmware, and regulatory domain
> — it's a thing to verify, not a feature to plan around.

## Documentation

| Page | What's in it |
|---|---|
| **[handoff.md](docs/handoff.md)** | The master document — goal, hardware status, power budget, software plans, enclosure notes, ordered next work |
| **[antennas.md](docs/antennas.md)** | Antenna comparison with published dBi, enclosure layout sketch, and the bench test that decides whether the uplink needs external antennas |
| **[controls.md](docs/controls.md)** | Front faceplate — `AIRPLANE` toggle, three action keys and ANO wheel, full control BOM, JLCPCB assembly caveats, mechanical test coupon |
| **[parts-sourcing.md](docs/parts-sourcing.md)** | JLCPCB/LCSC part lookup method and components checked so far |

## Project status

| Milestone | State |
|---|---|
| Both PCIe cards enumerate simultaneously | ❌ Not tested |
| Simultaneous 5 GHz client + AP passing traffic | ❌ Not tested |
| Captive portal login / reconnect / VPN recovery | ❌ Not implemented |
| Power measured at the board, battery runtime | ❌ Not measured |
| RF compared open / closed / in-hand | ❌ Not measured |
| Enclosure and BOM frozen | ❌ Not frozen |

### Roadmap

1. **Verify the parts.** Confirm what's on hand and how both PCIe cards
   connect. Verify both enumerate at once.
2. **Bring up the radios.** Boot Armbian Minimal, AX210 in client mode,
   MT7922 in AP mode, real client traffic with both links on 5 GHz. Record
   kernel, firmware, country setting, channels, stability.
3. **Make it survive travel.** Captive-portal login, reconnect, VPN recovery.
   Verify the private SSID stays up when the uplink drops.
4. **Measure it.** Power at the board, battery runtime, RF with the enclosure
   open, closed, and held normally.
5. **Freeze it.** Enclosure and parts list only after the above. Touchscreen,
   physical controls, and Wi-Fi surveying come afterward.

Full detail behind each step is in [handoff.md](docs/handoff.md).

## Design principles

- **Treat suggestions as candidates, not purchases.** Nothing moves from
  "discussed" to "chosen" without a bench result behind it.
- **Catalog specs are not measurements.** Published antenna gain, connector
  ratings, and battery capacity figures describe a part in isolation, not this
  build.
- **The private network is the product.** Uplink churn is an implementation
  detail that should never reach the client devices.
- **Verify before machining.** Panel cutouts come from current manufacturer
  drawings, never from nominal dimensions.

## License

[Blue Oak Model License 1.0.0](LICENSE.md) — SPDX `BlueOak-1.0.0`.

A plain-language permissive license: do what you like with it, contributors
get an explicit patent grant and a liability disclaimer. Comparable in effect
to MIT or Apache-2.0, written to be readable.

Blue Oak covers *software*. If the enclosure STLs and PCB design files become
the substantial part of this repo, a hardware license such as CERN-OHL-S or
CERN-OHL-P would fit those better — the two can coexist, scoped by directory.

---

<div align="center">
<sub><b>Vezha</b> — your network, wherever you land.</sub>
</div>
