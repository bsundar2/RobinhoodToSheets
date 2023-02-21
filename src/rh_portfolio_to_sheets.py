"""
File containing the logic of exporting a Robinhood portfolio to Google Sheets.
"""
import pandas as pd

from src.external_services.robinhood import get_rh_portfolio
from src.constants.robinhood_constants import (
    RobinhoodColumns
)
from src.constants.column_constants import AdditionalColumns


def get_rh_portfolio_as_df() -> pd.DataFrame:
    # Transpose to get all attributes as the columns
    portfolio_dict = get_rh_portfolio(is_live=False)
    portfolio_df = pd.DataFrame(portfolio_dict).transpose()

    return portfolio_df


def reorder_portfolio_columns(portfolio: pd.DataFrame) -> pd.DataFrame:
    column_list = [column.value for column in RobinhoodColumns]
    ordered_columns = column_list + (portfolio.columns.drop(column_list).tolist())
    portfolio = portfolio[ordered_columns]
    return portfolio


def add_extra_columns(portfolio: pd.DataFrame) -> pd.DataFrame:
    user_columns = AdditionalColumns(portfolio)
    for column in user_columns.get_columns():
        portfolio.insert(column.value.col_index,
                         column.value.col_name,
                         value=column.value.col_value)

    return portfolio


def export_rh_portfolio_to_sheets():
    """
    Driver function to get user's portfolio from Robinhood and write it to a Google sheet.
    :return:
    """
    print('Getting RH portfolio as dataframe')
    portfolio_df = get_rh_portfolio_as_df()

    print('Reordering portfolio DF columns')
    portfolio_df = reorder_portfolio_columns(portfolio_df)

    print('Adding additional columns')
    portfolio_df = add_extra_columns(portfolio_df)

    print('Writing DF to sheets')
    # write_to_sheets(portfolio_df)
