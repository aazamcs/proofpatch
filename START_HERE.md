# ProofPatch — our final submission package

Our final repository and submission media are together in this folder. The verifier runs locally without requiring further AI credits.

## 1. Run it locally
Use Python 3.12. Open a terminal inside this ProofPatch folder:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Windows: use `py -3.12 -m venv .venv`, then `.venv\Scripts\activate` instead of the first two lines. Open the local URL printed by Streamlit.

## 2. Check the three outcomes
On Run verification, leave preview page size at 3. Run each implementation:
- Original defect: **Defect reproduced**, task 4 absent from the preview.
- Repaired candidate: **Verified against this test suite**, IDs 1-8 returned once.
- Deliberately incorrect repair: **Repair rejected**, duplicates shown. This rejection is the intended result.
Download the candidate evidence ZIP and inspect report.json, patch.diff, XML reports and snapshot/.

## 3. Prepare the remaining submission evidence
Student A: export the team's existing IBM Bob sessions and screenshots. See evidence/bob/README.md. New Bob inference credits are not needed by this application. Whether old sessions remain exportable depends on the team's available Bob UI; do not invent or recreate them as historical evidence.
Student B: publish this folder's CONTENTS at the GitHub repository root, deploy app.py, open the public link while signed out, and review the included narrated MP4. The revised video uses our team voice; submission/DEMO_SCRIPT.md provides an optional screen-recording guide.
The supplied public GitHub repository was empty when checked on 26 September 2026. This ZIP has not been pushed or deployed.

## 4. Submit
Use submission/PITCH.pdf, COVER.png, and SUBMISSION_COPY.md. Consult submission/CHECKLIST.md. Attach genuine Bob reports, the public app link, repository and final video. Run `python scripts/check_submission.py` to identify missing local handoff items; it cannot validate organizer acceptance or public availability.

Our project is a Bob-assisted development workflow with an independent executable verifier for a disclosed sample case. Our development record is in PROVENANCE.md.
