import random
import dynet as dy
import numpy as np

# to use a particular example, uncomment its line and comment all the others

# If using a non-combined example, uncomment the next three lines
number_of_epochs = 50 #this is what we called T so far
training_execution_length = 50 #this is what we called L so far
runs = 1 # will be >1 only for combined examples


# from cycle_abc import *
# from cycle_abb import *
from schedule import *
# from cases import *
# from unlucky import *
# from strategy import *
# from combination_lock2 import *
# from choice import *
# from choice_scc import *
# from least_failures import *
# from good_failure import *
# from match_coins import *



# If using a combined example, comment the three lines number_of_epochs and training_execution_length and runs above, and uncomment the ones below that correspond to the example:

#from combine_scc_cycle_simplified import *
#number_of_epochs = 100 #this is what we called T so far
#training_execution_length = 8 #this is what we called L so far
#runs = 5


#from combine_schedule_cycle import *
#number_of_epochs = 10 #this is what we called T so far
#training_execution_length = 50 #this is what we called L so far
#runs = 2


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







    
# T is the number of "epochs" we'll do the training on; if T is iterated on a
# list of numbers, we'll do a different training with each number of epochs chosen
    
results = []
results_short = []

best = L_C
best_short = L_C_short

worst = 0
worst_short = 0

print("Computation for",number_of_epochs,"epochs and training executions of length",training_execution_length)

for tests in range(10):
    
    pve = create(model) # this generates the system and environment
    
    
    for r in range(runs):
        
    
        for (lookahead,epsilon) in [(3,0)]:
            #print("lookahead",lookahead,"and epsilon",epsilon)
        
        
            # iterating over the epochs
            for training in range(number_of_epochs):
                
                #iterating over the training sequences from length 1 to length L
                for length in range(1,training_execution_length):
                    
                    pve.reinitialize() #return system and environment to initial states
                    
                    # Now we generate a training sequence.
                    pve.generate_training_execution(length,lookahead = lookahead,epsilon = epsilon,compare_loss = False)
            
    
            
            
            
            
            
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
    #percentage *= 100
    percentage_short /= C
    #percentage_short *= 100
    
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
    
    
    
    
    print("##### test number",tests+1,"#####")
    print("short control",percentage_short*100,"%")
    print("long control",percentage*100,"%")
    

print("############  Global results:  ############")
print("_Short control_")
print("Best result:",best_short*100,"%")
print("Worst result:",worst_short*100,"%")
print("Average",sum(results_short)/len(results_short)*100,"%")

print("_Long control_")
print("Best result:",best*100,"%")
print("Worst result:",worst*100,"%")
print("Average",sum(results)/len(results)*100,"%")
    

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
