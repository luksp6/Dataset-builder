import re

from abstracto.Runnable import Runnable

class Seccion(Runnable):

    _nombre:str

    def __init__(self, nombre):
        self._nombre = nombre

    def _extraer_seccion(self, contenido:str) -> str:
        pattern = rf"\*\*{re.escape(self._nombre)}\*\*\s*(.*?)(?=\n\s*\*\*|$)"
        match = re.search(pattern, contenido, re.DOTALL)
        return match.group(0).strip() if match else ""

    