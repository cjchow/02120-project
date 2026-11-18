from main import run, recovery_time

# testing different floor values to see their impact
# initialy hypothesis: predators would have the most severe drop because they have the slowest reaction time/longest recovery time. However, this is incorrect because the producers, even though they have a shorter recovery time, have the greatest drop bc of the severe lack of food resources (for producers, sunlight and warmth)
# found that producers (the lowest food chain level and who had the most severe impact) only reach a minimum of 1% of normal, so the floor values never even activate (although barely: the producers drop to 1.003% vs a 1% floor)
# also found that the longest recovery time was for predators, at 23.5 years

list_floors = [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]

for i in range(len(list_floors)):
    t, trans, Ts, Td, prod, web = run(tau_soot=8.0, t_soot=1.5, tau_sulf=2.0, t_sulf=3.0, floor=list_floors[i])

    # first tested the drop and recovery time for predators bc i initially thought that predators would near extinction because they have the slowest reaction time (but I was wrong). They do have the longest recovery time, but they don't drop to near extinction
    time_preds = recovery_time(t, web[:, 2])
    print("the minimum predator population is", web[:,2].min() * 100, "percent of pre-impact population")
    print("the recovery time for the floor value of", list_floors[i], "for predators is", time_preds, "years after the impact")

    # now testing the drop and recovery time for producers, bc even though they have the quickest recovery time, they have the most severe drop
    time_prods = recovery_time(t, web[:, 0])
    print("the minimum producer population is", web[:,0].min() * 100, "percent of pre-impact population")
    print("the recovery time for the floor value of", list_floors[i], "for producers is", time_prods, "years after the impact")
    