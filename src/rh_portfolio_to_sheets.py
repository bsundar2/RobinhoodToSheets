"""
File containing the logic of exporting a Robinhood portfolio to Google Sheets.
"""
import pandas as pd

from src.external_services.robinhood import get_rh_portfolio
from src.external_services.google_sheets import write_to_sheets
from src.constants.robinhood_constants import (
    RobinhoodApiData,
    RobinhoodProductTypes
)
from src.constants.column_constants import AdditionalColumns


def get_rh_portfolio_as_df() -> pd.DataFrame:
    portfolio_dict = get_rh_portfolio(is_live=False, write_to_mock=False)
    # Transpose to get all attributes as the columns
    portfolio_df = pd.DataFrame(portfolio_dict).transpose()
    # Add indexes as a separate column
    portfolio_df = portfolio_df.reset_index(names=RobinhoodApiData.TICKER.value.name)

    return portfolio_df


def select_portfolio_columns(portfolio: pd.DataFrame) -> pd.DataFrame:
    """
    Function to select and order the required columns from the dataframe.
    :param portfolio: DataFrame object
    :return: DataFrame
    """
    # Select required columns
    column_names = [column.value.name for column in RobinhoodApiData if column.value.visible]
    portfolio = portfolio[portfolio.columns.intersection(column_names)]

    # Order the columns
    ordered_columns = column_names + (portfolio.columns.drop(column_names).tolist())
    portfolio = portfolio[ordered_columns]

    return portfolio


def add_extra_columns(portfolio: pd.DataFrame) -> pd.DataFrame:
    user_columns = AdditionalColumns(portfolio)
    portfolio = user_columns.add_df_columns()
    return portfolio


def export_rh_portfolio_to_sheets():
    """
    Driver function to get user's portfolio from Robinhood and write it to a Google sheet.
    :return:
    """
    print('Getting RH portfolio as dataframe')
    portfolio_df = get_rh_portfolio_as_df()

    print('Filter out non-equity rows')
    portfolio_df = portfolio_df[portfolio_df[RobinhoodApiData.TYPE.value.name] != RobinhoodProductTypes.ETP.value]

    print('Reordering portfolio DF columns')
    portfolio_df = select_portfolio_columns(portfolio_df)

    print('Adding additional columns')
    portfolio_df = add_extra_columns(portfolio_df)

    print('Writing DF to sheets')
    write_to_sheets(portfolio_df)
