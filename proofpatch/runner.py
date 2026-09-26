"""Execute a frozen snapshot; require reproduced baseline + unchanged mandatory tests.

This is a verifier for trusted bundled code, not a sandbox for uploaded code.
The release manifest detects changes; it is not a signature or a timestamp proof.
"""
from __future__ import annotations

import difflib
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
import xml.etree.ElementTree as ET
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_VARIANTS = ('baseline', 'candidate', 'bad_patch')
ALLOWED_PAGE_SIZES = (2, 3, 4)
SUBPROCESS_TIMEOUT = 15
STATUS_VERIFIED = 'Verified against this test suite'
STATUS_REPRODUCED = 'Defect reproduced'
STATUS_REJECTED = 'Repair rejected'
STATUS_EXEC_ERROR = 'Execution error'
STATUS_INTEGRITY = 'Evidence integrity check failed'
STATUS_NEEDS_INFO = 'Baseline did not reproduce'
MANIFEST_NAME = 'evidence/frozen_manifest.json'
REGRESSION_ID = 'tests.repro.test_missing_tasks.TestMissingTasksRegression.test_page_size_3_returns_all_ids'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def protected_files(root: Path) -> dict[str, str]:
    paths = [root / p for p in ('conftest.py', 'pyproject.toml', 'spec/expected_behavior.md',
                               'issues/missing_tasks.md', 'sample/data/tasks.json')]
    for directory in ('tests/repro', 'tests/acceptance', 'sample/baseline'):
        paths.extend((root / directory).rglob('*.py'))
    return {p.relative_to(root).as_posix(): sha(p.read_bytes()) for p in sorted(paths) if p.is_file()}


def snapshot_files(root: Path) -> dict[str, bytes]:
    paths = []
    for folder in ('sample', 'proofpatch', 'tests/repro', 'tests/acceptance'):
        paths.extend(p for p in (root / folder).rglob('*') if p.is_file() and p.suffix in ('.py', '.json'))
    paths.extend(root / p for p in ('conftest.py', 'pyproject.toml', 'requirements.txt',
                                  'spec/expected_behavior.md', 'issues/missing_tasks.md', MANIFEST_NAME))
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(paths) if p.is_file()}


def _process(command: list[str], cwd: Path, timeout: float) -> dict:
    # Prevent parent pytest selection/options and third-party plugins changing the suite.
    env = {k: v for k, v in os.environ.items() if not k.startswith(('PYTEST_', 'PROOFPATCH_'))}
    env['PYTEST_DISABLE_PLUGIN_AUTOLOAD'] = '1'
    start = time.monotonic()
    try:
        result = subprocess.run(command, cwd=cwd, env=env, capture_output=True,
                                text=True, timeout=timeout)
        return {'exit_code': result.returncode, 'stdout': result.stdout,
                'stderr': result.stderr, 'seconds': round(time.monotonic() - start, 4)}
    except subprocess.TimeoutExpired as exc:
        def decoded(value):
            return value.decode(errors='replace') if isinstance(value, bytes) else value or ''
        return {'exit_code': -1, 'stdout': decoded(exc.stdout), 'stderr': decoded(exc.stderr),
                'error': f'Process exceeded {timeout:g} seconds',
                'seconds': round(time.monotonic() - start, 4)}
    except OSError as exc:
        return {'exit_code': -1, 'stdout': '', 'stderr': str(exc), 'error': str(exc),
                'seconds': round(time.monotonic() - start, 4)}


def _parse_junit(xml: str) -> dict:
    try:
        root = ET.fromstring(xml)
        cases = []
        for tc in root.iter('testcase'):
            children = [c for c in tc if c.tag in ('failure', 'error', 'skipped')]
            state = children[0].tag if children else 'passed'
            cases.append({'id': f"{tc.get('classname', '')}.{tc.get('name', '')}",
                          'state': state, 'type': children[0].get('type', '') if children else '',
                          'message': children[0].get('message', '') if children else ''})
        if not cases:
            raise ValueError('No test cases in JUnit report')
        counts = {label: sum(c['state'] == state for c in cases)
                  for label, state in [('passed', 'passed'), ('failed', 'failure'),
                                       ('errors', 'error'), ('skipped', 'skipped')]}
        return {'total': len(cases), **counts, 'cases': cases}
    except (ET.ParseError, ValueError) as exc:
        return {'error': str(exc), 'total': 0, 'passed': 0, 'failed': 0, 'errors': 0, 'skipped': 0, 'cases': []}


