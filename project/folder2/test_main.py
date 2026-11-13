from main import optical_depth, productivity, food_web_step
import numpy as np

def test_optical_depth():
    """
    Tests optical depth w known values.
    
    blob_t# is the total tau value that optical_depth returns at t = #
    blob_t# = (tau_soot * e^(-t / t_soot)) + (tau_sulf * e^(-t / t_sulf))
    """

    # tests that the initial optical depth is corret
    # Before any fading (t=0), tau should equal the starting soot thickness (10).
    blob_t0 = optical_depth(0, 10, 1, 0, 1)
    assert blob_t0 == 10
    
    # tests that there's not a missing minus sign in t_yr
    # tests that one lifetime (t=1), the soot drops to e^(−1) ≈ 37%. This isolates soot and catches a sign error that would make the haze grow.
    blob_t1 = optical_depth(1, 10, 1, 0, 1)
    expected = 10 * np.exp(-1) # python's way of writing 10 * e^(-1)
    assert abs(blob_t1 - expected) < 1e-9

    # tests that t_sulf and t_soot aren't accidentally swtiched
    # tests that sulfate fades on its own clock (t_sulf = 5 years). Given different sulfate and soot lifetimes (t_soot != t_sulf), it isolates the sulfate component and catches a mix-up between t_soot and t_sulf.
    blob_t1_switched = optical_depth(1, 0, 1, 10, 5)
    expected_switched = 10 * np.exp(-1 / 5) # aka 10 * e^(-1/5)
    assert abs(blob_t1_switched - expected_switched) < 1e-9

def test_productivity():
    """
    Tests productivity (photosynthesis) w known values
    
    productivity = light * warm
        - light = (trans - 0.01) / 0.49
        - warm = (T - 263) / 25
        
        - Both light and warm are clipped to [0, 1]

    """

    # tests that the light limits (0.01 and 0.5) are correct
    # this isolates light (288 makes warm = 1), so we can check the limits in light
    blah_limits = productivity(0.255, 288)
    assert abs(blah_limits - 0.5) < 1e-9

    # tests that the clip works (for both ends)
    blah_clip = productivity(0.8, 250)
    assert abs(blah_clip - 0.0) < 1e-9

    # tests that productivity is calculated correctly (multiplication) and not averaged/the min taken
    blah_min = productivity(0.255, 275.5)
    assert abs(blah_min - 0.25) < 1e-9

    # test that the dark limit wasn't forgotten
    blah_dark = productivity(0.01, 288)
    assert abs(blah_dark - 0.0) < 1e-9

def test_food_web_step():
    """
    Tests that a step of the food web is correctly being calculated 
    
    - new_row = row + rates * row * (food - row) * dt
        - row = population of each level (0 = producers, 1 = prey, 2 = predators)
        - rates = each food level's response to changes in food availability
        - (food - row) = food available - mouths to feed
        - dt = 1/365.25 (1 day)
    """
    row = np.array([0.9, 0.95, 1.0])
    p = 0.2
    rates = np.array([12.0, 2.0, 0.5])
    dt = 1 / 365.25
    # uses default floor value of 1e-4

    # tests that it matches my hand check (no typos)
    bleh_correct = food_web_step(row, p, rates, dt)
    assert abs(bleh_correct[0] - (0.9 + (12 * 0.9 * (0.2 - 0.9) * (1 / 365.25)))) < 1e-9

    # tests that the floor works (that the maximum ensures the refugia when new_row[i] < 1e-4)
    # when producers are starving, they change very little, and this tests that the floor is functioning (needs a higher tolerance)
    row2 = np.array([1e-4, 0.5, 0.5])
    p2 = 0 # starve them like the french proletariat
    # rates and dt stay the same
    bleh_floor = food_web_step(row2, p2, rates, dt)
    assert abs(bleh_floor[0] - 1e-4) < 1e-16

test_optical_depth()
test_productivity()
test_food_web_step()
print("all tests passed!")