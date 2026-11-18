from export_data import symlog_x, snapshot_indices, scenario_dict
import numpy as np

def test_symlog_x():
    """
    tests that symlog_x (that i made the x axis correctly)
    
    t# refers to trial time inputs

    i use assert < 1e-6 bc floats can have rounding errors, which would fail ==
    """
    t1 = 0
    assert abs(symlog_x(t1) - 0.0) < 1e-6
    # t <= 1, so t = pos

    t2 = 0.5
    assert abs(symlog_x(t2) - 0.5) < 1e-6
    # t <= 1, so t = pos

    t3 = 1
    assert abs(symlog_x(t3) - 1.0) < 1e-6
    # t <= 1, so t = pos

    t4 = 10
    assert abs(symlog_x(t4) - 2.0) < 1e-6
    # t > 1, so pos = 1 + log10(10) = 1 + 1 = 2

    t5 = 60
    assert 2.0 < symlog_x(t5) and symlog_x(t5) < 3.0
    # t > 1, so pos = 1 + log10(60), and 10 < 60 < 100, so between (2,3)

def test_snapshot_indices():
    """
    tests that snapshot_indices is correctly: 
        1. producing the right number of snapshots
        2. the snapshot times are correct (tests that the first 3 values match)
        3. the last index is still within run()'s array length
    """
    snapshots: list[int] = snapshot_indices(60)

    assert len(snapshots) == 71

    assert snapshots[0:3] == [0, 30, 60] # aka 0 days/steps elapsed, 30 steps passed, 60 steps passed at the start, month 1, and month 2

    assert snapshots[-1] < 21915

def test_scenario_dict():
    """
    tests that scenario_dict is correctly turning the output of run() into a dictionary
    """
    a = np.array([10.0, 20.0, 30.0, 40.0])
    results = [a, a, a, a, a, a]
    idx = [0,2]

    assert scenario_dict(results,idx)["Ts"] == [10.0, 30.0]

    # making sure they correspond to their appropriate list values
    results2 = [a, 2*a, 4*a, a+1, a*67, a*1234]
    assert scenario_dict(results2, idx)["trans"] == [20.0, 60.0]
    assert scenario_dict(results2, idx)["Ts"] == [40.0, 120.0]
    assert scenario_dict(results2, idx)["prod"] == [670.0, 2010.0]