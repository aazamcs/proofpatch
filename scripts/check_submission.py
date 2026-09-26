"""Check local handoff completeness without asserting eligibility or authenticity."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
missing = []
for name in ['README.md', 'LICENSE', 'submission/PITCH.pdf', 'submission/COVER.png', 'submission/DEMO.mp4']:
    if not (root / name).is_file():
        missing.append(name)
links = json.loads((root / 'submission/links.json').read_text())
if not links.get('app_url', '').startswith('https://'):
    missing.append('Public app URL in submission/links.json')
entries = json.loads((root / 'evidence/bob/index.json').read_text()).get('artifacts', [])
if not entries:
    missing.append('Authentic original Bob task/session exports in evidence/bob/index.json')
for item in entries:
    path = (root / 'evidence/bob' / item.get('file', '')).resolve()
    if not path.is_relative_to((root / 'evidence/bob').resolve()) or not path.is_file():
        missing.append('Invalid Bob artifact entry: ' + item.get('file', ''))
print('Local handoff check: ' + ('INCOMPLETE' if missing else 'FILES PRESENT'))
for item in missing:
    print('- ' + item)
print('Manual checks remain: report authenticity, public GitHub/app access, team eligibility, video content and organizer acceptance.')
raise SystemExit(bool(missing))
