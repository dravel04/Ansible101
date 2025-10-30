# lab/application/use_cases/exercise/__init__.py
from .exercise_a import ExerciseA
from .exercise_c import ExerciseC

EXERCISES = {
    "a": ExerciseA,
    "c": ExerciseC
}
