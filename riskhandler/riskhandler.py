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
        self, portfolio
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
            units_dict.update({key: value.units})
