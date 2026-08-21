#!/usr/bin/env bash
# Cold-start / idempotency evidence: GENERATED, never asserted.
# Runs the pipeline entry point (src/pipeline.py, the single entry)
# twice into two empty temp directories via ARTIFACTS_ROOT and diffs
# every produced output, binaries included. Hand-written cold-start
# claims are not evidence; this script's output is.
#
# Exit: 0 ran + identical, 1 ran + differences (a finding),
#       3 could not run (checker ERROR — draw no conclusion).
set -uo pipefail
cd "$(dirname "$0")/.."

PY=""
for c in .venv/bin/python venv/bin/python "$(command -v python3 || true)"; do
  [ -n "$c" ] && [ -x "$c" ] && PY="$c" && break
done
[ -n "$PY" ] || { echo "COLDSTART-ERROR: no python interpreter" >&2; exit 3; }
[ -f src/pipeline.py ] || {
  echo "COLDSTART-ERROR: src/pipeline.py not present (nothing to check)" >&2
  exit 3
}

A=$(mktemp -d); B=$(mktemp -d)
trap 'rm -rf "$A" "$B"' EXIT
ARTIFACTS_ROOT="$A" "$PY" -m src.pipeline || {
  echo "COLDSTART-ERROR: pipeline failed on run 1" >&2; exit 3; }
ARTIFACTS_ROOT="$B" "$PY" -m src.pipeline || {
  echo "COLDSTART-ERROR: pipeline failed on run 2" >&2; exit 3; }

if diff -r "$A" "$B" > /dev/null 2>&1; then
  echo "COLDSTART: PASS — two empty-dir runs produced identical outputs"
  exit 0
else
  echo "COLDSTART: FAIL — outputs differ between two cold runs:" >&2
  diff -rq "$A" "$B" >&2 || true
  exit 1
fi
