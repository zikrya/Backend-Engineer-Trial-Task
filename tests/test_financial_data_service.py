from django.test import TestCase
from unittest.mock import patch
from services.financial_data_service import FinancialDataService

class FinancialDataServiceTest(TestCase):

    @patch('services.financial_data_service.requests.get')
    def test_fetch_stock_data_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "Time Series (Daily)": {
                "2024-09-01": {
                    "1. open": "150.00",
                    "2. high": "155.00",
                    "3. low": "148.00",
                    "4. close": "152.00",
                    "5. volume": "1000000"
                }
            }
        }

        result = FinancialDataService.fetch_stock_data('AAPL')
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['close'], "152.00")

    @patch('services.financial_data_service.requests.get')
    def test_handle_api_rate_limit(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "Note": "Thank you for using Alpha Vantage! Please consider our premium subscription..."
        }

        result = FinancialDataService.fetch_stock_data('AAPL')
        self.assertEqual(result, "Rate limit exceeded. Try again later.")
