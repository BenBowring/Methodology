#!/usr/bin/env python3
"""Scorecard generator: builds the expectation scorecard FROM the
structured evidence (REGISTRY.json + artifacts/*/expectations.json).
Gate digests embed this output; verdict strings and counts must come
from here, never be hand-written. Prose explains a result; it never
independently asserts one.

Counting rules: UNSCORED and ERROR never contribute to pass counts.

Usage: gen_scorecard.py            (markdown to stdout)
Exit: 0 ran, 3 could not run (draw no conclusion from 3)."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def main():
    reg = json.loads((ROOT / "REGISTRY.json").read_text())
    rows, counts = [], {"PASS": 0, "FAIL": 0, "UNSCORED": 0, "ERROR": 0}
    for s in reg.get("stages", []):
        p = ROOT / "artifacts" / s["id"] / "expectations.json"
        emitted = json.loads(p.read_text()) if p.exists() else {}
        for eid in s.get("expectations", []):
            r = emitted.get(eid)
            if r is None:
                state, note = "UNSCORED", "not emitted"
            else:
                state = r.get("state", "ERROR")
                note = str(r.get("value", r.get("reason", "")))
            counts[state] = counts.get(state, 0) + 1
            rows.append(f"| {eid} | {s['id']} | {state} | {note} |")
    print("| expectation | stage | state | value/reason |")
    print("|---|---|---|---|")
    for r in rows:
        print(r)
    scored = counts["PASS"] + counts["FAIL"]
    print(f"\nPASS {counts['PASS']}/{scored} scored · "
          f"FAIL {counts['FAIL']} · UNSCORED {counts['UNSCORED']} · "
          f"ERROR {counts['ERROR']}")
    print("(UNSCORED and ERROR are excluded from pass counts.)")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"SCORECARD-ERROR: could not generate ({e!r})", file=sys.stderr)
        sys.exit(3)
