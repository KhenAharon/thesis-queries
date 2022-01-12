import random
import dynet as dy
import numpy as np

# to use a particular example, uncomment its line and comment all the others

# from cycle_abc import *
# from cycle_random_abc import *
# from cycle_random_abc_anchor1 import *
# from cycle_random_abc_anchor2 import *
# from cycle_random_abc_anchor3 import *
# from cycle_random_abc_memory import *
# from detector import *
# from cycle_abb import *
# from schedule import *
# from cases import *
# from unlucky import *
# from strategy import *
# from strategy2 import *
# from cycle_abcbc import *
# from cycle_abcbca import *
# from combination_lock import *
# from combination_lock2 import *
# from choice import *
# from choice2 import *
# from choice3 import *
# from choice4 import *
# from choice5 import *
# from choice6 import *
# from choice_tournament import *
# from choice_scc import *
# from least_failures import *
# from good_failure import *
# from choice_and_good_failure import *
# from match_coins import *
# from matching_simplified import *
# from combine_scc_cycle import *
# from combine_scc_cycle_simplified import *
# from combine_scc_cycle_simplified_2 import *
from combine_schedule_cycle import *

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


def default_lookahead(history):
    return 0


def random_lookahead(history, average=3, variation=2):
    return random.randint(average - 2, average + 2)


# =============================================================================
# # debugging
# pve = create(model)
# failures = []
# for training in range(1):
#     pve.reinitialize()
#     pve.generate_random_execution(30)
#     print("#########################")
# =============================================================================







        
        
#another training scheme : learn sequences that are longer and longer
    
# T is the number of "epochs" we'll do the training on; if T is iterated on a
# list of numbers, we'll do a different training with each number of epochs chosen
    
results = []
for tests in range(100):
    

    
    for T in [100]: 
        
        # L is the max length of training sequences. When L has value 50 (for example)
        # then an epoch will consist in generating a training sequence of length 1,
        # then another training sequence of length 2, then another one of length 3,
        # and so on until generating an execution of length 50. If L is iterated over a 
        # list of numbers, same as with T: a different training will be done with every
        # value of L
        for L in [8]:
            pve = create(model) # this generates the system and environment
            
            
            for runs in range(4):
                
                #print("run",runs+1)
            
                for (lookahead,epsilon) in [(5,0),(0,0)]:
                    #print("lookahead",lookahead,"and epsilon",epsilon)
                
                
                    # iterating over the epochs
                    for training in range(T):
                        
                        #iterating over the training sequences from length 1 to length L
                        for length in range(1,L):
                            
                            pve.reinitialize() #return system and environment to initial states
                            
                            # Now we generate a training sequence.
                            pve.generate_training_execution(length,print_probs = False,random_exploration = False,lookahead = lookahead,epsilon = epsilon,new_loss = True,environment_strategy = None,compare_loss = False,discount_loss = False,discount_factor = 1)
                    
            
                    
                    
                    
                    
                    
            failures = []
            
            # this for loop takes the trained network, and uses it to generate an execution
            # (without training). C and L_C (defined above in my code, I chose C = 50 and L_C = 100)
            # are respectively the number of generated executions, and the length of these.
            # For every execution generated this way, I count the number of failures, and
            # print in the end the value of T, the value of L, and the average percentage
            # of failures in my executions. A low percentage means the training worked well!
            for control in range(C):
                pve.reinitialize()
                execution = pve.generate_controlled_execution(L_C,print_probs = False)#,environment_strategy = custom_strategy)
                #print("____________")
                failures.append(count_failures(execution))
            percentage = 0
            for i in range(C):
                percentage += failures[i]/L_C
            percentage /= C
            results.append(percentage*100)
            print("(",T,",",L,")",percentage*100,"%")

print("(average)",sum(results)/len(results))
    

def run(pve, steps = 50, print_first=False, print_probs=False):
    pve.reinitialize()
    if print_first:
        print(pve.generate_controlled_execution(steps, print_probs=print_probs)[0][0])
    else:
        print(pve.generate_controlled_execution(steps, print_probs=print_probs))


def count_results_within_bound(results, bound):
    return len([r for r in results if r < bound])


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
