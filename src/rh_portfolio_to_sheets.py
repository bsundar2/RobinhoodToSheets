"""
File containing the logic of exporting a Robinhood portfolio to Google Sheets.
"""
import pandas as pd
from functools import cache
from typing import Dict

from src.external_services.robinhood import (
    get_rh_portfolio,
    get_stock_fundamentals,
    get_dividends,
)
from src.external_services.google_sheets import write_to_sheets
from src.constants.robinhood import (
    RobinhoodApiData,
    RobinhoodProductTypes,
    RobinhoodDividendStatus,
    RobinhoodCategories,
    MONTHLY_DIVIDEND_TICKERS,
)
from src.constants.additional_columns import AdditionalColumns, ColumnNames
from src.constants.report import (
    BASE_SHEET_HEADERS,
    FUNDAMENTALS_HEADERS,
    DIVIDEND_HEADERS,
)
from src.constants.common import DataFrameMergeType, MONTHS_IN_QUARTER
from src.constants.gsheets import (
    RH_STOCK_DUMP_SHEET_NAME,
    RH_ETF_DUMP_SHEET_NAME,
)


def get_rh_portfolio_as_df(is_live=False, write_mock=False) -> pd.DataFrame:
    portfolio_dict = get_rh_portfolio(is_live=is_live, write_to_mock=write_mock)
    # Transpose to get all attributes as the columns
    portfolio_df = pd.DataFrame(portfolio_dict).transpose()
    # Add indexes as a separate column
    portfolio_df = portfolio_df.reset_index(names=RobinhoodApiData.TICKER.value.name)

    return portfolio_df


def select_report_headers() -> Dict[str, str]:
    """
    Function to select the report headers to be printed.
    :return: Dictionary mapping header name to value text that is printed
    """
    headers = BASE_SHEET_HEADERS.copy()
    headers.update(FUNDAMENTALS_HEADERS)
    headers.update(DIVIDEND_HEADERS)

    return headers


def select_portfolio_columns(portfolio: pd.DataFrame) -> pd.DataFrame:
    """
    Function to select and order the required columns from the dataframe.
    :param portfolio: DataFrame object
    :return: DataFrame
    """
    # Select required columns
    headers = select_report_headers()
    column_names = [column for column in headers.keys()]
    portfolio = portfolio[portfolio.columns.intersection(column_names)]

    # Order the columns
    ordered_columns = column_names + (portfolio.columns.drop(column_names).tolist())
    portfolio = portfolio[ordered_columns]

    # Rename column headers
    portfolio = portfolio.rename(columns=headers)

    return portfolio


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


def add_extra_information(portfolio: pd.DataFrame) -> pd.DataFrame:
    # Calculated total and diversity columns
    user_columns = AdditionalColumns(portfolio)
    portfolio = user_columns.add_total_column()

    user_columns = AdditionalColumns(portfolio)
    portfolio = user_columns.add_diversity_column()

    # Additional information
    print("Getting fundamentals data")
    portfolio = add_fundamentals_information(portfolio)

    print("Getting dividend data")
    portfolio = add_dividend_information(portfolio)

    # Calculated projected dividend column
    user_columns = AdditionalColumns(portfolio)
    portfolio = user_columns.add_projected_dividend_column()

    return portfolio


def write_required_columns(portfolio: pd.DataFrame, worksheet_name: str):
    print("Adding additional columns and information")
    portfolio = add_extra_information(portfolio)

    print("Sorting values by total invested")
    portfolio = portfolio.sort_values(by=ColumnNames.TOTAL.value.name, ascending=False)

    print("Dropping columns that are not required")
    portfolio = select_portfolio_columns(portfolio)

    write_to_sheets(portfolio, worksheet_name)


def export_rh_portfolio_to_sheets(is_live, write_mock) -> None:
    """
    Driver function to get user's portfolio from Robinhood and write it to a Google sheet.
    :param is_live: Boolean to control whether portfolio data is fetched from Robinhood or mock file
    :param write_mock: Boolean to control whether portfolio data is written to mock file
    :return:
    """
    print("Getting RH portfolio as dataframe")
    portfolio_df = get_rh_portfolio_as_df(is_live, write_mock)

    print("Replace NaN with 0 across DF")
    portfolio_df = portfolio_df.fillna(0)

    print("Filter data based on portfolio type - stocks, ETFs")
    stock_portfolio_df = portfolio_df[
        portfolio_df[RobinhoodApiData.TYPE.value.name]
        != RobinhoodProductTypes.ETP.value
    ]
    etf_portfolio_df = portfolio_df[
        portfolio_df[RobinhoodApiData.TYPE.value.name]
        == RobinhoodProductTypes.ETP.value
    ]

    print("Writing stock portfolio to sheets")
    write_required_columns(stock_portfolio_df, worksheet_name=RH_STOCK_DUMP_SHEET_NAME)

    print("Writing ETF portfolio to sheets")
    write_required_columns(etf_portfolio_df, worksheet_name=RH_ETF_DUMP_SHEET_NAME)
