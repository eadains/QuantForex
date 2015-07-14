from riskhandler.riskhandler import RiskHandlerBase


class DefaultTestHandler(RiskHandlerBase):

    """
    Test Risk Handler. Simply returns sized position
    as 2 percent of current account equity.
    """

    def __init__(self, portfolio):

        self.equity = portfolio.equity

    def size_position(self, signal_event):

        