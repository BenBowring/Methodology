# FINAL-GATE — criteria written by intake, committed before full-scale
# runs. DRAFT shell:
#
# The claim: quoted verbatim from ACCEPTABILITY.md.
#
# Sequence: FULL-SCALE BLIND -> blind freeze -> PARITY RECOVERY (failed
# load-bearing claims only) -> frozen candidate -> review ->
# ADJUDICATION -> human approval.
#
# - BLIND FREEZE: per-claim blind results frozen (value, score, code
#   version, parameters, evidence, diagnosis); git tag blind-freeze.
#   run_beat.sh refuses RECOVERY/FINAL without it. The blind value is
#   never overwritten or retroactively improved.
# - PARITY REPORT vs EVERY load-bearing FACT row (none skipped; a row
#   whose evidence cannot be obtained states the reason plainly), with
#   BLIND and RECOVERED results side by side where recovery ran, the
#   recovered choices and their evidence basis recorded as facts, and
#   per-claim recovery end states (RECOVERED / SUBSTANTIVE-DIVERGENCE /
#   NON-IDENTIFIABLE / UNRECOVERABLE / OUT-OF-SCOPE). Top-level: blind
#   parity rate, recovered parity rate, unresolved rate. Sensitivity
#   ranges where ACCEPTABILITY requires them. Generated from the scored
#   results, not hand-written.
# - DIVERGENCES ledger complete: every entry classified, attributed,
#   localized to a stage or PERMANENT-OPEN with its evidence.
# - Initial vs final bands shown for every pillar.
# - REVIEW: three perspectives in PARALLEL isolation on their evidence
#   pack slices (full scientific review). One bundled pass each
#   (BLOCKING/NON-BLOCKING), one remediation batch, one delta closure
#   pass; third pass only for a remediation-introduced blocker.
#   Unresolvable material blocker -> gate ends UNRESOLVED (R-block).
# - ADJUDICATION (read-only): assembles the per-claim outcome table,
#   rates, verdicts with dissents verbatim, carried non-blocking
#   findings, bands, spend vs COST-PROFILE -> the replication report.
#   It never investigates, changes methodology, or launches recovery.
# - Deliverable: the standalone replication report + approval R-block.
#
# Gate behaviour: ALWAYS STOPS. Human rules.
(written by intake)
