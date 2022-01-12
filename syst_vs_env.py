import random
import dynet as dy
import numpy as np

# to use a particular example, uncomment its line and comment all the others

#from cycle_abc import *
# from cycle_random_abc import *
# from cycle_random_abc_anchor1 import *
# from cycle_random_abc_anchor2 import *
# from cycle_random_abc_anchor3 import *
# from cycle_random_abc_memory import *
# from detector import *
#from cycle_abb import *  # "permitted"
#from schedule import *
#from cases import *
#from unlucky import *
#from strategy import *
# from strategy2 import *
# from cycle_abcbc import *
# from cycle_abcbca import *
#from combination_lock import *
# from combination_lock2 import *
# from choice import *
# from choice2 import *
# from choice3 import *
# from choice4 import *
# from choice5 import *
# from choice6 import *
# from choice_tournament import *
#from choice_scc import *
#from least_failures import *
#from unit3 import *
# from choice_and_good_failure import *
# from match_coins import *
#from matching_simplified import *
# from combine_scc_cycle import *
# from combine_scc_cycle_simplified import *
# from combine_scc_cycle_simplified_2 import *
#from combine_schedule_cycle import *
#from good_failure import *
#from unit4 import *
#from strategy_oracle import *
#from cases_oracle import *
#from choice_scc_oracle import *
#from schedule_oracle import *
#from cycle_abc_oracle import *
#from unlucky_oracle import *
#from least_failures_oracle import *
#from combination_lock_oracle import *
#from good_failure_oracle import *
from strategy3 import *

# number of controlled tests after training, and length of control executions
C = 100
L_C = 200
model = "any_available"


def count_failures(execution):
    counter = 0
    for step in execution:
        if step[0][:4] == "fail":
            counter += 1
    return counter

# same to test on a large amount of trainings
def test(number_of_tests, number_of_runs, size, print_probs=False, random_exploration=False, new_loss=False,
         lookahead=1, epsilon=0, compare_loss=False):
    results = []
    T = number_of_runs
    L = size

    for test in range(number_of_tests):
        pve = create(model)
        for training in range(T):
            for length in range(1, L):
                pve.reinitialize()
                pve.generate_training_execution(length, lookahead=lookahead, epsilon=epsilon)

        failures = []
        for control in range(C):
            pve.reinitialize()
            execution = pve.generate_controlled_execution(L_C)  # all executions of length 200
            failures.append(count_failures(execution))
        print(execution)
        percentage = 0
        for i in range(C):
            percentage += (failures[i]/L_C) * 100
        percentage /= C

        results.append(percentage)
        print(test)
    average = 0
    for r in results:
        average += r
    return average/len(results)

new_loss = ""
for l in [0,3,20]: #
    for e in [0,0.2,0.5]: #
        print("lookahead: ", l, " epsilon: ", e)
        this_failure = str(test(1, 50, 50, new_loss=True, lookahead=l, epsilon=e, compare_loss=False))
        print("loss for above params: " + this_failure)
        new_loss = new_loss + " " + this_failure
print("the new loss of all parameters is: ", new_loss)

# random
pve_rand = create(model)
failures = []
for control in range(C):
    pve_rand.reinitialize()
    execution = pve_rand.generate_random_execution(L_C)
    failures.append(count_failures(execution))
percentage = 0
for i in range(C):
    percentage += failures[i]/L_C
percentage /= C
print("(random)", percentage * 100, "%")
