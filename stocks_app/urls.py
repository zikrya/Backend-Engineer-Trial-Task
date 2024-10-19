from django.urls import path
from .views import fetch_data_view, stocks_home_view
from .views import fetch_data_view, run_backtest_view
from .views import predict_stock_view
from .views import generate_report_view

urlpatterns = [
    path('', stocks_home_view, name='stocks_home'),
    path('fetch/<str:symbol>/', fetch_data_view, name='fetch_data'),
    path('backtest/<str:symbol>/', run_backtest_view, name='run_backtest'),
    path('predict/<str:symbol>/', predict_stock_view, name='predict_stock'),
    path('report/<str:symbol>/', generate_report_view, name='generate_report'),
]

