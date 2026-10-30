# CLAUDE.md

## Who I am
I'm Christina, an undergrad in 02-120 Programming for Scientists (CMU, Fall 2026). I write Python. <!-- edit: add your year/major and how comfortable you are with Python, numpy, and plotting -->

## How I like to learn
- Teach me one idea at a time, and check that I understand it before moving on.
- When you explain or teach something, number each point (1, 2, 3…) so I can reply to a specific one by its number.
- Quiz me and ask me to predict results instead of just giving me the answer.
- Explain *why* you made a choice, not only what the code does.
- Use plain English. Define any climate-science or math term the first time you use it.
- When I'm learning, let me write the code myself with hints. Write it for me only if I ask.
<!-- edit: change these to match how you actually like to learn -->

## What I'm building
**Question:** How much did the asteroid impact at the Cretaceous–Paleogene (K-Pg) boundary disrupt climate and ecosystems?

**Model:** a simplified, runnable "impact winter" model in Python. It is a reduced version of what the full climate models in the papers do (CESM/WACCM/CARMA, CLIMBER-3a), which need a supercomputer. The chain is:
aerosol optical depth (soot, sulfate) → sunlight reaching the surface → two-box climate (surface layer + deep ocean) → photosynthesis → a three-level food web. It uses global means only, and the user can change scenarios from the command line.

**Checks:** reproduce the main published results:
- Bardeen et al. (2017): short-term effects of soot (darkness, surface cooling, photosynthesis collapse).
- Brugger et al. (2017): long-term cooling from sulfate aerosols.
Also check special cases by hand, e.g. with no aerosols the temperature must stay at the pre-impact value T0.

## Repo layout
- `project/data/`: the two source papers (PDFs). Teach me from these.
- `project/folder1/`: course project description and my proposal (`proposal.csv`).
- `project/folder2/main.py`: current draft of the model. `kpg_draft.png` is its output.
- `journal/`: build journal (generated). The hook redacts emails, IP addresses, and my Windows username automatically; still skim it before pushing.

## Rules for working with me
- Use plan mode for anything bigger than a small fix.
- Prove things work: every function gets a test, and you explain the test in plain English.
- Every number or constant must cite a paper or say "assumed/tuned".
- Never put passwords, API keys, or personal info in code, commits, or this file. This repo is public, so anyone can read it, including TAs and graders.
- I make my own commits. Suggest a commit message, but don't commit or push unless I ask.
