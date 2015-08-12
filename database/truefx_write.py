import pandas as pd
from sqlalchemy import create_engine


def write_data(csv_dir):
    dataframe = pd.read_csv(csv_dir, header=None)
    dataframe = dataframe.replace("EUR/USD", value=1)
    dataframe.insert(0, "data_provider_id", value=1)
    dataframe.columns = ["data_provider_id", "symbol_id", "date_time", "bid", "ask"]
    def test(row):
        unmodified = row["date_time"]
        modified = unmodified[:4] + '-' + unmodified[4:6] + '-' + unmodified[6:]
        return modified
    dataframe["date_time"] = dataframe.apply(test, axis=1)
    engine = create_engine("mysql+mysqldb://root:Slimjoewilly12@localhost:3306/price_data")
    dataframe.to_sql(con=engine, name='ticks', if_exists='replace', chunksize=10000)

if __name__ == "__main__":
    write_data("/home/eadains/Data/EURUSD-2014-01.csv")
