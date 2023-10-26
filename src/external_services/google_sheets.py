import pygsheets
import pandas as pd
import time

from src.constants.gsheets import DEFAULT_SPREADSHEET_NAME, SHEETS_AUTHENTICATION_FILE


def write_to_sheets(
    write_data: pd.DataFrame,
    worksheet_name: str,
    spreadsheet_name: str = DEFAULT_SPREADSHEET_NAME,
):
    # Login/Authenticate
    print("Authenticating to Google Sheets")
    gc = pygsheets.authorize(service_account_file=SHEETS_AUTHENTICATION_FILE)

    print("Open sheet to edit")
    sheet = gc.open(spreadsheet_name)
    worksheet = sheet.worksheet_by_title(worksheet_name)
    worksheet.clear()

    print("Write to sheet")
    start = time.time()
    worksheet.set_dataframe(write_data, (1, 1), copy_index=False, copy_head=True)
    end = time.time()
    print(f"Time taken to write to the sheet: {end - start}")
