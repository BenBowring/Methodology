#!/usr/bin/env bash
# Stage 0 pre-processing: refs/paper.pdf -> refs/paper.md (reading aid)
# and page rasters on demand via scripts/rasterize.py.
#
# The Markdown is a WORKING ARTIFACT, never the anchor. FACT rows cite
# the PDF page/table/equation; where paper.md and the rasterized page
# disagree, the image wins, unconditionally.
#
# Tries Marker if installed (best quality on multi-column + LaTeX);
# otherwise falls back to a plain PyMuPDF text dump with a loud
# degradation warning. The heavy tool is an environment choice, not a
# template requirement.
set -euo pipefail
PDF="refs/paper.pdf"
OUT="refs/paper.md"
[ -f "$PDF" ] || { echo "ERROR: $PDF not found." >&2; exit 1; }

if command -v marker_single >/dev/null 2>&1; then
  echo "extract_paper: using Marker"
  TMP=$(mktemp -d)
  marker_single "$PDF" --output_dir "$TMP" --output_format markdown
  MD=$(find "$TMP" -name "*.md" | head -1)
  { echo "<!-- extracted by Marker $(date -u +%F). Reading aid only:"
    echo "     facts cite the PDF; on disagreement the page image wins. -->"
    cat "$MD"; } > "$OUT"
  rm -rf "$TMP"
else
  echo "extract_paper: Marker not found — degraded fallback (plain text dump)"
  python3 - "$PDF" "$OUT" << 'PYEOF'
import sys
import fitz  # PyMuPDF
pdf, out = sys.argv[1], sys.argv[2]
doc = fitz.open(pdf)
with open(out, "w") as f:
    f.write("<!-- DEGRADED EXTRACTION: plain text dump (Marker not\n"
            "     installed). Treat layout, equations, tables, and\n"
            "     suspicious load-bearing readings with extra caution\n"
            "     and verify against page images where needed.\n"
            "     Reading aid only: facts cite the PDF; on disagreement\n"
            "     the page image wins. -->\n\n")
    for i, page in enumerate(doc, 1):
        f.write(f"\n\n<!-- page {i} -->\n\n")
        f.write(page.get_text())
PYEOF
fi
echo "extract_paper: wrote $OUT"
