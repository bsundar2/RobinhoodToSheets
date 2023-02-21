from enum import Enum
from dataclasses import dataclass

# Environment variables
RH_EMAIL_ENV_VAR = 'RH_EMAIL'
RH_PASSWORD_ENV_VAR = 'RH_PASSWORD'
RH_OTP_KEY_ENV_VAR = 'RH_OTP_KEY'


# RH specific types
@dataclass
class RobinhoodCredentials:
    email: str
    password: str
    otp_key: str


class RobinhoodProductTypes(Enum):
    STOCK = 'stock'
    ETP = 'etp'
    ADR = 'adr'


class RobinhoodColumns(Enum):
    """
    Ordering of columns is implicit in this class.
    """
    NAME = 'name'
    CURR_PRICE = 'price'
    AVG_BUY_PRICE = 'average_buy_price'
    QUANTITY = 'quantity'
    EQUITY = 'equity'
    TYPE = 'type'
    PE_RATIO = 'pe_ratio'


# Google Sheets
DEFAULT_SPREADSHEET_NAME = 'test_rh_python'
