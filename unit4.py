from system import *

def create(model):
    plant = process("plant",["g1"],[],[],"g1")
    environment = process("environment",["e1"],[],[],"e1")
    
    pve = plant_environment("syst",plant,environment,model = model)
    
    pve.add_transition("a",["plant","environment"],[["g1"],[]],[["g1"],[]])
    pve.add_transition("b",["plant","environment"],[[],["e1"]],[[],["e1"]])

    pve.create_RNN()
    pve.reinitialize()
    return pve


