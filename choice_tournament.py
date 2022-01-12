#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:50:49 2019

@author: simsim
"""


from system import *

cycles = ["cdd","ccd"]

def count_d(cycle):
    count = 0
    for l in cycle:
        if l == "d":
            count += 1
    return count
    
plant_states = ["g1"] + ["a"+str(i+1) for i in range(count_d(cycles[0]))] + ["b"+str(i+1) for i in range(count_d(cycles[1]))]
env_states = ["e"+str(i+1) for i in range(1 + len(cycles[0]) + len(cycles[1]))]

# choose the least failures path
def create(model):        
    plant = process("plant",plant_states,[],[],"g1",update_states = ["g1"])
    environment = process("environment",env_states,[],[],"e1")
    
    pve = plant_environment("syst",plant,environment,model = model)
    
    pve.add_transition("a",["plant","environment"],[["g1"],["e1"]],[["a1"],["e2"]])
    pve.add_transition("b",["plant","environment"],[["g1"],["e1"]],[["b1"],["e"+str(2+len(cycles[0]))]])
    pve.add_transition("c",["plant","environment"],[[],["e"+str(i+2) for i in range(len(cycles[0])) if cycles[0][i] == "c"]+["e"+str(i+2+len(cycles[0])) for i in range(len(cycles[1])) if cycles[1][i] == "c"]],[[],["e"+str(i+3) for i in range(len(cycles[0])-1) if cycles[0][i] == "c"]+(["e1"] if cycles[0][-1] == "c" else [])+["e"+str(i+3+len(cycles[1])) for i in range(len(cycles[1])-1) if cycles[1][i] == "c"]+(["e1"] if cycles[1][-1] == "c" else [])])
    pve.add_transition("d",["plant","environment"],[(["a"+str(i+1) for i in range(count_d(cycles[0]))])+(["b"+str(i+1) for i in range(count_d(cycles[1]))]),["e"+str(i+2) for i in range(len(cycles[0])) if cycles[0][i] == "d"]+["e"+str(i+2+len(cycles[0])) for i in range(len(cycles[1])) if cycles[1][i] == "d"]],[(["a"+str(i+2) for i in range(count_d(cycles[0])-1)]+["g1"])+(["b"+str(i+2) for i in range(count_d(cycles[1])-1)]+["g1"]),["e"+str(i+3) for i in range(len(cycles[0])-1) if cycles[0][i] == "d"]+(["e1"] if cycles[0][-1] == "d" else [])+["e"+str(i+3+len(cycles[1])) for i in range(len(cycles[1])-1) if cycles[1][i] == "d"]+(["e1"] if cycles[1][-1] == "d" else [])])

    pve.create_RNN()
    pve.reinitialize()
    return pve


pve = create("any_available")

print(pve.shared_transitions) 




