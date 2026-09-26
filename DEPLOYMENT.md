# Publish and deploy

Owner: Student B. Technical check: Student A.

1. Extract the final ZIP and enter its ProofPatch folder. The files app.py and requirements.txt must be visible at this level.
2. Publish the CONTENTS of this folder to the public repository https://github.com/aazamcs/proofpatch. Keep .bob, .github and .streamlit. Do not upload the outer ZIP as the only repository file. Do not publish virtual environments, API keys, local credentials or __pycache__ folders. The release includes no external AI keys.
3. If using Git, create a normal release commit with an accurate present-day message such as “Publish reviewed ProofPatch release”. Do not claim this new commit predates the original repair. Preserve any authentic prior history the team has elsewhere.
4. In Streamlit Community Cloud, choose the public repository, its published branch and app.py as the entrypoint. Select Python 3.12 in deployment settings. Install dependencies using requirements.txt. No secrets need to be configured. Exact hosting UI labels may change; use the platform's current repository/entrypoint settings.
5. Open the resulting HTTPS application URL while signed out. Run original, candidate and deliberately incorrect repair at page size 3. Expected results: Defect reproduced; Verified against this test suite; Repair rejected.
6. Change page size to 2 and 4. A previous result must clear until you run again. Each repaired preview must contain all 8 tasks once.
7. Download candidate evidence and confirm it contains patch.diff, checksums.json, both JUnit reports, acceptance tests and the fixture. This is a functional check, not just a homepage availability check.
8. Set app_url in submission/links.json and use that public URL on the submission form. Add authentic Bob artifacts using evidence/bob/README.md, and publish the updated files if these are added after deployment.
9. Check the mobile layout, the four tabs and all downloads. Do not require judges to sign in or enter an API key.
10. Save the accepted submission confirmation. The official deadline shown on the event site is 27 September 2026, 8 p.m. Pakistan Standard Time. Aim to finish several hours earlier.

This release was tested locally on Python 3.12. Hosted execution must be checked after deployment; local tests cannot establish public service availability.
