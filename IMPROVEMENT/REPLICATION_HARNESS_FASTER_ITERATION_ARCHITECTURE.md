# Replication Harness — Faster Iteration Architecture

## Goal

Reduce end-to-end iteration time without weakening scientific review.

The ASASSN-21qj run took roughly 16 hours. A large part of that came from:

- an excessively long red-team loop;
- repeated re-reading of a very large project state;
- heavyweight verification after small edits;
- reviewers repeatedly inspecting more context than they needed;
- a long-lived main agent carrying too much accumulated history.

The target architecture should make the **artifacts the project state**, not the long-running agent conversation.

## Core principle

> **Use short-lived agents with small evidence slices. Keep the coordinator thin. Parallelise independent work. Re-review only the changed area.**

More sub-agents alone are not enough. If several agents each reread the whole paper, repo, ledgers and report, the harness simply multiplies the expensive part.

The speed gain comes from fresh contexts, sliced evidence, parallelism where dependencies allow, narrow verification, and explicit stage boundaries.

---

## 1. Thin coordinator

The coordinator should know only:

- current stage;
- stage/dependency graph;
- current rulings;
- current claim/verdict status;
- artifact locations;
- which work items are open/closed.

It should **not** need the full scientific history in context.

Its role is orchestration: launch work, pass the right evidence slice, collect structured outputs, decide what runs next, and prevent unnecessary reruns.

---

## 2. Fresh context at each beat

Each major beat should start in fresh context.

Suggested flow:

**INTAKE → BLIND/MVP → PARITY RECOVERY → FINAL → ADJUDICATION**

At the end of each beat, write a compact state artifact that the next beat consumes.

The next agent should not inherit the full conversation history.

Example INTAKE output:

- target claims;
- supplied data;
- paper facts;
- scope;
- evidence boundary;
- acceptance rules;
- stage graph;
- open uncertainties.

BLIND/MVP starts from that artifact, not the entire INTAKE reasoning transcript.

---

## 3. Evidence slicing for sub-agents

Sub-agents should receive only the evidence needed for their task.

Example: an A4 velocity-recovery agent might receive:

- A4 paper claim;
- relevant paper excerpts;
- relevant cited method;
- S3/S4 inputs;
- S4 outputs;
- relevant divergences;
- relevant rulings;
- current diagnostic candidates.

It should **not** receive TESS analysis, A5 scattered-light work, unrelated rulings, the full final report, or the entire review history.

The slice should be generated automatically from claim/stage dependencies where possible.

---

## 4. Sub-agents as investigators, not concurrent repo editors

Parallel sub-agents are useful for:

- diagnosis;
- literature/method lookup;
- alternative-method analysis;
- review;
- parity-recovery hypotheses.

They should normally return **structured findings**, not all edit the repository independently.

One integration agent should apply accepted changes.

This reduces conflicting edits, merge/state inconsistencies, duplicated regeneration, stale prose, and unnecessary verification.

---

## 5. Parallelise independent scientific work

Independent pillars should run in parallel once their inputs are ready.

Example:

```text
                         ┌─ A1 / IR
                         ├─ A3 / eclipse
BLIND/MVP coordinator ───┼─ A4 / velocity
                         ├─ A5 / scattered light
                         └─ A6 / rotation
```

The same applies to parity recovery.

Failed claims can often be investigated independently:

```text
                     ┌─ recover A4
failed claims ───────┼─ recover A5
                     └─ recover timing
```

Their findings are then integrated once.

---

## 6. Parallel FINAL review

For a frozen FINAL candidate, run:

- red team;
- domain expert;
- practitioner;

**in parallel and in strict isolation**.

None should see another reviewer's verdict.

Their findings should then be consolidated into one remediation batch.

Avoid:

> red team → fix → red team → fix → domain → fix → practitioner → fix → red team again

Prefer:

> frozen candidate → three parallel reviews → one remediation batch → targeted closure check

---

## 7. Bound review recursion

Recommended default:

### Pass 1
Full review of the frozen candidate.

### Remediation
Fix all accepted blocking findings together.

### Pass 2
Targeted closure review of:

- previous blockers;
- changed files;
- affected outputs;
- likely regressions.

### Pass 3
Only if a genuinely new blocking defect was introduced by remediation.

Default maximum:

> **Three passes per perspective per gate.**

Further recursion requires explicit human approval.

The aim is adversarial review that **converges**.

---

## 8. Review the delta, not the whole project

After the first full review, later passes should receive:

- previous findings;
- remediation record;
- changed files;
- changed structured outputs;
- relevant regenerated reports;
- regression results.

