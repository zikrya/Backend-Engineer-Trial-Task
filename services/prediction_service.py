import numpy as np
import os
import joblib
from datetime import timedelta
from stocks_app.models import StockData, PredictionData

class PredictionService:
    @staticmethod
    def load_combined_model():

        model_path = 'models/combined_stock_price_model.pkl'
        if os.path.exists(model_path):
            return joblib.load(model_path)
        else:
            raise FileNotFoundError("Combined model not found.")

    @staticmethod
    def get_historical_data(symbol, days=60):

        historical_data = StockData.objects.filter(stock_symbol=symbol).order_by('-date')[:days]
        data = np.array([record.close_price for record in historical_data])
        dates = [record.date for record in historical_data]
        return data[::-1], dates[::-1]

    @staticmethod
    def predict_stock_prices(symbol, days=30):

        X_train, dates = PredictionService.get_historical_data(symbol)

        X_train_days = np.arange(len(X_train)).reshape(-1, 1)
        Y_train_prices = X_train

        model = PredictionService.load_combined_model()

        X_pred_days = np.arange(len(X_train_days), len(X_train_days) + days).reshape(-1, 1)
        predicted_prices = model.predict(X_pred_days)

        PredictionService.store_predictions(symbol, dates[-1], predicted_prices)

        return predicted_prices

    @staticmethod
    def store_predictions(symbol, last_date, predicted_prices):
        """Store predicted stock prices in the PredictionData model."""
        for i, predicted_price in enumerate(predicted_prices):
            prediction_date = last_date + timedelta(days=i+1)
            PredictionData.objects.update_or_create(
                stock_symbol=symbol,
                date=prediction_date,
                defaults={'predicted_price': predicted_price}
            )
