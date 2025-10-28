# lab/infrastructure/adapters/lab_repository_adapter.py
import json
from pathlib import Path
from typing import Tuple
from lab.core.entities.lab import Lab
import logging

LAB_CONFIG_PATH = Path.home() / ".lab_config.json"
logger = logging.getLogger("lab")

class LabRepositoryAdapter:
    
    def load(self, force: bool = False) -> Tuple[bool, Lab]:
        exists = True
        lab = Lab()
        if force or not LAB_CONFIG_PATH.exists():
            exists = False
            return exists, lab
        logger.debug(f"Cargando configuración desde {LAB_CONFIG_PATH}")
        try:
            data = json.loads(LAB_CONFIG_PATH.read_text())
        except json.JSONDecodeError:
            logger.warning("Archivo de configuración inválido, recreando.")
            return False, Lab()
        engine = data.get('engine')
        lab = Lab(engine=engine) 
        return exists,lab 

    def save(self, lab: Lab) -> None:
        """
        Persiste el estado actual de la entidad Lab recorriendo sus atributos.
        """
        import inspect
        data = {}
        # for key, value in vars(lab).items():
        #     data[key.replace('_','')] = value
        for name, _ in inspect.getmembers(lab.__class__, lambda x: isinstance(x, property)):
            data[name] = getattr(lab, name)
        LAB_CONFIG_PATH.write_text(json.dumps(data))
