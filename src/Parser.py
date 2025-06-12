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
    
    def _dividir_por_secciones(self, contenido: str) -> dict[str, str]:
        """
        Divide el contenido en secciones usando los nombres de las secciones conocidas.
        Devuelve un dict: { "Seccion 1": bloque, "Seccion 2": bloque, ... }
        """
        nombres = [seccion.get_nombre() for seccion in self._categoria]
        nombres_escapados = [re.escape(nombre) for nombre in nombres if nombre]

        pattern = rf"^({'|'.join(nombres_escapados)})\s*$"
        secciones = {}
        matches = list(re.finditer(pattern, contenido, re.MULTILINE))

        # 1️⃣ Sección inicial (sin título explícito)
        if matches and matches[0].start() > 0:
            secciones[""] = contenido[:matches[0].start()].strip()

        # 2️⃣ Resto de secciones con encabezado
        for i, match in enumerate(matches):
            nombre = match.group(1)
            inicio = match.end()
            fin = matches[i + 1].start() if i + 1 < len(matches) else len(contenido)
            secciones[nombre] = contenido[inicio:fin].strip()

        return secciones

    def get_nombre(self) -> str:
        return self._nombre
    
    def _sanitizar(self, text:str) -> str:
        # Eliminar etiquetas HTML <br>, <br/>, <br />
        text = re.sub(r"<br\s*/?>", "\n", text)

        # Eliminar imágenes ![](url)
        text = re.sub(r"!\[.*?\]\(.*?\)", "", text)

        # Eliminar enlaces [texto](url) → reemplazar por "texto"
        text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)

        # Eliminar negritas y itálicas
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
        text = re.sub(r"\*(.*?)\*", r"\1", text)
        text = re.sub(r"_(.*?)_", r"\1", text)

        # Eliminar líneas vacías múltiples
        text = re.sub(r"\n\s*\n", "\n\n", text)

        # Strip general
        return text.strip()

    def run(self, *args, **kwargs):
        executor = AdminConcurrencia.get_instance(self._categoria.get_num_secciones())        
        self._output = CatDataset(self._nombre)
        working_path = os.path.join(self._input_dir, self._nombre)
        for file in os.listdir(working_path):
            if not file.endswith(".md"):
                continue 
            filename = file.removesuffix(".md")           
            file_dataset = FileDataset(filename)
            contenido_sanitizado = self._sanitizar(self._get_target_content(os.path.join(working_path, file)))
            bloques = self._dividir_por_secciones(contenido_sanitizado)
            tareas = []
            for seccion in self._categoria:
                nombre = seccion._nombre
                bloque = bloques.get(nombre, "")
                tareas.append((seccion.run, (bloque, filename)))
            resultados = executor.collect(tareas)
            
            for result in resultados:
                file_dataset.add_bulk(result)
            
            self._output.add(file_dataset)
              
        return self._output

    