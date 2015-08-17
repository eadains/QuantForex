from executionbase import ExecutionHandler


class BacktestHandler(ExecutionHandler):

    """
    Execution Handler that just updates positions
    in the portfolio. Does not send orders to
    any exchange.
    """

    def __init__(self, portfolio):

        self.portfolio = portfolio

    def execute_order(self, order_event):

        """
        Function for executing given
        order event.
        """

        currency_pair = order_event.instrument
        units = order_event.units
        side = order_event.side

        if currency_pair not in self.portfolio.positions:
            self.portfolio.add_new_position(side, currency_pair, units)

        else:
            position = self.portfolio.positions[currency_pair]

            if side == "long" and position.side == "long":
                self.portfolio.add_position_units(currency_pair, units)

            elif side == "short" and position.side == "long":
                if units == position.units:
                    self.portfolio.close_position(currency_pair)
                elif units > position.units:
                    new_order_units = units - position.units
                    self.portfolio.close_position(currency_pair)
                    self.portfolio.add_new_position("short", currency_pair, new_order_units)
                elif units < position.units:
                    self.portfolio.remove_units(currency_pair, units)

            elif side == "long" and position.side == "short":
                if units == position.units:
                    self.portfolio.close_position(currency_pair)
                elif units > position.units:
                    new_order_units = units - position.units
                    self.portfolio.close_position(currency_pair)
                    self.portfolio.add_new_position("long", currency_pair, new_order_units)
                elif units < position.units:
                    self.portfolio.remove_position_units(currency_pair, units)

            elif side == "short" and position.side == "short":
                self.portfolio.add_position_units(currency_pair, units)
