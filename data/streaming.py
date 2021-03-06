from data.pricebase import PriceHandler
import requests
import json
from decimal import Decimal, getcontext, ROUND_HALF_DOWN
from event.event import TickEvent
import sqlalchemy as sql
import pandas as pd


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

    def _connect_to_stream(self):

        """
        Establishes a connection with Oanda API. URL is changed depending
        on api_source.
        join() is required in params because OANDA API requires currency pairs
        to be seperated by URL-encoded commas.
        """

        # Reformating pairs list to be URL compatible
        encoded_pairs = ["%s_%s" % (p[:3], p[3:]) for p in self.pairs]
        try:
            session = requests.Session()
            # Setting URL to stream from
            if self.api_source == "practice":
                url = "https://stream-fxpractice.oanda.com/v1/prices"
            elif self.api_source == "live":
                url = "https://stream-fxtrade.oanda.com/v1/prices"
            # Setting relevant GET headers and setting parameters to append on the URL
            headers = {'Authorization': 'Bearer ' + self.access_token}
            params = {'instruments': ','.join(encoded_pairs), 'accountId': self.account_id}
            response = session.get(url, headers=headers, params=params, stream=True)
            # Running GET request
            return response
        except Exception as excep:
            session.close()
            print "Exception when connecting to stream: " + str(excep)

    def stream_to_queue(self):

        """
        Calls the above connect_to_stream function, updates the prices dictionary,
        and then adds a Tick event to the supplied queue.
        """

        response = self._connect_to_stream()
        if response.status_code != 200:
            print "connect_to_stream did not return expected"
            return
        for line in response.iter_lines(1):
            if line:
                try:
                    # Decoding and loading into JSON
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
                    self.prices_dict[instrument]["bid"] = bid
                    self.prices_dict[instrument]["ask"] = ask
                    self.prices_dict[instrument]["time"] = time
                    # Getting inverted currency pairs and setting their prices in the dictionary
                    inv_pair, inv_bid, inv_ask = self.invert_prices(instrument, bid, ask)
                    self.prices_dict[inv_pair]["bid"] = inv_bid
                    self.prices_dict[inv_pair]["ask"] = inv_ask
                    self.prices_dict[inv_pair]["time"] = time
                    # Putting tick event on queue
                    tick_event = TickEvent(instrument, bid, ask, time)
                    self.events_queue.put(tick_event)


class HistoricPriceHandler(PriceHandler):

    """
    Queries database for historical tick information
    """

    def __init__(self, pairs, events_queue, date_range):

        """
        pairs = list of pairs to get data for
        events_queue = Queue() object to put tick events on
        date_range = tuple containing the two dates to fetch data between
        """

        self.pairs = pairs
        self.events_queue = events_queue
        self.start_date = date_range[0]
        self.end_date = date_range[1]
        self.prices = self.setup_prices_dict()
        self.pair_frames = {}
        self.pair_data = self.get_data()
        self.continue_backtest = True

    def get_data(self):

        """
        Fetches data for all pairs, using start_date
        and end_date.
        Concatenates data for each pair into one
        data frame.
        """

        engine = sql.create_engine("mysql+mysqldb://root:Slimjoewilly12@localhost:3306/price_data")
        pair_frames = {}
        for p in self.pairs:
            select = sql.select(['id']).where("ticker = '%s'" % p).select_from('symbols')
            ticker_id = engine.execute(select).fetchone()[0]
            query = ("SELECT symbols.ticker, ticks.date_time, ticks.bid, ticks.ask FROM ticks INNER JOIN symbols on ticks.symbol_id = symbols.id "
                     "WHERE (symbol_id = '%s') AND (DATE(date_time) BETWEEN '%s' AND '%s')" % (str(ticker_id), self.start_date, self.end_date))
            pair_frames[p] = pd.read_sql_query(query, con=engine, index_col="date_time")
        return pd.concat(pair_frames.values()).sort().iterrows()

    def stream_tick(self):

        """
        Puts next piece of price information onto
        the event queue.
        """

        try:
            index, row = next(self.pair_data)
        except StopIteration:
            self.continue_backtest = False
            return
        pair = row["ticker"]
        bid = Decimal(str(row["bid"])).quantize(
            Decimal("0.00001")
        )
        ask = Decimal(str(row["ask"])).quantize(
            Decimal("0.00001")
        )

        # Create decimalised prices for traded pair
        self.prices[pair]["bid"] = bid
        self.prices[pair]["ask"] = ask
        self.prices[pair]["time"] = index

        # Create decimalised prices for inverted pair
        inv_pair, inv_bid, inv_ask = self.invert_prices(pair, bid, ask)
        self.prices[inv_pair]["bid"] = inv_bid
        self.prices[inv_pair]["ask"] = inv_ask
        self.prices[inv_pair]["time"] = index

        # Create the tick event for the queue
        tev = TickEvent(pair, bid, ask, index)
        self.events_queue.put(tev)
