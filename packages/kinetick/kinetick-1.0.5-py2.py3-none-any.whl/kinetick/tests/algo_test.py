import unittest

from kinetick.algo import Algo
from kinetick.enums import Timeframes


class AlgoTest(unittest.TestCase):
    def test_create_order(self):
        algo = Algo(
            # instruments=["NSEBANK"],
            instruments=["GAIL"],
            resolution=Timeframes.MINUTE_1,
            tick_window=1000,
            bar_window=1000,
            # preload="1D",
            # backtest=True,
            # output="/Users/vinaygoudapatil/Desktop/vinay/github/qtpylib/examples/orders.csv",
            start="2020-06-17 9:15:00",
            # backfill=True
        )
        symbol = algo.get_instrument("GAIL")
        direction = "LONG"
        quantity = 10
        try:
            algo.order(direction, symbol, quantity, order_type="",
                       limit_price=98, expiry=0, orderId=0, target=0,
                       initial_stop=0, trail_stop_at=0, trail_stop_by=0,
                       stop_limit=False, trail_stop_type='percent')
        except Exception as e:
            print(e)
