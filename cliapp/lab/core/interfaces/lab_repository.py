# lab/core/interfaces/lab_repository.py
from typing import Protocol, Tuple
from lab.core.entities.lab import Lab

class LabRepository(Protocol):
    """
    Define el contrato para la persistencia de la entidad Lab.
    """
    def load(self, force: bool) -> Tuple[bool, Lab]:
        """
        Carga la instancia de Lab persistida.
        Retorna (exists: bool, instancia: Lab).
        """
        ...

    def save(self, lab: Lab) -> None:
        """
        Persiste el estado actual de la entidad Lab.
        """
        ...