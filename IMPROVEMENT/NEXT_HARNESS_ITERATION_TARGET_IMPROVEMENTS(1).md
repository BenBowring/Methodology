# NEXT HARNESS ITERATION — TARGET IMPROVEMENTS

This file captures the **generic improvements earned by the first two live replication runs**.

It is intentionally not a redesign document. The goal is to preserve the scientific behaviour that is working while fixing the structural weaknesses repeatedly exposed by `topdown` and ASASSN-21qj.

---

## 1. Make MVP a real hard gate

**Target improvement**

Full-scale execution must be impossible until the MVP gate is genuinely cleared.

Required sequence:

1. toy / MVP build completes;
2. MVP evidence pack freezes;
3. all three reviewers complete;
4. blocking findings are resolved;
5. MVP returns `PROCEED`;
6. only then may full-scale execution begin.

**Reason**

Run 1 allowed full-scale work to begin before the MVP review had fully cleared. That defeats the purpose of the gate. If MVP is meant to answer whether the system is diagnostically trustworthy enough to scale, then the orchestration must enforce that mechanically rather than relying on agent discipline.

---

## 2. Run the three reviewers concurrently

**Target improvement**

Launch:

- Red Team
- Domain Expert
- Practitioner

simultaneously in isolated contexts.

Aggregate only after all three return.

**Reason**

Both live runs show that the three roles catch different classes of failure. Running them sequentially adds substantial wall-clock time without improving independence. Their isolation matters; their ordering usually does not.

---

## 3. Bound reviewer correction loops

**Target improvement**

Use a convergent review protocol.

### MVP
1. three reviewer reports;
2. one targeted correction pass;
3. one focused verification pass;
4. `PROCEED`, `DO NOT PROCEED`, or human ruling.

### FINAL
1. three reviewer reports;
2. one targeted correction pass;
3. focused verification;
4. human approval.

A new research branch should start only if a reviewer finds a genuinely direction-changing scientific error.

**Reason**

Run 1 approached recursive FINAL review. Run 2 has already required multiple red-team passes. The reviews are valuable, but an autonomous harness must know when it has finished fixing the identified break rather than continuously inventing new work.

---

## 4. Mechanically derive structural truth from executable state

**Target improvement**

Never use comments, scorecards, milestone prose or hand-written evidence as proof of structural properties.

Mechanically verify:

- stage DAG dependencies;
- declared artefacts;
- produced artefacts;
- expectation IDs;
- duplicate IDs;
- cold-start idempotency;
- stage isolation;
- reviewer / gate state.

**Reason**

Run 2 produced a serious failure where the project **claimed the S1→S3 back-edge had been removed while the code still contained it**. A regex edit silently failed, while comments, scorecards and isolation evidence all asserted the opposite.

This is now an earned rule:

> Documentation may describe a structural property, but only executable inspection may prove it.

---

## 5. Add a bidirectional STAGE-MAP ↔ implementation consistency check

**Target improvement**

The framework should mechanically compare:

- every pre-registered stage expectation in `STAGE-MAP`;
- every expectation actually emitted by code;
- every stage that emits each expectation;
- every declared stage output;
- every produced stage output.

It should fail on:

- missing IDs;
- unregistered IDs;
- duplicate IDs;
- unexpected stage ownership;
- stale artefact declarations.

Parent / child IDs such as `E4.4` and `E4.4a/E4.4b` should be handled explicitly rather than heuristically.

**Reason**

Run 2's previous expectation checking was self-referential: each module checked against its own hard-coded ID list. The new cross-check immediately found **9 unregistered IDs and one duplicate expectation**.

The old check could not detect drift away from pre-registration.

---

## 6. Make `UNSCORED`, `SKIPPED`, `ERROR`, `PASS`, and `FAIL` first-class states

**Target improvement**

Expectation and gate states should be structurally distinct.

At minimum:

