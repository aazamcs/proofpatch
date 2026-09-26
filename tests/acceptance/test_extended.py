"""Post-build checks added during Codex review; original tests remain unchanged."""
import importlib
import os
from datetime import datetime, timezone, timedelta
import pytest

module = importlib.import_module('proofpatch.sample.' + os.environ.get('PROOFPATCH_VARIANT', 'baseline') + '.pagination')


def tasks(n):
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return [{'id': i + 1, 'created_at': start + timedelta(seconds=i // 5)} for i in range(n)]


@pytest.mark.parametrize('page_size', [2, 3, 4])
def test_large_export_never_silently_truncates(page_size):
    records = tasks(401)
    assert [r['id'] for r in module.export_all(records, page_size)] == list(range(1, 402))


def test_unsorted_input_uses_timestamp_then_id():
    records = tasks(17)[::-1]
    assert [r['id'] for r in module.export_all(records, 3)] == list(range(1, 18))


def test_final_page_has_no_next_cursor():
    page, cursor = module.list_tasks(tasks(1), None, 3)
    assert len(page) == 1
    assert cursor is None


def test_exhausted_budget_fails_explicitly():
    with pytest.raises(RuntimeError, match='incomplete'):
        module.export_all(tasks(12), 3, _max_iterations=1)


def test_input_is_not_mutated():
    records = tasks(13)[::-1]
    before = [r.copy() for r in records]
    module.export_all(records, 3)
    assert records == before
