from multiprocessing import Process, Queue

from abstracto.Runnable import Runnable
from concreto.categorias.Categoria import Categoria

import os
import re

class Parser(Runnable):

    _input_dir:str
    _categoria:Categoria

    def __init__(self, input_dir:str, categoria:Categoria):
        self._input_dir = input_dir
        self._categoria = categoria

    def _get_target_content(self, target_path) -> str:
        with open(target_path, encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r"<br\s*/?>", "\n", content)
        content = re.sub(r"!\[.*?\]\(.*?\)", "", content)  # eliminar imágenes
        return content


    def run(self):
        print("En parser.run()")
        for file in os.listdir(self._input_dir):
            if not file.endswith(".md"):
                continue
            
            print("Archivo: ", file)
            content = self._get_target_content(os.path.join(self._input_dir, file))
            procesos = []
            queue = Queue()
            for seccion in self._categoria:
                p = Process(target=seccion.run, args=(content, queue))
                procesos.append(p)
                p.start()

            resultados = []
            for p in procesos:
                p.join()
            while not queue.empty():
                resultados.append(queue.get())
            print(resultados)

    