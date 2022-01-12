import random
import dynet as dy
import numpy as np


def softmax(l):
    soft = l.copy()
    expl = np.exp(l)
    for i in range(len(l)):
        soft[i] = expl[i] / np.sum(expl)
    return soft


class Transition:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end


class process:
    # finite automaton where transitions can be shared with other processes.
    def __init__(self, name, states=[], internal=[], shared=[], initial_state=None, update_states=[]):
        self.name = name
        self.states = states  # list of names of the states.
        self.initial_state = initial_state
        self.current_state = initial_state
        self.internal = internal  # transitions that are specific to the process.
        self.shared = shared  # transitions of both processes, initialized empty and filled by add_transition.
        self.internal_transitions = []  # same as above, but the names of the transitions.
        self.shared_transitions = []  # initialized as empty lists that will be filled using list_transitions.
        self.all_transitions = []  # all_transitions will be updated as the concatenation of the two previous lists.
        self.update_states = update_states  # only states on which a learning pass can be done. empty = all states.

    def add_state(self, name):
        self.states.append(name)
        if self.current_state is None:
            self.initial_state = name
            self.current_state = name
            
    def define_update_state(self, name):
        if name not in self.states:
            raise ValueError("no state named", name)
        else:
            self.update_states.append(name)  # new update possible state, if it is a valid state of the process.
            
    def list_update_states(self, name_list):
        for name in name_list:
            self.define_update_state(name)  # define a list of update possible states.
            
    def reinitialize(self):
        self.current_state = self.initial_state  # return to initial state.
        if self.update_states is []:  # if list of update states is undefined, all states will be updated.
            self.list_update_states(self.states)
            
    def add_transition(self, name, start, end, internal=True):
        if internal:
            self.internal.append(Transition(name, start, end))  # add a new transition from state start to state end.
        else:
            self.shared.append(Transition(name, start, end))
        
    def trigger_transition(self, tr_name):
        try:  # move the process according to the transition tr_name, printing an error if not possible.
            self.current_state = next(tr.end for tr in self.internal if tr_name == tr.name and tr.start == self.current_state)
        except StopIteration:
            try:  # we trigger it in internal, but if not exist, in shared.
                self.current_state = next(tr.end for tr in self.shared if tr_name == tr.name and tr.start == self.current_state)
            except StopIteration:
                print("No transition named", tr_name, "from state", self.current_state)
      
    def list_transitions(self):
        for tr in self.internal:
            if tr.name not in self.internal_transitions:  # update the names of currently defined transitions.
                self.internal_transitions.append(tr.name)
        for tr in self.shared:
            if tr.name not in self.shared_transitions:
                self.shared_transitions.append(tr.name)
        self.all_transitions = self.internal_transitions + self.shared_transitions
        
    def available_transitions(self):
        available = []
        for tr in self.internal + self.shared:
            if tr.name not in available and tr.start == self.current_state:
                available.append(tr.name)
        return available  # returns a list of names of transitions that can be triggered in the current state.


class System:
    def __init__(self, name, processes):  # a system is a compound of processes.
        self.name = name
        self.processes = processes  # a list of the processes in the compound.
        self.shared_transitions = []  # list of the shared transitions of the different processes
        self.networks = None  # Neural networks associated to the processes (listed in the same order as the processes)
        self.R = None  # R, bias, parameters and trainer are respective lists of the parameters for the NNs
        self.bias = None
        self.parameters = None
        self.trainer = None
        
    def reinitialize(self):
        for pr in self.processes:  # reinitialize all processes in the system
            pr.reinitialize()
    
    def get_process(self, name):  # returns the process with that name
        return next(proc for proc in self.processes if name == proc.name)
    
    def add_process(self, process):
        self.processes.append(process)  # add a new process to the system
        
    def add_transition(self, name, pr_list, start_list, end_list):
        if len(pr_list) == 1:   # add a new transition shared between processes in pr_list
            is_internal = True  # for process pr_list[i], the transition goes from state start_list[i] to state end_list[i]
        else:
            is_internal = False
            self.shared_transitions.append((name, pr_list, start_list, end_list))  # parameters aren't changed.
        for i in range(len(pr_list)):
            start = start_list[i]
            end = end_list[i]
            for j in range(len(start)):
                self.get_process(pr_list[i]).add_transition(name, start[j], end[j], is_internal)


