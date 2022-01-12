#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:50:49 2019

@author: simsim
"""


from system import *

# choose the least failures path
def create(model):        
    plant = process("plant",["g1"],[],[],"g1",update_states = ["g1"])
    environment = process("environment",["e1","e2","e3","e4","e5","e6"],[],[],"e1")
    
    pve = plant_environment("syst",plant,environment,model = model)
    
    pve.add_transition("a",["plant","environment"],[["g1"],["e1","e4"]],[["g1"],["e2","e5"]])
    pve.add_transition("b",["plant","environment"],[["g1"],["e1","e2"]],[["g1"],["e4","e3"]])
    pve.add_transition("c",["plant","environment"],[[],["e3","e5","e6"]],[[],["e1","e6","e1"]])

    pve.create_RNN()
    pve.reinitialize()
    return pve


# =============================================================================
# # choose the least failures path
# def create(model):        
#     plant = process("plant",["g1","g2"],[],[],"g1")
#     environment = process("environment",["e1","e2","e3","e4"],[],[],"e1")
#     
#     pve = plant_environment("syst",plant,environment,model = model)
#     
#     pve.add_transition("a",["plant","environment"],[["g1"],["e1"]],[["g2"],["e2"]])
#     pve.add_transition("b",["plant","environment"],[["g1"],["e1"]],[["g2"],["e3"]])
#     pve.add_transition("c",["plant","environment"],[[],["e3"]],[[],["e4"]])
#     pve.add_transition("d",["plant","environment"],[["g2"],["e2","e4"]],[["g1"],["e1","e1"]])
# 
#     pve.create_RNN()
#     pve.reinitialize()
#     return pve
# =============================================================================
