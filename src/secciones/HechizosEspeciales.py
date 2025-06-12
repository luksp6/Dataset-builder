from secciones.Seccion import Seccion
from dataset.Entrada import Entrada

import re

class HechizosEspeciales(Seccion):

    def run(self, *args, **kwargs):
        content = args[0] if args else None
        filename = args[1] if args else ""

        if content:
            hechizos = self._extraer_hechizos_especiales(content)
            hechizos_str = []
            for i in range(0, len(hechizos)):
                nombre, efecto = map(str.strip, hechizos[i].split("|", 1))
                hechizos_str.append(f"{nombre} ({efecto})")

            if len(hechizos_str) == 0:
                output = f"Un {filename} no puede lanzar ningun hechizo especial."
            elif len(hechizos_str) == 1:
                output = f"Un {filename} puede lanzar el hechizo especial {hechizos_str[0]}."
            else:
                output = f"Un {filename} puede lanzar los hechizos especiales {', '.join(hechizos_str)}."

            return [Entrada(
                    instruction=f"¿Qué hechizos especiales puede lanzar un {filename}?",
                    input=content,
                    output=output
                    )]
        else:
            return None
        
    def _extraer_hechizos_especiales(self, tabla: str) -> list[str]:
        # Captura filas tipo: | algo | algo |
        filas = re.findall(r"\|\s*([^\|]+?)\s*\|\s*([^\|]+?)\s*\|", tabla)
        # Filtra la fila de encabezado si contiene "nombre" y "efecto"
        return [
            f"{nombre.strip()} | {efecto.strip()}"
            for nombre, efecto in filas
            if not (
                nombre.strip().lower() == "nombre"
                or nombre.strip() == "---"
                or efecto.strip().lower() == "efecto"
                or efecto.strip() == "---"
            )
    ]