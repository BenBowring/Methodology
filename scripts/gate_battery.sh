#!/usr/bin/env bash
# Deterministic battery. Exit 2 blocks the calling action (stop /
# commit / gate) with reasons on stderr; exit 0 allows.
#
# State rules honoured throughout: a check that RAN and FAILED blocks;
# a checker that COULD NOT RUN reports CHECKER-ERROR loudly and — in
# ordinary modes — does NOT block: no scientific or structural
# conclusion is drawn from a crashed checker.
# EXCEPTION, --gate mode: gate closure requires every checker
# runnable. A CHECKER-ERROR at gate closure blocks (exit 2) — that is
# an execution-control decision, not a scientific verdict. A clean
# MVP-gate-state cannot be produced while a required checker is down.
#
# Modes:
#   --on-stop     tests + conjecture tripwire + structure   (default)
#   --pre-commit  same as --on-stop
#   --quick       structure + registry only (proportional check for
#                 presentation-only edits)
#   --gate        everything above + cold-start check (gate closure;
#                 checker errors block here)
set -uo pipefail
cd "$(dirname "$0")/.."
MODE="${1:---on-stop}"
FAIL=0
say() { echo "$1" >&2; }
checker_error() {
  say "CHECKER-ERROR: $1"
  if [ "$MODE" = "--gate" ]; then
    say "BLOCKED: gate closure requires every checker runnable."
    FAIL=1
  else
    say "CHECKER-ERROR: not blocking; fix the environment."
  fi
}

# Resolve the project's own environment — never bare python/pytest.
PY=""
for c in .venv/bin/python venv/bin/python "$(command -v python3 || true)"; do
  [ -n "$c" ] && [ -x "$c" ] && PY="$c" && break
done
if [ -z "$PY" ]; then
  checker_error "no python interpreter found (.venv, venv, python3); battery cannot run."
  [ "$FAIL" -eq 1 ] && exit 2
  exit 0
fi

# 1. Structural verification against REGISTRY.json.
"$PY" scripts/verify_structure.py > /dev/null 2>&1
case $? in
  0) : ;;
  1) say "BLOCKED: structural verification failed. Run scripts/verify_structure.py for detail."
     FAIL=1 ;;
  *) checker_error "verify_structure.py could not run." ;;
esac

# 2. Tests must pass (battery is cheap by design; writes to temp only).
if [ "$MODE" != "--quick" ]; then
  if "$PY" -m pytest --version > /dev/null 2>&1; then
    if ! "$PY" -m pytest -q tests/ > /dev/null 2>&1; then
      say "BLOCKED: pytest failing. Fix, or mark xfail with a DIVERGENCES.md entry."
      FAIL=1
    fi
  else
    checker_error "pytest not installed in the resolved environment ($PY); tests NOT run — an environment defect, not a pass."
  fi
fi

# 3. No building on unfilled conjectures: CONFIRMED requires a
#    non-empty RESULT line. Crash here is CHECKER-ERROR, never a finding.
if [ "$MODE" != "--quick" ] && [ -f ledgers/CONJECTURES.md ]; then
  "$PY" - << 'PYCHK'
import re, sys
t = open("ledgers/CONJECTURES.md").read()
bad = 0
for block in re.split(r"\n(?=## CJ-)", t):
    if "STATUS: CONFIRMED" in block and re.search(r"RESULT:\s*(\n|$)", block):
        bad = 1
sys.exit(bad)
PYCHK
  case $? in
    0) : ;;
    1) say "BLOCKED: a conjecture is CONFIRMED with an empty RESULT line. Fill the run result or set it back to OPEN."
       FAIL=1 ;;
    *) checker_error "conjecture tripwire could not run." ;;
  esac
fi

# 4. Gate closure only: cold-start evidence must be generated.
if [ "$MODE" = "--gate" ]; then
  scripts/cold_start_check.sh
  case $? in
    0) : ;;
    1) say "BLOCKED: cold-start check found differing outputs."
       FAIL=1 ;;
    *) checker_error "cold-start check could not run." ;;
  esac
fi

[ "$FAIL" -eq 1 ] && exit 2
exit 0
