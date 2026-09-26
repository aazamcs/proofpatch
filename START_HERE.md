# ProofPatch — our final submission package

Our repository and submission media are published. The verifier runs without further AI credits.

## 1. Open the published project
- Live app: https://proofpatch-verified.streamlit.app/
- Source and submission assets: https://github.com/aazamcs/proofpatch
- Narrated demo: https://github.com/aazamcs/proofpatch/blob/main/submission/DEMO.mp4

The GitHub automated checks passed on Python 3.12. We verified public access and all three expected outcomes while signed out on 26 September 2026.

## 2. Check the three outcomes
On Run verification, leave preview page size at 3. Run each implementation:
- Original defect: **Defect reproduced**, task 4 absent from the preview.
- Repaired candidate: **Verified against this test suite**, IDs 1-8 returned once.
- Deliberately incorrect repair: **Repair rejected**, duplicates shown. This rejection is the intended result.
Download the candidate evidence ZIP and inspect report.json, patch.diff, XML reports and snapshot/.

## 3. Run it locally when needed
Use Python 3.12. Open a terminal inside this ProofPatch folder:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Windows: use `py -3.12 -m venv .venv`, then `.venv\Scripts\activate` instead of the first two lines. Open the local URL printed by Streamlit.

## 4. Complete the remaining submission steps
Student A: export the team's existing IBM Bob sessions and screenshots. See evidence/bob/README.md. New Bob inference credits are not needed by this application. Whether old sessions remain exportable depends on the available Bob UI; do not invent historical evidence.

Student B: review the included narrated MP4, confirm individual registrations and team membership, and complete the organizer submission. The video uses our team voice; submission/DEMO_SCRIPT.md provides an optional screen-recording guide.

Use submission/PITCH.pdf, COVER.png, and SUBMISSION_COPY.md. Consult submission/CHECKLIST.md. Attach genuine Bob reports, the public app link, repository and final video. Run `python scripts/check_submission.py` to identify missing local handoff items; it cannot validate organizer acceptance. Publishing and deployment do not submit our entry to the hackathon.

Our project is a Bob-assisted development workflow with an independent executable verifier for a disclosed sample case. Our development record is in PROVENANCE.md.
