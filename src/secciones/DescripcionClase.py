from secciones.Seccion import Seccion
from dataset.Entrada import Entrada

import re

class DescripcionClase(Seccion):

    def run(self, *args, **kwargs):
        content = args[0] if args else None
        filename = args[1] if args else ""

        content = re.sub(r"(?s)^---\s*\ntitle:.*?\n---\s*\n*", "", content)
        if content:
            return [Entrada(
                    instruction=f"¿Qué caracteriza a un {filename}?",
                    input=content,
                    output=content)]
        else:
            return None