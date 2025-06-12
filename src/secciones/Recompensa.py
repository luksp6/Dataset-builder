from multiprocessing import Queue
from secciones.Seccion import Seccion
from dataset.Entrada import Entrada

class Recompensa(Seccion):

    def run(self, *args, **kwargs):
        content = args[0] if args else ""

        seccion = self._extraer_seccion(content)
        if seccion:
            return Entrada(instruction="¿Qué recompensas obtiene el personaje?", input=seccion, output=seccion)
        else:
            return None