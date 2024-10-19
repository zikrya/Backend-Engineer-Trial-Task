import requests
import os
from datetime import datetime, timedelta
from stocks_app.models import StockData
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

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

            if 'Note' in data and 'Please consider' in data['Note']:
                logger.error(f"Rate limit exceeded for {symbol}.")
                raise ValueError("Rate limit exceeded. Try again later.")

            time_series = data.get('Time Series (Daily)')
            if not time_series:
                logger.error(f"Invalid data received for {symbol}")
                raise ValueError(f"Invalid data received for {symbol}")

            # Filter data from the last 2 years
            two_years_ago = datetime.now().date() - timedelta(days=730)
            stock_data_list = []

            for date_str, price_data in time_series.items():
                date = datetime.strptime(date_str, '%Y-%m-%d').date()

                if date >= two_years_ago:
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
                    logger.info(f"Stored data for {symbol} on {date} (created={created})")
                    stock_data_list.append({
                        'date': date_str,
                        'open': price_data['1. open'],
                        'close': price_data['4. close'],
                        'high': price_data['2. high'],
                        'low': price_data['3. low'],
                        'volume': price_data['5. volume'],
                    })

            logger.info(f"Fetched and processed {len(stock_data_list)} records for {symbol}")
            return stock_data_list

        except requests.exceptions.RequestException as e:
            logger.error(f"Network request error: {e}")
            raise SystemExit(e)
        except ValueError as ve:
            logger.error(f"Data processing error: {ve}")
            return str(ve)
