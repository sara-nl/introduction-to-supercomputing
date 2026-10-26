"""Aggregate exactly the successful average outputs in arguments or a manifest."""

import json
import sys
from pathlib import Path

if sys.argv[1:2] == ["--manifest"]:
    if len(sys.argv) != 3:
        sys.exit("Usage: aggregate.py --manifest selected.json")
    names = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    if (not isinstance(names, list) or not names
            or any(not isinstance(name, str) or not name for name in names)
            or len(set(names)) != len(names)):
        sys.exit("The manifest must contain a nonempty list of distinct output paths")
else:
    names = sys.argv[1:]

if not names:
    sys.exit("No average outputs were selected")
rows = []
for name in names:
    lines = Path(name).read_text().splitlines()
    if len(lines) != 1 or len(lines[0].split(",")) != 2:
        sys.exit(f"Expected one average row in {name}")
    rows.extend(lines)
print("\n".join(sorted(rows)))
