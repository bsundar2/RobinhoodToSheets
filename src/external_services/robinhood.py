import os
import robin_stocks.robinhood as rh
import pyotp
import time
import json
from typing import Dict, Any

from src.constants.robinhood_constants import (
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


def login():
    credentials = get_credentials()

    totp = pyotp.TOTP(credentials.otp_key).now()
    print(f"OTP: {totp}")

    login_obj = rh.login(credentials.email, credentials.password, mfa_code=totp)
    print(login_obj['detail'])

    return login_obj


def get_rh_portfolio(is_live=False) -> Dict[str, Dict[str, Any]]:
    if is_live:
        login()

        start = time.time()
        print('Sending request to get current portfolio.')
        my_stocks = rh.build_holdings()
        print('Successfully retrieved current portfolio.')
        end = time.time()
        print(f'Time taken to fetch portfolio: {end - start}')

        print(my_stocks)
        return my_stocks
    else:
        with open('data/mock_holdings.json', 'r') as f:
            portfolio = json.load(f)
        return portfolio