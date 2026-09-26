# Final submission checklist

This is a team-owned checklist, not a claim that every external requirement is already complete.

## Included technical deliverables
- Working Streamlit app and fixed navigation.
- 30 behavior checks, verifier tests and a deliberate negative control.
- Exact-snapshot evidence downloads with complete logs, XML, diff and checksums.
- Pinned dependencies, MIT license, reproducible setup and deployment guide.
- Our development record and AI narration credit.
- Revised team-voice slides, cover, submission text, narrated MP4, captions and optional recording guide.

## Student A
- [ ] Recover authentic IBM Bob task/session exports and relevant screenshots.
- [ ] Add files and accurate labels to evidence/bob/index.json; verify the downloads in the app.
- [ ] Confirm technical claims match actual results. Original tests are preserved; additional tests and current release manifest are explicitly post-build.
- [ ] Run `python -m pytest tests/system` and candidate behavior checks from a clean installation.

## Student B
- [ ] Publish this release's source at the public GitHub repository (it was empty during review).
- [ ] Deploy app.py with Python 3.12; verify public access and all three outcomes while signed out.
- [ ] Set app_url and video_url, if used, in submission/links.json.
- [ ] Review the included MP4 (recorded results with synthetic narration). Add authentic Bob evidence or record the team version with DEMO_SCRIPT.md; keep it within five minutes.
- [ ] Upload the PDF pitch, PNG cover, code URL, app URL, descriptions and required reports.
- [ ] Verify both students' individual event registrations/team membership and the listed mentor/leader role in the current event interface.
- [ ] Submit before the deadline and save the confirmation page. Do not assume a late extension.

`python scripts/check_submission.py` checks local asset/link presence only. It cannot verify the authenticity of reports, public availability, team eligibility or acceptance by the organizer.

Official sources checked 26 September 2026:
- https://lablab.ai/ai-hackathons/ibm-bob-2-hackathon
- https://lablab.ai/delivering-your-hackathon-solution
- https://lablab.ai/guide

The submission guide requests public GitHub code, relevant exported IBM Bob reports, an interactive app URL, an MP4 up to five minutes and PDF slides. Use the live form if its requirements change.
