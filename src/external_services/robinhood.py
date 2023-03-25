import os
import robin_stocks.robinhood as rh
import pyotp
import time
import json
from typing import Dict, Any, List
from functools import cache

from src.constants.robinhood import (
    RH_EMAIL_ENV_VAR,
    RH_PASSWORD_ENV_VAR,
    RH_OTP_KEY_ENV_VAR,
    RobinhoodCredentials
)


def get_credentials() -> RobinhoodCredentials:
    rh_email = os.environ.get(RH_EMAIL_ENV_VAR)
    rh_password = os.environ.get(RH_PASSWORD_ENV_VAR)
    rh_otp_key = os.environ.get(RH_OTP_KEY_ENV_VAR)

    if not any([rh_email, rh_password, rh_otp_key]):
        raise EnvironmentError(
            f'Missing required environment variables: {[RH_EMAIL_ENV_VAR, RH_PASSWORD_ENV_VAR, RH_OTP_KEY_ENV_VAR]}'
        )

    return RobinhoodCredentials(rh_email, rh_password, rh_otp_key)


@cache
def login() -> Dict[str, Any]:
    credentials = get_credentials()

    totp = pyotp.TOTP(credentials.otp_key).now()
    print(f"OTP: {totp}")

    login_obj = rh.login(credentials.email, credentials.password, mfa_code=totp)
    print(login_obj['detail'])

    return login_obj


def get_rh_portfolio(is_live=False, write_to_mock=False) -> Dict[str, Dict[str, Any]]:
    if is_live:
        login()

        start = time.time()
        print('Sending request to get current portfolio.')
        my_stocks = rh.build_holdings(with_dividends=True)
        print('Successfully retrieved current portfolio.')
        end = time.time()
        print(f'Time taken to fetch portfolio: {end - start}')

        if write_to_mock:
            print('Writing portfolio to mock holdings file')
            with open('data/mock_holdings.json', 'w') as mock_holding_file:
                json.dump(my_stocks, mock_holding_file)

        print(my_stocks)
        return my_stocks
    else:
        with open('data/mock_holdings.json', 'r') as f:
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
