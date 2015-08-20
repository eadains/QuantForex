class Event(object):
    pass


class TickEvent(Event):

    """
    Event object that contains tick data.

    Instrument = Instrument price data is for
    Bid = Bid price
    Ask = Ask price
    time = time event was created
    """

    def __init__(self, instrument, bid, ask, time):
        self.type = 'TICK'
        self.instrument = instrument
        self.bid = bid
        self.ask = ask
        self.time = time


class SignalEvent(Event):

    """
    Event object that contains Long or Short.
    Created by a trading strategy.

    Instrument = instrument to be traded
    Order Type = Market/Limit/stop/etc.
    Side = 'buy' or 'sell'
    time = time event was created
    """

    def __init__(self, instrument, order_type, side, time):
        self.type = 'SIGNAL'
        self.instrument = instrument
        self.order_type = order_type
        self.side = side
        self.time = time


class OrderEvent(Event):

    """
    Event object that contains information required
    for the exectution handler.

    Instrument = Instrument to be traded
    units = units to be bought or sold
    order type = Market/limit/stop/etc.
    side = 'buy' or 'sell'
    """

    def __init__(self, instrument, units, order_type, side):
        self.type = 'ORDER'
        self.instrument = instrument
        self.units = units
        self.order_type = order_type
        self.side = side
