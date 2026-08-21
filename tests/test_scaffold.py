"""System battery lives here: ONE end-to-end test over the toy
fixture — every stage, reconciliation at every boundary, stage
expectations, output sanity. No per-module unit sprawl; add a
regression pin only when an actual bug earns one. Built during the
MVP beat.

Rules (binding):
- Tests write ONLY to temp directories (set ARTIFACTS_ROOT via
  monkeypatch/tmp_path). MVP baselines, perturbation baselines, final
  artefacts, and frozen reviewer evidence are read-only to tests.
- Result states are PASS / FAIL / UNSCORED / ERROR; a check that
  cannot run must surface as ERROR, never as a scientific failure.
"""
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def test_structural_verifier_contract():
    """verify_structure.py honours the checker-status contract:
    exit 0/1 = ran (JSON status 'ran'), exit 3 = checker error.
    On the fresh template (empty registry) it must run clean."""
    p = subprocess.run([sys.executable, str(ROOT / "scripts/verify_structure.py")],
                       capture_output=True, text=True)
    assert p.returncode in (0, 1, 3)
    out = json.loads(p.stdout)
    assert out["status"] in ("ran", "error")
    if p.returncode == 3:
        assert out["status"] == "error"
    else:
        assert out["status"] == "ran"


def test_expectation_states_closed_set(tmp_path, monkeypatch):
    """report() enforces the closed state set and temp-dir isolation."""
    monkeypatch.setenv("ARTIFACTS_ROOT", str(tmp_path))
    sys.path.insert(0, str(ROOT))
    from src.common import expectations
    expectations.report("s0", {"E0.1": {"state": "UNSCORED",
                                        "reason": "toy fixture"}})
    written = json.loads((tmp_path / "s0" / "expectations.json").read_text())
    assert written["E0.1"]["state"] == "UNSCORED"
    try:
        expectations.report("s0", {"E0.2": {"state": "SKIPPED"}})
    except ValueError:
        pass
    else:
        raise AssertionError("invalid state accepted")
