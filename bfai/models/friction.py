from enum import Enum

class FrictionType(str, Enum):
    TIME_GAP = "time_gap"
    LOOP = "loop"
    HUMAN_DEPENDENCY = "human_dependency"
