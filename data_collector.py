# data_collector.py
import requests
import pandas as pd
import logging
from config import ALPHA_VANTAGE_API_KEY

logger = logging.getLogger(__name__)

def fetch_stock_data(symbol, outputsize="compact"):
    """
    Fetch daily stock data for the given symbol using Alpha Vantage.
    """
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY,
        "outputsize": outputsize
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        if "Time Series (Daily)" not in data:
            error_message = f"Error fetching data for {symbol}: {data.get('Error Message', data)}"
            logger.error(error_message)
            raise Exception(error_message)
        
        ts_data = data["Time Series (Daily)"]
        # Convert dictionary to DataFrame
        df = pd.DataFrame.from_dict(ts_data, orient="index")
        df = df.rename(columns={
            "1. open": "open",
            "2. high": "high",
            "3. low": "low",
            "4. close": "close",
            "5. volume": "volume"
        })
        df.index = pd.to_datetime(df.index)
        df = df.sort_index()
        df = df.astype({"open": float, "high": float, "low": float, "close": float, "volume": float})
        logger.info(f"Successfully fetched data for {symbol}")
        return df
    except Exception as e:
        logger.exception(f"Failed to fetch stock data for {symbol}: {e}")
        raise
