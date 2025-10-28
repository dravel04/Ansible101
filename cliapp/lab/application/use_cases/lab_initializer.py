# lab/application/use_cases/lab_initializer.py
import logging
from lab.core.interfaces.lab_repository import LabRepository
from lab.core.interfaces.lab_port import LabPort

logger = logging.getLogger("lab")

class LabInitializer:

    def execute(self, service: LabPort, repo_adapter: LabRepository, engine: str, force: bool) -> None:
        try:
            exists, lab = repo_adapter.load(force)
            if not exists:
                lab.engine=engine
                repo_adapter.save(lab)
            else:
                raise ValueError(f"Ya existe una instancia de Lab [engine={lab.engine}]. Para crear una nueva instancia, usar 'lab init <engine> -f' o borrar el fichero '~/.lab_config.json'")
            service.init(lab)
        except Exception as e:
            logger.error(f"{type(e).__name__}: {e}")