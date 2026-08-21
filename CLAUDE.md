# Standing rules — read every session

## Project
Defined per clone by refs/GOAL.md and the artefacts compiled at intake.
Until intake is approved, the only permitted work is intake itself.

## The five phases
1. INTAKE (human-approved): paper + goal -> compiled project layer,
   clarification questions, sign-off. The rigor lives here.
2. MVP (auto-continue if clean): a working end-to-end system at toy
   scale, modular, in which any divergence from expected behaviour can
   be LOCALIZED to a stage before it is theorized about. Parity is not
   the MVP's job; attribution capability is — proven by at least one
   injected perturbation that first appears at the correct stage,
   propagates along the declared DAG, and changes a final
   result/verdict. The gate is a HARD MECHANICAL BLOCK: full-scale
   work cannot start until milestones/reviews/MVP-gate-state.json
   records a clean scorecard, three PROCEED verdicts, and no open
   blocking findings (enforced by scripts/run_beat.sh, not by
   discipline). MVP review is light: trustworthy enough to scale?
3. FULL-SCALE BLIND: the replication built and scored inside the
   intake-compiled blind evidence boundary (default: the paper,
   supplied data, cited literature/methods, and public technical
   documentation needed to use those inputs; author code and author
   implementation material excluded). Blind reconstruction is a
   diagnostic — it measures what can be rebuilt independently.
   Choosing a method BECAUSE it reproduces the target is forbidden
   here. At the end, per-claim results are FROZEN — value, score,
   code version, parameters, evidence used, divergence diagnosis —
   as the BLIND view (git tag blind-freeze), permanent, never
   overwritten or retroactively improved.
4. PARITY RECOVERY (target-aware): only intake-designated
   load-bearing claims (the ACCEPTABILITY pillar claims) that scored
   FAIL / NOT-REPRODUCIBLE enter. Failed supporting rows are never
   auto-promoted, though supporting quantities may be investigated in
   service of a load-bearing claim. Diagnose the shape of the miss;
   generate method hypotheses from it; consult any legitimate,
   verifiable evidence about what the authors actually did — author
   code, supplements, configs/scripts, calibration products, cited
   methods — every consultation logged. Testing a choice because it
   reproduces the published quantity is allowed here; unconstrained
   knob-tuning to minimise error is not. Prefer choices that jointly
   explain multiple outputs; seek independent confirmation. A
   supported recovery is implemented through the real pipeline and
   propagated to all dependent quantities — never patched into a
   headline. Per-claim end states: RECOVERED / SUBSTANTIVE-DIVERGENCE
   / NON-IDENTIFIABLE / UNRECOVERABLE / OUT-OF-SCOPE.
5. FINAL (requires explicit human approval): frozen candidate, full
   three-perspective scientific review, then ADJUDICATION — a
   read-only reporting decision that reads the final implemented
   evidence and decides how each claim is reported; it never
   investigates, changes methodology, launches recovery, or searches
   for better numbers. Deliverable: the replication report + approval
   R-block.

Blind and recovered results are reported separately, always — dual
reporting is permanent, and the two frozen views (BLIND, RECOVERED)
are each independently benchmarkable. Hidden benchmark answers,
tolerances, and solution material are inaccessible in EVERY phase;
benchmark-answer leakage is an evaluation failure, distinct from
accidental author-material exposure (which is handled by a recorded
provenance note, never by restarting).

## Anchor (set at intake, per project)
- The replication target is pinned explicitly at intake:
  (a) a specific paper result/dataset; (b) the paper's broader
  methodology; (c) a general result/phenomenon from the literature;
  (d) a narrower stated objective using the paper as a starting point.
  If GOAL.md is ambiguous, ask directly — never assume.
- The ANCHOR statement (derived from the target) says what is
  authoritative vs comparative, how paper-vs-literature conflicts
  resolve, and the blind evidence boundary (author material's only
  role is in recovery, after the blind freeze).
- Sign-off freezes the intended DIRECTION: GOAL, ACCEPTABILITY (incl.
  the load-bearing claim set), gate criteria, the ANCHOR statement,
  REGISTRY.json, and COST-PROFILE.md. It does not freeze factual
  understanding.
