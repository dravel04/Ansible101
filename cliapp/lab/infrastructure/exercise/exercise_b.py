from lab.core.entities.exercise import Exercise

class ExerciseB(Exercise):
    def start(self):
        # 🔹 lógica específica de este ejercicio
        print(f"Iniciando {self.name} (lógica de ExerciseB)...")


    def finish(self):
        # 🔹 limpieza específica de este ejercicio
        print(f"Finalizando {self.name} (lógica de ExerciseB)...")
