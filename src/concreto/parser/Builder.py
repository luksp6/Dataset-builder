import json
import os
from abstracto.Runnable import Runnable

class Builder(Runnable):

    _output_dir:str
    _output_filename:str

    def __init__(self, output_dir, output_filename):
        self._output_dir = output_dir
        self._output_filename = output_filename


    def run(self):
        with open(os.path.join(self._output_dir, self._output_filename), "w", encoding="utf-8") as out_f:
            for root, _, files in os.walk(self._output_dir):
                for file in files:
                    if file.endswith(".json"):
                        with open(os.path.join(root, file), encoding="utf-8") as f:
                            samples = json.load(f)
                            for item in samples:
                                out_f.write(json.dumps(item, ensure_ascii=False) + "\n")
        print(f"✅ Dataset unificado exportado a: {self._output_filename}")