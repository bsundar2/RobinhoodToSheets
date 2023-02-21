from enum import Enum


class SheetHeaders(Enum):
    TICKER = 'Ticker'
    NAME = 'Name'
    CURRENT_PRICE = 'Curr Price'
    AVG_PRICE = 'Avg Price'
    QTY = 'Qty'
    TOTAL = 'Total'
    DIVIDEND = 'Dividend'
    DIVIDEND_PER_QTR = 'DVD / Qtr'
    DIVIDEND_PER_YEAR = 'DVD / Yr'
    DIVIDEND_YIELD = 'Dividend Yield'
    DIVERSITY = 'Diversity'
    EQUITY = 'Equity'
    PE_RATIO = 'PE Ratio'
