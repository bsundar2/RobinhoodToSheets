import pygsheets
import pandas as pd
import time

from src.constants.gsheets_constants import (
    DEFAULT_SPREADSHEET_NAME,
    RH_STOCK_DUMP_SHEET_NAME,
    SHEETS_AUTHENTICATION_FILE
)
from src.constants.report_constants import SHEET_HEADERS


def write_to_sheets(write_data: pd.DataFrame, spreadsheet_name: str = DEFAULT_SPREADSHEET_NAME):
    # Login/Authenticate
    print('Authenticating to Google Sheets')
    gc = pygsheets.authorize(service_account_file=SHEETS_AUTHENTICATION_FILE)

    print('Open sheet to edit')
    sheet = gc.open(spreadsheet_name)
    worksheet = sheet.worksheet_by_title(RH_STOCK_DUMP_SHEET_NAME)
    worksheet.clear()

    print('Write to sheet')
    start = time.time()
    # Initialize column headers
    write_data = write_data.rename(columns=SHEET_HEADERS)
    worksheet.set_dataframe(write_data, (1, 1), copy_index=False, copy_head=True)
    end = time.time()
    print(f'Time taken to write to the sheet: {end - start}')
