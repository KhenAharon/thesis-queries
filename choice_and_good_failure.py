#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:50:49 2019

@author: simsim
"""


#TODO !!!

from system import *

# choose the least failures path, only on the first step
def create(model):        
    plant = process("plant",["g1","g2","g3","g4"],[],[],"g1",update_states = ["g1","g2","g4"])
    environment = process("environment",["e1","e2"],[],[],"e1")
    
    pve = plant_environment("syst",plant,environment,model = model)
    
    pve.add_transition("a",["plant","environment"],[["g1"],["e1"]],[["g2"],["e2"]])
    pve.add_transition("b",["plant","environment"],[["g1"],["e1"]],[["g3"],["e2"]])
    pve.add_transition("c",["plant","environment"],[["g2","g3","g4"],[]],[["g3","g2","g4"],[]])
    pve.add_transition("d",["plant","environment"],[[],["e2"]],[[],["e2"]])

    pve.create_RNN()
    pve.reinitialize()
    return pve
