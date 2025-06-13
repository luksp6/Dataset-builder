from Parser import Parser
from categorias.Luchadora import Luchadora

from secciones import DescripcionClase, Recompensa, Equipamiento, HechizosEspeciales, Modificadores, VidaMana, Vida

from AdminConcurrencia import AdminConcurrencia
from dataset.FileDataset import FileDataset

from pathlib import Path

import atexit
import os


INPUT_DIR = Path("C:/Desarrollo/AO/FS-WIKI-2024")
STRUCT_FILE = Path("wikiPages.json")
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "Salida"

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Parser
    parser_luchadora_mana = Parser(INPUT_DIR,
                              "Clases luchadoras (con mana)",
                              Luchadora([
                                  DescripcionClase(""),
                                  Recompensa("Recompensas"),
                                  Equipamiento("Equipamiento"),
                                  HechizosEspeciales("Hechizos especiales"),
                                  Modificadores("Modificadores"),
                                  VidaMana("Promedios de vida y mana")
                                  ]))
    
    parser_luchadora_sin_mana = Parser(INPUT_DIR,
                              "Clases luchadoras (sin mana)",
                              Luchadora([
                                  DescripcionClase(""),
                                  Recompensa("Recompensas"),
                                  Equipamiento("Equipamiento"),
                                  Modificadores("Modificadores"),
                                  Vida("Promedios de vida")
                                  ]))
    
    parser_list = [parser_luchadora_mana, parser_luchadora_sin_mana]

    # Dataset
    dataset = FileDataset(INPUT_DIR.name)

    # Ejecucion
    executor = AdminConcurrencia(os.cpu_count())
    tareas = [(parser.run, ()) for parser in parser_list]
    results = executor.collect(tareas)
    for result in results:
        dataset.add_bulk(result.to_json(OUTPUT_DIR))
        
    dataset.to_json(OUTPUT_DIR)
    print("Ejecucion finalizada.")

    atexit.register(lambda: AdminConcurrencia.get_instance().shutdown())