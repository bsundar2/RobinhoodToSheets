from enum import Enum
from dataclasses import dataclass
from collections import namedtuple

# Environment variables
RH_EMAIL_ENV_VAR = 'RH_EMAIL'
RH_PASSWORD_ENV_VAR = 'RH_PASSWORD'
RH_OTP_KEY_ENV_VAR = 'RH_OTP_KEY'


# RH ticker exceptions
MONTHLY_DIVIDEND_TICKERS = {
    'LAND',
    'O',
    'SPHD'
}

# RH specific types
RobinhoodDataType = namedtuple('RobinhoodDataType', field_names=['name', 'label', 'type', 'category'])


@dataclass
class RobinhoodCredentials:
    email: str
    password: str
    otp_key: str


class RobinhoodProductTypes(Enum):
    STOCK = 'stock'
    ETP = 'etp'


class RobinhoodCategories(Enum):
    PORTFOLIO = 'portfolio'
    FUNDAMENTALS = 'fundamentals'


class RobinhoodApiData(Enum):
    # Portfolio data
    TICKER = RobinhoodDataType(name='ticker', label='Ticker', type=str, category=RobinhoodCategories.PORTFOLIO.value)
    NAME = RobinhoodDataType(name='name',  label='Name', type=str, category=RobinhoodCategories.PORTFOLIO.value)
    AVG_BUY_PRICE = RobinhoodDataType(name='average_buy_price', label='Avg Price', type=float,
                                      category=RobinhoodCategories.PORTFOLIO.value)
    QUANTITY = RobinhoodDataType(name='quantity', label='Quantity', type=float,
                                 category=RobinhoodCategories.PORTFOLIO.value)
    TYPE = RobinhoodDataType(name='type', label='Type', type=str, category=RobinhoodCategories.PORTFOLIO.value)
    TOTAL_DIVIDEND = RobinhoodDataType(name='total_dividend', label='Last Dividend', type=float,
                                       category=RobinhoodCategories.PORTFOLIO.value)

    # Fundamentals data
    DESCRIPTION = RobinhoodDataType(name='description', label='Description', type=str,
                                    category=RobinhoodCategories.FUNDAMENTALS.value)
    SECTOR = RobinhoodDataType(name='sector', label='Sector', type=str, category=RobinhoodCategories.FUNDAMENTALS.value)
    INDUSTRY = RobinhoodDataType(name='industry', label='Industry', type=str,
                                 category=RobinhoodCategories.FUNDAMENTALS.value)
    SYMBOL = RobinhoodDataType(name='symbol', label='Symbol', type=str, category=RobinhoodCategories.FUNDAMENTALS.value)
