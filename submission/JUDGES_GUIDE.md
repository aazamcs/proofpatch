# Our evidence map for judges

We built ProofPatch around a simple review question: can someone else reproduce why this repair should be accepted?

| What to assess | Where to inspect | What to expect |
|---|---|---|
| Problem and significance | PITCH.pdf, slides 1–2 | Silent loss of an export record and why review evidence matters |
| IBM Bob workflow | .bob/skills/proofpatch/SKILL.md; PROVENANCE.md; original Bob reports attached separately | Reusable repair workflow and accurate development attribution |
| Functional demonstration | App: Run verification; DEMO.mp4 | Original reproduced, candidate verified, incorrect repair rejected |
| Identical test gate | proofpatch/runner.py; evidence/frozen_manifest.json | Protected baseline/tests/fixture and required named regression |
| Behavior | evidence/verification/candidate-3.json | 30 checks pass; 8 IDs appear exactly once |
| Negative control | evidence/verification/bad_patch-3.json | 22 failing checks and rejected repair |
| Robustness | tests/system/; evidence/verification/system-tests.xml | 35 passing checks, including corruption and incomplete execution |
| Independent rerun | Downloaded evidence ZIP; README.md | Exact snapshots, logs, checksums and rerun commands |
| Business value | PITCH.pdf, slides 6–7 | Defined first users, ecosystem value and pilot/revenue hypotheses |
| Originality | PITCH.pdf, slide 7 | Integrated evidence handoff; tests and CI themselves are established methods |

Scope: this prototype supports one synthetic bundled case. The current hash manifest is a release reference, not proof of historical authorship. Test success supports review within the tested scope; it is not universal correctness or compliance certification.
