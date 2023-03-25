from src.constants.robinhood_constants import RobinhoodApiData
from src.constants.column_constants import ColumnNames


BASE_SHEET_HEADERS = {
    RobinhoodApiData.TICKER.value.name: RobinhoodApiData.TICKER.value.label,
    RobinhoodApiData.NAME.value.name: RobinhoodApiData.NAME.value.label,
    RobinhoodApiData.AVG_BUY_PRICE.value.name: RobinhoodApiData.AVG_BUY_PRICE.value.label,
    RobinhoodApiData.QUANTITY.value.name: RobinhoodApiData.QUANTITY.value.label,
    ColumnNames.TOTAL.value.name: ColumnNames.TOTAL.value.label,
    ColumnNames.DIVERSITY.value.name: ColumnNames.DIVERSITY.value.label,
    RobinhoodApiData.TOTAL_DIVIDEND.value.name: RobinhoodApiData.TOTAL_DIVIDEND.value.label,
}

FUNDAMENTALS_HEADERS = {
    RobinhoodApiData.DESCRIPTION.value.name: RobinhoodApiData.DESCRIPTION.value.label,
    RobinhoodApiData.SECTOR.value.name: RobinhoodApiData.SECTOR.value.label,
    RobinhoodApiData.INDUSTRY.value.name: RobinhoodApiData.INDUSTRY.value.label,
}
