import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

def convert_to_rub(transaction):
    try:
        amount = float(transaction['operationAmount']['amount'])
        currency = transaction['operationAmount']['currency']['code']
    except (KeyError, TypeError, ValueError):
        return 0.0

    if currency == 'RUB':
        return amount

    if currency in ['USD', 'EUR']:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={amount}"
        headers = {"apikey": API_KEY}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return float(data.get('result', 0.0))
        except (requests.RequestException, KeyError):
            return 0.0

    return 0.0
