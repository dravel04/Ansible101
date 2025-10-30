# lab/core/interfaces/container_port.py (AJUSTADO A PROTOCOL)
from typing import Protocol, Tuple, Optional, Any

class ContainerPort(Protocol):
    """
    Define el contrato para la gestion de contenedores.
    """
    engine: str
    client: Any
    def init_client(self) -> None:
        """
        Inicializa el cliente del container runtime
        """
        ...

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
    ) -> Tuple[bool, str]:
        """
        Elimina un contenedor y devuelve (failed: bool, error_message: str).
        """
        ...