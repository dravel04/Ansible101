# lab/application/use_cases/exercise/exercise_a.py
from typing import Callable, Tuple, Any
# Importamos Puertos del Core
from lab.core.interfaces.container_port import ContainerPort
from lab.core.interfaces.progress_notifier_port import ProgressNotifierPort

# Definimos el tipo de la funcion de chequeo que vamos a pasar al notificador
CheckFunc = Callable[[], Tuple[bool, str]]

class ExerciseA:
    """
    Logica de negocio especifica para la evaluacion y gestion del ejercicio
    """
    def __init__(
        self,
        name: str, 
        notifier: ProgressNotifierPort, 
        container_provider: ContainerPort
    ):
        # Inyeccion de Dependencias: Almacenamos los Puertos
        self.name = name
        self.notifier = notifier
        self.container_provider = container_provider

    def create_containers(self) -> Tuple[bool, str]:
        """
        Implementa una de las tareas (checks) de la secuencia
        """
        container, failed, error_output = self.container_provider.run_container(image="...", name="...")
        return failed, error_output

    def install_packages(self) -> Tuple[bool, str]:
        """ Implementa otra tarea de la secuencia. """
        # ... logica ...
        return True, "Paquetes instalados"
        
    def start(self):
        """
        Orquestacion del inicio: Define la secuencia de eventos.
        """
        checks: list[Tuple[str, CheckFunc]] = [
            ("Creating exercise containers", self.create_containers),
            ("Installing required packages", self.install_packages),
            # Añadir más checks...
        ]
        
        # ✅ CORRECTO: Llama al Puerto de Notificacion. NO sabe si hay un spinner o un log.
        self.notifier.run_checks('start', checks, instance=self)