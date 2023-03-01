from dataclasses import dataclass
from typing import Union
from enum import Enum
from pandas import Series, DataFrame
from numpy import where, ndarray

from src.constants.robinhood_constants import (
    RobinhoodApiData as RhData,
    MONTHLY_DIVIDEND_TICKERS
)


class ColumnNames(Enum):
    TOTAL = 'total'
    DVD_PER_QTR = 'dividend_per_qtr'
    DVD_PER_YEAR = 'dividend_per_year'
    DVD_YIELD = 'dividend_yield'
    DIVERSITY = 'portfolio_diversity'


@dataclass
class ColumnOrderType:
    col_name: str
    col_index: int
    col_value: Union[Series, str, ndarray]


class AdditionalColumns:
    def __init__(self, portfolio: DataFrame):
        self.portfolio = portfolio
        self.columns = [
            ColumnOrderType(
                ColumnNames.TOTAL.value,
                5,
                (
                    self.portfolio[RhData.AVG_BUY_PRICE.value.name].astype(RhData.AVG_BUY_PRICE.value.type) *
                    self.portfolio[RhData.QUANTITY.value.name].astype(RhData.QUANTITY.value.type)
                )
            ),
            ColumnOrderType(
                ColumnNames.DVD_PER_QTR.value,
                8,
                where(
                    self.portfolio[RhData.TICKER.value.name].map(lambda ticker: ticker in MONTHLY_DIVIDEND_TICKERS),
                    self.portfolio[RhData.DIVIDEND_PER_PERIOD.value.name].astype(
                        RhData.DIVIDEND_PER_PERIOD.value.type) * 3,
                    self.portfolio[RhData.DIVIDEND_PER_PERIOD.value.name].astype(RhData.DIVIDEND_PER_PERIOD.value.type)
                )
            ),
            ColumnOrderType(
                ColumnNames.DVD_PER_YEAR.value,
                9,
                self.portfolio[ColumnNames.DVD_PER_QTR.value].astype(float) * 4
            ),
            ColumnOrderType(
                ColumnNames.DVD_YIELD.value,
                10,
                (
                    (
                        self.portfolio[ColumnNames.DVD_PER_YEAR.value].astype(float) /
                        self.portfolio[RhData.QUANTITY.value.name].astype(RhData.QUANTITY.value.type)
                    ) / self.portfolio[RhData.AVG_BUY_PRICE.value.name].astype(RhData.AVG_BUY_PRICE.value.type)
                )
            ),
            ColumnOrderType(
                ColumnNames.DIVERSITY.name,
                11,
                self.portfolio[ColumnNames.TOTAL.value].astype(float) / self.portfolio[ColumnNames.TOTAL.value].sum()
            )
        ]

    def get_columns(self):
        return self.columns
