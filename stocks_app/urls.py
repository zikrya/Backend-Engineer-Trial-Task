from django.urls import path
from .views import fetch_data_view, stocks_home_view

urlpatterns = [
    path('', stocks_home_view, name='stocks_home'),
    path('fetch/<str:symbol>/', fetch_data_view, name='fetch_data'),
]

