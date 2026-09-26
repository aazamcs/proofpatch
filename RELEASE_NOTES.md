# Reviewed release - 26 September 2026

## Impact-focused opening
- Replaced the feature-led opening with “Verify the fix. Before you ship.”
- Revised opening and closing narration, cover and submission headline around the review decision.
- Retained scoped verification claims and the underlying tested implementation.

## Final submission revision
- Revised narration, slides, app explanation and submission text in our team voice.
- Expanded significance, stakeholder value, reproducibility, product positioning and next steps.
- 3 minute 56 second MP4 with AI narration credit, eight-slide PDF/PPTX, transcript and optional captions.
- Added judges evidence map and official requirements map.
- Re-ran all 35 verifier and interface checks successfully in 20.96 seconds.

## Fixed
- Wrong navbar routes such as /1_Verifier: replaced duplicated navigation with four Streamlit tabs, exercised in the browser.
- Verification without a preserved regression: protected file inventory and hashes plus mandatory test identities now gate results.
- Syntax/collection errors labelled as reproduced: environment failures cannot satisfy the required baseline assertion.
- Missing baseline dependency: every candidate verification now executes both baseline and candidate against the same suite.
- In-process export outside the timeout: previews and tests execute in separate bounded child processes.
- Evidence ZIP omissions and stale files: full baseline/candidate JUnit XML, complete logs, acceptance tests, fixture, dependencies, config, diff and exact run snapshots are packaged with checksums.
- Silent truncation after 100 pages: repaired export scales its iteration budget with input size; an explicitly exhausted budget raises an error.
- Final-page cursor did not match the contract: completed candidate pages return no next cursor.
- Retired Groq model and API-key friction: removed the auxiliary Groq features. Core app requires no credits or credentials.
- Unsupported proof claims: hashes identify bytes; actual chronology and authorship require original evidence.

## Validation
- 30 candidate behavior checks pass.
- 35 verifier and interface checks pass, including nine variant/page-size combinations, missing/changed tests, syntax errors, timeout, concurrent runs, checksums and independent archive replay.
- Browser checks: candidate verification; deliberate bad repair rejection; all four navigation tabs.
- After a small layout adjustment, the interface regression check passed again.
- Synthetic original and bad repair intentionally fail their behavior checks. Their expected verifier statuses are Defect reproduced and Repair rejected.
- Logs and JSON summaries are in evidence/verification/.

## Still external to this release
Authentic original Bob task/session exports, publishing to GitHub, public deployment and final organizer submission. The provided repository was public but empty during inspection. The release is ready for deployment testing; hosted availability and event acceptance are not established by local checks.