- `PASS`
- `FAIL`
- `UNSCORED`
- `SKIPPED_ON_FIXTURE`
- `ERROR`

Rules:

- `UNSCORED` can never contribute to pass counts;
- `SKIPPED` can never silently become PASS;
- checker crashes become `ERROR`, never scientific FAIL;
- stale defaults cannot re-score an excluded item.

**Reason**

Run 1 showed a voided criterion could later reacquire PASS through stale scoring logic. Run 2 showed a crashed checker could masquerade as a conjecture violation because missing Python was interpreted as a scientific failure.

The state machine needs to encode these distinctions rather than relying on prose.

---

## 7. Separate checker failure from scientific failure

**Target improvement**

Every harness utility should return explicit machine-readable status:

- checker ran and criterion passed;
- checker ran and criterion failed;
- checker itself crashed / could not execute.

No scientific conclusion may be drawn from the third case.

**Reason**

Run 2's tripwire reported a confirmed-conjecture breach in a repository with zero conjectures because the checker could not launch Python. That is a framework failure, not a project finding.

---

## 8. Resolve the project environment explicitly

**Target improvement**

All harness scripts should resolve and use the project's own environment:

- venv interpreter;
- pytest executable;
- required project packages;
- working directory.

Avoid bare `python`, `pytest`, or shell-environment assumptions.

**Reason**

The same environment bug appeared independently in both live runs. It is therefore clearly generic and should move into the base harness.

---

## 9. Generate verdicts and quantitative narrative from structured artefacts

**Target improvement**

All statements such as:

- `SUPPORTED`
- `WEAKENED`
- `NOT SUPPORTED`
- pillar PASS / FAIL;
- worst error;
- number of supported links;
- number of artefacts;
- number of passing expectations;

should be generated from the same structured evidence used for scoring.

Free-form prose may explain the result, but it may not independently assert the result.

**Reason**

This has failed repeatedly.

### Run 1
Hard-coded report prose contradicted tables and structured outputs.

### Run 2
S7 had hard-coded verdict strings and could emit statements such as:

- a perturbed `3.54 R_sun` result being described as inside a `5.38–9.10 R_sun` acceptance band;
- `a_min = 1.79 au` being narrated as reproducing an `at least 2 au` claim.

This is one of the most serious classes of failure because it allows the final report to tell a different story from the computation.

---

## 10. Never let a test validate itself

**Target improvement**

For each expectation, ask:

> Could this criterion only ever pass because the data were already selected using the same criterion?

Reject self-referential tests.

Examples to prohibit:

- checking accepted segments all satisfy the threshold that defined acceptance;
- checking a derived quantity by dividing it by its own definition;
- checking artefact completeness against a list generated from the same incomplete list;
- checking IDs against a module's own hard-coded IDs rather than the frozen specification.

**Reason**

Both runs exposed vacuous or self-fulfilling checks.

Run 2's E4.4b originally checked χ² on a set already filtered by χ². Once restored to the pre-registered meaning, it failed honestly: **43/70 segments passed**.

The purpose of an expectation is to have diagnostic power, not merely return green.

---

## 11. Stage expectations should test local correctness and identifiability

**Target improvement**

Stage expectations should primarily test:

- structural correctness;
- data validity;
- numerical sanity;
- identifiability;
- stage-boundary reconciliation;
- whether the stage is capable of supporting the downstream inference.

Final paper parity belongs in `ACCEPTABILITY`, not ordinary stage expectations.

**Reason**

Run 1 showed stage expectations could accidentally duplicate final parity or encode the desired sign / result. This makes stage-localisation less meaningful and encourages self-confirmation.

---

## 12. Add independent anchors only where coherent shared-state failure is possible

**Target improvement**

For every materially binding scientific quantity, ask:

> Could the same wrong constant / helper / transform be used everywhere and still make all stages agree?

If yes, add one independently implemented anchor.

The anchor should not share:

- constants;
- transformations;
- helper functions;
- selection logic

