# MVP-GATE — criteria written by intake, committed before build. DRAFT
# shell showing the required shape:
#
# The MVP claim: "a working end-to-end system, modular behind frozen
# artefacts, in which a divergence from literature or expected behaviour
# can be localized to a stage." Parity is NOT scored here.
#
# Required criteria (intake makes them concrete):
# - E2E: full pipeline runs on the toy fixture (src/pipeline.py);
#   battery clean (scripts/gate_battery.sh --gate).
# - STRUCTURE: scripts/verify_structure.py passes — declared artefacts
#   produced, expectation IDs reconciled with REGISTRY.json, no
#   undeclared cross-stage reads.
# - EXPECTATIONS: every stage reports vs its registered expectations
#   via src/common/expectations.py (states PASS/FAIL/UNSCORED/ERROR;
#   UNSCORED carries its reason).
# - COLD START: scripts/cold_start_check.sh passes (generated
#   evidence, not asserted).
# - PERTURBATION-TO-VERDICT: at least one injected fault first appears
#   at the correct stage, propagates along the declared DAG, changes a
#   downstream quantity, and changes a final result/verdict. Further
#   faults only as the intake perturbation plan earned them.
#
# Gate behaviour: STOP-ON-EXCEPTION with a HARD MECHANICAL BLOCK.
# Scorecard generated (scripts/gen_scorecard.py). The three
# perspectives review in PARALLEL isolation — the LIGHT question:
# is the toy system coherent and diagnostically trustworthy enough to
# scale? One bundled pass each (findings BLOCKING/NON-BLOCKING), one
# remediation batch, one delta closure pass; third pass only for a
# remediation-introduced blocker. Clean + three PROCEEDs -> write
# milestones/reviews/MVP-digest.md and
# milestones/reviews/MVP-gate-state.json
#   {"closed": true, "blocking_open": 0,
#    "verdicts": {"red-team": "PROCEED", "domain-expert": "PROCEED",
#                 "practitioner": "PROCEED"}}
# then CONTINUE to FULL (run_beat.sh enforces the block mechanically).
# Otherwise stop with the specific break.
(written by intake)
