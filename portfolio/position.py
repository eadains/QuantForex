import Decimal, ROUND_HALF_DOWN


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
        self.profit_base = self.calculate_profit()
        self.profit_percentage = self.profit_percentage()

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
        # Creating reciprocal qoute to have position exposure in your home currency
        self.reciprocal_qoute = "%s%s" % (self.qoute_currency, self.base_currency)
        # Fetching currency price of the currency pair
        self.pair_price = self.data_stream.prices[self.currency_pair]
        # Settings baseline average cost basis and current price
        if self.side == "long":
            self.avg_price = Decimal(str(self.pair_price["ask"]))
            self.cur_price = Decimal(str(self.pair_price["bid"]))
        elif self.side == "short":
            self.avg_price = Decimal(str(self.pair_price["bid"]))
            self.cur_price = Decimal(str(self.pair_price["ask"]))

    def calculate_pips(self):

        """
        Calculates current profit/loss in pips
        cur_price - avg_price multiplied by 1 or -1
        depending on if the position is long or short
        """

        if self.side == "long":
            multiplier = Decimal("1")
        elif self.side == "short":
            multiplier = Decimal("-1")
        # Calculating pips
        pips = (multiplier * (self.cur_price - self.avg_price)).quantize(
            Decimal("0.00001"), ROUND_HALF_DOWN
        )
        return pips

    def calculate_profit(self):

        """
        Calculates profit/loss of the position in your home currency
        pips * reciprocal currency qoute * position units
        """

        pips = self.calculate_pips()
        # Getting price information for reciprocal qoute
        reciprocal_price = self.data_stream.prices[self.reciprocal_qoute]
        # Getting proper bid/ask depending on position side
        if self.side == "long":
            reciprocal_close = reciprocal_price["ask"]
        elif self.side == "short":
            reciprocal_close = reciprocal_price["bid"]
        profit = (pips * reciprocal_close * self.units).quantize(
            Decimal("0.00001"), ROUND_HALF_DOWN
        )
        return profit

    def profit_percentage(self):

        """
        Calculates percentage profit on the position
        (profit_base / units) * 100
        """

        percentage = ((self.profit_base / self.units) * Decimal("100.0")).quantize(
            Decimal("0.00001"), ROUND_HALF_DOWN
        )
        return percentage

    def update_position(self):

        """
        Updates profit_base, profit_percentage,
        and current pair price
        """

        if self.side == "long":
            self.cur_price = self.pair_price["bid"]
        elif self.side == "short":
            self.cur_price = self.pair_price["ask"]
        self.profit_base = self.calculate_profit()
        self.profit_percentage = self.profit_percentage()

    def add_units(self, units):

        """
        Function to add units to the position
        Updates average cost basis and number of units.
        """

        if self.side == "long":
            add_price = self.pair_price["ask"]
        elif self.side == "short":
            add_price = self.pair_price["bid"]
        new_total_units = self.units + units
        new_total_cost = (self.avg_price * self.units) + (add_price * units)
        self.avg_price = new_total_cost / new_total_units
        self.units = new_total_units
        self.update_position()

    def remove_units(self, units):

        """
        Function to removed units from the position
        Updates