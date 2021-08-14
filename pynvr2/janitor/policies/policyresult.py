from enum import Enum


class PolicyResult(Enum):
    IGNORE = 1
    PRESERVE = 2
    DELETE = 3
