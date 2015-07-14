# General Plan:
# Needs to accept a signal event and return an order event.
# Needs to get current positions from portfolio and
# size order given that information


class RiskHandler(object):

    """
    Class to receive signal events.
    Uses current position information, as given
    by the Portfolio given to size orders.
    """

    def __init__(
        self, portfolio, risk_scheme
            ):  # TODO: Potentially add parameters related to risk management

        """
        Add doc
        """

        self.portfolio = portfolio

    def get_positions(self):

        """
        Gets currently open positions from
        given Portfolio object.
        Creates dictionary:
        {currency_pair : units}
        """
        # UNTESTED:::
        units_dict = {}
        for key, value in self.portfolio.positions.iteritems():
            self.units_dict.update({key: value.units})
        return units_dict

    def size_position(self, signal_event):

        """
        Calls get_positions to determine position size,
        given the side and currency pair by the signal
        event.
        Returns an order event.
        """

        positions = self.get_positions()
