#!/usr/bin/env python
"""Build both enclosures: STEP + STL + headless PNG, plus the provenance report.

    cad/.venv/bin/python cad/build.py          # build everything
    cad/.venv/bin/python cad/build.py --strict # fail if any dimension is a guess

--strict is what a CI gate on fucina should run once the measurements land.
Today it fails by design: 31 of 50 dimensions are still unverified.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import enclosure_a  # noqa: E402
import enclosure_b  # noqa: E402
import lib  # noqa: E402
import params  # noqa: E402


def check_stl(path: Path) -> str:
    """admesh sanity check -- manifold, no unconnected edges."""
    if not shutil.which("admesh"):
        return "admesh not installed"
    try:
        r = subprocess.run(["admesh", str(path)], capture_output=True,
                           text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return "admesh timed out"
    bad = []
    for line in r.stdout.splitlines():
        for key in ("Edges fixed", "Backwards edges", "Facets removed",
                    "Facets added", "Facets reversed", "Degenerate facets"):
            if line.strip().startswith(key):
                n = line.rsplit(":", 1)[-1].strip()
                if n not in ("0", ""):
                    bad.append(f"{key}={n}")
    return "clean" if not bad else "ISSUES: " + ", ".join(bad)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero while any dimension is unverified")
    ap.add_argument("--no-render", action="store_true")
    args = ap.parse_args()

    print(params.report())

    results: dict[str, dict[str, Path]] = {}
    for module in (enclosure_a, enclosure_b):
        for name, part in module.build().items():
            results[name] = lib.emit(part, name, render=not args.no_render)

    print("\nBuilt into cad/build/:")
    print(lib.summarise(results))

    print("\nMesh checks:")
    for name, files in results.items():
        if "stl" in files and "keepout" not in name:
            print(f"  {name:<30} {check_stl(files['stl'])}")

    n_open = len(params.unverified())
    n_ass = len(params.validate_later())
    if args.strict and n_open:
        print(f"\nSTRICT: {n_open} dimensions have no basis at all.", file=sys.stderr)
        return 1
    if n_open:
        print(f"\n{n_open} dimensions still open.")
    else:
        print(f"\nNo open dimensions. {n_ass} assumptions to validate "
              f"-- see docs/10-measurement-protocol.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
