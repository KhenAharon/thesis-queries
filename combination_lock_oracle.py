#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:25:36 2019

@author: simsim
"""


from system import *

# =============================================================================
# #combination lock automaton abaab
# def create(model):        
#     plant = process("plant",["g0","g1","g2","g3","g4","g5"],[],[],"g0",update_states = "g5")
#     environment = process("environment",["s0","s1","s2","s3","s4","s5","s6"],[],[],"s0")
#     
#     pve = plant_environment("syst",plant,environment,model = model)
#     
#     pve.add_transition("a",["plant","environment"],[["g0","g1","g2","g3","g4"],["s0","s1","s2","s3","s4","s6"]],[["g1","g2","g3","g4","g5"],["s1","s6","s3","s4","s6","s6"]])
#     pve.add_transition("b",["plant","environment"],[["g0","g1","g2","g3","g4"],["s0","s1","s2","s3","s4","s6"]],[["g1","g2","g3","g4","g5"],["s6","s2","s6","s6","s5","s6"]])
#     pve.add_transition("c",["plant","environment"],[["g5"],["s5"]],[["g5"],["s5"]])
# 
#     pve.create_RNN()
#     pve.reinitialize()
#     return pve
# =============================================================================



# =============================================================================
# #combination lock automaton abaabb
# def create(model):        
#     plant = process("plant",["g0","g1","g2","g3","g4","g5","g6"],[],[],"g0",update_states = "g5")
#     environment = process("environment",["s0","s1","s2","s3","s4","s5","s6","s7"],[],[],"s0")
#     
#     pve = plant_environment("syst",plant,environment,model = model)
#     
#     pve.add_transition("a",["plant","environment"],[["g0","g1","g2","g3","g4","g5"],["s0","s1","s2","s3","s4","s5","s7"]],[["g1","g2","g3","g4","g5","g6"],["s1","s7","s3","s4","s7","s7","s7"]])
#     pve.add_transition("b",["plant","environment"],[["g0","g1","g2","g3","g4","g5"],["s0","s1","s2","s3","s4","s5","s7"]],[["g1","g2","g3","g4","g5","g6"],["s7","s2","s7","s7","s5","s6","s7"]])
#     pve.add_transition("c",["plant","environment"],[["g6"],["s6"]],[["g6"],["s6"]])
# 
#     pve.create_RNN()
#     pve.reinitialize()
#     return pve
# =============================================================================



# =============================================================================
# #combination lock automaton abba
# def create(model):        
#     plant = process("plant",["g0","g1","g2","g3","g4"],[],[],"g0", update_states = ["g4"])
#     environment = process("environment",["s0","s1","s2","s3","s4","s5"],[],[],"s0")
#     
#     pve = plant_environment("syst",plant,environment,model = model)
#     
#     pve.add_transition("a",["plant","environment"],[["g0","g1","g2","g3"],["s0","s1","s2","s3","s5"]],[["g1","g2","g3","g4"],["s1","s5","s5","s4","s5"]])
#     pve.add_transition("b",["plant","environment"],[["g0","g1","g2","g3"],["s0","s1","s2","s3","s5"]],[["g1","g2","g3","g4"],["s5","s2","s3","s5","s5"]])
#     pve.add_transition("c",["plant","environment"],[["g4"],["s4"]],[["g4"],["s4"]])
# 
#     pve.create_RNN()
#     pve.reinitialize()
#     return pve
# =============================================================================


#combination lock automaton aba
def create(model):        
    plant = process("plant",["g0","g1","g2","g3"],[],[],"g0",update_states = ["g3"])
    environment = process("environment",["s0","s1","s2","s3","s4"],[],[],"s0")

    dict = {
        "g0s0":"a",
        "g1s1":"b",
        "g2s2":"a"
    }

    pve = plant_environment("syst",plant,environment,model = model,oracle=dict)

    pve.add_transition("a",["plant","environment"],[["g0","g1","g2"],["s0","s1","s2","s4"]],[["g1","g2","g3"],["s1","s4","s3","s4"]])
    pve.add_transition("b",["plant","environment"],[["g0","g1","g2"],["s0","s1","s2","s4"]],[["g1","g2","g3"],["s4","s2","s4","s4"]])
    pve.add_transition("c",["plant","environment"],[["g3"],["s3"]],[["g3"],["s3"]])

    pve.create_RNN()
    pve.reinitialize()
    return pve

