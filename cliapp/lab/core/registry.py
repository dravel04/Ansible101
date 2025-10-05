# lab/core/registry.py
import pkgutil
import importlib
import inspect
from lab.exercise.exercise import Exercise
from lab.grader.grader import Grader
import lab.exercise, lab.grader

EXERCISES = {}
GRADERS = {}

def auto_discover_exercises():
    print('HOLA EXER')
    for _, module_name, _ in pkgutil.iter_modules(lab.exercise.__path__):
        module = importlib.import_module(f"lab.exercise.{module_name}")
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Exercise) and obj is not Exercise:
                EXERCISES[module_name.replace('exercise_', '')] = obj

def auto_discover_graders():
    print('HOLA GRDER')
    for _, module_name, _ in pkgutil.iter_modules(lab.grader.__path__):
        module = importlib.import_module(f"lab.grader.{module_name}")
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Grader) and obj is not Grader:
                GRADERS[module_name.replace('grader_', '')] = obj
