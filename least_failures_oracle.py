from system import *
# choose the least failures path
def create(model):        
    plant = process("plant",["g1","g2"],[],[],"g1")
    environment = process("environment",["e1","e2","e3","e4"],[],[],"e1")

    dict = {
        "g1e1": "a"
    }
    pve = plant_environment("syst",plant,environment,model = model, oracle=dict)
    
    pve.add_transition("a",["plant","environment"],[["g1"],["e1"]],[["g2"],["e2"]])
    pve.add_transition("b",["plant","environment"],[["g1"],["e1"]],[["g2"],["e3"]])
    pve.add_transition("c",["plant","environment"],[[],["e2","e3","e5"]],[[],["e4","e5","e4"]])
    pve.add_transition("d",["plant","environment"],[["g2"],["e4"]],[["g1"],["e1"]])

    pve.create_RNN()
    pve.reinitialize()
    return pve
