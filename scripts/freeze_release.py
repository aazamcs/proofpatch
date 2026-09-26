"""Explicitly record reviewed tests and baseline as a new release snapshot."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from proofpatch.runner import freeze_release

if '--confirm-reviewed' not in sys.argv:
    raise SystemExit('Review all test, fixture and baseline changes first. Then pass --confirm-reviewed. This records current bytes; it cannot establish original authorship or chronology.')
manifest = freeze_release()
print(f"Frozen {len(manifest['protected_files'])} protected files and {len(manifest['required_test_ids'])} mandatory tests.")
