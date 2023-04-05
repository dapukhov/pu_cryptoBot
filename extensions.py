import requests
import json
from config import exchange, API


class ApiException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: float):
        if quote == base:
            raise ApiException(f'Не удалось совершить перевод - валюты одинаковы - {base}')
        elif float(amount) <= 0:
            raise ApiException(f'Указано отрицательное или нулевое значение для конвертации - {amount}')
        try:
            quote_ticker = exchange[quote]
        except KeyError:
            raise ApiException(f'Не удалось найти валюту {quote}')

        try:
            base_ticker = exchange[base]
        except KeyError:
            raise ApiException(f'Не удалось найти валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ApiException(f'Не удалось обработать количество {amount}! попробуйте использовать "." вместо '
                               f'","\n при указании дробной части')
        r = requests.get(f'https://v6.exchangerate-api.com/v6/{API}/pair/{quote_ticker}/{base_ticker}/{amount}')
        total_base = json.loads(r.content)['conversion_result']

        return round(total_base, 2)
