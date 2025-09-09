# lab/grader/__init__.py
from .grader_a import GraderA
from .grader_b import GraderB
from .grader_c import GraderC

GRADERS = {
    "a": GraderA,
    "b": GraderB,
    "c": GraderC,
}

