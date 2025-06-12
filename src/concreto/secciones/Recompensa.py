from abstracto.Seccion import Seccion
from concreto.dataset.Entrada import Entrada

class Recompensa(Seccion):

    def run(self, content, queue):
        seccion = self._extraer_seccion(content)
        if seccion:
            queue.put(Entrada("¿Qué recompensas obtiene el personaje?", seccion, seccion))