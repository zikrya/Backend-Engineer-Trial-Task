from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from services.financial_data_service import FinancialDataService
from services.backtesting_service import BacktestingService

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

        if isinstance(summary, str):
            return JsonResponse({'error': summary}, status=400)

        return JsonResponse(summary, status=200)

def stocks_home_view(request):
    return HttpResponse("Welcome to the Stocks API! Use /stocks/fetch/<symbol> to get stock data.")
