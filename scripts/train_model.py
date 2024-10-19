import sys
import os
import django
import numpy as np
import joblib

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trial_task.settings')
django.setup()

from ml.linear_regression import LinearRegression
from stocks_app.models import StockData

def get_combined_historical_data(symbols, days=60):
    """Fetch and combine historical stock data for multiple symbols."""
    all_data = []
    all_symbols = []

    for symbol in symbols:
        historical_data = StockData.objects.filter(stock_symbol=symbol).order_by('-date')[:days]
        data = np.array([float(record.close_price) for record in historical_data])
        all_data.append(data[::-1])  # Reversing to get oldest first
        all_symbols.append([symbol] * len(data))  # Adding stock symbol as a feature

    # Combine all data into one dataset
    combined_data = np.concatenate(all_data)
    combined_symbols = np.concatenate(all_symbols)
    return combined_data, combined_symbols

def train_combined_model(symbols, days=60):

    X_train, stock_symbols = get_combined_historical_data(symbols, days=days)

    X_train_days = np.arange(len(X_train)).reshape(-1, 1)

    Y_train_prices = X_train

    model = LinearRegression(learning_rate=0.0001, iterations=1000)
    model.fit(X_train_days, Y_train_prices)

    save_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models')
    os.makedirs(save_dir, exist_ok=True)
    model_path = os.path.join(save_dir, 'combined_stock_price_model.pkl')
    joblib.dump(model, model_path)

    print(f"Combined model trained and saved successfully at {model_path}!")

train_combined_model(['AAPL', 'GOOG', 'MSFT', 'TSLA', 'AMZN'])
