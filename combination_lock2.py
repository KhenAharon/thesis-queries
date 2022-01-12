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
#     plant = process("plant",["g0"],[],[],"g0")
#     environment = process("environment",["s0","s1","s2","s3","s4","s5","s6"],[],[],"s0")
#     
#     pve = plant_environment("syst",plant,environment,model = model)
#     
#     pve.add_transition("a",["plant","environment"],[["g0"],["s0","s1","s2","s3","s4","s5"]],[["g0"],["s1","s6","s3","s4","s6","s5"]])
#     pve.add_transition("b",["plant","environment"],[["g0"],["s0","s1","s2","s3","s4","s5"]],[["g0"],["s6","s2","s6","s6","s5","s5"]])
#     pve.add_transition("c",["plant","environment"],[[],["s6"]],[[],["s6"]])
# 
#     pve.create_RNN()
#     pve.reinitialize()
#     return pve
# =============================================================================



# =============================================================================
# #combination lock automaton abba
# def create(model):        
#     plant = process("plant",["g0","g1","g2","g3","g4"],[],[],"g0")
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


#combination lock automaton abaa
def create(model):        
    plant = process("plant",["g0"],[],[],"g0")
    environment = process("environment",["s0","s1","s2","s3","s4","s5"],[],[],"s0")
    
    pve = plant_environment("syst",plant,environment,model = model)
    
    pve.add_transition("a",["plant","environment"],[["g0"],["s0","s1","s2","s3","s4"]],[["g0"],["s1","s5","s3","s4","s4"]])
    pve.add_transition("b",["plant","environment"],[["g0"],["s0","s1","s2","s3","s4"]],[["g0"],["s5","s2","s5","s5","s4"]])
    pve.add_transition("f",["plant","environment"],[[],["s5"]],[[],["s5"]])

    pve.create_RNN()
    pve.reinitialize()
    return pve

