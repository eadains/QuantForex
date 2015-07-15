import abc


class RiskHandlerBase(object):

    """
    Abstract base Class to be subclassed by risk handling
    classes. Provides basic functionality and abstract
    size_position function.
    """

    __metaclass__ = abc.ABCMeta

    def get_positions(self, portfolio):

        """
        Gets currently open positions from
        given Portfolio object.
        Creates dictionary:
        {currency_pair : units}
        """
        # UNTESTED:::
        units_dict = {}
        for key, value in portfolio.positions.iteritems():
            units_dict.update({key: value.units})
        return units_dict

    @abc.abstractmethod
    def size_position(self, signal_event):

        """
        Calls get_positions to determine position size,
        given the side and currency pair by the signal
        event.
        Returns an order event.
        """

        return
