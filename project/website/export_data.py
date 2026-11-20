import json
import sys
sys.path.append("../simulation")
from main import run
import numpy

def symlog_x(t: float) -> float:
    """
    makes the x axis of the graph (y axis coems from simulation)

    t: float -- takes the current year as input and spits out where it would fall on the x axis, bc the first year is scaled linearly (by month) and the rest is scaled logarithmically (base 10)
    """
    pos = 0.0
    if t <= 1.0: 
        pos = t # less than a year has passed, so the x axis is still linear 
    else: 
        pos = 1 + numpy.log10(t) # more than a year has passed, so now we start counting in years (logarithmic spacing, base 10)

    return pos

def snapshot_indices(years: int) -> list[int]:
    """
    notes snapshots of which i want a user to hover over and see that time's value

    input: year (int) -- total time elapsed
    
    output: list of ints -- a list of the snapshot times, which will then get used to calculate the values at that time
    """
    snapshots = []
    for i in range(0,12):
        # less than a year has passed; snapshots are monthly
        a = i * (1/12) * 365.25 # time in years * (365.25 days / 1 year) = time in days
        snapshots.append(int(a))

    for i in range(1, years):
        # over a year has elapsed; snapshots are yearly
        snapshots.append(int(i * 365.25))
    
    return snapshots

def scenario_dict(results, idx):
    """
    - converts the results from run() into a dictionary
        - Omits t (store at the top as "time") and Td isn't in the graphs
    - makes the snapshots
    - turns the lists into a json.dump

    returns: the dictionary of a scenario (this will later be called 4 times for each scenario)
    """
    t, trans, Ts, Td, prod, web = results    # unpack what run() returns (aka results)

    return {
        "Ts":    Ts[idx].tolist(),
        "trans": trans[idx].tolist(),
        "prod":  prod[idx].tolist(),
        "web": web[idx].tolist(),
    }

def main():
    #   tau_soot, t_soot, tau_sulf, t_sulf, years=60, deep=True, floor = 1e-4)
    both = run(8.0, 1.5, 2.0, 3.0, years=60)
    soot = run(8.0, 1.5, 0.0, 1.0, years=60)
    sulfate = run(0.0, 1.0, 2.0, 3.0, years=60)
    neither = run(0.0, 1.0, 0.0, 1.0, years=60)

    idx = snapshot_indices(60)
    t = both[0]
    years = t[idx].tolist()    # times at the snapshots, as a list
    x = []

    for y in years: 
        x.append(symlog_x(y))

    data = {
        "years": years,
        "x": x, 
        "scenarios": {
            "both": scenario_dict(both, idx),
            "soot": scenario_dict(soot, idx),
            "sulfate": scenario_dict(sulfate, idx),
            "neither": scenario_dict(neither, idx),
        },
    }

    with open("data.json", "w") as f:
        json.dump(data, f)
        
if __name__ == "__main__":
    main()