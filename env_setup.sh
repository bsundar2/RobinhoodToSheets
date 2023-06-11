#!/bin/bash

# This file is to be run after activating the virtualenv using `source env_setup.sh`

# Setup Python dependencies
yes | pip install -r requirements.txt

# Setup required env variables
export RH_EMAIL=""
export RH_PASSWORD=""
export RH_OTP_KEY=""
