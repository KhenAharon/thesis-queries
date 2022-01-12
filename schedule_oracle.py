#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:25:36 2019

@author: simsim
"""


from system import *

#schedule from Doron's paper
def create(model):
    dict = {
        "g1e1": "b"
    }
    plant = process("plant",["g1","g2","g3"],[],[],"g1")
    environment = process("environment",["e1","e2","e3","e4"],[],[],"e1")
    
    pve = plant_environment("syst",plant,environment,model, oracle=dict)
    
    pve.add_transition("a",["plant","environment"],[["g1"],["e1","e4"]],[["g2"],["e3","e3"]])
    pve.add_transition("b",["plant","environment"],[["g1","g2"],["e1"]],[["g3","g1"],["e2"]])
    pve.add_transition("c",["plant","environment"],[["g3"],["e2","e3"]],[["g1"],["e1","e4"]])

    pve.create_RNN()
    pve.reinitialize()
    return pve