# lab/application/use_cases/grader/__init__.py
from .grader_vars import GraderVars
from .grader_role import GraderRole
from .grader_webservers import GraderWebservers

GRADERS = {
    "vars": GraderVars,
    "role": GraderRole,
    "webservers": GraderWebservers
}
