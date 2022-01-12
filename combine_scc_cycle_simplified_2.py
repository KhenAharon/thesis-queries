#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 15:25:36 2019

@author: simsim
"""


from system import *

#first easy example
def create(model):        
    plant = process("plant",["p0","p1"],[],[],"p0")
    environment = process("environment",["e"+str(i) for i in [0,1,2,3,4,5,6,19,20,21,22,23,24]],[],[],"e0")
    
    pve = plant_environment("syst",plant,environment,model = model)
    
    pve.add_transition("a",["plant","environment"],[["p0"],["e0"]],[["p1"],["e1"]])
    pve.add_transition("d",["plant","environment"],[["p0"],["e0"]],[["p1"],["e19"]])
    pve.add_transition("f",["plant","environment"],[[],["e"+str(i) for i in [1,2,3,22,23,24]]],[[],["e"+str(i) for i in [2,3,4,23,24,22]]])
    pve.add_transition("x",["plant","environment"],[["p1"],["e"+str(i) for i in [4,19,20,21]]],[["p1"],["e"+str(i) for i in [5,20,21,22]]])
    pve.add_transition("y",["plant","environment"],[["p1"],["e"+str(i) for i in [5,19,20,21]]],[["p1"],["e"+str(i) for i in [6,20,21,22]]])
    pve.add_transition("z",["plant","environment"],[["p1"],["e"+str(i) for i in [6,19,20,21]]],[["p1"],["e"+str(i) for i in [4,20,21,22]]])

    pve.create_RNN()
    pve.reinitialize()
    return pve