#!/usr/bin/env python3
"""Structural verifier: checks the implementation against REGISTRY.json,
the frozen structural declaration. Prose may describe structural state;
only executable inspection establishes it.

Checks:
  registry   — parses; unique stage ids; unique expectation ids; deps
               reference known stages; dependency graph is acyclic
  artifacts  — every declared artefact exists on disk (declared =
               shipped/load-bearing only; nothing else is checked)
  expect-ids — bidirectional reconciliation between registered
               expectation IDs and IDs actually emitted in
               artifacts/<stage>/expectations.json: missing,
               unregistered, wrong-owner, invalid state all FAIL.
               Exact-match IDs only (E4.4 and E4.4a are distinct).
  reads      — stage modules must not reference another stage's
               artifacts/ path unless that stage is a declared dep

Exit codes (checker status is machine-readable, per the state rules):
  0 — ran; no FAILs (PASS/UNSCORED only)
  1 — ran; at least one FAIL
  3 — checker itself could not run (ERROR): draw NO scientific or
      structural conclusion from this case
Output: one JSON object on stdout: {"status": "ran"|"error",
"checks": {name: {"state": ..., "detail": [...]}}}.
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
STATES = {"PASS", "FAIL", "UNSCORED", "ERROR"}


def check_registry(reg):
    detail = []
    stages = reg.get("stages")
    if not isinstance(stages, list):
        return {"state": "FAIL", "detail": ["'stages' is not a list"]}
    if not stages:
        return {"state": "UNSCORED",
                "detail": ["registry empty (pre-intake): nothing declared"]}
    ids = [s.get("id") for s in stages]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        detail.append(f"duplicate stage ids: {sorted(dup)}")
    eids = [e for s in stages for e in s.get("expectations", [])]
    edup = {e for e in eids if eids.count(e) > 1}
    if edup:
        detail.append(f"duplicate expectation ids: {sorted(edup)}")
    known = set(ids)
    for s in stages:
        bad = [d for d in s.get("deps", []) if d not in known]
        if bad:
            detail.append(f"{s.get('id')}: unknown deps {bad}")
    # cycle check (Kahn)
    deps = {s["id"]: set(s.get("deps", [])) & known for s in stages}
    order, ready = [], [i for i, d in deps.items() if not d]
    while ready:
        n = ready.pop()
        order.append(n)
        for i, d in deps.items():
            d.discard(n)
            if i not in order and i not in ready and not d:
                ready.append(i)
    if len(order) < len(deps):
        detail.append(f"dependency cycle among: "
                      f"{sorted(set(deps) - set(order))}")
    return {"state": "FAIL" if detail else "PASS", "detail": detail}


def check_artifacts(reg):
    stages = reg.get("stages", [])
    declared = [(s["id"], a) for s in stages for a in s.get("artifacts", [])]
    if not declared:
        return {"state": "UNSCORED", "detail": ["no artefacts declared"]}
    missing = [f"{sid}: {a}" for sid, a in declared
               if not (ROOT / a).exists()]
    return {"state": "FAIL" if missing else "PASS",
            "detail": [f"declared but not produced: {m}" for m in missing]}


def check_expectation_ids(reg):
    stages = reg.get("stages", [])
    registered = {e: s["id"] for s in stages
                  for e in s.get("expectations", [])}
    if not registered:
        return {"state": "UNSCORED", "detail": ["no expectations registered"]}
    detail, emitted_any = [], False
    for s in stages:
        p = ROOT / "artifacts" / s["id"] / "expectations.json"
        if not p.exists():
            continue
        emitted_any = True
        try:
            emitted = json.loads(p.read_text())
        except (json.JSONDecodeError, OSError) as e:
            detail.append(f"{s['id']}: unreadable expectations.json ({e})")
            continue
        for eid, r in emitted.items():
            if eid not in registered:
                detail.append(f"{s['id']}: emits unregistered id {eid}")
            elif registered[eid] != s["id"]:
                detail.append(f"{s['id']}: emits {eid} owned by "
                              f"{registered[eid]} (wrong owner)")
            if not (isinstance(r, dict) and r.get("state") in STATES):
                detail.append(f"{s['id']}: {eid} has invalid state "
                              f"{r.get('state') if isinstance(r, dict) else r!r}")
        missing = [e for e, owner in registered.items()
                   if owner == s["id"] and e not in emitted]
        if missing:
            detail.append(f"{s['id']}: registered but not emitted: {missing}")
    if not emitted_any:
        return {"state": "UNSCORED",
                "detail": ["no stage has emitted expectations yet"]}
    return {"state": "FAIL" if detail else "PASS", "detail": detail}


def check_reads(reg):
    stages = reg.get("stages", [])
    with_modules = [s for s in stages if s.get("module")]
    if not with_modules:
        return {"state": "UNSCORED", "detail": ["no stage modules declared"]}
    detail = []
    ids = {s["id"] for s in stages}
    for s in with_modules:
        mp = ROOT / s["module"]
        if not mp.exists():
            detail.append(f"{s['id']}: declared module missing: {s['module']}")
            continue
        src = mp.read_text()
        allowed = set(s.get("deps", [])) | {s["id"]}
        for ref in set(re.findall(r"artifacts/([A-Za-z0-9_\-]+)/", src)):
            if ref in ids and ref not in allowed:
                detail.append(f"{s['id']}: reads artifacts/{ref}/ "
                              f"without declaring dep on {ref}")
    return {"state": "FAIL" if detail else "PASS", "detail": detail}


def main():
    try:
        reg = json.loads((ROOT / "REGISTRY.json").read_text())
    except (OSError, json.JSONDecodeError) as e:
        print(json.dumps({"status": "error",
                          "error": f"cannot load REGISTRY.json: {e}"}))
        return 3
    checks = {"registry": check_registry(reg)}
    if checks["registry"]["state"] == "FAIL":
        print(json.dumps({"status": "ran", "checks": checks}, indent=1))
        return 1
    checks["artifacts"] = check_artifacts(reg)
    checks["expect-ids"] = check_expectation_ids(reg)
    checks["reads"] = check_reads(reg)
    print(json.dumps({"status": "ran", "checks": checks}, indent=1))
    return 1 if any(c["state"] == "FAIL" for c in checks.values()) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # checker crash is ERROR, never a finding
        print(json.dumps({"status": "error", "error": repr(e)}))
        sys.exit(3)
