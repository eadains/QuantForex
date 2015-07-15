from riskhandler.riskhandlerbase import RiskHandlerBase
from event.event import OrderEvent
import Decimal


class DefaultTestHandler(RiskHandlerBase):

    """
    Test Risk Handler. Simply returns sized position
    as 2 percent of current account equity.
    """

    def __init__(self, portfolio, queue):

        self.equity = portfolio.equity
        self.queue = queue

    def size_position(self, signal_event):

        """
        Takes information from signal event,
        and creates an order event with the
        proper currency pair and units.
        """
        currency_pair = signal_event.instrument
        units = self.equity * Decimal("0.02")
        order_type = signal_event.order_type
        side = signal_event.side
        order = OrderEvent(currency_pair, units, order_type, side)
        self.queue.put(order)
