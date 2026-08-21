# BEAT-STATE — the compact handoff between beats. The artefacts are
# the project; this file is what a fresh context reads first instead
# of inheriting conversation history. Rewritten (not appended) at the
# end of every beat by the coordinator. Keep it under a page.
#
# Format:
#   CURRENT: INTAKE | MVP | FULL | RECOVERY | FINAL
#   NEXT:    the beat that should run next
#   ## Summary
#   Target + anchor in two lines. Where the build stands. What is
#   frozen. Open items (one line each, pointing at the ledger entry
#   or artefact — never restating it).
#   ## Pointers
#   The artefacts a fresh context needs: REGISTRY.json, gate specs,
#   scored results, open divergences/conjectures, latest reviews.

CURRENT: INTAKE
NEXT: INTAKE

## Summary
(fresh clone — intake not yet run)

## Pointers
refs/GOAL.md, refs/paper.pdf
