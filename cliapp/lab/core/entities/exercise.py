# lab/exercise/exercise.py
from abc import ABC, abstractmethod
from enum import Enum, auto

class Exercise(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def start(self):
        """Inicializa dependencias y recursos específicos del ejercicio."""
        pass

    @abstractmethod
    def finish(self):
        """Libera recursos y hace limpieza específica del ejercicio."""
        pass
