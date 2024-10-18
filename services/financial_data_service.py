import requests
import os
from datetime import datetime
from stocks_app.models import StockData
from dotenv import load_dotenv

load_dotenv()

ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

BASE_URL = 'https://www.alphavantage.co/query'

class FinancialDataService:
    @staticmethod
    def fetch_stock_data(symbol):
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': 'full',
            'apikey': ALPHA_VANTAGE_API_KEY
        }

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()

            data = response.json()

            if 'Time Series (Daily)' not in data:
                raise ValueError(f"Invalid data received for {symbol}")

            time_series = data['Time Series (Daily)']

            stock_data_list = []

            for date_str, price_data in time_series.items():
                date = datetime.strptime(date_str, '%Y-%m-%d').date()

                stock_data, created = StockData.objects.update_or_create(
                    stock_symbol=symbol,
                    date=date,
                    defaults={
                        'open_price': price_data['1. open'],
                        'close_price': price_data['4. close'],
                        'high_price': price_data['2. high'],
                        'low_price': price_data['3. low'],
                        'volume': price_data['5. volume'],
                    }
                )

                stock_data_list.append({
                    'date': date_str,
                    'open': price_data['1. open'],
                    'close': price_data['4. close'],
                    'high': price_data['2. high'],
                    'low': price_data['3. low'],
                    'volume': price_data['5. volume'],
                })

            return stock_data_list

        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
        except ValueError as ve:
            print(ve)
            return str(ve)
