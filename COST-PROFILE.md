# COST-PROFILE — prospective EXTERNAL/metered spend ONLY. Compiled at
# intake, agreed at sign-off, frozen as direction.
#
# Covers: paid LLM/API calls, cloud compute, licensed data, hosted
# services, large storage/egress. Does NOT cover local CPU, free
# packages, or anything unmetered — no bookkeeping of zero-cost
# operations.
#
# If the project needs no external spend, this file's entire content is
# one line: "No external spend planned."
#
# Format otherwise, one block per item:
#   ## COST-<n>: <one-line name>
#   WHAT: what incurs the cost, concretely
#   WHY: why it is needed for the agreed criteria
#   SCALE: expected order of magnitude (currency/period or units)
#   ALTERNATIVE: the cheaper/local option considered, and why it was
#     or wasn't chosen
#
# Standing rule: no new paid dependency, and no material overrun of an
# agreed item's SCALE, without a STOP-AND-ASK escalation first. Actual
# spend against SCALE is summarised in gate digests and the final report.

(empty — written by the intake milestone)
