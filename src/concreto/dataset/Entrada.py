class Entrada:

    _instruction:str
    _input:str
    _output:str

    def __init__(self, instruction, input, output):
        self._instruction = instruction
        self._input = input
        self._output = output

    def get_instruction(self):
        return self._instruction
    
    def get_input(self):
        return self._input
    
    def get_output(self):
        return self._output
    
    def __str__(self):
        return f"instruction: {self._instruction},\n input: {self._input},\n output: {self._output}"
    
    def __repr__(self):
        return self.__str__()