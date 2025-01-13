from enum import Enum
from collections import namedtuple
from pandas import DataFrame

from src.constants.robinhood import RobinhoodApiData as RhData

ColumnNameDataType = namedtuple(
    "ColumnNameDataType", field_names=["name", "label", "type"]
)


class ColumnNames(Enum):
    TOTAL = ColumnNameDataType(name="total", label="Total", type="float")
    DIVERSITY = ColumnNameDataType(
        name="portfolio_diversity", label="Diversity", type="float"
    )
    PROJECTED_DVD = ColumnNameDataType(
        name="projected_dvd", label="Projected DVD", type="float"
    )


class CalculatedColumnManager:
    def __init__(self, portfolio: DataFrame):
        self.portfolio = portfolio

    def add_total_column(self) -> DataFrame:
        """
        Function to calculate and add the total value of a holding.
        """
        self.portfolio.insert(
            len(self.portfolio.columns),
            ColumnNames.TOTAL.value.name,
            (
                self.portfolio[RhData.AVG_BUY_PRICE.value.name].astype(
                    RhData.AVG_BUY_PRICE.value.type
                )
                * self.portfolio[RhData.QUANTITY.value.name].astype(
                    RhData.QUANTITY.value.type
                )
            ),
        )

    def add_diversity_column(self) -> DataFrame:
        """
        Function to calculate and add portfolio diversity.
        """
        self.portfolio.insert(
            len(self.portfolio.columns),
            ColumnNames.DIVERSITY.value.name,
            (
                self.portfolio[ColumnNames.TOTAL.value.name].astype(float)
                / self.portfolio[ColumnNames.TOTAL.value.name].sum()
            ),
        )

    def add_projected_dividend_column(self) -> DataFrame:
        """
        Function to calculate and add the projected dividend.
        """
        self.portfolio.insert(
            len(self.portfolio.columns),
            ColumnNames.PROJECTED_DVD.value.name,
            (
                self.portfolio[RhData.DVD_RATE.value.name].astype(
                    RhData.DVD_RATE.value.type
                )
                * self.portfolio[RhData.QUANTITY.value.name].astype(
                    RhData.QUANTITY.value.type
                )
            ),
        )
