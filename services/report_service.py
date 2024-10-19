import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
from stocks_app.models import StockData, PredictionData
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
from services.data_fetching_service import DataFetchingService
from services.backtesting_service import BacktestingService
from services.prediction_service import PredictionService
from django.core.cache import cache

class ReportService:
    @staticmethod
    def fetch_actual_data(symbol):
        stock_data = StockData.objects.filter(stock_symbol=symbol).order_by('-date')[:30]
        if not stock_data.exists():
            raise ValueError(f"No stock data available for {symbol}")
        dates = [data.date for data in stock_data]
        prices = [data.close_price for data in stock_data]
        return dates[::-1], prices[::-1]

    @staticmethod
    def fetch_predicted_data(symbol):
        predicted_data = PredictionData.objects.filter(stock_symbol=symbol).order_by('date')
        if not predicted_data.exists():
            raise ValueError(f"No predicted data available for {symbol}")
        dates = [data.date for data in predicted_data]
        prices = [data.predicted_price for data in predicted_data]
        return dates, prices

    @staticmethod
    def generate_graph(actual_dates, actual_prices, predicted_dates, predicted_prices):
        fig, ax1 = plt.subplots(figsize=(10, 5))

        ax1.plot(actual_dates, actual_prices, label='Actual Prices', color='blue', marker='o')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Actual Prices', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        ax2 = ax1.twinx()
        ax2.plot(predicted_dates, predicted_prices, label='Predicted Prices', color='red', linestyle='--', marker='x')
        ax2.set_ylabel('Predicted Prices', color='red')
        ax2.tick_params(axis='y', labelcolor='red')

        plt.title('Actual vs Predicted Stock Prices')
        plt.xticks(rotation=45)
        plt.grid(True)

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        graph_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()

        return graph_base64

    @staticmethod
    def ensure_data_ready(symbol):
        try:
            DataFetchingService.ensure_data_fetched(symbol)
            backtest_result = BacktestingService.run_backtest(symbol, initial_investment=10000)
            PredictionService.predict_stock_prices(symbol)
        except ValueError as e:
            raise ValueError(f"Error ensuring data is ready: {str(e)}")
        return backtest_result

    @staticmethod
    def generate_json_report(symbol):
        cache_key = f"json_report_{symbol}"
        cached_report = cache.get(cache_key)
        if cached_report:
            return cached_report

        try:
            backtest_result = ReportService.ensure_data_ready(symbol)
            actual_dates, actual_prices = ReportService.fetch_actual_data(symbol)
            predicted_dates, predicted_prices = ReportService.fetch_predicted_data(symbol)
        except ValueError as e:
            return {"error": str(e)}

        graph_base64 = ReportService.generate_graph(actual_dates, actual_prices, predicted_dates, predicted_prices)

        report = {
            "symbol": symbol,
            "total_return": backtest_result.get('total_return', 0),
            "max_drawdown": backtest_result.get('max_drawdown', 0),
            "trades_executed": backtest_result.get('trades_executed', 0),
            "graph": graph_base64
        }

        cache.set(cache_key, report, timeout=60 * 15)
        return report

    @staticmethod
    def generate_pdf_report(symbol):
        cache_key = f"pdf_report_{symbol}"
        cached_report = cache.get(cache_key)
        if cached_report:
            return cached_report

        try:
            backtest_result = ReportService.ensure_data_ready(symbol)
            actual_dates, actual_prices = ReportService.fetch_actual_data(symbol)
            predicted_dates, predicted_prices = ReportService.fetch_predicted_data(symbol)
        except ValueError as e:
            return None  # Handle error in view

        graph_base64 = ReportService.generate_graph(actual_dates, actual_prices, predicted_dates, predicted_prices)

        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)

        # Adding title and metadata
        pdf.setTitle(f"{symbol} Stock Report")
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(100, 750, f"Stock Report for {symbol}")
        pdf.setFont("Helvetica", 14)
        pdf.drawString(100, 730, f"Total Return: {backtest_result.get('total_return', 0):.2f}%")
        pdf.drawString(100, 710, f"Max Drawdown: {backtest_result.get('max_drawdown', 0):.2f}%")
        pdf.drawString(100, 690, f"Trades Executed: {backtest_result.get('trades_executed', 0)}")

        pdf.drawString(100, 670, "Comparison: Actual vs Predicted Stock Prices")

        graph_img = base64.b64decode(graph_base64)
        img_buffer = BytesIO(graph_img)

        image = ImageReader(img_buffer)
        pdf.drawImage(image, 100, 400, width=400, height=200)

        pdf.showPage()
        pdf.save()

        buffer.seek(0)
        pdf_content = buffer.getvalue()

        cache.set(cache_key, pdf_content, timeout=60 * 15)
        return pdf_content
