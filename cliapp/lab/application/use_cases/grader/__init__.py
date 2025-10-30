# lab/application/use_cases/grader/__init__.py
from .grader_a import GraderA
from .grader_c import GraderC

GRADERS = {
    "a": GraderA,
    "c": GraderC
}
