from enum import Enum
from collections import namedtuple
from pandas import DataFrame

from src.constants.common import DataFrameMergeType
from src.constants.robinhood import RobinhoodApiData as RhData, RobinhoodApiData

ColumnNameDataType = namedtuple(
    "ColumnNameDataType", field_names=["name", "label", "type"]
)


class ColumnNames(Enum):
    """
    Enum to store custom user-defined columns.
    """

    TOTAL = ColumnNameDataType(name="total", label="Total", type="float")
    DIVERSITY = ColumnNameDataType(
        name="portfolio_diversity", label="Diversity", type="float"
    )
    PROJECTED_DVD = ColumnNameDataType(
        name="projected_dvd", label="Projected DVD", type="float"
    )
    LAST_YEAR_DVD = ColumnNameDataType(
        name="last_year_dvd", label="Last Year's DVD", type="float"
    )
    YTD_DVD = ColumnNameDataType(name="ytd_dvd", label="YTD DVD", type="float")


class CalculatedColumnManager:
    """
    Column manager class to help add calculated user-defined columns to a DataFrame.
    """

    def __init__(self, portfolio: DataFrame):
        self.portfolio = portfolio

    def add_total_column(self) -> None:
        """
        Function to calculate the total value of a holding.
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

    def add_diversity_column(self) -> None:
        """
        Function to calculate the portfolio's diversity.
        """
        self.portfolio.insert(
            len(self.portfolio.columns),
            ColumnNames.DIVERSITY.value.name,
            (
                self.portfolio[ColumnNames.TOTAL.value.name].astype(float)
                / self.portfolio[ColumnNames.TOTAL.value.name].sum()
            ),
        )

    def add_projected_dividend_column(self) -> None:
        """
        Function to calculate the projected dividend.
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

    def add_dividend_payout_columns(self, dividend_info: DataFrame) -> DataFrame:
        """
        Function to calculate the total dividends paid out in the last year and YTD.
        """
        self.portfolio = self.portfolio.merge(
            dividend_info[
                [RobinhoodApiData.INSTRUMENT.value.name, ColumnNames.LAST_YEAR_DVD.value.name, ColumnNames.YTD_DVD.value.name]
            ],
            how=DataFrameMergeType.LEFT.value,
            on=RobinhoodApiData.INSTRUMENT.value.name,
        )
        self.portfolio[
            [ColumnNames.LAST_YEAR_DVD.value.name, ColumnNames.YTD_DVD.value.name]
        ] = self.portfolio[
            [ColumnNames.LAST_YEAR_DVD.value.name, ColumnNames.YTD_DVD.value.name]
        ].fillna(
            0
        )
        return self.portfolio
