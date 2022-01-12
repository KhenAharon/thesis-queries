#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:25:36 2019

@author: simsim
"""


from system import *

#mixup of the schedule and permitted (cycle_abc) from the paper
def create(model):        
    plant = process("plant",["g1","g2"],[],[],"g1")
    environment = process("environment",["e1","e2","e3","e4"],[],[],"e1")
    
    pve = plant_environment("syst",plant,environment,model = model)
    
    pve.add_transition("a",["plant","environment"],[["g1"],["e1","e4"]],[["g2"],["e4","e4"]])
    pve.add_transition("b",["plant","environment"],[["g1","g2"],["e1"]],[["g1","g2"],["e2"]])
    pve.add_transition("c",["plant","environment"],[["g1"],["e2"]],[["g1"],["e3"]])
    pve.add_transition("d",["plant","environment"],[["g1"],["e3"]],[["g1"],["e1"]])

    pve.create_RNN()
    pve.reinitialize()
    return pve




# =============================================================================
# #second version (harder, every a for the environment leads to the sink state)
# def create(model):        
#     plant = process("plant",["g1","g2"],[],[],"g1")
#     environment = process("environment",["e1","e2","e3","e4"],[],[],"e1")
#     
#     pve = plant_environment("syst",plant,environment,model = model)
#     
#     pve.add_transition("a",["plant","environment"],[["g1"],["e1","e2","e3","e4"]],[["g2"],["e4","e4","e4","e4"]])
#     pve.add_transition("b",["plant","environment"],[["g1","g2"],["e1"]],[["g1","g2"],["e2"]])
#     pve.add_transition("c",["plant","environment"],[["g1"],["e2"]],[["g1"],["e3"]])
#     pve.add_transition("d",["plant","environment"],[["g1"],["e3"]],[["g1"],["e1"]])
# 
#     pve.create_RNN()
#     pve.reinitialize()
#     return pve
# =============================================================================
