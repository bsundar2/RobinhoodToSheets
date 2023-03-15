from src.constants.robinhood_constants import RobinhoodApiData
from src.constants.column_constants import ColumnNames


SHEET_HEADERS = {
    RobinhoodApiData.TICKER.value.name: 'Ticker',
    RobinhoodApiData.NAME.value.name: 'Name',
    RobinhoodApiData.CURR_PRICE.value.name: 'Curr Price',
    RobinhoodApiData.AVG_BUY_PRICE.value.name: 'Avg Price',
    RobinhoodApiData.QUANTITY.value.name: 'Qty',
    ColumnNames.TOTAL.value.name: 'Total',
    RobinhoodApiData.EQUITY.value.name: 'Equity',
    RobinhoodApiData.PE_RATIO.value.name: 'PE Ratio',
    ColumnNames.DIVERSITY.value.name: 'Diversity',
}
