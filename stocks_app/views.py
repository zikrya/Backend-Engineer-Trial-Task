from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from services.financial_data_service import FinancialDataService

def fetch_data_view(request, symbol):
    if request.method == 'GET':
        try:
            symbol = symbol.upper()
            message = FinancialDataService.fetch_stock_data(symbol)
            return JsonResponse({'message': message}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

def stocks_home_view(request):
    return HttpResponse("Welcome to the Stocks API! Use /stocks/fetch/<symbol> to get stock data.")
