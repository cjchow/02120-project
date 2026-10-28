# K-Pg project study plan (Oct 28 – Dec 3, 2026)

Deadlines are from `project/folder1/Project_Description_F26.pdf` (all due 11:59 pm Eastern).
Each session is 30–60 min: one idea, a small exercise, and a journal entry. The course grades a steady rhythm, so spread the work out and don't cram.

| Date | Deadline |
|---|---|
| Fri Oct 30 | Journal checkpoint 1, repo link due |
| Nov 4–13 | 15-min TA check-in (book a slot) |
| Tue Nov 10 | Journal checkpoint 2 |
| Fri Nov 20 | Journal checkpoint 3, first app live on the web |
| Thanksgiving break | Nothing due |
| Tue Dec 1 | Demo day. Final app, code, video, and last journal checkpoint due |
| Thu Dec 3 | Closed, on-paper project assessment (35% of the project grade) |

## Week 1: Step 1–2, from aerosols to sunlight
- [ ] **Wed Oct 28 (30 min):** Why Brugger used 100 Gt of sulfur. Connect it to the "faucet at 1% vs 0%" idea.
- [ ] **Thu Oct 29 (45 min):** Optical depth: what `exp(-tau)` means (`main.py` line 46). Bardeen Fig. 1B–C: "sunlight declines exponentially with optical depth." Exercise: compute sunlight for tau = 1, 2, 5 by hand.
- [ ] **Fri Oct 30 (45 min):** How the haze fades over time: `optical_depth()` and "lifetime" (`t_soot`, `t_sulf`). Write its test. Read and redact `journal/`, then commit and push. **Checkpoint 1.**

## Week 2: Step 3, the two-tank climate, and the TA check-in
- [ ] **Mon Nov 2 (60 min):** The faucet and the drain as equations: `ABSORBED`, `SIGMA*T**4`, why `EPS` makes T0 balance. Hand check: no aerosols → temperature stays at T0.
- [ ] **Tue Nov 3 (60 min):** The tanks' size (`C_S`, `C_D`), the pipe (`GAMMA`), and stepping forward one day at a time (lines 52–55). Check 1 in `hand_check()`.
- [ ] **Thu Nov 5 (45 min):** TA check-in prep: explain the whole chain out loud in 2 minutes, run the program, and list your "I don't know yet" items.
- [ ] **Sat Nov 7 (45 min):** Step 4, photosynthesis: `productivity()`, Bardeen's 1% light threshold, and which numbers are "assumed." Write its test.

## Week 3: Step 5, then compare with the papers
- [ ] **Mon Nov 9 (45 min):** Step 5, the food web: how each level follows the level below it, and why predators drop last. Link to Bardeen's food-chain-collapse discussion.
- [ ] **Tue Nov 10 (30 min):** Redact the journal, commit, push. **Checkpoint 2.**
- [ ] **Thu Nov 12 (60 min):** Does the model match the papers? Compare the printed numbers to Bardeen and Brugger and find where they disagree, and why.
- [ ] **Sat Nov 14 (60 min):** Fix the mismatches you found (every changed number cites a paper or says "tuned"). Tests for every function.

## Week 4: Put it on the web
- [ ] **Mon Nov 16 (60 min):** Turn the command-line program into a web app (follow the course's deployment instructions).
- [ ] **Wed Nov 18 (60 min):** Add controls so a visitor can change the scenario (soot amount, sulfate lifetime).
- [ ] **Fri Nov 20 (30 min):** App live, commit, push. **Checkpoint 3.**

## Week 5: Before Thanksgiving
- [ ] **Mon Nov 23 (45 min):** Limitations and one extension, e.g. separate land and ocean (your question: Bardeen land −28 °C vs ocean −11 °C).
- [ ] **Tue Nov 24 (30 min):** Teach-a-friend test: explain the project with no notes. The gaps you find become your study list.
- Thanksgiving break: rest.

## Final stretch
- [ ] **Sun Nov 29 (60 min):** README, then record the ≤5-min video (your question, the program answering it, how you know it's right).
- [ ] **Mon Nov 30 (30 min):** Final check: everything runs, links work.
- [ ] **Tue Dec 1:** Demo day. **Final app, code, video, last journal checkpoint due.**
- [ ] **Wed Dec 2 (60 min):** Assessment practice: closed-book questions on the science, the code, and how you checked it. Draft reflective-essay notes.
- [ ] **Thu Dec 3:** Project assessment.
