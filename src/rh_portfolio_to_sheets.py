"""
File containing the logic of exporting a Robinhood portfolio to Google Sheets.
"""
import pandas as pd

from src.external_services.robinhood import (
    get_rh_portfolio,
    get_stock_fundamentals
)
from src.external_services.google_sheets import write_to_sheets
from src.constants.robinhood_constants import (
    RobinhoodApiData,
    RobinhoodProductTypes
)
from src.constants.column_constants import AdditionalColumns, ColumnNames
from src.constants.report_constants import BASE_SHEET_HEADERS, FUNDAMENTALS_HEADERS
from src.constants.gsheets_constants import (
    RH_STOCK_DUMP_SHEET_NAME,
    RH_ETF_DUMP_SHEET_NAME,
)


def get_rh_portfolio_as_df() -> pd.DataFrame:
    portfolio_dict = get_rh_portfolio(is_live=False, write_to_mock=False)
    # Transpose to get all attributes as the columns
    portfolio_df = pd.DataFrame(portfolio_dict).transpose()
    # Add indexes as a separate column
    portfolio_df = portfolio_df.reset_index(names=RobinhoodApiData.TICKER.value.name)

    return portfolio_df


def select_portfolio_columns(portfolio: pd.DataFrame, add_fundamentals=False) -> pd.DataFrame:
    """
    Function to select and order the required columns from the dataframe.
    :param add_fundamentals:
    :param portfolio: DataFrame object
    :return: DataFrame
    """
    # Select required columns
    headers = BASE_SHEET_HEADERS.copy()
    if add_fundamentals:
        headers.update(FUNDAMENTALS_HEADERS)
    column_names = [column for column in headers.keys()]
    portfolio = portfolio[portfolio.columns.intersection(column_names)]

    # Order the columns
    ordered_columns = column_names + (portfolio.columns.drop(column_names).tolist())
    portfolio = portfolio[ordered_columns]

    # Rename column headers
    portfolio = portfolio.rename(columns=headers)

    return portfolio


def add_fundamentals_information(portfolio: pd.DataFrame) -> pd.DataFrame:
    tickers = list(portfolio[RobinhoodApiData.TICKER.value.name])
    fundamentals = get_stock_fundamentals(tickers)

    df = pd.DataFrame(fundamentals)
    df = df.rename(columns={RobinhoodApiData.SYMBOL.value.name: RobinhoodApiData.TICKER.value.name})

    portfolio = portfolio.merge(df, on=[RobinhoodApiData.TICKER.value.name])
    return portfolio


def add_extra_information(portfolio: pd.DataFrame, add_fundamentals=False) -> pd.DataFrame:

    # Calculated columns
    user_columns = AdditionalColumns(portfolio)
    portfolio = user_columns.add_df_columns()

    # Additional information
    if add_fundamentals:
        print('Getting fundamentals data')
        portfolio = add_fundamentals_information(portfolio)

    return portfolio


def write_required_columns(portfolio: pd.DataFrame, worksheet_name: str, add_fundamentals=False):
    print('Adding additional columns and information')
    portfolio = add_extra_information(portfolio, add_fundamentals)

    print('Sorting values by total invested')
    portfolio = portfolio.sort_values(by=[ColumnNames.TOTAL.value.name], ascending=False)

    print('Dropping columns that are not required')
    portfolio = select_portfolio_columns(portfolio, add_fundamentals)

    write_to_sheets(portfolio, worksheet_name)


def export_rh_portfolio_to_sheets():
    """
    Driver function to get user's portfolio from Robinhood and write it to a Google sheet.
    :return:
    """
    print('Getting RH portfolio as dataframe')
    portfolio_df = get_rh_portfolio_as_df()

    print('Replace NaN with 0 across DF')
    portfolio_df = portfolio_df.fillna(0)

    print('Filter data based on type')
    stock_portfolio_df = portfolio_df[portfolio_df[RobinhoodApiData.TYPE.value.name] != RobinhoodProductTypes.ETP.value]
    etf_portfolio_df = portfolio_df[portfolio_df[RobinhoodApiData.TYPE.value.name] == RobinhoodProductTypes.ETP.value]

    print('Writing stock portfolio to sheets')
    write_required_columns(stock_portfolio_df, worksheet_name=RH_STOCK_DUMP_SHEET_NAME, add_fundamentals=True)

    print('Writing ETF portfolio to sheets')
    write_required_columns(etf_portfolio_df, worksheet_name=RH_ETF_DUMP_SHEET_NAME)
