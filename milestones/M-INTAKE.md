# M-INTAKE — project definition compilation (the heavy beat; the only one
# with ceremony). GOAL: paper.pdf + GOAL.md -> the compiled layer + a tight
# brief signed off by the human. No replication work before GREEN.

INPUTS: refs/paper.pdf, refs/GOAL.md.

STAGE 0 — EXTRACTION (automated, before the read)
- Run scripts/extract_paper.sh: refs/paper.pdf -> refs/paper.md (Marker
  if installed; degraded plain-text fallback otherwise, loudly marked).
- refs/paper.md is a READING AID, never the anchor. FACT rows cite the
  PDF page/table/equation. Where the Markdown and the rasterized page
  disagree, the image wins, unconditionally.
- Image verification is TARGETED, not blanket: rasterize and inspect
  pages (scripts/rasterize.py) wherever parsing, layout, equations,
  tables, or figures make the extracted reading untrustworthy, or a
  load-bearing number's parsed form is doubtful. A degraded
  (non-Marker) extraction is a reason for more suspicion — inspect
  the specific doubtful or load-bearing readings it puts in question,
  not everything.

STAGE 1 — READ + SCAN
- Read the paper end to end. PAPER-FACTS.md skeleton: every pillar, every
  stated number the final parity report will score. Quote-located, never
  from memory.
- Literature scan: field-standard options for everything the paper might
  be silent on -> refs/LIT-DEFAULTS.md (claim | citation | one sentence on
  what the citation actually supports).

STAGE 2 — COMPILE (all marked DRAFT until sign-off)
- THE REPLICATION TARGET (mandatory; the first compiled item):
  (a) reproduce a dataset/result from this specific paper;
  (b) reproduce the paper's overall methodology;
  (c) reproduce a broader result/phenomenon from the literature;
  (d) use the paper as a starting point for a narrower stated objective.
  If GOAL.md does not make this unambiguous, it is a DIRECT question in
  Stage 3 — never assumed.
- THE ANCHOR STATEMENT (derived from the target): what is authoritative
  vs comparative; how paper-vs-literature conflicts resolve; and the
  BLIND EVIDENCE BOUNDARY — the admissible sources for the blind build
  (default: paper, supplied data, cited literature/methods, public
  technical documentation needed to use those inputs; author code and
  implementation material excluded — their only role is in parity
  recovery, after the blind freeze). Hidden benchmark material is
  inaccessible in every phase, always.
- The stage map, in two forms:
  (1) PROSE (here): the pipeline decomposed into src/ modules, chosen
      for DIAGNOSTIC value — boundaries placed where divergences will
      need to be localized. Per stage: its expectations, worded — the
      checkable properties that give the stage diagnostic power (would
      this catch the stage failing locally? typical angles: sanity,
      reconciliation, identifiability — a principle, not a per-stage
      checklist). No expectation may be satisfiable purely because the
      data were already selected by the same criterion. Final paper
      parity lives in ACCEPTABILITY, not stage expectations.
      Post-registration changes are recorded here in place: original
      wording, new wording, reason, trigger — no classification.
  (2) REGISTRY.json (frozen structural declaration): per stage — id,
      module, deps, shipped/load-bearing artifacts, expectation IDs.
      Exactly those four structural facts; verified mechanically by
      scripts/verify_structure.py forever after.
- MVP-GATE.md and FINAL-GATE.md: pre-registered criteria (see shells).
- ACCEPTABILITY.md: standard (default ballpark-defensible), per-pillar
  metric | band + loosening ceiling (in the metric's own units) |
  evidence form; THE LOAD-BEARING CLAIM SET (the pillar claims — the
  only claims eligible for parity recovery); which pillars need a
  preprocessing-sensitivity range as evidence; the final-gate claim
  sentence; the abandonment line.
- POLICIES.md: the log-and-continue list. Aggressive is what buys
  hands-off runs.
- Per-pillar SUBSTITUTION LIMITS.
- COST-PROFILE.md: prospective external/metered spend only. If none:
  "No external spend planned." — one line.
- PERTURBATION PLAN: no fixed count. Minimum one meaningful fault that
  propagates from its stage into a changed final verdict; add more
  only where this project's structure/risk earns them (shared-state
  exposure, a central quantity, an intake-identified failure class).
- The domain-risk focus appended to
  .claude/agents/bench/domain-expert.md, cited.
- PROPORTIONALITY: scale the whole compile to the goal. A small
  reproduce-and-move-on job gets a short stage map, thin expectations,
  red team only at final, a wide POLICIES list. No cathedral for a shed.

STAGE 3 — INTERROGATE
Deep internal reasoning, thin human-facing contract. Forced-choice
questions with recommendations, bundled in ONE stop, as R-blocks. The
human sees: target, material ambiguities, stage map, acceptance
criteria, genuine judgment calls, external cost/dependency decisions —
not low-level implementation choices (those resolve via
POLICIES/LIT-DEFAULTS). Never ask what GOAL.md or the paper already
answers.

HUMAN GATE: strike/amend; approval freezes PAPER-FACTS (shell), the
stage map + REGISTRY.json, gate criteria, ACCEPTABILITY (incl.
load-bearing set), POLICIES, COST-PROFILE, the blind boundary, and the
domain-risk focus. Write milestones/beat-state.md (NEXT: MVP).

## WORKLOG
(empty)
