"""ProofPatch judge-facing verifier. No model credentials or network API calls."""
from pathlib import Path
import json
import streamlit as st
from proofpatch.runner import (run_verification, public_report, build_evidence_zip,
                               STATUS_VERIFIED, STATUS_REPRODUCED, STATUS_REJECTED)

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='ProofPatch | Fix bugs. Show proof.', page_icon='🔬', layout='wide')
st.markdown('''<style>
.block-container {max-width:1160px;padding-top:4.5rem;padding-bottom:3rem}
h1 {letter-spacing:-.045em;font-size:3.5rem!important}
h2,h3 {letter-spacing:-.02em}
[data-testid="stMetric"] {background:#1b2030;border-radius:12px;padding:16px}
.intro {font-size:1.15rem;line-height:1.6;color:#bac3dc;max-width:830px}
.brand {color:#9aa7ff;letter-spacing:.14em;font-size:.78rem;font-weight:700}
</style>''', unsafe_allow_html=True)
st.markdown('<div class="brand">IBM BOB 2.0 HACKATHON · DEVELOPER WORKFLOW</div>', unsafe_allow_html=True)
st.title('ProofPatch')
st.markdown('<p class="intro"><strong>Fix bugs. Show proof.</strong><br>A repair should come with a failing baseline, unchanged tests, and evidence a reviewer can rerun.</p>', unsafe_allow_html=True)
st.caption('Synthetic pagination case · Real pytest execution · No API keys required')

verify, evidence, workflow, handoff = st.tabs(['Run verification', 'Inspect evidence', 'Bob workflow', 'Project & submission'])
labels = {'baseline': 'Original defect', 'candidate': 'Repaired candidate', 'bad_patch': 'Deliberately incorrect repair'}

with verify:
    st.subheader('Can the repair earn a verified result?')
    st.write('The original export skips task 4 at a timestamp tie. The repair uses a timestamp-and-ID cursor. The deliberately incorrect repair repeats records.')
    left, middle, right = st.columns([2, 1, 2], vertical_alignment='bottom')
    with left:
        variant = st.selectbox('Implementation', list(labels), format_func=labels.get, index=1, key='variant')
    with middle:
        page_size = st.selectbox('Preview page size', [2, 3, 4], index=1, key='page_size')
    with right:
        run = st.button('Run verification', type='primary', width='stretch')
    st.caption('Every run checks the full mandatory suite, including page sizes 2, 3 and 4. The selector changes the separate export preview.')
    selection = (variant, page_size)
    if st.session_state.get('selection') != selection:
        st.session_state.pop('result', None)
        st.session_state['selection'] = selection
    if run:
        with st.spinner('Checking integrity, reproducing the baseline and testing the selected version…'):
            st.session_state['result'] = run_verification(variant, page_size=page_size)
    r = st.session_state.get('result')
    if not r:
        a, b, c = st.columns(3)
        with a:
            st.markdown('**1 · Reproduce**')
            st.write('The known regression assertion must fail on the frozen original.')
        with b:
            st.markdown('**2 · Verify**')
            st.write('The same complete test suite must pass on the repair.')
        with c:
            st.markdown('**3 · Review**')
            st.write('Download exact source snapshots, test reports and the patch.')
    else:
        status = r['status']
        if status == STATUS_VERIFIED:
            st.success(status)
        elif status == STATUS_REPRODUCED:
            st.warning(status)
        else:
            st.error(status)
        st.write(r['reason'])
        if variant == 'bad_patch' and status == STATUS_REJECTED:
            st.info('Negative control succeeded: the verifier rejected our deliberately incorrect repair.')
        j = r.get('selected', {}).get('junit', {})
        a, b, c, d = st.columns(4)
        for col, label, val in [(a, 'Tests executed', j.get('total', 0)), (b, 'Passed', j.get('passed', 0)),
                                (c, 'Failed / errors', f"{j.get('failed', 0)} / {j.get('errors', 0)}"),
                                (d, 'Run time', f"{r.get('elapsed_seconds', 0):.2f}s")]:
            col.metric(label, val)
        exp = r.get('export', {})
        st.markdown('#### Selected export preview')
        if exp:
            col1, col2 = st.columns(2)
            col1.write('**Expected task IDs**')
            col1.code(str(exp['expected_ids']), language=None)
            col2.write('**Actual task IDs**')
            actual = exp['actual_ids']
            col2.code(str(actual[:30]) + (f' … ({len(actual)} total)' if len(actual) > 30 else ''), language=None)
            if exp['matches_expected']:
                st.success('This preview returns all expected tasks once, in order.')
            else:
                st.warning(f"Missing: {exp['missing_ids']} · Repeated IDs: {exp['duplicate_ids']} · Unexpected: {exp['unexpected_ids']}")
        else:
            st.warning('No valid export result was produced. No correctness claim is made.')
        st.download_button('Download this run’s evidence ZIP', build_evidence_zip(r),
                           file_name=f"proofpatch-{variant}-{r['run_id'][:8]}.zip", mime='application/zip',
                           type='primary', width='stretch')
        st.caption('Includes exact executed source and tests, baseline and selected JUnit XML, complete logs, patch.diff, report.json and checksums.')
        with st.expander('Integrity checks and exact test outcomes'):
            st.json(r.get('integrity', {}))
            if j.get('cases'):
                st.dataframe(j['cases'], width='stretch', hide_index=True)
        for name in ('baseline', 'selected'):
            with st.expander(f'{name.capitalize()} execution log'):
                st.code(r.get(name, {}).get('stdout', 'No output'), language=None)
                if r.get(name, {}).get('stderr'):
                    st.code(r[name]['stderr'], language=None)
        st.caption(r['limitations'])

