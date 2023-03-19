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
RobinhoodDataType = namedtuple('RobinhoodDataType', field_names=['name', 'type'])


@dataclass
class RobinhoodCredentials:
    email: str
    password: str
    otp_key: str


class RobinhoodProductTypes(Enum):
    STOCK = 'stock'
    ETP = 'etp'


class RobinhoodApiData(Enum):
    """
    Ordering of columns is implicit in this class.
    """
    TICKER = RobinhoodDataType(name='ticker', type=str)
    NAME = RobinhoodDataType(name='name', type=str)
    AVG_BUY_PRICE = RobinhoodDataType(name='average_buy_price', type=float)
    QUANTITY = RobinhoodDataType(name='quantity', type=float)
    TYPE = RobinhoodDataType(name='type', type=str)
    TOTAL_DIVIDEND = RobinhoodDataType(name='total_dividend', type=float)
