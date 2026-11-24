# 01 · Brief — Upright Orange Pi 5 Plus Enclosure

> [!CAUTION]
> **Corrections to the brief below — read these first.**
>
> | The brief says | Actual |
> |---|---|
> | `OPENING TO LOWER MODULE` at the bottom | **No bottom opening.** The bottom is a **closed, stable foot** |
> | `40-PIN HEADER ACCESS OPENING`, and *"provide bottom access"* | **No header access.** The header is **internal only** — [0.5](README.md#05--the-40-pin-header-is-internal-only) |
> | *"Keep the lower header area available for a future module"* | The power module mounts on the **back** |
> | Fan at 40 × 40 × 10 mm | **12 mm installed** with its anti-vibration pads |
> | 30 mm cap depth | Does not survive [the depth budget](README.md#03--run-the-depth-budget--it-does-not-currently-close) |
>
> The display is an **OLED**, not e-paper. Ventilation is an explicit final
> phase — [Phase 5](README.md#phase-5--ventilation-and-airflow).
>
> **The ASCII diagrams below were not redrawn.** This file is the verbatim
> source brief; [the plan](README.md) is what to build from.

---

```text
DESIGN BRIEF — UPRIGHT ORANGE PI 5 PLUS ENCLOSURE
Game Boy-style handheld with a replaceable antenna cap.
Display faces forward; Orange Pi stands vertically behind it.
Orient the board so its 40-pin header is at the bottom.
Do not include antenna placement or antenna mounts in this revision.


FRONT VIEW — ASSEMBLED
=============================================

             <------ CASE WIDTH ------>
             +------------------------+
             |                        |
             |  REPLACEABLE ANTENNA   |
             |          CAP           |
             |                        |
             +========================+ <-- Removable cap seam
             |                        |
             |  +------------------+  |
             |  |                  |  |
             |  |                  |  |
             |  |     DISPLAY      |  |
             |  |                  |  |
             |  |                  |  |
             |  +------------------+  |
             |                        |
             |   CONTROL AREA /       |
             |   SPACE RESERVED       |
             |                        |
             +------------------------+
                 BOTTOM OF DEVICE


SIDE VIEW — SECTION
=============================================

       FRONT                         REAR
         |                             |
         v                             v
         +-----------------------------+
         |                             |
         |   REMOVABLE HOLLOW CAP      |
         |                             |
         +=============================+ <-- Cap seam
         |       CABLE PASSAGE         |
         |                             |
         | +---+       +---+           |
         | |   |       |   |  COOLING  |
         | | D |       | O |  SPACE    |
         | | I |       | P |           |
         | | S |       | I |           |
         | | P |       |   |           |
         | | L |       | 5 |           |
         | | A |       | + |           |
         | | Y |       |   |           |
         | +---+       +---+           |
         |               |             |
         |       40-PIN HEADER         |
         |       AT LOWER BOARD EDGE   |
         |                             |
         |   HEADER ACCESS / CLEARANCE |
         +-------------     -----------+
                       OPENING
                  TO LOWER MODULE


EXPLODED VIEW — CAP REMOVAL
=============================================

             +------------------------+
             |                        |
             |  REPLACEABLE ANTENNA   |
             |          CAP           |
             |                        |
             +------------------------+
                  |              |
                  |  LIFT OFF     |
                  ^              ^
                  |              |
             +----+--------------+----+
             |  LOCATING LIP / LEDGE  |
             |                        |
             |  OPEN CABLE PASSAGE    |
             |                        |
             |       MAIN CASE        |
             |                        |
             |   DISPLAY + UPRIGHT    |
             |   ORANGE PI 5 PLUS     |
             |                        |
             +------------------------+


BOTTOM VIEW — CONCEPTUAL ACCESS
=============================================

             +------------------------+
             |                        |
             |  +------------------+  |
             |  | 40-PIN HEADER    |  |
             |  | ACCESS OPENING   |  |
             |  +------------------+  |
             |                        |
             +------------------------+

The bottom opening provides access to the header.
It does NOT imply the stock header pins point downward.
Confirm the actual mating direction before designing
a lower module, ribbon cable, or right-angle adapter.


MECHANICAL REQUIREMENTS
=============================================

CAP
- One shared hollow cap above the display and board.
- Initial cap envelope: 110 W x 60 H x 30 D mm.
- Initial wall thickness: 2 mm.
- These are prototype dimensions, not final RF requirements.
- Match cap width and depth to the finalized main enclosure.
- Use an overlapping locating lip and reusable screw fastening.
- Prefer rear-access screws; keep the front face clean.
- Keep fasteners and bosses out of the central cap volume.
- Provide a smooth cable passage into the main enclosure.
- Cap must lift clear without pulling attached cables taut.
- Allow cable disconnection before the cap is fully removed.
- Do not permanently glue the cap.
- Do not add antenna layout, pockets, or mounts yet.

MAIN CASE
- Orange Pi 5 Plus stands vertically behind the front display.
- Orient the board with its 40-pin header at the bottom.
- Provide bottom access and mating-connector clearance.
- Keep the lower header area available for a future module.
- Provide a removable rear service panel.
- Support the board using its actual mounting holes.
- Reserve cooling space and ventilation around the heatsink.
- Place port openings from the actual board CAD / measurements.

VERIFY BEFORE FINAL CAD
- Display outline, active area, thickness, and mounting points.
- Orange Pi board orientation, component heights, and port access.
- 40-pin header position, pin direction, and connector envelope.
- Cooling assembly dimensions.
- Cable routing and required service slack.
- Final main-case width and depth.

All diagrams are conceptual and not to scale.
```

---

## Added in the follow-up conversation

These came in alongside the brief and are part of the same ask:

- **Style reference:** the
  [Lilygo T-Beam SUPREME TS1 case by Alley Cat](https://www.printables.com/model/705817-lilygo-t-beam-supreme-ts1-case-by-alley-cat)
  — specifically its **curved features, the slots for a strap, and the
  textured surface lines.**
- **Board mechanical files:**
  [Google Drive](https://drive.google.com/file/d/1rW0tlabPHQ-_rhFcBBpHRGK9TQmT1JEP/view)
- **Start with the main case**, with a **removable lid on the edge opposite
  the 40-pin header**, which is **later replaced by the antenna cap.**
- **Make room for** the Orange Pi 5 Plus aluminium heatsink at
  **50 × 46 × 12.6 mm** and a **Noctua NF-A4x10 5V** fan, 3-pin, ~$16 USD.
- **A charging module box comes later** and mounts on the **back** — that is
  [Enclosure B](../docs/03-enclosure-b-lower.md) in the main repo.
- A board **with the Wi-Fi cards installed is physically on hand**, so
  installed dimensions can be measured on request rather than guessed.
