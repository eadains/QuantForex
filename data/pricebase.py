from decimal import Decimal, getcontext, ROUND_HALF_DOWN


class PriceHandler(object):

    """
    Base class to provide common functions to all price handlers
    Any derivatives of this class should serve to output a tick event
    to the events queue.
    """

    def setup_prices_dict(self):

        """
        Sets up a dictionary to store price information.
        Will create a key not only for the given currency pair,
        but also it's recirocal.
        Ex: "GBPUSD" and "USDGBP" will be in the dictionary
        """

        prices_dict = dict(
            (k, v) for k, v in [(p, {"bid": None, "ask": None, "time": None}) for p in self.pairs]
        )

        inv_prices_dict = dict(
            (k, v) for k, v in [("%s%s" % (p[3:], p[:3]), {"bid": None, "ask": None, "time": None}) for p in self.pairs]
        )

        prices_dict.update(inv_prices_dict)
        return prices_dict

    def invert_prices(self, pair, bid, ask):

        """
        Inverts the given currency pair.
        Ex: "GBPUSD" and its associated bid/ask will be turned info
            "USDGBP" with proper bid/ask
        """

        getcontext().rounding = ROUND_HALF_DOWN
        inv_pair = "%s%s" % (pair[3:], pair[:3])
        inv_bid = (Decimal("1.0")/bid).quantize(
            Decimal("0.00001")
        )
        inv_ask = (Decimal("1.0")/ask).quantize(
            Decimal("0.00001")
        )
        return inv_pair, inv_bid, inv_ask
