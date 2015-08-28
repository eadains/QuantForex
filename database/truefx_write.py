import pandas as pd
from sqlalchemy import create_engine
import os


def write_data(csv_dir, currency_pair):

    """
    Writes csv files for TrueFx to database.
    Very rudimentary.
    Will be made more dynamic in future.
    """
    for file in os.listdir(csv_dir):

        filedir = csv_dir + "/" + file
        dataframe = pd.read_csv(filedir, header=None)
        dataframe = dataframe.replace(currency_pair, value=1)
        dataframe.insert(0, "data_provider_id", value=1)
        dataframe.columns = ["data_provider_id", "symbol_id", "date_time", "bid", "ask"]

        def parse_date(row):
            unmodified = row["date_time"]
            modified = unmodified[:4] + '-' + unmodified[4:6] + '-' + unmodified[6:]
            return modified
        dataframe["date_time"] = dataframe.apply(parse_date, axis=1)
        engine = create_engine("mysql+mysqldb://root:Slimjoewilly12@localhost:3306/price_data")
        dataframe.to_sql(con=engine, name='ticks', if_exists='replace', chunksize=10000)
