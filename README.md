<div align="center">

# Vezha — Travel Router

**Your network, wherever you land.**

A travel router for taking your home network on the road.

<!-- Project status -->

[![Status](https://img.shields.io/badge/status-design%20%26%20research-orange?style=flat-square)](docs/handoff.md)
[![Bench test](https://img.shields.io/badge/dual--radio%20bench%20test-not%20yet%20run-red?style=flat-square)](docs/handoff.md#next-work-in-order)
[![BOM](https://img.shields.io/badge/BOM-not%20frozen-red?style=flat-square)](docs/parts-sourcing.md)
[![Hardware](https://img.shields.io/badge/hardware-not%20assembled-red?style=flat-square)](docs/handoff.md#hardware-and-current-status)
[![Docs](https://img.shields.io/badge/docs-4%20pages-brightgreen?style=flat-square)](#documentation)

<!-- Hardware -->

[![SBC](https://img.shields.io/badge/SBC-Orange%20Pi%205%20Plus-F47B20?style=flat-square)](docs/handoff.md#hardware-and-current-status)
[![SoC](https://img.shields.io/badge/SoC-Rockchip%20RK3588-0E7C7B?style=flat-square)](docs/handoff.md#hardware-and-current-status)
[![Uplink radio](https://img.shields.io/badge/uplink-Intel%20AX210-0071C5?style=flat-square&logo=intel&logoColor=white)](docs/antennas.md)
[![AP radio](https://img.shields.io/badge/AP-MediaTek%20MT7922%20%2F%20RZ616-EC1C24?style=flat-square)](docs/antennas.md)
[![Wi-Fi](https://img.shields.io/badge/Wi--Fi-6E-1F8ACB?style=flat-square)](docs/handoff.md#goal)
[![Bands](https://img.shields.io/badge/5%20GHz-simultaneous%20up%20%2B%20down-success?style=flat-square)](docs/handoff.md#goal)
[![6 GHz AP](https://img.shields.io/badge/6%20GHz%20AP-unverified-lightgrey?style=flat-square)](docs/antennas.md#open-questions)

<!-- Build -->

[![Antennas](https://img.shields.io/badge/antennas-4%C3%97%20Taoglas%20flex-blueviolet?style=flat-square)](docs/antennas.md)
[![Enclosure](https://img.shields.io/badge/enclosure-3D%20printed%20STL-FF6F00?style=flat-square)](docs/antennas.md#enclosure-layout)
[![Power](https://img.shields.io/badge/power-USB--C%20PD-333333?style=flat-square)](docs/handoff.md#power-and-portability)
[![Battery](https://img.shields.io/badge/battery-runtime%20unmeasured-lightgrey?style=flat-square)](docs/handoff.md#power-and-portability)
[![Controls](https://img.shields.io/badge/controls-AIRPLANE%20%2B%203%20keys%20%2B%20ANO%20wheel-795548?style=flat-square)](docs/controls.md)
[![Front board](https://img.shields.io/badge/front%20board-JLCPCB%20assembly-2E7D32?style=flat-square)](docs/controls.md#before-sending-the-board-to-jlcpcb)
[![Form factor](https://img.shields.io/badge/form%20factor-handheld-9C27B0?style=flat-square)](docs/antennas.md#enclosure-layout)

<!-- Software -->

[![OS](https://img.shields.io/badge/OS-Armbian%20Minimal-1A1A1A?style=flat-square&logo=linux&logoColor=white)](docs/handoff.md#software-and-network-behavior)
[![Alt OS](https://img.shields.io/badge/alt-OpenWrt%20%2B%20Travelmate-00B5E2?style=flat-square&logo=openwrt&logoColor=white)](docs/handoff.md#software-and-network-behavior)
[![VPN](https://img.shields.io/badge/VPN-undecided-lightgrey?style=flat-square)](docs/handoff.md#software-and-network-behavior)
[![WireGuard](https://img.shields.io/badge/WireGuard-candidate-88171A?style=flat-square&logo=wireguard&logoColor=white)](docs/handoff.md#software-and-network-behavior)
[![Tailscale](https://img.shields.io/badge/Tailscale-candidate-242424?style=flat-square&logo=tailscale&logoColor=white)](docs/handoff.md#software-and-network-behavior)
[![Captive portal](https://img.shields.io/badge/captive%20portal-design%20task-yellow?style=flat-square)](docs/handoff.md#software-and-network-behavior)

<!-- Repo -->

[![Repo](https://img.shields.io/badge/repo-private-black?style=flat-square&logo=github&logoColor=white)](https://github.com/ParkWardRR/vezha)
[![License](https://img.shields.io/badge/license-Blue%20Oak%201.0.0-0F766E?style=flat-square)](LICENSE.md)
[![SPDX](https://img.shields.io/badge/SPDX-BlueOak--1.0.0-0F766E?style=flat-square)](https://spdx.org/licenses/BlueOak-1.0.0.html)
[![Topics](https://img.shields.io/badge/topics-travel--router%20%C2%B7%20homelab%20%C2%B7%20self--hosted-informational?style=flat-square)](https://github.com/ParkWardRR/vezha)

<!--
  Live repo badges — shields.io cannot read a private repo, so these render
  as "repo not found" until ParkWardRR/vezha is made public. Uncomment then.

[![Last commit](https://img.shields.io/github/last-commit/ParkWardRR/vezha?style=flat-square)](https://github.com/ParkWardRR/vezha/commits/main)
[![Commit activity](https://img.shields.io/github/commit-activity/m/ParkWardRR/vezha?style=flat-square)](https://github.com/ParkWardRR/vezha/commits/main)
[![Repo size](https://img.shields.io/github/repo-size/ParkWardRR/vezha?style=flat-square)](https://github.com/ParkWardRR/vezha)
[![Issues](https://img.shields.io/github/issues/ParkWardRR/vezha?style=flat-square)](https://github.com/ParkWardRR/vezha/issues)
[![Stars](https://img.shields.io/github/stars/ParkWardRR/vezha?style=flat-square)](https://github.com/ParkWardRR/vezha/stargazers)
-->


</div>

---

Vezha is my travel router project, built as a portable extension of my
`alpina.casa` home network. The goal is simple: connect the router to whatever
uplink is available, then let my devices join the same familiar Wi-Fi instead
of setting up each one again at every stop.

**Hard requirement:** two independent Wi-Fi radios, with a 5 GHz upstream
client and a 5 GHz downstream private AP running at the same time. A
2.4 GHz + 5 GHz split, or a shared-radio repeater, does not meet the goal.

## Documentation

| Page | What's in it |
|---|---|
| [handoff.md](docs/handoff.md) | Project handoff — goal, hardware status, power and software plans, enclosure notes, ordered next work |
| [antennas.md](docs/antennas.md) | Antenna comparison with published dBi, enclosure layout sketch, and the bench test to run before freezing the STL |
| [controls.md](docs/controls.md) | Front faceplate — `AIRPLANE` toggle, three action keys and ANO wheel, full control BOM, JLCPCB assembly caveats, mechanical test coupon |
| [parts-sourcing.md](docs/parts-sourcing.md) | JLCPCB/LCSC part lookup method and components checked so far |

## Status

Nothing here is built, measured, or purchased. The red badges above are
accurate: there is **no confirmed dual-radio bench result, no final BOM, no
runtime measurement, no enclosure revision, and no working VPN or captive
portal implementation.**

Part numbers, prices, and layouts in these docs are candidates to re-verify,
not selections. Published gain and spec figures are manufacturer catalog
values, not measurements taken in this enclosure.

## Next work, in order

1. Confirm parts on hand and how both PCIe cards connect. Verify both
   enumerate simultaneously.
2. Boot Armbian Minimal. AX210 in client mode, MT7922 in AP mode, real client
   traffic with both links on 5 GHz. Record kernel, firmware, country setting,
   channels, stability.
3. Exercise captive-portal login, reconnect, and VPN recovery. Verify the
   private SSID stays up when the uplink drops.
4. Measure power at the board and test battery runtime. Compare RF performance
   with the enclosure open, closed, and held normally.
5. Freeze the enclosure and parts list only after those tests. Touchscreen,
   physical controls, and surveying features come afterward.

See [handoff.md](docs/handoff.md) for the full detail behind each step.

## License

[Blue Oak Model License 1.0.0](LICENSE.md) — SPDX `BlueOak-1.0.0`.

A plain-language permissive license: do what you like with it, contributors
get an explicit patent grant and a liability disclaimer. Comparable in effect
to MIT or Apache-2.0, written to be readable.

Note it covers *software*. If the enclosure STLs and PCB design files end up
being the valuable part of this repo, a hardware license such as CERN-OHL-S or
CERN-OHL-P would fit those better — the two can coexist, scoped by directory.
