import numpy as np
import os
import joblib
import logging
from datetime import timedelta
from stocks_app.models import StockData, PredictionData
from services.data_fetching_service import DataFetchingService

logger = logging.getLogger(__name__)

class PredictionService:
    @staticmethod
    def load_combined_model():
        model_path = 'models/combined_stock_price_model.pkl'
        if os.path.exists(model_path):
            logger.info(f"Loading model from {model_path}")
            return joblib.load(model_path)
        else:
            logger.error("Combined model not found.")
            raise FileNotFoundError("Combined model not found.")

    @staticmethod
    def get_historical_data(symbol, days=60):
        historical_data = StockData.objects.filter(stock_symbol=symbol).order_by('-date')[:days]
        data = np.array([record.close_price for record in historical_data])
        dates = [record.date for record in historical_data]
        return data[::-1], dates[::-1]

    @staticmethod
    def predict_stock_prices(symbol, days=30):
        DataFetchingService.ensure_data_fetched(symbol)

        X_train, dates = PredictionService.get_historical_data(symbol)

        # Sanity check
        if len(X_train) < 30:
            logger.error(f"Not enough data to predict for {symbol}. Need at least 30 days of historical data.")
            raise ValueError("Not enough historical data to make predictions.")

        X_train_days = np.arange(len(X_train)).reshape(-1, 1)
        Y_train_prices = X_train

        model = PredictionService.load_combined_model()

        X_pred_days = np.arange(len(X_train_days), len(X_train_days) + days).reshape(-1, 1)
        predicted_prices = model.predict(X_pred_days)

        # Sanity check
        if np.any(predicted_prices < 0):
            logger.error(f"Invalid predicted prices for {symbol}. Predicted prices should not be negative.")
            raise ValueError("Invalid predicted prices detected.")

        PredictionService.store_predictions(symbol, dates[-1], predicted_prices)

        logger.info(f"Predicted prices for {symbol}: {predicted_prices}")
        return predicted_prices

    @staticmethod
    def store_predictions(symbol, last_date, predicted_prices):
        for i, predicted_price in enumerate(predicted_prices):
            prediction_date = last_date + timedelta(days=i+1)
            PredictionData.objects.update_or_create(
                stock_symbol=symbol,
                date=prediction_date,
                defaults={'predicted_price': predicted_price}
            )
        logger.info(f"Predicted prices for {symbol} saved to database.")
