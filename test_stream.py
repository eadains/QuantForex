from data.streaming import DataStream
import Queue as queue
from settings import ACCESS_TOKEN, ACCOUNT_ID

events_queue = queue.Queue()
handler = DataStream("practice", ACCESS_TOKEN, ACCOUNT_ID, ['EURUSD'], events_queue)

while True:
    try:
        var = events_queue.get(False).time
    except queue.Empty:
        pass
    else:
        print var
