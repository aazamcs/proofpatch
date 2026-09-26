from streamlit.testing.v1 import AppTest
from proofpatch.runner import ROOT


def test_app_runs_all_variants_and_clears_stale_result():
    app = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=25).run()
    assert not app.exception
    for variant, expected in [('candidate', 'Verified against this test suite'),
                              ('baseline', 'Defect reproduced'), ('bad_patch', 'Repair rejected')]:
        app.selectbox(key='variant').set_value(variant).run()
        next(b for b in app.button if b.label == 'Run verification').click().run()
        assert not app.exception
        assert app.session_state['result']['status'] == expected
    app.selectbox(key='page_size').set_value(2).run()
    assert 'result' not in app.session_state
    assert not app.exception
