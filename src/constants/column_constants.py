from enum import Enum
from pandas import DataFrame
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


class AdditionalColumns:
    def __init__(self, portfolio: DataFrame):
        self.portfolio = portfolio

    def add_df_columns(self):
        self.portfolio.insert(
            5,
            ColumnNames.TOTAL.value,
            (
                self.portfolio[RhData.AVG_BUY_PRICE.value.name].astype(RhData.AVG_BUY_PRICE.value.type) *
                self.portfolio[RhData.QUANTITY.value.name].astype(RhData.QUANTITY.value.type)
            )
        )
        self.portfolio.insert(
            9,
            ColumnNames.DIVERSITY.name,
            self.portfolio[ColumnNames.TOTAL.value].astype(float) / self.portfolio[ColumnNames.TOTAL.value].sum()
        )

        return self.portfolio
