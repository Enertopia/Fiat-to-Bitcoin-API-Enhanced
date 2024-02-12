# Copyright Emiliano German Solazzi Griminger 2023

import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# Configure logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Placeholder for a bank account balance (in fiat)

BANKACCOUNTBALANCE = 100000  # Example starting balance: $100,000

# Placeholder for a Bitcoin wallet balance

WALLET_BALANCE = 0  # Example starting balance: 0 BTC

# Constants

CONVERSION_RATE = 0.000020  # Example conversion rate: 1 fiat = 0.000020 BTC

DEFAULT_PERCENTAGE = 0.05

# Merchant's preset conversion percentage (initially set to the default)

merchantconversionpercentage = DEFAULT_PERCENTAGE

def validate_input_data(data):
    """
    Validate and e