from utils import *

class TuringMachine:

    def __init__(self, config):
        self.config = config
        self.header = 0
        self.current_state = None
        self.tape = Tape()

        self.max_attempts = self.config["maxAttempts"]
        self.transitions = self.config["transitions"]

        self.states = []
        self.final_states = []
        self.init_states()

        self.initial_state = self.states[0]
        self.alphabets = self.config["alphabets"]

        alphabets_set = set(self.alphabets)
        tape_alphabets_set = set(self.config["tapeAlphabets"])
        self.tape_alphabets = list(alphabets_set.union(tape_alphabets_set))
        self.tape_alphabets.append(symbols["BLANK"])

        Validator.validate_config(self.transitions, self.tape_alphabets, len(self.states), self.final_states)


    def init_states(self):

        for i in range(self.config["statesCount"]):
            new_state = State(i, False)
            self.states.append(new_state)

        for i in self.config["finalStates"]:
            self.states[i].isFinal = True
            self.final_states.append(self.states[i])


    # applying the turing machine process to input
    def process_input(self, string):
        self.reset()
        counter = 0
        
        for i, char in enumerate(string):
            self.tape.set(i, char)

        currentTransition = self.findTransition(self.current_state.index, self.tape.get(self.header))
        print(self.getRepr(), end=' ')

        while currentTransition != None:
            if counter > self.max_attempts:
                counter += 1
                break
            
            self.tape.set(self.header, currentTransition["writeChar"])

            if currentTransition["direction"] == symbols["RIGHT"]:
                self.header += 1
            else:
                self.header -= 1

            self.current_state = self.states[currentTransition["nextState"]]
            currentTransition = self.findTransition(self.current_state.index, self.tape.get(self.header))
            print("⊢ " + self.getRepr(), end=' ')

        if counter > self.max_attempts:
            print("reached the maximum number of attempts, please modify turing_config.json")
        elif self.current_state.isFinal:
            print("\naccepted")
        else:
            print("\nrejected")


    # outputting a representation of process at each step in the required format
    def getRepr(self):
        string = list(str(self.tape))
        string.insert(len(self.tape.negative_tape) + self.header, str(self.current_state))
        if self.header == len(self.tape.positive_tape):
            string.append(symbols["BLANK"])
        return "(%s)"%''.join(string)


    def findTransition(self, transition_state, char):
        for transition in self.transitions:
            if transition['readChar'] == char and transition['currentState'] == transition_state:
                return transition
        return None


    def reset(self):
        self.tape.clear_tape()
        self.current_state = self.initial_state
        self.header = 0


    # formatting output to be nicer
    def __repr__(self):
        qs = 'Q = {'
        for i in range(len(self.states) - 1):
            qs += 'q%d, '%i
        qs += 'q%d}\n'%(len(self.states) - 1)

        fs = 'F = {'
        for i in range(len(self.final_states) - 1):
            fs += 'q%d, '%(self.final_states[i].index)
        fs += 'q%d}\n'%(self.final_states[-1].index)

        ds = ''
        for transition in self.transitions:
            ds += "δ(q%d, %c) = (q%d, %c, %c)\n"\
            %(transition['currentState'], transition['readChar'], transition['nextState'], transition['writeChar'], transition['direction'])

        ss = '∑ = {'
        arr = self.config['alphabets']
        for i in range(len(arr) - 1):
            ss += '%s, '%arr[i]
        ss += '%s}\n'%arr[-1]

        ts = 'Γ = {'
        arr = self.tape_alphabets
        for i in range(len(arr) - 1):
            ts += '%s, '%arr[i]
        ts += '%s}\n\n'%arr[-1]

        return 'Turing Machine:\n\n' + \
               "M = {Q, ∑, Γ, q0, F, δ}\n" + qs + fs + ss + ts + ds
    