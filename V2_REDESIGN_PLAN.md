# V2 REDESIGN PLAN

Consolidated from the current template state and the five improvement
documents in IMPROVEMENT/, after the first two live runs (Run 1, Run 2).
This is a plan, not an implementation. Nothing in the template has been
changed.

---

## 1. Current V1 architecture

Three beats: INTAKE (human sign-off) -> MVP at toy scale (auto-continue
if clean) -> FINAL at full scale (human approval required).

Components as they exist:

- **Standing rules**: CLAUDE.md — anchor/target pinning, two exception
  ledgers (CONJECTURES, DIVERGENCES), band ceilings, substitution
  limits, localize-first, cost discipline, two escalation modes.
- **Intake-compiled project layer**: PAPER-FACTS, ACCEPTABILITY,
  POLICIES, COST-PROFILE, refs/LIT-DEFAULTS, gate shells
  (M-INTAKE, MVP-GATE, FINAL-GATE). The stage map (modules + frozen
  outputs + expectations) is compiled at intake but exists only as
  prose inside milestone/spec files — there is no machine-readable
  stage-map artefact.
- **Ledgers**: RULINGS (human decisions), DIVERGENCES, CONJECTURES,
  KNOWN-WEAK, IMPROVEMENT-BACKLOG.
- **Skills**: intake-compiler, replication-milestone, gate-review.
- **Reviewers**: red-team (Read/Grep/Glob/Bash) + domain-expert and
  practitioner (Read-only), convened at both gates; V1 specifies
  serial order (red team FIRST, recorded before the others run).
- **Scripts**: extract_paper.sh (Marker or degraded dump),
  rasterize.py (300-DPI page images), gate_battery.sh (Stop +
  pre-commit hook: pytest, conjecture tripwire, red-team-section
  check), run_milestone.sh (headless iteration loop).
- **Stage I/O**: src/common/freeze.py — parquet save/load, optional
  hash manifest. One system-battery test scaffold.

Execution model: a long-lived agent session iterates on a milestone;
gates are enforced by agent discipline plus two thin hook checks.
Reviews are assembled by the same session that did the work, with
fresh-context subagents for the three perspectives.

V1-internal inconsistencies found in this review (stale duplicated
state inside the harness itself): run_milestone.sh halts on a
`## PENDING` marker and a `checkpoint/*-review` git tag that no current
file or skill ever writes (RULINGS uses `STATUS: OPEN`; gate-review
writes `MVP-digest.md` / `FINAL-review.md`); gate_battery.sh checks for
a `## 4. Red-team report` heading that matches neither digest format.
The harness already exhibits, in miniature, the stale-presentation
failure class the runs exposed.

---

## 2. Failure modes actually observed across the two runs

Grouped; each backed by at least one concrete incident in the notes.

**F1 — Gate not mechanically enforced.** Run 1 began full-scale work
before the MVP review had cleared. The gate existed as prose only.

**F2 — Unbounded reviewer recursion.** Run 2: 16 red-team iterations,
roughly 8 hours at the final gate; serial review->fix->review chains;
drip-fed blockers; no stopping condition other than reviewer
exhaustion.

**F3 — Prose asserting properties the executable state lacked.** Three
separate Run 2 red-team passes each caught one instance: verdict prose
contradicting the computed band; a claimed-removed cross-stage
dependency still present in code; a scorecard claiming a producer that
did not exist. The recurring shape: documentation described a state the
project did not have.

**F4 — Silent no-op edits trusted as applied.** A pattern-based edit
failed to match, changed nothing, and was then described everywhere as
completed. Root of the F3 pass-2 incident.

**F5 — Hard-coded verdicts in reporting stages.** Both runs: final
narrative strings asserted results independently of the computation,
letting the report tell a different story from the numbers — including
describing an out-of-band perturbed value as in-band.

**F6 — Self-referential expectations.** Checks that could only pass:
a filter criterion re-checked on data already selected by that
criterion; ID lists checked against a module's own hard-coded copy.
Restoring one to its pre-registered meaning produced an honest FAIL.

**F7 — Checker failure read as scientific failure.** A tripwire
reported a conjecture breach in a repository with zero conjectures
because the interpreter could not launch. The same environment-
resolution bug appeared independently in both runs.

**F8 — Stale duplicated ruling/result state.** A ruling changed a
scored interpretation to FAIL; scoring reflected it; several shipped
artefacts still asserted the old PASS and that the ruling was open.
Separately, a voided criterion re-acquired PASS through stale scoring
logic.

**F9 — Goalpost movement.** A band was loosened to just below the
observed value, recorded only in a code comment; caught by review, not
by the framework.

**F10 — Perturbation demo that stopped short.** The injected fault
localized correctly but never altered the final assessment, because
the reporting stage was hard-coded (F5). Diagnostic power was claimed
but not demonstrated end-to-end.

**F11 — Declared artefacts never produced.** Seven declared figures
had no producing code; the artefact test was derived from a separate
manually maintained (incomplete) list, so the gap was invisible until
review.

**F12 — Tests mutating baseline evidence.** The battery overwrote a
frozen baseline, making a warm run pass as cold; earlier cold-start
evidence was hand-written rather than generated.

**F13 — Runtime dominated by orchestration, not science.** ~16-hour
run; small prose edits triggering multi-minute rebuilds; repeated
full-context rereads; a long-lived session carrying the whole history;
reviewers re-inspecting the entire repository per pass.

**F14 — Blind/exposed distinction improvised mid-run.** Author-code
details reached the main context before a blind-first ruling existed;
handled sensibly ad hoc, but the framework had no native provenance
labels and no defined recovery path for blind failures — several blind
FAILs were later shown recoverable as hidden method choices.

