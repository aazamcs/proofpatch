"""Save reproducible CLI run evidence for one bundled variant."""
import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from proofpatch.runner import run_verification, public_report, build_evidence_zip

p = argparse.ArgumentParser()
p.add_argument('--variant', choices=['baseline', 'candidate', 'bad_patch'], default='candidate')
p.add_argument('--page-size', type=int, choices=[2, 3, 4], default=3)
p.add_argument('--output', default='evidence/verification')
args = p.parse_args()
result = run_verification(args.variant, page_size=args.page_size)
dest = Path(args.output)
dest.mkdir(parents=True, exist_ok=True)
name = f'{args.variant}-{args.page_size}'
(dest / f'{name}.json').write_text(json.dumps(public_report(result), indent=2))
(dest / f'{name}.zip').write_bytes(build_evidence_zip(result))
print(result['status'] + ': ' + result['reason'])
expected = {'baseline': 'Defect reproduced', 'candidate': 'Verified against this test suite', 'bad_patch': 'Repair rejected'}
raise SystemExit(0 if result['status'] == expected[args.variant] else 1)
