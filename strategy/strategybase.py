import abc


class StrategyBase(object):

    """
    Abstract base class for all strategy classes
    All inheritants need to put a signal event
    onto queue.
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def calculate_signals(self, tick_event):

        """
        Needs to accept tick event and
        put a signal event onto the queue
        """

        return