with evidence:
    st.subheader('Evidence you can inspect and rerun')
    st.write('Downloaded evidence comes from the same isolated snapshot that was executed. The release manifest rejects changed or missing protected files before tests begin.')
    r = st.session_state.get('result')
    if r:
        st.markdown('**Patch tested in the current run**')
        st.code(r.get('patch_diff', 'No diff available'), language='diff')
        with st.expander('Full machine-readable report'):
            st.json(public_report(r))
    else:
        st.info('Run verification first to inspect a diff bound to an actual execution.')
    file_choices = ['issues/missing_tasks.md', 'spec/expected_behavior.md', 'sample/data/tasks.json',
                    'sample/baseline/pagination.py', 'sample/candidate/pagination.py',
                    'sample/bad_patch/pagination.py', 'tests/repro/test_missing_tasks.py',
                    'tests/acceptance/test_acceptance.py', 'tests/acceptance/test_extended.py']
    selected_file = st.selectbox('Browse bundled project files', file_choices)
    st.code((ROOT / selected_file).read_text(), language='python' if selected_file.endswith('.py') else None)
    st.markdown('**What the hashes establish**')
    st.write('They identify the tested bytes and detect differences from this release’s frozen manifest. They do not establish when a test was originally authored, who wrote it, or correctness outside the suite. The current manifest was created during post-build review.')

with workflow:
    st.subheader('IBM Bob works in the local repository')
    st.write('We used IBM Bob during our original development. Our reusable Bob skill organizes the repair workflow around reproduction, preserved tests, verification and evidence. After using our allocated credits, we continued improving and testing the project locally. The app runs the verification stage independently. Our development tools and contributions are documented in PROVENANCE.md.')
    steps = [
        ('Understand', 'Read the issue and behavioral contract; identify the faulty flow.'),
        ('Clarify', 'If expected behavior is missing, ask a focused question before changing code.'),
        ('Reproduce', 'Write an observable regression assertion and run it on the original.'),
        ('Preserve', 'Save the failing run and reviewed test snapshot before a new repair attempt.'),
        ('Repair', 'Change candidate code while retaining protected tests and baseline.'),
        ('Verify', 'Run the same mandatory suite on baseline and candidate; reject incomplete evidence.'),
        ('Package', 'Export the tested snapshots, patch and execution reports for human review.')]
    for i, (title, detail) in enumerate(steps, 1):
        st.markdown(f'**{i}. {title}** — {detail}')
    with st.expander('Reusable Bob skill'):
        st.code((ROOT / '.bob/skills/proofpatch/SKILL.md').read_text(), language='markdown')
    st.markdown('#### Original Bob session artifacts')
    index_path = ROOT / 'evidence/bob/index.json'
    entries = json.loads(index_path.read_text()).get('artifacts', []) if index_path.exists() else []
    if not entries:
        st.warning('Our original Bob session exports are a separate submission attachment; they have not yet been added to this local package.')
    for entry in entries:
        path = (ROOT / 'evidence/bob' / entry['file']).resolve()
        if path.is_relative_to((ROOT / 'evidence/bob').resolve()) and path.is_file():
            st.download_button(entry.get('label', path.name), path.read_bytes(), path.name, key='bob_' + path.name)

with handoff:
    st.subheader('A practical review workflow for small teams')
    st.write('ProofPatch targets developers and reviewers who need to establish what failed, what changed, and what actually passed. The prototype automates evidence collection around one disclosed defect. It is not a general autonomous bug fixer.')
    st.markdown('**Team:** Mohammad Aazam · Mirza Yasir Abdullah Baig · Faza E Badar')
    st.link_button('Public GitHub repository', 'https://github.com/aazamcs/proofpatch')
    st.caption('Our latest local release is ready for publication at this repository.')
    st.markdown('**Measured value:** one run collects paired baseline/repair results and a complete evidence bundle. Run duration is displayed from actual execution. No unmeasured time-saving percentage is claimed.')
    st.markdown('**Scope:** trusted bundled Python code, one synthetic defect, three variants. A real repository adapter and CI integration are future work.')
    st.markdown('**Submission handoff:** see `START_HERE.md` and `submission/CHECKLIST.md` in the release. They guide our final evidence attachments, deployment and submission.')

st.divider()
st.caption('ProofPatch · Tested behavior, reviewable evidence · Human approval remains part of the workflow')
