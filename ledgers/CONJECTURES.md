# CONJECTURES — the guess registry. One of the only two metadata files.
#
# A hypothesis goes here BEFORE anything is built on it. The single rule:
# nothing is premised on a conjecture until its RESULT line is filled by
# an actual run. Carrying an open conjecture as the question behind an
# investigation is fine, for as long as it takes — citing it as a
# premise is the violation.
#
# Format:
#   ## CJ-<n>: <hypothesis, one line>
#   TEST: what run would confirm or kill it
#   RESULT: (empty until the run happens) number/output + command or
#           output path
#   STATUS: OPEN | CONFIRMED | KILLED
# A KILLED conjecture stays. Re-raising it needs new evidence.

(empty)
