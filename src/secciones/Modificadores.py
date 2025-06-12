from secciones.Seccion import Seccion
from dataset.Entrada import Entrada

import re

class Modificadores(Seccion):

    def run(self, *args, **kwargs):
        content = args[0] if args else None
        filename = args[1] if args else ""

        print(content)
        if content:
            modificadores = self._extraer_modificadores(content)
            entradas = []
            for modificador in modificadores:
                nombre, valor = map(str.strip, modificador.split("|", 1))
                entradas.append(Entrada(
                        instruction=f"¿Cuánta {nombre} tiene un {filename}?",
                        input=content,
                        output=f"La {nombre} del {filename} es {valor}"))
            return entradas
        
    def _extraer_modificadores(self, tabla: str) -> list[str]:
        filas = re.findall(r"\|\s*([^\|]+?)\s*\|\s*([^\|]+?)\s*\|", tabla)
        return [
            f"{nombre.strip()} | {valor.strip()}"
            for nombre, valor in filas
            if nombre.strip() != "---" and valor.strip() != "---"
        ]