class plant_environment(System):
    def __init__(self, name, plant: process, environment: process, model="correctly_guess", layers=1, hidden_dim=5, oracle={}):
        self.plant = plant  # define the system with processes plant and environment
        self.environment = environment
        System.__init__(self, name, [self.plant, self.environment])
        self.plant.list_transitions()
        self.layers = layers  # parameters of the neural network that will be used by the plant
        self.hidden_dim = hidden_dim
        self.model = model
        self.oracle = oracle

    def create_RNN(self):
        self.plant.list_transitions()
        self.parameters = dy.ParameterCollection()
        input_dim = (len(self.plant.internal_transitions)+len(self.plant.shared_transitions))*len(self.plant.states)
        output_dim = len(self.plant.all_transitions)
        self.R = self.parameters.add_parameters((output_dim,self.hidden_dim))
        self.bias = self.parameters.add_parameters((output_dim))
        self.network = dy.VanillaLSTMBuilder(self.layers,input_dim,self.hidden_dim,self.parameters,forget_bias = 1.0)
        self.trainer = dy.SimpleSGDTrainer(self.parameters)
    
    def RNN_input(self, last_transition):
        v = [0]*((len(self.plant.internal_transitions)+len(self.plant.shared_transitions))*len(self.plant.states))
        i = next(i for i in range(len(self.plant.states)) if self.plant.states[i] == self.plant.current_state)
        if last_transition is not None:
            if last_transition[:4] == "fail":
                failed_action = ""
                current_char_index = 5
                while last_transition[current_char_index] != ")":
                        failed_action += last_transition[current_char_index]
                        current_char_index += 1
                j = next(j for j in range(len(self.plant.shared_transitions)) if failed_action == self.plant.shared_transitions[j])
                v[((len(self.plant.internal_transitions) + j))*len(self.plant.states)+i] = -1    
            else:
                j = next(j for j in range(len(self.plant.all_transitions)) if last_transition == self.plant.all_transitions[j])
                v[(len(self.plant.internal_transitions) + j)*len(self.plant.states)+i] = 1
        return v       

    def RNN_output(self, output):
        available = self.plant.available_transitions()
        if len(available) > 1:
            next_transition = random.choices(available,
                                         ([output[i] for i,tr in enumerate(self.plant.all_transitions) if tr in available]))[0]
        else:
            next_transition = available[0]
        return next_transition

    def check_transition(self, plant_transition):
        available = self.environment.available_transitions()
        if plant_transition in available:
            return [plant_transition, plant_transition]
        else:
            return ["fail("+plant_transition+")", random.choice(available)]

    def trigger_transition(self,transition):
        if transition[0][:4] != "fail":
            self.plant.trigger_transition(transition[0])
        self.environment.trigger_transition(transition[1])

    def random_transition(self):
        plant_action = random.choice([tr for tr in self.plant.internal + self.plant.shared if tr.start == self.plant.current_state]).name
        environment_action = random.choice([tr for tr in self.environment.internal + self.environment.shared if tr.start == self.environment.current_state]).name
        return [plant_action,environment_action]

    def generate_random_execution(self, steps):
        execution = []
        for s in range(steps):
            tr = self.random_transition()
            tr = self.check_transition(tr[0])
            self.trigger_transition(tr)
            execution.append(tr)
        return execution

    def generate_controlled_execution(self, steps):
        execution = []
        dy.renew_cg()
        state = self.network.initial_state()
        last_transition = None
        for step in range(steps):
            network_input = self.RNN_input(last_transition)
            input_vector = dy.inputVector(network_input)
            state = state.add_input(input_vector)
            output = dy.softmax(self.R * state.output() + self.bias).value()

            oracle_state = self.plant.current_state + self.environment.current_state
            if oracle_state in self.oracle:
                next_plant_action = self.oracle[oracle_state]
            else:
                next_plant_action = self.RNN_output(output)

            tr = self.check_transition(next_plant_action)
            self.trigger_transition(tr)
            execution.append(tr)
            last_transition = tr[0]
        return execution

    def generate_training_execution(self, steps=50, lookahead=1, epsilon=0):
        rollout = [None] * (lookahead + 1)
        rollout_error = [None] * (lookahead + 1)

        def rollout_update(rollout, new_state):
            return rollout[1:]+[new_state]

        def rollout_error_update(rollout_errors, error):
            return rollout_errors[1:]+[error]

        def get_rollouts(tr, rollout, rollout_error):
            plant_tr = tr[0]
            if plant_tr[:4] == "fail":
                plant_tr = plant_tr[5]
                rollout_error = rollout_error_update(rollout_error, True)
            else:
                rollout_error = rollout_error_update(rollout_error, False)
            # store information about the output to compute the loss
            rollout = rollout_update(rollout, (output, self.plant.available_transitions(), plant_tr))
            i_train = next(i for i in range(len(rollout)) if rollout[i] is not None)
            return rollout, rollout_error, i_train

        def get_loss(p: process, rollout, rollout_error, i_train, loss):
            if rollout[i_train] is not None:
                nb_failures = rollout_error.count(True)  # count successes and failures in lookahead window
                nb_successes = 1 + lookahead - nb_failures
                for i in range(len(self.plant.all_transitions)):
                    if self.plant.all_transitions[i] in rollout[i_train][1]:
                        if self.plant.all_transitions[i] == rollout[i_train][2]:  # chosen action
                            loss.append((nb_successes/(lookahead+1))*dy.pickneglogsoftmax(rollout[i_train][0],i))
                        else:  # not chosen action
                            loss.append((nb_failures/(lookahead+1))*dy.pickneglogsoftmax(rollout[i_train][0],i))
            return loss

        execution = []
        last_transition = None
        dy.renew_cg()
        state = self.network.initial_state()
        loss = [dy.scalarInput(0)]
        for step in range(steps):
            network_input = self.RNN_input(last_transition)
            input_vector = dy.inputVector(network_input)
            state = state.add_input(input_vector)
            output = dy.softmax(self.R*state.output() + self.bias)
            output_value = output.value()

            oracle_state = self.plant.current_state + self.environment.current_state
            if oracle_state in self.oracle:
                next_plant_action = self.oracle[oracle_state]

            elif random.random() < epsilon:
                next_plant_action = self.random_transition()[0]
            else:
                next_plant_action = self.RNN_output(output_value)
            tr = self.check_transition(next_plant_action)
            # update the information for the loss with lookahead: remember the successes and failures
            rollout, rollout_error, i_train = get_rollouts(tr, rollout, rollout_error)
            loss = get_loss(self.plant, rollout, rollout_error, i_train, loss)

            loss_compute = dy.esum(loss)
            loss_compute.value()
            loss_compute.backward()
            self.trainer.update()
            loss = [dy.scalarInput(0)]
            self.trigger_transition(tr)
            execution.append(tr)
            last_transition = tr[0]
        return execution