#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:50:49 2019

@author: simsim
"""


from system import *

# matching coins game (but not adversarial...)

def custom_strategy(environment):
    if environment.current_state == "e1":
        if random.random() < 0.3:
            return "a"
        else:
            return "b"
    else:
        if environment.current_state == "e2":
            return "c"
        else:
            return "d"


def create(model):
    dict = {
        "g1e1":"d"
    }
    plant = process("plant",["g1"],[],[],"g1",update_states = ["g1"],dict=dict)
    environment = process("environment",["e1","e2","e3"],[],[],"e1",dict={})
    
    pve = plant_environment(plant,environment,model = model)
    
    pve.add_transition("a",["plant","environment"],[[],["e2"]],[[],["e1"]])
    pve.add_transition("c",["plant","environment"],[["g1"],["e1"]],[["g1"],["e2"]])
    pve.add_transition("d",["plant","environment"],[["g1"],["e1","e3"]],[["g1"],["e3","e1"]])

    pve.create_RNN()
    pve.reinitialize()
    return pve


