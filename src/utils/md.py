def extraer_filas(tabla: str) -> list[str]:
    """
    Para una tabla en formato MarkDown, elimina línes inválidas.
    Devuelve un list[str] con el contenido de cada fila de la tabla.
    """
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