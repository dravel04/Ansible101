# lab/infrastructure/adapters/registry_adapter.py
import pkgutil       # Para iterar sobre modulos en un paquete
import importlib     # Para importar modulos dinamicamente por nombre
import inspect       # Para inspeccionar objetos (clases, funciones) dentro de un modulo
from pathlib import Path

import lab.application.use_cases.exercise, lab.application.use_cases.grader

class RegistryAdapter:
    def auto_discover_exercises(self):
        """
        Recorre todos los modulos dentro de lab.application.use_cases.exercise y registra
        las clases que heredan de Exercise en el diccionario EXERCISES.
        
        Clave del diccionario: nombre del modulo sin 'exercise_'
        Valor: clase correspondiente
        """
        EXERCISES = {}
        # pkgutil.iter_modules devuelve (loader, module_name, ispkg) para cada modulo
        for _, module_name, _ in pkgutil.iter_modules(lab.application.use_cases.exercise.__path__):
            # Importamos dinamicamente el modulo
            module = importlib.import_module(f"lab.application.use_cases.exercise.{module_name}")
            # Recorremos todos los miembros del modulo y filtramos solo clases
            for _, obj in inspect.getmembers(module, inspect.isclass):
                # Comprobamos si la clase hereda de Exercise y no es la clase base Exercise
                if hasattr(obj, 'start') and callable(obj.start) and hasattr(obj, 'finish') and callable(obj.finish):
                    # Guardamos la clase en el diccionario con clave simplificada
                    # Por ejemplo: 'exercise_a' -> 'a'
                    EXERCISES[module_name.replace('exercise_', '')] = obj
        return EXERCISES

    def auto_discover_graders(self):
        """
        Recorre todos los modulos dentro de lab.application.use_cases.grader y registra
        las clases que heredan de Grader en el diccionario GRADERS.
        
        Clave del diccionario: nombre del modulo sin 'grader_'
        Valor: clase correspondiente
        """
        GRADERS = {}
        for _, module_name, _ in pkgutil.iter_modules(lab.application.use_cases.grader.__path__):
            # Importamos dinamicamente el modulo
            module = importlib.import_module(f"lab.application.use_cases.grader.{module_name}")
            # Recorremos todos los miembros del modulo y filtramos solo clases
            for _, obj in inspect.getmembers(module, inspect.isclass):
                # Comprobamos si la clase hereda de Grader y no es la clase base Grader
                if hasattr(obj, 'grade') and callable(obj.grade):
                    # Guardamos la clase en el diccionario con clave simplificada
                    # Por ejemplo: 'grader_a' -> 'a'
                    GRADERS[module_name.replace('grader_', '')] = obj
        return GRADERS

    def auto_discover_images(self):
        """
        Recorre todos los Containerfile en lab/infrastructure/containerfile/
        y registra los tags e info necesaria en LAB_IMAGES.
        
        Clave: nombre simplificado del containerfile sin extension
        Valor: ruta del containerfile y tag de la imagen
        """
        LAB_IMAGES = {}
        containerfile_dir = Path(__file__).parent.parent / "infrastructure/containerfile"
        
        for containerfile_path in containerfile_dir.glob("*.Containerfile"):
            name = containerfile_path.stem.replace(".Containerfile", "")  # nombre simplificado
            tag = f"{name}:latest"  # puedes derivar el tag automáticamente o definir en un dict aparte
            LAB_IMAGES[name] = {
                "containerfile_path": containerfile_path,
                "tag": tag
            }
        return LAB_IMAGES