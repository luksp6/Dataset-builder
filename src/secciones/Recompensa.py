from secciones.Seccion import Seccion
from dataset.Entrada import Entrada

import re

class Recompensa(Seccion):

    def run(self, *args, **kwargs):
        content = args[0] if args else ""
        filename = args[1] if args else ""

        bloque = self._extraer_seccion(content)
        if bloque:
            niveles = self._extraer_niveles_como_dict(bloque)

            entradas = []
            for nivel, recompensas in niveles.items():
                recompensas = [r for r in recompensas if r.strip() != "--- | ---"]
                nombre1, efecto1 = map(str.strip, recompensas[1].split("|", 1))
                nombre2, efecto2 = map(str.strip, recompensas[2].split("|", 1))

                entradas.append(Entrada(
                    instruction=f"¿Qué recompensas tiene un {filename} en el {nivel}?",
                    input=recompensas,
                    output=f"Al {nivel}, un {filename} puede elegir entre {nombre1} ({efecto1}) o {nombre2} ({efecto2})."
                ))
            return entradas
        
        return None

    def _extraer_seccion(self, contenido: str) -> str:
        contenido = contenido.replace("<br />", "\n").replace("<br/>", "\n").replace("<br>", "\n")
        # Extrae desde "Recompensas" hasta el siguiente encabezado en MAYÚSCULAS o fin del texto
        pattern = rf"{self._nombre}\s*\n(.*?)(?=\n[A-ZÁÉÍÓÚÑ ]{{3,}}\n|\Z)"
        match = re.search(pattern, contenido, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def _extraer_niveles_como_dict(self, bloque: str) -> dict:
        niveles = ["Nivel 18", "Nivel 25", "Nivel 34"]
        resultado = {}

        for i, nivel in enumerate(niveles):
            nivel_lower = nivel.lower()
            if i < len(niveles) - 1:
                siguiente = niveles[i + 1]
                pattern = rf"{nivel}:\s*(.*?)(?=\n{re.escape(siguiente)}:)"
            else:
                pattern = rf"{nivel}:\s*(.*)"

            match = re.search(pattern, bloque, re.DOTALL)
            if match:
                contenido = match.group(1).strip()
                # Extraer filas de la tabla, ignorando encabezado
                filas = re.findall(r"\|([^|]+?)\|([^|]+?)\|", contenido)
                resultado[nivel_lower] = [f"{nombre.strip()} | {efecto.strip()}" for nombre, efecto in filas]

        return resultado