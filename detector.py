#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:36:04 2019

@author: simsim
"""

from system import *

# another kind of example

def create(model):    
    plant = process("plant",["p0"],[],[],"p0")
    environment = process("environment",["e0","e1","e2","e3"],[],[],"e0")
    
    pve = plant_environment("syst",plant,environment,model = model)
    
    pve.add_transition("a",["plant","environment"],[["p0"],["e0"]],[["p0"],["e1"]])
    pve.add_transition("b",["plant","environment"],[["p0"],["e0"]],[["p0"],["e2"]])
    pve.add_transition("c",["plant","environment"],[["p0"],["e1"]],[["p0"],["e3"]])
    pve.add_transition("d",["plant","environment"],[["p0"],["e2"]],[["p0"],["e3"]])
    pve.add_transition("e",["plant","environment"],[["p0"],["e3"]],[["p0"],["e0"]])

    pve.create_RNN()
    pve.reinitialize()
    return pve



def strategy(environment:process):
    if environment.current_state == "e0":
        return random.choices(["a","b"],[60,40])[0]
    elif environment.current_state == "e1":
        return "c"
    elif environment.current_state == "e2":
        return "d"
    elif environment.current_state == "e3":
        return "e"