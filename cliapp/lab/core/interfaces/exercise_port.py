# lab/core/interfaces/exercise_port.py
from typing import Protocol

class Exercise(Protocol):
    name: str
    debug_msg: list[str]
    def start(self) -> None:
        """
        Inicializa dependencias y recursos especificos del ejercicio
        """
        ...

    def finish(self) -> None:
        """
        Libera recursos y hace limpieza especifica del ejercicio
        """
        pass