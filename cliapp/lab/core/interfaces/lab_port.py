# lab/core/interfaces/lab_port.py
from typing import Protocol
from lab.core.entities.lab import Lab

class LabPort(Protocol):
    """
    Define el contrato para la inicializacion tecnica 
    de la infraestructura del Lab (Ej: inicializar el lab, construir imagenes, etc).
    """
    def init(self, lab: Lab) -> None:
        """
        Ejecuta las dependencias de inicializacion
        """
        ...