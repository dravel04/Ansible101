# lab/core/interfaces/lab_repository.py
from typing import Protocol, Tuple
from lab.core.entities.lab import Lab

class LabRepository(Protocol):
    """
    Define el contrato para la persistencia de la entidad Lab
    """
    def load(self, force: bool) -> Tuple[bool, Lab]:
        """
        Carga la instancia de Lab persistida.
        Si `force=True` o no existe la configuracion previa, retorna (False, nuevo_lab)
        Retorna (exists: bool, lab: Lab)
        """
        ...

    def save(self, lab: Lab) -> None:
        """
        Persiste el estado actual de la entidad Lab
        """
        ...