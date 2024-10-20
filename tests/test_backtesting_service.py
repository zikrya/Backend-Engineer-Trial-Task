from django.test import TestCase
from stocks_app.models import StockData
from services.backtesting_service import BacktestingService
import factory

class StockDataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StockData

    stock_symbol = 'AAPL'
    date = factory.Faker('date')
    open_price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    close_price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    high_price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    low_price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    volume = factory.Faker('random_int', min=1000, max=1000000)

class BacktestingServiceTest(TestCase):

    def setUp(self):
        StockDataFactory.create_batch(300, stock_symbol='AAPL')

    def test_backtest_success(self):
        result = BacktestingService.run_backtest('AAPL', initial_investment=10000)
        self.assertIn('total_return', result)
        self.assertIn('max_drawdown', result)
        self.assertIn('trades_executed', result)

    def test_backtest_insufficient_data(self):
        StockData.objects.all().delete()
        StockDataFactory.create_batch(100, stock_symbol='AAPL')

        result = BacktestingService.run_backtest('AAPL', initial_investment=10000)
        self.assertEqual(result['error'], "Not enough data to run the backtest for AAPL.")
