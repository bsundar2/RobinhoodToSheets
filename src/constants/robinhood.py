from enum import Enum, StrEnum
from dataclasses import dataclass
from collections import namedtuple

# Environment variables
RH_EMAIL_ENV_VAR = "RH_EMAIL"
RH_PASSWORD_ENV_VAR = "RH_PASSWORD"
RH_OTP_KEY_ENV_VAR = "RH_OTP_KEY"


# RH ticker exceptions
MONTHLY_DIVIDEND_TICKERS = {"STAG", "O", "LAND", "ADC"}

ACCOUNT_BUYING_POWER = "buying_power"

# RH specific types
RobinhoodDataType = namedtuple(
    "RobinhoodDataType", field_names=["name", "label", "type", "category"]
)


@dataclass
class RobinhoodCredentials:
    email: str
    password: str
    otp_key: str


class RobinhoodDividendStatus(StrEnum):
    VOIDED = "voided"
    PENDING = "pending"
    REINVESTED = "reinvested"
    PAID = "paid"


class RobinhoodProductTypes(StrEnum):
    STOCK = "stock"
    ETP = "etp"


class RobinhoodCategories(StrEnum):
    PORTFOLIO = "portfolio"
    FUNDAMENTALS = "fundamentals"
    ID = "id"
    DIVIDEND = "dividend"
    CRYPTO = "crypto"


class RobinhoodApiData(Enum):
    # ID Data
    INSTRUMENT = RobinhoodDataType(
        name="instrument",
        label="Instrument URL",
        type=str,
        category=RobinhoodCategories.ID.value,
    )

    # Portfolio data
    TICKER = RobinhoodDataType(
        name="ticker",
        label="Ticker",
        type=str,
        category=RobinhoodCategories.PORTFOLIO.value,
    )
    NAME = RobinhoodDataType(
        name="name",
        label="Name",
        type=str,
        category=RobinhoodCategories.PORTFOLIO.value,
    )
    AVG_BUY_PRICE = RobinhoodDataType(
        name="average_buy_price",
        label="Avg Price",
        type=float,
        category=RobinhoodCategories.PORTFOLIO.value,
    )
    QUANTITY = RobinhoodDataType(
        name="quantity",
        label="Quantity",
        type=float,
        category=RobinhoodCategories.PORTFOLIO.value,
    )
    TYPE = RobinhoodDataType(
        name="type",
        label="Type",
        type=str,
        category=RobinhoodCategories.PORTFOLIO.value,
    )

    # Fundamentals data
    DESCRIPTION = RobinhoodDataType(
        name="description",
        label="Description",
        type=str,
        category=RobinhoodCategories.FUNDAMENTALS.value,
    )
    SECTOR = RobinhoodDataType(
        name="sector",
        label="Sector",
        type=str,
        category=RobinhoodCategories.FUNDAMENTALS.value,
    )
    INDUSTRY = RobinhoodDataType(
        name="industry",
        label="Industry",
        type=str,
        category=RobinhoodCategories.FUNDAMENTALS.value,
    )
    SYMBOL = RobinhoodDataType(
        name="symbol",
        label="Symbol",
        type=str,
        category=RobinhoodCategories.FUNDAMENTALS.value,
    )

    # Dividend data
    DVD_STATUS = RobinhoodDataType(
        name="state",
        label="DVD Status",
        type=str,
        category=RobinhoodCategories.DIVIDEND.value,
    )
    PAYABLE_DATE = RobinhoodDataType(
        name="payable_date",
        label="Dividend Date",
        type=str,
        category=RobinhoodCategories.DIVIDEND.value,
    )
    PAID_AT_DATE = RobinhoodDataType(
        name="paid_at",
        label="Paid At",
        type=str,
        category=RobinhoodCategories.DIVIDEND.value,
    )
    DVD_RATE = RobinhoodDataType(
        name="rate",
        label="DVD Rate",
        type=float,
        category=RobinhoodCategories.DIVIDEND.value,
    )
    DVD_AMOUNT = RobinhoodDataType(
        name="amount",
        label="DVD Amount",
        type=float,
        category=RobinhoodCategories.DIVIDEND.value,
    )
    LAST_DIVIDEND = RobinhoodDataType(
        name="amount",
        label="Last Quarterly Dividend",
        type=float,
        category=RobinhoodCategories.DIVIDEND.value,
    )
    TOTAL_DVD_AMT_PAID = RobinhoodDataType(
        name="amount_paid_to_date",
        label="Total DVD Paid",
        type=float,
        category=RobinhoodCategories.DIVIDEND.value,
    )


class CryptoDataKeys(StrEnum):
    CURRENCY = "currency"
    TICKER_CODE = "code"
    NAME = "name"
    QUANTITY = "quantity_available"
    COST_BASES = "cost_bases"
    DIRECT_COST_BASIS = "direct_cost_basis"
    DIRECT_QUANTITY = "direct_quantity"
