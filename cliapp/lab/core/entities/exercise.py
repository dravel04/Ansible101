# lab/core/entities/exercise.py
from abc import ABC, abstractmethod

class Exercise(ABC):
    def __init__(self, name: str):
        self.name = name
        self.debug_msg = []

    @abstractmethod
    def start(self):
        """Inicializa dependencias y recursos especificos del ejercicio."""
        pass

    @abstractmethod
    def finish(self):
        """Libera recursos y hace limpieza especifica del ejercicio."""
        pass
