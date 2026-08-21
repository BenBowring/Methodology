#!/usr/bin/env bash
# Beat runner: ./scripts/run_beat.sh INTAKE|MVP|FULL|RECOVERY|FINAL [max_iters]
#
# The artefacts are the project, not the session: every iteration is a
# fresh context that resumes from milestones/beat-state.md and the
# ledgers. Halts on any open ruling (STATUS: OPEN in RULINGS.md).
#
# HARD MVP BLOCK: FULL, RECOVERY and FINAL refuse to start unless
# milestones/reviews/MVP-gate-state.json exists, is closed, and holds
# three PROCEED verdicts. RECOVERY and FINAL additionally require the
# blind freeze (git tag blind-freeze). Enforced here, mechanically —
# not by agent discipline.
set -euo pipefail
cd "$(dirname "$0")/.."
BEAT="${1:?usage: run_beat.sh INTAKE|MVP|FULL|RECOVERY|FINAL [max_iters]}"
CAP="${2:-6}"
GATE="milestones/reviews/MVP-gate-state.json"

PY=""
for c in .venv/bin/python venv/bin/python "$(command -v python3 || true)"; do
  [ -n "$c" ] && [ -x "$c" ] && PY="$c" && break
done

open_ruling() {
  grep -q "^STATUS: OPEN" ledgers/RULINGS.md 2>/dev/null
}

mvp_gate_closed() {
  [ -f "$GATE" ] || return 1
  [ -n "$PY" ] || { echo "CHECKER-ERROR: no python to read $GATE" >&2; return 1; }
  "$PY" - "$GATE" << 'PYCHK'
import json, sys
g = json.load(open(sys.argv[1]))
ok = (g.get("closed") is True
      and g.get("blocking_open", 1) == 0
      and len(g.get("verdicts", {})) == 3
      and all(v == "PROCEED" for v in g.get("verdicts", {}).values()))
sys.exit(0 if ok else 1)
PYCHK
}

case "$BEAT" in
  FULL|RECOVERY|FINAL)
    if ! mvp_gate_closed; then
      echo ">>> HARD BLOCK: MVP gate not cleared ($GATE missing, open, or not 3x PROCEED)."
      echo ">>> Full-scale work cannot start. Run the MVP beat to completion first."
      exit 1
    fi ;;
esac
# The gate-state file asserts closure; the battery re-establishes it
# executably at the FULL boundary (toy-scale, cheap here). A gate-state
# written over a broken or failing battery does not open the gate.
if [ "$BEAT" = "FULL" ]; then
  if ! scripts/gate_battery.sh --gate; then
    echo ">>> HARD BLOCK: gate battery does not pass in --gate mode."
    echo ">>> The MVP gate-state is not backed by runnable, passing checkers."
    exit 1
  fi
fi
case "$BEAT" in
  RECOVERY|FINAL)
    if ! git tag --list blind-freeze | grep -q .; then
      echo ">>> HARD BLOCK: blind results not frozen (git tag blind-freeze absent)."
      echo ">>> Complete and freeze the FULL blind beat first."
      exit 1
    fi ;;
esac

echo "BEAT $BEAT start $(date -u +%FT%TZ)" >> timing.log
for i in $(seq 1 "$CAP"); do
  echo "=== $BEAT attempt $i/$CAP ==="
  echo "ITER $BEAT $i start $(date -u +%FT%TZ)" >> timing.log
  claude -p "Advance the $BEAT beat per the replication-milestone skill. \
Start from milestones/beat-state.md and the ledgers — do not rebuild \
context you can read from artefacts. If any block in ledgers/RULINGS.md \
has STATUS: OPEN, stop immediately and say so." \
    --permission-mode acceptEdits || true
  echo "ITER $BEAT $i end $(date -u +%FT%TZ)" >> timing.log

  if open_ruling; then
    echo ">>> Halted: ruling request open. Review ledgers/RULINGS.md."
    echo "BEAT $BEAT halt-ruling $(date -u +%FT%TZ)" >> timing.log
    exit 0
  fi
  done_marker=""
  case "$BEAT" in
    INTAKE)   grep -q "RULING: GREEN" ledgers/RULINGS.md 2>/dev/null && done_marker=y ;;
    MVP)      mvp_gate_closed && done_marker=y ;;
    FULL)     git tag --list blind-freeze | grep -q . && done_marker=y ;;
    RECOVERY) grep -q "^NEXT: FINAL" milestones/beat-state.md 2>/dev/null && done_marker=y ;;
    FINAL)    :  ;; # FINAL always ends in an open R-block (caught above)
  esac
  if [ -n "$done_marker" ]; then
    echo ">>> Beat $BEAT complete."
    echo "BEAT $BEAT end $(date -u +%FT%TZ)" >> timing.log
    exit 0
  fi
done
echo ">>> Iteration cap hit before beat completion. Inspect milestones/beat-state.md."
echo "BEAT $BEAT cap-hit $(date -u +%FT%TZ)" >> timing.log
exit 1
