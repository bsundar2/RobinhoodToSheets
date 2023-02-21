from dataclasses import dataclass
from typing import Union

from pandas import Series, DataFrame

from src.constants.robinhood_constants import RobinhoodApiData as RhData


@dataclass
class ColumnOrderType:
    col_name: str
    col_index: int
    col_value: Union[Series, None]


class AdditionalColumns:
    def __init__(self, portfolio: DataFrame):
        self.portfolio = portfolio

    def get_columns(self):
        return [
            ColumnOrderType(
                'total',
                4,
                (
                    self.portfolio[RhData.AVG_BUY_PRICE.value.name].astype(RhData.AVG_BUY_PRICE.value.col_type) *
                    self.portfolio[RhData.QUANTITY.value.col_name].astype(RhData.QUANTITY.value.col_type)
                )
            ),
            ColumnOrderType('dividend', 5, None),
            ColumnOrderType('dividend_per_qtr', 7)
            #ColumnOrderType('dividend_per_year', 8)
            #ColumnOrderType('dividend_yield', 9)
            #ColumnOrderType('portfolio_diversity', 10)
        ]
