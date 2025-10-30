# lab/infrastructure/adapters/lab_adapter.py
from lab.core.entities.lab import Lab
import logging

logger = logging.getLogger("lab")

class LabAdapter:

    def init(self, lab: Lab) -> None:
        if lab.engine == "docker":
            # logica docker
            ...

