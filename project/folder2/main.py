"""First draft of a K-Pg impact-winter model.

Chain: aerosol optical depth -> sunlight at surface -> two-box climate
-> photosynthesis -> three-level food web. Global means only.

Run:  python main.py                     (soot and sulfate scenarios)
      python main.py --tau-soot 10 --t-soot 2 --tau-sulf 0
"""
import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SIGMA = 5.67e-8          # Stefan-Boltzmann constant, W/m^2/K^4
S0 = 1361.0              # solar constant, W/m^2 (assumed close to today's)
ALBEDO = 0.30
T0 = 288.0               # pre-impact global mean surface temperature, K
ABSORBED = S0 / 4 * (1 - ALBEDO)          # ~238 W/m^2
EPS = ABSORBED / (SIGMA * T0**4)          # effective emissivity: balances at T0
C_S = 4.2e6 * 150        # surface layer: 150 m of water (tuned), J/m^2/K
C_D = 4.2e6 * 1000       # deep ocean: 1000 m of water, J/m^2/K
GAMMA = 0.7              # surface <-> deep ocean exchange, W/m^2/K
YEAR = 3.156e7           # seconds per year
DT_DAYS = 1.0


def optical_depth(t_yr, tau_soot, t_soot, tau_sulf, t_sulf):
    """Total aerosol optical depth; each type decays exponentially."""
    return tau_soot * np.exp(-t_yr / t_soot) + tau_sulf * np.exp(-t_yr / t_sulf)
    # shows how thick the haze is (tau)
    # has nothing to do w how much light is passed through (yet). just calcualtes how thick the haze is
    # does addition to get the total tau value (multiplying w exponents means adding the exponentials)
    
def productivity(trans, T):
    """Photosynthesis relative to normal (0..1), limited by light and cold.
    Light: none below 1% of normal sunlight, full above 50%.
    Temperature: none at 263 K (-10 C) or colder, full at T0."""
    light = np.clip((trans - 0.01) / (0.50 - 0.01), 0, 1)
        # 0.01 is the dark limit (1% of normal sunlight). It comes from Bardeen et al. 2017 (photosynthesis stops at 1% of normal sunlight)
        # 0.50 is the maximum brightness that allows the max cap of productivity. It is an assumed number, picked as a round number because real plankton do have maximum light saturation but the exact point varies greatly amongst different species. 
    warm = np.clip((T - 263.0) / (T0 - 263.0), 0, 1)
        # 263.0 degrees K is the minimum temperature that allows photosynthesis (cold slows down enzymes). It is an assumed number, based loosely on seawater freezing temps (~271 K) and plankton photosynthesis. 
    return light * warm
        # multiplying light * warmth is the common convention when modeling photosynthesis, as it roughly matches lab measurements. It is an assumed calculation, not derived from physics. 

def food_web_step(row, p, rates, dt, floor = 1e-4):
    # Each level grows toward the level below it (logistic tracking).
    # calculated with Euler's method
    # logistic tracking and Euler's method are assumed methods for simplicity's sake      
    
    food = np.array([p, row[0], row[1]])
    new_row = row + (rates * row * (food - row) * dt)
    new_row = np.maximum(new_row, floor)   # small refugia survive
        # the minimum number is an assumed number. It is not derived from physics. It was picked bc it's nice. Later on I will fine tune it to have it have a more accurate represnetation of recovery time
    return new_row

def run(tau_soot, t_soot, tau_sulf, t_sulf, years=60, deep=True):
    dt = DT_DAYS / 365.25
    n = int(years / dt)
    t = np.arange(n) * dt
    trans = np.exp(-optical_depth(t, tau_soot, t_soot, tau_sulf, t_sulf))
    Ts, Td = np.full(n, T0), np.full(n, T0)
    prod = np.ones(n)
    web = np.ones((n, 3)) # column 0: producers; column 1: herbivores; column 2: predators
    rates = np.array([12.0, 2.0, 0.5])    # per year: fast plankton, slow predators
        # the above are assumed numbers, picked to represent the response times to change in food availability of plankton (catch up in about a month) vs bigger animals (take about 2 years to recover)
    
    for i in range(n - 1):
        net = ABSORBED * trans[i] - EPS * SIGMA * Ts[i]**4
        exch = GAMMA * (Ts[i] - Td[i]) if deep else 0.0
        Ts[i + 1] = Ts[i] + ((net - exch) * dt * YEAR) / C_S
        Td[i + 1] = Td[i] + ((exch * dt * YEAR) / C_D)
        prod[i] = productivity(trans[i], Ts[i])
        web[i+1] = food_web_step(web[i], prod[i], rates, dt)
        
    prod[-1] = productivity(trans[-1], Ts[-1])
    return t, trans, Ts, Td, prod, web


