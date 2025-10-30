# lab/infrastructure/adapters/lab_adapter.py
import logging
from lab.core.entities.lab import Lab

logger = logging.getLogger("lab")

class LabAdapter:

    def init(self, lab: Lab) -> None:
        if lab.engine == "docker":
            # logica docker
            ...