with the primary implementation.

**Reason**

Run 1 showed coherent shared-state mutations could propagate through the whole pipeline without detection. The fix does not need duplicate implementations everywhere; it needs independent anchors only where correlated failure can change the conclusion.

---

## 13. Make perturbation tests reach a final scientific verdict

**Target improvement**

The MVP perturbation demo should not merely trigger an intermediate expectation.

At least one deliberately injected fault should:

1. first appear at the correct stage;
2. propagate along the declared DAG;
3. alter a downstream scientific quantity;
4. change a final assessment / verdict where scientifically appropriate.

**Reason**

Run 2's initial perturbation demo localised at S1 but did not affect the final assessment because S7 verdicts were hard-coded. After the fix, the perturbation changed:

- `L1 SUPPORTED → WEAKENED`
- `L2 SUPPORTED → NOT SUPPORTED`

That is a substantially stronger demonstration that the whole system can register a wrong answer.

---

## 14. Keep targeted fault injection, not exhaustive mutation testing

**Target improvement**

Default MVP red-team perturbations should cover:

- one fault per major stage boundary;
- one coherent / shared-state fault;
- one central scientific quantity;
- one project-specific high-risk failure identified at INTAKE.

Do not turn every project into exhaustive mutation testing.

**Reason**

Fault injection has been extremely valuable in both runs, but it can become a major runtime sink. The goal is to prove diagnostic power across representative failure classes, not to prove formal software correctness.

---

## 15. Preserve every correction to a pre-registered expectation visibly

**Target improvement**

When an expectation changes after first execution, preserve:

- original wording;
- corrected wording;
- reason;
- whether the original was malformed, incoherent, or merely inconvenient;
- who / what triggered the correction.

Use simple labels such as:

- `INTAKE-REGISTERED`
- `REVIEW-ADDED`
- `CORRECTED-AFTER-EXECUTION`
- `FINAL-ADDED`

**Reason**

Both runs contained legitimate corrections and dangerous goalpost movement.

Examples:

- Run 2 E0.5: legitimate correction of an off-by-two-day specification.
- Run 2 E5.3: genuine post-hoc goalpost movement toward an observed value.

The framework must preserve enough history for the reviewer to tell those apart.

---

## 16. Never loosen a criterion because the observed answer almost passes

**Target improvement**

Acceptance-band changes must:

- stay inside an INTAKE-set ceiling;
- be logged before re-scoring;
- state the methodological reason;
- never be justified by proximity to the current result.

If no independent reason exists, keep the failure.

**Reason**

Run 2 produced a concrete example where E5.3 was moved to `V ≥ 15.4`, just below the observed `15.48`, and initially recorded only in a code comment. The red team correctly identified this as goalpost movement.

The system needs to make such moves difficult and highly visible.

---

## 17. Make preprocessing sensitivity a first-class output when it is load-bearing

**Target improvement**

If a scientifically important result changes materially under defensible preprocessing choices, report the range rather than presenting one pipeline choice as uniquely determined.

Sensitivity output should identify:

- parameter varied;
- defensible range;
- affected output;
- whether the final scientific verdict changes.

**Reason**

Run 2's A4 result depends strongly on χ² segment filtering.

The honest range became approximately:

**0.67 → 2.45 km/s**

rather than presenting a single value as uniquely determined.

Similarly, the scattered-light result depends strongly on whether deep high-error B-band points survive the frozen quality cut.

This is scientifically useful information, not noise to hide.

---

## 18. Distinguish reproduction, methodological independence, and code exposure

**Target improvement**

For every major result, allow separate labels:

- numerical parity achieved;
- blind methodological reconstruction;
- author-code-exposed;
- author-code-assisted;
- literature-default reconstruction;
- not reproducible from available inputs.

**Reason**

Run 2 accidentally exposed the main agent to some author-code details before the blind-first ruling existed. The project handled this sensibly, but the framework should make the distinction native rather than improvised.

