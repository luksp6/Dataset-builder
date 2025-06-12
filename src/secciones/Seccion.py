import re

from utils.Runnable import Runnable

class Seccion(Runnable):

    _nombre:str

    def __init__(self, nombre):
        self._nombre = nombre