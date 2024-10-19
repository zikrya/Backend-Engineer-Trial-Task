from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from services.financial_data_service import FinancialDataService
from services.backtesting_service import BacktestingService
from services.prediction_service import PredictionService
from services.report_service import ReportService
import logging

logger = logging.getLogger(__name__)

def fetch_data_view(request, symbol):
    if request.method == 'GET':
        try:
            symbol = symbol.upper()
            stock_data = FinancialDataService.fetch_stock_data(symbol)

            if isinstance(stock_data, str):
                return JsonResponse({'error': stock_data}, status=500)

            return JsonResponse({'data': stock_data}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def run_backtest_view(request, symbol):
    if request.method == 'GET':
        initial_investment = request.GET.get('initial_investment', 10000)
        try:
            initial_investment = float(initial_investment)
        except ValueError:
            return JsonResponse({'error': 'Invalid investment amount'}, status=400)

        summary = BacktestingService.run_backtest(symbol, initial_investment)

        if 'error' in summary:
            return JsonResponse({'error': summary['error']}, status=400)

        logger.info(f"Backtest run for {symbol} completed successfully: {summary}")
        return JsonResponse(summary, status=200)

def predict_stock_view(request, symbol):
    """API endpoint to predict stock prices for the next 30 days."""
    if request.method == 'GET':
        try:
            predictions = PredictionService.predict_stock_prices(symbol)
            logger.info(f"Predictions generated for {symbol}")
            return JsonResponse({
                'symbol': symbol,
                'predictions': list(predictions),
            }, status=200)
        except Exception as e:
            logger.error(f"Error predicting stock prices for {symbol}: {e}")
            return JsonResponse({'error': str(e)}, status=500)

def generate_report_view(request, symbol):

    report_format = request.GET.get('format', 'json')

    if report_format == 'json':
        report = ReportService.generate_json_report(symbol)
        return JsonResponse(report, status=200)

    elif report_format == 'pdf':
        pdf_report = ReportService.generate_pdf_report(symbol)
        response = HttpResponse(pdf_report, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{symbol}_report.pdf"'
        return response

    else:
        return JsonResponse({'error': 'Invalid format requested. Use "json" or "pdf".'}, status=400)

def stocks_home_view(request):
    return HttpResponse("Welcome to the Stocks API! Use /stocks/fetch/<symbol> to get stock data.")
