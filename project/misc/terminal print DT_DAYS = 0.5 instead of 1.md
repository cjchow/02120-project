Check 1 (hand-solvable): max relative error vs exact = 0.16%  -> PASS
Check 2 (no aerosol): max drift from T0 = 0.00e+00 K  -> PASS

Soot only (Bardeen-like)
  peak cooling:               26.3 K
  years below freezing:        7.6
  years photosynthesis <10%:   6.3
  producers  fall below 10% at year  0.75, minimum 0.0203
  herbivores fall below 10% at year  5.85, minimum 0.0869
  predators  fall below 10% at year   nan, minimum 0.2503

Sulfate only (Brugger-like)
  peak cooling:               21.1 K
  years below freezing:        7.6
  years photosynthesis <10%:   0.0
  producers  fall below 10% at year   nan, minimum 0.1624
  herbivores fall below 10% at year   nan, minimum 0.2038
  predators  fall below 10% at year   nan, minimum 0.3283

Soot + sulfate
  peak cooling:               31.6 K
  years below freezing:       10.8
  years photosynthesis <10%:   9.4
  producers  fall below 10% at year  0.75, minimum 0.0100
  herbivores fall below 10% at year  5.56, minimum 0.0577
  predators  fall below 10% at year   nan, minimum 0.1912

Approx. published targets (verify in the papers): Brugger 2017 sulfate: >=26 K cooling, 3-16 yr below freezing, ~30 yr recovery; Bardeen 2017 soot: photosynthesis halted ~1-2 yr.


--
KEY TAKEAWAY: 
  Halving DT_DAYS has neglible imapct on the results; therefore DT_DAYS = 1.0 is accurate enough to the numbers the results converge to when the time step gets infinitely small
