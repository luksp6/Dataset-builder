from secciones.Seccion import Seccion
from dataset.Entrada import Entrada

import re

class Vida(Seccion):

    def run(self, *args, **kwargs):
        content = args[0] if args else None
        filename = args[1] if args else ""

        print("//////")
        print(filename)
        print(content)
        print("//")


        if content:
            promedios = self._extraer_filas_tabla(content)
    
            for promedio in promedios:
                print(promedio)
                print()

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
                        instruction=f"¿Cuánta vida tiene un {filename} {columnas[0]} al {nivel}?",
                        input=content,
                        output=f"Un {filename} {columnas[0]} al {nivel} se espera que tenga en promedio {valor}. (sin tener en cuenta las recompensas de vida)"
                    ))
            return entradas
        else:
            return None
        
    def _extraer_filas_tabla(self, tabla: str) -> list[str]:
        lineas = [line.strip() for line in tabla.splitlines() if line.strip()]
        filas = []
        raza_pendiente = None

        for linea in lineas:
            if set(linea) <= {"|", "-", " "}:
                continue  # Ignorar separadores

            celdas = [c.strip() for c in linea.strip("|").split("|") if c.strip()]
            if len(celdas) == 1:
                raza_pendiente = celdas[0]
            elif len(celdas) >= 2:
                if raza_pendiente:
                    fila = [raza_pendiente] + celdas
                    raza_pendiente = None
                else:
                    fila = celdas
                filas.append(" | ".join(fila))

        return filas