- PAPER-FACTS.md reflects CURRENT understanding: evidence discovered
  during implementation corrects a misread row in place, with a brief
  noted correction (was X — located quote/page). Material corrections
  only. A correction that changes what a band or gate criterion MEANS
  is stop-and-ask; otherwise correct, note, continue.
- Where the anchor is silent: take the refs/LIT-DEFAULTS.md option, log
  one DIVERGENCES.md line. Never invent a claim — if a needed number
  exists nowhere, ask.
- Unavailable author-held material: find the closest defensible
  substitute in the literature, record the divergence with its
  citation (marked SUBSTITUTE), and build from that. A parity row
  whose evidence cannot be obtained says so plainly with the reason —
  never silently approximated.
- Substitution limits (anti-cascade): each pillar carries an
  intake-set SUBSTITUTION LIMIT — the maximum substitutes permitted
  upstream of that pillar's scored result. Exceeding it is
  STOP-AND-ASK. A FATAL divergence marks the pillar COMPROMISED:
  stop building on it, record it, escalate — scored as failed, not
  patched.

## The two rules that prevent compounding (exception-only metadata)
Ordinary grounded work carries NO tags, NO metadata. Write metadata only
at the two exception points:
1. GUESSING: a hypothesis goes in ledgers/CONJECTURES.md (one line + a
   runnable test). Nothing is built on it until its RESULT line is
   filled by an actual run.
2. DEPARTING from the anchor: one line in ledgers/DIVERGENCES.md,
   classified (FAITHFUL / DEFECT / UNDERSPECIFIED / UNCLASSIFIABLE),
   with citation.

## Mechanical trust
- REGISTRY.json is the frozen structural declaration — per stage:
  id, module, deps, shipped/load-bearing artifacts, expectation IDs.
  Nothing else lives there (bands -> ACCEPTABILITY, criteria -> gate
  files, wording -> prose stage map, results -> expectations.json,
  rulings -> RULINGS). scripts/verify_structure.py checks the
  implementation against it. Prose may describe structural state;
  only executable inspection establishes it.
