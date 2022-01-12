#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:50:49 2019

@author: simsim
"""


from system import *

# choose the path with a failure at the beginning
def create(model):        
    plant = process("plant",["s1","s2","s3"],[],[],"s1")
    environment = process("environment",["e1","e2","e3"],[],[],"e1")
    
    pve = plant_environment("syst",plant,environment,model = model)
    
    pve.add_transition("a",["plant","environment"],[["s1"],["e1"]],[["s2"],["e2"]])
    pve.add_transition("b",["plant","environment"],[["s1","s3"],["e2","e3"]],[["s3","s3"],["e3","e3"]])
    pve.add_transition("c",["plant","environment"],[["s2"],[]],[["s2"],[]])

    pve.create_RNN()
    pve.reinitialize()
    return pve


