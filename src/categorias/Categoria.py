from secciones.Seccion import Seccion

class Categoria():
        
    _secciones:list[Seccion]

    def __init__(self, secciones:list[Seccion]):
        self._secciones = secciones

    def __iter__(self):
        return iter(self._secciones)
    
    def get_num_secciones(self) -> int:
        return len(self._secciones)