from abc import ABC, abstractmethod

class Dataset(ABC):

    _nombre:str
    _entradas:list

    def __init__(self, nombre:str):
        self._nombre = nombre
        self._entradas = list()

    def add(self, entrada):
        self._entradas.append(entrada)

    @abstractmethod
    def to_json(self, output_dir):
        raise NotImplementedError