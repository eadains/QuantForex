from data.streaming import HistoricPriceHandler
from strategy.strategies import TestStrategy
from portfolio.portfolio import Portfolio
from riskhandler.riskhandlers import DefaultTestHandler
from execution.execution import BacktestHandler
from backtest.backtest import Backtest

backtest = Backtest(['EURUSD'], ('2014-01-01', '2014-01-01'),
    HistoricPriceHandler, TestStrategy, Portfolio, DefaultTestHandler,
    BacktestHandler, 100000)

backtest.do_backtest()