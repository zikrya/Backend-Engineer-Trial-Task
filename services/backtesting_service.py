from decimal import Decimal
from stocks_app.models import StockData
import pandas as pd
from services.financial_data_service import FinancialDataService
import logging

logger = logging.getLogger(__name__)

class BacktestingService:
    @staticmethod
    def calculate_moving_average(data, window, column_name):
        data[column_name] = data['close_price'].rolling(window=window).mean()
        return data

    @staticmethod
    def run_backtest(symbol, initial_investment, short_window=50, long_window=200):
        stock_data = StockData.objects.filter(stock_symbol=symbol)

        if not stock_data.exists():
            logger.info(f"No data found for {symbol}. Fetching stock data.")
            FinancialDataService.fetch_stock_data(symbol)
            stock_data = StockData.objects.filter(stock_symbol=symbol)

        if not stock_data.exists():
            logger.error(f"No data available for backtesting for {symbol}.")
            return {
                "error": f"No data available for backtesting for {symbol}."
            }

        data = pd.DataFrame(list(stock_data.values('date', 'close_price')))
        data.set_index('date', inplace=True)
        data['close_price'] = data['close_price'].astype(float)

        if len(data) < long_window:
            logger.error(f"Not enough data to run the backtest for {symbol}.")
            return {
                "error": f"Not enough data to run the backtest for {symbol}."
            }

        data = BacktestingService.calculate_moving_average(data, short_window, 'short_ma')
        data = BacktestingService.calculate_moving_average(data, long_window, 'long_ma')

        investment = Decimal(initial_investment)
        position = 0
        cash = Decimal(investment)
        shares_held = Decimal(0)
        trade_count = 0
        max_drawdown = Decimal(0)
        peak_value = Decimal(investment)

        for i in range(long_window, len(data)):
            short_ma = Decimal(data.iloc[i]['short_ma'])
            long_ma = Decimal(data.iloc[i]['long_ma'])

            if position == 0 and short_ma < long_ma:
                shares_held = cash / Decimal(data.iloc[i]['close_price'])
                cash = Decimal(0)
                position = 1
                trade_count += 1
                logger.info(f"Buying {shares_held} shares at {data.iloc[i]['close_price']} on {data.index[i]}")

            elif position == 1 and short_ma > long_ma:
                cash = shares_held * Decimal(data.iloc[i]['close_price'])
                shares_held = Decimal(0)
                position = 0
                trade_count += 1
                logger.info(f"Selling shares at {data.iloc[i]['close_price']} on {data.index[i]}")

            current_value = cash + shares_held * Decimal(data.iloc[i]['close_price'])
            if current_value > peak_value:
                peak_value = current_value
            drawdown = (peak_value - current_value) / peak_value
            if drawdown > max_drawdown:
                max_drawdown = drawdown

        final_value = cash + shares_held * Decimal(data.iloc[-1]['close_price'])
        total_return = (final_value - investment) / investment * 100

        summary = {
            'symbol': symbol,
            'initial_investment': float(initial_investment),
            'final_value': float(final_value),
            'total_return': float(total_return),
            'max_drawdown': float(max_drawdown),
            'trades_executed': trade_count,
        }

        logger.info(f"Backtest completed for {symbol}: {summary}")
        return summary