**F15 — Ceremony without payoff.** Cost accounting around zero-spend
local operations; a high volume of human-facing intake surface for
decisions that needed no human judgment.

---

## 3. Consolidated V2 changes, by area

Format per change: WHAT / EARNED BY / WHERE / RELATION (replaces,
modifies, or adds).

### Area A — Beat structure

**A1. Split the post-MVP work into FULL BLIND -> PARITY RECOVERY ->
FINAL REVIEW.**
- WHAT: The full-scale build runs under a blind evidence boundary.
  Blind reconstruction is a DIAGNOSTIC phase — it measures what can
  be rebuilt independently — not an artificial restriction on the
  final replication. Default blind evidence: the paper, the supplied
  data, cited literature/methods, and legitimate public technical
  documentation needed to use those inputs. Author code and author
  implementation material are excluded from BLIND by default.
  Per-claim blind results are then frozen — value, score, code
  version, parameters, evidence used, divergence diagnosis.
  Recovery is scoped to primary load-bearing quantitative claims —
  the intake-defined scored set, default the ACCEPTABILITY pillar
  claims. A load-bearing claim scoring FAIL or NOT-REPRODUCIBLE
  enters target-aware recovery; failed supporting rows and ordinary
  stage expectations are never auto-promoted into recovery — they
  are reported as-is, though supporting quantities may of course be
  investigated where needed to diagnose or recover a load-bearing
  claim. Recovery: diagnose the shape of the miss, generate method
  hypotheses from it, and use any legitimate, verifiable evidence
  relevant to reconstructing what the authors actually did — author
  code, supplementary implementation material, configs/scripts,
  calibration products, cited methods, other public technical
  evidence — each consultation logged. Test choices because they
  reproduce the published quantity, prefer choices that jointly
  explain multiple outputs, seek independent confirmation. A
  supported recovered method is implemented through the real
  pipeline and propagated to all dependent quantities — the
  recovered value is produced by the pipeline, never patched into a
  headline. Hidden benchmark answers, tolerances, and solution or
  evaluation-specific material remain inaccessible throughout BOTH
  phases — that boundary never expands.
  Recovery per claim ends in one of: RECOVERED / SUBSTANTIVE-
  DIVERGENCE / NON-IDENTIFIABLE / UNRECOVERABLE / OUT-OF-SCOPE.
- EARNED BY: F14 — several blind failures on Run 2 were later shown
  to be recoverable hidden method choices (a unit-convention
  discrepancy, a threshold definition, an aggregation rule); under
  pure blind rules they would terminate as "cannot replicate", which
  under-reports both the paper and the system.
- WHERE: CLAUDE.md three-beats section; a new RECOVERY section in the
  replication-milestone skill; FINAL-GATE shell; intake-compiler
  (compiles the blind evidence boundary and the recovery policy).
- RELATION: modifies the beat structure; adds one stage. The MVP toy
  beat is unchanged.

**A2. Permanent dual reporting: blind vs recovered, never merged.**
- WHAT: Every scored claim reports its blind result and, where
  recovery ran, its recovered result side by side, each with its
  provenance (E1). For a recovered result, the evidence basis of
  each recovered choice (confirmed by text, code, or data; inferred
  from multiple outputs; inferred from the target alone) is recorded
  as fact in the row's evidence — recorded facts, not a closed
  support-label set. Top-level metrics reported separately: blind
  parity rate (paper completeness), recovered parity rate (system
  capability), unresolved rate (the only basis for a strong
  "could not reproduce" statement). The recovered value never
  replaces or retroactively improves the blind value.
  This yields two frozen, separately benchmarkable evaluation
  views: the BLIND view (project state at the end of the full-scale
  blind build) and the RECOVERED view (state after legitimate
  recovery). Each can be scored independently against the same
  hidden benchmark tasks and tolerances — the blind score measures
  independent reconstruction ability, the recovered score full
  replication capability. The harness never sees hidden benchmark
  expected answers or tolerances during either phase;
  benchmark-answer leakage is an evaluation failure, distinct from
  author-material exposure.
- EARNED BY: F14; the design principle in the parity note — do not
  manufacture parity, preserve the difference.
- WHERE: ACCEPTABILITY (evidence-form conventions), FINAL-GATE shell,
  gate-review skill (parity report format).
- RELATION: adds to the parity report format; modifies nothing about
  scoring rules.

**A3. Hard MVP gate, mechanically enforced.**
- WHAT: Full-scale execution is impossible until a machine-checkable
  gate-state artefact exists recording: MVP scorecard all-PASS, three
  PROCEED verdicts, no blocking findings open. The battery/hook
  refuses full-scale stage runs without it. Auto-continue is kept —
  the change is that the harness, not agent discipline, enforces the
  sequence.
- EARNED BY: F1.
- WHERE: gate_battery.sh (or successor verifier), MVP-GATE shell,
  replication-milestone skill.
- RELATION: modifies existing gate behaviour from prose rule to
  mechanical block.

**A4. Final adjudication step.**
- WHAT: After FINAL review and remediation, one explicit decision
  step reads the final implemented evidence and decides how each
  claim is reported: the per-claim outcome table (blind status,
  recovery status, provenance labels, sensitivity ranges where
  load-bearing), the three reviewer verdicts with dissents verbatim,
  initial-vs-final bands, and carried non-blocking findings —
  producing the
  replication report plus the approval R-block, generated from the
  structured evidence (C3), not written fresh. Adjudication is a
  reporting decision only: it does not investigate, change
  methodology, launch recovery, or search for better numbers. Mixed
  outcomes are preserved; there is no project-level PASS/FAIL
  collapse.
- EARNED BY: F5, F8 (the report must be a projection of the evidence,
  not a parallel narrative); the strong mixed-outcome behaviour both
  runs already showed is kept as the required output shape.