def _suite(root: Path, variant: str, timeout: float) -> dict:
    # A tiny fixed launcher sets the variant inside the child without inheriting pytest flags.
    launcher = "import os,pytest; os.environ['PROOFPATCH_VARIANT']=" + repr(variant) + "; raise SystemExit(pytest.main(['tests/repro','tests/acceptance','--junitxml=junit-" + variant + ".xml','-v','--tb=short']))"
    result = _process([sys.executable, '-c', launcher], root, timeout)
    xml_path = root / f'junit-{variant}.xml'
    result['xml'] = xml_path.read_text() if xml_path.exists() else ''
    result['junit'] = _parse_junit(result['xml'])
    return result


def _healthy_suite(run: dict, required: list[str]) -> bool:
    j = run['junit']
    ids = [c['id'] for c in j['cases']]
    return (not run.get('error') and not j.get('error') and run['exit_code'] in (0, 1)
            and j['total'] > 0 and j['errors'] == 0 and j['skipped'] == 0
            and len(ids) == len(set(ids)) and sorted(ids) == sorted(required)
            and ((run['exit_code'] == 0) == (j['failed'] == 0)))


def _reproduced(run: dict) -> bool:
    return any(c['id'] == REGRESSION_ID and c['state'] == 'failure'
               and (c['type'].endswith('AssertionError') or c['message'].startswith('AssertionError:'))
               for c in run['junit']['cases'])


def run_verification(variant: str, fixture_id: str = 'main', page_size: int = 3,
                     *, root: Path | None = None, timeout: float | None = None) -> dict:
    root = Path(root or ROOT)
    timeout = SUBPROCESS_TIMEOUT if timeout is None else timeout
    result = {'run_id': str(uuid.uuid4()), 'timestamp': datetime.now(timezone.utc).isoformat(),
              'variant': variant, 'fixture_id': fixture_id, 'page_size': page_size,
              'status': STATUS_EXEC_ERROR, 'reason': '', 'baseline': {}, 'selected': {},
              'export': {}, 'integrity': {}, 'snapshot_hashes': {},
              'limitations': 'Bundled synthetic fixture; verification is limited to this suite. Hashes identify bytes, not authorship or chronology. Human review is required.'}
    if variant not in ALLOWED_VARIANTS or fixture_id != 'main' or type(page_size) is not int or page_size not in ALLOWED_PAGE_SIZES:
        result['reason'] = 'Unsupported variant, fixture or page size.'
        return result
    start = time.monotonic()
    try:
        frozen = json.loads((root / MANIFEST_NAME).read_text())
        actual = protected_files(root)
        expected = frozen['protected_files']
        required = frozen['required_test_ids']
        if not expected or not required or REGRESSION_ID not in required:
            raise ValueError('Incomplete frozen manifest')
        changed = sorted(k for k in set(actual) | set(expected) if actual.get(k) != expected.get(k))
        result['integrity'] = {'matches_frozen_manifest': not changed, 'changed_files': changed,
                               'manifest_sha256': sha((root / MANIFEST_NAME).read_bytes()),
                               'freeze_note': frozen['note']}
        if changed:
            result.update(status=STATUS_INTEGRITY, reason='Protected tests, fixture, specification or baseline changed. Review the change before explicitly creating a new release manifest.')
            return result
        snapshot = snapshot_files(root)
        result['snapshot_hashes'] = {k: sha(v) for k, v in snapshot.items()}
        with tempfile.TemporaryDirectory(prefix='proofpatch-') as td:
            work = Path(td)
            for name, data in snapshot.items():
                path = work / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
            # Close the check/copy race by validating the actual copied bytes too.
            if protected_files(work) != expected:
                result.update(status=STATUS_INTEGRITY, reason='Files changed while creating the run snapshot.')
                return result
            baseline = _suite(work, 'baseline', timeout)
            selected = baseline if variant == 'baseline' else _suite(work, variant, timeout)
            export_run = _process([sys.executable, '-m', 'proofpatch.worker', variant, str(page_size)], work, timeout)
            result['baseline'], result['selected'] = baseline, selected
            if export_run['exit_code'] == 0:
                try:
                    result['export'] = json.loads(export_run['stdout'])
                except json.JSONDecodeError:
                    export_run['error'] = 'Export produced invalid JSON'
            else:
                export_run['error'] = export_run.get('error') or export_run['stderr'] or 'Export process failed'
            result['export_process'] = export_run
            after = snapshot_files(work)
            if after != snapshot:
                result.update(status=STATUS_INTEGRITY, reason='Execution modified the source or test snapshot.')
            elif not _healthy_suite(baseline, required) or not _healthy_suite(selected, required) or export_run.get('error'):
                result.update(status=STATUS_EXEC_ERROR, reason='A required test is missing/skipped, a process failed, or the test environment returned an error. This is not evidence of a reproduced defect.')
            elif not _reproduced(baseline):
                result.update(status=STATUS_NEEDS_INFO, reason='The required regression assertion did not fail on the frozen baseline.')
            elif variant == 'baseline':
                result.update(status=STATUS_REPRODUCED, reason='The unchanged regression assertion fails on the baseline. The preview below uses your selected page size; the complete suite always tests 2, 3 and 4.')
            elif selected['junit']['failed'] or not result['export'].get('matches_expected'):
                result.update(status=STATUS_REJECTED, reason='The repair fails required behavior checks.' + (' This deliberately incorrect negative control was correctly rejected.' if variant == 'bad_patch' else ''))
            else:
                result.update(status=STATUS_VERIFIED, reason='The regression fails on the frozen baseline, the identical mandatory suite passes on this repair, and the selected export matches the expected IDs.')
        result['elapsed_seconds'] = round(time.monotonic() - start, 3)
        result['_snapshot'] = snapshot
        result['patch_diff'] = ''.join(difflib.unified_diff(
            snapshot['sample/baseline/pagination.py'].decode().splitlines(keepends=True),
            snapshot[f'sample/{variant}/pagination.py'].decode().splitlines(keepends=True),
            fromfile='sample/baseline/pagination.py', tofile=f'sample/{variant}/pagination.py'))
        return result
    except (OSError, KeyError, ValueError, TypeError) as exc:
        result.update(status=STATUS_EXEC_ERROR, reason=f'Cannot verify this release: {exc}')
        return result


