from functools import cache

import pandas as pd

from src.constants.common import DataFrameMergeType, MONTHS_IN_QUARTER
from src.constants.robinhood import RobinhoodApiData, RobinhoodDividendStatus, RobinhoodCategories, \
    MONTHLY_DIVIDEND_TICKERS
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


def add_dividend_information(portfolio: pd.DataFrame) -> pd.DataFrame:
    """
    Get dividend history for the portfolio and keep only the latest dividend.
    """
    dividend_df = get_dividend_history()

    # Sort by latest payable date
    dividend_df[RobinhoodApiData.PAYABLE_DATE.value.name] = pd.to_datetime(
        dividend_df[RobinhoodApiData.PAYABLE_DATE.value.name]
    )
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
