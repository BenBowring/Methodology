"""Expectation reporting: the one convention that makes results
mechanical instead of narrated.

Each stage, after running, calls report() with the outcome of every
expectation it owns (IDs pre-registered in REGISTRY.json). Results land
in artifacts/<stage>/expectations.json, which is what the structural
verifier reconciles against the registry and what the scorecard
generator reads. Verdict strings in any report must come from these
files, never be written by hand.

States (closed set — the only structured result vocabulary):
  PASS     — checked and satisfied
  FAIL     — checked and not satisfied
  UNSCORED — not scoreable here; never counts toward passes; must
             carry a reason (e.g. "not scoreable on toy fixture")
  ERROR    — the checker itself could not run; never a scientific FAIL
"""
import json
from .freeze import resolve

STATES = {"PASS", "FAIL", "UNSCORED", "ERROR"}


def report(stage_id: str, results: dict) -> None:
    """results: {expectation_id: {"state": <STATE>, ...}} — extra keys
    (value, expected, reason) are recorded as facts alongside."""
    for eid, r in results.items():
        state = r.get("state")
        if state not in STATES:
            raise ValueError(f"{eid}: state {state!r} not in {sorted(STATES)}")
        if state == "UNSCORED" and not r.get("reason"):
            raise ValueError(f"{eid}: UNSCORED requires a reason")
    p = resolve(f"artifacts/{stage_id}/expectations.json")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(results, indent=1, sort_keys=True))