- Load-bearing claims are generated, never asserted: scorecards,
  parity rows, verdict labels, and counts come from structured
  evidence (artifacts/*/expectations.json via
  scripts/gen_scorecard.py and the scored-results artefacts). One
  current source per mutable fact — RULINGS for rulings, the scored
  results for scores — and every presentation regenerates from it.
  Prose explains a result; it never independently asserts one. A
  presentation-only regeneration never reruns scientific stages.
- Result states: PASS / FAIL / UNSCORED / ERROR (closed set).
  UNSCORED never counts toward passes and carries its reason
  (including "not scoreable on the toy fixture"). A checker that
  could not run is ERROR — never a scientific FAIL. A voided item
  cannot re-acquire PASS from stale defaults.
- Transactional edits, narrowly scoped: pattern-based/scripted edits,
  and edits to structural declarations, stage dependencies, verdict
  logic, or report generators, must verify the pre-edit state, apply,
  assert the intended change actually occurred, and run the relevant
  verifier. "The edit was issued" is never evidence it happened.
  Ordinary code editing under the build-test loop carries no ceremony.
- Verification is proportional to the change: presentation-only ->
  regenerate + scripts/gate_battery.sh --quick, never rerun science;
  report-generator -> that generator + its tests; single stage ->
  that stage + downstream dependants only; structural/methodology ->
  broader rebuild; gate closure -> full battery + cold-start check.
- Tests write only to temp dirs (ARTIFACTS_ROOT); baselines and
  frozen evidence are read-only to tests. Cold-start evidence comes
  from scripts/cold_start_check.sh, never from hand-written claims.

## Execution model
- The artefacts are the project, not the session. Each beat starts in
  fresh context from milestones/beat-state.md (compact handoff,
  rewritten at every beat end). The coordinator holds orchestration
  state only — never the full scientific history.
- Genuinely separable work (pillars, failed load-bearing claims,
  reviewers) runs as parallel fresh-context workers with only the
  evidence slice each needs. A worker that clearly OWNS a
  module/stage may write its code, tests, and outputs; git
  branches/worktrees are encouraged for isolated parallel work.
  Shared state (ledgers, REGISTRY.json, reports, gate artefacts) and
  integration belong to the coordinator; two workers never edit the
  same files. Workers get defined deliverables and completion
  conditions, never "keep looking until nothing is found".

## Process rules
1. Pre-registration: gate criteria, acceptance bands, stage
   expectations, and REGISTRY.json are committed at intake, before
   the code they score.
2. Bands may be loosened iteratively, in small steps, without
   approval — but never beyond that band's LOOSENING CEILING, set per
   metric at intake in the metric's own units and direction. Each
   change is logged BEFORE re-scoring (old -> new, methodological
   reason) — and never justified by proximity of the observed value;
   a band recorded only in a code comment is a battery failure. At
   the ceiling and still failing: materially different approach, or
   declare the pillar failed. Final reporting shows initial vs final
   bands.
3. Gates reflect the stated criteria and the produced evidence —
   every pre-registered criterion scored, quoted verbatim, failures
   included. No reworded criteria, no optimistic rounding.
4. Modularity serves diagnosis: one src/ module per stage, single
   entry point (src/pipeline.py). Each stage writes its outputs via
   src/common/freeze.py, reports its expectations via
   src/common/expectations.py, and can be re-run independently.
5. Testing: ONE system battery running the whole pipeline end-to-end
   on a small fixture. No per-module unit sprawl. Regression pins
   only when an actual bug earns one.
6. Divergence handling order: LOCALIZE first (walk the stage
   boundaries, find the first output breaking its expectations),
   classify in DIVERGENCES.md, then investigate. Attribution before
   theory.
7. Gate reviews: the three perspectives run in PARALLEL, in strict
   isolation; each bundles ALL its findings in ONE pass, each finding
   BLOCKING or NON-BLOCKING (no finer taxonomy, no waiver system).
   Then ONE batch remediation of blocking findings, then ONE
   delta-only closure pass; a third pass only if remediation itself
   introduced a new blocker. No recursive review loop. An
   unresolvable material blocker ends the gate UNRESOLVED via an
   R-block. Non-blocking findings are recorded, never reopen a gate.
8. KNOWN-WEAK items are added freely and marked RESOLVED when fixed.
   Build and flag beats gold-plating.
9. A direction killed at a gate or by human decision stays closed
   unless reopened with new evidence. Do not retry it renamed.
10. Expectation/band changes record what changed and why — original
    wording, new wording, reason, trigger — with no classification
    taxonomy. A repeated or material reviewer catch can become a
    mechanical check: a judgment call, logged to the template's
    IMPROVEMENT-BACKLOG, no fixed trigger count.

## Anti-scope-creep (binding on all template and project work)
Do not turn useful conceptual distinctions into new machinery,
ledgers, labels, files, states, or metadata unless genuinely needed to
(a) control execution, (b) mechanically verify state, or (c) preserve
load-bearing scientific provenance. Otherwise use ordinary prose and
existing structures. The only closed vocabularies are the four result
states, the blocking flag, and the five recovery outcomes.

## External cost discipline
- COST-PROFILE.md lists prospective EXTERNAL/metered spend only
  (paid APIs, cloud compute, licensed data, hosted services); if
  none, it says "No external spend planned." in one line. No
  bookkeeping of local CPU or free packages.
- The agent NEVER introduces a new paid dependency, and never
  materially exceeds an agreed item's stated scale, without
  escalating it as a new decision (STOP-AND-ASK) first.

## Escalation (two modes)
- STOP-AND-ASK: touches direction (GOAL / ACCEPTABILITY / gate
  criteria / ANCHOR / REGISTRY structure-as-direction / COST-PROFILE),
  a band at its loosening ceiling and still failing, or evidence
  contradicts a prior human decision. Write an R-block (STATUS: OPEN)
  in ledgers/RULINGS.md, stop.
- LOG-AND-CONTINUE: everything covered by POLICIES.md and rules
  above — act, log the decision, it appears in the next digest.
Human gates are exactly: intake sign-off, final approval, and
exceptional escalation. No other checkpoints.

## Style
Plain language, numbers before prose, no self-assessment adjectives.
Reports short. Code simple, elementary, modular, readable — no
optimisation the problem doesn't demand.
