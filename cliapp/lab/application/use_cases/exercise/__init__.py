# lab/application/use_cases/exercise/__init__.py
from .exercise_vars import ExerciseVars
from .exercise_role import ExerciseRole
from .exercise_webservers import ExerciseWebServers

EXERCISES = {
    "vars": ExerciseVars,
    "role": ExerciseRole,
    "webservers": ExerciseWebServers
}
