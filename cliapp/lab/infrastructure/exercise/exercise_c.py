from lab.core.entities.exercise import Exercise

class ExerciseC(Exercise):
    def start(self):
        # 🔹 logica especifica de este ejercicio
        print(f"Iniciando {self.name} (logica de ExerciseC)...")


    def finish(self):
        # 🔹 limpieza especifica de este ejercicio
        print(f"Finalizando {self.name} (logica de ExerciseC)...")