A numerically reproduced result may still be methodologically contaminated.

---

## 19. Keep author-code fallback explicit and narrow

**Target improvement**

When the project selects blind-first:

1. reconstruct independently;
2. score blind result;
3. localise material failure;
4. only then, if intake policy allows, consult author code as a diagnostic;
5. preserve both blind and code-assisted results.

**Reason**

This gives the system access to useful diagnostic evidence without turning replication into a re-run of the authors' implementation.

It also matches realistic production conditions better than pretending author repositories do not exist.

---

## 20. Cold-start evidence must be generated, not asserted

**Target improvement**

Idempotency / isolation evidence should come from an executable generator script that:

- starts from empty output directories;
- runs the relevant stages;
- compares every declared output;
- includes binary artefacts such as PNGs;
- reports the diff mechanically.

Do not allow hand-written JSON / markdown claiming a cold run occurred.

**Reason**

Run 2's earlier isolation evidence was a hand-written assertion with no producer, and a warm run was temporarily passed off as cold because pytest mutated the baseline.

After replacement with a real generator, cold-start equality became genuinely demonstrable.

---

## 21. Tests must not mutate benchmark / baseline evidence

**Target improvement**

System-battery / pytest runs should write only to isolated temp directories.

They must not modify:

- MVP baseline outputs;
- perturbation baselines;
- final scientific artefacts;
- frozen reviewer evidence.

**Reason**

Run 2 found pytest was overwriting the M6 baseline, creating the appearance of a clean comparison when the baseline had already been altered.

---

## 22. Declared figures and artefacts must be mandatory outputs

**Target improvement**

If `STAGE-MAP` declares an artefact, the gate must mechanically verify it exists.

The test should derive required outputs from the frozen declaration, not from a separate manually maintained list.

**Reason**

Run 2 declared seven figures in `STAGE-MAP` but had written no plotting code at all. The original artefact test omitted every PNG, so the gap remained invisible until red-team review.

The new check immediately closes that class of failure.

---

## 23. Keep report claims separated into fact, inference and explanation

**Target improvement**

For material scientific conclusions, use three conceptual levels:

- **OBSERVED** — directly measured or quoted;
- **SUPPORTED INFERENCE** — follows from reproduced evidence;
- **POSSIBLE EXPLANATION** — plausible but not established.

This can be a reporting convention rather than a new ledger.

**Reason**

Run 1 repeatedly produced plausible causal stories that later needed narrowing. The distinction reduces overclaiming without preventing useful interpretation.

---

## 24. Keep scientific failure visible even when the broader conclusion survives

**Target improvement**

The final report should be comfortable with mixed outcomes such as:

- numerical result reproduced;
- stated method failed;
- alternative reconstruction succeeded;
- one supporting inference weakened;
- broader interpretation still plausible.

Do not collapse everything into one project-level PASS / FAIL.

**Reason**

This is one of the strongest behaviours of both runs.

`topdown` had:

- failed literal coefficient reconstruction;
- successful published-formula reproduction;
- successful corrected reconstruction.

ASASSN currently has:

- several strong reproductions;
- multiple well-localised failures;
- interpretation links that are SUPPORTED, WEAKENED, or NOT TESTABLE.

For difficult papers, this is exactly the right output shape.

---

## 25. Keep impossible / unavailable pieces explicitly out of scope

**Target improvement**

If required evidence is unavailable from the supplied project inputs, classify it explicitly rather than silently approximating it.

Possible states:

- NOT AVAILABLE
- NOT REPRODUCIBLE FROM SUPPLIED INPUTS
- OUT OF AGREED SCOPE
- AUTHOR-HELD
- REQUIRES NEW EXTERNAL DEPENDENCY

**Reason**

Run 2 correctly excluded ALMA, SPH and DENIS-dependent pieces instead of inventing substitutes. This behaviour should remain native to the framework.

---

