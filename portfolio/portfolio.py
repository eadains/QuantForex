import Decimal
from portfolio.position import Position


class Portfolio(object):

    """
    Class that stores and manages positions.
    Aims to replicate Oanda's positions as closely
    as possible.
    """

    def __init__(
        self, data_stream, events_queue, home_currency="USD",
        leverage=20, equity=Decimal("100000.0"), backtest=None
        ):

        """
        data_stream = Streaming object. Object must be subclassed from PriceHandler
        events_queue = Queue() object to fetch/put events from
        home_currency = Account currency. All position exposure will be qouted in this currency
        # TODO: fetch leverage from API
        leverage = leverage of the account
        # TODO: fetch equity from API
        equity = account equity
        backtest = supply a backtest object if Portfolio is being used in a backtest
        """

        self.data_stream = data_stream
        self.events_queue = events_queue
        self.home_currency = home_currency
        self.leverage = leverage
        self.equity = equity
        self.backtest = backtest
        self.positions = {}
        if self.backtest:
            self.backtest_file = self.backtest.backtest_file_dir

    def add_new_position(self, side, currency_pair, units):

        """
        Adds new position into positions dictionary.
        side = "long" or "short"
        currency_pair = currency pair being traded
        units = number of currency units long/short
        """

        position = Position(
            self.home_currency, side, currency_pair,
            units, self.data_stream
        )
        self.positions[currency_pair] = position

    def add_position_units(self, currency_pair, units):

        """
        Adds units to an exsisting Position,
        denoted by the currency_pair
        """

        if currency_pair not in self.positions:
            return False
        else:
            position = self.positions[currency_pair]
            position.add_units(units)
            return True

    def remove_position_units(self, currency_pair, units):

        """
        Removes units from an existing Position,
        denoted by currency_pair
        """

        if currency_pair not in self.positions:
            return False
        else:
            position = self.positions[currency_pair]
            pnl = position.remove_units(units)
            self.balance += pnl
            return True

    def close_position(self, currency_pair):

        """
        Closes exsiting position,
        as denoted by currency_pair
        """

        if currency_pair not in self.positions:
            return False
        else:
            position = self.positions[currency_pair]
            pnl = position.close_position()
            self.balance += pnl
            del[self.positions[currency_pair]]
            return True

    def update_portfolio(self, tick_event):

        """
        Updates portfolio, ensuring up-to-date profit/loss
        Tick Event: An event of the tick class,
            supplied by the events queue.
        """

        currency_pair = tick_event.instrument
        if currency_pair in self.positions:
            position = self.positions[currency_pair]
            position.update_position()
