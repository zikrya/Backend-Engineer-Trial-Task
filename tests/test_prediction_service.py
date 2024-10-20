from django.test import TestCase
from unittest.mock import patch
from services.prediction_service import PredictionService
from stocks_app.models import StockData

class PredictionServiceTest(TestCase):

    @patch('services.prediction_service.PredictionService.get_historical_data')
    @patch('services.prediction_service.PredictionService.load_combined_model')
    def test_predict_stock_prices_success(self, mock_model, mock_get_historical_data):
        mock_get_historical_data.return_value = (list(range(60)), ['2024-10-01']*60)
        mock_model.return_value.predict.return_value = [300.0, 305.0, 310.0]

        predictions = PredictionService.predict_stock_prices('AAPL')
        self.assertEqual(len(predictions), 30)
        self.assertEqual(predictions[0], 300.0)

    @patch('services.prediction_service.PredictionService.get_historical_data')
    def test_predict_stock_prices_insufficient_data(self, mock_get_historical_data):
        mock_get_historical_data.return_value = ([], [])

        with self.assertRaises(ValueError) as cm:
            PredictionService.predict_stock_prices('AAPL')

        self.assertEqual(str(cm.exception), "Not enough historical data to make predictions.")
