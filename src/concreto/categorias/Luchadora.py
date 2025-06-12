from abstracto.Seccion import Seccion
from concreto.categorias.Categoria import Categoria

class Luchadora(Categoria):

    def __init__(self, secciones:list[Seccion]):
        self._secciones = secciones

