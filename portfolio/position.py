

class Position(object):

    """
    Object that represents a long/short position in a currency.
    Tries to replicate Oanda's position statistics as closely
    as possible.
    """

    def __init__(
        self, home_currency, side,
        currency_pair, units, data_stream
    ):

        """
        home_currency = account currnecy to qoute exposure in
        side = "long" or "short"
        currency_pair = currency pair being traded
        units = currency units long/short
        data_stream = data streaming object. Must be subclass of PriceHandler
        """

        self.home_currency = home_currency
        self.side = side
        self.currency_pair = currency_pair
        self.units = units
        self.data_stream = data_stream
        self.setup_currencies()

    def setup_currencies(self):

        """
        Sets position qoute currency and base currency.
        Also sets home currency qoute.
        Sets currenct price for position currency pair,
        and sets a baseline value for the positions average
        cost basis.
        """

        # Left side of qoute. Currency being used to trade qoute currency
        self.base_currency = self.currency_pair[:3]
        # Right side of qoute. Currency being bought/sold
        self.qoute_currency = self.currency_pair[3:]
        # The below is to account for different profit calculations depending
        # on the pair you are trading and your home currency.
        if self.base_currency != self.home_currency:
            self.home_currency_qoute = "%s%s" % (self.home_currency, self.base_currency)
        elif self.base_currency == self.home_currency:
            self.home_currency_qoute = "%s%s" % (self.qoute_currency, self.home_currency)