def public_report(result: dict) -> dict:
    return {k: v for k, v in result.items() if not k.startswith('_')}


def build_evidence_zip(result: dict) -> bytes:
    """Package the exact executed bytes, never reread source after the run."""
    files = {'report.json': json.dumps(public_report(result), indent=2).encode(),
             'patch.diff': result.get('patch_diff', '').encode()}
    lines = ['# ProofPatch run evidence', '', f"Run: {result['run_id']}",
             f"Status: {result['status']}", '', result['reason'], '', result['limitations'], '',
             'The full suite always covers page sizes 2, 3 and 4. The preview uses the selected size.', '',
             '## Re-run', 'Use Python 3.12. From snapshot/:',
             '```', 'python -m pip install -r requirements.txt',
             'PROOFPATCH_VARIANT=baseline python -m pytest tests/repro tests/acceptance',
             f"PROOFPATCH_VARIANT={result['variant']} python -m pytest tests/repro tests/acceptance", '```', '',
             'A failing baseline and a rejected deliberate bad patch are expected.',
             'IBM Bob session exports are separate provenance artifacts under evidence/bob in the project release.']
    files['summary.md'] = '\n'.join(lines).encode()
    for label in ('baseline', 'selected'):
        run = result.get(label, {})
        for field, suffix in [('stdout', 'txt'), ('stderr', 'txt'), ('xml', 'xml')]:
            files[f'logs/{label}-{field}.{suffix}'] = run.get(field, '').encode()
    files.update({f'snapshot/{k}': v for k, v in result.get('_snapshot', {}).items()})
    files['checksums.json'] = json.dumps({k: sha(v) for k, v in files.items()}, indent=2).encode()
    output = io.BytesIO()
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in files.items():
            z.writestr(name, data)
    return output.getvalue()


def freeze_release(root: Path = ROOT) -> dict:
    """Explicit maintainer action after reviewing test/baseline changes; never called by UI."""
    with tempfile.TemporaryDirectory(prefix='proofpatch-freeze-') as td:
        work = Path(td)
        for name, data in snapshot_files(root).items():
            p = work / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
        baseline = _suite(work, 'baseline', SUBPROCESS_TIMEOUT)
        candidate = _suite(work, 'candidate', SUBPROCESS_TIMEOUT)
        required = sorted(c['id'] for c in candidate['junit']['cases'])
        if (not _healthy_suite(baseline, required) or not _healthy_suite(candidate, required)
                or not _reproduced(baseline) or candidate['exit_code'] != 0):
            raise ValueError('Cannot freeze: require complete matching suites, an assertion failure on baseline, and all candidate tests passing.')
    manifest = {'schema_version': 1, 'created_at': datetime.now(timezone.utc).isoformat(),
                'note': 'Release snapshot recorded during post-build hardening. This is not evidence that the original test predates the original repair.',
                'protected_files': protected_files(root), 'required_test_ids': required}
    (root / MANIFEST_NAME).parent.mkdir(parents=True, exist_ok=True)
    (root / MANIFEST_NAME).write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest
