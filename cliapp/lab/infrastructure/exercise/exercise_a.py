# lab/infrastructure/exercise/exercise_a.py
from lab.core.entities.exercise import Exercise
from lab.infrastructure.ui.console_utils import run_with_spinner


class ExerciseA(Exercise):

    def create_containers(self):
        return False

    def install_packages(self):
        return False

    def start(self):
        import logging
        
        logger = logging.getLogger("lab")
        logger.debug(f"Cargando clase '{self.__class__.__name__}' para el ejercicio '{self.name}'")
        logger.debug(f"Instancia creada: {self.name}")

        checks = [
            ("Creating podman containers",self.create_containers),
            ("Installing required packages",self.install_packages),
        ]
        # 🔹 lógica específica de este ejercicio
        print(f"Iniciando {self.name}...\n")
        run_with_spinner('start', checks)


    def finish(self):
        # 🔹 limpieza específica de este ejercicio
        print(f"Finalizando {self.name} (lógica de ExerciseA)...")
