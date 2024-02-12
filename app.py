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
    Validate and extract input data.
    Args:
        data (dict): JSON payload with 'amountfiat' and 'conversionpercentage'.
    Returns:
        Tuple[float, float]: Amount in fiat and conversion percentage.
    Raises:
        ValueError: If input is invalid.
    """
    try:
        amountfiat = float(data.get('amountfiat'))
        conversionpercentage = float(data.get('conversionpercentage', DEFAULT_PERCENTAGE))
        if not 0 <= conversionpercentage <= 1:
            raise ValueError("Conversion percentage must be between 0 and 1.")
        return amountfiat, conversionpercentage
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid input: {e}")

def convert_fiat_to_bitcoin(amountfiat, conversion_percentage):
    """
    Converts a fiat currency amount to Bitcoin.
    Args:
        amount_fiat (float): Amount in fiat currency.
        conversion_percentage (float): Conversion percentage.
    Returns:
        dict: Conversion details.
    """
    totalamounttoconvert = amountfiat * conversion_percentage
    global BANKACCOUNTBALANCE
    BANKACCOUNTBALANCE -= totalamounttoconvert
    amounttowallet = totalamounttoconvert * CONVERSION_RATE
    amounttobankaccount = amountfiat - totalamounttoconvert
    global WALLET_BALANCE
    WALLET_BALANCE += amounttowallet
    conversion_details = {
        'amountfiat': amountfiat,
        'amounttowallet': amounttowallet,
        'amounttobankaccount': amounttobankaccount,
        'conversionrate': CONVERSION_RATE,
        'merchantconversionpercentage': conversion_percentage,
        'bankaccountbalance': BANKACCOUNTBALANCE,
        'walletbalance': WALLET_BALANCE
    }
    return conversion_details

@app.route('/convert', methods=['POST'])
def convert_to_bitcoin():
    """
    Converts a fiat currency amount to Bitcoin.
    Expects a JSON payload with 'amountfiat' and 'conversionpercentage'.
    """
    try:
        data = request.get_json()
        amountfiat, conversionpercentage = validate_input_data(data)
        conversion_details = convert_fiat_to_bitcoin(amountfiat, conversionpercentage)
        return jsonify(conversion_details), 200
    except ValueError as e:
        logging.error(f"Invalid input: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    # Use a production-ready web server like Gunicorn or uWSGI for deployment
    app.run(host='0.0.0.0', port=3000, debug=True)
