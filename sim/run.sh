#!/bin/sh
# Run the PCB 2 ngspice decks and print only the result lines.
#
# Decks tag every line they want shown with a leading "@@" so ngspice's own
# per-analysis chatter ("Reset re-loads circuit", "No. of Data Rows", the
# banner) can be filtered out without also hiding real errors.
#
# Usage (inside the container):   sh /work/run.sh [deck.cir ...]
# Usage (from a dev machine):
#   rsync -az sim/ fucina:~/builds/vezha-sim/sim/
#   ssh fucina 'cd ~/builds/vezha-sim && \
#     podman run --rm -v ./sim:/work:z vezha-sim sh /work/run.sh'

set -e
cd "$(dirname "$0")"

decks="$*"
[ -n "$decks" ] || decks=$(ls [0-9]*.cir | sort)

status=0
for d in $decks; do
  out=$(ngspice -b "$d" 2>&1) || status=1
  # Real failures: ngspice's own error lines. Show them loudly.
  echo "$out" | grep -E '^(Error|Warning|.*PPerror|.*fatal)' >&2 || true
  echo "$out" | sed -n 's/^@@//p'
  echo ""
  case "$out" in
    *Error*) echo "!! $d reported an ngspice Error - results above are suspect" >&2
             status=1 ;;
  esac
done
exit $status
