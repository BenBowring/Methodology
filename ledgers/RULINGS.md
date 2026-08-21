# RULINGS — human decisions. Append-only. The agent writes requests;
# only the human writes rulings.
#
# Request format (agent), one block per question:
#   ## R-<n>
#   STATUS: OPEN
#   MODE: STOP-AND-ASK | LOG-AND-CONTINUE (cite POLICIES.md id)
#   QUESTION: one sentence.
#   EVIDENCE: numbers, file paths, references that bear on it.
#   OPTIONS: 2-3 concrete options, one-line consequence each.
#   RECOMMENDATION: one option, one sentence of why.
#
# Ruling format (human), appended inside the same block:
#   RULING: GREEN | RED | <option letter> | free text
#   STATUS: RULED   (edit the block's STATUS line)
#
# Automation halts only on STATUS: OPEN blocks. Gate approvals are
# R-blocks like any other. LOG-AND-CONTINUE entries need no reply —
# they appear in the digest.

(no rulings yet — the first entry in a clone is the intake sign-off)
