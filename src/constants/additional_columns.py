from enum import Enum
from collections import namedtuple
from pandas import DataFrame

from src.constants.robinhood import (
    RobinhoodApiData as RhData
)

ColumnNameDataType = namedtuple('ColumnNameDataType', field_names=['name', 'label', 'type'])


class ColumnNames(Enum):
    TOTAL = ColumnNameDataType(name='total', label='Total' , type='float')
    DIVERSITY = ColumnNameDataType(name='portfolio_diversity', label='Diversity', type='float')


class AdditionalColumns:
    def __init__(self, portfolio: DataFrame):
        self.portfolio = portfolio

    def add_df_columns(self):
        self.portfolio.insert(
            len(self.portfolio.columns),
            ColumnNames.TOTAL.value.name,
            (
                self.portfolio[RhData.AVG_BUY_PRICE.value.name].astype(RhData.AVG_BUY_PRICE.value.type) *
                self.portfolio[RhData.QUANTITY.value.name].astype(RhData.QUANTITY.value.type)
            )
        )
        self.portfolio.insert(
            len(self.portfolio.columns),
            ColumnNames.DIVERSITY.value.name,
            (
                    self.portfolio[ColumnNames.TOTAL.value.name].astype(float) /
                    self.portfolio[ColumnNames.TOTAL.value.name].sum()
            )
        )

        return self.portfolio
