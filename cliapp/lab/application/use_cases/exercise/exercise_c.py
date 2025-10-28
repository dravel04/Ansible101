# lab/infrastructure/exercise/e_c.py
from lab.core.entities.exercise import Exercise
from lab.infrastructure.ui.console_utils import run_with_spinner
import logging

logger = logging.getLogger("lab")

class ExerciseC(Exercise):

    def create_containers(self):
        return False

    def install_packages(self):
        return False

    def start(self):
        logger.debug(f"Cargando clase '{self.__class__.__name__}' para el ejercicio '{self.name}'")
        logger.debug(f"Instancia creada: {self.name}")

        checks = [
            ("Creating podman containers",self.create_containers),
            ("Installing required packages",self.install_packages),
        ]
        # 🔹 logica especifica de este ejercicio
        print(f"Iniciando {self.name}...\n")
        run_with_spinner('start', checks)


    def finish(self):
        # 🔹 limpieza especifica de este ejercicio
        print(f"Finalizando {self.name}...\n")
