from typing import Protocol

from lab.core.interfaces.progress_notifier_port import ProgressNotifierPort

class Grader(Protocol):
    """
    Define el contrato para la inicializacion tecnica 
    de la infraestructura del Lab (Ej: inicializar el lab, construir imagenes, etc).
    """
    exercisename: str
    def grade(self, notifier: ProgressNotifierPort) -> None:
        """
        Ejecuta la logica de evaluacion del ejercicio
        """
        ...
