# Our submission text

## Project title
ProofPatch — Verify the fix. Before you ship.

## Short description
We turn AI-assisted repairs into reviewable evidence: reproduce the bug, preserve the tests, verify the fix, reject a wrong patch, and share an executable evidence package. Built with IBM Bob and tested locally.

## Long description
An AI-assisted fix can look right and still leave a defect behind. We built ProofPatch so that, before approving a repair, reviewers can inspect and reproduce the evidence behind it. Our workflow connects the original failure, the repaired code, unchanged tests and the exact execution artifacts in one place.

We used IBM Bob during our original development and created a reusable local Bob skill for the repair workflow. After consuming our allocated credits, we continued improving and testing the project locally. Our contribution record identifies the tools used at each stage.

Our working prototype demonstrates a synthetic task-export defect. A timestamp-only pagination cursor drops a record when timestamps tie. Our repaired cursor uses both timestamp and identifier. The verifier checks our frozen release reference, reproduces the named failure on the original implementation, and requires the repair to pass the same complete suite. It rejects incomplete runs, missing or changed protected tests, errors and skipped checks. A deliberately incorrect patch provides a negative control.

The repaired candidate passes all 30 behavior checks. Our 35 verifier and interface checks cover failure handling, evidence integrity, timeouts, concurrent runs and reproducibility. The downloadable package contains the exact executed source and tests, fixture, patch, complete logs, JUnit reports and checksums; a reviewer can rerun it independently.

Developers gain a repeatable review handoff. Reviewers and governance teams gain traceable evidence for their decisions. IBM's developer ecosystem could benefit from a reusable verification pattern around Bob-assisted development. End users benefit indirectly when teams catch incomplete exports and regressions before release.

Our first audience is small Python teams reviewing AI-assisted changes. The prototype handles one trusted bundled case; our next steps are repository adapters, CI integration and pilots measuring review time and escaped defects. Potential revenue would come from hosted team history and CI reporting, while keeping the core workflow open. This is a product hypothesis to validate, not an existing commercial result. Our distinctive contribution is the integrated, reproducible handoff of baseline failure, unchanged checks, candidate result and executable evidence. Verification remains scoped to the supplied suite and supports human review.

## Technology and category tags
IBM Bob; Python; Streamlit; pytest; developer tools; software testing; AI-assisted development.

## Repository
https://github.com/aazamcs/proofpatch

## Submission attachments
Upload PITCH.pdf, DEMO.mp4 and COVER.png from this folder. Use the public application URL after deployment. Attach our original Bob task/session exports with the repository as required by the submission guide. Checklist instructions are in CHECKLIST.md and are not part of the long-description field.
