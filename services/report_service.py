import matplotlib
# Set the backend to 'Agg' to avoid GUI issues
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


class ReportService:
    @staticmethod
    def fetch_actual_data(symbol):
        """Fetch actual stock prices for the past 30 days."""
        stock_data = StockData.objects.filter(stock_symbol=symbol).order_by('-date')[:30]
        dates = [data.date for data in stock_data]
        prices = [data.close_price for data in stock_data]
        return dates[::-1], prices[::-1]

    @staticmethod
    def fetch_predicted_data(symbol):
        """Fetch predicted stock prices for the next 30 days."""
        predicted_data = PredictionData.objects.filter(stock_symbol=symbol).order_by('date')
        dates = [data.date for data in predicted_data]
        prices = [data.predicted_price for data in predicted_data]
        return dates, prices

    @staticmethod
    def generate_graph(actual_dates, actual_prices, predicted_dates, predicted_prices):
        """Generate a graph comparing actual vs predicted stock prices."""
        plt.figure(figsize=(10, 5))
        plt.plot(actual_dates, actual_prices, label='Actual Prices', color='blue', marker='o')
        plt.plot(predicted_dates, predicted_prices, label='Predicted Prices', color='red', linestyle='--', marker='x')
        plt.xlabel('Date')
        plt.ylabel('Stock Price')
        plt.title('Actual vs Predicted Stock Prices')
        plt.xticks(rotation=45)
        plt.legend()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        graph_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()

        return graph_base64

    @staticmethod
    def generate_json_report(symbol):
        """Generate the report in JSON format with a base64-encoded graph."""
        actual_dates, actual_prices = ReportService.fetch_actual_data(symbol)
        predicted_dates, predicted_prices = ReportService.fetch_predicted_data(symbol)

        graph_base64 = ReportService.generate_graph(actual_dates, actual_prices, predicted_dates, predicted_prices)

        report = {
            "symbol": symbol,
            "total_return": 431.81,
            "max_drawdown": 77.93,
            "trades_executed": 30,
            "graph": graph_base64
        }
        return report

    @staticmethod
    def generate_pdf_report(symbol):
        """Generate the report in PDF format using ReportLab."""
        actual_dates, actual_prices = ReportService.fetch_actual_data(symbol)
        predicted_dates, predicted_prices = ReportService.fetch_predicted_data(symbol)

        graph_base64 = ReportService.generate_graph(actual_dates, actual_prices, predicted_dates, predicted_prices)

        buffer = BytesIO()

        pdf = canvas.Canvas(buffer, pagesize=letter)

        pdf.setFont("Helvetica", 16)
        pdf.drawString(100, 750, f"Stock Report for {symbol}")
        pdf.setFont("Helvetica", 12)
        pdf.drawString(100, 730, f"Total Return: 431.81%")
        pdf.drawString(100, 710, f"Max Drawdown: 77.93%")
        pdf.drawString(100, 690, f"Trades Executed: 30")

        # Add the graph as an image
        pdf.drawString(100, 670, "Comparison: Actual vs Predicted Stock Prices")

        graph_img = base64.b64decode(graph_base64)
        img_buffer = BytesIO(graph_img)

        image = ImageReader(img_buffer)
        pdf.drawImage(image, 100, 400, width=400, height=200)

        pdf.showPage()
        pdf.save()

        buffer.seek(0)
        return buffer.getvalue()
