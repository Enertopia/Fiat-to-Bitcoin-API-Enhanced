# Copyright Emiliano German Solazzi Griminger 2024

from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from decimal import Decimal
import logging
from os import environ

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["5 per minute"]
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ConversionService:
    def __init__(self):
        self.bank_account_balance = Decimal(environ.get('BANK_ACCOUNT_BALANCE', '100000'))
        self.wallet_balance = Decimal(environ.get('WALLET_BALANCE', '0'))
        self.conversion_rate = Decimal(environ.get('CONVERSION_RATE', '0.000020'))
        self.default_percentage = Decimal(environ.get('DEFAULT_PERCENTAGE', '0.05'))

    def validate_input_data(self, data):
        try:
            amount_fiat = Decimal(data.get('amountfiat'))
            conversion_percentage = Decimal(data.get('conversionpercentage', str(self.default_percentage)))
            if not Decimal('0') <= conversion_percentage <= Decimal('1'):
                raise ValueError("Conversion percentage must be between 0 and 1.")
            return amount_fiat, conversion_percentage
        except (ValueError, TypeError, ArithmeticError) as e:
            raise ValueError(f"Invalid input: {e}")

    def convert_fiat_to_bitcoin(self, amount_fiat, conversion_percentage):
        total_amount_to_convert = amount_fiat * conversion_percentage
        self.bank_account_balance -= total_amount_to_convert
        amount_to_wallet = total_amount_to_convert * self.conversion_rate
        amount_to_bank_account = amount_fiat - total_amount_to_convert
        self.wallet_balance += amount_to_wallet
        conversion_details = {
            'amount_fiat': str(amount_fiat),
            'amount_to_wallet': str(amount_to_wallet),
            'amount_to_bank_account': str(amount_to_bank_account),
            'conversion_rate': str(self.conversion_rate),
            'merchant_conversion_percentage': str(conversion_percentage),
            'bank_account_balance': str(self.bank_account_balance),
            'wallet_balance': str(self.wallet_balance)
        }
        return conversion_details

service = ConversionService()

@app.route('/convert', methods=['POST'])
@limiter.limit("5 per minute")
def convert_to_bitcoin():
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No data provided")
        amount_fiat, conversion_percentage = service.validate_input_data(data)
        conversion_details = service.convert_fiat_to_bitcoin(amount_fiat, conversion_percentage)
        return jsonify(conversion_details), 200
    except ValueError as e:
        logging.error(f"Invalid input: {e}")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

if __name__ == '__main__':
    port = int(environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, ssl_context='adhoc')
