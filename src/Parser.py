from utils.Runnable import Runnable
from categorias.Categoria import Categoria
from AdminConcurrencia import AdminConcurrencia
from dataset.CatDataset import CatDataset
from dataset.FileDataset import FileDataset

import os
import re

class Parser(Runnable):

    _input_dir:str
    _nombre:str
    _categoria:Categoria
    _output:CatDataset
    
    def __init__(self, input_dir:str, nombre, categoria:Categoria):
        self._input_dir = input_dir
        self._nombre = nombre
        self._categoria = categoria
        self._output = None

    def _get_target_content(self, target_path) -> str:
        with open(target_path, encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r"<br\s*/?>", "\n", content)
        content = re.sub(r"!\[.*?\]\(.*?\)", "", content)  # eliminar imágenes
        return content
    
    def get_nombre(self) -> str:
        return self._nombre


    def run(self, *args, **kwargs):
        executor = AdminConcurrencia.get_instance(self._categoria.get_num_secciones())        
        self._output = CatDataset(self._nombre)
        working_path = os.path.join(self._input_dir, self._nombre)
        for file in os.listdir(working_path):
            if not file.endswith(".md"):
                continue            
            file_dataset = FileDataset(file.removesuffix(".md"))
            content = self._get_target_content(os.path.join(working_path, file))
            
            tareas = [(seccion.run, (content,)) for seccion in self._categoria]
            resultados = executor.collect(tareas)
            
            for result in resultados:
                file_dataset.add(result)
            
            self._output.add(file_dataset)
              
        return self._output

    