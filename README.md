# ProofPatch
## Fix bugs. Show proof.

A reproducible verification workflow for AI-assisted repairs, built for the IBM Bob 2.0 Hackathon. The live app executes trusted bundled Python code; no AI service or API key is required.

A pagination export drops task 4 when records share timestamps. ProofPatch connects a baseline assertion failure to a candidate repair, checks that mandatory tests and inputs are unchanged, and creates a rerunnable evidence package. A deliberately incorrect repair demonstrates rejection.

### Quick start
Python 3.12 is the tested runtime.
```sh
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
See START_HERE.md for virtual environments and Windows setup.

### Verification commands
```sh
python -m pytest tests/system
PROOFPATCH_VARIANT=candidate python -m pytest tests/repro tests/acceptance
python scripts/verify.py --variant baseline
python scripts/verify.py --variant candidate
python scripts/verify.py --variant bad_patch
```
The three CLI verifier commands return success when their intended outcomes occur. Raw pytest on the baseline or bad patch intentionally fails. `python -m pytest` defaults to verifier system tests, so routine project checks can finish green. On PowerShell set `$env:PROOFPATCH_VARIANT="candidate"` before the raw pytest command.

### Verification contract
1. Compare protected baseline, fixture, specification, regression and acceptance files with the release manifest.
2. Copy source, tests and configuration into a fresh temporary directory. Validate copied protected bytes.
3. Execute the entire mandatory suite on baseline and selected variant in bounded subprocesses.
4. Require the known regression ASSERTION to fail on baseline. Reject collection errors, zero tests, missing test identities, skipped checks and inconsistent exit codes.
5. Require the candidate suite to pass and the selected export preview to match the expected IDs.
6. Check that execution did not modify snapshot files. Package those exact bytes rather than rereading live project files.

The full suite always covers preview sizes 2, 3 and 4. Page size changes the independent ID preview only. Each subprocess has a 15-second limit; one candidate verification can take roughly 45 seconds in a worst-case sequence of timed-out children. The web UI is synchronous during a run.

### Evidence contents
report.json, summary.md, patch.diff, full baseline and selected stdout/stderr, JUnit XML, checksums.json, and snapshot/ containing all executable sample code, regression and acceptance tests, fixture, conftest.py, configuration, requirements and frozen manifest. Run summary.md instructions from snapshot/ to reproduce the checks.

`evidence/verification/` contains release checks generated locally. They are real execution reports, not IBM Bob session reports. Actual Bob exports belong in `evidence/bob/`.

### Integrity limits
The manifest detects accidental or unreviewed changes relative to a local reference. A maintainer who changes both manifest and files can change that reference. SHA-256 hashes are not signatures, authorship proof, or trusted timestamps. This release manifest was created after the original build. Original Bob provenance must be established with the team's actual session artifacts.

If tests or baseline intentionally change, review the changes and then explicitly run:
```sh
python scripts/freeze_release.py --confirm-reviewed
```
Never regenerate the manifest just to bypass a failed integrity check. Creating a new manifest requires a complete matching suite, a reproduced baseline assertion and a passing candidate. Existing evidence remains bound to its own snapshot.

### Layout
- app.py: one-page judge interface with four tabs
- proofpatch/runner.py: snapshot, execution, result classification and ZIP assembly
- proofpatch/worker.py: bounded export preview worker
- sample/: original, repaired and deliberately incorrect variants
- tests/repro/: original regression assertions, preserved from the supplied ZIP
- tests/acceptance/: original acceptance tests plus disclosed post-build edge cases
- tests/system/: tests of the verifier, packaging and UI
- .bob/skills/proofpatch/SKILL.md: reusable local Bob workflow
- submission/: pitch, cover, copy, demo script and publishing checklist

### Deployment
Publish this folder's contents at https://github.com/aazamcs/proofpatch, preserving hidden folders. Use Streamlit Community Cloud with entrypoint `app.py`, Python 3.12, and the included requirements.txt. No secrets are required. See DEPLOYMENT.md.

### Scope and limitations
The dataset is synthetic and the bad patch is an intentional negative control, used to test rejection. The verifier accepts only bundled variants; it is not an execution sandbox for arbitrary uploads. The repaired pagination code assumes unique integer IDs and comparable datetime values. It reads an in-memory dataset and is not a production database adapter. Performance and commercial benefits beyond observed local runs remain hypotheses.

We used IBM Bob during our original development. After our allocated credits were consumed, we continued local engineering and testing with Codex assistance. See PROVENANCE.md for the contribution record. MIT license applies to the team's original project code; dependency licenses remain their own.
