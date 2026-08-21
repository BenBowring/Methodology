"""Stage I/O: each stage writes its output to disk in an inspectable
form and can be re-run independently. That is the whole requirement —
enough state to reproduce, inspect, and localize; nothing more.

Path resolution: paths under "artifacts/" are re-rooted to
$ARTIFACTS_ROOT when that env var is set. This is what lets the system
battery and the cold-start check run the pipeline into isolated temp
directories without touching baselines or frozen evidence (tests must
never mutate those).

Optional (per-project choice at intake, for long multi-session work):
pass verify=True to also write/check a small manifest (rows + sha256),
guarding against stale-artefact bugs across sessions."""
import hashlib, json, os, pathlib

ARTIFACTS_PREFIX = "artifacts/"


def resolve(path: str) -> pathlib.Path:
    """Re-root an artifacts/ path under $ARTIFACTS_ROOT if set."""
    root = os.environ.get("ARTIFACTS_ROOT")
    if root and str(path).startswith(ARTIFACTS_PREFIX):
        return pathlib.Path(root) / str(path)[len(ARTIFACTS_PREFIX):]
    return pathlib.Path(path)


def save(df, path: str, verify: bool = False) -> None:
    p = resolve(path); p.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(p)
    if verify:
        m = {"rows": len(df),
             "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
        p.with_suffix(p.suffix + ".manifest.json").write_text(json.dumps(m))


def load(path: str, verify: bool = False):
    import pandas as pd
    p = resolve(path)
    if verify:
        mp = p.with_suffix(p.suffix + ".manifest.json")
        if mp.exists():
            m = json.loads(mp.read_text())
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            if h != m["sha256"]:
                raise RuntimeError(f"stale/modified artefact: {path}")
    return pd.read_parquet(p)
