# lab/infrastructure/exercise/exercise_a.py
from lab.exercise.exercise import Exercise
from lab.infrastructure.ui.console_utils import run_with_spinner

class ExerciseA(Exercise):

    def create_containers(self):
        return False

    def install_packages(self):
        return False

    def start(self):
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
