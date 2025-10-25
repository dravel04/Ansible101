from abc import ABC, abstractmethod

class Grader(ABC):
    def __init__(self, exercisename: str):
        self.exercisename = exercisename

    @abstractmethod
    def grade(self):
        """Ejecuta la lógica de evaluación del ejercicio"""
        pass
