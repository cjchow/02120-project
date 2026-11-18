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
    }