from strategy.strategybase import StrategyBase
from event.event import SignalEvent


class TestStrategy(StrategyBase):

    """
    Simply randomly chooses long or short
    after 5 tick events are recieved.
    """

    def __init__(self, events_queue):
        self.events_queue = events_queue
        self.ticks = 0
        self.invested = False

    def calculate_signals(self, tick_event):
        currency_pair = tick_event.instrument
        time = tick_event.time
        if self.ticks % 5 == 0:
            if self.invested == False:
                signal = SignalEvent(currency_pair, "market", "buy", time)
                self.events_queue.put(signal)
                self.invested = True
            elif self.invested == True:
                signal = SignalEvent(currency_pair, "market", "sell", time)
                self.events_queue.put(signal)
                self.invested = False
        self.ticks += 1
