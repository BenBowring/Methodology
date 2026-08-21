# DIVERGENCES — every departure from the paper, classified before it is
# worked around. Append-only; classification changes require the evidence
# that forced them, logged in the entry.
#
# Format, one block per divergence:
#   ## D-<n>: <one-line name>
#   CLASS: FAITHFUL | DEFECT | UNDERSPECIFIED | UNCLASSIFIABLE | FATAL
#     FAITHFUL       — paper-consistent choice; ours differs for stated,
#                      cited reasons (literature anchor wins).
#     DEFECT         — our bug. Link the fix commit when closed.
#     UNDERSPECIFIED — paper silent; state the choice made and its
#                      LIT-DEFAULTS citation (or the ruling/policy id).
#     UNCLASSIFIABLE — blocked; state exactly what would unblock it
#                      (e.g. an equation the paper does not give).
#   BLOCKING: yes | no  (blocking = a gate row depends on it)
#   SUBSTITUTE: yes | no  (yes = a literature stand-in for unavailable
#     author-held material; counts against the pillar's intake-set
#     substitution limit)
#   ATTRIBUTION: the causal chain — which stage owns it (localize
#                first), what evidence establishes that
#   STATUS: OPEN | CLOSED | PERMANENT-OPEN
#     PERMANENT-OPEN is a valid state: parked with its evidence, not
#     forced to a conclusion.

(empty)
