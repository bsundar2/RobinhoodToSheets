import os
import robin_stocks.robinhood as rh
import pyotp
import time
import json
from typing import Dict, Any, List
from functools import cache

from src.aws_utilities.kms_decryption import is_base64, decrypt_kms_value
from src.constants.additional_columns import ColumnNames
from src.constants.robinhood import (
    RH_EMAIL_ENV_VAR,
    RH_PASSWORD_ENV_VAR,
    RH_OTP_KEY_ENV_VAR,
    RobinhoodCredentials,
    ACCOUNT_BUYING_POWER,
    CryptoDataKeys,
    RobinhoodApiData,
)


def get_credentials() -> RobinhoodCredentials:
    print("Getting credentials from environment variables.")
    rh_email = os.getenv(RH_EMAIL_ENV_VAR)
    rh_password = os.getenv(RH_PASSWORD_ENV_VAR)
    rh_otp_key = os.getenv(RH_OTP_KEY_ENV_VAR)

    if not any([rh_email, rh_password, rh_otp_key]):
        raise EnvironmentError(
            f"Missing required environment variables: {[RH_EMAIL_ENV_VAR, RH_PASSWORD_ENV_VAR, RH_OTP_KEY_ENV_VAR]}"
        )

    credentials = []
    for secret_value in [rh_email, rh_password, rh_otp_key]:
        if is_base64(secret_value) and len(secret_value) > 16:
            # If the value appears to be base64-encoded (likely encrypted), decrypt it
            print("Encrypted value detected, attempting to decrypt...")
            decrypted_value = decrypt_kms_value(secret_value)
            credentials.append(decrypted_value)
            print(f"Decryption successful")
        else:
            # If it's not encrypted, just use the plain text value
            credentials.append(secret_value)

    return RobinhoodCredentials(*credentials)


@cache
def login() -> Dict[str, Any]:
    credentials = get_credentials()
    totp = pyotp.TOTP(credentials.otp_key).now()
    print(f"OTP: {totp}")

    login_obj = rh.login(
        credentials.email,
        credentials.password,
        mfa_code=totp,
        store_session=False,
        pickle_path="/tmp",  # Lambda's writable directory
    )

    return login_obj


def get_rh_portfolio(is_live=False, write_to_mock=False) -> Dict[str, Dict[str, Any]]:
    if is_live:
        login()

        start = time.time()
        print("Sending request to get current portfolio.")
        my_stocks = rh.build_holdings(with_dividends=True)
        print("Successfully retrieved current portfolio.")
        end = time.time()
        print(f"Time taken to fetch portfolio: {end - start} seconds")

        if write_to_mock:
            print("Writing portfolio to mock holdings file")
            with open("data/mock_holdings.json", "w") as mock_holding_file:
                json.dump(my_stocks, mock_holding_file)

        return my_stocks
    else:
        with open("data/mock_holdings.json", "r") as f:
            portfolio = json.load(f)
        return portfolio


def get_stock_fundamentals(tickers: List[str]) -> List[Dict[str, Any]]:
    login()
    fundamentals = rh.get_fundamentals(tickers)
    return fundamentals


def get_dividends() -> List[Dict[str, Any]]:
    login()
    dividends = rh.get_dividends()
    return dividends


def get_available_cash() -> float:
    login()
    account_profile = rh.profiles.load_account_profile()
    buying_power = account_profile[ACCOUNT_BUYING_POWER]
    return buying_power


def get_crypto_portfolio(is_live=False):
    crypto_data = []
    if is_live:
        login()
        print("Getting crypto portfolio.")
        crypto_positions = rh.crypto.get_crypto_positions()

        for position in crypto_positions:
            # Extract relevant details
            crypto_id = position[CryptoDataKeys.CURRENCY][CryptoDataKeys.TICKER_CODE]
            name = position[CryptoDataKeys.CURRENCY][CryptoDataKeys.NAME]
            quantity = float(position[CryptoDataKeys.QUANTITY])
            average_buy_price = (
                float(
                    position[CryptoDataKeys.COST_BASES][0][
                        CryptoDataKeys.DIRECT_COST_BASIS
                    ]
                )
                / float(
                    position[CryptoDataKeys.COST_BASES][0][
                        CryptoDataKeys.DIRECT_QUANTITY
                    ]
                )
                if position[CryptoDataKeys.COST_BASES]
                else 0
            )

            crypto_data.append(
                {
                    RobinhoodApiData.TICKER.value.label: crypto_id,
                    RobinhoodApiData.NAME.value.label: name,
                    RobinhoodApiData.AVG_BUY_PRICE.value.label: average_buy_price,
                    RobinhoodApiData.QUANTITY.value.label: quantity,
                    ColumnNames.TOTAL.value.label: quantity * average_buy_price,
                }
            )
    return crypto_data
