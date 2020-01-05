from abc import ABC, abstractmethod

import alpaca_trade_api as tradeapi

from mobile_app.utils import get_logger

logger = get_logger()

# API_KEY = "PKWUCDMU2A1SA1FMCWZC"
# API_SECRET = "QFGAo52OvuE3vC8bI86J8Hy8cfXHlV0GTztDDPaB"
ALPACA_API_BASE_URL = "https://paper-api.alpaca.markets"


class Trade(ABC):
    @abstractmethod
    def list_orders(self, *args, **kwargs):
        pass

    @abstractmethod
    def buy_order(self, *args, **kwargs):
        pass

    @abstractmethod
    def sell_order(self, *args, **kwargs):
        pass


class StocksTrading(Trade):
    def __init__(self, api_key, api_secret):
        self.trade_api = tradeapi.REST(api_key, api_secret, ALPACA_API_BASE_URL,
                                       api_version='v2')

    def list_orders(self, *args, **kwargs):
        for order in self.trade_api.list_positions():
            yield order.symbol

    def buy_order(self, symbol, quantity):
        self.trade_api.submit_order(
            symbol=symbol, qty=quantity,
            side='buy', type='market',
            time_in_force='gtc')
        logger.info("Buy order for %s with quantity %s is submitted", symbol,
                    quantity)

    def sell_order(self, symbol, quantity):
        self.trade_api.submit_order(
            symbol=symbol, qty=quantity,
            side='buy', type='market',
            time_in_force='gtc')
        logger.info("Sell order for %s with quantity %s is submitted", symbol,
                    quantity)

    def get_account(self):
        return self.trade_api.get_account()