from utils import Runnable
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
        """
        Abre el archivo ubicado en el path recibido como parámetro.
        Devuelve un str con el contenido del archivo.
        """
        with open(target_path, encoding="utf-8") as f:
            content = f.read()
        return content
    
    def _dividir_por_secciones(self, contenido: str) -> dict[str, str]:
        """
        Divide el contenido en secciones usando los nombres de las secciones conocidas.
        Devuelve un dict: { "Sección 1": bloque, "Sección 2": bloque, ... }
        """
        nombres = [seccion.get_nombre() for seccion in self._categoria]
        nombres_escapados = [re.escape(nombre) for nombre in nombres if nombre]

        # Crea un patrón para detectar encabezados con o sin negritas
        pattern = rf"^(?:\*\*)?\s*({'|'.join(nombres_escapados)})\s*(?:\*\*)?\s*$"
        matches = list(re.finditer(pattern, contenido, re.MULTILINE | re.IGNORECASE))

        secciones = {}

        # Si hay contenido antes del primer encabezado, lo asignamos a la sección sin nombre
        if matches and matches[0].start() > 0:
            secciones[""] = contenido[:matches[0].start()].strip()

        for i, match in enumerate(matches):
            nombre = match.group(1).strip()
            inicio = match.end()
            fin = matches[i + 1].start() if i + 1 < len(matches) else len(contenido)

            bloque = contenido[inicio:fin].strip()
            secciones[nombre] = bloque

        return secciones
    
    def _sanitizar(self, text:str) -> str:        
        """
        Elimina el formato de un str con contenido MarkDown.
        Devuelve un str con el contenido en texto plano.
        """
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
                bloque = bloques.get(seccion._nombre, "")
                tareas.append((seccion.run, (bloque, filename)))
            resultados = executor.collect(tareas)
            
            for result in resultados:
                file_dataset.add_bulk(result)
            
            self._output.add(file_dataset)
              
        return self._output