# Two Recent Harness Changes

## 1. A change must apply everywhere it appears

### Problem

The same ruling or result can appear in several places: scoring, reports, scorecards, comments, gate snapshots, etc.

We have repeatedly seen a change applied correctly in one place while stale contradictory wording survives elsewhere.

Example from ASASSN-21qj:

- R-9 changed the scored interpretation of E3.4a to FAIL.
- The scoring reflected that.
- Several shipped artefacts still said E3.4a passed and that R-9 was open.

### Change

Use one current source for each mutable ruling/result and make every presentation of it reflect that source.

A ruling/result change should update everywhere it is presented.

### Important constraint

A presentation-only change must **not** trigger a rerun of the scientific replication.

Scientific outputs remain frozen unless the ruling actually changes:

- data;
- methodology;
- parameters;
- or another scientific input.

If only the status, verdict, or wording changes, update the dependent presentation only.

### Practical rule

> **A change is not complete until every place that presents that ruling/result agrees with the current state. Do not rerun scientific stages unless the change alters scientific inputs or methodology.**

---

## 2. Verification must be proportional to the change

### Problem

Late in the run, tiny changes were taking several minutes because the agent was coupling small edits to heavyweight rebuilds and verification.

A stale comment, ruling-status correction, or report sentence should not require a full pipeline rerun.

### Change

Run only the smallest verification needed for the change that was made.

Examples:

- **Comment/prose/status change** — update the relevant presentation and run a light consistency check.
- **Report-generator change** — rerun that generator and its relevant tests.
- **Single scientific-stage change** — rerun that stage and downstream dependent stages only.
- **Structural/scientific change** — run the broader battery as needed.
- **Gate closure** — full verification is appropriate here.

### Practical rule

> **Verification must be proportional to the change. Do not run the full pipeline or full battery after documentation, comment, ruling-status, or presentation-only edits. Reserve full rebuilds for scientific/structural changes and gate closure.**
