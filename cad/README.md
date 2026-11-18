# CAD — programmatic enclosures and board interchange

Code-defined geometry for [Enclosure A](../docs/02-enclosure-a-upper.md) and
[Enclosure B](../docs/03-enclosure-b-lower.md), plus the STEP path that joins
the power board to the box it has to fit inside.

> [!WARNING]
> **These are skeletons, not designs.** They build, export and pass a mesh
> check. `python cad/params.py` reports **0 open dimensions and 21 assumptions**
> — the model is closed and proceeds on stated assumptions, it is not proven.
> Nothing here is ready to print or order until docs/10 retires those 21.

## Why code-CAD for this project specifically

Every enclosure document opens with a warning that its numbers are published
part figures, not installed measurements — the underside M.2 stack, the RotoPD
Pro outline, the mated USB-C plug and its bend radius. A GUI model hides that;
a parameter file makes it the first thing you see, and a git diff shows exactly
what moved when a real measurement lands.

`params.py` exists to make that mechanical:

- Every dimension carries its **source** and one of three states: `ok`
  (vendor drawing, published spec, standard, or a settled decision of ours),
  `ASSUME` (a deliberate assumption with a stated basis), or `OPEN` (no basis
  at all).
- Arithmetic propagates both, so a derived value is only as solid as its
  weakest input: assumed + verified = assumed.
- `build.py --strict` fails on `OPEN` only. It passes today because there are
  none left; `validate_later()` is the punch list of the 21 assumptions, and
  [docs/10](../docs/10-measurement-protocol.md) is how they get retired.

## Why build123d and not OpenSCAD

build123d sits on OpenCASCADE, so it **imports STEP**. OpenSCAD cannot. That
single fact decides it:

```
kicad-cli pcb export step --subst-models -o cad/build/power-board.step power-board.kicad_pcb
   → enclosure_b.py imports the real solid, not a retyped rectangle
   → boolean against the tray interior = a clash check, not an argument
```

The board outline is never typed in twice. OpenSCAD is installed for throwaway
sketches only.

## Layout

| File | Role |
|---|---|
| `params.py` | Every dimension, its source, and whether anyone has measured it. Run it standalone for the provenance table. |
| `lib.py` | Tray/lid/standoff helpers and the STEP+STL+PNG export pipeline. |
| `enclosure_a.py` | Upper router box: a perimeter band plus a base plate and a replaceable top cap. Models the underside stack, SBC headroom and antenna strips as explicit keep-out solids. |
| `enclosure_b.py` | Lower power box. Imports `build/power-board.step` when KiCad has written it, else a flagged placeholder. |
| `build.py` | Builds both, renders, runs `admesh`, prints what is still a guess. |

## Running

```sh
cad/.venv/bin/python cad/params.py        # provenance table only
cad/.venv/bin/python cad/build.py         # STEP + STL + PNG into cad/build/
cad/.venv/bin/python cad/build.py --strict  # fails today, by design
```

`cad/build/` and `cad/.venv/` are gitignored. Geometry is regenerated, not
committed.

## Toolchain

Installed and verified on this machine:

| Tool | Version | Role |
|---|---|---|
| build123d | 0.13.0 | parametric solids, STEP in/out (venv: `cad/.venv`) |
| KiCad / `kicad-cli` | 10.0.6 | schematic, layout, **STEP export** |
| FreeCAD | 1.1.4 | GUI inspection of STEP, `freecadcmd` headless |
| f3d | 4.0.1 | headless PNG renders |
| admesh | 0.98.5 | manifold / edge checks on exported STL |
| OrcaSlicer | 2.5.1 | printability, wall thickness, overhangs |
| OpenSCAD | 2026.10.11 | sketches only — no STEP, dead end for the fit loop |

The STEP round-trip is verified end to end: build123d writes
`enclosure-a-tray.step`, and FreeCAD's headless interpreter reads it back as a
single valid solid (48 670 mm³). The two kernels agree, which is what makes the
KiCad fit check trustworthy.

### Paths worth knowing

