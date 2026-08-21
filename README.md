# Replication template

A repeatable, lightweight methodology for replicating a paper or process
with an agent. Clone per project, drop in the paper + a goal, sign off a
tight brief, step away. Heavy at intake, nearly naked in the loop, human
judgment at exactly two gates. The base template is always the current
clean framework — improvements replace it directly; no version clutter.

## The repeatable task
1. `cp -r replication-template <project>/`, `git init`.
2. `refs/paper.pdf` + write `refs/GOAL.md` (one paragraph).
   (Optional: install Marker for best PDF extraction; without it the
   template falls back to a plain dump, where more readings warrant a
   page-image check.)
3. `./scripts/run_beat.sh INTAKE`. Stage 0 extracts the PDF to a
   Markdown reading aid; page images are inspected wherever parsing,
   layout, or figures make the extraction untrustworthy (the PDF is
   the anchor; on disagreement the image wins). Intake reads, scans
   the literature, pins the replication target, compiles the project
   layer — including REGISTRY.json (the frozen structural declaration)
   and the blind evidence boundary — asks its bundled forced-choice
   questions, stops.
4. Sign off: strike/amend, approval in ledgers/RULINGS.md. Direction
   freezes; understanding stays correctable by evidence.
5. `./scripts/run_beat.sh MVP` and step away. Clean MVP auto-continues.

## The five phases
INTAKE (human) -> MVP toy scale (hard mechanical gate, light review,
auto-continue) -> FULL-SCALE BLIND (per-claim results frozen: the
BLIND view) -> PARITY RECOVERY (failed load-bearing claims only,
target-aware, dual-reported) -> FINAL full review + read-only
ADJUDICATION (human approval required).

The MVP's deliverable is diagnostic infrastructure: an end-to-end
modular system in which any divergence is localizable to a stage —
proven by a perturbation that propagates into a changed final verdict.
The blind build measures what can be reconstructed independently;
recovery reconstructs what the authors actually did, from any
legitimate verifiable evidence, and reports it separately. The blind
value is never overwritten. Both frozen views (BLIND, RECOVERED) are
independently benchmarkable; hidden benchmark material is inaccessible
in every phase.

## What keeps it honest (and nothing else)
- Intake rigor: the replication target pinned explicitly and its
  ANCHOR statement (including the blind evidence boundary);
  quote-located facts; cited literature defaults; pre-registered gate
  criteria, bands + ceilings, stage expectations, and REGISTRY.json;
  the external COST-PROFILE agreed up front.
- Two exception rules, zero metadata on ordinary work: guesses ->
  CONJECTURES.md (nothing built on an unfilled RESULT); anchor
  departures -> DIVERGENCES.md (one line, classified, cited).
- Mechanical trust: structural claims verified by
  scripts/verify_structure.py against REGISTRY.json; scorecards and
  verdicts generated from structured evidence
  (scripts/gen_scorecard.py), never hand-written; cold-start evidence
  generated (scripts/cold_start_check.sh), never asserted; result
  states PASS/FAIL/UNSCORED/ERROR with checker crashes never read as
  scientific failures; scoped transactional edits; verification
  proportional to the change.
- Localize first: a bad number is walked back along stage boundaries
  to the first output breaking its expectations.
- Bands: loosenable in small logged steps, never past each metric's
  intake-set ceiling, never justified by proximity to the observed
  value. Reports show initial vs final.
- Substitution limits per pillar; a FATAL divergence marks a pillar
  compromised — scored as failed, not patched.
- Judgment at gates: the same three perspectives (red team, domain
  expert, practitioner) review both gates in PARALLEL and strict
  isolation — light at MVP (trustworthy enough to scale?), full at
  FINAL. One bundled pass each (findings BLOCKING/NON-BLOCKING), one
  remediation batch, one delta-only closure pass; a third pass only
  for remediation-introduced blockers. FINAL requires explicit human
  approval.
- The MVP gate is enforced mechanically: run_beat.sh refuses FULL /
  RECOVERY / FINAL until milestones/reviews/MVP-gate-state.json is
  clean, and refuses RECOVERY / FINAL until the blind freeze exists.

## Layout
CLAUDE.md (standing rules) · REGISTRY.json (frozen structure) ·
PAPER-FACTS.md / ACCEPTABILITY.md / POLICIES.md / COST-PROFILE.md
(intake-compiled) · refs/ (paper, GOAL, LIT-DEFAULTS) · milestones/
(M-INTAKE, MVP-GATE, FINAL-GATE shells, beat-state.md, reviews/) ·
ledgers/ (RULINGS, DIVERGENCES, CONJECTURES, KNOWN-WEAK,
IMPROVEMENT-BACKLOG) · .claude/ (3 skills; red-team + 2 final
perspectives) · scripts/ (run_beat, gate_battery, verify_structure,
gen_scorecard, cold_start_check, extract_paper, rasterize) ·
src/common/ (freeze.py stage I/O, expectations.py result states) ·
timing.log (plain beat/iteration timing).

## Template governance
Process fixes go to the TEMPLATE via a project's IMPROVEMENT-BACKLOG —
update/replace the base directly, remove obsolete machinery, never
patch a running clone. A repeated or material reviewer catch is a
candidate for a mechanical check here (judgment call, no fixed count).
Clean current state beats framework history.
