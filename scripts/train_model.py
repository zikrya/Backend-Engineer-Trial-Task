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
    """Fetch historical stock data for multiple symbols and combine it."""
    combined_data = []
    combined_labels = []

    for symbol in symbols:
        historical_data = StockData.objects.filter(stock_symbol=symbol).order_by('-date')[:days]

        if historical_data.exists():
            stock_prices = np.array([float(record.close_price) for record in historical_data])
            days_feature = np.arange(len(stock_prices)).reshape(-1, 1)

            # Append to combined dataset
            combined_data.append(days_feature)
            combined_labels.append(stock_prices)
        else:
            print(f"No data found for {symbol}, skipping...")

    # Stack data and labels for all symbols
    if combined_data and combined_labels:
        X_train = np.vstack(combined_data)
        Y_train = np.hstack(combined_labels)
        return X_train, Y_train
    else:
        return None, None

def train_combined_model(symbols, days=60):
    """Train a single Linear Regression model on combined stock data."""
    print(f"Training combined model for symbols: {symbols}")

    # Get combined data for all symbols
    X_train, Y_train = get_combined_historical_data(symbols, days=days)

    if X_train is None or Y_train is None:
        print("No sufficient data to train the model.")
        return

    # Initialize and train the Linear Regression model
    model = LinearRegression(learning_rate=0.0001, iterations=1000)
    model.fit(X_train, Y_train)

    # Save the combined model
    save_dir = 'models'
    os.makedirs(save_dir, exist_ok=True)
    model_path = os.path.join(save_dir, 'combined_stock_price_model.pkl')
    joblib.dump(model, model_path)
    print(f"Combined model trained and saved successfully at {model_path}!")

# Get all available stock symbols from StockData
symbols = StockData.objects.values_list('stock_symbol', flat=True).distinct()

# Train the combined model on all symbols
train_combined_model(symbols, days=60)