- WHERE: gate-review skill (extends the existing step-5 approval
  request into a defined artefact); FINAL-GATE shell.
- RELATION: modifies the existing final-review assembly; adds the
  per-claim outcome table as its structured input.

### Area B — Review architecture

**B1. Parallel isolated reviewers.**
- WHAT: For a frozen candidate, red team, domain expert, and
  practitioner launch simultaneously, each with fresh context and its
  evidence-pack slice only; none sees another's verdict; findings are
  aggregated only after all three return. This replaces the V1
  "red team first, recorded before the others run" serial rule.
- EARNED BY: F13 — serial ordering added wall-clock without adding
  independence; both runs show the roles catch different failure
  classes regardless of order.
- WHERE: gate-review skill, README, .claude/agents/bench/README.md.
- RELATION: replaces the serial-order rule; isolation rules unchanged.

**B2. Fixed two-pass review protocol (conditional third).**
- WHAT: Per gate: freeze candidate -> Pass 1 full review (three
  perspectives in parallel; each bundles ALL its findings in one
  pass, each finding marked BLOCKING or NON-BLOCKING — no finer
  taxonomy, no severity hierarchy, no waiver system) -> ONE batch
  remediation of blocking findings -> Pass 2 targeted closure
  review of the delta only (previous blockers, changed files,
  affected outputs, likely regressions). A Pass 3 occurs only if
  remediation itself introduced a new blocking defect; there is no
  normal recursive loop. A blocking finding must be addressed
  before normal gate closure; if a material blocker cannot be
  resolved, the gate ends UNRESOLVED and surfaces it through the
  existing human approval/escalation path. Non-blocking findings
  are recorded and carried; they never reopen the gate. Gate
  closure requires: blocking findings addressed, battery clean,
  three closure verdicts — not the absence of any possible
  criticism. The same shape runs at both gates, but MVP review is
  materially lighter: it asks only whether the toy pipeline is
  trustworthy enough to scale; FINAL performs the serious
  scientific review of the replication claim itself.
- EARNED BY: F2 — 16 iterations / ~8 hours is a calibration result,
  not an operating model; adversarial review with no stopping
  condition never terminates.
- WHERE: gate-review skill (both gates); reviewer briefs (add the
  bundle-and-classify requirement and the closure-pass scope).
- RELATION: modifies the review loop; adds the blocking/non-blocking
  distinction and fixed pass structure. Appears in three improvement
  docs — implemented once.

**B3. Delta review packs.**
- WHAT: Passes after the first receive: prior findings, remediation
  record, changed files/artefacts, regenerated outputs, regression
  results — not the whole repository. Full re-review only when a fix
  changed core methodology, data selection, acceptance logic, or a
  major dependency.
- EARNED BY: F2, F13 — a small fix should produce a small review
  surface.
- WHERE: gate-review skill (pack-assembly rules).
- RELATION: adds pack rules to the existing evidence-pack mechanism.

**B4. Recurring reviewer catches can become mechanical checks.**
- WHAT: Standing rule: a repeated or material review catch can
  motivate a mechanical check — a judgment call logged to the
  template IMPROVEMENT-BACKLOG, with no fixed trigger count and no
  automatic conversion. The
  V2 battery ships pre-seeded with the classes already earned by the
  two runs: declared-artefact existence, stage-map/implementation
  consistency, hard-coded verdict detection (verdict strings must
  come from structured evidence), stale generated reports, silent
  no-op edits, self-referential expectations, quarantined values
  leaking into active state, perturbations not reaching final
  verdicts.
- EARNED BY: F2's root cause — reviewer cycles spent on repository
  hygiene already discovered on previous papers.
- WHERE: CLAUDE.md process rules (one line); the battery/verifier
  set (C1); template governance section of README.
- RELATION: adds a rule; the checks themselves land via Area C.

### Area C — Mechanical trust

**C1. Structural truth only from executable state; one verifier set.**
- WHAT: A small script set (battery members, not a framework) that
  mechanically verifies: stage DAG / cross-stage reads match the
  declared structure (the C9 registry); every declared artefact is
  produced — declaration covers shipped/load-bearing artefacts only
  (stage outputs consumed downstream, gate evidence, report
  figures); scratch plots, caches, and diagnostics are neither
  declared nor checked; expectation IDs bidirectionally reconciled
  between the frozen declaration and what code actually emits
  (missing, unregistered, duplicate, wrong-owner all fail;
  parent/child IDs handled explicitly); cold-start idempotency
  demonstrated by a generator that starts from empty output
  directories and diffs every declared output including binaries —
  never by hand-written evidence. Prose may describe structural
  state; only executable inspection may establish it.
- EARNED BY: F3, F11, F12 — the claimed-removed dependency still in
  code; nine unregistered IDs and a duplicate found the moment a real
  cross-check ran; seven declared figures with no producing code; a
  warm run passed off as cold.
- WHERE: scripts/ + tests/ (battery); referenced from MVP-GATE
  criteria and gate_battery.
- RELATION: adds the verifiers; replaces trust-by-narrative. Requires
  C9 (the minimal structural registry) to have something to verify
  against.

**C2. First-class result states.**
- WHAT: Expectation and gate results use a minimal closed state
  set — PASS / FAIL / UNSCORED / ERROR — with rules: UNSCORED never
  contributes to pass counts and carries its reason as recorded fact
  (including "not scoreable on the toy fixture" — no dedicated skip
  state); a checker crash is ERROR, never scientific FAIL; a voided
  item cannot re-acquire PASS from stale defaults. Every harness
  utility returns machine-readable status distinguishing
  "ran and passed" / "ran and failed" / "could not run".
- EARNED BY: F7, F8 — the crashed tripwire read as a conjecture
  breach; the voided criterion re-acquiring PASS.
