from secciones.Seccion import Seccion
from dataset.Entrada import Entrada
from utils import md

import re

class VidaMana(Seccion):

    def run(self, *args, **kwargs):
        content = args[0] if args else None
        filename = args[1] if args else ""
        if content:
            promedios = md.extraer_filas(content)
            encabezado = list(map(str.strip, promedios[0].split("|")))
            entradas = []
            for promedio in promedios[2:]:
                columnas = list(map(str.strip, promedio.split("|")))
                if len(columnas) != len(encabezado):
                    continue  # Saltear filas mal formateadas

                entradas.append(Entrada(
                        instruction=f"¿Qué promedio de vida por nivel tiene un {filename} {columnas[0]}?",
                        input=content,
                        output=f"Un {filename} {columnas[0]} tiene un promedio por nivel de {columnas[1]} puntos de vida."
                    ))
                for i in range(2, len(encabezado)):  # Desde la columna de Nivel 13 en adelante
                    nivel = encabezado[i]
                    valor = columnas[i]

                    entradas.append(Entrada(
                        instruction=f"Cuánta vida y mana tiene un {filename} {columnas[0]} al {nivel}?",
                        input=content,
                        output=f"Un {filename} {columnas[0]} al {nivel} se espera que tenga en promedio {valor}. (sin tener en cuenta las recompensas de vida y mana)"
                    ))
            return entradas
        else:
            return None