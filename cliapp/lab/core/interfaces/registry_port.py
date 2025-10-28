# lab/core/interfaces/registry_port.py
from typing import Protocol, Dict, Type
from lab.core.interfaces.exercise_port import Exercise
from lab.core.interfaces.grader_port import Grader

class RegistryPort(Protocol):
    def auto_discover_exercises(self) -> Dict[str, Type[Exercise]]:
        """
        Descubre y retorna un diccionario de clases Exercise (Clave: nombre, Valor: Clase).
        """
        ...

    def auto_discover_graders(self) -> Dict[str, Type[Grader]]:
        """
        Descubre y retorna un diccionario de clases Grader (Clave: nombre, Valor: Clase).
        """
        ...

    def auto_discover_images(self) -> Dict[str, Dict[str, str]]:
        """
        Descubre y retorna la información de las imágenes del Lab (rutas, tags).
        """
        ...