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

def get_historical_data(symbol, days=60):
    historical_data = StockData.objects.filter(stock_symbol=symbol).order_by('-date')[:days]
    data = np.array([float(record.close_price) for record in historical_data])
    return data[::-1]

def train_model(symbol, days=60):
    X_train = get_historical_data(symbol, days=days)
    X_train_days = np.arange(len(X_train)).reshape(-1, 1)
    Y_train_prices = X_train

    model = LinearRegression(learning_rate=0.0001, iterations=1000)
    model.fit(X_train_days, Y_train_prices)

    save_dir = 'models'
    os.makedirs(save_dir, exist_ok=True)

    model_path = os.path.join(save_dir, 'stock_price_model.pkl')
    joblib.dump(model, model_path)
    print(f"Model trained and saved successfully for {symbol} at {model_path}!")

train_model('AAPL')
