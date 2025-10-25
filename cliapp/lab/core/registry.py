# lab/core/registry.py
import pkgutil       # Para iterar sobre modulos en un paquete
import importlib     # Para importar modulos dinamicamente por nombre
import inspect       # Para inspeccionar objetos (clases, funciones) dentro de un modulo
from lab.core.entities.exercise import Exercise
from lab.core.entities.grader import Grader
import lab.infrastructure.exercise, lab.infrastructure.grader

EXERCISES = {}
GRADERS = {}

# -----------------------------------------
# Funcion para descubrir automaticamente todos los ejercicios
# -----------------------------------------
def auto_discover_exercises():
    """
    Recorre todos los modulos dentro de lab.infrastructure.exercise y registra
    las clases que heredan de Exercise en el diccionario EXERCISES.
    
    Clave del diccionario: nombre del modulo sin 'e_'
    Valor: clase correspondiente
    """
    # pkgutil.iter_modules devuelve (loader, module_name, ispkg) para cada modulo
    for _, module_name, _ in pkgutil.iter_modules(lab.infrastructure.exercise.__path__):
        # Importamos dinamicamente el modulo
        module = importlib.import_module(f"lab.infrastructure.exercise.{module_name}")
        # Recorremos todos los miembros del modulo y filtramos solo clases
        for _, obj in inspect.getmembers(module, inspect.isclass):
            # Comprobamos si la clase hereda de Exercise y no es la clase base Exercise
            if issubclass(obj, Exercise) and obj is not Exercise:
                # Guardamos la clase en el diccionario con clave simplificada
                # Por ejemplo: 'e_a' -> 'a'
                EXERCISES[module_name.replace('e_', '')] = obj

# -----------------------------------------
# Funcion para descubrir automaticamente todos los graders
# -----------------------------------------
def auto_discover_graders():
    """
    Recorre todos los modulos dentro de lab.infrastructure.grader y registra
    las clases que heredan de Grader en el diccionario GRADERS.
    
    Clave del diccionario: nombre del modulo sin 'g_'
    Valor: clase correspondiente
    """
    for _, module_name, _ in pkgutil.iter_modules(lab.infrastructure.grader.__path__):
        # Importamos dinamicamente el modulo
        module = importlib.import_module(f"lab.infrastructure.grader.{module_name}")
        # Recorremos todos los miembros del modulo y filtramos solo clases
        for _, obj in inspect.getmembers(module, inspect.isclass):
            # Comprobamos si la clase hereda de Grader y no es la clase base Grader
            if issubclass(obj, Grader) and obj is not Grader:
                # Guardamos la clase en el diccionario con clave simplificada
                # Por ejemplo: 'g_a' -> 'a'
                GRADERS[module_name.replace('g_', '')] = obj
    