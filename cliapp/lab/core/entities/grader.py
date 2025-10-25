from abc import ABC, abstractmethod

class Grader(ABC):
    def __init__(self, exercisename: str):
        self.exercisename = exercisename

    @abstractmethod
    def grade(self):
        """Ejecuta la logica de evaluacion del ejercicio"""
        pass
