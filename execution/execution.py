from execution.executionbase import ExecutionHandler


class BactestHandler(ExecutionHandler):

    """
    Execution Handler that just updates positions
    in the portfolio. Does not send orders to
    any exchange.
    """
    