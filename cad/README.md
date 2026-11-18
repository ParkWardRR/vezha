# CAD — programmatic enclosures and board interchange

Code-defined geometry for [Enclosure A](../docs/02-enclosure-a-upper.md) and
[Enclosure B](../docs/03-enclosure-b-lower.md), plus the STEP path that joins
the power board to the box it has to fit inside.

> [!WARNING]
> **These are skeletons, not designs.** They build, export and pass a mesh
> check, but `python cad/params.py` reports **31 of 50 dimensions unverified**.
> Nothing here is ready to print or order.

## Why code-CAD for this project specifically

Every enclosure document opens with a warning that its numbers are published
part figures, not installed measurements — the underside M.2 stack, the RotoPD
Pro outline, the mated USB-C plug and its bend radius. A GUI model hides that;
a parameter file makes it the first thing you see, and a git diff shows exactly
what moved when a real measurement lands.

`params.py` exists to make that mechanical:

- Every dimension carries its **source** (which doc line it came from) and a
  **verified** flag.
- Arithmetic propagates the flag. A derived envelope is verified only if every
  input is — so `A outer` reports `TBD` until the adapter stack is measured.
- `build.py --strict` exits non-zero while any dimension is a guess. That is
  the CI gate for "these numbers are now real".

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
| `enclosure_a.py` | Upper router box. Models the underside stack, SBC headroom and antenna strips as explicit keep-out solids. |
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

Two switches exist because the docs disagree with themselves. Neither is
resolved here, because resolving it is a design decision, not a CAD one.

- **`B.HAS_PANEL`** — [01](../docs/01-architecture.md) asserts Enclosure B
  "carries the only panel" and treats the OLED + encoder as settled by the v1
  scope cut. [06's "What is still open"](../docs/06-power-board-schematic.md)
  still lists *"Whether Enclosure B has a front panel at all — decides whether
  J4 and J5 exist."* Both cannot be true. The flag changes box height and
  whether the lid has openings.
- **`B.PICO_MOUNT`** — castellated or socketed, 11 mm apart in Z.
  [03](../docs/03-enclosure-b-lower.md) says "pick one, it changes the
  height"; 06 still lists it open.

## What sets Enclosure B's height today

Folding 06's verified numbers in produced a result worth stating: the tallest
thing above the board is **not** the encoder. It is the RotoPD Pro's **2-position
5 mm screw terminal** at ~22 mm total, which 06 flags as *"an assembly and
enclosure constraint, not just a schematic one"*. Removing it and soldering to
its pads is an open decision that is currently worth about 10 mm of box height.

## Next

1. **Decide the screw terminal** — keep or remove. Costs nothing to decide,
   worth ~10 mm, and 06 says decide it *before* drawing the carrier.
2. **Draw the power board in KiCad.** 06 is detailed enough to lay out — ref
   designators, verified module pinouts, nets, Pico pin map, six passing sim
   decks. Then `kicad-cli pcb export step` and delete the placeholder block in
   `enclosure_b.py`. This is the only major step that needs no new measurement.
3. **Measure the three dimensions nobody should guess** and flip them to
   `verified=True`. This gates everything dimensional, and item 2 does not
   depend on it.
4. **Decide how Enclosure A opens for service** — the geometry here assumes a
   tray + lid, which is the open question in
   [02](../docs/02-enclosure-a-upper.md#open-questions), not a decision.
