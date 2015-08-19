from execution.execution import OandaExecution
from settings import ACCESS_TOKEN, ACCOUNT_ID
from event.event import OrderEvent

order_event = OrderEvent('EURUSD', 100, 'market', 'buy')
order_event_two = OrderEvent('EURUSD', 500, 'market', 'sell')
execution = OandaExecution("practice", ACCESS_TOKEN, ACCOUNT_ID)

execution.execute_order(order_event)
execution.execute_order(order_event_two)
