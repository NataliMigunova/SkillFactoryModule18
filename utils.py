import json

import requests

from config import keys


class ConvertionException(Exception):
    pass


def get_currency_key(currency: str):
    try:
        return keys[currency]
    except KeyError:
        raise ConvertionException(f'Не удалось обработать валюту {currency}')


class CurrencyConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}')

        from_currency = get_currency_key(quote)
        to_currency = get_currency_key(base)

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://api.exchangeratesapi.io/latest?symbols={from_currency},{to_currency}')
        conversion_response = json.loads(r.content)
        total_base = conversion_response['rates'][to_currency] / conversion_response['rates'][from_currency]
        return total_base * float(amount)
