"""Rasterize PDF pages to high-resolution PNGs for vision verification.
Usage: python scripts/rasterize.py <page> [<page> ...]   (1-indexed)
Writes refs/pages/page-<n>.png at 300 DPI. Cached: existing files are
kept. When an extracted reading is checked, doubtful, layout-sensitive,
or contested, the page image is the authoritative source."""
import sys, pathlib
import fitz  # PyMuPDF

PDF = pathlib.Path("refs/paper.pdf")
OUTDIR = pathlib.Path("refs/pages")

def main() -> None:
    if not PDF.exists():
        sys.exit("ERROR: refs/paper.pdf not found")
    OUTDIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)
    for arg in sys.argv[1:]:
        n = int(arg)
        out = OUTDIR / f"page-{n}.png"
        if out.exists():
            print(f"cached: {out}")
            continue
        page = doc[n - 1]
        pix = page.get_pixmap(dpi=300)
        pix.save(out)
        print(f"wrote: {out}")

if __name__ == "__main__":
    main()
