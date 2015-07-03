


class Portfolio(object):

    """
    Class that stores and manages positions.
    Aims to replicate Oanda's positions as closely
    as possible.
    """

    def __init__(
        self, data_stream, events_queue, home_currency="USD", 
        leverage=20, equity=Decimal("100000.0"), bactest=None
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