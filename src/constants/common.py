from enum import Enum


MONTHS_IN_QUARTER = 3
UTF_8 = 'utf-8'


class DataFrameMergeType(Enum):
    INNER = "inner"
    LEFT = "left"
