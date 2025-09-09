# lab/exercise/exercise_a.py
from lab.exercise.exercise import Exercise

class ExerciseA(Exercise):
    def start(self):
        # 🔹 lógica específica de este ejercicio
        print(f"Iniciando {self.name} (lógica de ExerciseA)...")


    def finish(self):
        # 🔹 limpieza específica de este ejercicio
        print(f"Finalizando {self.name} (lógica de ExerciseA)...")
