class Entrada:

    _instruction:str
    _input:str
    _output:str

    def __init__(self, instruction=None, input=None, output=None, from_dict=None):
        if from_dict:
            self._instruction = from_dict.get("instruction", "")
            self._input = from_dict.get("input", "")
            self._output = from_dict.get("output", "")
        else:
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
        return str(self.to_dict())
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self) -> dict:
        return {
            "instruction": self._instruction,
            "input": self._input,
            "output": self._output
        }