- WHERE: freeze.py/expectation-runner conventions, gate_battery,
  scorecard format in gate-review skill.
- RELATION: replaces implicit binary pass/fail; merges improvement
  items 6 and 7 (same state machine).

**C3. Load-bearing claims are generated, with one source per mutable
fact.**
- WHAT: Scorecards, parity rows, verdict labels, counts, and
  band-status lines are generated from the same structured evidence
  files used for scoring. Free prose may explain a result, never
  independently assert one. Each mutable ruling/result has exactly
  one current source (RULINGS for rulings; the structured results
  artefact for scores); every presentation is regenerated from it, so
  a change propagates everywhere or the generator fails — stale
  contradictory copies cannot survive. A presentation-only
  regeneration never reruns scientific stages.
- EARNED BY: F5, F8 — hard-coded report prose contradicting computed
  results in both runs; the ruling whose old verdict survived in
  shipped artefacts.
- WHERE: a thin report-generator convention in src/ + gate-review
  skill; CLAUDE.md one-line rule.
- RELATION: replaces hand-written scorecards/report sections;
  subsumes TWO_RECENT_HARNESS_CHANGES item 1 entirely.

**C4. Transactional, self-verifying edits (narrowly scoped).**
- WHAT: The transactional discipline — verify the expected pre-edit
  state; apply; assert exactly the intended change occurred; verify
  the post-edit invariant; fail loudly otherwise — applies where
  silent no-ops or partial application actually matter: pattern-
  based/scripted edits, and edits to structural declarations, stage
  dependencies, verdict logic, or generated-report producers. Such
  edits then trigger the relevant C1 verifier (dependency change ->
  DAG check; ID change -> map consistency; verdict-logic change ->
  perturbation/assessment tests; artefact-declaration change ->
  completeness), and are not complete until the postcondition is
  mechanically demonstrated — "the edit was issued" is never
  evidence it happened. Ordinary code editing under the normal
  build-test loop carries no ceremony.
- EARNED BY: F4 — repeated silent no-op edits described as completed.
- WHERE: CLAUDE.md process rules + replication-milestone skill; the
  postconditions are the C1 verifiers, no new machinery.
- RELATION: adds a working rule; leans on C1 rather than adding a
  layer.

**C5. Explicit environment resolution.**
- WHAT: All harness scripts resolve and use the project's own
  environment — venv interpreter, pytest executable, working
  directory — never bare `python`/`pytest`/shell assumptions.
- EARNED BY: F7 — the identical environment bug appeared
  independently in both runs.
- WHERE: gate_battery.sh, run scripts, any C1 verifier.
- RELATION: modifies existing scripts.

**C6. Tests never mutate baseline or frozen evidence.**
- WHAT: The battery writes only to isolated temp directories; MVP
  baselines, perturbation baselines, final artefacts, and frozen
  reviewer evidence are read-only to tests.
- EARNED BY: F12.
- WHERE: test scaffold docstring contract + a battery check.
- RELATION: adds a rule to the existing battery design.

**C7. Expectation quality rules + perturbation-to-verdict demo.**
- WHAT: Intake-time authoring rules: no expectation may be satisfiable
  purely because the data were selected by the same criterion
  (self-validation test applied to each); stage expectations exist
  to give the stage diagnostic power — properties that would catch
  the stage failing locally (correctness, sanity, reconciliation,
  identifiability are typical examples, a guiding principle, not a
  mandatory per-stage category checklist) — and final paper parity
  lives in ACCEPTABILITY only.
  Independent anchors are added only where the same wrong constant/
  helper/transform could make all stages agree while being wrong.
  Perturbation testing carries no template-mandated count: the
  minimum is one meaningful injected fault that first appears at the
  correct stage, propagates along the declared DAG, changes a
  downstream quantity, and changes a final result/verdict. Any
  additional perturbations are justified by the project's actual
  structure and risk (shared-state exposure, a central quantity, an
  intake-identified failure class) — never by ritual, and never
  exhaustive mutation testing.
- EARNED BY: F6, F10; the shared-state propagation incident in Run 1;
  fault injection's demonstrated value vs its runtime cost.
- WHERE: intake-compiler skill (stage-map authoring section),
  MVP-GATE shell (bisection-demo criterion strengthened).
- RELATION: modifies existing expectation and perturbation-demo
  specifications; merges improvement items 10–14.

**C8. Visible history for expectation and band changes.**
- WHAT: Every post-registration change to an expectation preserves
  original wording, corrected wording, the reason, and what
  triggered it — a plain record of what changed and why, with no
  classification taxonomy. Band changes must be logged before
  re-scoring, state a
  methodological reason, stay inside the intake ceiling, and may
  never cite proximity of the observed value as justification — a
  band recorded only in a code comment is a battery failure.
- EARNED BY: F9; both runs contained legitimate corrections and one
  genuine goalpost move, and reviewers need the history to tell them
  apart.
- WHERE: the prose stage map carries the wording and change notes
  (same correct-note-continue discipline PAPER-FACTS already uses);
  CLAUDE.md band rules extended by one sentence; a battery check
  that scored bands match ACCEPTABILITY's logged band state (the
  single source for bands). No new ledger, no human checkpoint —
  agents correct and record autonomously; only changes to what a
  band or criterion MEANS escalate, per the existing rule.
- RELATION: modifies the existing band-loosening rules and
  PAPER-FACTS-style correction discipline; extends it to
  expectations.

**C9. Minimal structural registry (reconsidered, slimmed).**
- WHAT SPECIFIC PROBLEM IT SOLVES: The C1 verifiers and D3 targeted
  reruns need a frozen declaration of pipeline structure to check
  the implementation against. The existing template cannot supply
  one cleanly: the V1 stage map exists only as prose inside
  intake/milestone files (not mechanically checkable); declarations
  embedded in the code itself are exactly the self-referential
  failure F6 (code checked against code); freeze.py manifests are
  per-run outputs, not pre-registered declarations; and no existing
  artefact records dependency edges, declared artefacts, or
  expectation ownership at all. Both runs' new checks only became
  possible after an ad-hoc version of this declaration was created.
- WHAT: One flat structured file, compiled at intake alongside the
  prose stage map and frozen at sign-off, containing ONLY the
  structural declarations nothing else records: stage IDs,
  dependency edges (declared inputs -> outputs), declared artefacts
  per stage, and expectation IDs with their owning stage. It
  explicitly EXCLUDES everything that already has a home — bands and
  ceilings (ACCEPTABILITY), acceptance criteria (gate files),
  expectation wording and correction history (the prose stage map,
  C8), results and scores (structured results artefacts), rulings
  (RULINGS). It is therefore not a second source of truth for
  anything: for its four structural facts it is the only source.
- EARNED BY: F3, F6, F11 — undeclared cross-stage reads, IDs checked
  against modules' own lists, declared figures nothing produced.
- WHERE: new small file under the intake-compiled layer, written by
  intake-compiler, frozen at sign-off. Post-sign-off structural
  corrections follow the normal correct-record-continue discipline
  (no new human checkpoint); only direction-touching changes
  escalate, per the existing rules.
- RELATION: adds the one genuinely new artefact of V2, cut to four
  fields; the C1 verifiers and D3 rerun scoping key off it. If
  during implementation the same four facts can be carried in an
  existing intake file as a marked table, that is acceptable — the
  requirement is a frozen, parseable declaration, not a new file
  per se.

### Area D — Orchestration and iteration speed

**D1. Thin coordinator; artefacts are the project state.**
- WHAT: The long-lived session stops being the project. Each beat
  starts in fresh context from a compact state artefact written at
  the end of the previous beat (target, scope, boundary, stage map
  reference, open items, artefact locations, current rulings/verdict
  status). The coordinator holds orchestration state only — never
  the full scientific history — and launches short-lived workers.
- EARNED BY: F13 — accumulated context, repeated rereads, and
  anchoring on hours of prior reasoning dominated the 16-hour run.
- WHERE: replication-milestone skill (execution model section);
  run_milestone.sh rewritten around beat-level fresh starts; the
  beat-state artefact format defined once in the skill.
- RELATION: replaces the single-session iteration model.

**D2. Modular sub-agents with clear ownership; coordinator owns
shared state.**
- WHAT: Genuinely separable work (pillars in the blind build, failed
  load-bearing claims in recovery, the three reviewers) runs as
  parallel fresh-context workers, used aggressively where the split
  is real. Each worker gets only the evidence slice it needs (its
  claim, relevant facts/excerpts, its stage inputs/outputs, relevant
  divergences/rulings) — assembled by the coordinator by convention,
  not by a built slicing engine. A worker that clearly OWNS a
  module/stage may write its code, tests, and outputs directly;
  git branches/worktrees are encouraged for isolated parallel
  development. Shared/global state — ledgers, the registry, final
  reports, gate artefacts — and integration/merge belong to the
  coordinator's integration step; two parallel workers never edit
  the same files or state. Workers return small structured summaries
  (claim, status, finding, evidence, confidence, affected stages)
  and get defined deliverables and completion conditions, never
  "keep reviewing until nothing is found".
- EARNED BY: F13; F2 (open-ended review instructions); parallel
  edits to shared state risk the stale-state class of F8.
- WHERE: replication-milestone + gate-review skills; reviewer briefs
  already assume slices — extended to build/recovery workers.
- RELATION: adds an execution convention; no new files.

**D3. Proportional, dependency-aware verification.**
- WHAT: Verification scales to the change, using the C9 dependency
  edges: presentation-only edit -> regenerate presentation + light
  consistency check, never rerun science; report-generator change ->
  that generator + its tests; single-stage change -> that stage +
  downstream dependants only; structural/methodology change ->
  broader rebuild; gate closure -> full battery + cold start.
  Frozen scientific outputs are rerun only when scientific inputs or
  methodology actually change.
- EARNED BY: F13 — minutes-long rebuilds after one-sentence edits;
  subsumes TWO_RECENT_HARNESS_CHANGES item 2.
- WHERE: replication-milestone skill; gate_battery gains a
  scoped mode alongside the full mode.
- RELATION: modifies the "run the battery" default; replaces the
  separate two-changes note.

**D4. Minimal timing log.**
- WHAT: Beat, stage, worker, and review-pass start/end times plus
  counts of full vs targeted reruns, appended to one plain log file.
  Nothing more.
- EARNED BY: F13 — regressions in orchestration cost were invisible.
- WHERE: run scripts.
- RELATION: adds one thin log; explicitly capped to prevent
  telemetry growth.

**D5. Repair the harness's own stale mechanics.**
- WHAT: run_milestone.sh stop conditions and gate_battery.sh checks
  are rewritten against the actual artefact names and the A3
  gate-state artefact — the successor mechanisms, not patches to the
  dead grep targets.
- EARNED BY: found in this review (Section 1); same failure class as
  F8, inside the harness.
- WHERE: scripts/.
- RELATION: replaces broken stop conditions.

### Area E — Scientific reporting

**E1. Result provenance recorded, minimally.**
- WHAT: The load-bearing provenance distinction is structural and
  already carried by dual reporting: BLIND (built inside the blind
  boundary) vs RECOVERED (with the consulted author/external
  material listed from the recovery log). Beyond that, provenance is
  recorded fact, not a label set: a recovered row cites what was
  consulted; a blind-phase result that author material accidentally
  reached carries a note saying so. The sequence is explicit:
  reconstruct blind, score, freeze, localize — and only then consult
  author material, in recovery, preserving both results (feeds
  A1/A2). Accidental exposure is handled by that recorded note,
  never by restarting; benchmark-answer leakage is a separate
  evaluation failure, not a provenance matter.
- EARNED BY: F14 — the distinction was improvised mid-run; a
  numerically reproduced result can still be methodologically
  contaminated.
- WHERE: parity-report format (gate-review skill), DIVERGENCES
  conventions, intake-compiler (anchor statement already covers the
  role of released code — extended to the blind-first sequence).
- RELATION: modifies existing anchor/divergence conventions; no new
  ledger.

**E2. Unavailability stated plainly, not vocabularised.**
- WHAT: A parity row whose evidence cannot be obtained says so with
  its reason in plain language (unavailable, author-held, out of
  agreed scope, would require a new external dependency) rather than
  silently approximating. A stated reason in the row — not a new
  status vocabulary: the existing DIVERGENCES machinery
  (UNCLASSIFIABLE, PERMANENT-OPEN, substitution limits) already
  carries the structured part.
- EARNED BY: Run 2 did this correctly ad hoc; making it native
  preserves the behaviour.
- WHERE: parity-report format (gate-review skill), one line.
- RELATION: a reporting rule only; no new states.

**E3. Preprocessing sensitivity as a first-class output where
load-bearing.**
- WHAT: When a scored result changes materially under defensible
  preprocessing alternatives, the report gives the range (parameter
  varied, defensible span, affected output, whether the verdict
  changes) instead of presenting one choice as uniquely determined.
- EARNED BY: two Run 2 results whose values moved several-fold under
  defensible filtering choices.
- WHERE: ACCEPTABILITY evidence forms (intake decides which pillars
  need it); final report format.
- RELATION: adds an evidence form; applied selectively, not
  universally.

**E4. Fact / inference / explanation labelling in reports.**
- WHAT: Material conclusions distinguish OBSERVED / SUPPORTED
  INFERENCE / POSSIBLE EXPLANATION. A reporting convention only — no
  ledger, no tags on ordinary work.
- EARNED BY: Run 1's plausible causal stories that later needed
  narrowing.
- WHERE: gate-review skill report rules + practitioner brief (one
  line each).
- RELATION: adds a convention.

### Area F — Slimming

**F1. Thin human-facing intake.**
- WHAT: Deep internal intake reasoning is kept; the human-facing
  contract shrinks to: target, material ambiguities, stage map,
  acceptance criteria, genuine judgment calls, external cost/
  dependency decisions. Low-level implementation choices resolve via
  POLICIES/LIT-DEFAULTS without surfacing as rulings.
- EARNED BY: F15 — both runs produced a large sign-off surface for
  decisions needing no judgment.
- WHERE: intake-compiler skill (interrogation + compile sections).
- RELATION: modifies presentation; the compiled layer itself is
  unchanged.

**F2. Cost profile stays thin.**
- WHAT: COST-PROFILE lists prospective external/metered spend only;
  a project with none states "No external spend planned." in one
  line. No bookkeeping of local CPU or free packages.
- EARNED BY: F15 — cost ceremony around zero-cost operations.
- WHERE: COST-PROFILE header, intake-compiler.
- RELATION: modifies emphasis; governance rule unchanged.

**F3. Targeted image verification at intake.**
- WHAT: Page-image verification is applied where parsing, layout,
  or figures make the extracted reading aid untrustworthy — garbled
  extraction, dense equations, complex tables, load-bearing numbers
  whose parsed form is doubtful — replacing V1's blanket rule that
  every equation and numeric fact is automatically image-verified.
  The anchor rule is unchanged: the PDF/page image wins on any
  disagreement. A degraded extraction lowers the threshold for
  suspicion; it does not make verification blanket.
- EARNED BY: F15 — the blanket rule spends intake effort where
  extraction is already clean; confirmed as a ruled simplification.
- WHERE: intake-compiler skill (Stage 0 discipline), README,
  PAPER-FACTS header.
- RELATION: modifies the V1 automatic-verification rule from
  blanket to judgment; the image-wins anchor rule is untouched.

(Model/effort routing, previously sketched here as an optional
orchestration hook, is deleted from V2 entirely — no config, no
hook point. Add it only when a real need appears.)

---

## 4. Improvement notes that should NOT become separate machinery

- **NEXT_HARNESS_ITERATION_TARGET_IMPROVEMENTS.md** (no "(1)") is a
  strict subset of the "(1)" file, which adds items 31–32. Treat the
  plain file as an obsolete duplicate; it contributes nothing the
  superset lacks.
- **TWO_RECENT_HARNESS_CHANGES.md** is fully subsumed: item 1
  (change applies everywhere) is C3's single-source generation;
  item 2 (proportional verification) is D3. No separate rules or
  files should be created from it.
