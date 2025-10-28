import json
from pathlib import Path
from typing import Tuple
from lab.core.entities.lab import Lab

LAB_CONFIG_PATH = Path.home() / ".lab_config.json"

class LabRepositoryAdapter:
    
    def load(self, force: bool = False) -> Tuple[bool, Lab]:
        exists = True
        lab = Lab()
        if force or not LAB_CONFIG_PATH.exists():
            exists = False
            return exists, lab
        
        data = json.loads(LAB_CONFIG_PATH.read_text())
        engine = data.get('engine')
        lab = Lab(engine=engine) 
        return exists,lab 

    def save(self, lab: Lab) -> None:
        """
        Persiste el estado actual de la entidad Lab recorriendo sus atributos.
        """
        data = {}
        for key, value in vars(lab).items():
            data[key] = value
        LAB_CONFIG_PATH.write_text(json.dumps(data))
