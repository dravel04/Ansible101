# lab/core/registry.py
import pkgutil       # Para iterar sobre módulos en un paquete
import importlib     # Para importar módulos dinámicamente por nombre
import inspect       # Para inspeccionar objetos (clases, funciones) dentro de un módulo
from lab.exercise.exercise import Exercise
from lab.grader.grader import Grader
import lab.exercise, lab.grader

EXERCISES = {}
GRADERS = {}

# -----------------------------------------
# Función para descubrir automáticamente todos los ejercicios
# -----------------------------------------
def auto_discover_exercises():
    """
    Recorre todos los módulos dentro de lab.exercise y registra
    las clases que heredan de Exercise en el diccionario EXERCISES.
    
    Clave del diccionario: nombre del módulo sin 'exercise_'
    Valor: clase correspondiente
    """
    # pkgutil.iter_modules devuelve (loader, module_name, ispkg) para cada módulo
    for _, module_name, _ in pkgutil.iter_modules(lab.exercise.__path__):
        # Importamos dinámicamente el módulo
        module = importlib.import_module(f"lab.exercise.{module_name}")
        # Recorremos todos los miembros del módulo y filtramos solo clases
        for _, obj in inspect.getmembers(module, inspect.isclass):
            # Comprobamos si la clase hereda de Exercise y no es la clase base Exercise
            if issubclass(obj, Exercise) and obj is not Exercise:
                # Guardamos la clase en el diccionario con clave simplificada
                # Por ejemplo: 'exercise_a' -> 'a'
                EXERCISES[module_name.replace('exercise_', '')] = obj

# -----------------------------------------
# Función para descubrir automáticamente todos los graders
# -----------------------------------------
def auto_discover_graders():
    """
    Recorre todos los módulos dentro de lab.grader y registra
    las clases que heredan de Grader en el diccionario GRADERS.
    
    Clave del diccionario: nombre del módulo sin 'grader_'
    Valor: clase correspondiente
    """
    for _, module_name, _ in pkgutil.iter_modules(lab.grader.__path__):
        # Importamos dinámicamente el módulo
        module = importlib.import_module(f"lab.grader.{module_name}")
        # Recorremos todos los miembros del módulo y filtramos solo clases
        for _, obj in inspect.getmembers(module, inspect.isclass):
            # Comprobamos si la clase hereda de Grader y no es la clase base Grader
            if issubclass(obj, Grader) and obj is not Grader:
                # Guardamos la clase en el diccionario con clave simplificada
                # Por ejemplo: 'grader_a' -> 'a'
                GRADERS[module_name.replace('grader_', '')] = obj
