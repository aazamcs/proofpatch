"""Checks of the verifier itself, independent of the intentionally failing baseline."""
import io
import json
import os
import shutil
import subprocess
import sys
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import pytest
from proofpatch import runner as r


@pytest.fixture
def project(tmp_path):
    for name, data in r.snapshot_files(r.ROOT).items():
        p = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)
    return tmp_path


@pytest.mark.parametrize('variant,status', [('baseline', r.STATUS_REPRODUCED), ('candidate', r.STATUS_VERIFIED), ('bad_patch', r.STATUS_REJECTED)])
@pytest.mark.parametrize('page_size', [2, 3, 4])
def test_matrix(variant, status, page_size):
    result = r.run_verification(variant, page_size=page_size)
    assert result['status'] == status, result['reason']
    assert result['selected']['junit']['total'] == 30


@pytest.mark.parametrize('name', ['tests/repro/test_missing_tasks.py', 'tests/acceptance/test_acceptance.py',
                                 'sample/baseline/pagination.py', 'sample/data/tasks.json'])
@pytest.mark.parametrize('operation', ['delete', 'change'])
def test_protected_changes_block_verification(project, name, operation):
    path = project / name
    if operation == 'delete':
        path.unlink()
    else:
        path.write_text(path.read_text() + '\n# changed\n')
    result = r.run_verification('candidate', root=project)
    assert result['status'] == r.STATUS_INTEGRITY
    assert name in result['integrity']['changed_files']


def test_added_test_blocks_until_review(project):
    (project / 'tests/repro/test_added.py').write_text('def test_added(): assert True\n')
    assert r.run_verification('candidate', root=project)['status'] == r.STATUS_INTEGRITY


def test_candidate_syntax_error_is_execution_error(project):
    (project / 'sample/candidate/pagination.py').write_text('invalid python !!!')
    assert r.run_verification('candidate', root=project)['status'] == r.STATUS_EXEC_ERROR


def test_hung_candidate_is_bounded(project):
    path = project / 'sample/candidate/pagination.py'
    path.write_text(path.read_text() + '\ndef export_all(*a, **k):\n    while True: pass\n')
    result = r.run_verification('candidate', root=project, timeout=1)
    assert result['status'] == r.STATUS_EXEC_ERROR
    assert result['selected'].get('error')
    assert result['export_process'].get('error')
    assert result['elapsed_seconds'] < 5


@pytest.mark.parametrize('xml', ['', '<testsuites/>', '<testsuite tests="0"/>'])
def test_no_test_report_cannot_pass(xml):
    parsed = r._parse_junit(xml)
    assert parsed['error']
    assert not r._healthy_suite({'junit': parsed, 'exit_code': 0}, [])


@pytest.mark.parametrize('state', ['error', 'skipped'])
def test_errors_and_skips_cannot_pass(state):
    j = r._parse_junit(f'<testsuite><testcase classname="a" name="b"><{state}/></testcase></testsuite>')
    assert not r._healthy_suite({'junit': j, 'exit_code': 0}, ['a.b'])


def test_inconsistent_exit_code_cannot_pass():
    j = r._parse_junit('<testsuite><testcase classname="a" name="b"/></testsuite>')
    assert not r._healthy_suite({'junit': j, 'exit_code': 2}, ['a.b'])
    assert not r._healthy_suite({'junit': j, 'exit_code': 1}, ['a.b'])
    assert not r._healthy_suite({'junit': j, 'exit_code': 0}, ['a.b', 'a.missing'])


def test_missing_manifest_is_error(project):
    (project / r.MANIFEST_NAME).unlink()
    assert r.run_verification('candidate', root=project)['status'] == r.STATUS_EXEC_ERROR


def test_snapshot_modification_during_execution_is_blocked(project):
    path = project / 'sample/candidate/pagination.py'
    path.write_text(path.read_text() + '\nfrom pathlib import Path\nPath(__file__).write_text(Path(__file__).read_text() + "\\n# changed during run\\n")\n')
    assert r.run_verification('candidate', root=project)['status'] == r.STATUS_INTEGRITY


def test_zip_is_exact_complete_and_rerunnable(project, tmp_path):
    result = r.run_verification('candidate', root=project)
    original = (project / 'sample/candidate/pagination.py').read_bytes()
    (project / 'sample/candidate/pagination.py').write_text('# changed after execution')
    z = zipfile.ZipFile(io.BytesIO(r.build_evidence_zip(result)))
    assert z.read('snapshot/sample/candidate/pagination.py') == original
    checksums = json.loads(z.read('checksums.json'))
    assert all(r.sha(z.read(name)) == digest for name, digest in checksums.items())
    for name in ['logs/baseline-xml.xml', 'logs/selected-xml.xml', 'patch.diff',
                 'snapshot/tests/acceptance/test_acceptance.py', 'snapshot/conftest.py',
                 'snapshot/sample/data/tasks.json', 'snapshot/requirements.txt']:
        assert name in z.namelist()
    replay = tmp_path / 'replay'
    z.extractall(replay)
    env = dict(os.environ, PROOFPATCH_VARIANT='candidate', PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    proc = subprocess.run([sys.executable, '-m', 'pytest', 'tests/repro', 'tests/acceptance'],
                          cwd=replay / 'snapshot', env=env, capture_output=True, text=True, timeout=15)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_parallel_runs_are_isolated():
    with ThreadPoolExecutor(max_workers=2) as pool:
        a, b = list(pool.map(r.run_verification, ['baseline', 'candidate']))
    assert a['run_id'] != b['run_id']
    assert a['status'] == r.STATUS_REPRODUCED
    assert b['status'] == r.STATUS_VERIFIED


@pytest.mark.parametrize('kwargs', [{'variant': '../other'}, {'variant': 'candidate', 'page_size': 0},
                                   {'variant': 'candidate', 'page_size': True}, {'variant': 'candidate', 'fixture_id': '../x'}])
def test_invalid_inputs(kwargs):
    assert r.run_verification(**kwargs)['status'] == r.STATUS_EXEC_ERROR