## 26. Keep external benchmark scoring completely separate

**Target improvement**

Continue the current sequence:

1. scientific project complete;
2. FINAL review complete;
3. human approval;
4. repo freeze / tag;
5. fresh read-only extraction;
6. benchmark tasks exposed only after freeze;
7. external score recorded separately.

Extraction prompts should mirror benchmark wording exactly and should not guess which project object the benchmark intends.

**Reason**

Run 1 achieved an honest **3/4 (75%)** result. Keeping the benchmark outside the project prevented the scientific workflow from chasing hidden tolerances.

---

## 27. Keep cost handling thin

**Target improvement**

`COST-PROFILE` should contain only prospective external / metered spend.

Examples:

- paid LLM APIs;
- cloud compute;
- paid storage / egress;
- licensed data;
- hosted services.

If none:

**No external spend planned.**

**Reason**

The first run showed cost accounting could become ceremony around zero-cost local operations. Cost governance is useful; bookkeeping local CPU and free packages is not.

---

## 28. Keep model routing in orchestration, not methodology

**Target improvement**

Add configurable model / effort routing such as:

- strongest model for main scientific reasoning;
- strong domain reviewer;
- cheaper models for mechanical checks;
- smaller models for formatting / extraction;
- configurable use of Fable / equivalent for high-value runs.

Keep this in runtime / orchestration configuration.

**Reason**

Model choice is an execution strategy, not a scientific policy. Mixing it into `COST-PROFILE` or methodology makes the framework harder to reason about.

The current two-run evidence is not yet enough to aggressively downgrade models, so configurability should come before optimisation.

---

## 29. Slim the visible INTAKE without necessarily reducing internal reasoning

**Target improvement**

Aim for:

> **deep internal intake reasoning, thin human-facing contract**

The human should mainly see:

- target;
- material ambiguities;
- stage map;
- acceptance criteria;
- genuine decisions requiring judgment;
- external cost / dependency decisions.

Avoid surfacing every low-level implementation choice as a ruling.

**Reason**

Both runs show that deep intake work is useful, but the volume of files / facts / policies is high. The likely optimisation is not to make the model think less; it is to surface less ceremony when the internal detail does not require human judgment.

---

## 30. Keep the base template clean rather than version-heavy

**Target improvement**

After a run:

- log generic defects;
- finish the project;
- apply accepted fixes to the clean base;
- let the base become the new current state.

Avoid accumulating framework `v2`, `v3`, historical patch layers or project-specific modes unless there is a real external release need.

**Reason**

The goal is a reusable scientific instrument, not a museum of framework history.

---

# Priority order for the next harness iteration

## P0 — correctness / trust

1. Hard MVP block.
2. Mechanical DAG verification.
3. Bidirectional STAGE-MAP ↔ implementation consistency.
4. First-class PASS / FAIL / ERROR / UNSCORED / SKIPPED states.
5. Structured verdict generation.
6. Cold-start / isolation evidence generated mechanically.
7. No test may validate itself.
8. Checker errors separated from scientific failures.
9. Explicit project-environment resolution.

## P1 — review quality / convergence

10. Concurrent isolated reviewers.
11. Bounded review loops.
12. Targeted rather than exhaustive fault injection.
13. Preserve corrected expectation history.
14. Independent anchors for coherent shared-state risks.

## P2 — scientific reporting quality

15. First-class preprocessing sensitivity.
16. Fact vs inference vs explanation.
17. Blind / exposed / code-assisted result labels.
18. Explicit unavailable / out-of-scope states.
19. Mixed scientific outcomes preserved.

## P3 — efficiency / usability

20. Thinner human-facing intake.
21. Minimal cost profile.
22. Configurable model routing.
23. Clean current base rather than version clutter.

---

# What should NOT be redesigned yet

The first two runs still support keeping:

