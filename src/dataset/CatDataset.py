from dataset.Dataset import Dataset

import os

class CatDataset(Dataset):

    def to_json(self, output_dir:str):
        os.makedirs(output_dir, exist_ok=True)
        output_dir = os.path.join(output_dir, self._nombre)
        entradas_json = []
        for entrada in self._entradas:
            entradas_json.extend(entrada.to_json(output_dir))
        return entradas_json