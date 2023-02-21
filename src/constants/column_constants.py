from dataclasses import dataclass
from typing import Union

from pandas import Series, DataFrame


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
            ColumnOrderType('total', 4, self.portfolio['average_buy_price'].astype(float) * self.portfolio['quantity'].astype(float)),
            ColumnOrderType('dividend', 5, None),
            ColumnOrderType('dividend_per_qtr', 7)
            #ColumnOrderType('dividend_per_year', 8)
            #ColumnOrderType('dividend_yield', 9)
            #ColumnOrderType('portfolio_diversity', 10)
        ]
