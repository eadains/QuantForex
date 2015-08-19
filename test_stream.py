from data.streaming import DataStream
import Queue as queue
from settings import ACCESS_TOKEN, ACCOUNT_ID

events_queue = queue.Queue()
handler = DataStream("practice", ACCESS_TOKEN, ACCOUNT_ID, ['EURUSD'], events_queue)

handler.stream_to_queue()