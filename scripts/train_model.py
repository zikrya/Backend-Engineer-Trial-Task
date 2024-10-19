import sys
import os
import django
import numpy as np
import joblib

# Django setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trial_task.settings')
django.setup()

from ml.linear_regression import LinearRegression
from stocks_app.models import StockData

def get_historical_data(symbol, days=60):
    """Fetch historical stock data for the past X days."""
    historical_data = StockData.objects.filter(stock_symbol=symbol).order_by('-date')[:days]
    data = np.array([float(record.close_price) for record in historical_data])
    return data[::-1]

def train_model(symbol, days=60):
    """Train the linear regression model for the given stock symbol."""
    # Get historical data for training
    X_train = get_historical_data(symbol, days=days)
    X_train_days = np.arange(len(X_train)).reshape(-1, 1)  # Feature: day numbers
    Y_train_prices = X_train  # Target: stock prices

    # Initialize and train the model
    model = LinearRegression(learning_rate=0.0001, iterations=1000)
    model.fit(X_train_days, Y_train_prices)

    # Save the model with the symbol name
    save_dir = 'models'
    os.makedirs(save_dir, exist_ok=True)
    model_path = os.path.join(save_dir, f'{symbol}_stock_price_model.pkl')  # Save with symbol name
    joblib.dump(model, model_path)

    print(f"Model trained and saved successfully for {symbol} at {model_path}!")

# Example usage
train_model('AAPL')
