# lab/application/use_cases/exercise/exercise_a.py
from typing import Callable, Tuple, Union, List
from functools import partial
from rich.text import Text
# Importamos Puertos del Core
from lab.core.interfaces.container_port import ContainerPort
from lab.core.interfaces.progress_notifier_port import ProgressNotifierPort
from lab.infrastructure.adapters.container_adapter import ContainerAdapter
import logging
logger = logging.getLogger("lab")

# Definimos el tipo de la funcion de chequeo que vamos a pasar al notificador
CheckFunc = Callable[[], Tuple[bool, str]]

class ExerciseC:
    """
    Logica de negocio especifica para la evaluacion y gestion del ejercicio
    """
    def __init__(self, name: str, debug_msg: List[Union[str, Text]] = []):
        self.name = name
        self.debug_msg = debug_msg

    def _create_containers(self, container_provider: ContainerPort) -> Tuple[bool, str]:
        """
        Implementa una de las tareas (checks) de la secuencia
        """
        container, failed, error_output = container_provider.run_container(
            image="ssh-ol:8.10",
            name="machine-a",
            ports={"22/tcp": 2223, "80/tcp": 8080},
        )
        return failed, error_output

    def _install_packages(self) -> Tuple[bool, str]:
        """ Implementa otra tarea de la secuencia. """
        # ... logica ...
        return True, "ERROR: Paquetes no instalados correctamente"
    
    def _delete_containers(self, container_provider: ContainerPort):
        failed = False
        error_output = ''
        failed, error_output = container_provider.remove_container('machine-a')
        # if logger.isEnabledFor(logging.DEBUG):
        #     append_msg_with_datatime(instance=self,msg=f"Output: {error_output}",last=True)
        return failed,error_output

  
    def start(self, notifier: ProgressNotifierPort) -> None:
        """
        Orquestacion del inicio: Define la secuencia de eventos.
        """
        container_provider = ContainerAdapter()
        checks: list[Tuple[str, CheckFunc]] = [
            ("Creating exercise containers", partial(self._create_containers, container_provider)),
            ("Installing required packages", self._install_packages),
            # Añadir mas checks...
        ]
        notifier.run_checks('start', checks)
    
    def finish(self, notifier: ProgressNotifierPort) -> None:
        """
        Orquestacion del finalizacion: Define la secuencia de eventos.
        """
        container_provider = ContainerAdapter()
        checks: list[Tuple[str, CheckFunc]] = [
            ("Removing exercise containers", partial(self._delete_containers, container_provider)),
            # Añadir mas checks...
        ]
        notifier.run_checks('finish', checks)