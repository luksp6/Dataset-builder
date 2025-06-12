from pathlib import Path
from concreto.parser.Parser import Parser
from concreto.categorias.Luchadora import Luchadora
from concreto.secciones.Recompensa import Recompensa
from concreto.concurrencia.AdminConcurrencia import AdminConcurrencia
from concreto.dataset.FileDataset import FileDataset

import atexit
import os


INPUT_DIR = Path("C:/Desarrollo/AO/FS-WIKI-2024")
OUTPUT_DIR = Path(__file__).resolve().parent / "Salida"

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Secciones
    recompensa = Recompensa("Recompensas")

    # Parser
    parser_luchadora = Parser(INPUT_DIR, "Clases luchadoras", Luchadora({recompensa}))
    parser_list = [parser_luchadora]

    # Dataset
    dataset = FileDataset(INPUT_DIR.name)

    # Ejecucion
    executor = AdminConcurrencia(os.cpu_count())
    futures = [
                executor.submit(parser.run)
                for parser in parser_list]
    
    for future in futures:
        try:
            result = future.result()
            if result:
                dataset.add_bulk(result.to_json(OUTPUT_DIR))
        except Exception as e:
            print(f"⚠️ Error en parser: {e}")
    dataset.to_json(OUTPUT_DIR)

    atexit.register(lambda: AdminConcurrencia.get_instance().shutdown())