#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:25:36 2019

@author: simsim
"""


from system import *

#first easy example
def create(model):        
    plant = process("plant",["p0"],[],[],"p0")
    environment = process("environment",["e0","e1","e2","e3","e4","e5"],[],[],"e0")
    
    pve = plant_environment("syst",plant,environment,model = model)
    
    pve.add_transition("a",["plant","environment"],[["p0"],["e0","e5"]],[["p0"],["e1","e0"]])
    pve.add_transition("b",["plant","environment"],[["p0"],["e1","e3"]],[["p0"],["e2","e4"]])
    pve.add_transition("c",["plant","environment"],[["p0"],["e2","e4"]],[["p0"],["e3","e5"]])

    pve.create_RNN()
    pve.reinitialize()
    return pve