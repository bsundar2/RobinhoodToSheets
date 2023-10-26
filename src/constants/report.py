from src.constants.robinhood import RobinhoodApiData
from src.constants.additional_columns import ColumnNames


BASE_SHEET_HEADERS = {
    RobinhoodApiData.TICKER.value.name: RobinhoodApiData.TICKER.value.label,
    RobinhoodApiData.NAME.value.name: RobinhoodApiData.NAME.value.label,
    RobinhoodApiData.AVG_BUY_PRICE.value.name: RobinhoodApiData.AVG_BUY_PRICE.value.label,
    RobinhoodApiData.QUANTITY.value.name: RobinhoodApiData.QUANTITY.value.label,
    ColumnNames.TOTAL.value.name: ColumnNames.TOTAL.value.label,
    ColumnNames.DIVERSITY.value.name: ColumnNames.DIVERSITY.value.label,
}

FUNDAMENTALS_HEADERS = {
    RobinhoodApiData.DESCRIPTION.value.name: RobinhoodApiData.DESCRIPTION.value.label,
    RobinhoodApiData.SECTOR.value.name: RobinhoodApiData.SECTOR.value.label,
    RobinhoodApiData.INDUSTRY.value.name: RobinhoodApiData.INDUSTRY.value.label,
}

DIVIDEND_HEADERS = {
    RobinhoodApiData.DVD_RATE.value.name: RobinhoodApiData.DVD_RATE.value.label,
    RobinhoodApiData.LAST_DIVIDEND.value.name: RobinhoodApiData.LAST_DIVIDEND.value.label,
    RobinhoodApiData.TOTAL_DVD_AMT_PAID.value.name: RobinhoodApiData.TOTAL_DVD_AMT_PAID.value.label,
}
