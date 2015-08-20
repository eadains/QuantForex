from executionbase import ExecutionHandler
import requests


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


class OandaExecution(ExecutionHandler):

    """
    Executes order with oandas using
    provided account ID and access
    token information.
    """

    def __init__(self, api_source, access_token, account_id, portfolio):

        self.portfolio = portfolio
        self.access_token = access_token
        self.account_id = account_id
        if api_source == "practice":
            self.api_source = "https://api-fxpractice.oanda.com/v1/accounts/%s/orders" % account_id
        elif api_source == "live":
            self.api_source = "https://api-fxtrade.oanda.com/v1/accounts/%s/orders" % account_id
        self.session = requests.Session()
        self.session.headers.update({'Authorization': 'Bearer ' + self.access_token})

    def adjust_portfolio(self, order_event):

        """
        Adjusts local portfolio positions.
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

    def execute_order(self, order_event):

        encoded_pair = "%s_%s" % (order_event.instrument[:3], order_event.instrument[3:])
        order = {'instrument': encoded_pair, 'units': int(order_event.units),
                 'side': order_event.side, 'type': order_event.order_type}
        try:
            self.session.post(self.api_source, data=order)
            print "%s order for %d units of %s executed." % (order_event.side, order_event.units, order_event.instrument)
        except Exception as exception:
            print "Exception when trying to execute order: " + str(exception)
        self.adjust_portfolio(order_event)
