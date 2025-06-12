from dataset.Dataset import Dataset
from dataset.Entrada import Entrada

import json, os

class FileDataset(Dataset):
    
    def to_json(self, output_dir:str):
        os.makedirs(output_dir, exist_ok=True)
        output_filepath = os.path.join(output_dir, f"{self._nombre}.json")
        entradas_json = [e.to_dict() for e in self._entradas]
        with open(output_filepath, "w", encoding="utf-8") as f:
            json.dump(entradas_json, f, indent=2, ensure_ascii=False)
        return entradas_json
    
    def add_bulk(self, entradas:list):
            for entrada in entradas:
                if isinstance(entrada, Entrada):
                    self._entradas.append(entrada)
                elif isinstance(entrada, dict):
                    self._entradas.append(Entrada(from_dict=entrada))
                else:
                    raise TypeError("Los elementos deben ser Entrada o dicts convertibles.")