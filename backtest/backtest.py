import Queue as queue
import pandas as pd
from settings import OUTPUT_RESULTS_DIR


class Backtest(object):

    """
    Class object for conducting a backtest.
    """

    def __init__(
        self, pairs, dates, price_handler,
        strategy, portfolio, risk, execution, equity
    ):

        self.pairs = pairs
        self.events = queue.Queue()
        self.dates = dates
        self.prices = price_handler(self.pairs, self.events, self.dates)
        self.strategy = strategy(self.events)
        self.portfolio = portfolio(self.prices, self.events, equity=equity)
        self.risk = risk(self.portfolio, self.events)
        self.execution = execution(self.portfolio)

    def _run_backtest(self):

        equity_data = pd.DataFrame(columns=['DateTime', 'Equity'])
        print "Running backtest now..."
        while self.prices.continue_backtest == True:
            try:
                event = self.events.get(False)
            except queue.Empty:
                self.prices.stream_tick()
            else:
                if event.type == 'TICK':
                    self.strategy.calculate_signals(event)
                    self.portfolio.update_portfolio(event)
                    equity_data = equity_data.append(
                        {'DateTime': event.time, 'Equity': self.portfolio.equity},
                        ignore_index=True)
                    print event.time
                elif event.type == 'SIGNAL':
                    self.risk.size_position(event)
                elif event.type == 'ORDER':
                    self.execution.execute_order(event)
        equity_data.to_csv(OUTPUT_RESULTS_DIR)

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
        # self._output_performance()
        print "Backtest complete"
