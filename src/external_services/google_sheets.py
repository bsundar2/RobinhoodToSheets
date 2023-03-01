import pygsheets
import pandas as pd
import time

from src.constants.gsheets_constants import DEFAULT_SPREADSHEET_NAME, SHEETS_AUTHENTICATION_FILE
from src.constants.report_constants import SheetHeaders


def initialize_column_headers(worksheet: pygsheets.Worksheet) -> None:
    for idx, item in enumerate(SheetHeaders):
        cell = pygsheets.Cell((1, idx + 1), worksheet=worksheet)
        cell.set_text_format('bold', True)
        cell.set_value(item.value)


def write_to_sheets(write_data: pd.DataFrame, spreadsheet_name: str = DEFAULT_SPREADSHEET_NAME):
    # Login/Authenticate
    print('Authenticating to Google Sheets')
    gc = pygsheets.authorize(service_account_file=SHEETS_AUTHENTICATION_FILE)

    print('Open sheet to edit')
    sheet = gc.open(spreadsheet_name)
    worksheet = sheet[0]
    worksheet.clear()

    print('Write to sheet')
    start = time.time()
    initialize_column_headers(worksheet)
    worksheet.set_dataframe(write_data, (2, 1), copy_index=False, copy_head=False)
    end = time.time()
    print(f'Time taken to write to the sheet: {end - start}')