def years_where(t, mask):
    return mask.sum() * (t[1] - t[0])


def hand_check():
    """Small constant forcing, no deep ocean: compare with the exact solution
    of the linearized one-box model, T(t) = F/lam * (1 - exp(-lam t / C))."""
    tau = 0.01
    t, trans, Ts, *_ = run(tau, 1e9, 0, 1, years=10, deep=False)
    F = -ABSORBED * (1 - np.exp(-tau))
    lam = 4 * EPS * SIGMA * T0**3
    exact = F / lam * (1 - np.exp(-lam * t * YEAR / C_S))
    err = np.max(np.abs((Ts - T0) - exact)) / np.max(np.abs(exact))
    _, _, Ts0, *_ = run(0, 1, 0, 1, years=10)
    print(f"Check 1 (hand-solvable): max relative error vs exact = {err:.2%}"
          f"  -> {'PASS' if err < 0.02 else 'FAIL'}")
    print(f"Check 2 (no aerosol): max drift from T0 = {np.max(np.abs(Ts0 - T0)):.2e} K"
          f"  -> {'PASS' if np.max(np.abs(Ts0 - T0)) < 1e-6 else 'FAIL'}")


def report(name, t, trans, Ts, prod, web):
    first_low = lambda x, lvl: t[np.argmax(x < lvl)] if (x < lvl).any() else np.nan
    print(f"\n{name}")
    print(f"  peak cooling:              {T0 - Ts.min():5.1f} K")
    print(f"  years below freezing:      {years_where(t, Ts < 273.15):5.1f}")
    print(f"  years photosynthesis <10%: {years_where(t, prod < 0.1):5.1f}")
    for j, lbl in enumerate(["producers", "herbivores", "predators"]):
        print(f"  {lbl:10s} fall below 10% at year {first_low(web[:, j], 0.1):5.2f},"
              f" minimum {web[:, j].min():.4f}")


def main():
    p = argparse.ArgumentParser(description="K-Pg impact winter, first draft")
    p.add_argument("--tau-soot", type=float, default=8.0, help="soot optical depth at impact")
    p.add_argument("--t-soot", type=float, default=1.5, help="soot e-folding lifetime, years")
    p.add_argument("--tau-sulf", type=float, default=2.0, help="sulfate optical depth at impact")
    p.add_argument("--t-sulf", type=float, default=3.0, help="sulfate e-folding lifetime, years")
    p.add_argument("--years", type=float, default=60)
    a = p.parse_args()

    hand_check()
    scenarios = {
        "Soot only (Bardeen-like)": (a.tau_soot, a.t_soot, 0, 1),
        "Sulfate only (Brugger-like)": (0, 1, a.tau_sulf, a.t_sulf),
        "Soot + sulfate": (a.tau_soot, a.t_soot, a.tau_sulf, a.t_sulf),
    }
    fig, ax = plt.subplots(4, 1, figsize=(9, 11), sharex=True)
    for name, args in scenarios.items():
        t, trans, Ts, Td, prod, web = run(*args, years=a.years)
        report(name, t, trans, Ts, prod, web)
        line, = ax[0].plot(t, trans * 100, label=name)
        ax[1].plot(t, Ts - 273.15, color=line.get_color())
        ax[1].plot(t, Td - 273.15, color=line.get_color(), ls=":")
        ax[2].plot(t, prod * 100, color=line.get_color())
        for j, ls in enumerate(["-", "--", ":"]):
            ax[3].plot(t, web[:, j] * 100, color=line.get_color(), ls=ls)
    print("\nApprox. published targets (verify in the papers): Brugger 2017 sulfate:"
          " >=26 K cooling, 3-16 yr below freezing, ~30 yr recovery;"
          " Bardeen 2017 soot: photosynthesis halted ~1-2 yr.")

    ax[0].set_ylabel("Sunlight at\nsurface (%)")
    ax[0].legend(fontsize=8)
    ax[1].axhline(0, color="gray", lw=0.8)
    ax[1].set_ylabel("Temperature (deg C)\nsolid surface, dotted deep")
    ax[2].set_ylabel("Photosynthesis\n(% of normal)")
    ax[3].set_ylabel("Biomass (% of normal)\nsolid prod, dash herb,\ndot pred")
    ax[3].set_yscale("log")
    ax[3].set_xlabel("Years after impact")
    ax[3].set_xscale("symlog", linthresh=1)
    ax[3].set_xlim(0, a.years)
    fig.suptitle("K-Pg impact winter: first-draft coupled model")
    fig.tight_layout()
    fig.savefig("kpg_draft.png", dpi=120)
    print("\nSaved kpg_draft.png")


if __name__ == "__main__":
    main()
