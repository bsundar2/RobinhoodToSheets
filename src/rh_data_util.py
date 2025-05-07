from datetime import datetime
from functools import cache

import pandas as pd

from src.constants.additional_columns import ColumnNames
from src.constants.common import DataFrameMergeType, MONTHS_IN_QUARTER, PANDAS_ERROR_COERCE
from src.constants.robinhood import (
    RobinhoodApiData,
    RobinhoodDividendStatus,
    RobinhoodCategories,
    MONTHLY_DIVIDEND_TICKERS,
)
from src.external_services.robinhood import get_dividends, get_stock_fundamentals


@cache
def get_dividend_history() -> pd.DataFrame:
    dividends = get_dividends()
    df = pd.DataFrame(dividends)

    # Filter out voided dividends
    df = df[
        df[RobinhoodApiData.DVD_STATUS.value.name]
        != RobinhoodDividendStatus.VOIDED.value
    ]
    return df


def add_latest_dividend_information(portfolio: pd.DataFrame) -> pd.DataFrame:
    """
    Get dividend history of the account and keep only one row containing the latest dividend information for each holding.
    """
    dividend_df = get_dividend_history()

    # Convert payable date column to datetime
    dividend_df[RobinhoodApiData.PAYABLE_DATE.value.name] = pd.to_datetime(
        dividend_df[RobinhoodApiData.PAYABLE_DATE.value.name]
    )

    # Sort by latest payable date
    dividend_df = dividend_df.sort_values(
        by=RobinhoodApiData.PAYABLE_DATE.value.name, ascending=False
    )

    # Group by ticker name
    dividend_groups = dividend_df.groupby(
        by=RobinhoodApiData.INSTRUMENT.value.name, as_index=False
    )
    dividend_df = dividend_groups.first()

    # Merge into portfolio
    portfolio = portfolio.merge(
        dividend_df,
        how=DataFrameMergeType.LEFT.value,
        on=RobinhoodApiData.INSTRUMENT.value.name,
    )

    # Replace NaN with 0 for dividend columns
    for column in RobinhoodApiData:
        if (
            column.value.category == RobinhoodCategories.DIVIDEND.value
            and column.value.type == float
        ):
            portfolio[column.value.name] = portfolio[column.value.name].fillna(0)

    # Update dividend for monthly payout stocks
    portfolio.loc[
        portfolio[RobinhoodApiData.TICKER.value.name].isin(MONTHLY_DIVIDEND_TICKERS),
        [
            RobinhoodApiData.DVD_RATE.value.name,
            RobinhoodApiData.LAST_DIVIDEND.value.name,
        ],
    ] = portfolio.loc[
        portfolio[RobinhoodApiData.TICKER.value.name].isin(MONTHLY_DIVIDEND_TICKERS),
        [
            RobinhoodApiData.DVD_RATE.value.name,
            RobinhoodApiData.LAST_DIVIDEND.value.name,
        ],
    ].apply(
        lambda x: x.astype(float) * MONTHS_IN_QUARTER
    )

    return portfolio


def add_fundamentals_information(portfolio: pd.DataFrame) -> pd.DataFrame:
    """
    Add stock fundamentals to the portfolio dataframe.
    """
    tickers = list(portfolio[RobinhoodApiData.TICKER.value.name])
    fundamentals = get_stock_fundamentals(tickers)

    df = pd.DataFrame(fundamentals)
    portfolio = portfolio.merge(
        df,
        how=DataFrameMergeType.INNER.value,
        left_on=RobinhoodApiData.TICKER.value.name,
        right_on=RobinhoodApiData.SYMBOL.value.name,
    )
    return portfolio


@cache
def get_last_year_and_ytd_dividend():
    """
    Function to get the total dividends received in the previous year and YTD.
    """
    dividend_df = get_dividend_history()
    # Remove future dividend payments and convert pay date to datetime
    dividend_df = dividend_df.dropna(subset=[RobinhoodApiData.PAID_AT_DATE.value.name])
    dividend_df[RobinhoodApiData.PAID_AT_DATE.value.name] = pd.to_datetime(
        dividend_df[RobinhoodApiData.PAID_AT_DATE.value.name]
    )
    # Convert pay date to be timezone-naive
    dividend_df[RobinhoodApiData.PAID_AT_DATE.value.name] = dividend_df[
        RobinhoodApiData.PAID_AT_DATE.value.name
    ].dt.tz_localize(None)

    # Convert the amount column to float
    dividend_df[RobinhoodApiData.DVD_AMOUNT.value.name] = pd.to_numeric(
        dividend_df[RobinhoodApiData.DVD_AMOUNT.value.name], errors=PANDAS_ERROR_COERCE
    )
    # Group by holding and sort by recent pay dates
    dividend_df = dividend_df.sort_values(
        by=[
            RobinhoodApiData.INSTRUMENT.value.name,
            RobinhoodApiData.PAID_AT_DATE.value.name,
        ],
        ascending=[True, False],
    )

    def filter_by_pay_date(start_date: datetime, end_date: datetime, column_name: str) -> pd.DataFrame:
        """
        Filter by dividend pay date and calculate the total amount paid.
        :param start_date: Start date for filtering
        :param end_date: End date for filtering
        :param column_name: Column name to rename 'amount' to
        :return: Dataframe containing sum of dividends paid in the timeframe provided
        """
        filtered_df = dividend_df[
            (dividend_df[RobinhoodApiData.PAID_AT_DATE.value.name] >= start_date)
            & (dividend_df[RobinhoodApiData.PAID_AT_DATE.value.name] <= end_date)
        ]
        # Group by ticker and calculate the total dividends for each period
        totals_df = (
            filtered_df.groupby(RobinhoodApiData.INSTRUMENT.value.name)[
                RobinhoodApiData.DVD_AMOUNT.value.name
            ]
            .sum()
            .reset_index()
        )
        totals_df.rename(
            columns={
                RobinhoodApiData.DVD_AMOUNT.value.name: column_name
            },
            inplace=True,
        )
        return totals_df


    # Dates to filter out dividend payments
    today = datetime.today()
    start_of_current_year = datetime(today.year, 1, 1)
    start_of_last_year = datetime(today.year - 1, 1, 1)
    end_of_last_year = datetime(today.year - 1, 12, 31)

    # Filter for dividends paid in the last full calendar year
    last_year_dividends_df = filter_by_pay_date(start_of_last_year, end_of_last_year, column_name=ColumnNames.LAST_YEAR_DVD.value.name)
    # Filter for dividends paid YTD
    ytd_dividends_df = filter_by_pay_date(start_of_current_year, today, column_name=ColumnNames.YTD_DVD.value.name)

    # Merge the two totals
    total_dividends = pd.merge(
        last_year_dividends_df,
        ytd_dividends_df,
        on=RobinhoodApiData.INSTRUMENT.value.name,
        how=DataFrameMergeType.OUTER,
    ).fillna(0)
    return total_dividends
