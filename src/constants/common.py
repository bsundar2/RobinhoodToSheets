from enum import StrEnum


MONTHS_IN_QUARTER = 3
UTF_8 = 'utf-8'


class DataFrameMergeType(StrEnum):
    INNER = "inner"
    LEFT = "left"
    OUTER = "outer"
