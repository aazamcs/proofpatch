---
name: proofpatch
description: >
  Reproduce a reported bug with a regression test, repair only the candidate
  implementation, verify the fix, and package all evidence for review.
  Use this skill for any debugging workflow in this repository.
---

# ProofPatch Workflow

## Overview

ProofPatch is a structured debugging workflow. It requires that a bug is
**reproduced** before it is **fixed**, and that the fix is **verified**
with the same test that caught the original failure.

Steps: **Understand → Clarify → Reproduce → Preserve → Repair → Verify → Package**

---

## Step 1 — Understand

Read the following files before doing anything else:

- `issues/missing_tasks.md` — the bug report
- `spec/expected_behavior.md` — the full behavioral contract
- `sample/baseline/pagination.py` — the original defective code
- `sample/candidate/pagination.py` — the target for repair

Explain in your own words:
1. What the reported symptom is.
2. Which file and which lines cause it.
3. What the correct behavior should be.

If the report lacks an observable expected result or reproduction conditions,
ask one focused clarifying question and **stop** — do not edit source files.

---

## Step 2 — Clarify (if needed)

Ask for exactly the missing information:
- What is the input?
- What result is observed?
- What result is expected?
- Under what conditions does the failure occur?

Do not assume a specific defect until you can point to the file and line.

---

## Step 3 — Reproduce

Create a failing test under `tests/repro/` that asserts the **externally
visible** behavior described in the bug report.

Rules:
- The test must assert IDs, ordering, and absence of duplicates — not
  implementation details like cursor shape.
- Run it against `sample/baseline/` using `PROOFPATCH_VARIANT=baseline`.
- The test **must fail** on the baseline. A passing test does not reproduce
  the bug.
- A collection error, import error, or syntax error is **not** a reproduction.
  Fix the environment and rerun.

Command:
```
PROOFPATCH_VARIANT=baseline python -m pytest tests/repro/ -v
```

Save the output. Report the exact assertion failure message.

---

## Step 4 — Preserve

Before touching any production code:

1. Commit the failing test as-is.
2. Record the SHA-256 hash of the test file bytes.
3. Record the SHA-256 hash of the baseline source directory.

These hashes identify the preserved bytes. They do not prove authorship or
chronology. Retain the actual failing run and session export as separate evidence.
The bundled frozen manifest was created during post-build review, not before
the original repair. Never relabel a retrospective snapshot as original evidence.

---

## Step 5 — Repair

Repair **only** `sample/candidate/`.

Constraints:
- Keep the public interface: `list_tasks(records, cursor, page_size)` and
  `export_all(records, page_size)`.
- Do not modify `sample/baseline/` or the fixture.
- Do not modify `tests/repro/` or `tests/acceptance/`.
- Make the **smallest clear change** that satisfies the behavioral contract.
- Explain the diff in plain language before applying it.

If the patch fails after two attempts, stop and describe the cause.

---

## Step 6 — Verify

Run both the regression test and the acceptance suite against the candidate:

```
PROOFPATCH_VARIANT=candidate python -m pytest tests/repro/ tests/acceptance/ -v
```

All tests must pass. If any fail, report the failure — do not claim
completion.

---

## Step 7 — Package evidence

Use Prompt 3 to produce `summary.md` containing:

- Original issue and root cause
- Files changed and nature of the change
- Tests run, counts, and results
- Known limitations
- Statement that the repair is verified only against the listed tests

Reference actual file paths and measured results. Do not invent timings or
claim correctness beyond the test suite.

---

## Prompts

### Prompt 1 — Diagnose and reproduce

```
Use our ProofPatch workflow. Read issues/missing_tasks.md,
spec/expected_behavior.md, and the sample baseline code. Explain the
affected flow with actual file references. If the report is insufficient,
ask a focused clarification question and stop. Otherwise create a regression
test under tests/repro that captures the externally visible defect. Run it
on the baseline and save the output. Do not repair production code yet. A
test collection or environment error is not a reproduction.
```

### Prompt 2 — Repair and verify

```
The reproducing test has been reviewed and preserved. Repair only
sample/candidate, keeping the shared function interfaces and the fixture
unchanged. Do not modify the preserved regression test or the independent
acceptance tests. Make the smallest clear change that satisfies the behavior
specification. Run the same regression and acceptance checks. Save the actual
logs and explain the diff. If checks fail, report that rather than claiming
completion.
```

### Prompt 3 — Prepare the review summary

```
Read this run's report, test results, logs, and diff. Create summary.md
explaining the original issue, cause, changes, checks performed, and
remaining limitations. Cite the files in the evidence package. Do not
invent results, timings, or savings. State that the repair is verified only
against the listed tests and awaits human review.
```

### Prompt 4 — Check incomplete input

```
Use ProofPatch for this report: 'The export is wrong.' Determine what
information is missing before making a change. Do not assume a specific
defect or edit source files without enough information to reproduce it.
```

---

## Result classification

| Status | Meaning |
|--------|---------|
| Reproduced | Regression assertion fails on baseline |
| Verified against this test suite | Baseline fails, candidate passes all checks |
| Repair rejected | Candidate fails a required check |
| Execution error | Timeout, import error, or missing output |
| Needs information | Report lacks reproducible expected behavior |

A zero test count is always an error, never a success.
