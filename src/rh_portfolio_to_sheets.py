"""
File containing the logic of exporting a Robinhood portfolio to Google Sheets.
"""

import pandas as pd
from typing import Dict

from src.external_services.google_sheets import write_to_sheets
from src.external_services.robinhood import (
    get_rh_portfolio,
)
from src.constants.robinhood import (
    RobinhoodApiData,
    RobinhoodProductTypes,
)
from src.constants.additional_columns import CalculatedColumnManager, ColumnNames
from src.constants.report import (
    BASE_SHEET_HEADERS,
    FUNDAMENTALS_HEADERS,
    DIVIDEND_HEADERS,
)
from src.constants.gsheets import (
    RH_STOCK_DUMP_SHEET_NAME,
    RH_ETF_DUMP_SHEET_NAME,
)
from src.rh_data_util import (
    add_latest_dividend_information,
    add_fundamentals_information,
    get_last_year_and_ytd_dividend,
)


def get_rh_portfolio_as_df(is_live=False, write_mock=False) -> pd.DataFrame:
    portfolio_dict = get_rh_portfolio(is_live=is_live, write_to_mock=write_mock)
    # Transpose to get all attributes as the columns
    portfolio_df = pd.DataFrame(portfolio_dict).transpose()
    # Add indexes as a separate column
    portfolio_df = portfolio_df.reset_index(names=RobinhoodApiData.TICKER.value.name)

    return portfolio_df


def get_spreadsheet_column_headers() -> Dict[str, str]:
    """
    Function to select the column headers to be printed in the sheet.
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
    headers = get_spreadsheet_column_headers()
    column_names = [column for column in headers.keys()]
    portfolio = portfolio[portfolio.columns.intersection(column_names)]

    # Order the columns
    ordered_columns = column_names + (portfolio.columns.drop(column_names).tolist())
    portfolio = portfolio[ordered_columns]

    # Rename column headers
    portfolio = portfolio.rename(columns=headers)

    return portfolio


def add_extra_information(portfolio: pd.DataFrame) -> pd.DataFrame:
    # Get additional information
    print("Getting fundamentals data")
    portfolio = add_fundamentals_information(portfolio)

    print("Getting dividend data")
    portfolio = add_latest_dividend_information(portfolio)

    # Calculated columns
    print("Adding columns for additional calculated information")
    custom_columns = CalculatedColumnManager(portfolio)
    custom_columns.add_total_column()
    custom_columns.add_diversity_column()
    custom_columns.add_projected_dividend_column()
    portfolio = custom_columns.add_dividend_payout_columns(get_last_year_and_ytd_dividend())
    return portfolio


def write_required_columns_to_sheets(portfolio: pd.DataFrame, worksheet_name: str):
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
    write_required_columns_to_sheets(
        stock_portfolio_df, worksheet_name=RH_STOCK_DUMP_SHEET_NAME
    )

    print("Writing ETF portfolio to sheets")
    write_required_columns_to_sheets(
        etf_portfolio_df, worksheet_name=RH_ETF_DUMP_SHEET_NAME
    )
