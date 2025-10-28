# lab/core/interfaces/progress_notifier_port.py
from typing import Protocol, Callable, Tuple

# Define el tipo (la "firma") de las funciones que representan las tareas de verificación (checks).
# Firma: Una función que no acepta argumentos (representado por '[]') y debe retornar una tupla.
# Retorno: Tuple[bool, str] donde:
#          - bool: Indica si el check tuvo exito (True) o fallo (False)
#          - str: Es el mensaje (ej. mensaje de error si falla)
CheckFunc = Callable[[], Tuple[bool, str]]

class ProgressNotifierPort(Protocol):
    """
    Define el contrato para notificar el progreso de 
    la ejecucion del Caso de Uso (ej. con un spinner de CLI).
    """
    # def run_checks(self, action: str, checks: list[Tuple[str, CheckFunc]], instance: Exercise) -> None:
    def run_checks(self, action: str, checks: list[Tuple[str, CheckFunc]]) -> None:
        """
        Ejecuta una lista de checks o tareas, manejando la visualización del progreso.
        """
        ...