from stocks_app.models import StockData
from services.financial_data_service import FinancialDataService

class DataFetchingService:
    @staticmethod
    def ensure_data_fetched(symbol):
        print(f"Checking data for {symbol}")
        if not StockData.objects.filter(stock_symbol=symbol).exists():
            print(f"Data not found for {symbol}, fetching now.")
            FinancialDataService.fetch_stock_data(symbol)
        else:
            print(f"Data already exists for {symbol}")