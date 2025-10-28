# lab/core/interfaces/container_port.py (AJUSTADO A PROTOCOL)
from typing import Protocol, Tuple, Optional, Any # Añadimos 'Any' para el objeto genérico

class ContainerPort(Protocol):
    """
    Define el contrato para la gestion de contenedores.
    """
    def run_container(
        self,
        image: str,
        name: str,
        ports: Optional[dict] = None,
    ) -> Tuple[Any, bool, str]:
        """
        Lanza un contenedor y devuelve (container_object, failed: bool, error_message: str).
        """
        ...

    def remove_container(
        self,
        name: str,
    ) -> Tuple[str, bool, str]:
        """
        Elimina un contenedor y devuelve (output: str, failed: bool, error_message: str).
        """
        ...