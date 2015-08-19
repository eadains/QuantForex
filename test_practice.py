import threading
from data.streaming import DataStream
from execution.execution import OandaExecution
from portfolio.portfolio import Portfolio
from riskhandler.riskhandlers import DefaultTestHandler
from strategy.strategies import TestStrategy
import Queue as queue
from settings import ACCESS_TOKEN, ACCOUNT_ID

def trade(execution, portfolio, risk, strategy, events):

    while True:
        try:
            event = events.get(False)
        except queue.Empty:
            pass
        else:
            if event.type == "TICK":
                strategy.calculate_signals(event)
                portfolio.update_portfolio(event)
            elif event.type == "SIGNAL":
                risk.size_position(event)
            elif event.type == "ORDER":
                execution.execute_order(event)

if __name__ == "__main__":

    events = queue.Queue()
    pairs = ['EURUSD']
    stream = DataStream("practice", ACCESS_TOKEN, ACCOUNT_ID, pairs, events)
    execution = OandaExecution("practice", ACCESS_TOKEN, ACCOUNT_ID)
    portfolio = Portfolio(DataStream, events)
    risk = DefaultTestHandler(portfolio, events)
    strategy = TestStrategy(events)

    trade_thread = threading.Thread(
        target=trade, args=(execution, portfolio, risk, strategy, events))
    price_thread = threading.Thread(target=stream.stream_to_queue, args=[])

    trade_thread.start()
    price_thread.start()