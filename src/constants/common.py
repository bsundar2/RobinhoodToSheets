from enum import Enum


MONTHS_IN_QUARTER = 3


class DataFrameMergeType(Enum):
    INNER = "inner"
    LEFT = "left"