**`freecadcmd` is not on `PATH`.** The cask links only the GUI. The headless
interpreter — and a useful set of bundled binaries — live here:

```sh
/Applications/FreeCAD.app/Contents/Resources/bin/freecadcmd  script.py
```

That directory also ships **`ccx` (CalculiX)** and **`gmsh`**, neither of which
is in brew core as a formula. If a drop test or a thermal study on Enclosure A
ever becomes worth doing — [02 calls thermal "unresolved and
untested"](../docs/02-enclosure-a-upper.md#thermal) — the solver is already
installed, no extra dependency.

**The `openscad` cask is disabled**, as of 2026-09-01: *"does not pass the
macOS Gatekeeper check"*. Use `openscad@snapshot`, which links
`/opt/homebrew/bin/openscad` normally and renders headless
(`openscad -o out.stl in.scad`).
| atopile | 0.12.6 | code-defined schematic (venv) — not yet adopted |
| SKiDL | 3.0.0 | Python → KiCad netlist (venv) — not yet adopted |

### Two things that will bite

**`pcbnew` is not importable from the venv.** It ships only inside KiCad's
bundled Python **3.9** at
`/Applications/KiCad/KiCad.app/Contents/Frameworks/Python.framework/Versions/3.9/bin/python3`,
which cannot share an environment with build123d on 3.13. Use `kicad-cli` for
anything scriptable; treat `pcbnew` work as a separate, older interpreter.

**kibot does not run on macOS here.** It is installed in the venv but imports
`wx` and `pcbnew`, neither of which is present — `kibot --version` raises
`ModuleNotFoundError: No module named 'wx'`. It is designed to run in its own
container. Per the project build rule that belongs on **fucina** in podman,
alongside the existing ngspice container in [`sim/`](../sim/run.sh) — not on
this Mac.

## Open contradictions this model surfaces

One switch remains because the docs disagree with themselves. It is not
resolved here, because resolving it is a product decision, not a CAD one.

- **`B.HAS_PANEL`** — [01](../docs/01-architecture.md) asserts Enclosure B
  "carries the only panel" and treats the OLED + encoder as settled by the v1
  scope cut. [06's "What is still open"](../docs/06-power-board-schematic.md)
  still lists *"Whether Enclosure B has a front panel at all — decides whether
  J4 and J5 exist."* Both cannot be true. The flag changes box height and
  whether the lid has openings. Currently `True`.

Settled since, and recorded in `params.py` with the reasoning:

| Was open | Decided |
|---|---|
| RotoPD screw terminal, keep or remove | **Removed**, wires soldered to the pads |
| How Enclosure A opens for service | **Band + two broad plates**, SBC on the base plate |
| `B.PICO_MOUNT` castellated vs socketed | **Socketed**, and `pcb/` follows it |
| Accessory port config A or B | **A** — 36 k / 22.6 k, 1.06–1.23 A |

## Current envelopes

Both are assumed, not proven — every input is `ok` or `ASSUME`, none `OPEN`.

| | Outer | Driven by |
|---|---|---|
| **Enclosure A** | 114 × 89 × 36.8 mm | Orange Pi footprint; thickness by the underside M.2 stack |
| **Enclosure B** | 100 × 80 × 29.6 mm | The 90 × 70 mm power board; height by the encoder at 20 mm |

Enclosure B grew when the accessory port was added — the board went from
80 × 60 to 90 × 70 to fit U4, L1, U5 and J6.

## Next

1. **Confirm U4's middle four pins** against section 6 of TI's SNVSC40E.
   `pcb/power_board.py` marks VIN, FB, RT and PG as assumed. A wrong VIN pin
   on an 80 V part is a destroyed board, not a rework. This is the single
   most dangerous assumption in the repo.
2. **Confirm U3's Pololu pin order** — 06 says it is not legible at published
   resolution, and EN and PG are adjacent on different rows.
3. **Route the board.** It has 43 nets assigned and 0 substantive DRC
   violations, so it opens in KiCad ready to route.
4. **Retire the 21 assumptions** per
   [docs/10](../docs/10-measurement-protocol.md), starting with the three
   that need real parts in hand.
