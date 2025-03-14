# database.py
from influxdb_client import InfluxDBClient, Point, WriteOptions
from config import INFLUXDB_URL, INFLUXDB_TOKEN, INFLUXDB_ORG, INFLUXDB_BUCKET
import logging

logger = logging.getLogger(__name__)

# Create a client instance with batching options
client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = client.write_api(write_options=WriteOptions(batch_size=500, flush_interval=10_000))
query_api = client.query_api()

def write_stock_data(symbol, df):
    """
    Writes the stock data to InfluxDB.
    Each row in the DataFrame is stored as a point.
    """
    try:
        for index, row in df.iterrows():
            point = (
                Point("stock")
                .tag("symbol", symbol)
                .field("open", row["open"])
                .field("high", row["high"])
                .field("low", row["low"])
                .field("close", row["close"])
                .field("volume", row["volume"])
                .time(index)
            )
            write_api.write(bucket=INFLUXDB_BUCKET, record=point)
        logger.info(f"Successfully wrote data for {symbol} to InfluxDB")
    except Exception as e:
        logger.exception(f"Failed to write data for {symbol} to InfluxDB: {e}")
        raise

def query_stock_data(symbol, start="-30d"):
    """
    Queries InfluxDB for historical stock data for a given symbol.
    Adjust the start time as needed.
    """
    try:
        query = f'''
        from(bucket: "{INFLUXDB_BUCKET}")
          |> range(start: {start})
          |> filter(fn: (r) => r["_measurement"] == "stock" and r["symbol"] == "{symbol}")
          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
          |> sort(columns: ["_time"])
        '''
        result = query_api.query_data_frame(query)
        if isinstance(result, list):
            df = result[0]
            for table in result[1:]:
                df = df.append(table)
        else:
            df = result
        for col in ["_result", "_start", "_stop"]:
            if col in df.columns:
                df.drop(columns=[col], inplace=True)
        logger.info(f"Successfully queried data for {symbol} from InfluxDB")
        return df
    except Exception as e:
        logger.exception(f"Failed to query data for {symbol} from InfluxDB: {e}")
        raise
