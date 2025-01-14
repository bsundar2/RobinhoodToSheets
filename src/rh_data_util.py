from datetime import datetime
from functools import cache

import pandas as pd

from src.constants.additional_columns import ColumnNames
from src.constants.common import DataFrameMergeType, MONTHS_IN_QUARTER
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
def get_last_years_dividend():
    df = get_dividend_history()
    df = df.dropna(subset=[RobinhoodApiData.PAID_AT_DATE.value.name])
    df[RobinhoodApiData.PAID_AT_DATE.value.name] = pd.to_datetime(
        df[RobinhoodApiData.PAID_AT_DATE.value.name]
    )
    # Ensure that the 'Amount' column is numeric (convert to float)
    df[RobinhoodApiData.DVD_AMOUNT.value.name] = pd.to_numeric(
        df[RobinhoodApiData.DVD_AMOUNT.value.name], errors="coerce"
    )

    # Convert 'Paid At' to timezone-naive
    df[RobinhoodApiData.PAID_AT_DATE.value.name] = df[
        RobinhoodApiData.PAID_AT_DATE.value.name
    ].dt.tz_localize(None)
    df = df.sort_values(
        by=[
            RobinhoodApiData.INSTRUMENT.value.name,
            RobinhoodApiData.PAID_AT_DATE.value.name,
        ],
        ascending=[True, False],
    )

    # Get today's date
    today = datetime.today()
    # Calculate start of the current year (YTD)
    start_of_year = datetime(today.year, 1, 1)
    # Calculate the start and end of the last full calendar year
    start_of_last_year = datetime(today.year - 1, 1, 1)
    end_of_last_year = datetime(today.year - 1, 12, 31)

    # Filter for dividends paid in the last full calendar year (January 1 to December 31 of last year)
    last_year_dividends_df = df[
        (df[RobinhoodApiData.PAID_AT_DATE.value.name] >= start_of_last_year)
        & (df[RobinhoodApiData.PAID_AT_DATE.value.name] <= end_of_last_year)
    ]

    # Filter for dividends paid YTD
    ytd_dividends_df = df[df[RobinhoodApiData.PAID_AT_DATE.value.name] >= start_of_year]

    # Group by ticker and calculate the total dividends for each period
    last_year_totals = (
        last_year_dividends_df.groupby(RobinhoodApiData.INSTRUMENT.value.name)[
            RobinhoodApiData.DVD_AMOUNT.value.name
        ]
        .sum()
        .reset_index()
    )
    last_year_totals.rename(
        columns={
            RobinhoodApiData.DVD_AMOUNT.value.name: ColumnNames.LAST_YEAR_DVD.value.name
        },
        inplace=True,
    )

    ytd_totals = (
        ytd_dividends_df.groupby(
            by=RobinhoodApiData.INSTRUMENT.value.name, as_index=False
        )[RobinhoodApiData.DVD_AMOUNT.value.name]
        .sum()
        .reset_index()
    )
    ytd_totals.rename(
        columns={
            RobinhoodApiData.DVD_AMOUNT.value.name: ColumnNames.YTD_DVD.value.name
        },
        inplace=True,
    )

    # Merge the two summaries together
    total_dividends = pd.merge(
        last_year_totals,
        ytd_totals,
        on=RobinhoodApiData.INSTRUMENT.value.name,
        how=DataFrameMergeType.OUTER,
    ).fillna(0)
    return total_dividends
