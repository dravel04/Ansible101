# lab/core/interfaces/container_provider.py
from abc import ABC, abstractmethod
from typing import Tuple, Optional

class ContainerProvider(ABC):
    @abstractmethod
    def run_container(
        self,
        image: str,
        name: str,
        ports: Optional[dict] = None,
    ) -> Tuple[Optional[object], bool, str]:
        """
        Runs a container and returns (container, failed, error_message).
        If failed is True, container will be None.
        """
        pass

    @abstractmethod
    def remove_container(
        self,
        name: str,
    ) -> Tuple[Optional[object], bool, str]:
        """
        Removes a container and returns (failed, error_message).
        """
        pass
