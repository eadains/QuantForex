from data.streaming import HistoricPriceHandler
import Queue as queue

event_queue = queue.Queue()
handler = HistoricPriceHandler(['EURUSD'], event_queue, ('2014-01-01', '2014-01-01'))

while handler.continue_backtest == True:
    try:
        var = event_queue.get(False).time
    except queue.Empty:
        handler.stream_tick()
    else:
        print var