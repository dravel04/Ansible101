# lab/application/use_cases/exercise/__init__.py
from .exercise_vars import ExerciseVars
from .exercise_role import ExerciseRole
from .exercise_c import ExerciseC

EXERCISES = {
    "vars": ExerciseVars,
    "role": ExerciseRole,
    "c": ExerciseC
}
