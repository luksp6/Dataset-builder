from secciones.Seccion import Seccion
from dataset.Entrada import Entrada

import re

class DescripcionClase(Seccion):

    def run(self, *args, **kwargs):
        content = args[0] if args else ""
        filename = args[1] if args else ""

        bloque = self._extraer_seccion(content)
        if bloque:
            return [Entrada(
                    instruction=f"¿Qué caracteriza a un {filename}?",
                    input=bloque,
                    output=bloque)]
        else:
            return None
        
    def _extraer_seccion(self, contenido: str) -> str:
        # Eliminar encabezado YAML
        contenido = re.sub(r"(?s)^---\s*\ntitle:.*?\n---\s*\n*", "", contenido)

        # Dividir el contenido en base a la palabra clave que marca el fin de la sección
        partes = re.split(r"^\s*Recompensas\s*$", contenido, maxsplit=1, flags=re.MULTILINE | re.IGNORECASE)

        return partes[0].strip() if partes else ""