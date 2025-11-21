# lab/application/use_cases/exercise/__init__.py
from .exercise_vars import ExerciseVars
from .exercise_c import ExerciseC

EXERCISES = {
    "vars": ExerciseVars,
    "c": ExerciseC
}
