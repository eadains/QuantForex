import Queue as queue


class Backtest(object):

    """
    Class object for conducting a backtest.
    """

    def __init__(
        self, pairs, dates, price_handler,
        strategy, portfolio, risk, execution, equity
    ):

        self.pairs = pairs
        self.queue = queue.Queue()
        self.dates = dates
        self.prices = price_handler(self.pairs, self.queue, self.dates)
        self.strategy = strategy(self.queue)
        self.portfolio = portfolio(self.prices, self.queue, equity=equity)
        self.risk = risk(self.portfolio, self.queue)
        self.exection = execution(self.portfolio)

    def _run_backtest(self):

        print "Running backtest now..."
        while self.prices.continue_backtest == True:
            try:
                event = self.queue.get(False)
            except queue.Empty:
                self.prices.stream_tick()
            else:
                if event.type == 'TICK':
                    self.strategy.calculate_signals(event)
                    self.portfolio.update_portfolio(event)
                elif event.type == 'SIGNAL':
                    self.risk.size_position(event)
                elif event.type == 'ORDER':
                    self.execution.execute_order(event)

    def _output_performance(self):

        """
        Outputs performance stats of the backtest
        """

        # Implement after performance stuff is done

    def do_backtest(self):

        """
        Calls the above functions to
        do a backtest and output the results.
        """

        self._run_backtest()
        self._output_performance()
        print "Backtest complete"
