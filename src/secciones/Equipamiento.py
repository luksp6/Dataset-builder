from secciones.Seccion import Seccion
from dataset.Entrada import Entrada

import re

class Equipamiento(Seccion):

    def run(self, *args, **kwargs):
        content = args[0] if args else None
        filename = args[1] if args else ""

        equipamiento = self._extraer_equipamiento(content)
        if equipamiento:
            return [Entrada(
                    instruction=f"¿Cuál es el mejor equipamiento que puede usar un {filename}?",
                    input=content,
                    output=f"Un buen {filename} viste {', '.join(equipamiento)}")]
        else:
            return None
        
    def _extraer_equipamiento(self, bloque: str) -> list[str]:
        # Separar la primera tabla del resto del contenido
        primer_tabla = bloque.split("Usando el set full")[0]

        # Buscar filas de tabla Markdown y extraer la segunda columna (nombre)
        filas = re.findall(r"\|\s*[^|]*\s*\|\s*([^|]+?)\s*\|\s*[^|]*\|", primer_tabla)

        # Eliminar posibles encabezados duplicados
        nombres = [
            nombre.strip()
            for nombre in filas
            if nombre.strip().lower() not in {"nombre", "---"}
        ]
        
        # Quitar duplicados conservando el orden
        return list(dict.fromkeys(nombres))