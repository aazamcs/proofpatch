"""Run a trusted, bundled sample export in a time-limited child process."""
import importlib
import json
import sys
from datetime import datetime
from pathlib import Path


def main():
    variant, page_size = sys.argv[1], int(sys.argv[2])
    if variant not in ('baseline', 'candidate', 'bad_patch') or page_size not in (2, 3, 4):
        raise ValueError('Unsupported selection')
    path = Path(__file__).resolve().parents[1] / 'sample/data/tasks.json'
    records = json.loads(path.read_text())
    for record in records:
        record['created_at'] = datetime.fromisoformat(record['created_at'])
    expected = [r['id'] for r in sorted(records, key=lambda r: (r['created_at'], r['id']))]
    module = importlib.import_module(f'sample.{variant}.pagination')
    actual = [r['id'] for r in module.export_all(records, page_size)]
    print(json.dumps({'expected_ids': expected, 'actual_ids': actual,
                     'missing_ids': [i for i in expected if i not in actual],
                     'duplicate_ids': sorted({i for i in actual if actual.count(i) > 1}),
                     'unexpected_ids': sorted(set(actual) - set(expected)),
                     'matches_expected': actual == expected}))


if __name__ == '__main__':
    main()
