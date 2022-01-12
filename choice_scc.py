#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:50:49 2019

@author: simsim
"""


from system import *
import itertools

# choose the least failures path (connected components with path to access them)
def create(model):        
    plant = process("plant",["g1","g2"],[],[],"g1",update_states = ["g1"])
    environment = process("environment",["e0",(l+str(i) for (l,i) in itertools.product("abcd",range(1,7)))],[],[],"e0")
    
    pve = plant_environment("syst",plant,environment,model = model)
    
    #pve.add_transition("a",["plant","environment"],[["g1"],["e0"]],[["g2"],["a1"]])
    pve.add_transition("b",["plant","environment"],[["g1"],["e0"]],[["g2"],["b1"]])
    pve.add_transition("c",["plant","environment"],[["g1"],["e0"]],[["g2"],["c1"]])
    pve.add_transition("d",["plant","environment"],[["g1"],["e0"]],[["g2"],["d1"]])
    pve.add_transition("e",["plant","environment"],[["g2"],["a1","a2","a3","b1","b2","b4","c1","c4","c5","d4","d5","d6"]],[["g2"],["a2","a3","a4","b2","b3","b5","c2","c5","c6","d5","d6","d4"]])
    pve.add_transition("f",["plant","environment"],[[],["a4","a5","a6","b3","b5","b6","c2","c3","c6","d1","d2","d3"]],[[],["a5","a6","a4","b4","b6","b4","c3","c4","c4","d2","d3","d4"]])

    pve.create_RNN()
    pve.reinitialize()
    return pve

