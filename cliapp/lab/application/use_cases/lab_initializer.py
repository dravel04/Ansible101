# lab/application/use_cases/lab_initializer.py
import sys

from lab.core.entities.lab import Lab
from lab.core.dtos.EventInfo import EventInfo
from lab.core.interfaces.lab_repository import LabRepository
from lab.core.interfaces.lab_port import LabPort
from lab.infrastructure.ui.progress_notifier_adapter import ProgressNotifierAdapter
from lab.infrastructure.adapters.container_adapter import ContainerAdapter
from lab.infrastructure.adapters.registry_adapter import RegistryAdapter

class LabInitializer:

    # def execute(self, service: LabPort, repo_adapter: LabRepository, engine: str, force: bool) -> None:
    def execute(self, service: LabPort, repo_adapter: LabRepository, lab: Lab) -> None:
        notifier = ProgressNotifierAdapter()

        event_info = EventInfo(name='Verificando si Ansible esta instalado')
        spinner_handle, finished_event = notifier.start(event_info)
        failed, error_output = service.verify_context()
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

        event_info = EventInfo(name='Definiendo fichero de configuracion')
        spinner_handle, finished_event = notifier.start(event_info)
        repo_adapter.save(lab)
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None

        event_info = EventInfo(name='Inicializando laboratorio')
        spinner_handle, finished_event = notifier.start(event_info)
        LAB_IMAGES = RegistryAdapter().auto_discover_images()
        failed, error_output = service.init(ContainerAdapter(engine=lab.engine), LAB_IMAGES)
        event_info.failed = failed; event_info.error_msg = error_output
        notifier.finish(spinner_handle, finished_event)
        sys.exit(1) if event_info.failed else None
