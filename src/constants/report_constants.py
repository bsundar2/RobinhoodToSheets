from src.constants.robinhood_constants import RobinhoodApiData
from src.constants.column_constants import ColumnNames


SHEET_HEADERS = {
    RobinhoodApiData.TICKER.value.name: 'Ticker',
    RobinhoodApiData.NAME.value.name: 'Name',
    RobinhoodApiData.AVG_BUY_PRICE.value.name: 'Avg Price',
    RobinhoodApiData.QUANTITY.value.name: 'Qty',
    ColumnNames.TOTAL.value.name: 'Total',
    ColumnNames.DIVERSITY.value.name: 'Diversity',
    RobinhoodApiData.TOTAL_DIVIDEND.value.name: 'Last Dividend'
}
