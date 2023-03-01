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
                5,
                (
                    self.portfolio[RhData.AVG_BUY_PRICE.value.name].astype(RhData.AVG_BUY_PRICE.value.type) *
                    self.portfolio[RhData.QUANTITY.value.name].astype(RhData.QUANTITY.value.type)
                )
            ),
            ColumnOrderType('dividend', 6, None),
            ColumnOrderType('dividend_per_qtr', 7, None)
            #ColumnOrderType('dividend_per_year', 8)
            #ColumnOrderType('dividend_yield', 9)
            #ColumnOrderType('portfolio_diversity', 10)
        ]
