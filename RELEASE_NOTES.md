# Reviewed release - 26 September 2026

## Published and deployed
- Source, presentation and narrated demo: https://github.com/aazamcs/proofpatch
- Live app: https://proofpatch-verified.streamlit.app/
- GitHub automated checks passed on Python 3.12: 35 verifier/interface checks and 30 candidate behavior checks.
- Public signed-out testing confirmed all three expected outcomes and all four app tabs.
- Candidate: 30 passed; original: 17 passed / 13 failed; deliberately incorrect repair: 8 passed / 22 failed. Failures in the two controls are expected.

## Impact-focused opening
- Replaced the feature-led opening with “Verify the fix. Before you ship.”
- Revised opening and closing narration, cover and submission headline around the review decision.
- Retained scoped verification claims and the underlying tested implementation.

## Final submission revision
- Revised narration, slides, app explanation and submission text in our team voice.
- Expanded significance, stakeholder value, reproducibility, product positioning and next steps.
- 3 minute 56 second MP4 with AI narration credit, eight-slide PDF/PPTX, transcript and optional captions.
- Added judges evidence map and official requirements map.

## Fixed
- Wrong navbar routes: replaced duplicated navigation with four Streamlit tabs, exercised in the browser.
- Verification without a preserved regression: protected file inventory and hashes plus mandatory test identities now gate results.
- Syntax/collection errors labelled as reproduced: environment failures cannot satisfy the required baseline assertion.
- Missing baseline dependency: every candidate verification executes both baseline and candidate against the same suite.
- In-process export outside the timeout: previews and tests execute in separate bounded child processes.
- Evidence ZIP omissions and stale files: baseline/candidate JUnit XML, complete logs, acceptance tests, fixture, dependencies, config, diff and exact run snapshots are packaged with checksums.
- Silent truncation after 100 pages: repaired export scales its iteration budget with input size; an explicitly exhausted budget raises an error.
- Final-page cursor did not match the contract: completed candidate pages return no next cursor.
- Retired Groq model and API-key friction: removed auxiliary Groq features. Core app requires no credits or credentials.
- Unsupported proof claims: hashes identify bytes; actual chronology and authorship require original evidence.

## Validation scope
- Verifier checks include nine variant/page-size combinations, missing/changed tests, syntax errors, timeout, concurrent runs, checksums and independent archive replay.
- Synthetic original and bad repair intentionally fail behavior checks. Their expected verifier statuses are Defect reproduced and Repair rejected.
- Logs and JSON summaries are in evidence/verification/.

## Remaining team submission steps
Authentic original Bob task/session exports and final organizer submission remain outstanding. Confirm individual registrations and team membership in the event interface. Publication and public deployment are complete; they do not establish eligibility or organizer acceptance.
