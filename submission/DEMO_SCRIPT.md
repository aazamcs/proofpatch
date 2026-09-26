# Our demo recording guide

The included DEMO.mp4 is our narrated submission video. It starts with our project and slide story, then shows recorded executable results, testing and reproducibility. The transcript is in DEMO_TRANSCRIPT.txt. AI narration is disclosed in the closing credit.

If we choose to replace the result frames with a screen recording, keep the same script and total duration below five minutes:

1. Open with “An AI-generated fix can look right and still lose data.” Show our title: “Verify the fix. Before you ship.” Then explain the missing record and our intended users.
2. Show our Bob workflow slide and, if available, a brief genuine original task report. Explain original Bob development and continued local work after credits were used.
3. Open the running app. In Run verification set preview size to 3 and select Original defect. Click Run verification. Show Defect reproduced and task 4 missing.
4. Select Repaired candidate and run again. Show Verified against this test suite, 30 passing checks and all 8 IDs exactly once.
5. Select Deliberately incorrect repair and run again. Show Repair rejected and the repeated IDs. Explain that we intentionally use this negative control to test the verifier.
6. Run the candidate again, download its evidence ZIP, and show report.json, patch.diff, logs and snapshot/. Show the supplied rerun commands from README.md.
7. Close with stakeholders, pilot/revenue hypothesis, next steps and our takeaway: Verify the fix. Before you ship.

Use the checked-in results for a reliable rehearsal. Record a fresh run if presenting it as live. Original Bob reports document our actual historical sessions; a recreated workflow should be labeled as a demonstration.
