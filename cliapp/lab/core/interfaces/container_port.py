# lab/core/interfaces/container_port.py
from typing import Protocol, Tuple, Optional, Any, runtime_checkable

@runtime_checkable
class ContainerPort(Protocol):
    """
    Define el contrato para la gestion de contenedores.
    """
    engine: str
    client: Any
    def init_client(self) -> Tuple[bool, str]:
        """
        Inicializa el cliente del container runtime
        """
        ...

    def build_image(
        self,
        name: str,
    ) -> Tuple[bool, str]:
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