from typing import Protocol

class Grader(Protocol):
    """
    Define el contrato para la inicializacion tecnica 
    de la infraestructura del Lab (Ej: inicializar el lab, construir imagenes, etc).
    """
    exercisename: str
    def grade(self) -> None:
        """
        Ejecuta la logica de evaluacion del ejercicio
        """
        ...
