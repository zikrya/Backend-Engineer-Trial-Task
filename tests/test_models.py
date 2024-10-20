from django.test import TestCase
from stocks_app.models import StockData, PredictionData
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

class PredictionDataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PredictionData

    stock_symbol = 'AAPL'
    date = factory.Faker('date')
    predicted_price = factory.Faker('pydecimal', left_digits=3, right_digits=2)

class ModelsTest(TestCase):

    def test_stock_data_creation(self):
        stock = StockDataFactory()
        self.assertIsNotNone(stock.id)
        self.assertEqual(stock.stock_symbol, 'AAPL')

    def test_prediction_data_creation(self):
        prediction = PredictionDataFactory()
        self.assertIsNotNone(prediction.id)
        self.assertEqual(prediction.stock_symbol, 'AAPL')