They should not restart from the entire repository unless the fix was genuinely structural.

A small fix should produce a small review surface.

---

## 9. Dependency-aware verification

Verification should be proportional to the change.

### Presentation-only change

Examples: stale sentence, ruling status, comment, scorecard wording.

Action:

- update presentation;
- run light consistency check.

**Do not rerun science.**

### Report-generator change

Action:

- rerun that generator;
- run its tests.

### Single scientific-stage change

Action:

- rerun that stage;
- rerun downstream dependants only.

### Structural or methodology change

Action:

- broader dependent rebuild.

### Gate closure

Action:

- full battery/cold-start verification.

---

## 10. Cache stable understanding

Stable project understanding should be written once and reused.

Examples:

- parsed paper facts;
- extracted tables;
- figure readings;
- survey/data inventory;
- literature defaults;
- calibration choices;
- data-overlap summaries;
- claim-to-stage mapping.

Agents should not repeatedly rediscover facts that are already established.

---

## 11. Small structured handoffs

Each sub-agent should return a compact structured result such as:

```text
CLAIM: A4
STATUS: RECOVERY_CANDIDATE
FINDING: diameter convention + fine segmentation recovers 7.9 km/s
EVIDENCE:
- paper wording
- diagnostic output
- relevant data behaviour
CONFIDENCE: MULTI-OUTPUT-INFERRED
REQUIRES_CODE_CHANGE: yes
AFFECTED_STAGES:
- S4
- downstream orbital-separation calculation
```

The coordinator can then decide what to do without rereading the whole analysis.

---

## 12. Wall-clock awareness

Agents should have defined jobs, not open-ended instructions like:

> keep reviewing until nothing else can be found.

Each task should have:

- clear deliverable;
- clear scope;
- expected completion condition.

Unexpectedly long tasks should be treated as a signal.

Examples:

- review pass running much longer than normal;
- tiny edit triggering a multi-minute rebuild;
- repeated full-context rereads;
- repeated reruns of unchanged stages.

These should trigger diagnosis rather than become normal behaviour.

---

## 13. Minimal timing log

The harness should record lightweight timing information:

- beat start/end;
- sub-agent start/end;
- stage runtime;
- review runtime;
- number of full-pipeline runs;
- number of targeted reruns;
- number of reviewer passes.

No elaborate telemetry is needed.

Example:

```text
INTAKE              28m
BLIND BUILD         54m
A4                    9m
A5                   14m
PARITY RECOVERY      31m
FINAL REVIEW
  red team           22m
  domain expert      18m
  practitioner       14m
remediation          11m
closure               6m
```

This makes performance regressions visible.

---

## 14. Proposed execution structure

```text
                         ┌─ paper-facts agent
INTAKE coordinator ──────┼─ data agent
                         └─ methods/code agent
                                │
                         compact INTAKE state
                                │
                 ┌──────────────┼──────────────┐
                 ▼              ▼              ▼
              pillar A        pillar B       pillar C ...
                 │              │              │
                 └──────────────┼──────────────┘
                                ▼
                           BLIND/MVP
                                │
                         failed claims only
                                │
                 ┌──────────────┼──────────────┐
                 ▼              ▼              ▼
              recovery A4    recovery A5    recovery ...
                 └──────────────┼──────────────┘
                                ▼
                       integrated candidate
                                │
              ┌─────────────────┼─────────────────┐
              ▼                 ▼                 ▼
           red team        domain expert      practitioner
              └─────────────────┼─────────────────┘
                                ▼
                     one remediation batch
                                ▼
                      targeted closure check
                                ▼
                          adjudication
                                ▼
                         human approval
```

---

## 15. Main architectural shift

The key change is:

> **The long-lived Claude session should stop being the project. The artifacts are the project.**

Agents become short-lived workers.

They:

- receive a narrow state slice;
- do one job;
- return structured findings;
- exit.

This should improve both speed and reasoning quality.

A fresh A4 agent looking only at A4 is less likely to be anchored by many hours of previous reasoning about why the current method was acceptable.

---

## 16. Target behaviour

For a difficult paper, the mature harness should aim for:

- hours rather than a 16-hour continuous run;
- most independent scientific work parallelised;
- one full review pass per perspective;
- one remediation batch;
- one targeted closure pass;
- full rebuild only at meaningful boundaries;
- small, fresh contexts for most agents;
- no repeated rediscovery of stable project facts.

The scientific computation itself was not the main source of the 16-hour runtime.

The major cost was orchestration, accumulated context, repeated verification, and reviewer recursion.

Those are addressable implementation problems.
