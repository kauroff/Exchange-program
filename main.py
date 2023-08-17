import json
import os
from datetime import datetime

import requests

API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
CURRENCY_RATES_FILE = 'currency_rates.json'


def main():
    """
        Основная функция программы.
        Получает от пользователя название валюты — USD или EUR,
        получает и выводит на экран текущий курс валюты от API.
        Записывает данные в JSON-файл.
        """
    while True:
        currency = input('Введите название валюты (USD или EUR): ').upper()
        if currency not in ('USD', 'EUR'):
            print('Некорректный ввод')
            continue

        rate = get_currency_rate(currency)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(f'Курс {currency} к рублю: {rate:.2f}')
        data = {'currency': currency, "rate": rate, "timestamp": timestamp}
        save_to_json(data)

        choice = input('Выберите действие (продолжить или выйти): ').lower()
        if choice == 'продолжить':
            continue
        elif choice == 'выйти':
            break
        else:
            print('Некорректный ввод')
            continue


def get_currency_rate(currency: str) -> float:
    """Получает курс по API и возвращает его в виде float."""

    url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency}"
    response = requests.get(url, headers={"apikey": API_KEY})
    rate = response.json()['rates']['RUB']
    return rate


def save_to_json(data: dict) -> None:
    """Сохраняет данные в JSON файл"""

    with open(CURRENCY_RATES_FILE, 'a') as file:
        if os.stat(CURRENCY_RATES_FILE).st_size == 0:
            json.dump([data], file)
        else:
            with open(CURRENCY_RATES_FILE) as json_file:
                data_list = json.load(json_file)
            data_list.append(data)
            with open(CURRENCY_RATES_FILE, 'w') as json_file:
                json.dump(data_list, json_file)


if __name__ == '__main__':
    main()
