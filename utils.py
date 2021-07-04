# helper class for all tools and needed classes

symbols = {
    "RIGHT": "R",
    "LEFT": "L",
    "BLANK": "~"
}


class Tape:
    def __init__(self):
        self.positive_tape = TapeList()
        self.negative_tape = TapeList()

    def set(self, index, char):
        if index < 0:
            self.negative_tape.set(-index - 1, char)
        else:
            self.positive_tape.set(index, char)


    def get(self, index):
        if index < 0:
            return self.negative_tape.get(index)
        else:
            return self.positive_tape.get(index)

    def clear_tape(self):
        self.positive_tape.clear()
        self.negative_tape.clear()

    def __str__(self):
        return ''.join(list(reversed(str(self.negative_tape)))) + str(self.positive_tape)



class TapeList:
    def __init__(self):
        self.array = []

    def set(self, index, char):
        if index >= len(self.array):
            self.array.extend([symbols["BLANK"] for _ in range(index - len(self.array) + 1)])

        self.array[index] = char


    def get(self, index):
        if index < len(self.array):
            return self.array[index]
        else:
            return symbols["BLANK"]

    def clear(self):
        self.array.clear()

    def __len__(self):
        return len(self.array)

    def __str__(self):
        return ''.join(self.array)


class State:
    def __init__(self, index, isFinal):
        self.index = index
        self.isFinal = isFinal

    def __str__(self):
        return 'q%d'%self.index 


    
class Validator:

    @staticmethod
    def validate_config(transitions, tape_alphabets, states_count, final_states):
        Validator.validate_transitions(transitions, tape_alphabets, states_count)

        if not states_count:
            raise ValueError("Number of states could not be 0!")

        for final_state in final_states:
            if final_state.index >= states_count or final_state.index < 0:
                raise ValueError("Invalid final state index!")

         
    @staticmethod
    def validate_transitions(transitions, tape_alphabets, states_count):
        for transition in transitions:
            if transition['readChar'] not in tape_alphabets or transition['writeChar'] not in tape_alphabets:
                raise ValueError('Invalid symbol, not a member of tape alphabets!', transition)

        
        for transition in transitions:
            if transition['currentState'] >= states_count or transition['currentState'] < 0:
                raise ValueError('Invalid transition state!')

            if transition['nextState'] >= states_count or transition['nextState'] < 0:
                raise ValueError('Invalid transition state!')
            

        for transition in transitions:
            if transition['direction'] not in symbols.values():
                raise ValueError('Invalid transition direction!')


    @staticmethod
    def validate_input(alphabets, string):
        for char in string:
            if char not in alphabets:
                return False

        return True
