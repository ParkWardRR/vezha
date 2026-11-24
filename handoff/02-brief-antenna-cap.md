# 02 · Brief — Replaceable Antenna Cap

> [!NOTE]
> **Source document, reproduced verbatim.** Follow-up to
> [01 · Upright case](01-brief-upright-case.md), covering the cap only.
> Kept unedited as a stable reference. Where
> [the plan](README.md) differs, it says so and explains why.

**Design decision recorded alongside it:** use a lift-off cap with a locating
skirt and **two rear-access M3 screws**. Put the heat-set inserts in
reinforced pockets in the **main case**, just below the cap seam — *not* up in
the antenna compartment. That keeps the fastening discreet, installation
accessible, and the cap inexpensive to replace.

---

```text
FOLLOW-UP DESIGN BRIEF — REPLACEABLE ANTENNA CAP
For upright Orange Pi 5 Plus handheld enclosure
All dimensions in mm. Diagrams conceptual, not to scale.

DESIGN INTENT
------------------------------------------------------------
Create a removable, hollow plastic antenna cap above the
display and upright Orange Pi.

The cap must be replaceable without removing the display,
Orange Pi, or main rear service panel.

Use a locating skirt to position the cap and two rear-access
machine screws to retain it. Use heat-set threaded inserts,
not screws threaded directly into printed plastic.

Do not finalize antenna positions or add permanent antenna
pockets in this revision.


INITIAL ENVELOPE
------------------------------------------------------------
External cap:       110 W x 60 H x 30 D
Nominal wall:       2
Approx. interior:   106 W x 56 H x 26 D before local features

These are prototype dimensions, NOT verified RF dimensions.
Match the final width/depth to the main enclosure.

Keep the overlapping skirt and fastening hardware BELOW the
clear antenna chamber as far as practical. Do not silently
consume the quoted clear space with mounting hardware.

Use a hollow, open-bottom cap with a closed top.
Keep the interior front and rear walls flat and unobstructed.


RECOMMENDED FASTENING — TWO REAR-ACCESS M3 SCREWS
------------------------------------------------------------
Put two short downward mounting ears on the REAR of the cap,
one near each side.

Each cap ear overlaps a recessed receiving area in the main
case, BELOW the cap seam.

Each screw enters from the rear, passes through a clearance
hole in its cap ear, and threads into a heat-set insert in
the MAIN CASE.

The cap ears should sit flush with the surrounding rear
surface when assembled.

Use recessed socket/button-head screws with suitable flat
bearing surfaces. Avoid countersunk wedges in thin cap ears.

After removing both screws, the cap lifts straight upward.


REAR VIEW — FASTENER LOCATIONS
------------------------------------------------------------

        +--------------------------------------+
        |                                      |
        |         HOLLOW ANTENNA CAP           |
        |                                      |
        |                                      |
        +======================================+ <- Cap seam
        | [ o ]                          [ o ] |
        | CAP EAR                        CAP EAR|
        |                                      |
        |              MAIN CASE               |
        |                                      |
        +--------------------------------------+

        o = rear-access screw
        Inserts are in the main case behind the ears.
        Ears extend below the seam, not into antenna space.


SIDE SECTION — ONE FASTENER
------------------------------------------------------------

    REAR / TOOL ACCESS                    INSIDE
             |                               |
             v                               v

        Cap rear wall
             |
             |        Hollow antenna chamber
             |
    =========+===============================  Cap seam
             |
          +--+--+     +-------------------+
 screw -> | EAR |---->| HEAT-SET INSERT   |
          +-----+     | IN MAIN-CASE BOSS |
                      +-------------------+
                            |
                      Main-case structure

    Screw axis is front-to-back.
    Insert bore faces rearward.
    Ear is part of the removable cap.
    Boss and insert remain with the main case.

    Diagram is schematic: provide a recessed rear pocket
    so the ear and screw head do not protrude unnecessarily.


CLEVER BUT EASY INSERT PLACEMENT
------------------------------------------------------------
Locate inserts in two reinforced rear shoulder pockets
immediately below the cap seam, near the left/right sides.

Benefits:
- No screws visible from the front.
- No screwdriver access needed through the antenna chamber.
- No tall metal-containing posts beside the antenna strips.
- Cap can be replaced without moving the threaded inserts.
- Soldering iron approaches each insert straight from rear.

Make each insert bore directly accessible while the main
case is bare. Do not hide it under an overhang, inside a
narrow tunnel, or behind a permanently installed component.

Keep enough space around the bore for the actual heat-set
installation tip and tool body.

Install inserts before fitting electronics or antennas.

Support each boss with a fillet and/or short gussets into
the main-case structure. Do not attach a boss only to a thin,
unsupported cosmetic wall.

Keep boss reinforcement clear of the separate rear service
panel and its removal path.


INSERT AND SCREW SPECIFICATION
------------------------------------------------------------
Preferred thread: M3.

Select the EXACT insert SKU before finalizing:
- Installation bore diameter.
- Bore depth.
- Boss outside dimensions.
- Entry geometry.
- Required surrounding plastic.

Do not size an insert bore from "M3" alone.

Use the insert supplier's drawing. Print a small test coupon
in the final material and orientation before the whole case.

Starting screw clearance hole: approximately 3.4 mm;
verify against printer accuracy and selected hardware.

Choose screw length from the actual assembled stack:
ear thickness + clearance + intended thread engagement.

The screw must not bottom out or protrude toward electronics.

Include a positive locating shoulder/hard stop so tightening
does not distort the cap or crush an unsupported thin wall.


LOCATING SKIRT AND SEAM
------------------------------------------------------------
Add an approximately 4-5 mm deep locating skirt extending
downward from the cap into the main-case opening.

The skirt locates the cap; the screws retain it.
Do not rely on screw shanks alone to align the cap.

Use an initial sliding clearance of approximately
0.25-0.35 mm PER MATING SIDE for an FDM prototype.

These are starting tolerances, not guaranteed fits.
Print a small skirt/receiver coupon first.

Add lead-in edges so the cap seats without snagging.

Provide a positive seating ledge for a consistent seam.

Interrupt the skirt wherever necessary for cable passage.
Do not create a cable pinch point at the joint.

Do not use a full-width rigid divider immediately beneath
the cap if it blocks access or traps antenna cables.


ANTENNA ACCOMMODATION — NO FIXED LAYOUT YET
------------------------------------------------------------
Planned antennas:
4 x Taoglas FXP830.24.0100B adhesive flex antennas.

Each strip footprint:
42 x 7.

Provide smooth mounting surfaces rather than deep recesses.
Do not specify a recess depth until the actual antenna
assembly and adhesive thickness have been checked.

Reserve front/rear wall space for later placement trials.
Do not put ribs, screw bosses, embossed labels, or cable
clips through those potential mounting areas.

Use plain, non-conductive plastic in the antenna chamber.
No metal plate, foil liner, conductive coating, or metal
decorative trim in this area.

Do not assume a universal metal-clearance dimension.
Final placement and hardware proximity require RF testing.


CABLE PASSAGE AND SERVICE ACCESS
------------------------------------------------------------
Provide a generous, radiused passage between cap and body.

Size the opening for the actual cable connectors and the
number of cables, not merely the thin coax diameters.

Provide accessible strain-relief features BELOW the seam.
Do not clamp or sharply bend the micro-coax.

Provide a temporary service position:
the cap can be loosened and tilted/lifted enough to access
cables without putting tension on card connectors.

The specified antennas have 100 mm leads. Confirm the complete
routing path before finalizing the cap and card positions.

Do not assume those leads permit fully separating the cap
while everything remains connected.

Antenna cables are disconnected manually before exchanging
the complete cap. No blind-mate connector system is requested.


PRINTING AND VALIDATION
------------------------------------------------------------
Use a plain thermoplastic compatible with heat-set inserts.
Confirm material choice against actual case temperature.

No waterproof or RF-performance claim is requested.

Before final CAD release, verify:
- Skirt fit using a small printed coupon.
- Insert installation using the selected hardware.
- Straight soldering-iron access to both insert bores.
- Screwdriver access with the unit fully assembled.
- Cap removal without removing the rear service panel.
- No cable pinching or tension during removal.
- No collision with display frame, heatsink, board, or ports.
- Antenna performance with the final cap and hardware fitted.

DELIVERABLES
------------------------------------------------------------
Editable parametric CAD plus separate printable files for:
- Main enclosure with receiving shoulders and insert bosses.
- Removable antenna cap with locating skirt and mounting ears.
- Skirt-fit test coupon.
- Heat-set insert test coupon.
```

---

## Provenance of the above

The cap geometry, the two-screw arrangement and the starting tolerances are a
**proposed mechanical design**, not a validated one. For the inserts, the
genuinely load-bearing requirements are narrower and well established: follow
the selected insert's own drawing, provide adequate supporting plastic, and
leave straight installation-tool access. See
[Prusa's heat-set insert guidance](https://www.prusa3d.com/product/heat-set-inserts-m3-standard-100-pcs/).