- **Bounded review** appears in three documents (parity note §4,
  target-improvements #3, faster-iteration §7) with slightly
  different pass counts; B2 is the single merged mechanism (one full
  pass + one delta closure pass; a third only when remediation
  itself introduced a new material blocker).
- **Parallel isolated reviewers** appears in three documents; B1
  implements it once.
- **Delta review** appears in two documents; B3 implements it once.
- **Structural-truth items** 4, 5, 20, 22, 31 in the target-
  improvements list are one verifier set (C1 + C9), not five
  mechanisms.
- **States items** 6 and 7 are one state machine (C2).
- The parity note's own suggestion to simplify its 8-label recovery
  vocabulary is taken further: the only structured recovery
  vocabulary is the five terminal outcomes in A1 (they control
  execution — they are the stop conditions). The evidence basis of
  a recovered choice, provenance details, and unavailability
  reasons are recorded facts in the rows, not closed label sets.
- **Items already implemented in V1** and needing no new work beyond
  keeping them: exception-only metadata, localize-first, band
  ceilings with logged loosening (C8 only adds the change record and
  the anti-proximity sentence), substitution limits, three
  perspectives with fresh context and pack slices, evidence-pack
  reviewer isolation, stop-on-exception MVP digest, external
  benchmark separation (improvement item 26 — already outside the
  template's job), clean-base governance (item 30 — already the
  README rule).

---

## 5. Scope-creep and complexity risks

**Implementation principle (binding).** Do not turn useful
conceptual distinctions into new machinery, ledgers, labels, files,
states, or metadata unless the harness genuinely needs them to
(a) control execution, (b) mechanically verify state, or
(c) preserve load-bearing scientific provenance. If a distinction
does not control execution, mechanically verify something
important, or preserve genuinely load-bearing provenance, it does
not deserve a schema, status code, ledger, or mandatory workflow
step — use ordinary prose and existing structures. In particular:
no reviewer personas/councils/voting machinery beyond the three
existing briefs; no persistent sub-agent identities — workers are
task/module owners; no issue-tracker-style review metadata; no
proliferation of recovery/status labels; no workflow engine; no
automatic context-slicing system; no additional human gates; no
fixed ritual counts unless mechanically necessary; no duplicated
sources of truth.

Specific risks:

- **Automatic evidence-slice generation** ("generated from claim/
  stage dependencies where possible"): building a slicer is a
  project in itself. V2: the coordinator assembles slices by
  convention using the C9 registry. No slicing engine.
- **The C9 registry growing into a workflow/DAG framework or a
  second source of truth**: it is four structural fields in one flat
  parseable table plus a handful of check scripts, and must never
  absorb bands, criteria, results, or rulings. If it needs a schema
  library or an execution engine, it has overgrown.
- **Speculative hooks**: none ship — model routing is deleted
  outright rather than stubbed; a hook nobody uses is machinery.
- **Timing telemetry (D4)**: one plain append-only log. Anything
  resembling dashboards or metrics infrastructure is out.
- **Review findings (B2)**: one findings file per review pass, each
  finding BLOCKING or NON-BLOCKING. No severity hierarchy, no
  waiver system, no issue tracker, no cross-referencing system.
- **Fault injection**: minimal and risk-justified — one propagating
  end-to-end perturbation as the floor, more only where the project's
  structure earns them; exhaustive mutation testing is named in the
  notes as the failure mode.
- **Independent anchors (C7)**: only where correlated shared-state
  failure could change a conclusion — not duplicate implementations
  as a norm.
- **Recovery stage ambition**: A1's evidence-boundary expansion is
  logged consultation, not a second full replication project per
  failed claim; the stop conditions exist to end it.
- **Sub-agent proliferation**: parallel workers are used
  aggressively but only where ownership is genuinely separable
  (pillars, failed claims, reviewers, clearly owned modules); two
  workers never share files or global state, and integration stays
  with the coordinator. Intake does not need to fragment into many
  workers by default.
- **New states/labels generally**: the only closed vocabularies in
  this plan are the four C2 result states, B2's blocking flag, and
  A1's five recovery outcomes — each controls execution. Everything
  else (evidence basis, provenance, unavailability, expectation
  changes) is recorded fact or prose; resist per-project extensions
  and re-vocabularisation.

---

## 6. Proposed V2 execution flow, end-to-end

```
INTAKE (human gate — direction sign-off)
  compile: facts (image-checked where extraction warrants) · anchor
    + target · stage map
    (prose) + minimal structural registry (stages, edges, declared
    artefacts, expectation IDs + owners — nothing else)
  compile: blind evidence boundary (author material excluded from
    BLIND; hidden benchmark material excluded from EVERY phase) +
    recovery policy · gate criteria · ACCEPTABILITY (incl. the
    load-bearing claim set) · POLICIES · COST-PROFILE (thin) ·
    perturbation plan (risk-justified; no fixed count)
  interrogate: one bundled stop, thin human-facing contract
  sign-off -> direction frozen -> beat-state artefact written
        |
        v  (fresh context)
MVP — toy scale
  parallel workers own separable stages (branches/worktrees);
    coordinator integrates; battery = system test + structural
    verifiers (DAG/reads, artefact completeness, expectation-ID
    reconciliation, cold-start generator, state rules)
  perturbation demo: injected fault -> correct stage -> propagates ->
    changes a final verdict
  gate (LIGHT — trustworthy enough to scale?):
    scorecard generated from structured results
    -> 3 reviewers in PARALLEL isolation (bundled findings, each
       BLOCKING or NON-BLOCKING)
    -> ONE batch remediation -> ONE delta closure pass
       (3rd pass only if remediation introduced a new blocker)
    -> machine-checkable gate-state artefact written
  HARD BLOCK: full scale cannot start without it
        |  clean -> auto-continue (fresh context)
        v
FULL-SCALE BLIND BUILD
  independent pillars in parallel (owned modules, worktrees);
    coordinator owns shared state + integration; transactional edits
    (postcondition-verified, verifier-triggered)
  proportional verification per change class (via registry deps)
  score every claim against the blind boundary
  -> FREEZE blind results (values, scores, code, params, evidence,
     diagnosis) — permanent, never overwritten
     = BLIND evaluation view, independently benchmarkable
        |
        v  (fresh context; failed LOAD-BEARING claims only)
PARITY RECOVERY (target-aware, per intake policy)
  per claim in parallel: diagnose miss shape -> hypotheses -> expand
    evidence boundary (logged) -> test target-aware -> prefer joint
    multi-output recovery -> seek independent confirmation
  supported recoveries implemented through the real pipeline and
    propagated downstream — never patched into a headline
  end states: RECOVERED / SUBSTANTIVE-DIVERGENCE / NON-IDENTIFIABLE /
    UNRECOVERABLE / OUT-OF-SCOPE
  -> integrated candidate; dual results preserved (blind + recovered)
     = RECOVERED evaluation view, separately benchmarkable
        |
        v
FINAL — frozen candidate (FULL scientific review)
  parity report generated from structured evidence: per-claim blind
    vs recovered rows, provenance labels, unavailability states,
    sensitivity ranges, initial-vs-final bands
  3 reviewers in PARALLEL isolation on evidence-pack slices
    -> ONE batch remediation (blocking findings only) -> ONE delta
       closure pass (3rd pass only if remediation introduced a new
       blocker; unresolvable material blocker -> UNRESOLVED R-block)
        |
        v
ADJUDICATION (reporting decision only — reads final implemented
  evidence; no investigation, no methodology change, no recovery)
  per-claim outcome table + blind/recovered/unresolved rates +
    verdicts with dissents verbatim + carried non-blocking findings
    -> replication report
    (OBSERVED / SUPPORTED INFERENCE / POSSIBLE EXPLANATION)
  -> approval R-block. HUMAN GATE — always stops.
```

---

## 7. Summary

### 7.1 V2 architecture in one line per element

Five phases — INTAKE (human) -> MVP toy (hard mechanical gate, light
review, auto-continue) -> FULL BLIND (results frozen) -> RECOVERY
(failed load-bearing claims, target-aware, dual-reported) -> FINAL
full review + read-only ADJUDICATION (human). Executed by a thin
coordinator over fresh-context workers that own separable modules
(branches/worktrees), with shared state and integration held by the
coordinator; project state lives in artefacts, structural
declarations in one minimal frozen registry; every load-bearing
claim is generated from or verified against executable state; edits
are transactional; verification is proportional to the change;
review is parallel, isolated, bundled, delta-scoped, and
non-recursive. Human involvement stays where V1 put it: sign-off,
final approval, exceptional escalation.

### 7.2 Highest-priority changes

1. C9 + C1 + C3 — the minimal structural registry, the structural
   verifier set, and generated (single-source) scorecards/verdicts.
   These close the largest observed failure class (F3–F6, F8, F11)
   and are prerequisites for most other changes.
2. A3 — hard mechanical MVP gate (F1).
3. B1 + B2 + B3 — parallel isolated reviewers with bundled findings,
   one batch remediation, one delta closure pass, conditional third
   (F2).
4. A1 + A2 — parity recovery on frozen blind results, scoped to
   load-bearing claims, with permanent dual reporting (F14).
5. C4 — transactional self-verifying edits (F4).
6. D1 + D2 + D3 — artefacts-as-state with fresh-context beats,
   module-owning parallel workers, and proportional verification
   (F13).
7. C2 + C5 — first-class result states and explicit environment
   resolution (F7, F8).

### 7.3 Not carried into V2

- NEXT_HARNESS_ITERATION_TARGET_IMPROVEMENTS.md (the non-"(1)" file)
  — obsolete duplicate; delete when V2 lands.
- TWO_RECENT_HARNESS_CHANGES.md as separate machinery — subsumed by
  C3 and D3.
- The stale run_milestone.sh / gate_battery.sh stop-condition
  mechanics — replaced, not patched.
- Exhaustive mutation testing; duplicate implementations as a norm.
- Model-routing configuration or hooks — deleted entirely; added
  only when a real need appears. Telemetry beyond one plain timing
  log; any evidence-slicing engine.
- Label/state taxonomies beyond the minimal execution-controlling
  sets: no expectation-change classification, no fixture-skip
  result state, no recovery support-label set, no unavailability
  vocabulary, no provenance label scheme — recorded facts and
  prose instead.
- Blanket per-fact image verification at intake — replaced by
  targeted verification where extraction quality warrants it.
- Version/compatibility layers, migrations, per-paper modes —
  excluded by standing governance.
- The 8-label recovery vocabulary at full size — simplified per its
  own note.
- Weighted/aggregate project-level PASS-FAIL scoring — mixed
  per-claim outcomes remain the output shape.

### 7.4 Status before implementation

All design questions are resolved by ruling and embedded above:
gate topology (no new human checkpoints; sign-off, final approval,
exceptional escalation only); review shape (two passes, conditional
third, no recursion; findings BLOCKING or NON-BLOCKING only, no
severity hierarchy or waiver machinery; MVP light, FINAL full);
adjudication as a read-only reporting decision; recovery scoped to
the intake-compiled load-bearing pillar claims (supporting
quantities investigable in their service, never auto-promoted);
blind evidence defaults (paper, supplied data, cited
literature/methods, public technical documentation needed to use
them; author material excluded) with recovery free to use any
legitimate verifiable evidence; hidden benchmark material
inaccessible in every phase; two frozen benchmarkable views (BLIND,
RECOVERED); perturbation testing risk-justified with no fixed
count; the minimal four-field registry; the binding
anti-scope-creep principle (Section 5). A final pruning pass is
also embedded: result states reduced to PASS / FAIL / UNSCORED /
ERROR; expectation changes recorded, not classified; recovery
support levels, provenance, and unavailability carried as recorded
facts rather than label sets; the mechanical-check conversion rule
is a judgment call with no trigger count; transactional-edit
discipline scoped to where silent no-ops matter; artefact
declaration limited to shipped/load-bearing outputs; expectation
quality a principle, not a per-stage checklist; image verification
targeted rather than blanket; model-routing hooks deleted.

What remains is implementer's discretion within those constraints,
not design decisions: the registry's serialization form (anything
flat and parseable), the freeze mechanism for the two evaluation
views (git tag vs copied artefacts), and file naming.
