import random
import dynet as dy
import numpy as np

# number of controlled tests after training, and length of control executions
C = 100
L_C = 200
L_C_short = 50
model = "any_available"


def count_failures(execution):
    counter = 0
    for step in execution:
        if step[0][:4] == "fail":
            counter += 1
    return counter


results = []
results_short = []
best = L_C
best_short = L_C_short
worst = 0
worst_short = 0

from combine_schedule_cycle import *
#from combine_scc_cycle import *

number_of_epochs = 1000
training_execution_length = 8
runs = 2

line = ""
for tests in range(10):
    pve = create(model)
    for _ in range(runs):
        for (lookahead,epsilon) in [(5, 0), (0, 0)]:
            for epoch in range(number_of_epochs):
                d_epsilon = epsilon * (1 - epoch / (number_of_epochs - 1))
                for length in range(1,training_execution_length):
                    pve.reinitialize()
                    pve.generate_training_execution_target_network(length,lookahead = lookahead,epsilon = epsilon,compare_loss = True)

    failures = []
    failures_short = []

    for control in range(C):
        pve.reinitialize()
        execution = pve.generate_controlled_execution(L_C_short,print_probs = False)
        failures_short.append(count_failures(execution))

    for control in range(C):
        pve.reinitialize()
        execution = pve.generate_controlled_execution(L_C,print_probs = False)
        failures.append(count_failures(execution))

    percentage = 0
    percentage_short = 0
    for i in range(C):
        percentage += failures[i]/L_C
        percentage_short += failures_short[i]/L_C_short
    percentage /= C
    percentage_short /= C

    if percentage > worst:
        worst = percentage
    if percentage < best:
        best = percentage
    if percentage_short > worst_short:
        worst_short = percentage_short
    if percentage_short < best_short:
        best_short = percentage_short

    results.append(percentage)
    results_short.append(percentage_short)
    # test number...

# global results..
add = ""
add += str(best_short * 100) + " " + str(worst_short * 100) + " " + str(sum(results_short) / len(results_short) * 100) + " "
add += str(best * 100) + " " + str(worst * 100) + " " + str(sum(results) / len(results) * 100) + " "

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

add += str(percentage * 100) + " "
print(add)

'''
print("############  Global results:  ############")
print("_Short control_")
print("Best result:",best_short*100,"%")
print("Worst result:",worst_short*100,"%")
print("Average",sum(results_short)/len(results_short)*100,"%")

print("_Long control_")
print("Best result:",best*100,"%")
print("Worst result:",worst*100,"%")
print("Average",sum(results)/len(results)*100,"%")
'''

def run(pve, steps = 50, print_first=False, print_probs=False):
    pve.reinitialize()
    if print_first:
        print(pve.generate_controlled_execution(steps, print_probs=print_probs)[0][0])
    else:
        print(pve.generate_controlled_execution(steps, print_probs=print_probs))



# same to test on a large amount of trainings
def test(number_of_tests, number_of_runs, size, print_probs=False, random_exploration=False, new_loss=False,
         lookahead=1, epsilon=0, compare_loss=False):
    results = []
    T = number_of_runs
    L = size

    for test in range(number_of_tests):
        for T in [number_of_runs]:
            for L in [size]:
                pve = create(model)
                for training in range(T):
                    for length in range(1,L):
                        pve.reinitialize()
                        pve.generate_training_execution(length,print_probs = False,random_exploration = random_exploration,new_loss = new_loss,lookahead = T,epsilon = epsilon,compare_loss = compare_loss)
                        
                        #print("____________")
                    for length in range(1,L):
                        pve.reinitialize()
                        pve.generate_training_execution(length,print_probs = False,random_exploration = random_exploration,new_loss = new_loss,lookahead = 0,epsilon = epsilon,compare_loss = compare_loss)
                        
                failures = []
                for control in range(C):
                    pve.reinitialize()
                    execution = pve.generate_controlled_execution(L_C,print_probs = print_probs)
                    #print("____________")
                    failures.append(count_failures(execution))
                percentage = 0
                for i in range(C):
                    percentage += (failures[i]/L_C)*100
                percentage /= C
                #print("test number",test+1,"(",T,",",L,")",percentage*100,"%")
                #run(pve,True)
                run(pve,False,print_probs = True)

        
        results.append(percentage)

    average = 0
    for r in results:
        average += r
    return average/len(results)



# =============================================================================
# for l in [0, 3, 20]:
#     for e in [0, 0.2, 0.5]:
#         print("lookahead = ", l, "epsilon = ", e)
#         print("new_loss", test(50, 50, 50, new_loss=True, lookahead=l, epsilon=e, compare_loss=False))
#         print("old_loss", test(50, 50, 50, new_loss=True, lookahead=l, epsilon=e, compare_loss=True))
# =============================================================================

