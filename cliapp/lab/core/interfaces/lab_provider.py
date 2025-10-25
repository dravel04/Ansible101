# lab/core/interfaces/container_provider.py
from abc import ABC, abstractmethod
from typing import Tuple, Optional

class LabProvider(ABC):
    @abstractmethod
    def init(self):
        """
        Removes a container and returns (failed, error_message).
        """
        pass
