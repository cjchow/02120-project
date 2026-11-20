# Website plan (DRAFT — finish next session; first version due Fri 2026-11-20)

## Context
Course requires the app live on the web by **Fri 2026-11-20** (final app + video due Tue 12/1).
Must work for anyone with the link, no install; repo needs a README.
Christina's note: "soot/sulfate toggle? or time toggle?? interactive"

## Decided (11/17)
- Host: **Vercel** (shown in class).
- Controls: **soot on/off + sulfate on/off switches** → 4 scenarios (both, soot only, sulfate only, neither = control that must stay flat at T0 = 288 K).
- Because only 4 settings exist → **precompute** the 4 runs (option b), static page; no Python server needed.
- Graphs per scenario: sunlight (trans), surface temp (Ts), productivity (prod), food web (web, 3 levels).
- Hover shows exact values. Data sampled: **monthly early, yearly later** (matches the symlog x-axis already used in main.py line 157; also keeps the file small — a full run is ~21,900 daily steps).

- Sampling rule: **monthly for year 0–1, yearly from year 1 (10^0) on** (matches symlog linthresh=1).
- Layout ("control console"): toggles + **Run simulation** button on top; **2x2 grid of the 4 graphs (~75% width)**; right **~25% panel** with the terminal blurb for that scenario (output of `report()`, main.py:110) + other notes.
- Fun layer (stage 2, after core works): asteroid flies in from a corner → impact/explosion → clears to show new scenario. Cretaceous footer animals: T. rex, Triceratops, Quetzalcoatlus (pterosaur, not a dinosaur), and a Cretaceous sauropod instead of Diplodocus (Jurassic) — e.g. Alamosaurus. Christina worried constant motion is distracting — decide later (e.g. only move during/after a run).

## Staging
- **By Fri 11/20 (first version):** switches, run button, 4 hover graphs, blurb panel, deployed on Vercel.
- **Before 12/1:** asteroid animation, dinosaur footer, page text, video link.

## Still to decide next session
1. (done) sampling rule.
2. Chart library for hover (likely Plotly.js; loaded from CDN).
3. Page text beyond the blurb (question, how the model works, checks, limitations, video link later).
6. (decided) Footer: animals still except a small idle wiggle, **but they run around (panic) when the asteroid hits**; **how many appear depends on the model results**. Still open: which model level maps to which animal (plants = producers; Triceratops/Alamosaurus = herbivores; T. rex/Quetzalcoatlus = predators?) and at what time (minimum? year shown on hover?). Page must say the footer is an illustration: the model's 3 levels are generic, global-mean groups, not dinosaur counts.
4. File layout: e.g. `project/folder2/export_data.py` → writes `site/data.json`; `site/index.html`.
5. Test for the export (e.g. "neither" scenario: every Ts value == T0; sampled points match `run()` at those indices).

## Reuse
- `run(tau_soot, t_soot, tau_sulf, t_sulf, years, deep, floor)` — project/folder2/main.py:58 (one run ≈ 0.5 s)
- `recovery_time(t, x, threshhold)` — main.py:84 (could show recovery years on page)
- Scenario defaults: tau_soot 8.0, t_soot 1.5, tau_sulf 2.0, t_sulf 3.0, years 60

## Verification
- Run export script, check JSON has 4 scenarios; run tests (`pytest project/folder2`).
- Open index.html locally, toggle each switch, hover; then deploy to Vercel and open the public link.

## Progress (11/18)
- **x-axis decision:** Plotly has no symlog axis, so Python converts times itself with `symlog_x(t)` (t if t <= 1, else 1 + log10(t)); Plotly then draws on a plain linear axis with tick labels 0, 1, 10, 100 yr. This keeps the t = 0 control point, which a pure log axis would drop.
- Files moved into `project/website/`: `export_data.py`, `test_export_data.py`.
- Done and tested: `symlog_x(t)` and `snapshot_indices(years)`, which gives months 0-11, then years 1..years-1. That's 71 indices for 60 yr. Year 60 is left out because index 21915 is past the end of run()'s arrays.
- Done and tested: `scenario_dict(results, idx)` (Ts, trans, prod sampled as lists; `web` is 2-D, to add later).
- Next: all 4 scenarios, then `json.dump` to `data.json`, then a test (the "neither" run must stay at T0 = 288 K), then the page, then Vercel.
- To solve: export_data.py (in website/) needs to import `run` from folder2/main.py.

## Progress (11/20): v1 live on Vercel
- **Import solved:** `sys.path.append("../simulation")` before `from main import run`. This only works when the script is run from `project/website/` (relative paths start from the terminal's folder).
- **`export_data.py` `main()`** (behind `if __name__ == "__main__":`, so tests don't trigger it) runs the 4 scenarios. To turn an aerosol off, set its tau to 0 and keep its t (t = 1.0, same as main.py:131, because t is divided into). It builds `{"years", "x", "scenarios"}` and writes `data.json`. `scenario_dict` now includes `web` (71 x 3).
- **Checked by eye in data.json:** "neither" has Ts = 288.0 everywhere and web = [1.0, 1.0, 1.0] everywhere.
- **Page:** `index.html` (written by Claude, as agreed with the TA) loads `data.json`. Test it locally with `python -m http.server 8000` in `project/website`, then open http://localhost:8000.
- **Vercel:** Root Directory = `project/website`. The 404 was fixed by setting it and redeploying.
- **Page edits:** removed the "Preview" tag; Pachycephalosaurus always in front; sea predators (2 at full strength) follow the predator level; notes are now click-to-open sections with my own text.
- Without `"report"` in data.json, the readout box says "Summary numbers coming soon" and the herd sizes use the minimum of the sampled web.

## To do
### Now
1. Commit and push today's page edits.
2. Check that the site is public: open the short `.vercel.app` link in an incognito window. If you get a login page, go to Settings → Deployment Protection and turn off Vercel Authentication.

### Next session
3. `test_neither_stays_at_T0` in `test_export_data.py`: call `run(0.0, 1.0, 0.0, 1.0)` (not data.json, which could be outdated), then assert Ts == T0 and web == 1.0. Do a mutation check after (change a tau to 0.1, so the test should fail).
4. `report_dict` in Python (uses `T0`, `years_where`, `recovery_time` from main.py). Shape the page expects per scenario: `"report": {"peak_cooling", "yrs_freezing", "yrs_dark", "levels": [{"min", "below10", "recover"} x3]}`.

### Before 12/1 (stage 2)
5. Page text: the question, how the model works (haze → sunlight → temperature → photosynthesis → food web), checks (Bardeen, Brugger, T0), limitations.
6. Video link on the page.
7. `__file__` path fix so `export_data.py` (and its `data.json` output) works from any folder.

### Ongoing / later
8. Exam: GO OVER TAU AND SOOT FORMULAS (`optical_depth` from memory).
9. Skim the journal for anything personal before each push.
10. Recursion side quest (recursive food-web step in a scratch file), once the project is nearly done.
