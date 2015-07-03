from data.pricebase import PriceHandler
import requests
import json
from decimal import Decimal, getcontext, ROUND_HALF_DOWN
from event.event import TickEvent


class DataStream(PriceHandler):

    """
    Instantiates an object that will stream forex data
    from Oanda's API.
    """

    def __init__(self, api_source, access_token, account_id, pairs, events_queue):

        """
        api_source = "practice" or "live" used to determine proper URL
        access_token = access token given by Oanda
        account_id = id of your oanda account_id
        pairs = list of pairs you want to get price information for
        events_queue = Queue() object that you want to put tick events on
        """

        self.api_source = api_source
        self.access_token = access_token
        self.account_id = account_id
        self.pairs = pairs
        self.events_queue = events_queue
        self.prices_dict = self.setup_prices_dict()

    def connect_to_stream(self):

        """
        Establishes a connection with Oanda API. URL is changed depending
        on api_source.
        join() is required in params because OANDA API requires currency pairs
        to be seperated by URL-encoded commas.
        """

        encoded_pairs = ["%s_%s" % (p[:3], p[3:]) for p in self.pairs]
        try:
            session = requests.Session()
            if self.api_source == "practice":
                url = "https://stream-fxpractice.oanda.com/v1/prices"
            elif self.api_source == "live":
                url = "https://stream-fxtrade.oanda.com/v1/prices"
            headers = {'Authorization': 'Bearer ' + self.access_token}
            params = {'instruments': ','.join(encoded_pairs), 'accountId': self.account_id}
            response = session.get(url, headers=headers, params=params, stream=True)
            return response
        except Exception as excep:
            session.close()
            print "Exception when connecting to stream: " + str(excep)

    def stream_to_queue(self):

        """
        Calls the above connect_to_stream function, updates the prices dictionary,
        and then adds a Tick event to the supplied queue.
        """

        response = self.connect_to_stream()
        if response.status_code != 200:
            print "connect_to_stream did not return expected"
            return
        for line in response.iter_lines(1):
            if line:
                try:
                    decode_line = line.decode('utf-8')
                    data = json.loads(decode_line)
                except Exception as excep:
                    print "Exception when trying to decode response: " + str(excep)
                if ("instrument" in data) or ("tick" in data):
                    print data
                    getcontext().rounding = ROUND_HALF_DOWN
                    # Getting data from JSON response
                    instrument = data["tick"]["instrument"].replace("_", "")
                    time = data["tick"]["time"]
                    bid = Decimal(str(data["tick"]["bid"])).quantize(
                        Decimal("0.00001")
                    )
                    ask = Decimal(str(data["tick"]["bid"])).quantize(
                        Decimal("0.00001")
                    )
                    # Setting prices in dictionary
                    self.prices[instrument]["bid"] = bid
                    self.prices[instrument]["ask"] = ask
                    self.prices[instrument]["time"] = time
                    # Gettings inverted currency pairs
                    inv_pair, inv_bid, inv_ask = self.invert_price(instrument, bid, ask)
                    self.prices[inv_pair]["bid"] = inv_bid
                    self.prices[inv_pair]["ask"] = inv_ask
                    self.prices[inv_pair]["time"] = time
                    # Putting tick event on queue
                    tick_event = TickEvent(instrument, bid, ask, time)
                    self.events_queue.put(tick_event)


class HistoricCSVPriceHandler(PriceHandler):

    """
    Imports price data from CSV files and puts tick events
    onto the queue.
    """

    def __init__(self, pairs, events_queue, csv_dir):

        """
        pairs = pairs 