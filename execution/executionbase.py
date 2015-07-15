import abc


class ExecutionHandler(object):

    """
    Abstract Base class for all execution handler.
    Every handler needs a execute_order function,
    as given here.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def execute_order(self):

        """
        Executes Order. Needs to add position
        to portfolio and sends order to
        exchange.
        """

        return