- `INTAKE → MVP → FINAL`;
- human sign-off after INTAKE;
- explicit human FINAL approval;
- frozen direction;
- `CONJECTURES` vs `DIVERGENCES`;
- localise-first;
- three reviewer perspectives;
- blind / code-assisted separation;
- 2× band-relaxation ceiling;
- preservation of failed preregistered routes;
- generic framework with no paper-specific modes.

---

# Overall target for the next iteration

The scientific reasoning is increasingly looking like the strongest part of the system.

The next harness iteration should therefore optimise for:

> **making every claim of correctness mechanically trustworthy, while cutting runtime and review overhead without weakening the adversarial scientific behaviour.**

The goal is **not** to make difficult papers one-shot perfectly.

The goal is to make sure that when the harness cannot reproduce something, it:

- notices;
- localises the failure;
- states what remains unknown;
- resists tuning itself toward the paper;
- and leaves a trustworthy record of what succeeded and what did not.

---

## 31. No load-bearing state claim may exist only in prose

**Target improvement**

Any claim about the current state of the system that can affect trust, gating, localisation or interpretation must be either:

1. **generated directly from executable / structured state**, or
2. **mechanically verified against executable / structured state**.

This applies especially to claims about:

- code edits having applied;
- stage dependencies / DAG edges;
- declared `IN` / `OUT` relationships;
- artefact existence and completeness;
- expectation registration and ownership;
- scorecard provenance;
- cold-start / isolation status;
- gate status;
- final scientific verdicts;
- whether a remediation actually removed the defect it claims to remove.

Comments, markdown, scorecards and remediation notes may explain these properties, but must not be the sole evidence that they are true.

**Reason**

ASASSN exposed the same failure class across three separate red-team passes:

- **Pass 1:** S7 prose said a value was "within the factor-1.3 band" when the computed value was outside that band.
- **Pass 2:** comments, scorecard, perturbation demo and isolation evidence all said the `S1 → S3` back-edge had been removed, while the executable code still contained it because a string replacement silently failed.
- **Pass 3:** the scorecard claimed it had been generated by a producer that did not exist, and claimed all cross-stage reads were declared when several were not.

In each case, the underlying numerical work was reproducible; the failure was that **documentation asserted a property the executable project did not have**.

This is therefore a first-class harness risk, not a one-off documentation problem.

The countermeasure should be structural:

- scorecards generated from artefacts;
- cold-start / isolation evidence generated by scripts;
- DAG / cross-stage reads mechanically inspected;
- pre-registration ↔ implementation checks run bidirectionally;
- verdicts computed from stated tests;
- edits verified after application.

The general rule is:

> **Prose may describe system state; executable evidence must establish it.**

---

## 32. Make load-bearing edits transactional and self-verifying

**Target improvement**

Any automated edit to a load-bearing file should behave like a small transaction:

1. verify the expected pre-edit pattern / state exists;
2. apply the change;
3. assert that exactly the intended change occurred;
4. verify the post-edit invariant;
5. fail loudly if any step does not hold.

For structural changes, the edit should then trigger the relevant mechanical verifier automatically.

Examples:

- changing a stage dependency → rerun DAG/read verification;
- changing expectation IDs → rerun STAGE-MAP ↔ implementation consistency;
- changing verdict logic → rerun affected perturbation / assessment tests;
- changing declared artefacts → rerun artefact completeness;
- removing a code path → verify that the forbidden read/import no longer exists.

**Reason**

ASASSN repeatedly suffered from **silent no-op edits**:

- the attempted removal of the `S1 → S3` back-edge did not match the source and therefore changed nothing;
- later STAGE-MAP edits also silently failed to apply;
- the agent then described those edits as completed because it trusted the intended mutation rather than the observed post-edit state.

An autonomous harness should never infer:

> "I issued the edit, therefore the edit happened."

The correct rule is:

> **An edit is not complete until its postcondition is mechanically demonstrated.**

This is especially important for unattended runs, where there may be no human watching the diff in real time.

