from lab.exercise.exercise import Exercise

class ExerciseC(Exercise):
    def start(self):
        # 🔹 lógica específica de este ejercicio
        print(f"Iniciando {self.name} (lógica de ExerciseC)...")


    def finish(self):
        # 🔹 limpieza específica de este ejercicio
        print(f"Finalizando {self.name} (lógica de ExerciseC)...")
