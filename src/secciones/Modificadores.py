from secciones.Seccion import Seccion
from dataset.Entrada import Entrada

import re

class Modificadores(Seccion):

    def run(self, *args, **kwargs):
        content = args[0] if args else None
        filename = args[1] if args else ""
        return None

        equipamiento = self._extraer_equipamiento(content)
        print(equipamiento)

        if content:
            return [Entrada(
                    instruction=f"¿Cuál es el mejor equipamiento que puede usar un {filename}?",
                    input=content,
                    output=f"Un buen {filename} viste {equipamiento}")]
        else:
            return None
        
    def _extraer_equipamiento(self, bloque: str) -> list:
        equip = re.findall(r"\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|", bloque)
        nombres = [nombre for _, nombre, _ in equip if nombre.lower() != "nombre"]
        return list(dict.fromkeys(nombres))